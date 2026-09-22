from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import http_exception_handler

from app.routers import users
from app.routers import admin
from app.routers import documents
from app.routers import qa

app = FastAPI(
    title="FastAPI AI Platform"
)


# =========================
# CORS 跨域配置
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    HTTPException,
    http_exception_handler
)


app.include_router(users.router)
app.include_router(admin.router)
app.include_router(documents.router)
app.include_router(qa.router)


@app.get("/")
def root():
    return {
        "message": "FastAPI AI Platform running"
    }