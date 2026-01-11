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
    path = request.url.path

    # Public endpoint kontrolü
    if any(path.startswith(p) for p in PUBLIC_PATHS):
        return await call_next(request)

    # Authorization header kontrolü
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Auth service doğrulama
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{config.AUTH_SERVICE_URL}/auth/verify",
                headers={"Authorization": auth_header}
            )

            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")

    except httpx.ConnectError:
        logger.error("Auth service unreachable")
        raise HTTPException(status_code=503, detail="Auth service unavailable")

    return await call_next(request)
