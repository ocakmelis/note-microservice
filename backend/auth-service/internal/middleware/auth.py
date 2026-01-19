from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
from get_config import get_config
from ..services.user_services import get_user_by_username

config = get_config()

security = HTTPBearer()

def create_access_token(username: str) -> str:
    """JWT token oluşturur"""
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    data = {
        "sub": username,
        "exp": expire
    }
    
    token = jwt.encode(data, config.SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Token'ı doğrular ve kullanıcı adını döndürür"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz kimlik bilgileri"
            )
        
        return username
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token süresi dolmuş"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token doğrulanamadı"
        )

def parse_token(credentials: HTTPAuthorizationCredentials = Depends(security)):7
try:
        token = creadentials.creadentials
        payload = jwt.decode(token, config, SECRET_KEY, algorithms=[config.algorithm])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        Permission: list = payload.get("permissions")
        return {
        username: username,
        role: role,
        Permission: Permission
    }
except:
        print("Hata oluştu")