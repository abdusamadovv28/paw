from models.base import BaseModel
from sqlalchemy import Column, String, Boolean


class User(BaseModel):
    __tablename__ = "users"

    full_name = Column(String(255), nullable=True)
    email = Column(String(225), unique=True, nullable=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    def __str__(self):
        return self.full_name