from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_db_session
from app.models.advertisement import Advertisement, Category, SubCategory
from app.schemas.advertisement import (
    AdvertisementSchema,
    CategorySchema,
    CreateAdvertisementSchema,
    CreateCategorySchema,
    CreateSubCategorySchema,
    SubCategorySchema,
    UpdateAdvertisementReturnSchema,
    UpdateAdvertisementSchema,
)
from app.services.advertisement import AdvertisementService
from app.services.user import UserService
from celery_app.tasks import update_ads_views

router = APIRouter()


@router.get("/category", response_model=List[CategorySchema])
async def get_category_list(db_session: AsyncSession = Depends(get_db_session)):
    service = AdvertisementService(db_session)
    return await service.get_instances(Category)


@router.post(
    "/category", response_model=CategorySchema, status_code=status.HTTP_201_CREATED
)
async def create_category(
    data: CreateCategorySchema, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    return await service.create_instance(Category, data)


@router.get("/category/{category_id}", response_model=CategorySchema)
async def get_category(
    category_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    return await service.get_instance(Category, Category.id, category_id)


@router.delete("/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    return await service.delete_instance(Category, Category.id, category_id)


@router.get("/subcategory", response_model=List[SubCategorySchema])
async def get_subcategory_list(db_session: AsyncSession = Depends(get_db_session)):
    service = AdvertisementService(db_session)
    return await service.get_instances(SubCategory)


@router.post(
    "/subcategory",
    response_model=SubCategorySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_subcategory(
    data: CreateSubCategorySchema, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    return await service.create_instance(SubCategory, data)


@router.get("/subcategory/{subcategory_id}", response_model=SubCategorySchema)
async def get_subcategory(
    subcategory_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    return await service.get_instance(SubCategory, SubCategory.id, subcategory_id)


@router.delete("/subcategory/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(
    subcategory_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    return await service.delete_instance(SubCategory, SubCategory.id, subcategory_id)


@router.get("/", response_model=List[AdvertisementSchema])
async def get_all_ads(db_session: AsyncSession = Depends(get_db_session)):
    service = AdvertisementService(db_session)
    return await service.get_instances(Advertisement)


@router.post(
    "/", response_model=AdvertisementSchema, status_code=status.HTTP_201_CREATED
)
async def create_ad(
    data: CreateAdvertisementSchema, db_session: AsyncSession = Depends(get_db_session)
):
    service = AdvertisementService(db_session)
    user_service = UserService(db_session)
    user = await user_service.get_user(data.user_id)

    ad_data = data.model_copy(
        update={"contact_email": user.email, "contact_phone": user.phone_number}
    )
    return await service.create_instance(Advertisement, ad_data)


@router.get("/{ad_id}", response_model=AdvertisementSchema)
async def get_ad(ad_id: int, db_session: AsyncSession = Depends(get_db_session)):
    service = AdvertisementService(db_session)
    update_ads_views.delay()
    return await service.get_instance(Advertisement, Advertisement.id, ad_id)


@router.patch("/{ad_id}", response_model=UpdateAdvertisementReturnSchema)
async def update_ad(
    ad_id: int,
    update_data: UpdateAdvertisementSchema,
    db_session: AsyncSession = Depends(get_db_session),
):
    service = AdvertisementService(db_session)
    return await service.update_instance(Advertisement, ad_id, update_data)
