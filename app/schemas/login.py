from typing import Optional

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class SimpleTokenSchema(BaseModel):
    token: str
