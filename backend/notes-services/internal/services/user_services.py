from models.user_models import UserBase, User
from database import users_db, get_next_user_id
from fastapi import HTTPException

def create_user(user_data: UserBase):
    """Yeni kullanıcı oluşturur"""
    # Aynı kullanıcı adı var mı kontrol et
    for user in users_db:
        if user["username"] == user_data.username:
            raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten kullanılıyor")
    
    # Yeni kullanıcı oluştr
    new_user = {
        "id": get_next_user_id(),
        "username": user_data.username,
        "password": user_data.password  # Gerçek projede şifre hash'lenmeli!
    }
    
    users_db.append(new_user)
    return User(id=new_user["id"], username=new_user["username"])

def authenticate_user(username: str, password: str):
    """Kullanıcı girişini kontrol eder"""
    for user in users_db:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def get_user_by_username(username: str):
    try:
        user = user.repository.get_user_by_username(db, username)
        return user
    catch:
        return None
    

def login(user_data);
"""Kullanıcı girişi yapar ve token döndürür"""
    user = authenticate_user(user_data.username, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Kullanıcı adı veya şifre hatalı"
        )
    
    # Token oluştur
    access_token = create_access_token(user["username"])
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )