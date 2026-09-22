from typing import Optional

from pydantic import BaseModel


# =========================
# 用户注册
# =========================

class UserCreate(BaseModel):

    username: str

    email: str

    password: str


# =========================
# 用户登录
# =========================

class UserLogin(BaseModel):

    username: str

    password: str


# =========================
# 用户响应
# =========================

class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    class Config:
        from_attributes = True


# =========================
# JWT Token
# =========================

class Token(BaseModel):

    access_token: str

    token_type: str


# =========================
# 用户启用/禁用
# =========================

class UserStatusUpdate(BaseModel):

    is_active: bool


# =========================
# 管理员修改用户信息
# =========================

class UserUpdate(BaseModel):

    username: Optional[str] = None

    email: Optional[str] = None

    password: Optional[str] = None

    is_active: Optional[bool] = None

    is_admin: Optional[bool] = None