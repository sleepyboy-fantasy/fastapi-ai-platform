from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def search_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 5
):
    """
    根据问题搜索最相似的文档片段
    """

    # 1. 生成问题向量
    query_embedding = generate_embedding(query)


    # 2. 向量相似度查询
    results = (
        db.query(
            DocumentChunk,
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            ).label("distance")
        )
        .order_by(
            "distance"
        )
        .limit(top_k)
        .all()
    )


    # 3. 格式化返回
    chunks = []

    for chunk, distance in results:

        chunks.append(
            {
                "id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "distance": float(distance)
            }
        )


    return chunks