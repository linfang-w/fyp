from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# BaseModel schema for post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class PostCreate(PostBase):
    pass

## response to user
class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut

    ## converts to orm model
    class Config:
        orm_mode = True


