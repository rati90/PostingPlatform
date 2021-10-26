from typing import Optional

from beanie import Document


class User(Document):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Posts(Document):
    created_by: Optional[str]
    name: Optional[str]
    desc: str
