from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.text_service import split_text

from app.services.embedding_service import generate_embedding

def create_document(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str,
    file_type: str,
    file_hash: str,
    content: str | None = None
):
    # =========================
    # 创建文档
    # =========================

    document = Document(
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_hash=file_hash,
        content=content
    )

    db.add(document)

    # =========================
    # 先提交文档
    # 获取 document.id
    # =========================

    db.commit()
    db.refresh(document)

    # =========================
    # 文档存在内容时进行 Chunk 切分
    # =========================

    if content:

        chunks = split_text(
            content,
            chunk_size=500,
            chunk_overlap=50
        )

        # =========================
        # 创建 DocumentChunk
        # =========================

        for index, chunk_content in enumerate(chunks):

            embedding = generate_embedding(
                chunk_content
            )

            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk_content,
                embedding=embedding
            )

            db.add(chunk)

        # =========================
        # 保存所有 Chunk
        # =========================

        db.commit()

    return document