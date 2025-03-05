from typing import Any
import httpx
from uuid import UUID
from app.masterdata_shared.config import masterdata_settings

from .domain.client import MasterdataClient
from .domain.data import TestProps, CourseProps
from app.shared.utils.error import DomainError


class MasterdataAPIClient(MasterdataClient):
    def __init__(self) -> None:
        self._endpoint = (
            f"{masterdata_settings.BASE_URL}{masterdata_settings.API_V1_STR}"
        )

    def _get_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def get_test(self, test_id: UUID) -> TestProps:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self._endpoint}/test/{test_id}",
                headers=self._get_headers(),
            )
            if res.status_code != 200:
                raise DomainError("Invalid MasterData Service")
            result: dict[str, Any] = res.json()
            test_props = TestProps.parse_obj(result)
            return test_props