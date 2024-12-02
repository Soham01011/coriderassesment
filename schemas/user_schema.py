from pydantic import EmailStr, BaseModel
from typing import Optional
import uuid

class UserCreate(BaseModel):
    id: str  = str(uuid.uuid4())
    username: str
    email: EmailStr
    password: str 

class UserResponce(BaseModel):
    id: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = None

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]