from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from note_schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from database import get_db
from models import Note
from auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/notes", tags=["Notlar"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Yeni bir not oluşturur"""
    new_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
        user_id=current_user.id,
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
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Kullanıcının tüm notlarını listeler
    Query parametresi ile filtreleme yapılabilir: ?title=arama_kelimesi"""
    query = db.query(Note).filter(Note.user_id == current_user.id)
    
    # Başlığa göre filtreleme
    if title:
        query = query.filter(Note.title.contains(title))
    
    notes = query.all()
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Belirli bir notu ID ile getirir"""
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id == current_user.id
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
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Var olan bir notu günceller"""
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not bulunamadı"
        )
    
    # Sadece gönderilen alanları güncelle
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
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Belirli notu siler"""
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not bulunamadı"
        )
    
    db.delete(note)
    db.commit()
    return None