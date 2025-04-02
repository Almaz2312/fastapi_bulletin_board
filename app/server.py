import contextlib

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.authentication import AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse

from app.api.base import api_router
from app.config.settings import settings
from app.generics.exceptions import validation_exception_handler
from app.db.session import sessionmanager
from app.middleware.authentication import BaseAuthentication


def include_router(app: FastAPI):
    app.include_router(api_router)


def add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        AuthenticationMiddleware,
        backend=BaseAuthentication(),
        on_error=on_error,
    )


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


def use_bearer_schema(app: FastAPI):
    """
    Использовать BearerAuth метод в свагере.
    Нужно лишь передать токен без ничего
    """
    app.openapi_schema = app.openapi()
    app.openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    app.openapi_schema["security"] = [{"BearerAuth": []}]


def add_exception_handler(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ResponseValidationError, validation_exception_handler)


def on_error(conn: HTTPConnection, exc: AuthenticationError) -> JSONResponse:
    return JSONResponse(
        content={"error": str(exc)},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def start_application():
    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        debug=settings.DEBUG
    )

    add_middleware(app)
    include_router(app)
    use_bearer_schema(app)
    add_exception_handler(app)
    return app


app = start_application()
