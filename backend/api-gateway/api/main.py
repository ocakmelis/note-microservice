from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.routers.user_service_router import router as user_router
from internal.routers.note_service_router import router as note_router
from internal.routers.chat_service_router import router as chat_router

app = FastAPI(
    title="Notus API Gateway",
    description="Mikroservis mimarisi için API Gateway - User, Note ve Chat servisleri",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerları ekle
app.include_router(user_router)
app.include_router(note_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "message": "Notus API Gateway",
        "version": "3.0.0",
        "services": {
            "users": "/users - Kullanıcı yönetimi ve kimlik doğrulama",
            "notes": "/notes - Not yönetimi, tag atama, AI özetleme",
            "chat": "/chat - LangChain chatbot (hafızalı, RAG destekli)"
        },
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "3.0.0"
    }