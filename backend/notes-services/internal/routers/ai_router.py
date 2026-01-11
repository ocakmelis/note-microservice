from fastapi import APIRouter, Depends
from models import SummaryResponse, CategoryResponse
from note_services import get_note_by_id
from summary_services import SummaryService
from category_services import CategoryService
from auth import verify_token
from user_services import get_user_by_username

router = APIRouter(prefix="/notes", tags=["Yapay Zeka Özellikleri"])

summary_service = SummaryService(API_KEY)
category_service = CategoryService(API_KEY)

def get_current_user_id(username: str = Depends(verify_token)) -> int:
    """Mevcut kullanıcının ID'sini döndürür"""
    user = get_user_by_username(username)
    return user["id"]

@router.post("/{note_id}/summarize", response_model=SummaryResponse)
def summarize_note(
    note_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Bir notu özetler"""
    # Notu getir
    note = get_note_by_id(note_id, user_id)
    
    # Özet oluştur
    summary = summary_service.summarize_text(note.content)
    
    return SummaryResponse(summary=summary)

@router.post("/{note_id}/categorize", response_model=CategoryResponse)
def categorize_note(
    note_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """
    Bir not için etiketler/kategoriler oluşturur
    """
    # Notu getir
    note = get_note_by_id(note_id, user_id)
    
    # Etiketler oluştur
    tags = category_service.generate_tags(note.content)
    
    return CategoryResponse(tags=tags)
