from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import find_user_info
from .schemas import ProjectCreate
from core.models import Project


async def create_project(
        session: AsyncSession,
        project_in: ProjectCreate
) -> Project:
    project_in_user_id = project_in.user_id

    project = await find_user_info.get_project_by_user_id(session=session, user_id=project_in_user_id)

    if not project:
        project = Project(**project_in.model_dump(exclude_unset=True))

        session.add(project)

        await session.commit()

        await session.refresh(project)
        return project

    else:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"project from user with user_id {project_in_user_id} already exists"}
        )


async def delete_project(
        session: AsyncSession,
        user_id: int,
):
    project = await find_user_info.get_project_by_user_id(session=session, user_id=user_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"project from user with user_id {user_id} not found"}
        )

    await session.delete(project)
    await session.commit()
