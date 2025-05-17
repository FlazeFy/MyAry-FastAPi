from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.users import User
from utils.jwt import create_access_token
from passlib.context import CryptContext
from controllers.schemas import UserCreate, UserLogin
from configs.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(user: UserCreate, db: Session):
    # Query
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)

    # Data Map
    db_user = User(
        username=user.username, 
        email=user.email, 
        password=hashed_password
    )

    # Execute
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Response 
    return {
        "message": "User registered successfully",
        "status": "success"
    }

def login_user(user: UserLogin, db: Session):
    # Query
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Token
    token = create_access_token({
        "sub": db_user.username
    })

    # Response
    return {
        "access_token": token, 
        "token_type": "bearer",
        "status": "success"
    }
