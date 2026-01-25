from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from internal.database.database import Base

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100))
    summary = Column(Text)
    tags = Column(String)  # ARRAY yerine String (JSON olarak saklanabilir)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
