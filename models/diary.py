import uuid
from sqlalchemy import Column, Integer, String, DateTime, func, Text
from configs.database import Base

class Diary(Base):
    __tablename__ = "diary"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    diary_title = Column(String(255), nullable=False)  
    diary_desc = Column(Text, nullable=True)  
    diary_date = Column(DateTime(timezone=True), nullable=False) 
    diary_mood = Column(Integer, nullable=False)       
    diary_tired = Column(Integer, nullable=False)      
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True) 
