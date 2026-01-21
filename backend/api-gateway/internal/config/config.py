import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # Service URLs -  User ve Auth servisleri birleşti
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
    NOTE_SERVICE_URL: str = os.getenv("NOTE_SERVICE_URL", "http://note-service:8002")
    CHAT_SERVICE_URL: str = os.getenv("CHAT_SERVICE_URL", "http://chat-service:8003")
    
    # Auth - Gateway'in gelen isteği doğrulaması (Authentication) için gerekli
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secure-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Timeouts - Yönlendirme (Proxy) sırasında kullanılacak zaman aşımı
    REQUEST_TIMEOUT: float = 10.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True

config = Config()