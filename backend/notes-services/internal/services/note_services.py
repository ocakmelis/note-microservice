from models import NoteCreate, Note
from database import notes_db, get_next_note_id
from fastapi import HTTPException
from typing import Optional

def create_note(note_data: NoteCreate, user_id: int):
    """Yeni not oluşturur"""
    new_note = {
        "id": get_next_note_id(),
        "title": note_data.title,
        "content": note_data.content,
        "owner_id": user_id
    }
    
    notes_db.append(new_note)
    return Note(**new_note)

def get_all_notes(user_id: int, title_filter: Optional[str] = None):
    """Kullanıcının tüm notlarını getirir"""
    user_notes = [note for note in notes_db if note["owner_id"] == user_id]
    
    # Eğer başlık filtresi varsa uygula
    if title_filter:
        user_notes = [note for note in user_notes if title_filter.lower() in note["title"].lower()]
    
    return [Note(**note) for note in user_notes]

def get_note_by_id(note_id: int, user_id: int):
    """Belirli bir notu getirir"""
    for note in notes_db:
        if note["id"] == note_id:
            # Not kullanıcıya ait mi kontrol et
            if note["owner_id"] != user_id:
                raise HTTPException(status_code=403, detail="Bu nota erişim yetkiniz yok")
            return Note(**note)
    
    raise HTTPException(status_code=404, detail="Not bulunamadı")

def update_note(note_id: int, note_data: NoteCreate, user_id: int):
    """Bir notu günceller"""
    for note in notes_db:
        if note["id"] == note_id:
            # Not kullanıcıya ait mi kontrol et
            if note["owner_id"] != user_id:
                raise HTTPException(status_code=403, detail="Bu notu güncelleme yetkiniz yok")
            
            note["title"] = note_data.title
            note["content"] = note_data.content
            return Note(**note)
    
    raise HTTPException(status_code=404, detail="Not bulunamadı")

def delete_note(note_id: int, user_id: int):
    """Bir notu siler"""
    for i, note in enumerate(notes_db):
        if note["id"] == note_id:
            # Not kullanıcıya ait mi kontrol et
            if note["owner_id"] != user_id:
                raise HTTPException(status_code=403, detail="Bu notu silme yetkiniz yok")
            
            notes_db.pop(i)
            return {"message": "Not başarıyla silindi"}
    
    raise HTTPException(status_code=404, detail="Not bulunamadı")