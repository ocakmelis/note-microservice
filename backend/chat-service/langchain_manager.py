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
