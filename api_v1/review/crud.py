from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ReviewCreate
from core.models import Review
from fastapi import HTTPException, status


async def create_review(
        session: AsyncSession,
        review_in: ReviewCreate
) -> Review:
    review = Review(**review_in.model_dump(exclude_unset=True))
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def get_review_by_user_id(
        session: AsyncSession,
        user_id: int
):
    review = await session.get(Review, user_id)
    if review:
        return review
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": f"user with user_id {user_id} does not have a pair to review yet"})
