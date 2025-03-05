from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from app.api.api_v1.connections.dependencies.connection import (
    get_connection,
    get_connencted_profiles_count,
)
from app.api.api_v1.student.dependencies.profile import (
    current_profile_privacy,
    other_profile_privacy,
    other_profile_privacy_by_profile_id,
    valid_current_user_profile,
    valid_other_parent_profile,
    valid_parent_user_profile,
    valid_profile_id,
    valid_student_profile_id,
)
from app.api.api_v1.student.dto.profile import (
    CreateUserProfileDTO,
    OtherUserProfileResponseDTO,
    SuggestedUsersParams,
    UpdateProfilePrivacyDTO,
    UpdateUserProfileDTO,
    UserProfileListResponseDTO,
    UserProfileResponseDTO,
    ValidateParentCodeDTO,
)
from app.container import Container
from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.activity_stream import ActivityStream
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.domain.connections.usecase.count_mutual_connections import (
    count_mutual_connections_usecase,
)
from app.domain.connections.usecase.get_connection import get_connection_usecase
from app.domain.connections.usecase.get_connection_request import (
    get_connection_request_usecase,
)
from app.domain.connections.usecase.get_pending_connection_request_count import (
    get_pending_connection_request_count_usecase,
)
from app.domain.student.data.profile import UserProfileProps
from app.domain.student.data.profile_privacy import ProfilePrivacyProps
from app.domain.student.repository.db.children_profile import ChildrenProfileRepository
from app.domain.student.repository.db.profile import UserProfileRepository
from app.domain.student.repository.db.profile_privacy import ProfilePrivacyRepository
from app.domain.student.usecase.create_profile import create_user_profile_usecase
from app.domain.student.usecase.delete_child import delete_child_usecase
from app.domain.student.usecase.get_profile_privacy import get_profile_privacies_usecase
from app.domain.student.usecase.get_suggested_users import get_suggested_users_usecase
from app.domain.student.usecase.list_all_children_profile import (
    list_all_children_profile_usecase,
)
from app.domain.student.usecase.list_others_children_profile import (
    list_others_children_profile_usecase,
)
from app.domain.student.usecase.update_profile import update_user_profile_usecase
from app.domain.student.usecase.update_profile_privacy import (
    update_profile_privacy_usecase,
)
from app.domain.student.usecase.upload_profile_pic import upload_profile_pic_usecase
from app.domain.student.usecase.upsert_profile_embeddings import (
    upsert_profile_embedding_usecase,
)
from app.domain.student.usecase.validate_parent_code import validate_parent_code_usecase
from app.shared.domain.data.page import Page, PageRequestDTO
from app.shared.domain.repository.event_client import EventClient
from app.shared.domain.repository.vectordb_client import VectorDBClient
from app.shared.repository.storage_client import StorageClient
from app.shared.utils.auth import AuthUser

router = APIRouter()


ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
]


@router.post("/", response_model=UserProfileResponseDTO)
@inject
async def create_user_profile(
    create_user_profile_dto: CreateUserProfileDTO,
    request: Request,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    profile_privacy_repo: ProfilePrivacyRepository = Depends(
        Provide[Container.profile_privacy_db_repository]
    ),
    event_client: EventClient = Depends(Provide[Container.event_client]),
) -> UserProfileProps:
    user: AuthUser = request.state.user
    profile_props = await create_user_profile_usecase(
        user,
        create_user_profile_dto,
        user_profile_repo,
        profile_privacy_repo,
        event_client
    )
    return profile_props


@router.put("/student/me", response_model=UserProfileResponseDTO)
@inject
async def update_student_profile(
    update_user_profile_dto: UpdateUserProfileDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    event_client: EventClient = Depends(Provide[Container.event_client]),
) -> UserProfileProps:
    profile_props = await update_user_profile_usecase(
        current_user_profile_props, update_user_profile_dto, user_profile_repo, event_client
    )
    return profile_props


@router.get("/student/me", response_model=UserProfileResponseDTO)
@inject
async def get_my_user_profile(
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    profile_privacy_props: UserProfileProps = Depends(current_profile_privacy),
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
) -> UserProfileProps:
    pending_connection_request_count = await get_pending_connection_request_count_usecase(
        current_user_profile_props.id, connection_request_repo)
    return UserProfileResponseDTO.from_props(
        current_user_profile_props, profile_privacy_props, pending_connection_request_count)


@router.get("/student/", response_model=dict)
@inject
async def get_suggested_users(
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    suggested_user_params: SuggestedUsersParams = Depends(SuggestedUsersParams),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
) -> Page[UserProfileProps]:
    # user: AuthUser = request.state.user
    user_profile_props = await get_suggested_users_usecase(
        current_user_profile_props, suggested_user_params, user_profile_repo, connection_repo
    )
    return user_profile_props


@router.post("/student/me/picture", response_model=UserProfileResponseDTO)
@inject
async def upload_my_profile_image(
    file: UploadFile,
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    event_client: EventClient = Depends(Provide[Container.event_client]),
    store_client: StorageClient = Depends(Provide[Container.gcp_storage_client]),
) -> UserProfileProps:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, detail="Invalid media type")
    user_profile = await upload_profile_pic_usecase(
        current_user_profile_props, file, user_profile_repo, event_client, store_client
    )
    return user_profile


