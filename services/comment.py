from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import Type


def create_comment(db: Session, comment_data: CommentCreate, user_id: int) -> Comment:
    new_comment = Comment(
        user_id=user_id,
        lesson_id=comment_data.lesson_id,
        text=comment_data.text,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all_comments(db: Session) -> list[Type[Comment]]:
    return db.query(Comment).all()

def get_comment_by_id(db: Session, comment_id: int) -> Type[Comment]:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

def get_comments_by_lesson_id(db: Session, lesson_id: int) -> list[Type[Comment]]:
    return db.query(Comment).filter(Comment.lesson_id == lesson_id).all()

def update_comment(db: Session, comment_id: int, user_id: int, update_data: CommentUpdate) -> Type[Comment]:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")

    if update_data.text is not None:
        comment.text = update_data.text

    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int, user_id: int) -> dict:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}