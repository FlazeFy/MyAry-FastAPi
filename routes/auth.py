from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.schemas import UserCreate, UserLogin
from controllers.auth import register_user, login_user, get_db, refresh_auth_token
from fastapi import Request

router = APIRouter()

@router.post("/register", response_model=dict, 
    summary="Register",
    description="This request is used to create a new account for user using username, email, and password",
    tags=["Auth"],
    status_code=201,
    responses={
        201: {
            "description": "Successful regist a new account",
            "content": {
                "application/json": {
                    "example": {
                        "message": "user registered successfully",
                        "status": "success"
                    }
                }
            }
        },
        409: {
            "description": "Duplicated account",
            "content": {
                "application/json": {
                    "example": {
                        "message": "the email or username already been used. try using other",
                        "status": "failed"
                    }
                }
            }
        },
        422: {
            "description": "Validation failed",
            "content": {
                "application/json": {
                    "example": {
                        "message": "[validation message]",
                        "status": "failed"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "something went wrong",
                        "status": "failed"
                    }
                }
            }
        }
    })
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login", response_model=dict,
    summary="User Login",
    description="Authenticate user with username and password, returning access and refresh tokens.",
    tags=["Auth"],
    responses={
        200: {
            "description": "User successfully logged in",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "AISKWNB123123",
                        "refresh_token": "AISKWNB123123",
                        "message": "user login successfully",
                        "status": "success"
                    }
                }
            }
        },
        401: {
            "description": "Invalid username or password",
            "content": {
                "application/json": {
                    "example": {
                        "message": "invalid username or password",
                        "status": "failed",
                    }
                }
            }
        },
        422: {
            "description": "Validation failed",
            "content": {
                "application/json": {
                    "example": {
                        "message": "[validation message]",
                        "status": "failed"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "something went wrong",
                        "status": "failed",
                    }
                }
            }
        }
    }
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.post("/refresh", response_model=dict,
    summary="Refresh Access Token",
    description="Use a valid refresh token from the Authorization header to get a new access token.",
    tags=["Auth"],
    responses={
        200: {
            "description": "Access token refreshed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "AISKWNB123123",
                        "message": "user token refresh",
                        "status": "success"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized: Missing, invalid, or expired refresh token",
            "content": {
                "application/json": {
                    "example": {
                        "message": "invalid token",
                        "status": "failed"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "something went wrong",
                        "status": "failed",
                    }
                }
            }
        }
    }
)
def refresh(request: Request, db: Session = Depends(get_db)):
    return refresh_auth_token(request, db)
