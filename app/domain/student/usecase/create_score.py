from uuid import UUID

import structlog

from app.api.api_v1.student.dto.score import CreateScoreDTO
from app.domain.student.data.score import CreateScoreProps, Score, ScoreProps
from app.domain.student.repository.db.score import ScoreRepository

logger = structlog.get_logger()


async def create_score_usecase(
    profile_id: UUID,
    create_score_dto: CreateScoreDTO,
    education_repo: ScoreRepository,
) -> ScoreProps:
    score_props = CreateScoreProps(**create_score_dto.dict())
    score = Score.create_from(props=score_props, profile_id=profile_id)
    await education_repo.create(score.props)
    return score.props
