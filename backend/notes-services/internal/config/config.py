from dotenv import load_dotenv
import os

load_dotenv()

# JWT ayarları
SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_config():
    return {
        "SECRET_KEY": SECRET_KEY,  
        "ALGORITHM": ALGORITHM,
        "ACCESS_TOKEN_EXPIRE_MINUTES": ACCESS_TOKEN_EXPIRE_MINUTES
    }

class Settings:
    API_KEY: str = os.getenv("API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")  
    
    @staticmethod  
    def validate():
        if not Settings.API_KEY:
            raise ValueError("API_KEY bulunamadı! .env dosyasını kontrol edin.")
        if not Settings.DATABASE_URL:
            raise ValueError("DATABASE_URL bulunamadı!")
        if not Settings.SECRET_KEY:
            raise ValueError("SECRET_KEY bulunamadı!")
        if not Settings.API_URL:
            raise ValueError("API_URL bulunamadı!")

# Uygulama başlarken kontrol et
Settings.validate()

def get_settings() :
    return Settings()