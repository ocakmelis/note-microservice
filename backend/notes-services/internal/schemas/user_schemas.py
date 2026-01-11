from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    """Kullanıcı oluşturma request"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    """Kullanıcı response"""
    id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    