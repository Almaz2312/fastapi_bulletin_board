from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.middleware.permissions import PermissionMiddleware
from app.permissions.base import AllowAny, IsAuthenticated
from app.schemas.login import LoginSchema, TokenSchema, SimpleTokenSchema
from app.services.login import LoginService

router = APIRouter()


@router.post("/login", response_model=TokenSchema, dependencies=[Depends(PermissionMiddleware(AllowAny))])
async def login(data: LoginSchema, db_session: AsyncSession = Depends(get_db_session)):
    service = LoginService(db_session)
    return await service.login(data)


@router.post(
    "/refresh-token",
    response_model=SimpleTokenSchema,
    dependencies=[Depends(PermissionMiddleware(IsAuthenticated))]
)
async def refresh_token(token: SimpleTokenSchema, db_session: AsyncSession = Depends(get_db_session)):
    service = LoginService(db_session)
    return await service.refresh_token(token)


@router.post("/verify-token", dependencies=[Depends(PermissionMiddleware(IsAuthenticated))])
async def verify_token(token: SimpleTokenSchema, db_session: AsyncSession = Depends(get_db_session)):
    service = LoginService(db_session)
    await service.verify_token(token)
    return {"result": "Ok"}
