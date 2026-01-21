from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from internal.schemas.note_schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from internal.database.database import get_db
from internal.models.note_models import Note
from datetime import datetime

router = APIRouter(prefix="/notes", tags=["Notlar"])

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate, 
    db: Session = Depends(get_db)
):
    # Yeni bir not oluşturur
    # TODO: get_current_user eklenecek (user-service ile iletişim)
    user_id = 1  # Geçici olarak hardcoded
    
    new_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("", response_model=List[NoteListResponse])
def get_notes(
    title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Kullanıcının tüm notlarını listeler
    user_id = 1  # Geçici olarak hardcoded
    
    query = db.query(Note).filter(Note.user_id == user_id)
    
    if title:
        query = query.filter(Note.title.contains(title))
    
    notes = query.all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    # Belirli bir notu ID ile getirir
    user_id = 1  # Geçici olarak hardcoded
    
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id == user_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not bulunamadı"
        )
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    # Var olan bir notu günceller
    user_id = 1  # Geçici olarak hardcoded
    
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id == user_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not bulunamadı"
        )
    
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content
    if note_update.category is not None:
        note.category = note_update.category
    
    note.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    # Belirli notu siler
    user_id = 1  # Geçici olarak hardcoded
    
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id == user_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not bulunamadı"
        )
    
    db.delete(note)
    db.commit()
    return None
