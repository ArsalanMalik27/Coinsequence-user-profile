import structlog

from app.api.api_v1.student.dto.work import CreateWorkDTO
from app.domain.student.data.work import (
    CreateWorkProps,
    WorkProps,
    Work
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.repository.db.work import WorkRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError
from datetime import datetime


logger = structlog.get_logger()


async def create_work_usecase(
    userprofile_props: UserProfileProps,
    create_work_dto: CreateWorkDTO,
    work_repo: WorkRepository,
) -> WorkProps:
    current_date = datetime.now().date()
    if create_work_dto.start_date >= create_work_dto.end_date or create_work_dto.start_date > current_date:
        raise DomainError("Invalid Date Range")
    if len(create_work_dto.description) > 600:
        raise DomainError("Description is too long")
    work_props = CreateWorkProps(**create_work_dto.dict())
    work = Work.create_from(props=work_props,profile_id=userprofile_props.id)
    await work_repo.create(work.props)
    return work.props
