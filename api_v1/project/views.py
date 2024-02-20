import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.project.schemas import ProjectCreate
from core.models import db_helper, Project
from api_v1.project import crud

router = APIRouter(tags=["Projects"])


async def get_project_by_user_id(
    session: AsyncSession,
    user_id: int,
) -> Project | None:
    return await session.get(Project, user_id)


@router.post("/find-pair-or-create-project")
async def find_pair_or_create_project(
        project_in: ProjectCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
        ):
    project_in_difficulty = project_in.project_difficulty
    project_in_user_id = project_in.user_id
    project_list = await crud.get_project_by_project_difficulty(
        session=session,
        project_difficulty=project_in_difficulty,
    )
    if project_list:

        review_project: Project = project_list[0]
        review_project_user_id = review_project.user_id

        if project_in_user_id == review_project_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"project from user with user_id {project_in_user_id} already exists"
            )

        await crud.delete_project(
            session=session,
            project=review_project
        )

        return {"message": f"successfully found pair for user_id {project_in.user_id}",
                "user for review": review_project}

    else:
        try:
            await crud.create_project(session=session, project_in=project_in)
            return "successfully added project to database"

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user already exists"
            )


