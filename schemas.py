from pydantic import BaseModel, EmailStr
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

class postResponse(PostBase):
    post_id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True

# TokenModel
class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    id: str = None