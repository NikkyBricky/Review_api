from typing import Annotated
from annotated_types import MinLen
from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: int
    password: Annotated[str, MinLen(8)]


class UserCreate(UserBase):
    pass


class UserSchema(UserBase):
    pass
