from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..user.dependencies import get_user_by_user_id
from core.models import Review, Project


async def get_review_by_user_id(
        session: AsyncSession,
        user_id: int
):
    await get_user_by_user_id(
        session=session,
        user_id=user_id
    )
    review = await session.get(Review, user_id)
    if review:
        return review

    project_exists = await get_project_by_user_id(
        session=session,
        user_id=user_id
    )
    if project_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"user with user_id {user_id} does not have a pair to review yet"}
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": f"user with user_id {user_id} has not sent a project yet"}
    )


async def get_project_by_user_id(
        session: AsyncSession,
        user_id: int
) -> bool:
    project = await session.get(Project, user_id)
    if project:
        return True
    return False
