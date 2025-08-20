from typing import Any, Optional, Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from starlette import status

from app.models.base_class import Base
from app.repositories.advertisement import AdvertisementRepository
from app.schemas.advertisement import UpdateAdvertisementSchema


class AdvertisementService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = AdvertisementRepository(db=db)

    async def get_instances(self, model: Type[Base]) -> Type[Base]:
        return await self.repository.get_instance_list(model)

    async def create_instance(
        self, model: Type[Base], data: BaseModel
    ) -> Optional[Base]:
        return await self.repository.create_instance(model, data)

    async def get_instance(
        self, model: Type[Base], field: InstrumentedAttribute, value: Any
    ) -> Optional[Base]:
        return await self.repository.get_instance(model, field, value)

    async def delete_instance(
        self, model: Type[Base], field: InstrumentedAttribute, value: Any
    ) -> dict:
        instance = await self.repository.get_instance(model, field, value)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} not found",
            )
        return await self.repository.delete_instance(instance)

    async def update_instance(
        self, model: Type[Base], value: Any, schema: UpdateAdvertisementSchema
    ):
        data = schema.model_dump(exclude_unset=True)
        return await self.repository.update_instance(model, model.id, value, data)
