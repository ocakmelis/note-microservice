from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from internal.routers import note_router, auth_router
from internal.database.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Note Service",
    description="Not yönetimi mikroservisi - JWT Auth",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(note_router.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Note Service with JWT Auth", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "note-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003)
