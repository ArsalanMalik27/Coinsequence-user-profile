from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import update

from app.domain.student.data.score import CreateScoreProps, ScoreProps
from app.domain.student.repository.db.score import ScoreRepository
from app.repository.db.schema.score import Score
from app.shared.repository.db.base import BaseDBRepository


class ScoreDBRepository(BaseDBRepository[CreateScoreProps, Score], ScoreRepository):
    @property
    def _table(self) -> Type[Score]:
        return Score

    @property
    def _entity(self) -> Type[ScoreProps]:
        return ScoreProps

    async def update_score(self, entity: ScoreProps) -> None:
        async with self._db_session() as session:
            entity_dict = entity.dict(exclude={"address"})
            query = (
                update(self._table)  # type: ignore
                .where(self._table.id == entity.id)
                .values(**entity_dict)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()

    async def get_data_by_score_id(self, score_id: UUID) -> Optional[ScoreProps]:
        async with self._db_session() as session:
            query = self.select().where(id == score_id)
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                return None
            return self._entity.from_orm(obj)

    async def get_score_list(self, profile_id: UUID) -> List:
        async with self._db_session() as session:
            query = self.select().where(self._table.profile_id == profile_id)
            result = await session.execute(query)
            return list(
                map(lambda obj: self._entity.from_orm(obj), result.scalars().all())
            )
