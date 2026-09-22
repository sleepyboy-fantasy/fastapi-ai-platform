from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database import get_db

from app.services.qa_service import ask_question


router = APIRouter(
    prefix="/qa",
    tags=["qa"]
)



@router.post("/ask")
def question(
    data: dict,
    db: Session = Depends(get_db)
):

    question = data["question"]


    result = ask_question(
        db,
        question
    )


    return {
        "question": question,
        **result
    }