"""
Authentication Router
Login, register ve token işlemleri
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import timedelta

from internal.database.database import get_db
from internal.utils.auth_utils import create_access_token
from internal.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Kullanıcı girişi yapar ve JWT token döndürür"""
    
    # Mock user (gerçek uygulamada database'den alınmalı)
    mock_user = {
        "id": 123,
        "username": "john_doe",
        "email": "user@example.com"
    }
    
    # Şifre kontrolü (gerçekte bcrypt ile yapılmalı!)
    if login_data.email != mock_user["email"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # JWT token oluştur
    access_token = create_access_token(
        data={
            "user_id": mock_user["id"],
            "email": mock_user["email"],
            "username": mock_user["username"]
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": mock_user["id"],
            "username": mock_user["username"],
            "email": mock_user["email"]
        }
    }


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Mevcut kullanıcının bilgilerini döndürür"""
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "username": current_user["username"]
    }
