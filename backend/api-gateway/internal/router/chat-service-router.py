from fastapi import APIRouter, Request, Header
from pydantic import BaseModel
from typing import Optional, List
import httpx
from internal.config.config import config

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    room_id: str = "default"
    use_rag: bool = False
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    room_id: str
    response: str

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    authorization: str = Header(...)
):
    """
    Chat yap
    
    - Hafızalı konuşma (user_id + room_id)
    - RAG desteği
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{config.CHAT_SERVICE_URL}/chat",
            json=request.dict(),
            headers={"Authorization": authorization}
        )
        response.raise_for_status()
        return response.json()

@router.get("/history/{room_id}")
async def get_chat_history(
    room_id: str,
    authorization: str = Header(...)
):
    """Chat geçmişini getir"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{config.CHAT_SERVICE_URL}/chat/history/{room_id}",
            headers={"Authorization": authorization}
        )
        response.raise_for_status()
        return response.json()

@router.delete("/history/{room_id}")
async def clear_chat_history(
    room_id: str,
    authorization: str = Header(...)
):
    """Chat geçmişini temizle"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.delete(
            f"{config.CHAT_SERVICE_URL}/chat/history/{room_id}",
            headers={"Authorization": authorization}
        )
        response.raise_for_status()
        return response.json()