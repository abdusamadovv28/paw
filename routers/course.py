from fastapi import APIRouter, status, HTTPException
from models.course import Course
from core.dependencies import DBSessionDep, CurrentUserDep
from schemas.course import CourseCreate, CourseOut

course_router = APIRouter(
    prefix="/course",
    tags=["course"]
)


@course_router.get("/")
async def get_all_courses(db: DBSessionDep, current_user: CurrentUserDep):
    data = db.query(Course).all()
    return {"courses": data}


@course_router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(db: DBSessionDep, course: CourseCreate, current_user: CurrentUserDep):
    new_course = Course(
        title=course.title,
        description=course.description,
        author_id=course.author_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@course_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseCreate, db: DBSessionDep, current_user: CurrentUserDep):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_course.title = course.title
    db_course.description = course.description
    db_course.author_id = course.author_id
    db.commit()
    db.refresh(db_course)
    return db_course


@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: DBSessionDep, current_user: CurrentUserDep):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()
    return
