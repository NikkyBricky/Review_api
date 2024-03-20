from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ReviewSend
from core.models import db_helper
from .crud import process_review, delete_review

router = APIRouter(tags=["Reviews"])


@router.post("/send-review")
async def send_review(
        review_in: ReviewSend,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    pairs = await process_review(session=session, review_in=review_in)

    user_id = pairs[0]
    review_user_review_text = pairs[1]
    review_id = pairs[2]
    user_review_text = pairs[3]

    return {"message": f"user with user_id {review_id} has got a review for user with user_id {user_id}",
            "reviews": {"user_id_1": {review_id},
                        "review_for_1": user_review_text,
                        "user_id_2": {user_id},
                        "review_for_2": review_user_review_text}
            }


@router.post("/delete-review-text")
async def delete_review_text(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    await delete_review(session=session, user_id=user_id)

    return {"message": f"Successfully deleted review from user with user_id {user_id}"}
