from langchain_manager import LangChainManager

class ChatService:
    def __init__(self):
        self.ai = LangChainManager()
    
    async def process_chat(self, user_id, room_id, message, use_rag, system_prompt):
        return self.ai.chat(user_id, room_id, message, use_rag, system_prompt)

    async def get_summarization(self, text):
        return self.ai.summarize_text(text)
    
    