import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # Service URLs
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
    NOTE_SERVICE_URL: str = os.getenv("NOTE_SERVICE_URL", "http://note-service:8002")
    CHAT_SERVICE_URL: str = os.getenv("CHAT_SERVICE_URL", "http://chat-service:8003")
    
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-shared-key-for-all-services")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Timeouts
    REQUEST_TIMEOUT: float = 10.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True

config = Config()