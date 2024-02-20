from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: int
    password: str


class UserCreate(UserBase):
    pass


class UserSchema(UserBase):
    pass
