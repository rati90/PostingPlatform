from pydantic import BaseModel


class UserOut(BaseModel):
    email: str
    first_name: str
    last_name: str

