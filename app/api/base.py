from fastapi import APIRouter

from app.api.v1 import base

api_router = APIRouter(prefix="/api")
api_router.include_router(base.api_router)
