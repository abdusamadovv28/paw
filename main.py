from fastapi import FastAPI
from routers.user import auth_router
from routers.course import course_router
from core.db import engine
from routers import lesson

from models import base

app = FastAPI()

base.Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(course_router)
app.include_router(lesson.router)