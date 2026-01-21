from fastapi import APIRouter, Depends
from internal.handler.chat_handler import ChatHandler
from schemas import ChatRequest, ChatResponse
from auth import get_current_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])
handler = ChatHandler()

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, user_id: int = Depends(get_current_user_id)):
    response = await handler.handle_chat(user_id, request)
    return ChatResponse(message=request.message, room_id=request.room_id, response=response)