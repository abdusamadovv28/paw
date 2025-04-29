from sqlalchemy.orm import Session
from models.course import Lesson
from schemas.lesson import LessonCreate
from fastapi import HTTPException, status

def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lesson).offset(skip).limit(limit).all()

def get_lesson(db: Session, lesson_id: int):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()

def create_lesson(db: Session, lesson: LessonCreate, user_id: int):
    db_lesson = Lesson(
        title=lesson.title,
        description=lesson.description,
        video_url=lesson.video_url,
        course_id=lesson.course_id,
        owner_id=user_id
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def update_lesson(db: Session, lesson_id: int, lesson: LessonCreate, user_id: int):
    db_lesson = get_lesson(db, lesson_id=lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if db_lesson.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this lesson"
        )
    update_data = lesson.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lesson, key, value)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def delete_lesson(db: Session, lesson_id: int, user_id: int):
    db_lesson = get_lesson(db, lesson_id=lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if db_lesson.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this lesson"
        )
    db.delete(db_lesson)
    db.commit()
    return db_lesson