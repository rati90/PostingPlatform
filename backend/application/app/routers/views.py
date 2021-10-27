from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .users import User, Posts, Comments
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
async def get_log(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/api/create/post")
async def create_post(post_data: Posts, current_user: User = Depends(get_current_user)):
    post_data.created_by = str(current_user.email)
    return await post_data.save()


@router.post("/api/update/post/{post_id}")
async def update_post(post_id: str, update_desc: str, current_user: User = Depends(get_current_user)):
    if Posts.created_by == str(current_user.email):
        post_update = await Posts.get(post_id)

        return await post_update.set({Posts.desc: update_desc})


@router.get("/api/get/post/{post_id}")
async def get_post(post_id):
    return await Posts.get(post_id)


@router.post("/api/delete/post/{post_id}")
async def delete_post(post_id, current_user: User = Depends(get_current_user)):
    if Posts.created_by == str(current_user.email):
        post_delete = await Posts.get(post_id)
        return await post_delete.delete()


@router.post("/api/create/comment/{post_id}")
async def make_a_comment(
        post_id,
        comment_data: Comments,
        current_user: User = Depends(get_current_user),
                        ):

        comment_data.created_by = str(current_user.email)
        comment_data.created_for_post = str(post_id)

        return await comment_data.save()


@router.post("/api/update/comment/{comment_id}")
async def update_comment(comment_id, renewed_comment: str, current_user: User = Depends(get_current_user)):
    if Comments.created_by == str(current_user.email):
        comment_update = await Comments.get(comment_id)

        return await comment_update.set({Comments.comment: renewed_comment})


@router.get("/api/get/comment/{comment_id}")
async def get_comment(comment_id):
    return await Comments.get(comment_id)


@router.post("/api/delete/comment/{comment_id}")
async def delete_comment(comment_id, current_user: User = Depends(get_current_user)):
    if Comments.created_by == str(current_user.email):
        comment_delete = await Comments.get(comment_id)
        return await comment_delete.delete()
