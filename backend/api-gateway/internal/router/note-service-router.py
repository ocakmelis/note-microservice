from fastapi import APIRouter, Request, Response
import httpx
from internal.config.config import config

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_notes(request: Request, path_name: str):
    """
    Note Service'e gelen tüm istekleri (oluşturma, listeleme, özetleme vb.) 
    hiçbir iş mantığı yürütmeden doğrudan iletir.
    """
    url = f"{config.NOTE_SERVICE_URL}/{path_name}"
    
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

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