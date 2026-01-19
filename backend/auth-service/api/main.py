from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
import sys
import os

# Internal modülleri import edebilmek için path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from internal.services import auth_service
from internal.database.database import get_db
from internal.schemas.user_schemas import UserCreate, UserLogin
from internal.auth.jwt_handler import create_access_token

app = FastAPI(
    title="Auth Service",
    description="Kimlik doğrulama mikroservisi",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.post("/api/v1/auth/register", tags=["auth"])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydı"""
    try:
        user = auth_service.register_user(db, user_data)
        return {
            "message": "Kullanıcı başarıyla oluşturuldu",
            "user": {
                "id": user.id,
                "username": user.username
            }
        }
    except HTTPException as e:
        raise e

@app.post("/api/v1/auth/login", tags=["auth"])
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Kullanıcı girişi"""
    try:
        user = auth_service.authenticate_user(db, user_data.username, user_data.password)
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username
            }
        }
    except HTTPException as e:
        raise e

@app.get("/", tags=["root"])
async def root():
    return {"message": "Auth Service is running", "service": "auth-service"}

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "auth-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
