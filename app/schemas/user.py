from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    phone_number: Optional[str]


class UserRegistrationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    password: str
    confirm_password: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
