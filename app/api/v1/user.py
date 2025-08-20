from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.db.session import get_db_session
from app.middleware.permissions import PermissionMiddleware
from app.permissions.base import AllowAny, IsAuthenticated
from app.schemas.user import ProfileSchema, UserRegistrationSchema
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/register-user",
    response_model=ProfileSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionMiddleware(AllowAny))],
)
async def register_user(
    data: UserRegistrationSchema, db_session: AsyncSession = Depends(get_db_session)
):
    service = UserService(db_session)
    result = await service.register_user(data)
    return result


@router.get("/", response_model=List[ProfileSchema])
async def get_users_list(db_session: AsyncSession = Depends(get_db_session)):
    service = UserService(db_session)
    return await service.get_users()


@router.get(
    "/profile",
    response_model=ProfileSchema,
    dependencies=[Depends(PermissionMiddleware(IsAuthenticated))],
)
async def get_profile(
    request: Request, db_session: AsyncSession = Depends(get_db_session)
):
    service = UserService(db_session)
    return await service.get_user(request.user.id)
