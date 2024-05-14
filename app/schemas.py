from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: int | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class PostBase(BaseModel):
    title: str
    content: str
    published:bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: User

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: bool
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    post: Post
    votes: int

    class Config:
        orm_mode = True