from sqlalchemy.orm import Session
from internal.models.note_models import Note
from internal.schemas.note_schemas import NoteUpdate
from typing import Optional, List
from datetime import datetime


def create_note(
    db: Session, 
    title: str, 
    content: str, 
    user_id: int, 
    category: Optional[str] = None
) -> Note:
    """Yeni not oluşturur"""
    note = Note(
        title=title,
        content=content,
        category=category,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes_by_user(
    db: Session, 
    user_id: int, 
    title_filter: Optional[str] = None
) -> List[Note]:
    """Kullanıcının notlarını getirir"""
    query = db.query(Note).filter(Note.user_id == user_id)
    
    if title_filter:
        query = query.filter(Note.title.ilike(f"%{title_filter}%"))
    
    return query.order_by(Note.created_at.desc()).all()


def get_note_by_id(
    db: Session, 
    note_id: int, 
    user_id: int
) -> Optional[Note]:
    """ID ile not getirir"""
    return db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id
    ).first()


def update_note(
    db: Session, 
    note: Note, 
    note_update: NoteUpdate
) -> Note:
    """Not günceller"""
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


def delete_note(db: Session, note: Note) -> None:
    """Not siler"""
    db.delete(note)
    db.commit()


def update_note_summary(db: Session, note: Note, summary: str) -> Note:
    """Not özetini günceller"""
    note.summary = summary
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note


def update_note_tags(db: Session, note: Note, tags: List[str]) -> Note:
    """Not etiketlerini günceller"""
    note.tags = tags
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note