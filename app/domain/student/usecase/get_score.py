from uuid import UUID
from typing import List

import structlog

from app.domain.student.data.score import ScoreProps
from app.domain.student.repository.db.score import ScoreRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def get_score_usecase(
    profile_id: UUID,
    score_repo: ScoreRepository,
) -> List:
    score_list = await score_repo.get_score_list(profile_id)
    return score_list
