import pytest

from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from main import app
from app.routers.users import User, Post, Comment


@pytest.fixture()
async def client() -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            yield client
            await asyncio.sleep(0.1)
            await Post.get_motor_collection().drop()
            await User.get_motor_collection().drop()
            await Comment.get_motor_collection().drop()
