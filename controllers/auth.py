from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
from models.users import User
from utils.jwt import create_auth_token, decode_auth_token
from passlib.context import CryptContext
from controllers.schemas import UserCreate, UserLogin
from configs.database import SessionLocal
from datetime import timedelta
from fastapi import Request

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
    
    data = {
        "sub": db_user.username
    }

    # Utils - Create Token
    access_token = create_auth_token(data, expires_delta=timedelta(hours=1))
    refresh_auth_token = create_auth_token(data, expires_delta=timedelta(hours=7))

    # Response
    return {
        "access_token": access_token, 
        "refresh_auth_token": refresh_auth_token, 
        "message": "User login successfully",
        "status": "success"
    }

def refresh_auth_token(request: Request):
    try:
        # Extract Refresh Token From Header
        refresh_auth_token = request.headers.get("Authorization")
        if not refresh_auth_token or not refresh_auth_token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid refresh token")

        refresh_auth_token = refresh_auth_token.split(" ")[1]

        # Utils - Decode Token
        payload = decode_auth_token(refresh_auth_token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Utils - New Access Token
        new_access_token = create_auth_token(
            {"sub": username}, expires_delta=timedelta(hours=1)
        )

        # Response
        return {
            "access_token": new_access_token,
            "message": "User token refresh",
            "status": "success"
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")