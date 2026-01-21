from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from internal.services import auth_service
from internal.database.database import get_db
from internal.schemas.user_schemas import UserCreate, UserLogin
from internal.auth.jwt_handler import create_access_token

router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Kullanıcı kaydı"""
    try:
        user = auth_service.register_user(db, user_data)
        return {
            "message": "Kullanıcı başarıyla oluşturuldu",
            "user": {"id": user.id, "username": user.username}
        }
    except HTTPException as e:
        raise e

@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Kullanıcı girişi"""
    try:
        user = auth_service.authenticate_user(db, user_data.username, user_data.password)
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"id": user.id, "username": user.username}
        }
    except HTTPException as e:
        raise e
