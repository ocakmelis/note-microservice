from fastapi import APIRouter, Depends
from models import NoteCreate, Note
from note_services import (
    create_note, 
    get_all_notes, 
    get_note_by_id, 
    update_note, 
    delete_note
)
from auth import verify_token
from user_services import get_user_by_username
from typing import Optional

router = APIRouter(prefix="/notes", tags=["Notlar"])

def get_current_user_id(username: str = Depends(verify_token)) -> int:
    """Mevcut kullanıcının ID'sini döndürür"""
    user = get_user_by_username(username)
    return user["id"]

@router.post("", response_model=Note)
def create_new_note(
    note_data: NoteCreate,
    user_id: int = Depends(get_current_user_id)
):
    """Yeni bir not oluşturur"""
    return create_note(note_data, user_id)

@router.get("", response_model=list[Note])
def get_notes(
    title: Optional[str] = None,
    user_id: int = Depends(get_current_user_id)
):
    """Kullanıcının tüm notlarını listeler
    Query parametresi ile filtreleme yapılabilir: ?title=arama_kelimesi"""
    return get_all_notes(user_id, title)

@router.get("/{note_id}", response_model=Note)
def get_note(
    note_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """
    Belirli bir notu ID ile getirir
    """
    return get_note_by_id(note_id, user_id)

@router.put("/{note_id}", response_model=Note)
def update_existing_note(
    note_id: int,
    note_data: NoteCreate,
    user_id: int = Depends(get_current_user_id)
):
    """
    Var olan bir notu günceller
    """
    return update_note(note_id, note_data, user_id)

@router.delete("/{note_id}")
def delete_existing_note(
    note_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Belirli notu siler"""
    return delete_note(note_id, user_id)
