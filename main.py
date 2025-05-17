from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Schema
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# Route GET
@app.get("/")
def read_root():
    return {"message": "Hello world!"}
