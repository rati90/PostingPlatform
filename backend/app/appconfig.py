import motor.motor_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie

from .routers.views import router
from .routers.users import User, Post, Comment
from .config import settings
from .Server.config_socketatio import sio, subapi



def create_app() -> FastAPI:
    app = FastAPI()
    subapi = FastAPI()

    app.mount("/s", subapi)

    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )



    @app.on_event("startup")
    async def startup_event():
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(database=client[settings.MONGODB_DATABASE_NAME], document_models=[User, Post, Comment])

    return app

