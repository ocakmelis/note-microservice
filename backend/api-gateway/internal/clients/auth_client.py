import httpx
from internal.config.config import config


class AuthClient:
    """Auth Service HTTP Client"""

    @staticmethod
    async def request(method: str, path: str, headers: dict, json: dict | None = None):
        async with httpx.AsyncClient(
            base_url=config.AUTH_SERVICE_URL,
            timeout=config.REQUEST_TIMEOUT
        ) as client:
            response = await client.request(
                method=method,
                url=path,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return response.json()
