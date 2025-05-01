from models.base import BaseModel
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped


class Course(BaseModel):
    __tablename__ = "course"

    title: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    __tablename__ = "lesson"
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    video_url: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    content: Mapped[str] = mapped_column(String(255), nullable=True)

    def __str__(self):
        return self.title