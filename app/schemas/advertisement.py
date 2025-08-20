from typing import List, Optional

from pydantic import BaseModel, ConfigDict, condecimal

from app.schemas.user import ProfileSchema


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    sub_categories: Optional[List["SubCategorySchema"]] = None


class CreateCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class SubCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    category_id: Optional[int] = None


class CreateSubCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    category_id: int


class AdvertisementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: Optional[ProfileSchema]
    sub_category: Optional[SubCategorySchema]
    location: str
    price: condecimal(ge=0, decimal_places=2)  # type: ignore
    active: bool
    negotiable: bool
    description: str
    contact_email: str
    contact_phone: str
    images: Optional[List["AdImageSchema"]]


class CreateAdvertisementSchema(BaseModel):
    user_id: int
    sub_category_id: int
    location: Optional[str] = None
    price: Optional[int] = 0
    active: Optional[bool] = True
    negotiable: Optional[bool] = False
    description: Optional[str] = "Отсутствует описание"
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class UpdateAdvertisementSchema(BaseModel):
    subcategory_id: Optional[int] = None
    location: Optional[str] = None
    price: Optional[condecimal(ge=0, decimal_places=2)] = None  # type: ignore
    active: Optional[bool] = None
    negotiable: Optional[bool] = None
    description: Optional[str] = None


class UpdateAdvertisementReturnSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    sub_category_id: int
    location: str
    price: condecimal(ge=0, decimal_places=2)  # type: ignore
    active: bool
    negotiable: bool
    description: str
    contact_email: str
    contact_phone: str
    images: Optional[List["AdImageSchema"]]


class AdImageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_link: str
    advertisement: Optional[AdvertisementSchema]
