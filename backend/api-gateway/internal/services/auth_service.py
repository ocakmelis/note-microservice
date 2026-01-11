from internal.clients.auth_client import AuthClient

class AuthService:

    @staticmethod
    async def register(data: dict, headers: dict):
        return await AuthClient.request("POST", "/api/auth/register", headers, data)

    @staticmethod
    async def login(data: dict, headers: dict):
        return await AuthClient.request("POST", "/api/auth/login", headers, data)

    @staticmethod
    async def me(headers: dict):
        return await AuthClient.request("GET", "/api/auth/me", headers)

    @staticmethod
    async def update(data: dict, headers: dict):
        return await AuthClient.request("PUT", "/api/auth/me", headers, data)
