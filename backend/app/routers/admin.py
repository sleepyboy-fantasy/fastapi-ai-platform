from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import (
    get_current_username,
    hash_password
)
from app.schemas.user import UserStatusUpdate, UserUpdate


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# =========================
# 管理员权限检查
# =========================

def get_current_admin(
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):
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

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


# =========================
# 获取当前管理员
# =========================

@router.get("/me")
def get_admin_me(
    admin: User = Depends(get_current_admin)
):
    return {
        "message": "Admin access granted",
        "id": admin.id,
        "username": admin.username,
        "email": admin.email,
        "is_active": admin.is_active,
        "is_admin": admin.is_admin
    }


# =========================
# 获取所有用户
# =========================

@router.get("/users")
def get_all_users(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users = (
        db.query(User)
        .order_by(User.id)
        .all()
    )

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
        for user in users
    ]


# =========================
# 获取单个用户
# =========================

@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }


# =========================
# 修改用户启用/禁用状态
# =========================

@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_active = status_data.is_active

    db.commit()
    db.refresh(user)

    return {
        "message": "User status updated",
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }


# =========================
# 修改用户信息
# =========================

@router.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =========================
    # 检查用户名是否重复
    # =========================

    if user_data.username is not None:
        existing_username = (
            db.query(User)
            .filter(
                User.username == user_data.username,
                User.id != user_id
            )
            .first()
        )

        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        user.username = user_data.username

    # =========================
    # 检查邮箱是否重复
    # =========================

    if user_data.email is not None:
        existing_email = (
            db.query(User)
            .filter(
                User.email == user_data.email,
                User.id != user_id
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user.email = user_data.email

    # =========================
    # 修改密码
    # =========================

    if user_data.password is not None:
        user.hashed_password = hash_password(
            user_data.password
        )

    # =========================
    # 修改启用状态
    # =========================

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    # =========================
    # 修改管理员权限
    # =========================

    if user_data.is_admin is not None:
        user.is_admin = user_data.is_admin

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }


# =========================
# 删除用户
# =========================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # =========================
    # 查询目标用户
    # =========================

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =========================
    # 防止管理员删除自己
    # =========================

    if user.id == admin.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )

    # =========================
    # 删除用户
    # =========================

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully",
        "id": user.id,
        "username": user.username
    }