from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    video_url = Column(String)
    course_id = Column(Integer, ForeignKey("course.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
