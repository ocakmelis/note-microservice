"""
Authentication dependencies
JWT Token'dan user bilgilerini alır ve doğrular
"""
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from internal.utils.auth_utils import verify_token

# Bearer token şeması
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    JWT token'dan current user bilgilerini alır
    
    Bu fonksiyon:
    1. Authorization header'dan Bearer token'ı alır
    2. Token'ı verify eder (şifresini çözer)
    3. User bilgilerini döndürür
    
    Kullanım:
        @router.get("/profile")
        def get_profile(current_user: dict = Depends(get_current_user)):
            user_id = current_user["user_id"]
            email = current_user["email"]
    
    Returns:
        dict: {
            "user_id": 123,
            "email": "user@example.com",
            "username": "john_doe"
        }
    
    Raises:
        HTTPException: Token yoksa, geçersizse veya expire olduysa
    """
    token = credentials.credentials
    
    # Token'ı verify et ve payload'u al
    payload = verify_token(token)
    
    # User bilgilerini kontrol et
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload. User ID not found.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "username": payload.get("username")
    }


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Sadece user_id döndürür (daha basit kullanım)
    
    Kullanım:
        @router.post("/notes")
        def create_note(
            note: NoteCreate,
            user_id: int = Depends(get_current_user_id)
        ):
            # user_id direkt kullanılabilir
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload. User ID not found.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user_id


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    Opsiyonel authentication - token yoksa None döner
    Public endpoint'ler için kullanılır
    
    Kullanım:
        @router.get("/public/notes")
        def get_public_notes(
            current_user: Optional[dict] = Depends(get_optional_current_user)
        ):
            if current_user:
                # Login olmuş kullanıcı
                user_id = current_user["user_id"]
            else:
                # Anonim kullanıcı
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        return {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "username": payload.get("username")
        }
    except:
        return None