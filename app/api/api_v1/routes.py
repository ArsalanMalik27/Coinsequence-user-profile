from fastapi import APIRouter, Depends

from app.api.api_v1.connections.connection import router as connection_router
from app.api.api_v1.connections.connection_request import (
    router as connection_request_router,
)
from app.api.api_v1.health import router as health_router
from app.api.api_v1.student.education import router as education_router
from app.api.api_v1.student.grade import router as grade_router
from app.api.api_v1.student.profile import router as user_profile_router
from app.api.api_v1.student.score import router as score_router
from app.api.api_v1.student.award import router as award_router
from app.api.api_v1.student.work import router as work_router
from app.api.api_v1.student.voluntary import router as voluntary_router
from app.api.api_v1.student.roles import router as roles_router
from app.api.api_v1.student.college_university import router as college_university_router
from app.api.api_v1.student.activity import router as activity_router
from app.api.api_v1.student.test import router as test_router
from app.api.api_v1.student.application import router as application_router
from app.api.api_v1.student.search_profile import router as search_router

from app.shared.utils.jwt import JWTBearer

api_router = APIRouter()
api_router.include_router(
    user_profile_router,
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    education_router,
    prefix="/profile/student/me/education",
    tags=["education"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    grade_router,
    prefix="/profile/student/me/grade",
    tags=["grade"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    score_router,
    prefix="/profile/student/score",
    tags=["score"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    connection_request_router,
    prefix="/connection-request",
    tags=["connection-request"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    connection_router,
    prefix="/connection",
    tags=["Connection"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    award_router,
    prefix="/profile/student/me/award",
    tags=["Award"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    work_router,
    prefix="/profile/student/me/work",
    tags=["Work"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    voluntary_router,
    prefix="/profile/student/me/voluntary",
    tags=["Voluntary"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    college_university_router,
    prefix="/profile/student/me/university",
    tags=["CollegeUniversity"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    roles_router,
    prefix="/profile/student/me/roles",
    tags=["Roles"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    activity_router,
    prefix="/profile/student/me/activity",
    tags=["Activity"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    test_router,
    prefix="/profile/student/me/test",
    tags=["Test"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    application_router,
    prefix="/profile/student",
    tags=["Application"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    search_router,
    prefix="/profile/student",
    tags=["Search"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(health_router, prefix="/health", tags=["health"])
