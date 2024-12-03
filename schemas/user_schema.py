import uuid
from typing import Optional
from pydantic import EmailStr, BaseModel, Field

class UserCreateRequest(BaseModel):
    id: str  = str(uuid.uuid4())
    username: str = Field(..., pattern=r'^[a-zA-Z]{2,15}$')
    email: EmailStr
    password: str = Field(..., pattern=r'^[a-zA-Z0-9!@#$%^&*()_+]{8,25}$')

class UserCreate(BaseModel):
    id: str  = str(uuid.uuid4())
    username: str = Field(..., pattern=r'^[a-zA-Z]{2,15}$')
    email: EmailStr
    password: str 

class UserResponce(BaseModel):
    id: str
    username: str = Field(..., pattern=r'^[a-zA-Z]{2,15}$')
    email: EmailStr

    class Config:
        from_attributes = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(..., pattern=r'^[a-zA-Z]{2,15}$')
    email: Optional[EmailStr]
    password: Optional[str]