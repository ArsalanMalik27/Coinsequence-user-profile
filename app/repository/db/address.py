from typing import Optional, Type

from app.domain.student.data.address import AddressProps
from app.domain.student.repository.db.education import EducationRepository
from app.repository.db.schema.address import Address
from app.shared.repository.db.base import BaseDBRepository


class AddressDBRepository(BaseDBRepository[AddressProps, Address], EducationRepository):
    @property
    def _table(self) -> Type[Address]:
        return Address

    @property
    def _entity(self) -> Type[AddressProps]:
        return AddressProps

    async def get_by_address_id(self, id: str) -> Optional[AddressProps]:
        async with self._db_session() as session:
            query = self.select().where(Address.address_id == id).limit(1)
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                return None
            return self._entity.from_orm(obj)
