from fastapi import FastAPI
from user_router import router as user_router
from ai_router import router as ai_router
from note_router import router as note_router

app = FastAPI()

app.include_router(user_router)
app.include_router(ai_router)
app.include_router(note_router)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
