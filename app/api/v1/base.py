from fastapi import APIRouter

from app.api.v1 import login, user, advertisement


api_router = APIRouter(prefix="/v1")
api_router.include_router(login.router, prefix="/auth", tags=["v1 - auth"])
api_router.include_router(user.router, prefix="/users", tags=["v1 - user"])
api_router.include_router(advertisement.router, prefix="/advertisements", tags=["v1 - advertisement"])
