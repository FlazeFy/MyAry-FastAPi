from fastapi import FastAPI
from configs.database import Base, engine
from routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
