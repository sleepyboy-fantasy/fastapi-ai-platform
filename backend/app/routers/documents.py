import os
import uuid

import fitz

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session
from app.services.hash_service import calculate_file_hash
from app.database import get_db

from app.core.security import get_current_username

from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.schemas.document import DocumentResponse

from app.services.document_service import create_document
from app.services.search_service import search_similar_chunks

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


# =========================
# 文件上传
# =========================

@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    file: UploadFile = File(...),
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):

    # =========================
    # 查询当前用户
    # =========================

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =========================
    # 检查用户状态
    # =========================

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )

    # =========================
    # 检查文件名
    # =========================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    # =========================
    # 获取文件扩展名
    # =========================

    original_filename = file.filename

    extension = os.path.splitext(
        original_filename
    )[1].lower()

    # =========================
    # 只允许 PDF 和 TXT
    # =========================

    allowed_extensions = {
        ".pdf",
        ".txt"
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )

    # =========================
    # 创建 uploads 目录
    # =========================

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    # =========================
    # 生成唯一文件名
    # =========================

    saved_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = os.path.join(
        upload_dir,
        saved_filename
    )

    # =========================
    # 保存文件
    # =========================

    with open(
        file_path,
        "wb"
    ) as buffer:

        while True:

            chunk = file.file.read(
                1024 * 1024
            )

            if not chunk:
                break

            buffer.write(chunk)

    # =========================
    # 计算文件hash
    # =========================

    file_hash = calculate_file_hash(
        file_path
    )    

    # =========================
    # 检查文件是否重复
    # =========================

    exist_document = (
        db.query(Document)
        .filter(
            Document.user_id == user.id,
            Document.file_hash == file_hash
        )
        .first()
    )


    if exist_document:

        # 删除刚保存的文件

        if os.path.exists(file_path):
            os.remove(file_path)


        raise HTTPException(
            status_code=400,
            detail="Document already exists"
        )

    # =========================
    # 读取文档内容
    # =========================

    content = None

    # =========================
    # TXT解析
    # =========================

    if extension == ".txt":

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as text_file:

                content = text_file.read()

        except UnicodeDecodeError:

            # 删除已经保存的文件
            if os.path.exists(file_path):
                os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail="TXT file must use UTF-8 encoding"
            )

    # =========================
    # PDF解析
    # =========================

    elif extension == ".pdf":

        try:

            pdf_document = fitz.open(
                file_path
            )

            text_parts = []

            for page in pdf_document:

                page_text = page.get_text()

                if page_text:
                    text_parts.append(
                        page_text
                    )

            pdf_document.close()

            content = "\n".join(
                text_parts
            )

        except Exception:

            # 删除解析失败的文件
            if os.path.exists(file_path):
                os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail="Failed to parse PDF file"
            )

    # =========================
    # 写入数据库
    # =========================

    document = create_document(
        db=db,
        user_id=user.id,
        filename=original_filename,
        file_path=file_path,
        file_type=extension,
        file_hash=file_hash,
        content=content
    )

    return document


# =========================
# 获取当前用户的文档列表（分页）
# =========================

@router.get("")
def get_documents(
    page: int = Query(
        1,
        ge=1
    ),

    page_size: int = Query(
        10,
        ge=1,
        le=100
    ),

    username: str = Depends(get_current_username),

    db: Session = Depends(get_db)
):


    # 查询用户

    user = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    if not user.is_active:

        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )


    # 总数量

    total = (
        db.query(Document)
        .filter(
            Document.user_id == user.id
        )
        .count()
    )


    # 分页查询

    documents = (
        db.query(Document)
        .filter(
            Document.user_id == user.id
        )
        .order_by(
            Document.created_at.desc()
        )
        .offset(
            (page - 1) * page_size
        )
        .limit(
            page_size
        )
        .all()
    )


    return {

        "page": page,

        "page_size": page_size,

        "total": total,

        "items": documents

    }


# =========================
# 获取单个文档
# =========================

@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
def get_document(
    document_id: int,
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):

    # =========================
    # 查询当前用户
    # =========================

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =========================
    # 检查用户状态
    # =========================

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )

    # =========================
    # 查询文档
    # =========================

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


# =========================
# 删除文档
# =========================

@router.delete(
    "/{document_id}"
)
def delete_document(
    document_id: int,
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):

    # =========================
    # 查询当前用户
    # =========================

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =========================
    # 检查用户状态
    # =========================

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )

    # =========================
    # 查询文档
    # =========================

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # =========================
    # 删除服务器上的文件
    # =========================

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # =========================
    # 删除文档对应的向量数据
    # =========================

    db.query(DocumentChunk)\
        .filter(
            DocumentChunk.document_id == document.id
        )\
        .delete()


    # =========================
    # 删除文档记录
    # =========================

    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted successfully",
        "id": document_id,
        "filename": document.filename
    }
# =========================
# 文档向量搜索
# =========================

@router.post(
    "/search"
)
def search_documents(
    query: str,
    top_k: int = 5,
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):

    # =========================
    # 查询当前用户
    # =========================

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    # =========================
    # 用户状态检查
    # =========================

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )


    # =========================
    # 向量搜索
    # =========================

    results = search_similar_chunks(
        db=db,
        query=query,
        top_k=top_k
    )


    return {
        "query": query,
        "results": results
    }