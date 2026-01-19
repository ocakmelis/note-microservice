from sqlalchemy.orm import Session
from internal.models.note_models import Note
from typing import Optional, List

def create_note(db: Session, title: str, content: str, user_id: int, category: Optional[str] = None) -> Note:
    """Yeni not oluştur"""
    note = Note(
        title=title,
        content=content,
        category=category,
        user_id=user_id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes_by_user(db: Session, user_id: int, title_filter: Optional[str] = None) -> List[Note]:
    """Kullanıcının notlarını getir"""
    query = db.query(Note).filter(Note.user_id == user_id)
    
    if title_filter:
        query = query.filter(Note.title.ilike(f"%{title_filter}%"))
    
    return query.order_by(Note.created_at.desc()).all()

def get_note_by_id(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    """ID ile not getir"""
    return db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user_id
    ).first()

def update_note(db: Session, note: Note, title: Optional[str] = None, content: Optional[str] = None, category: Optional[str] = None) -> Note:
    """Not güncelle"""
    if title is not None:
        note.title = title
    if content is not None:
        note.content = content
    if category is not None:
        note.category = category
    
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note: Note):
    """Not sil"""
    db.delete(note)
    db.commit()

def update_note_summary(db: Session, note: Note, summary: str) -> Note:
    """Not özetini güncelle"""
    note.summary = summary
    db.commit()
    db.refresh(note)
    return note

def update_note_tags(db: Session, note: Note, tags: List[str]) -> Note:
    """Not etiketlerini güncelle"""
    note.tags = tags
    db.commit()
    db.refresh(note)
    return note