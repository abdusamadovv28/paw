from fastapi import APIRouter, HTTPException,status
from models.course import Course
from core.dependencies import DBSessionDep, CurrentUserDep
from models.user import User
from schemas.course import CourseCreate, CourseOut, CourseUpdate
course_router = APIRouter(
    prefix="/course",
    tags=["course"]
)

@course_router.get("/get")
async def get_all_courses(db: DBSessionDep):
    data = db.query(Course).all()
    return {"courses": data}

@course_router.post("/create", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: DBSessionDep, current_user: CurrentUserDep):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Get author_id from the JWT token
    author_id = current_user["id"]
        
    # Verify the author exists in the database
    author = db.query(User).filter(User.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found"
        )
    
    # Create course with data from request and author_id from token
    course_data = course.dict()
    new_course = Course(**course_data, author_id=author_id)
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@course_router.put("/{course_id}",response_model=CourseOut,status_code=status.HTTP_200_OK)
async def update_course(course_id: int, course:CourseUpdate, db: DBSessionDep, current_user: CurrentUserDep):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
        
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    if db_course.author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz faqat ozingizni kursingizni o'zgartirishingiz mumkun"  #noqa
        )
    
    for field,value in course.dict(exclude_unset=True).items():
        setattr(db_course, field, value)

    db.commit()
    db.refresh(db_course)
    return db_course

@course_router.delete("/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(course_id: int, db: DBSessionDep, current_user: CurrentUserDep):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
        
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    if db_course.author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own courses"
        )
    
    db.delete(db_course)
    db.commit()
    
    return {"message": f"Course with id {course_id} has been deleted successfully"}