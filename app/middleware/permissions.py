from typing import Type, Any

from starlette.requests import Request

from app.permissions.base import BasePermission, AllowAny


class PermissionMiddleware:
    def __init__(self, permission_class: Type[BasePermission] = AllowAny, obj: Any = None):
        self.permission_class = permission_class()
        self.obj = obj

    async def __call__(self, request: Request):
        if self.obj:
            await self.permission_class.has_object_permission(request, self.obj)
        else:
            await self.permission_class.has_permission(request)
