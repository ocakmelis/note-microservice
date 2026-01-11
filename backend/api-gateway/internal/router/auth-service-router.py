from fastapi import APIRouter, Header
from typing import Optional
from pydantic import BaseModel
from internal.handlers.auth_service_handler import AuthServiceHandler

router = APIRouter(prefix="/auth", tags=["Authentication"])
handler = AuthServiceHandler()

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

@router.post("/register")
async def register(user_data: UserCreate):
    """Kullanıcı kaydı"""
    return await handler.register_user(user_data.dict())

@router.post("/login")
async def login(credentials: UserCreate):
    """Kullanıcı girişi"""
    return await handler.login_user(credentials.dict())

@router.get("/users/me")
async def get_current_user(authorization: str = Header(...)):
    """Mevcut kullanıcı bilgisi"""
    return await handler.get_current_user(authorization)

@router.put("/users/me")
async def update_user(user_data: UserUpdate, authorization: str = Header(...)):
    """Kullanıcı güncelle"""
    return await handler.update_user(authorization, user_data.dict(exclude_unset=True))

@router.delete("/users/me")
async def delete_user(authorization: str = Header(...)):
    """Kullanıcı sil"""
    await handler.delete_user(authorization)
    return {"message": "User deleted successfully"}