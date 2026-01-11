from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.routers import user_router, note_router, ai_router

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Notus API",
    description="Yapay zeka destekli not alma uygulaması",
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

# Routerları ekle
app.include_router(user_router.router)
app.include_router(note_router.router)
app.include_router(ai_router.router)
app.include_router(router.router)

@app.get("/")
def root():
    """Ana sayfa"""
    return {
        "message": "Notus API'ye hoş geldiniz!",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# uvicorn main:app --reload
