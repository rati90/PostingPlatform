from typing import Optional, List
from pydantic import BaseModel

from beanie import Document


class User(Document):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Comment(BaseModel):
    created_by: str
    comment: str


class Post(Document):
    created_by: str
    name: Optional[str]
    desc: str
    comments: Optional[List[Comment]] = []




