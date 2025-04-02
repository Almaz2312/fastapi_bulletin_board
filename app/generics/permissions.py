from typing import Any

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request


class BasePermission:

    async def check_permission(self, request: Request) -> bool:
        raise NotImplementedError()

    async def has_permission(self, request: Request) -> bool:
        if not await self.check_permission(request):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this operation."
            )
        return True

    async def has_object_permission(self, request: Request, obj: Any) -> bool:
        raise NotImplementedError()

    async def __call__(self, request: Request, *args, **kwargs):
        await self.has_permission(request)


class AllowAny(BasePermission):
    async def check_permission(self, request: Request) -> bool:
        return True


class IsAuthenticated(BasePermission):
    async def check_permission(self, request: Request) -> bool:
        return request.user.is_authenticated
