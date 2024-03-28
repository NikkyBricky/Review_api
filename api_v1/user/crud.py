import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .auth import check_password, hash_password
from .schemas import UserCreate, UserSchema
from core.models import User
from .dependencies import get_user_by_user_id, get_review_by_user_id


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
):
    password = user_in.password
    user_id = user_in.user_id

    hashed_password = hash_password(password=password)

    user = User(user_id=user_id, password=hashed_password)

    session.add(user)
    try:
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        #TODO Я бы делал проверку на существование, так как ошибки - дело крайне многоресурсное
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "user already exists"}
        )

    await session.refresh(user)


async def log_in_user(
        session: AsyncSession,
        user_in: UserSchema
) -> bool:
    password = user_in.password
    user_id = user_in.user_id
    user = await get_user_by_user_id(
        session=session,
        user_id=user_id
    )

    correct_hashed_password = user.password
    result = check_password(correct_hashed_password=correct_hashed_password,
                            password=password)
    return result


async def delete_user(
        session: AsyncSession,
        user_id: int,
):
    user = await get_user_by_user_id(
        session=session,
        user_id=user_id
    )

    await get_review_by_user_id(
        session=session,
        user_id=user_id
    )

    await session.delete(user)

    await session.commit()
