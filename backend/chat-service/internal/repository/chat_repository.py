from vector_store import VectorStore # Mevcut vector_store.py'yi kullanıyoruz

class ChatRepository:
    def __init__(self):
        self.db = VectorStore()
    
    def save_chat(self, user_id, room_id, role, content):
        return self.db.add_message(user_id, room_id, role, content)
        
    def get_history(self, user_id, room_id):
        return self.db.get_chat_history(user_id, room_id)

    def delete_history(self, user_id, room_id):
        return self.db.clear_room_history(user_id, room_id)