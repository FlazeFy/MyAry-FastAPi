from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.schemas import UserCreate, UserLogin
from controllers.auth import register_user, login_user, get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)
