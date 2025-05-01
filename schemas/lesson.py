from pydantic import BaseModel
from typing import Optional


class LessonCreate(BaseModel):
    course_id: int
    title: str
    video_url: str
    content: str


class LessonOut(BaseModel):
    id: int
    course_id: int
    title: str
    video_url: str
    content: str

    class Config:
        orm_mode = True


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    video_url: Optional[str] = None
    content: Optional[str] = None