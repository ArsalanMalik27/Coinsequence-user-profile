from typing import Any, Type
from uuid import UUID

from sqlalchemy import and_, func, or_, update
from sqlalchemy.orm import aliased, contains_eager

from app.domain.connections.data.connection_request import (
    ConnectionRequestProps,
    ConnectionRequestStatus,
)
from app.domain.connections.repository.db.connection_request import (
    ConnectionRequestRepository,
)
from app.repository.db.schema.connection_request import ConnectionRequestConnection
from app.repository.db.schema.education import Education
from app.repository.db.schema.profile import UserProfile
from app.shared.domain.data.page import Page, PageMetadata
from app.shared.repository.db.base import BaseDBRepository
from app.shared.utils.error import DomainError


class ConnectionRequestDBRepository(
    BaseDBRepository[ConnectionRequestProps, ConnectionRequestConnection],
    ConnectionRequestRepository,
):
    @property
    def _table(self) -> Type[ConnectionRequestConnection]:
        return ConnectionRequestConnection

    @property
    def _entity(self) -> Type[ConnectionRequestProps]:
        return ConnectionRequestProps

    async def paginate_connection_request(
        self, query: Any, page: int, page_size: int
    ) -> tuple[list[ConnectionRequestConnection], PageMetadata]:
        async with self._db_session() as session:
            if page <= 0:
                raise DomainError("page should be be >= 1")
            if page_size <= 0:
                raise DomainError("page_size should be >= 1")
            paginated_query = query.limit(page_size).offset((page - 1) * page_size)
            count_query = query.with_only_columns(func.count(self._table.id))
            results = await session.execute(paginated_query)
            total_result = await session.execute(count_query)
            page_data = PageMetadata(
                page=page,
                page_size=page_size,
                total=total_result.scalar_one(),
            )
            return (results.scalars().unique().all(), page_data)

    async def filter_by_receiver_id(
        self,
        receiver_id: UUID,
        status: ConnectionRequestStatus | None,
        page: int,
        page_size: int,
    ) -> Page:
        sender_profile = aliased(UserProfile)
        receiver_profile = aliased(UserProfile)
        sender_education = aliased(Education)
        receiver_education = aliased(Education)
        query = self.select().where(self._table.receiver_id == receiver_id)
        if status:
            query = query.where(self._table.status == status)
        query = (
            query.outerjoin(sender_profile, self._table.sender_id == sender_profile.id)
            .options(contains_eager(ConnectionRequestConnection.sender, alias=sender_profile).contains_eager(UserProfile.educations, alias=sender_education))
            .outerjoin(receiver_profile, self._table.receiver_id == receiver_profile.id)
            .options(contains_eager(ConnectionRequestConnection.receiver, alias=receiver_profile).contains_eager(UserProfile.educations, alias=receiver_education))
            .outerjoin(
                sender_education,
                and_(
                    sender_education.is_current == True,
                    sender_education.profile_id == sender_profile.id,
                    sender_education.deleted != True,
                ),
            )
            .outerjoin(
                receiver_education,
                and_(
                    receiver_education.is_current == True,
                    receiver_education.profile_id == receiver_profile.id,
                    receiver_education.deleted != True,
                ),
            )
            .execution_options(synchronize_session="fetch")
        )
        results, page_metadata = await self.paginate_connection_request(
            query, page, page_size
        )
        items = list(map(lambda obj: self._entity.from_orm(obj), results))
        return Page(items=items, **page_metadata.dict())

    async def filter_by_profile_id(
        self,
        profile_id: UUID,
        status: ConnectionRequestStatus | None,
        page: int,
        page_size: int,
        text: str,
    ) -> Page:
        sender_profile = aliased(UserProfile)
        receiver_profile = aliased(UserProfile)
        sender_education = aliased(Education)
        receiver_education = aliased(Education)
        query = self.select().where(
            or_(
                self._table.receiver_id == profile_id,
                self._table.sender_id == profile_id,
            )
        )
        if status:
            query = query.where(self._table.status == status)
        query = (
            query.outerjoin(sender_profile, self._table.sender_id == sender_profile.id)
            .options(contains_eager(ConnectionRequestConnection.sender, alias=sender_profile).contains_eager(UserProfile.educations, alias=sender_education))
            .outerjoin(receiver_profile, self._table.receiver_id == receiver_profile.id)
            .options(contains_eager(ConnectionRequestConnection.receiver, alias=receiver_profile).contains_eager(UserProfile.educations, alias=receiver_education))
            .outerjoin(
                sender_education,
                and_(
                    sender_education.is_current == True,
                    sender_education.profile_id == sender_profile.id,
                    sender_education.deleted != True,
                ),
            )
            .outerjoin(
                receiver_education,
                and_(
                    receiver_education.is_current == True,
                    receiver_education.profile_id == receiver_profile.id,
                    receiver_education.deleted != True,
                ),
            )
            .execution_options(synchronize_session="fetch")
            .filter(
                or_(
                    sender_profile.first_name.like(f"{text}%"),
                    sender_profile.last_name.like(f"{text}%"),
                    receiver_profile.first_name.like(f"{text}%"),
                    receiver_profile.last_name.like(f"{text}%"),
                )
            )
        )
        results, page_metadata = await self.paginate_connection_request(
            query, page, page_size
        )
        items = list(map(lambda obj: self._entity.from_orm(obj), results))
        return Page(items=items, **page_metadata.dict())

    async def create_connection_request(self, entity: ConnectionRequestProps) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict(exclude={"sender", "receiver"})
            query = self._table(**entity_dict)
            session.add(query)
            await session.commit()

    async def get_pending_by_id(self, id: UUID) -> ConnectionRequestProps | None:
        async with self._db_session() as session:
            sender_profile = aliased(UserProfile)
            receiver_profile = aliased(UserProfile)
            sender_education = aliased(Education)
            receiver_education = aliased(Education)
            query = (
                self.select()
                .where(
                    and_(
                        self._table.id == id,
                        self._table.status == ConnectionRequestStatus.PENDING,
                    )
                )
                .outerjoin(sender_profile, self._table.sender_id == sender_profile.id)
                .options(contains_eager(ConnectionRequestConnection.sender, alias=sender_profile).contains_eager(UserProfile.educations, alias=sender_education))
                .outerjoin(
                    receiver_profile, self._table.receiver_id == receiver_profile.id
                )
                .options(contains_eager(ConnectionRequestConnection.receiver, alias=receiver_profile).contains_eager(UserProfile.educations, alias=receiver_education))
                .outerjoin(
                    sender_education,
                    and_(
                        sender_education.is_current == True,
                        sender_education.profile_id == sender_profile.id,
                        sender_education.deleted != True,
                    ),
                )
                .outerjoin(
                    receiver_education,
                    and_(
                        receiver_education.is_current == True,
                        receiver_education.profile_id == receiver_profile.id,
                        receiver_education.deleted != True,
                    ),
                )
            )
            results = await session.execute(query)
            record = results.scalars().first()
            if not record:
                return None
            return self._entity.from_orm(record)

    async def update_connection_request(self, entity: ConnectionRequestProps) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict(exclude={"sender", "receiver"})
            query = (
                update(self._table)  # type: ignore
                .where(self._table.id == entity.id)
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()

    async def get_by_profile_ids(
        self,
        profile_a_id: UUID,
        profile_b_id: int,
        status: ConnectionRequestStatus | None = None,
    ) -> ConnectionRequestProps | None:
        async with self._db_session() as session:
            sender_profile = aliased(UserProfile)
            receiver_profile = aliased(UserProfile)
            sender_education = aliased(Education)
            receiver_education = aliased(Education)
            query = (
                self.select()
                .where(
                    or_(
                        and_(
                            self._table.sender_id == profile_a_id,
                            self._table.receiver_id == profile_b_id,
                        ),
                        and_(
                            self._table.sender_id == profile_b_id,
                            self._table.receiver_id == profile_a_id,
                        ),
                    )
                )
                .outerjoin(sender_profile, self._table.sender_id == sender_profile.id)
                .options(contains_eager(self._table.sender, alias=sender_profile).contains_eager(UserProfile.educations, alias= sender_education))
                .outerjoin(
                    receiver_profile, self._table.receiver_id == receiver_profile.id
                )
                .options(contains_eager(self._table.receiver, alias=receiver_profile).contains_eager(UserProfile.educations, alias= receiver_education))
                .outerjoin(
                    sender_education,
                    and_(
                        sender_education.is_current == True,
                        sender_education.profile_id == sender_profile.id,
                        sender_education.deleted != True,
                    ),
                )
                .outerjoin(
                    receiver_education,
                    and_(
                        receiver_education.is_current == True,
                        receiver_education.profile_id == receiver_profile.id,
                        receiver_education.deleted != True,
                    ),
                )
            )
            if status:
                query = query.where(self._table.status == status)
            results = await session.execute(query)
            record = results.scalars().first()
            if not record:
                return None
            return self._entity.from_orm(record)

    async def get_pending_connection_request_count(self, profile_id: UUID) -> int:
        async with self._db_session() as session:
            query = self.select().where(
                and_(
                    or_(self._table.receiver_id == profile_id),
                    self._table.status == ConnectionRequestStatus.PENDING,
                )
            )
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count
