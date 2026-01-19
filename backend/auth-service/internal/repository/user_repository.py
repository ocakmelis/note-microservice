from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class NoteCreate(BaseModel):
    """Not oluşturma request"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: Optional[str] = Field(None, max_length=100)

class NoteUpdate(BaseModel):
    """Not güncelleme request"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=100)

class NoteResponse(BaseModel):
    """Not detay response"""
    id: int
    title: str
    content: str
    category: Optional[str]
    summary: Optional[str]
    tags: List[str] = []
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class NoteListResponse(BaseModel):
    """Not liste response"""
    id: int
    title: str
    category: Optional[str]
    summary: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    """Özet response"""
    summary: str

class CategoryResponse(BaseModel):
    """Etiket response"""
    tags: List[str]