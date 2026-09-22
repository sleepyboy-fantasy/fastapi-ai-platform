from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.exceptions.exceptions import AppException


# =========================
# 自定义异常处理器
# =========================

async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.code,
        content={
            "code": exc.code,
            "message": exc.message
        }
    )


# =========================
# FastAPI HTTPException 处理器
# =========================

async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail
        }
    )