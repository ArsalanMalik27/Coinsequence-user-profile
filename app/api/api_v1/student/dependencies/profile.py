from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request

from app.container import Container
from app.domain.student.data.profile import UserProfileProps, UserProfileType
from app.domain.student.data.profile_privacy import ProfilePrivacyProps
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.student.usecase.get_profile import get_user_profile_usecase
from app.domain.student.usecase.get_profile_by_id import get_user_by_profile_id_usecase
from app.domain.student.usecase.get_profile_privacy import get_profile_privacies_usecase
from app.shared.utils.auth import AuthUser
from app.shared.utils.error import DomainError


@inject
async def valid_profile_id(
    user_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user_profile_props = await get_user_profile_usecase(user_id, user_profile_repo)
    if not user_profile_props:
        raise DomainError("Invalid Profile Id")
    return user_profile_props


@inject
async def valid_current_user_profile(
    request: Request,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user: AuthUser = request.state.user
    user_profile_props = await get_user_profile_usecase(user.id, user_profile_repo)
    if not user_profile_props:
        raise DomainError("Profile doesn't exist")
    return user_profile_props


@inject
async def valid_student_profile_id(
    request: Request,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user: AuthUser = request.state.user
    user_profile_props = await get_user_profile_usecase(user.id, user_profile_repo)
    if (
        not user_profile_props
        or user_profile_props.profile_type != UserProfileType.STUDENT
    ):
        raise DomainError("Invalid Student Id")
    return user_profile_props


@inject
async def valid_student_or_teacher_profile_id(
    request: Request,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user: AuthUser = request.state.user
    user_profile_props = await get_user_profile_usecase(user.id, user_profile_repo)
    if not (
        user_profile_props
        and user_profile_props.profile_type
        in [UserProfileType.STUDENT, UserProfileType.TEACHER]
    ):
        raise DomainError("Invalid User")
    return user_profile_props


@inject
async def other_profile_privacy(
    user_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    profile_privacy_repo: ProfilePrivacyRepository = Depends(
        Provide[Container.profile_privacy_db_repository]
    ),
) -> list[ProfilePrivacyProps]:
    user_profile_props = await get_user_profile_usecase(user_id, user_profile_repo)
    if not user_profile_props:
        raise DomainError("Invalid Profile Id")
    profile_privacies_props = await get_profile_privacies_usecase(
        user_profile_props.id, profile_privacy_repo
    )
    return profile_privacies_props


@inject
async def current_profile_privacy(
    request: Request,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    profile_privacy_repo: ProfilePrivacyRepository = Depends(
        Provide[Container.profile_privacy_db_repository]
    ),
) -> list[ProfilePrivacyProps]:
    user: AuthUser = request.state.user
    user_profile_props = await get_user_profile_usecase(user.id, user_profile_repo)
    if not user_profile_props:
        raise DomainError("Profile doesn't exist")
    profile_privacies_props = await get_profile_privacies_usecase(
        user_profile_props.id, profile_privacy_repo
    )
    return profile_privacies_props


@inject
async def other_profile_privacy_by_profile_id(
    profile_id: UUID,
    profile_privacy_repo: ProfilePrivacyRepository = Depends(
        Provide[Container.profile_privacy_db_repository]
    ),
) -> list[ProfilePrivacyProps]:
    profile_privacies_props = await get_profile_privacies_usecase(
        profile_id, profile_privacy_repo
    )
    return profile_privacies_props


@inject
async def other_profile_by_profile_id(
    profile_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user_profile_props = await get_user_by_profile_id_usecase(
        profile_id, user_profile_repo
    )
    if not user_profile_props:
        raise DomainError("Invalid Profile Id")
    return user_profile_props


@inject
async def valid_parent_user_profile(
    request: Request,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user: AuthUser = request.state.user
    user_profile_props = await get_user_profile_usecase(user.id, user_profile_repo)
    if (
        not user_profile_props
        or user_profile_props.profile_type != UserProfileType.PARENT
    ):
        raise DomainError("Invalid Parent Id")
    return user_profile_props


@inject
async def valid_other_parent_profile(
    profile_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
) -> UserProfileProps:
    user_profile_props = await get_user_by_profile_id_usecase(
        profile_id, user_profile_repo
    )
    if (
        not user_profile_props
        or user_profile_props.profile_type != UserProfileType.PARENT
    ):
        raise DomainError("Invalid Parent Id")
    return user_profile_props
