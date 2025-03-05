from uuid import UUID
import structlog


from app.domain.student.data.profile import UserProfileProps
from app.repository.db.work import WorkDBRepository
from app.shared.utils.error import DomainError


logger = structlog.get_logger()


async def delete_work_usecase(
    work_id: UUID,
    userprofile_props: UserProfileProps,
    work_repo: WorkDBRepository,
) -> None:
    work_props = await work_repo.get_by_id(work_id)
    if not work_props or work_props.profile_id != userprofile_props.id:
        logger.info(
            "[DeleteWorkUsecase: attempt to delete non-existing Work]",
            data=userprofile_props,
        )
        raise DomainError("Invalid Work Id")
    await work_repo.delete_work(
        work_id, userprofile_props.id
    )
