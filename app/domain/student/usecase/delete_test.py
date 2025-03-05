import structlog
from uuid import UUID

from app.domain.student.repository.db.test import TestRepository
from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def delete_test_usecase(
    profile_id: UUID,
    test_id: UUID,
    test_repo: TestRepository,
) -> None:
    existing_test = await test_repo.get_by_test_id(test_id)
    if not existing_test or existing_test.profile_id != profile_id:
        logger.info(
            "[DeleteTestUsecase: attempt to Delete non-existing Test]",
            data=test_id,
        )
        raise DomainError("attempt to Delete non-existing test")

    await test_repo.delete(test_id)
