import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .schemas import UserCreate, UserSchema
from core.models import User
from .dependencies import get_user_by_user_id, get_project_by_user_id, get_review_by_user_id


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
    user = await get_user_by_user_id(
        session=session,
        user_id=user_id
    )

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


async def delete_user(
        session: AsyncSession,
        user_id: int,
):
    user = await get_user_by_user_id(
        session=session,
        user_id=user_id
    )

    await get_project_by_user_id(
        session=session,
        user_id=user_id
    )

    await get_review_by_user_id(
        session=session,
        user_id=user_id
    )

    await session.delete(user)

    await session.commit()
