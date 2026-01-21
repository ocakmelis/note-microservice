from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Internal modülleri import edebilmek için path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from internal.routers import note_router
from internal.database.database import engine, Base

# Database tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Note Service",
    description="Not yönetimi mikroservisi",
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

# Router'ları ekle (SADECE note router)
app.include_router(note_router.router, prefix="/api/v1/notes", tags=["notes"])

@app.get("/")
async def root():
    return {"message": "Note Service is running", "service": "note-service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "note-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003)




