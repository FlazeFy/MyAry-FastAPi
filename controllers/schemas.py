from pydantic import BaseModel, EmailStr, Field

# Auth Controller
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

# Diary Controller
class DiaryCreate(BaseModel):
    diary_title: str = Field(..., max_length=255)
    diary_desc: str = Field(..., max_length=1000)
    diary_date: str 
    diary_mood: int = Field(..., ge=0, le=10)
    diary_tired: int = Field(..., ge=0, le=10)