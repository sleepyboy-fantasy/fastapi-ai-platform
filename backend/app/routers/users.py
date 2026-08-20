from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from fastapi import HTTPException

from app.schemas.user import UserLogin

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
from app.core.security import (
    verify_password,
    create_access_token
)

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(
        user.password
    )


    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )


    db.add(db_user)
    db.commit()
    db.refresh(db_user)


    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(
            User.username == user.username
        )
        .first()
    )


    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )


    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Wrong password"
        )


    token = create_access_token(
        {
            "sub": db_user.username
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }
