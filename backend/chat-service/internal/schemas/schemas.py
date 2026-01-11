from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    message: str
    room_id: str = "default"
    use_rag: bool = False
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    room_id: str
    response: str

class HistoryResponse(BaseModel):
    user_id: int
    room_id: str
    messages: List[Dict]

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

class CategorizeRequest(BaseModel):
    text: str

class CategorizeResponse(BaseModel):
    category: str
    confidence: float

class TagsRequest(BaseModel):
    text: str

class TagsResponse(BaseModel):
    tags: List[str]