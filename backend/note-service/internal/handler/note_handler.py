from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from internal.schemas.note_schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from internal.services.note_services import (
    create_note as service_create_note,
    get_all_notes as service_get_all_notes,
    get_note_by_id as service_get_note_by_id,
    update_note as service_update_note,
    delete_note as service_delete_note
)


class NoteHandler:
    """Not işlemlerini yöneten handler katmanı"""
    
    @staticmethod
    def create_note(
        note_data: NoteCreate,
        user_id: int,
        db: Session
    ) -> NoteResponse:
        """Yeni not oluşturur"""
        try:
            note = service_create_note(
                db=db,
                note_data=note_data,
                user_id=user_id
            )
            return note
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Not oluşturulurken hata: {str(e)}"
            )
    
    @staticmethod
    def get_notes(
        user_id: int,
        db: Session,
        title: Optional[str] = None
    ) -> List[NoteListResponse]:
        """Kullanıcının notlarını listeler"""
        try:
            notes = service_get_all_notes(
                db=db,
                user_id=user_id,
                title_filter=title
            )
            return notes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Notlar getirilirken hata: {str(e)}"
            )
    
    @staticmethod
    def get_note(
        note_id: int,
        user_id: int,
        db: Session
    ) -> NoteResponse:
        """Belirli bir notu getirir"""
        note = service_get_note_by_id(
            db=db,
            note_id=note_id,
            user_id=user_id
        )
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not bulunamadı"
            )
        return note
    
    @staticmethod
    def update_note(
        note_id: int,
        note_update: NoteUpdate,
        user_id: int,
        db: Session
    ) -> NoteResponse:
        """Notu günceller"""
        note = service_get_note_by_id(
            db=db,
            note_id=note_id,
            user_id=user_id
        )
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not bulunamadı"
            )
        
        try:
            updated_note = service_update_note(
                db=db,
                note_id=note_id,
                note_data=note_update,
                user_id=user_id
            )
            return updated_note
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Not güncellenirken hata: {str(e)}"
            )
    
    @staticmethod
    def delete_note(
        note_id: int,
        user_id: int,
        db: Session
    ) -> None:
        """Notu siler"""
        note = service_get_note_by_id(
            db=db,
            note_id=note_id,
            user_id=user_id
        )
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not bulunamadı"
            )
        
        try:
            service_delete_note(
                db=db,
                note_id=note_id,
                user_id=user_id
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Not silinirken hata: {str(e)}"
            )