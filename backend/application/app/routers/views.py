from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .users import User, Posts
from .usersout import UserOut
from ..internal.services.auth import get_password_hash, get_current_user,authenticate_user, create_access_token
from ..config import settings

router = APIRouter(prefix="")


@router.post("/api/signup", status_code=201, response_model=UserOut)
async def user_signup(user_data: User):
    user_data.password = get_password_hash(user_data.password)
    return await user_data.save()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


@router.get("/api/login", response_model=UserOut)
async def get_user(current_user: User = Depends(get_current_user)):
    print(current_user.id)
    return current_user


@router.post("/api/create/post")
async def create_post(post_data: Posts, current_user: User = Depends(get_current_user)):
    post_data.created_by = str(current_user.id)
    return await post_data.save()

#@router.get("/api/update/post/{id}")


@router.post("/api/get/post/{id}")
async def get_post(id):
    return await Posts.get(id)

