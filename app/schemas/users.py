from pydantic import BaseModel 
from app.models.users import UserRole

class UserBase(BaseModel): 
    name: str 

    
class UserCreate(UserBase): 
    password:str
    
    class Config:
            extra = "forbid"


class UserLogin(BaseModel):
    name: str 
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
    class Config:
        extra = "forbid"

class AdminUpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None
    role: UserRole | None = None

    


class UserResponse(UserBase): 
    id: int 
    
    class Config: 
        from_attributes = True
