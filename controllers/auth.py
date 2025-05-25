from fastapi.responses import JSONResponse
import jwt
from sqlalchemy.orm import Session
from models.users import User
from utils.jwt import create_auth_token, decode_auth_token
from passlib.context import CryptContext
from controllers.schemas import UserCreate, UserLogin
from configs.database import SessionLocal
from models.users import is_username_or_email_taken
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
    try:
        # Query : Check account availability
        if is_username_or_email_taken(db, username=user.username, email=user.email):
            return JSONResponse(
                status_code=409,
                content={
                    "message": "the email or username already been used. try using other",
                    "status": "failed",
                }
            )

        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )

        # Exec Create User
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Response
        return JSONResponse(
            status_code=201,
            content={
                "message": "user registered successfully",
                "status": "success"
            }
        )

    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "something went wrong",
                "status": "failed",
            }
        )


def login_user(user: UserLogin, db: Session):
    try:
        # Query : Get User By Username
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            return JSONResponse(
                status_code=401,
                content={
                    "message": "invalid username or password",
                    "status": "failed",
                }
            )
        
        data = {
            "sub": db_user.username
        }

        # Utils - Create Token
        access_token = create_auth_token(data, expires_delta=timedelta(hours=1))
        refresh_auth_token = create_auth_token(data, expires_delta=timedelta(hours=7))

        # Response
        return JSONResponse(
            status_code=200,
            content={
                "access_token": access_token, 
                "refresh_token": refresh_auth_token, 
                "message": "user login successfully",
                "status": "success"
            }
        )

    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "something went wrong",
                "status": "failed",
            }
        )

def refresh_auth_token(request: Request, db: Session):
    try:
        # Extract Refresh Token From Header
        refresh_auth_token = request.headers.get("Authorization")
        if not refresh_auth_token or not refresh_auth_token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "message": "invalid refresh token",
                    "status": "failed",
                }
            )

        refresh_auth_token = refresh_auth_token.split(" ")[1]

        # Utils - Decode Token
        payload = decode_auth_token(refresh_auth_token)
        username = payload.get("sub")
        if not username:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "invalid token",
                    "status": "failed",
                }
            )

        # Utils - New Access Token
        new_access_token = create_auth_token(
            {"sub": username}, expires_delta=timedelta(hours=1)
        )

        # Response
        return JSONResponse(
            status_code=200,
            content={
                "access_token": new_access_token,
                "message": "user token refresh",
                "status": "success"
            }
        )

    except jwt.ExpiredSignatureError or jwt.PyJWTError:
        return JSONResponse(
            status_code=401,
            content={
                "message": "invalid token",
                "status": "failed",
            }
        )
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "something went wrong",
                "status": "failed",
            }
        )