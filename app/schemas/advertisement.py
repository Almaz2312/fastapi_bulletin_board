from typing import Optional, List

from pydantic import BaseModel, ConfigDict, condecimal

from app.schemas.user import ProfileSchema


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    subcategories: Optional[list] = None


class CreateCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    subcategories: Optional["CreateSubCategorySchema"] = None


class SubCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    category: Optional[CategorySchema] = None


class CreateSubCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    category_id: int


class AdvertisementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: Optional[ProfileSchema]
    subcategory: Optional[SubCategorySchema]
    location: str
    price: condecimal(ge=0, decimal_places=2)
    active: bool
    negotiable: bool
    description: str
    contact_email: str
    contact_phone: str
    images: Optional[List["AdImageSchema"]]


class CreateAdvertisementSchema(BaseModel):
    user_id: int
    subcategory_id: int
    location: Optional[str] = None
    price: Optional[int] = 0
    active: Optional[bool] = True
    negotiable: Optional[bool] = False
    description: Optional[str] = "Отсутствует описание"


class UpdateAdvertisementSchema(BaseModel):
    subcategory_id: Optional[int] = None
    location: Optional[str] = None
    price: Optional[condecimal(ge=0, decimal_places=2)] = None
    active: Optional[bool] = None
    negotiable: Optional[bool] = None
    description: Optional[str] = None


class AdImageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_link: str
    advertisement: Optional[AdvertisementSchema]
