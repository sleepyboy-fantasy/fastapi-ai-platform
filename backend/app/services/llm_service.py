from openai import OpenAI

from app.core.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL
)


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)



def generate_answer(
    question: str,
    context: str
):

    response = client.chat.completions.create(

        model="deepseek-chat",

        messages=[

            {
                "role": "system",
                "content":
                """
你是一个企业知识库助手。

回答规则：
1. 只能根据提供的知识回答。
2. 如果知识不存在，不要编造。
3. 回答简洁准确。
"""
            },


            {
                "role": "user",
                "content":
                f"""
知识库内容：

{context}


用户问题：

{question}
"""
            }

        ],

        temperature=0.2

    )


    return (
        response
        .choices[0]
        .message
        .content
    )