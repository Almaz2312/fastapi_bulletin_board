from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors: dict = {}
    for error in exc.errors():
        field = error["loc"][-1]
        message = error["msg"]
        if field in errors:
            errors[field].append(message)
        else:
            errors[field] = [message]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"error": errors}
    )
