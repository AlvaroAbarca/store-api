from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.responses import JSONResponse
from tortoise import Tortoise

from src.core.auth import get_auth_router
from src.core.config import Environment, settings
from src.db.tortoise import lifespan
from src.router import api_router
from src.sales.routes import router as sales_router
from src.users.routes import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Store App",
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.DEBUG,
    )
    Tortoise.init_models(["src.users.models", "src.sales.models", "aerich.models"], "models")


    app.include_router(get_auth_router())
    app.include_router(api_router)
    app.include_router(users_router)
    app.include_router(sales_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        exc_str = f"{e}".replace("\n", " ").replace("   ", " ")
        logger.warning(f"{request}: {exc_str}")
        content = {"message": exc_str, "data": None}
        return JSONResponse(content=content, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    if settings.ENVIRONMENT == Environment.prod:
        logger.add("logs/store_app.log", rotation="1 day", retention="7 days")
    return app
app = create_app()
