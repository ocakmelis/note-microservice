from fastapi import Request, HTTPException
import logging

logger = logging.getLogger("note-service-auth")


async def note_auth_middleware(request: Request, call_next):
    """
    API Gateway'den gelen X-User-ID header'ını okur ve request.state'e kaydeder
    """
    # Health check ve docs endpoint'lerini atla
    if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    # X-User-ID header'ını al
    user_id = request.headers.get("X-User-ID")
    
    if not user_id:
        logger.warning(f"Request without X-User-ID header: {request.url.path}")
        raise HTTPException(
            status_code=401,
            detail="User authentication required"
        )
    
    try:
        # User ID'yi integer'a çevir ve request.state'e kaydet
        request.state.user_id = int(user_id)
        
        # Opsiyonel: Diğer kullanıcı bilgilerini de kaydet
        if username := request.headers.get("X-Username"):
            request.state.username = username
        if email := request.headers.get("X-Email"):
            request.state.email = email
        
        logger.info(f"Authenticated request for user: {user_id}")
        
    except ValueError:
        logger.error(f"Invalid X-User-ID format: {user_id}")
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format"
        )
    
    response = await call_next(request)
    return response