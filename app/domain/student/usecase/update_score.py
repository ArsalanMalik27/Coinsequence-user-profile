from uuid import UUID

import structlog

from app.api.api_v1.student.dto.score import UpdateScoreDTO
from app.domain.student.data.score import CreateScoreProps, Score, ScoreProps
from app.domain.student.repository.db.score import ScoreRepository
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


async def update_score_usecase(
    profile_id: UUID,
    score_id: UUID,
    update_score_dto: UpdateScoreDTO,
    score_repo: ScoreRepository,
) -> ScoreProps:
    existing_score = await score_repo.get_by_id(score_id)
    if not existing_score or existing_score.profile_id != profile_id:
        logger.info(
            "[UpdateScoreUsecase: attempt to update non-existing Score]",
            data=update_score_dto,
        )
        raise DomainError("Invalid Score")

    score_updated_props = CreateScoreProps(**update_score_dto.dict())
    score = Score(props=existing_score)
    score.update_from(score_updated_props)
    await score_repo.update_score(score.props)
    return score.props
