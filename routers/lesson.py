from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.lesson import Lesson, LessonCreate
from services import lesson as lesson_service
from core.dependencies import get_db
from typing import List

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.post("/", response_model=Lesson)
def create(lesson: LessonCreate, db: Session = Depends(get_db)):
    return lesson_service.create_lesson(db, lesson, user_id=1)

@router.get("/", response_model=List[Lesson])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return lesson_service.get_lessons(db, skip, limit)

@router.get("/{lesson_id}", response_model=Lesson)
def get_one(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = lesson_service.get_lesson(db, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson

@router.put("/{lesson_id}", response_model=Lesson)
def update(lesson_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
    return lesson_service.update_lesson(db, lesson_id, lesson)

@router.delete("/{lesson_id}", response_model=Lesson)
def delete(lesson_id: int, db: Session = Depends(get_db)):
    return lesson_service.delete_lesson(db, lesson_id)
