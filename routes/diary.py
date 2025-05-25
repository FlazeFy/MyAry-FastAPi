from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.schemas import DiaryCreate
from controllers.diary import post_diary, get_db

router_diary = APIRouter()

@router_diary.post("/", response_model=dict,
    summary="Create Diary",
    description="This request is used to insert a new diary with mood, tired level, and description",
    tags=["Diary"],
    status_code=201,
    responses={
        201: {
            "description": "Diary created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Diary created",
                        "status": "success",
                        "data": {
                            "diary_title": "A good day",
                            "diary_desc": "I felt productive and focused.",
                            "diary_date": "2025-05-25T15:00:00",
                            "diary_mood": 8,
                            "diary_tired": 3
                        },
                        "count": 1
                    }
                }
            }
        },
        400: {
            "description": "Bad request or invalid data",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Invalid diary_date format. Use ISO 8601.",
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
def create_diary(data: DiaryCreate, db: Session = Depends(get_db)):
    return post_diary(data, db)
