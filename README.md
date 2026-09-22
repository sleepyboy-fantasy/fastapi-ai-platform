# FastAPI-RAG 智能文档知识库问答系统

基于 **FastAPI + PostgreSQL + pgvector + RAG + DeepSeek LLM** 构建的企业级智能知识库问答平台。

系统支持用户管理、文档上传、文本解析、智能分块、向量化存储、语义检索以及基于大语言模型的增强问答，实现企业内部文档知识的智能检索与问答。

项目面向企业知识管理场景，可用于产品手册、技术文档、规章制度、项目资料等非结构化文本的智能查询。

---

## 📌 项目演示

### 核心功能

- 用户注册与登录
- JWT 身份认证
- 用户权限管理
- 文档上传管理
- 文档内容解析
- 文本自动分块
- SHA-256 文件去重
- BGE Embedding 向量化
- pgvector 相似度检索
- RAG 检索增强生成
- DeepSeek 大模型问答
- 管理员用户管理

# 🛠️ 技术栈

## 后端

| 技术 | 作用 |
|-|-|
| FastAPI | Web API 服务框架 |
| SQLAlchemy | ORM 数据库操作 |
| Alembic | 数据库迁移 |
| PostgreSQL | 关系型数据库 |
| pgvector | 向量数据库扩展 |
| Redis | 缓存与任务支持 |
| JWT | 用户认证 |
| Pydantic | 数据校验 |

---

## AI / RAG

| 技术 | 作用 |
|-|-|
| RAG | 检索增强生成架构 |
| BGE-small-zh-v1.5 | 中文文本向量模型 |
| Embedding | 文本语义向量化 |
| Cosine Similarity | 向量相似度搜索 |
| DeepSeek API | 大语言模型生成回答 |

---

## 前端

| 技术 | 作用 |
|-|-|
| React | 前端框架 |
| Vite | 前端构建工具 |
| Axios | HTTP请求 |
| React Router | 页面路由 |

---

## 部署

| 技术 | 作用 |
|-|-|
| Docker | 容器化部署 |
| Docker Compose | 多服务编排 |

---
---

# ⚙️ 环境要求

## 基础环境

建议环境：


Python >= 3.10

Node.js >= 18

Docker >= 24

Docker Compose >= 2

PostgreSQL >= 15


---

# 🚀 快速开始

## 1. 克隆项目

```bash
git clone https://github.com/sleepyboy-fantasy/fastapi-ai-platform.git

cd fastapi-ai-platform

2. 配置环境变量

复制环境变量模板：

cp .env.example .env

修改：

.env

示例：

POSTGRES_USER=fastapi_user

POSTGRES_PASSWORD=123456

POSTGRES_DB=fastapi_db

POSTGRES_HOST=localhost

POSTGRES_PORT=5432

后端配置：

进入 backend：

cd backend

复制：

cp .env.example .env

修改：

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30


DATABASE_URL=postgresql://fastapi_user:123456@localhost:5432/fastapi_db


DEEPSEEK_API_KEY=your_api_key

DEEPSEEK_BASE_URL=https://api.deepseek.com
3. 使用 Docker 启动数据库

回到项目根目录：

cd ..

启动：

docker compose up -d

启动服务：

PostgreSQL
Redis

查看：

docker ps
4. 初始化数据库

进入 backend：

cd backend

创建虚拟环境：

python -m venv venv

激活：

Windows:

venv\Scripts\activate

Linux:

source venv/bin/activate

安装依赖：

pip install -r requirements.txt

执行数据库迁移：

alembic upgrade head
5. 启动后端

执行：

uvicorn app.main:app --reload

默认地址：

http://127.0.0.1:8000

接口文档：

http://127.0.0.1:8000/docs
6. 启动前端

进入：

cd frontend

安装依赖：

npm install

启动：

npm run dev

访问：

http://localhost:5173