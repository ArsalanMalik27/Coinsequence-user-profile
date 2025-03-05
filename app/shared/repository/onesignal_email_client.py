from typing import Any
from uuid import UUID

import httpx

from app.infra.config import settings
from app.shared.domain.repository.email_client import EmailClient


class OneSignalEmailClient(EmailClient):
    def __init__(self) -> None:
        self._rest_api_key = settings.ONESIGNAL_API_KEY
        self._base_endpoint = settings.ONESIGNAL_BASE_ENDPOINT

    def _get_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Basic {self._rest_api_key}",
            "Content-Type": "application/json",
        }

    async def add_user(
        self,
        id: UUID,
        email: str,
        first_name: str,
        last_name: str,
        token: str,
    ) -> None:
        async with httpx.AsyncClient() as client:
            data = {
                "app_id": settings.ONESIGNAL_APP_ID,
                "device_type": 11,
                "identifier": email,
                "language": "en",
                "tags": {
                    "token": token,
                },
                "external_user_id": str(id),
            }
            await client.post(
                f"{self._base_endpoint}/players",
                json=data,
                headers=self._get_headers(),
            )

    async def update_tags(
        self,
        id: UUID,
        tags: dict[str, Any],
    ) -> None:
        async with httpx.AsyncClient() as client:
            await client.put(
                f"{self._base_endpoint}/apps/{settings.ONESIGNAL_APP_ID}/users/{id}",
                json={"tags": tags},
                headers=self._get_headers(),
            )

    async def send_mail(
        self, to: str, external_user_id: UUID, template_id: str
    ) -> None:
        async with httpx.AsyncClient() as client:
            data = {
                "app_id": settings.ONESIGNAL_APP_ID,
                "include_email_tokens": [to],
                "channel_for_external_user_ids": "email",
                "template_id": template_id,
                "external_user_id": str(external_user_id),
            }
            await client.post(
                f"{self._base_endpoint}/notifications",
                json=data,
                headers=self._get_headers(),
            )
