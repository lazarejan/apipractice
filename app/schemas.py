from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# UserModel
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(UserBase):
    pass

# PostModel
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    post_id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Posts: PostResponse
    votes: int

# TokenModel
class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    id: str = None

# VoteModel
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore