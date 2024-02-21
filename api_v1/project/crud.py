from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ProjectCreate
from core.models import Project


async def create_project(
        session: AsyncSession,
        project_in: ProjectCreate
) -> Project:
    project = Project(**project_in.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def delete_project(
        session: AsyncSession,
        project: Project,
):
    await session.delete(project)
    await session.commit()
