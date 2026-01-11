from fastapi import APIRouter, Request
from internal.handlers.user_service_handler import user_handler

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register_user(request: Request):
    """
    Yeni kullanıcı kaydı
    
    Body:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    """
    body = await request.body()
    return await user_handler.register_user(request, body)

@router.post("/login")
async def login_user(request: Request):
    """
    Kullanıcı girişi
    
    Body:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns: JWT token
    """
    body = await request.body()
    return await user_handler.login_user(request, body)

@router.get("/me")
async def get_current_user(request: Request):
    """
    Mevcut kullanıcı bilgilerini getir
    
    Headers:
        Authorization: Bearer <token>
    """
    return await user_handler.get_current_user(request)

@router.get("")
async def get_all_users(request: Request):
    """
    Tüm kullanıcıları listele (Admin only)
    
    Headers:
        Authorization: Bearer <token>
    """
    return await user_handler.get_all_users(request)

@router.get("/{user_id}")
async def get_user_by_id(user_id: int, request: Request):
    """
    Belirli bir kullanıcıyı ID ile getir
    
    Headers:
        Authorization: Bearer <token>
    """
    return await user_handler.get_user_by_id(user_id, request)

@router.put("/{user_id}")
async def update_user(user_id: int, request: Request):
    """
    Kullanıcı bilgilerini güncelle
    
    Body:
    {
        "email": "string (optional)",
        "password": "string (optional)",
        "is_active": "boolean (optional)"
    }
    
    Headers:
        Authorization: Bearer <token>
    """
    body = await request.body()
    return await user_handler.update_user(user_id, request, body)

@router.delete("/{user_id}")
async def delete_user(user_id: int, request: Request):
    """
    Kullanıcıyı sil (soft delete)
    
    Headers:
        Authorization: Bearer <token>
    """
    return await user_handler.delete_user(user_id, request)

@router.delete("/{user_id}/permanent")
async def permanently_delete_user(user_id: int, request: Request):
    """
    Kullanıcıyı kalıcı olarak sil (Admin only)
    
    Headers:
        Authorization: Bearer <token>
    """
    return await user_handler.permanently_delete_user(user_id, request)