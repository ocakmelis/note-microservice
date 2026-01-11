import httpx
from fastapi import HTTPException, Request, Response
from typing import Optional
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from internal.config.config import config

logger = logging.getLogger(__name__)

class ChatServiceHandler:
    """Handler for Chat Service operations"""
    
    def __init__(self):
        self.base_url = config.CHAT_SERVICE_URL
        self.timeout = 30.0  # Chat için daha uzun timeout
    
    async def forward_request(
        self,
        path: str,
        method: str,
        request: Request,
        body: Optional[bytes] = None
    ) -> Response:
        """Forward request to Chat Service"""
        
        url = f"{self.base_url}{path}"
        
        if request.url.query:
            url = f"{url}?{request.url.query}"
        
        headers = dict(request.headers)
        headers.pop("host", None)
        
        logger.info(f"Forwarding {method} request to Chat Service: {url}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    content=body
                )
                
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.headers.get("content-type")
                )
                
            except httpx.ConnectError:
                logger.error(f"Chat Service connection error: {url}")
                raise HTTPException(
                    status_code=503,
                    detail="Chat Service yanıt vermiyor"
                )
            
            except httpx.TimeoutException:
                logger.error(f"Chat Service timeout: {url}")
                raise HTTPException(
                    status_code=504,
                    detail="Chat Service zaman aşımına uğradı"
                )
            
            except Exception as e:
                logger.error(f"Chat Service error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Chat Service hatası: {str(e)}"
                )
    
    async def chat(self, request: Request, body: bytes) -> Response:
        """Send chat message"""
        return await self.forward_request("/chat", "POST", request, body)
    
    async def get_chat_history(self, room_id: str, request: Request) -> Response:
        """Get chat history for a room"""
        return await self.forward_request(f"/chat/history/{room_id}", "GET", request)
    
    async def clear_chat_history(self, room_id: str, request: Request) -> Response:
        """Clear chat history for a room"""
        return await self.forward_request(f"/chat/history/{room_id}", "DELETE", request)

# Create singleton instance
chat_handler = ChatServiceHandler()