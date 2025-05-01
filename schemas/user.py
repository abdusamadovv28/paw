from pydantic import BaseModel


class CreateUserFrom(BaseModel):
    full_name: str
    email: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str