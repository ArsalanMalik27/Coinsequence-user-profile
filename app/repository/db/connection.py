from typing import Any, Type
from uuid import UUID

from sqlalchemy import and_, except_, func, intersect, not_, or_
from sqlalchemy.orm import aliased, contains_eager

from app.domain.connections.data.connection import ConnectionProps
from app.domain.connections.repository.db.connection import ConnectionRepository
from app.repository.db.schema.connection import ConnectionConnection
from app.repository.db.schema.education import Education
from app.repository.db.schema.profile import UserProfile
from app.shared.domain.data.page import Page, PageMetadata
from app.shared.repository.db.base import BaseDBRepository
from app.shared.utils.error import DomainError


class ConnectionDBRepository(
    BaseDBRepository[ConnectionProps, ConnectionConnection],
    ConnectionRepository,
):
    @property
    def _table(self) -> Type[ConnectionConnection]:
        return ConnectionConnection

    @property
    def _entity(self) -> Type[ConnectionProps]:
        return ConnectionProps

    async def paginate_connection(
        self, query: str, page: int = 1, page_size: int = 10
    ) -> tuple[list[ConnectionConnection], PageMetadata]:
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

    async def filter_by_profile_id(
        self, profile_id: UUID, page: int, page_size: int
    ) -> Page[ConnectionProps]:
        user_a_profile = aliased(UserProfile)
        user_b_profile = aliased(UserProfile)
        user_a_education = aliased(Education)
        user_b_education = aliased(Education)
        query = (
            self.select()
            .where(
                or_(self._table.user_a == profile_id, self._table.user_b == profile_id)
            )
            .outerjoin(user_a_profile, self._table.user_a == user_a_profile.id)
            .options(contains_eager(ConnectionConnection.user_a_profile, alias=user_a_profile).contains_eager(UserProfile.educations, alias=user_a_education))
            .outerjoin(user_b_profile, self._table.user_b == user_b_profile.id)
            .options(contains_eager(ConnectionConnection.user_b_profile, alias=user_b_profile).contains_eager(UserProfile.educations, alias=user_b_education))
            .outerjoin(
                user_a_education,
                and_(
                    user_a_education.is_current == True,
                    user_a_education.profile_id == user_a_profile.id,
                ),
            )
            .outerjoin(
                user_b_education,
                and_(
                    user_b_education.is_current == True,
                    user_b_education.profile_id == user_b_profile.id,
                ),
            )
        )
        results, page_metadata = await self.paginate_connection(query, page, page_size)
        items = list(map(lambda obj: self._entity.from_orm(obj), results))
        return Page(items=items, **page_metadata.dict())

    async def get_connection_by_id(self, id: UUID) -> ConnectionProps | None:
        async with self._db_session() as session:
            user_a_profile = aliased(UserProfile)
            user_b_profile = aliased(UserProfile)
            user_a_education = aliased(Education)
            user_b_education = aliased(Education)
            query = (
                self.select()
                .where(self._table.id == id)
                .outerjoin(user_a_profile, self._table.user_a == user_a_profile.id)
                .options(contains_eager(ConnectionConnection.user_a_profile, alias=user_a_profile).contains_eager(UserProfile.educations, alias=user_a_education))
                .outerjoin(user_b_profile, self._table.user_b == user_b_profile.id)
                .options(contains_eager(ConnectionConnection.user_b_profile, alias=user_b_profile).contains_eager(UserProfile.educations, alias=user_b_education))
                .outerjoin(
                    user_a_education,
                    and_(
                        user_a_education.is_current == True,
                        user_a_education.profile_id == user_a_profile.id,
                    ),
                )
                .outerjoin(
                    user_b_education,
                    and_(
                        user_b_education.is_current == True,
                        user_b_education.profile_id == user_b_profile.id,
                    ),
                )
            )
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                return None
            return self._entity.from_orm(obj)

    async def create_connection(self, entity: ConnectionProps) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict(exclude={"user_a_profile", "user_b_profile"})
            query = self._table(**entity_dict)
            session.add(query)
            await session.commit()

    async def get_by_profile_ids(
        self, profile_a_id: UUID, profile_b_id: int
    ) -> ConnectionProps | None:
        async with self._db_session() as session:
            user_a_profile = aliased(UserProfile)
            user_b_profile = aliased(UserProfile)
            user_a_education = aliased(Education)
            user_b_education = aliased(Education)
            query = (
                self.select()
                .where(
                    or_(
                        and_(
                            self._table.user_a == profile_a_id,
                            self._table.user_b == profile_b_id,
                        ),
                        and_(
                            self._table.user_a == profile_b_id,
                            self._table.user_b == profile_a_id,
                        ),
                    )
                )
                .outerjoin(user_a_profile, self._table.user_a == user_a_profile.id)
                .options(contains_eager(ConnectionConnection.user_a_profile, alias=user_a_profile).contains_eager(UserProfile.educations, alias=user_a_education))
                .outerjoin(user_b_profile, self._table.user_b == user_b_profile.id)
                .options(contains_eager(ConnectionConnection.user_b_profile, alias=user_b_profile).contains_eager(UserProfile.educations, alias=user_b_education))
                .outerjoin(
                    user_a_education,
                    and_(
                        user_a_education.is_current == True,
                        user_a_education.profile_id == user_a_profile.id,
                    ),
                )
                .outerjoin(
                    user_b_education,
                    and_(
                        user_b_education.is_current == True,
                        user_b_education.profile_id == user_b_profile.id,
                    ),
                )
            )
            results = await session.execute(query)
            record = results.scalars().first()
            if not record:
                return None
            return self._entity.from_orm(record)

    async def get_connections_by_profile_id(
        self, profile_id: UUID
    ) -> list[ConnectionProps]:
        async with self._db_session() as session:
            query = self.select().where(
                or_(self._table.user_a == profile_id, self._table.user_b == profile_id)
            )
            results = await session.execute(query)
            items = list(
                map(lambda obj: self._entity.from_orm(obj), results.scalars().all())
            )
            return items

    async def get_connected_user(self, user_a: UUID, user_b: UUID) -> int:
        async with self._db_session() as session:
            query = self.select().where(
                or_(
                    and_(self._table.user_a == user_a and self._table.user_b == user_b),
                    and_(self._table.user_a == user_b and self._table.user_b == user_a),
                )
            )
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count

    async def get_connection_count(self, profile_id: UUID) -> int:
        async with self._db_session() as session:
            query = self.select().where(
                or_(self._table.user_a == profile_id, self._table.user_b == profile_id)
            )
            counter = query.with_only_columns(func.count())
            results = await session.execute(counter)
            count = results.scalar()
            return count

    async def count_mutual_connections(
        self, profile_id: UUID, other_profile_id: UUID
    ) -> int:
        async with self._db_session() as session:
            query = except_(
                self.select().where(
                    and_(
                        or_(
                            self._table.user_a == other_profile_id,
                            self._table.user_b == other_profile_id,
                        ),
                        (
                            not_(
                                or_(
                                    and_(
                                        self._table.user_a == other_profile_id,
                                        self._table.user_b == profile_id,
                                    ),
                                    and_(
                                        self._table.user_b == other_profile_id,
                                        self._table.user_a == profile_id,
                                    ),
                                )
                            )
                        ),
                    )
                ),
                self.select().where(
                    and_(
                        or_(
                            self._table.user_a == profile_id,
                            self._table.user_b == profile_id,
                        ),
                        (
                            not_(
                                or_(
                                    and_(
                                        self._table.user_a == profile_id,
                                        self._table.user_b == other_profile_id,
                                    ),
                                    and_(
                                        self._table.user_b == profile_id,
                                        self._table.user_a == other_profile_id,
                                    ),
                                )
                            )
                        ),
                    )
                ),
            )

            results = await session.execute(query)
            obj = results.scalars().all()
            if obj:
                count = len(obj)
                return count
            return None
