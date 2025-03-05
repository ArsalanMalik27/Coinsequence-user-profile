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

logger = structlog.get_logger()


async def get_work_list_usecase(
    userprofile_props: UserProfileProps,
    work_repo: WorkRepository,
) -> list[WorkProps]:
    work_list = await work_repo.get_all_work(userprofile_props.id)
    return work_list