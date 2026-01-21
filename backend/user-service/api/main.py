cat > user-service/api/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Internal modülleri import edebilmek için path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from internal.routers import user_router, auth_router
from internal.database.database import engine, Base

# Database tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service",
    description="Kullanıcı yönetimi ve kimlik doğrulama mikroservisi",
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

# Router'ları ekle
app.include_router(user_router.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {
        "message": "User Service is running",
        "service": "user-service",
        "endpoints": {
            "users": "/api/v1/users",
            "auth": "/api/v1/auth"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
EOF