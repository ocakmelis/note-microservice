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
    title="Auth & User Service",
    description= '',
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefixleri sadeleştiriyoruz ki Gateway kolayca yönlendirsin
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)