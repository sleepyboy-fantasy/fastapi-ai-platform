from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session


from app.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token
)

from app.core.security import (
    create_access_token,
    get_current_username
)

from app.core.exceptions import (
    UserAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCredentialsException
)

from app.services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_username,
    get_user_by_email,
    get_cached_username,
    cache_user
)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# =========================
# 用户注册
# =========================

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # 检查用户名
    exist_username = get_user_by_username(
        db,
        user.username
    )

    if exist_username:
        raise UserAlreadyExistsException()


    # 检查邮箱
    exist_email = get_user_by_email(
        db,
        user.email
    )

    if exist_email:
        raise EmailAlreadyExistsException()


    # 创建用户
    db_user = create_user(
        db,
        user.username,
        user.email,
        user.password
    )


    return db_user


# =========================
# 用户登录
# =========================

@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user, auth_status = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )


    # 用户被禁用
    if auth_status == "disabled":
        raise HTTPException(
            status_code=401,
            detail="User is disabled"
        )


    # 用户不存在 / 密码错误
    if auth_status == "invalid":
        raise InvalidCredentialsException()


    access_token = create_access_token(
        {
            "sub": user.username
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# 获取当前用户
# =========================

@router.get("/me")
def get_me(
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
):

    # =========================
    # 先查询 Redis
    # =========================

    cached_username = get_cached_username(
        username
    )

    if cached_username:

        user = get_user_by_username(
            db,
            cached_username
        )

    else:

        # =========================
        # Redis 没有缓存
        # 查询 PostgreSQL
        # =========================

        user = get_user_by_username(
            db,
            username
        )

        if user:

            cache_user(
                user.username
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