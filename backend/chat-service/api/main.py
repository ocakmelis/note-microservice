from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from langchain_manager import LangChainManager
from schemas import (
    ChatRequest, ChatResponse, HistoryResponse,
    SummarizeRequest, SummarizeResponse,
    CategorizeRequest, CategorizeResponse,
    TagsRequest, TagsResponse
)
from auth import get_current_user_id

app = FastAPI(
    title="Chat Service",
    description="LangChain-based chat service with memory and RAG",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangChain Manager
chat_manager = LangChainManager()

@app.get("/")
def root():
    return {
        "service": "Chat Service",
        "version": "1.0.0",
        "status": "running",
        "features": ["LangChain", "OpenRouter", "Qdrant", "RAG"]
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

    # ==========================================
# chat-service/requirements.txt
# ==========================================
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
langchain==0.1.0
langchain-openai==0.0.2
langchain-community==0.0.10
qdrant-client==1.7.0
httpx==0.25.2

# ==========================================
# chat-service/.env
# ==========================================
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
DEFAULT_MODEL=openai/gpt-3.5-turbo
SECRET_KEY=super-secret-shared-key-for-all-services
ALGORITHM=HS256
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=chat_history

# ==========================================
# chat-service/Dockerfile
# ==========================================
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]

# ==========================================
# chat-service/config.py
# ==========================================
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL: str = "openai/gpt-3.5-turbo"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "chat_history"
    
    class Config:
        env_file = ".env"

settings = Settings()

# ==========================================
# chat-service/auth.py
# ==========================================
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import settings

security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """JWT token'dan user_id çıkar"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id = payload.get("user_id")
        if user_id:
            return int(user_id)
        
        return hash(username) % 1000000
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# ==========================================
# chat-service/vector_store.py
# ==========================================
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict
import hashlib
import json
from datetime import datetime
from config import settings

class VectorStore:
    """Qdrant Vector Store Manager"""
    
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Collection yoksa oluştur"""
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
    
    def _generate_id(self, user_id: int, room_id: str, message: str) -> str:
        """Unique ID oluştur"""
        content = f"{user_id}:{room_id}:{message}:{datetime.utcnow().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _create_embedding(self, text: str) -> List[float]:
        """
        Basit embedding oluştur (production'da OpenAI embedding kullanılmalı)
        Bu örnek için dummy embedding
        """
        # TODO: OpenAI/OpenRouter embedding API kullan
        import random
        random.seed(hash(text))
        return [random.random() for _ in range(1536)]
    
    def add_message(
        self,
        user_id: int,
        room_id: str,
        role: str,
        content: str,
        metadata: Dict = None
    ):
        """Mesajı vector store'a ekle"""
        
        point_id = self._generate_id(user_id, room_id, content)
        embedding = self._create_embedding(content)
        
        payload = {
            "user_id": user_id,
            "room_id": room_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload=payload
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
    
    def get_chat_history(
        self,
        user_id: int,
        room_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Chat geçmişini getir"""
        
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "user_id", "match": {"value": user_id}},
                    {"key": "room_id", "match": {"value": room_id}}
                ]
            },
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        
        messages = []
        for point in results[0]:
            payload = point.payload
            messages.append({
                "role": payload["role"],
                "content": payload["content"],
                "timestamp": payload["timestamp"]
            })
        
        # Timestamp'e göre sırala
        messages.sort(key=lambda x: x["timestamp"])
        return messages
    
    def search_similar(
        self,
        user_id: int,
        room_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """Benzer mesajları ara (RAG için)"""
        
        query_vector = self._create_embedding(query)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter={
                "must": [
                    {"key": "user_id", "match": {"value": user_id}},
                    {"key": "room_id", "match": {"value": room_id}}
                ]
            },
            limit=limit
        )
        
        return [
            {
                "content": hit.payload["content"],
                "role": hit.payload["role"],
                "score": hit.score,
                "timestamp": hit.payload["timestamp"]
            }
            for hit in results
        ]
    
    def clear_room_history(self, user_id: int, room_id: str):
        """Oda geçmişini temizle"""
        
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={
                "filter": {
                    "must": [
                        {"key": "user_id", "match": {"value": user_id}},
                        {"key": "room_id", "match": {"value": room_id}}
                    ]
                }
            }
        )

# ==========================================
# chat-service/langchain_manager.py
# ==========================================
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
from config import settings
from vector_store import VectorStore

class LangChainManager:
    """LangChain Chat Manager with Memory"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_MODEL,
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base=settings.OPENROUTER_BASE_URL,
            temperature=0.7,
            max_tokens=1000
        )
        self.vector_store = VectorStore()
        self.memories = {}  # user_id:room_id -> Memory
    
    def _get_memory_key(self, user_id: int, room_id: str) -> str:
        """Memory key oluştur"""
        return f"{user_id}:{room_id}"
    
    def _get_or_create_memory(self, user_id: int, room_id: str) -> ConversationBufferMemory:
        """Memory al veya oluştur"""
        key = self._get_memory_key(user_id, room_id)
        
        if key not in self.memories:
            memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
            
            # Vector store'dan geçmişi yükle
            history = self.vector_store.get_chat_history(user_id, room_id, limit=10)
            for msg in history:
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["content"])
                elif msg["role"] == "assistant":
                    memory.chat_memory.add_ai_message(msg["content"])
            
            self.memories[key] = memory
        
        return self.memories[key]
    
    def chat(
        self,
        user_id: int,
        room_id: str,
        message: str,
        use_rag: bool = False,
        system_prompt: str = None
    ) -> str:
        """Chat yapılandır"""
        
        memory = self._get_or_create_memory(user_id, room_id)
        messages = []
        
        # System prompt
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        else:
            messages.append(SystemMessage(
                content="You are a helpful AI assistant. Be concise and helpful."
            ))
        
        # RAG: Benzer geçmiş mesajları ekle
        if use_rag:
            similar_messages = self.vector_store.search_similar(
                user_id, room_id, message, limit=3
            )
            if similar_messages:
                context = "\n".join([
                    f"Previous context: {msg['content']}"
                    for msg in similar_messages
                ])
                messages.append(SystemMessage(
                    content=f"Relevant conversation history:\n{context}"
                ))
        
        # Memory'den chat history ekle
        history = memory.load_memory_variables({})
        for msg in history.get("chat_history", []):
            messages.append(msg)
        
        # Kullanıcı mesajı ekle
        messages.append(HumanMessage(content=message))
        
        # LLM'den yanıt al
        response = self.llm.invoke(messages)
        assistant_message = response.content
        
        # Memory'yi güncelle
        memory.chat_memory.add_user_message(message)
        memory.chat_memory.add_ai_message(assistant_message)
        
        # Vector store'a kaydet
        self.vector_store.add_message(user_id, room_id, "user", message)
        self.vector_store.add_message(user_id, room_id, "assistant", assistant_message)
        
        return assistant_message
    
    def get_history(self, user_id: int, room_id: str) -> List[Dict]:
        """Chat geçmişini getir"""
        return self.vector_store.get_chat_history(user_id, room_id)
    
    def clear_history(self, user_id: int, room_id: str):
        """Chat geçmişini temizle"""
        key = self._get_memory_key(user_id, room_id)
        if key in self.memories:
            del self.memories[key]
        
        self.vector_store.clear_room_history(user_id, room_id)
    
    def summarize_text(self, text: str) -> str:
        """Metni özetle"""
        prompt = f"Please summarize the following text concisely:\n\n{text}"
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def categorize_text(self, text: str) -> Dict:
        """Metni kategorize et"""
        prompt = f"""Categorize the following text into one of these categories:
        - Work
        - Personal
        - Study
        - Ideas
        - Todo
        - General
        
        Text: {text}
        
        Respond with just the category name and a confidence score (0-1).
        Format: Category: <name>, Confidence: <score>
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        result = response.content
        
        # Parse response
        try:
            parts = result.split(",")
            category = parts[0].split(":")[1].strip()
            confidence = float(parts[1].split(":")[1].strip())
            return {"category": category, "confidence": confidence}
        except:
            return {"category": "General", "confidence": 0.5}
    
    def generate_tags(self, text: str) -> List[str]:
        """Tag'ler oluştur"""
        prompt = f"""Generate 3-5 relevant tags for the following text.
        Return only the tags separated by commas, lowercase, no hashtags.
        
        Text: {text}
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        tags_str = response.content.strip()
        
        # Parse tags
        tags = [tag.strip().lower() for tag in tags_str.split(",")]
        return tags[:5]  # Max 5 tags

# ==========================================
# chat-service/schemas.py
# ==========================================
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

# ==========================================
# chat-service/main.py
# ==========================================
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from langchain_manager import LangChainManager
from schemas import (
    ChatRequest, ChatResponse, HistoryResponse,
    SummarizeRequest, SummarizeResponse,
    CategorizeRequest, CategorizeResponse,
    TagsRequest, TagsResponse
)
from auth import get_current_user_id

app = FastAPI(
    title="Chat Service",
    description="LangChain-based chat service with memory and RAG",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangChain Manager
chat_manager = LangChainManager()

@app.get("/")
def root():
    return {
        "service": "Chat Service",
        "version": "1.0.0",
        "status": "running",
        "features": ["LangChain", "OpenRouter", "Qdrant", "RAG"]
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# ============ CHAT ENDPOINTS ============

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id)
):
    """
    Chat yap (hafızalı)
    
    - user_id ve room_id ile conversation tracking
    - RAG desteği (use_rag=true)
    - Custom system prompt
    """
    try:
        response = chat_manager.chat(
            user_id=user_id,
            room_id=request.room_id,
            message=request.message,
            use_rag=request.use_rag,
            system_prompt=request.system_prompt
        )
        
        return ChatResponse(
            message=request.message,
            room_id=request.room_id,
            response=response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )

@app.get("/chat/history/{room_id}", response_model=HistoryResponse)
async def get_chat_history(
    room_id: str,
    user_id: int = Depends(get_current_user_id)
):
    """Chat geçmişini getir"""
    try:
        messages = chat_manager.get_history(user_id, room_id)
        
        return HistoryResponse(
            user_id=user_id,
            room_id=room_id,
            messages=messages
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"History error: {str(e)}"
        )

@app.delete("/chat/history/{room_id}")
async def clear_chat_history(
    room_id: str,
    user_id: int = Depends(get_current_user_id)
):
    """Chat geçmişini temizle"""
    try:
        chat_manager.clear_history(user_id, room_id)
        return {"message": f"History cleared for room {room_id}"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Clear history error: {str(e)}"
        )

# ============ AI UTILITY ENDPOINTS ============

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    """Metni özetle (Note Service için)"""
    try:
        summary = chat_manager.summarize_text(request.text)
        return SummarizeResponse(summary=summary)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Summarize error: {str(e)}"
        )

@app.post("/categorize", response_model=CategorizeResponse)
async def categorize_text(request: CategorizeRequest):
    """Metni kategorize et (Note Service için)"""
    try:
        result = chat_manager.categorize_text(request.text)
        return CategorizeResponse(
            category=result["category"],
            confidence=result["confidence"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Categorize error: {str(e)}"
        )

@app.post("/generate-tags", response_model=TagsResponse)
async def generate_tags(request: TagsRequest):
    """Tag'ler oluştur (Note Service için)"""
    try:
        tags = chat_manager.generate_tags(request.text)
        return TagsResponse(tags=tags)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generate tags error: {str(e)}"
        )