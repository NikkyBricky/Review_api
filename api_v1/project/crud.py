from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path
from .schemas import ProjectCreate
from core.models import Project
from typing import Annotated


async def create_project(
        session: AsyncSession,
        project_in: ProjectCreate
) -> Project:
    project = Project(**project_in.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


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


async def delete_project(
        session: AsyncSession,
        project: Project,
):
    await session.delete(project)
    await session.commit()
