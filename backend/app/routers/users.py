from datetime import datetime, time, timedelta
from typing import Optional, List
from fastapi import Body

from beanie import Document


class User(Document):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Comment(Document):
    created_by: str
    comment: str
    date_created: Optional[datetime] = Body(None)


class Post(Document):
    created_by: str
    name: Optional[str]
    desc: str
    date_created: Optional[datetime] = Body(None)
    comments: Optional[List[Comment]] = []





