import httpx
from internal.config.config import config

class NoteServiceClient:
    """Note Service ile HTTP iletişimini yöneten client"""

    @staticmethod
    async def create(data: dict):
        return await NoteServiceClient._request(
            method="POST",
            path="/notes",
            json=data
        )

    @staticmethod
    async def get(note_id: int):
        return await NoteServiceClient._request(
            method="GET",
            path=f"/notes/{note_id}"
        )

    @staticmethod
    async def assign_tags(note_id: int, tags: list[str]):
        return await NoteServiceClient._request(
            method="POST",
            path=f"/notes/{note_id}/tags",
            json={"tags": tags}
        )

    @staticmethod
    async def summarize(note_id: int):
        return await NoteServiceClient._request(
            method="POST",
            path=f"/notes/{note_id}/summary"
        )

    @staticmethod
    async def _request(method: str, path: str, **kwargs):
        async with httpx.AsyncClient(
            base_url=config.NOTE_SERVICE_URL,
            timeout=config.REQUEST_TIMEOUT
        ) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
