import httpx
from fastapi import Request, HTTPException
from internal.config.config import config
import logging

logger = logging.getLogger("api-gateway-auth")

# Public endpoint'ler (token istemez)
PUBLIC_PATHS = [
    "/api/auth/login",
    "/api/auth/register",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/"
]


async def auth_middleware(request: Request, call_next):
    """
    Auth middleware - Token doğrulama ve user_id'yi request.state'e kaydetme
    """
    path = request.url.path

    # Public endpoint kontrolü
    if any(path.startswith(p) for p in PUBLIC_PATHS):
        return await call_next(request)

    # Authorization header kontrolü
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(
            status_code=401, 
            detail="Authorization header missing"
        )

    # Auth service ile token doğrulama
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{config.AUTH_SERVICE_URL}/auth/verify",
                headers={"Authorization": auth_header}
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, 
                    detail="Invalid or expired token"
                )
            
            # Auth service'den dönen user bilgisini al
            user_data = response.json()
            
            # User ID'yi request.state'e kaydet
            # Böylece downstream servisler kullanabilir
            request.state.user_id = user_data.get("user_id")
            request.state.username = user_data.get("username")
            request.state.email = user_data.get("email")
            
            logger.info(f"User authenticated: {request.state.user_id}")

    except httpx.ConnectError:
        logger.error("Auth service unreachable")
        raise HTTPException(
            status_code=503, 
            detail="Auth service unavailable"
        )
    except httpx.TimeoutException:
        logger.error("Auth service timeout")
        raise HTTPException(
            status_code=504, 
            detail="Auth service timeout"
        )
    except Exception as e:
        logger.error(f"Auth middleware error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal authentication error"
        )

    response = await call_next(request)
    return response