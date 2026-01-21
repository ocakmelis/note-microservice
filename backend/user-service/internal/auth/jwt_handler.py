from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from internal.config.config import Settings

class JWTHandler:
    """
    Sadece token oluşturma ve parse etme işini yapar.
    İş mantığı ve veritabanı sorgusu barındırmaz.
    """
    
    @staticmethod
    def create_access_token(username: str, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": username,
            "user_id": user_id,
            "exp": expire
        }
        return jwt.encode(payload, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token süresi dolmuş")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Geçersiz token")