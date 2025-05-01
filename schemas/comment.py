from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    lesson_id: int
    text: str = Field(..., max_length=500)

class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, max_length=500)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)