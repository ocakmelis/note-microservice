from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from repository.note_repository import (
    create_note as repo_create_note,
    get_notes_by_user,
    get_note_by_id as repo_get_note,
    update_note as repo_update_note,
    delete_note as repo_delete_note
)
from schemas.note_schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note_data: NoteCreate, user_id: int):
    """Yeni not oluşturur"""
    return repo_create_note(
        db=db,
        title=note_data.title,
        content=note_data.content,
        category=note_data.category,
        user_id=user_id
    )


def get_all_notes(
    db: Session,
    user_id: int,
    title_filter: Optional[str] = None
):
    """Kullanıcının tüm notlarını getirir"""
    return get_notes_by_user(db, user_id, title_filter)


def get_note_by_id(
    db: Session,
    note_id: int,
    user_id: int
):
    """ID ile not getirir"""
    note = repo_get_note(db, note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Not bulunamadı")
    return note


def update_note(
    db: Session,
    note_id: int,
    note_data: NoteUpdate,
    user_id: int
):
    """Not günceller"""
    note = get_note_by_id(db, note_id, user_id)
    return repo_update_note(db, note, note_data)


def delete_note(
    db: Session,
    note_id: int,
    user_id: int
):
    """Not siler"""
    note = get_note_by_id(db, note_id, user_id)
    repo_delete_note(db, note)
    return {"message": "Not başarıyla silindi"}