from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.schemas import UserCreate, UserLogin
from controllers.auth import register_user, login_user, get_db, refresh_auth_token
from fastapi import Request

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.post("/refresh")
def refresh(request: Request):
    return refresh_auth_token(request)
