from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.routers.auth_service_router import router as auth_router
from internal.routers.note_service_router import router as note_router

app = FastAPI(
    title="Notus API Gateway",
    description="Mikroservis mimarisi için API Gateway",
    version="2.0.0"
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
app.include_router(auth_router)
app.include_router(note_router)

@app.get("/")
def root():
    return {
        "message": "Notus API Gateway",
        "version": "2.0.0",
        "services": {
            "auth": "/auth",
            "notes": "/notes",
            "ai": "/ai"
        }
    }
