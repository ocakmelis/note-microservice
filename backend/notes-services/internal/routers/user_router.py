from fastapi import APIRouter
from models import UserBase, User, TokenResponse
from ..handler import user_handler

router = APIRouter(prefix="/auth", tags=["Kimlik Doğrulama"])

@router.post("/register", response_model=User)
def register(user_data: UserBase):
    
    """Yeni kullanıcı kaydı oluşturur"""
    return user_handler.create_user(user_data)

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserBase):
  return user_handler.login(user_data)  
    
