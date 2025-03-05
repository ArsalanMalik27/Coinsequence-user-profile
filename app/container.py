import pinecone
import sentry_sdk
from dependency_injector import containers, providers
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.infra.config import settings
from app.masterdata_shared.api_client import MasterdataAPIClient
from app.repository.activity_stream import GetStreamActivityStream
from app.repository.db.activity import ActivityDBRepository
from app.repository.db.application import ApplicationDBRepository
from app.repository.db.award import AwardDBRepository
from app.repository.db.children_profile import ChildrenProfileDBRepository
from app.repository.db.college_university import UniversityDBRepository
from app.repository.db.connection import ConnectionDBRepository
from app.repository.db.connection_request import ConnectionRequestDBRepository
from app.repository.db.education import EducationDBRepository
from app.repository.db.grade import GradeDBRepository
from app.repository.db.profile import UserProfileDBRepository
from app.repository.db.profile_privacy import ProfilePrivacyDBRepository
from app.repository.db.roles import RolesDBRepository
from app.repository.db.score import ScoreDBRepository
from app.repository.db.student_fund_courses import StudentFundCoursesDBRepository
from app.repository.db.test import TestDBRepository
from app.repository.db.user_karma import UserKarmaDBRepository
from app.repository.db.voluntary import VoluntaryDBRepository
from app.repository.db.work import WorkDBRepository
from app.shared.infra.database import get_db
from app.shared.repository.event_client import EventClient
from app.shared.repository.onesignal_email_client import OneSignalEmailClient
from app.shared.repository.pinecone_vectordb_client import PineconeVectorDBClient
from app.shared.repository.storage_client import StorageClient

if settings.ENV != "local":
    sentry_sdk.init(
        dsn=settings.SENTRY_DNS,
        traces_sample_rate=1.0,
        server_name=settings.PROJECT_NAME,
        enable_tracing=True,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint"
            ),
            FastApiIntegration(
                transaction_style="endpoint"
            ),
        ]
    )

pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)


class Container(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(
    #    packages=["app.api", "app.consumer"])

    db_pool = providers.Resource(get_db)

    # Infra Gateways
    event_client = providers.Singleton(EventClient)
    gcp_storage_client = providers.Singleton(StorageClient)
    getstream_activity_stream = providers.Singleton(GetStreamActivityStream)
    vectordb_client = providers.Singleton(PineconeVectorDBClient)

    # Repositories
    education_db_repository = providers.Factory(
        EducationDBRepository, db_session=db_pool
    )
    user_profile_db_repository = providers.Factory(
        UserProfileDBRepository, db_session=db_pool
    )
    user_karma_db_repository = providers.Factory(
        UserKarmaDBRepository, db_session=db_pool
    )
    student_fund_courses_db_repository = providers.Factory(
        StudentFundCoursesDBRepository, db_session=db_pool
    )
    grade_db_repository = providers.Factory(GradeDBRepository, db_session=db_pool)
    score_db_repository = providers.Factory(ScoreDBRepository, db_session=db_pool)
    connection_request_db_repository = providers.Factory(
        ConnectionRequestDBRepository,
        db_session=db_pool,
    )
    connection_db_repository = providers.Factory(
        ConnectionDBRepository,
        db_session=db_pool,
    )
    award_db_repository = providers.Factory(
        AwardDBRepository,
        db_session=db_pool,
    )
    profile_privacy_db_repository = providers.Factory(
        ProfilePrivacyDBRepository,
        db_session=db_pool,
    )
    work_db_repository = providers.Factory(
        WorkDBRepository,
        db_session=db_pool,
    )
    voluntary_db_repository = providers.Factory(
        VoluntaryDBRepository,
        db_session=db_pool,
    )
    university_db_repository = providers.Factory(
        UniversityDBRepository,
        db_session=db_pool,
    )
    roles_db_repository = providers.Factory(
        RolesDBRepository,
        db_session=db_pool,
    )
    activity_db_repository = providers.Factory(
        ActivityDBRepository,
        db_session=db_pool,
    )
    test_db_repository = providers.Factory(
        TestDBRepository,
        db_session=db_pool,
    )
    children_profile_db_repository = providers.Factory(
        ChildrenProfileDBRepository,
        db_session=db_pool,
    )
    application_db_repository = providers.Factory(
        ApplicationDBRepository,
        db_session=db_pool,
    )
    # Services
    email_client = providers.Factory(OneSignalEmailClient)
    masterdata_client = providers.Factory(MasterdataAPIClient)
