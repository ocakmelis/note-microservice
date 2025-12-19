from pydantic import BaseModel
from typing import Optional

# Not Modelleri
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True

# Yanıt Modelleri
class SummaryResponse(BaseModel):
    summary: str

class CategoryResponse(BaseModel):
    tags: list[str]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str