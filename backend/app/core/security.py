from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from app.database import get_db
from app.models.user import User


# =========================
# 密码加密
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================
# JWT Token
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================
# OAuth2
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


# =========================
# 获取当前用户
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get(
            "sub"
        )

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    # =========================
    # 查询数据库中的用户
    # =========================

    user = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    # =========================
    # 检查用户是否被禁用
    # =========================

    if not user.is_active:

        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )


    return user


# =========================
# 获取当前用户名
# =========================

def get_current_username(
    current_user: User = Depends(get_current_user)
):

    return current_user.username