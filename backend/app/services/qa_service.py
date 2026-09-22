from sqlalchemy.orm import Session

from app.services.search_service import search_similar_chunks
from app.services.llm_service import generate_answer


# 相似度阈值
# 越小代表越相似
DISTANCE_THRESHOLD = 0.5


def ask_question(
    db: Session,
    question: str
):

    # 1. 检索相关知识
    results = search_similar_chunks(
        db,
        question
    )


    # 2. 没有搜索结果
    if not results:
        return {
            "answer": "根据提供的知识库，没有相关信息，无法回答。",
            "sources": []
        }


    # 3. 判断最高相似度

    best_distance = results[0]["distance"]


    if best_distance > DISTANCE_THRESHOLD:

        return {

            "answer":
            "根据提供的知识库，没有关于该问题的信息，无法回答。",

            "sources": []

        }


    # 4. 拼接上下文

    context = "\n".join(
        [
            item["content"]
            for item in results
        ]
    )


    # 5. 调用大模型生成答案

    answer = generate_answer(
        question,
        context
    )


    return {

        "answer": answer,

        "sources": results

    }