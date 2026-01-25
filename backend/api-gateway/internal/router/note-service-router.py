from fastapi import APIRouter, Request, Response, HTTPException
import httpx
from internal.config.config import config
import logging

logger = logging.getLogger("api-gateway-note-router")

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_notes(request: Request, path_name: str):
    """
    Note Service'e gelen tüm istekleri iletir.
    Auth middleware'den gelen user_id'yi custom header ile note-service'e gönderir.
    """
    # Middleware'den user_id'yi al
    user_id = getattr(request.state, "user_id", None)
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated"
        )
    
    # Note service URL'i oluştur
    url = f"{config.NOTE_SERVICE_URL}/{path_name}"
    
    # Request body ve headers'ı al
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    
    # User ID'yi custom header olarak ekle
    # Note service bu header'ı okuyacak
    headers["X-User-ID"] = str(user_id)
    
    # Opsiyonel: Username ve email de gönderilebilir
    if hasattr(request.state, "username"):
        headers["X-Username"] = request.state.username
    if hasattr(request.state, "email"):
        headers["X-Email"] = request.state.email
    
    try:
        async with httpx.AsyncClient() as client:
            proxy_response = await client.request(
                method=request.method,
                url=url,
                params=request.query_params,
                content=body,
                headers=headers,
                timeout=config.REQUEST_TIMEOUT
            )
            
        return Response(
            content=proxy_response.content,
            status_code=proxy_response.status_code,
            headers=dict(proxy_response.headers)
        )
        
    except httpx.ConnectError:
        logger.error(f"Note service unreachable: {url}")
        raise HTTPException(
            status_code=503,
            detail="Note service unavailable"
        )
    except httpx.TimeoutException:
        logger.error(f"Note service timeout: {url}")
        raise HTTPException(
            status_code=504,
            detail="Note service timeout"
        )
    except Exception as e:
        logger.error(f"Proxy error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal gateway error"
        )