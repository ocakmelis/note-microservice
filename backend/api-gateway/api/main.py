from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.routers.auth_service_router import router as auth_router 
from internal.routers.note_service_router import router as note_router
from internal.routers.chat_service_router import router as chat_router

app = FastAPI(
    title="Notus API Gateway",
    description="Mikroservis mimarisi için API Gateway - Sadece Yönlendirme Katmanı",
    version="3.0.0"
)

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotalar iş mantığı barındırmadan ilgili servislere proxy görevi görür.
app.include_router(auth_router, prefix="/auth", tags=["Auth & User"])
app.include_router(note_router, prefix="/notes", tags=["Notes"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {
        "message": "Notus API Gateway",
        "status": "Running",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "api-gateway"
    }