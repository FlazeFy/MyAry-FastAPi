from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.orm import Session
from controllers.schemas import DiaryCreate
from models.diary import Diary
from configs.database import SessionLocal
from utils.generator import get_UUID

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def post_diary(data: DiaryCreate, db: Session):
    try:
        # Validator Diary Date
        try:
            diary_date = datetime.fromisoformat(data.diary_date)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid diary_date format. Use ISO 8601.")

        created_at = datetime.utcnow()

        # Query : Add Diary
        query = insert(Diary).values(
            id=get_UUID(),
            diary_title=data.diary_title,
            diary_desc=data.diary_desc,
            diary_date=diary_date,
            diary_mood=data.diary_mood,
            diary_tired=data.diary_tired,
            created_at=created_at
        )

        # Exec
        result = db.execute(query)
        db.commit()

        # Response
        if result.rowcount > 0:
            return JSONResponse(
                status_code=201,
                content={
                    "message": "diary created",
                    "status": "success",
                    "data": data.dict(),
                }
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "diary failed to created",
                    "status": "failed",
                }
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()

        return JSONResponse(
            status_code=500,
            content={
                "message": "something went wrong",
                "status": "failed"
            }
        )
