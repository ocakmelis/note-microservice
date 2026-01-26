from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from internal.schemas.note_schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from internal.database.database import get_db
from internal.handler.note_handler import NoteHandler
from internal.dependencies import get_current_user_id

router = APIRouter(prefix="/notes", tags=["Notlar"])

@router.post("")
def create_note(
    note: NoteCreate, 
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return NoteHandler.create_note(
        note_data=note,
        user_id=user_id,
        db=db
    )


@router.get("", response_model=List[NoteListResponse])
def get_notes(
    title: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Kullanıcının tüm notlarını listeler"""
    return NoteHandler.get_notes(
        user_id=user_id,
        db=db,
        title=title
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Belirli bir notu getirir"""
    return NoteHandler.get_note(
        note_id=note_id,
        user_id=user_id,
        db=db
    )


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Notu günceller"""
    return NoteHandler.update_note(
        note_id=note_id,
        note_update=note_update,
        user_id=user_id,
        db=db
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Notu siler"""
    NoteHandler.delete_note(
        note_id=note_id,
        user_id=user_id,
        db=db
    )
    return None