@router.get("/student/{user_id}", response_model=OtherUserProfileResponseDTO)
@inject
async def get_other_user(
    user_profile_props: UserProfileProps = Depends(valid_profile_id),
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy),
    connection_props: ConnectionProps = Depends(get_connection),
    connection_repo: ConnectionRepository = Depends(
        Provide[Container.connection_db_repository]
    ),
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
) -> OtherUserProfileResponseDTO:
    mutual_counts = await count_mutual_connections_usecase(current_user_profile_props.id, user_profile_props.id,
                                                           connection_repo)
    connection_request_props = await get_connection_request_usecase(
        user_profile_props.id, current_user_profile_props.id, connection_request_repo
    )
    response = OtherUserProfileResponseDTO.from_props(
        user_profile_props, profile_privacy_props, connection_request_props, connection_props, mutual_counts
    )
    return response


@router.get("/student/{user_id}/doner-view")
@inject
async def get_other_user_for_doner(
    user_profile_props: UserProfileProps = Depends(valid_profile_id),
):
    return user_profile_props


@router.put("/student/me/privacy", response_model=UserProfileResponseDTO)
@inject
async def update_profile_privacy(
    update_profile_privacy_dto: UpdateProfilePrivacyDTO,
    current_user_profile_props: UserProfileProps = Depends(valid_current_user_profile),
    profile_privacy_props: UserProfileProps = Depends(current_profile_privacy),
    profile_privacy_repo: ProfilePrivacyRepository = Depends(
        Provide[Container.profile_privacy_db_repository]
    ),
    connection_request_repo: ConnectionRequestRepository = Depends(
        Provide[Container.connection_request_db_repository]
    ),
) -> UserProfileResponseDTO:
    profile_privacies_props = await update_profile_privacy_usecase(
        update_profile_privacy_dto, profile_privacy_props, profile_privacy_repo
    )
    pending_connection_request_count = await get_pending_connection_request_count_usecase(
        current_user_profile_props.id, connection_request_repo)
    return UserProfileResponseDTO.from_props(
        current_user_profile_props, profile_privacies_props, pending_connection_request_count)


@router.post("/validate/{parent_code}", response_model=str)
@inject
async def validate_parent_code(
        validate_parent_code_dto: ValidateParentCodeDTO,
        parent_profile_props: UserProfileProps = Depends(valid_parent_user_profile),
        user_profile_repo: UserProfileRepository = Depends(
            Provide[Container.user_profile_db_repository]
        ),
        connection_request_repo: ConnectionRequestRepository = Depends(
            Provide[Container.connection_request_db_repository]
        ),
        children_profile_repo: ChildrenProfileRepository = Depends(
            Provide[Container.children_profile_db_repository]
        ),
) -> str:
    await validate_parent_code_usecase(
        validate_parent_code_dto.parent_code,
        parent_profile_props,
        user_profile_repo,
        connection_request_repo,
        children_profile_repo
    )
    return "success"



@router.get("/child/me", response_model=list[UserProfileProps])
@inject
async def get_children_profiles(
        parent_profile_props: UserProfileProps = Depends(valid_parent_user_profile),
        user_profile_repo: UserProfileRepository = Depends(
            Provide[Container.user_profile_db_repository]
        ),
        children_profile_repo: ChildrenProfileRepository = Depends(
            Provide[Container.children_profile_db_repository]
        ),
) -> list[UserProfileProps]:
    children_profiles = await list_all_children_profile_usecase(
        parent_profile_props,
        user_profile_repo,
        children_profile_repo,
    )
    return children_profiles


@router.delete("/child/me/{child_id}")
@inject
async def delete_children_profile(
        child_id: UUID,
        parent_profile_props: UserProfileProps = Depends(valid_parent_user_profile),
        connection_repo: ConnectionRepository = Depends(
                Provide[Container.connection_db_repository]
            ),
        children_profile_repo: ChildrenProfileRepository = Depends(
            Provide[Container.children_profile_db_repository]
        ),
        activity_steam: ActivityStream = Depends(
        Provide[Container.getstream_activity_stream]
        )
) -> str:

    await delete_child_usecase(
        child_id,
        parent_profile_props,
        children_profile_repo,
        connection_repo,
        activity_steam
    )
    return "success"


@router.get("/child/{profile_id}", response_model=list[UserProfileProps])
@inject
async def get_other_children_profiles(
        parent_profile_props: UserProfileProps = Depends(valid_other_parent_profile),
        user_profile_repo: UserProfileRepository = Depends(
            Provide[Container.user_profile_db_repository]
        ),
        children_profile_repo: ChildrenProfileRepository = Depends(
            Provide[Container.children_profile_db_repository]
        ),
        connected_profile: ConnectionProps = Depends(get_connencted_profiles_count),
        profile_privacy_props: ProfilePrivacyProps = Depends(other_profile_privacy_by_profile_id),
) -> list[UserProfileProps]:
    children_profiles = await list_others_children_profile_usecase(
        parent_profile_props,
        user_profile_repo,
        children_profile_repo,
        profile_privacy_props,
        connected_profile
    )
    return children_profiles

@router.get("/testing-mint_coins")
@inject
async def testing_mint_coins(
    user_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
    vectordb_client: VectorDBClient = Depends(
        Provide[Container.vectordb_client]
    ),
):
    result = await upsert_profile_embedding_usecase(
        user_id,
        user_profile_repo,
        vectordb_client,
    )
    return result


@router.get("/get_all_for_user")
@inject
async def get_all_for_user(
    user_id: UUID,
    user_profile_repo: UserProfileRepository = Depends(
        Provide[Container.user_profile_db_repository]
    ),
):

    result = await user_profile_repo.get_all_joined_by_user_id(user_id)
    return result
