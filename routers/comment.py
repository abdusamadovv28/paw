from fastapi import APIRouter, status
from typing import List
from schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from core.dependencies import DBSessionDep, CurrentUserDep
import services.comment as comment_service

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@comment_router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate,
    db: DBSessionDep,
    current_user: CurrentUserDep
):
    return comment_service.create_comment(db=db, comment_data=comment_data, user_id=current_user["id"])


@comment_router.get("/", response_model=List[CommentResponse])
def get_all_comments(db: DBSessionDep):
    return comment_service.get_all_comments(db)


@comment_router.get("/lesson/{lesson_id}", response_model=List[CommentResponse])
def get_comments_by_lesson(lesson_id: int, db: DBSessionDep):
    return comment_service.get_comments_by_lesson_id(db, lesson_id=lesson_id)


@comment_router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    update_data: CommentUpdate,
    db: DBSessionDep,
    current_user: CurrentUserDep
):
    return comment_service.update_comment(db, comment_id, user_id=current_user["id"], update_data=update_data)


@comment_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: DBSessionDep,
    current_user: CurrentUserDep
):
    comment_service.delete_comment(db, comment_id, user_id=current_user["id"])