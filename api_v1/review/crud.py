from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_review_by_user_id
from .schemas import ReviewCreate, ReviewSend, ReviewSchema
from core.models import Review


async def create_review(
        session: AsyncSession,
        review_in_1: ReviewCreate,
        review_in_2: ReviewCreate
):
    review_1 = Review(**review_in_1.model_dump(exclude_unset=True))
    review_2 = Review(**review_in_2.model_dump(exclude_unset=True))

    session.add(review_1)
    session.add(review_2)

    await session.commit()

    await session.refresh(review_1)
    await session.refresh(review_2)



async def process_review(
        session: AsyncSession,
        review_in: ReviewSend
):
    user_id = review_in.user_id

    user_review = await get_review_by_user_id(
        session=session,
        user_id=user_id
    )

    review_id = user_review.review_id

    review_user_review = await get_review_by_user_id(
        session=session,
        user_id=review_id
    )
    review_user_review_text = review_user_review.review_text
    if review_user_review_text == "no review":

        for review_data, value in review_in.model_dump(exclude_none=True).items():
            setattr(user_review, review_data, value)
        await session.commit()

        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail={"message": f"successfully added review from user with user_id {user_id} to database"}
        )

    user_review_text = review_in.review_text

    await session.delete(user_review)

    await session.delete(review_user_review)

    await session.commit()

    return user_id, review_user_review_text, review_id, user_review_text


async def delete_review(
        session: AsyncSession,
        user_id: int
):
    review_schema = ReviewSchema(user_id=user_id, review_text="no review")
    review = await get_review_by_user_id(session=session, user_id=user_id)

    if review.review_text == "no review":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"user with user_id {user_id} does not have a review yet"}
        )

    for review_data, value in review_schema.model_dump(exclude_none=True).items():
        setattr(review, review_data, value)

    await session.commit()
