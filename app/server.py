import structlog
from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.routes import api_router
from app.container import Container
from app.infra.config import settings
from app.shared.utils.error import DomainError

logger = structlog.get_logger()


def include_router(main_app: FastAPI) -> None:
    main_app.include_router(api_router, prefix=settings.API_V1_STR)


def setup_cors(main_app: FastAPI) -> None:
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        main_app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def domain_error_handler(request: Request, error: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": error.message},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return await http_exception_handler(
        request,
        HTTPException(
            500,
            "Internal server error",
            headers={
                "X-Request-ID": correlation_id.get() or "",
                "Access-Control-Expose-Headers": "X-Request-ID",
            },
        ),
    )


def create_app() -> FastAPI:
    container = Container()
    container.wire(packages=["app.api.api_v1"])

    main_app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    main_app.state.container = container
    setup_cors(main_app)
    include_router(main_app)
    main_app.add_exception_handler(DomainError, domain_error_handler)
    main_app.add_exception_handler(Exception, unhandled_exception_handler)

    # @main_app.on_event("startup")
    # async def startup() -> None:
    #     await db.connect_db()

    # @main_app.on_event("shutdown")
    # async def shutdown() -> None:
    #     await db.disconnect_db()

    return main_app


main_app = create_app()
