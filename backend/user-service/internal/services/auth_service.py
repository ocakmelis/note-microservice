from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from internal.repository import user_repository
from internal.schemas.user_schemas import UserCreate
from internal.models.user_models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Şifreyi hashle"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrula"""
    return pwd_context.verify(plain_password, hashed_password)

def register_user(db: Session, user_data: UserCreate) -> User:
    """Yeni kullanıcı kaydı"""
    # Kullanıcı adı kontrolü
    existing_user = user_repository.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu kullanıcı adı zaten kullanılıyor"
        )
    
    # Şifreyi hashle
    hashed_password = hash_password(user_data.password)
    
    # Kullanıcıyı oluştur
    user = user_repository.create_user(db, user_data.username, hashed_password)
    return user

def authenticate_user(db: Session, username: str, password: str) -> User:
    """Kullanıcı kimlik doğrulama"""
    user = user_repository.get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı"
        )
    
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı"
        )
    
    return user