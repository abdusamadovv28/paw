from pydantic import BaseModel
from typing import Optional


class CourseCreate(BaseModel):
    title: str
    description: str


class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    author_id: int

    class Config:
        orm_mode = True


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
