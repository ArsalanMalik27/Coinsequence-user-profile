from uuid import UUID

import structlog

from app.api.api_v1.student.dto.work import UpdateWorkDTO

from app.api.api_v1.student.dto.work import (
    CreateWorkDTO,
    WorkResponseDTO,
    UpdateWorkDTO
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.work import WorkProps,CreateWorkProps,Work
from app.domain.student.repository.db.work import WorkRepository
from app.shared.utils.error import DomainError
from datetime import datetime

logger = structlog.get_logger()


async def update_work_usecase(
    work_id: UUID,
    update_work_dto: UpdateWorkDTO,
    work_repo: WorkRepository,
    user_profile_props: UserProfileProps,
) -> WorkProps:
    current_date = datetime.now().date()
    if update_work_dto.start_date >= update_work_dto.end_date or update_work_dto.start_date > current_date:
        raise DomainError("Invalid Date Range")
    if len(update_work_dto.description) > 600:
        raise DomainError("Description is too long")
    existing_work = await work_repo.get_by_id(work_id)
    if not existing_work or existing_work.profile_id != user_profile_props.id:
        logger.info(
            "[UpdateWorkUsecase: attempt to update non-existing Work]",
            data=user_profile_props,
        )
        raise DomainError("Invalid Work")

    update_work_props = CreateWorkProps(**update_work_dto.dict())
    work_props = Work(props=existing_work)
    work_props.update_from(update_work_props)
    await work_repo.update_work(work_props.props, user_profile_props.id)
    return work_props.props
