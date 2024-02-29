from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Review, User


async def get_review_by_user_id(
        session: AsyncSession,
        user_id: int
):

    review = await session.get(Review, user_id)

    if review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"cannot delete user with user_id {user_id} while he has got a review in database"}
        )


async def get_user_by_user_id(
        session: AsyncSession,
        user_id: int
):
    user = await session.get(User, user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"message": f"user with user_id {user_id} is unauthorised"}
    )
