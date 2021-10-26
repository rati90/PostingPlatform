from typing import Union
from fastapi import HTTPException, status

from .users import User, Posts


async def get_user(email: str) -> Union[User, None]:
    return await User.find_one(User.email == email)


"""async def get_post(id):
    credentials_exception = HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="Could not find the post",
    )
    current_post = await Posts.get(id)
    if current_post is None:
        return credentials_exception
    return current_post"""
