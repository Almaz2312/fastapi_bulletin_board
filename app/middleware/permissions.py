from typing import Type

from starlette.requests import Request

from app.permissions.base import BasePermission, AllowAny


class PermissionMiddleware:
    def __init__(self, permission_class: Type[BasePermission] = AllowAny):
        self.permission_class = permission_class()

    async def __call__(self, request: Request):
        await self.permission_class.has_permission(request)
