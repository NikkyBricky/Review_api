import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .schemas import UserCreate
from core.models import User


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    password = UserCreate(**user_in.model_dump()).password
    user_id = UserCreate(**user_in.model_dump()).user_id
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    user = User(user_id=user_id, password=hashed_password)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def log_in_user(
        session: AsyncSession,
        user_in: UserCreate
) -> bool:
    password = UserCreate(**user_in.model_dump()).password
    user_id = UserCreate(**user_in.model_dump()).user_id
    user = await session.get(User, user_id)
    if user:
        correct_hashed_password = user.password
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=correct_hashed_password,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"no user with user_id {user_id}"
    )


# async def delete_user_parameters(
#         session: AsyncSession,
#         user: User,
# ):
#     await session.delete(user)
#     await session.commit()


async def get_user(
        session: AsyncSession,
        user_id: int
) -> bool:
    found = await session.get(User, user_id)
    if found:
        return True
    return False
