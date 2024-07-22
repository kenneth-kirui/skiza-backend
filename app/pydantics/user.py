from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    is_active:  bool = True
    role_id: Optional[int] = 1

class UserCreate(UserBase):
    pass
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    role_id: Optional[int] = 1
    class Config:
        orm_mode = True
        
class UserInDB(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str