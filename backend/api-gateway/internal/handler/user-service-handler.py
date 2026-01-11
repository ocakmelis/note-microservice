import httpx
from fastapi import HTTPException, Request, Response
from typing import Optional
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from internal.config.config import config

logger = logging.getLogger(__name__)

class UserServiceHandler:
    """Handler for User Service operations"""
    
    def __init__(self):
        self.base_url = config.USER_SERVICE_URL
        self.timeout = config.REQUEST_TIMEOUT
    
    async def forward_request(
        self,
        path: str,
        method: str,
        request: Request,
        body: Optional[bytes] = None
    ) -> Response:
        """
        Forward request to User Service
        
        Args:
            path: API path (e.g., '/users/register')
            method: HTTP method (GET, POST, PUT, DELETE)
            request: FastAPI Request object
            body: Request body (optional)
        
        Returns:
            Response from User Service
        """
        
        # Build full URL
        url = f"{self.base_url}{path}"
        
        # Add query parameters if any
        if request.url.query:
            url = f"{url}?{request.url.query}"
        
        # Prepare headers
        headers = dict(request.headers)
        headers.pop("host", None)  # Remove host header
        
        logger.info(f"Forwarding {method} request to User Service: {url}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    content=body
                )
                
                # Return response
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.headers.get("content-type")
                )
                
            except httpx.ConnectError:
                logger.error(f"User Service connection error: {url}")
                raise HTTPException(
                    status_code=503,
                    detail="User Service yanıt vermiyor"
                )
            
            except httpx.TimeoutException:
                logger.error(f"User Service timeout: {url}")
                raise HTTPException(
                    status_code=504,
                    detail="User Service zaman aşımına uğradı"
                )
            
            except Exception as e:
                logger.error(f"User Service error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"User Service hatası: {str(e)}"
                )
    
    async def register_user(self, request: Request, body: bytes) -> Response:
        """Register new user"""
        return await self.forward_request("/users/register", "POST", request, body)
    
    async def login_user(self, request: Request, body: bytes) -> Response:
        """Login user"""
        return await self.forward_request("/users/login", "POST", request, body)
    
    async def get_current_user(self, request: Request) -> Response:
        """Get current user info"""
        return await self.forward_request("/users/me", "GET", request)
    
    async def get_all_users(self, request: Request) -> Response:
        """Get all users (Admin only)"""
        return await self.forward_request("/users", "GET", request)
    
    async def get_user_by_id(self, user_id: int, request: Request) -> Response:
        """Get user by ID"""
        return await self.forward_request(f"/users/{user_id}", "GET", request)
    
    async def update_user(self, user_id: int, request: Request, body: bytes) -> Response:
        """Update user"""
        return await self.forward_request(f"/users/{user_id}", "PUT", request, body)
    
    async def delete_user(self, user_id: int, request: Request) -> Response:
        """Delete user (soft delete)"""
        return await self.forward_request(f"/users/{user_id}", "DELETE", request)
    
    async def permanently_delete_user(self, user_id: int, request: Request) -> Response:
        """Permanently delete user (Admin only)"""
        return await self.forward_request(f"/users/{user_id}/permanent", "DELETE", request)

# Create singleton instance
user_handler = UserServiceHandler()