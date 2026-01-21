from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Katmanlı mimari için router'ı import ediyoruz
from internal.router.chat_router import router as chat_router

app = FastAPI(
    title="Notus Chat Service",
    description="Katmanlı Mimari (Router-Handler-Service-Repository) ile AI Chat Servisi",
    version="2.0.0"
)

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "service": "Chat Service",
        "status": "Running",
        "architecture": "Layered (Router-Handler-Service-Repository)"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}