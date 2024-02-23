from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ReviewCreate
from core.models import Review


async def create_review(
        session: AsyncSession,
        review_in: ReviewCreate
) -> Review:
    review = Review(**review_in.model_dump(exclude_unset=True))
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review
