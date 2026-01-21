from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
# Repository sınıfını import ediyoruz
from internal.repository.user_repository import UserRepository
from internal.schemas.user_schemas import UserCreate
from internal.models.user_models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    " İş mantığı (şifreleme, doğrulama) burada olur."
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        # 1. Kontrol: Repository üzerinden kullanıcıyı sor
        existing_user = UserRepository.get_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu kullanıcı adı zaten kullanılıyor"
            )
        
        # 2. İş mantığı: Şifreyi hashle
        hashed_pwd = AuthService.hash_password(user_data.password)
        
        # 3. Model objesini oluştur
        new_user_obj = User(
            username=user_data.username,
            email=user_data.email, # Schema'da varsa ekle
            password=hashed_pwd
        )
        
        # 4. Kayıt için Repository'ye gönder
        return UserRepository.create_user(db, new_user_obj)

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        user = UserRepository.get_by_username(db, username)
        
        if not user or not AuthService.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Kullanıcı adı veya şifre hatalı"
            )
        
        return user