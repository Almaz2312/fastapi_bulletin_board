from fastapi import Request, status, HTTPException


class BasePermission:
    async def check_permission(self, request: Request):
        raise NotImplementedError()

    async def has_permission(self, request: Request) -> bool:
        if not await self.check_permission(request):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return True

    async def __call__(self, request: Request):
        await self.has_permission(request)


class AllowAny(BasePermission):
    async def check_permission(self, request: Request) -> bool:
        return True


class IsAuthenticated(BasePermission):
    async def check_permission(self, request: Request):
        return request.user.is_authenticated
