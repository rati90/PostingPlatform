from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .users import User, Post, Comment
from .usersout import UserOut
from ..internal.services.auth import get_password_hash, get_current_user, authenticate_user, create_access_token
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
async def create_post(post_data: Post, current_user: User = Depends(get_current_user)):
    post_data.created_by = str(current_user.email)
    return await post_data.save()


@router.post("/api/update/post/{post_id}")
async def update_post(post_id: str, update_desc: str, current_user: User = Depends(get_current_user)):
    if Post.created_by == str(current_user.email):
        post_update = await Post.get(post_id)

        return await post_update.set({Post.desc: update_desc})


@router.get("/api/get/post/{post_id}")
async def get_post(post_id: str):
    return await Post.get(post_id)


@router.post("/api/delete/post/{post_id}")
async def delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    if Post.created_by == str(current_user.email):
        post_delete = await Post.get(post_id)
        return await post_delete.delete()


@router.post("/api/create/comment/{post_id}")
async def make_a_comment(
        post_id: str,
        new_comments: Comment,
        current_user: User = Depends(get_current_user),
):
    comment_data = await Post.get(post_id)
    new_comments.created_by = str(current_user.email)
    await new_comments.save()
    comment_data.comments.append(new_comments)
    return await comment_data.save()


@router.post("/api/update/comment/{comment_id}")
async def update_comment(comment_id: str, renewed_comment: str, current_user: User = Depends(get_current_user)):
    current_comment = await Comment.get(comment_id)
    if current_comment.created_by == str(current_user.email):
        return await current_comment.set({current_comment.comment: renewed_comment})


@router.post("/api/delete/comment/{comment_id}")
async def delete_comment(comment_id, current_user: User = Depends(get_current_user)):
    comment_data = await Comment.get(comment_id)
    print(comment_data.created_by)
    if comment_data.created_by == str(current_user.email):

        comment_delete = await Comment.get(comment_id)
        return await comment_delete.delete()
