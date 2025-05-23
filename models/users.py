from sqlalchemy import Column, Integer, String, DateTime, func
from configs.database import Base
from sqlalchemy.orm import Session

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

def is_username_or_email_taken(db: Session, username: str = None, email: str = None) -> bool:
    if not username and not email:
        return True

    if username:
        if db.query(User).filter(User.username == username).first():
            return True

    if email:
        if db.query(User).filter(User.email == email).first():
            return True

    return False