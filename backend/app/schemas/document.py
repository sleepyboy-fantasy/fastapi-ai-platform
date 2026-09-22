from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):

    id: int
    user_id: int
    filename: str
    file_path: str
    file_type: str
    content: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True