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