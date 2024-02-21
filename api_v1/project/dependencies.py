from typing import Annotated

from fastapi import Path, status, HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Project


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
        detail="project from user with such user_id not found"
    )

