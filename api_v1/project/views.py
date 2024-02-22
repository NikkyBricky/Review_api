import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.project.schemas import ProjectCreate
from core.models import db_helper, Project
from api_v1.project import crud, dependencies
from ..user.crud import get_user_by_user_id
from ..review.crud import create_review
from ..review.schemas import ReviewCreate
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

    if not await get_user_by_user_id(
        session=session,
        user_id=project_in_user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"user with user_id {project_in_user_id} is not authorised"}
        )

    await dependencies.get_review_by_user_id(
        session=session,
        user_id=project_in_user_id
    )

    project_list = await dependencies.get_project_by_project_difficulty(
        session=session,
        project_difficulty=project_in_difficulty,
    )

    if project_list:

        review_project: Project = project_list[0]
        review_project_user_id = review_project.user_id

        if project_in_user_id == review_project_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": f"project from user with user_id {project_in_user_id} already exists"}
            )

        await crud.delete_project(
            session=session,
            project=review_project
        )

        await create_review(
            session=session,
            review_in=ReviewCreate(user_id=project_in_user_id, review_id=review_project_user_id)
        )

        await create_review(
            session=session,
            review_in=ReviewCreate(user_id=review_project_user_id, review_id=project_in_user_id)
        )

        return {"message": f"successfully found pair for user_id {project_in.user_id}",
                "user for review": review_project}

    else:

        try:
            await crud.create_project(session=session, project_in=project_in)
            raise HTTPException(
                status_code=status.HTTP_201_CREATED,
                detail={"message": f"successfully added project from user "
                        f"with user_id {project_in_user_id} to database"}
            )

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": f"project from user with user_id {project_in_user_id} already exists"}
            )


@router.delete("/delete-project", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    project = await dependencies.get_project_by_user_id(session=session, user_id=user_id)
    await crud.delete_project(
        session=session,
        project=project
    )
