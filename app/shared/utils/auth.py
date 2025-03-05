from enum import Enum
from uuid import UUID, uuid4

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.infra.config import settings
from app.shared.domain.data.entity import Entity

JWT_SECRET = settings.JWT_KEY_PASSWORD
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_HOURS = 1


class UserProfileType(Enum):
    STUDENT = "STUDENT"
    INVESTOR = "INVESTOR"
    TEACHER = "TEACHER"
    PARENT = "PARENT"


class UserProps(Entity):
    profile: UserProfileType
    first_name: str
    last_name: str
    is_active: bool = False
    is_superuser: bool = False


class AuthUser(BaseModel):
    id: UUID
    profile: UserProfileType
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_superuser: bool


def get_current_user(token: str) -> AuthUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or expired token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if settings.ENV == "local":
        return AuthUser(
            # id=uuid4(),
            id="c1af1084-06cf-420b-9e62-8b649d635e02",
            # id="b6ed542c-188d-4e0e-9b85-fe6af07c6c3e",
            profile=UserProfileType.STUDENT,
            first_name="First",
            last_name="Last",
            is_active=True,
            is_superuser=True,
        )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        id = payload.get("sub")
        profile = payload.get("profile")
        is_active = payload.get("is_active")
        is_superuser = payload.get("is_superuser")
        if id is None:
            raise credentials_exception
        user = AuthUser(
            id=id, profile=profile, is_active=is_active, is_superuser=is_superuser
        )
    except jwt.PyJWTError:
        raise credentials_exception
    return user


def create_access_token(userProps: UserProps) -> str:
    payload = {
        "sub": str(userProps.id),
        "profile": userProps.profile.value,
        "is_active": userProps.is_active,
        "first_name": userProps.first_name,
        "last_name": userProps.last_name,
        "is_superuser": userProps.is_superuser,
    }
    return jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
