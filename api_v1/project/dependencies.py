from typing import Annotated

from fastapi import Path, status, HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Project, Review


async def get_project_by_project_difficulty(
        session: AsyncSession,
        project_difficulty: Annotated[int, Path(ge=1, le=10)]
) -> list[Project]:
    stmt = (
        select(Project)
        .where(Project.project_difficulty == project_difficulty)
        .order_by(Project.user_id)
    )
    result: Result = await session.execute(stmt)
    projects = result.scalars().all()
    return list(projects)


async def get_project_by_user_id(
        session: AsyncSession,
        user_id: int
):
    project = await session.get(Project, user_id)
    if project:
        return project

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": f"project from user with user_id {user_id} not found"}
    )


async def get_review_by_user_id(
        session: AsyncSession,
        user_id: int
):
    review = await session.get(Review, user_id)
    if review:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": f"user with user_id {user_id} already has got a project for review"}
        )
