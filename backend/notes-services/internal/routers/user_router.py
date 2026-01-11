from fastapi import APIRouter
from models import UserBase, User, TokenResponse
from sqlalchemy.orm import Session
from user_schemas import UserCreate, UserResponse
from ..handler import user_handler
from auth_service.auth_service import register_user, login_user
from database import get_db

router = APIRouter(prefix="/auth", tags=["Kimlik Doğrulama"])
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydı"""
    new_user = register_user(user.username, user.password, db)
    return new_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    """Kullanıcı girişi"""
    return login_user(user.username, user.password, db)