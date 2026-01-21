from internal.service.chat_service import ChatService

class ChatHandler:
    def __init__(self):
        self.service = ChatService()

    async def handle_chat(self, user_id, request):
        # Burada gerekirse ek validation yapılabilir
        return await self.service.process_chat(
            user_id, request.room_id, request.message, request.use_rag, request.system_prompt
        )