from pydantic import BaseModel, EmailStr

# Auth Controller
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str