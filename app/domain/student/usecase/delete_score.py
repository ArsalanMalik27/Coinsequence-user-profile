import structlog
from uuid import UUID
from app.api.api_v1.student.dto.score import UpdateScoreDTO
from app.domain.student.data.score import (
    CreateScoreProps,
    Score,
    ScoreProps,
)
from app.domain.student.repository.db.score import ScoreRepository
from app.infra.config import settings
from app.shared.repository.event_client import EventClient
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def delete_score_usecase(
    profile_id: UUID,
    score_id: UUID,
    score_repo: ScoreRepository,
) -> None:
    existing_score = await score_repo.get_by_id(score_id)
    if not existing_score or existing_score.profile_id != profile_id:
        logger.info(
            "[DeleteScoreUsecase: attempt to Delete non-existing Score]",
            data=score_id,
        )
        raise DomainError("attempt to Delete non-existing Score")

    await score_repo.delete(score_id)
