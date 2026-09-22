from sqlalchemy.orm import Session

from app.models.user import User

from app.core.redis import redis_client

from app.core.security import (
    hash_password,
    verify_password
)


# =========================
# 根据用户名查询用户
# =========================

def get_user_by_username(
    db: Session,
    username: str
):

    return (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


# =========================
# 根据邮箱查询用户
# =========================

def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )


# =========================
# 创建用户
# =========================

def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
):

    hashed_password = hash_password(
        password
    )

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


# =========================
# 用户认证
# =========================

def authenticate_user(
    db: Session,
    username: str,
    password: str
):

    user = get_user_by_username(
        db,
        username
    )

    # 用户不存在
    if not user:
        return None, "invalid"


    # 密码错误
    if not verify_password(
        password,
        user.hashed_password
    ):
        return None, "invalid"


    # 用户被禁用
    if not user.is_active:
        return user, "disabled"


    # =========================
    # 登录成功后写入 Redis
    # =========================

    redis_client.setex(
        f"user:{user.username}",
        300,
        user.username
    )

    return user, "success"


# =========================
# 获取缓存中的用户名
# =========================

def get_cached_username(
    username: str
):

    return redis_client.get(
        f"user:{username}"
    )


# =========================
# 缓存用户
# =========================

def cache_user(
    username: str
):

    redis_client.setex(
        f"user:{username}",
        300,
        username
    )