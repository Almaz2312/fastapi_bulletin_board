from typing import Any, Optional, Type

from pydantic import BaseModel
from sqlalchemy import ScalarResult, Update, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.models.base_class import Base


class AdvertisementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_instance_list(self, model: Type[Base]):
        query = select(model)
        result = await self.db.scalars(query)
        return result.all()

    async def create_instance(self, model: Type[Base], data: BaseModel):
        new_instance = model(**data.model_dump(exclude_unset=True))
        self.db.add(new_instance)
        await self.db.commit()
        await self.db.refresh(new_instance)
        return new_instance

    async def get_instance(
        self, model: Type[Base], field: InstrumentedAttribute, value: Any
    ) -> Optional[Base]:
        query = select(model).where(field == value)
        result: ScalarResult = await self.db.scalars(query)
        return result.one_or_none()

    async def delete_instance(self, instance: Base) -> dict:
        await self.db.delete(instance)
        await self.db.commit()
        return {"result": "Deleted successfully"}

    async def update_instance(
        self, model: Type[Base], field: InstrumentedAttribute, value: Any, data: dict
    ):
        query: Update = (
            update(model).where(field == value).values(**data).returning(model)  # type: ignore
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()
