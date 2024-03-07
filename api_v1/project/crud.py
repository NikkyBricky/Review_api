import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import dependencies
from .schemas import ProjectCreate
from core.models import Project


async def create_project(
        session: AsyncSession,
        project_in: ProjectCreate
) -> Project:
    project = Project(**project_in.model_dump(exclude_unset=True))

    session.add(project)

    try:

        await session.commit()

    except sqlalchemy.exc.IntegrityError:

        project_in_user_id = project_in.user_id
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"project from user with user_id {project_in_user_id} already exists"}
        )

    await session.refresh(project)
    return project


async def delete_project(
        session: AsyncSession,
        user_id: int,
):
    project = await dependencies.get_project_by_user_id(session=session, user_id=user_id)
    await session.delete(project)
    await session.commit()
