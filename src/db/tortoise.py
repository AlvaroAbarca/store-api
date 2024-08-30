# from tortoise import Tortoise
# import os

# async def init_db():
#     # Here we create a SQLite DB using file "db.sqlite3"
#     #  also specify the app name of "models"
#     #  which contain models from "app.models"
#     user=os.getenv("MYSQL_USER", "mysql_zoco")
#     password=os.getenv("MYSQL_PASSWORD", "zoco2019")
#     host=os.getenv("MYSQL_HOST", "mysqldb")
#     port=int(os.getenv("MYSQL_PORT", 3306))
#     db=os.getenv("MYSQL_DB", "zocodb")

#     await Tortoise.init(
#         db_url='mysql://{user}:{password}@{host}:{port}/{db}'.format(
#             user=user, password=password, host=host, port=port, db=db
#         ),
#         modules={'models': ['db.models', 'meli.models']}
#     )
#     # Generate the schema
#     await Tortoise.generate_schemas()

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from src.core.config import settings

TORTOISE_ORM = {
    "connections": { "default": settings.DATABASE_URI },
    "apps": {
        "models": {
            "models": ["src.users.models", "src.sales.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    # asyncpg://postgres:pass@db.host:5432/somedb
    async with RegisterTortoise(
        app,
        # db_url="asyncpg://postgres:postgres@localhost:5432/postgres",
        # modules={"models": ["src.db.models", "src.users.models", "aerich.models"]},
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,

    ):
        # db connected
        yield
        # app teardown
    # db connections closed
