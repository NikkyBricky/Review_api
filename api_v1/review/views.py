from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ReviewSend, ReviewSchema
from core.models import db_helper
from .crud import get_review_by_user_id
router = APIRouter(tags=["Reviews"])


@router.post("/send-review")
async def send_review(
        review_in: ReviewSend,
        session: AsyncSession = Depends(db_helper.session_dependency)
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

    if review_user_review.review_text == "no review":

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

    return {"message": f"user with user_id {review_id} has got a review for user with user_id {user_id}",
            "reviews": {f"review for user_id {review_id}": user_review_text,
                        f"review for user_id {user_id}": review_user_review.review_text}
            }


@router.post("/delete-review-text")
async def delete_review_text(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    review_schema = ReviewSchema(user_id=user_id, review_text="no review")
    review = await get_review_by_user_id(session=session, user_id=user_id)
    for review_data, value in review_schema.model_dump(exclude_none=True).items():
        setattr(review, review_data, value)
    await session.commit()
    return {"message": f"Successfully deleted review from user with user_id {user_id}"}
