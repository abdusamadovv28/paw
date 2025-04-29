from pydantic import BaseModel
from typing import Optional

class LessonBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    course_id: Optional[int] = None

class LessonCreate(LessonBase):
    title: str
    course_id: int

class Lesson(LessonBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True