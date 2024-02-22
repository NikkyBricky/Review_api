import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .schemas import UserCreate, UserSchema
from core.models import User


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
):
    password = UserCreate(**user_in.model_dump()).password
    user_id = UserCreate(**user_in.model_dump()).user_id
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    user = User(user_id=user_id, password=hashed_password)

    session.add(user)
    await session.commit()
    await session.refresh(user)


async def log_in_user(
        session: AsyncSession,
        user_in: UserSchema
) -> bool:
    password = UserSchema(**user_in.model_dump()).password
    user_id = UserSchema(**user_in.model_dump()).user_id
    user = await session.get(User, user_id)
    if user:
        correct_hashed_password = user.password
        result = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=correct_hashed_password,
        )
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "password is incorrect"}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"message": f"user with user_id {user_id} not found"}
    )


async def delete_user(
        session: AsyncSession,
        user: User,
):
    await session.delete(user)
    await session.commit()


async def get_user_by_user_id(
        session: AsyncSession,
        user_id: int
):
    user = await session.get(User, user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"message": f"user with user_id {user_id} not found"}
    )
