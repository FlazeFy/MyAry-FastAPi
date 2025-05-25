from fastapi import FastAPI
from configs.database import Base, engine
from routes.auth import router_auth
from routes.diary import router_diary

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_auth, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(router_diary, prefix="/api/v1/diary", tags=["Diary"])
