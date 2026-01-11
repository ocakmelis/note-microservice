from fastapi import APIRouter, Header, Query
from typing import Optional
from pydantic import BaseModel
from internal.handlers.note_service_handler import NoteServiceHandler

router = APIRouter(prefix="/notes", tags=["Notes"])
handler = NoteServiceHandler()

class NoteCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None

@router.post("")
async def create_note(note_data: NoteCreate, authorization: str = Header(...)):
    """Not oluştur"""
    return await handler.create_note(authorization, note_data.dict())

@router.get("")
async def get_notes(authorization: str = Header(...), title: Optional[str] = Query(None)):
    """Notları listele"""
    return await handler.get_notes(authorization, title)

@router.get("/{note_id}")
async def get_note(note_id: int, authorization: str = Header(...)):
    """Tek not getir"""
    return await handler.get_note(authorization, note_id)

@router.put("/{note_id}")
async def update_note(note_id: int, note_data: NoteUpdate, authorization: str = Header(...)):
    """Not güncelle"""
    return await handler.update_note(authorization, note_id, note_data.dict(exclude_unset=True))

@router.delete("/{note_id}")
async def delete_note(note_id: int, authorization: str = Header(...)):
    """Not sil"""
    await handler.delete_note(authorization, note_id)
    return {"message": "Note deleted successfully"}

@router.post("/{note_id}/summarize")
async def summarize_note(note_id: int, authorization: str = Header(...)):
    """Not özetle"""
    return await handler.summarize_note(authorization, note_id)

@router.post("/{note_id}/categorize")
async def categorize_note(note_id: int, authorization: str = Header(...)):
    """Not etiketle"""
    return await handler.categorize_note(authorization, note_id)