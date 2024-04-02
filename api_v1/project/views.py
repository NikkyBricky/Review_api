from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.project.schemas import ProjectCreate
from core.models import db_helper, Project
from api_v1.project import crud, find_user_info
from api_v1.user.find_user_info import get_user_by_user_id
from api_v1.review.crud import create_review
from api_v1.review.schemas import ReviewCreate
router = APIRouter(tags=["Projects"])


@router.post("/find-pair-or-create-project")
async def find_pair_or_create_project(
        project_in: ProjectCreate,
        response: Response,
        session: AsyncSession = Depends(db_helper.session_dependency),
        ):

    project_in_difficulty = project_in.project_difficulty
    project_in_user_id = project_in.user_id

    await get_user_by_user_id(
        session=session,
        user_id=project_in_user_id
    )

    await find_user_info.get_review_by_user_id(
        session=session,
        user_id=project_in_user_id
    )

    project_list = await find_user_info.get_project_by_project_difficulty(
        session=session,
        project_difficulty=project_in_difficulty,
    )

    if not project_list:
        await crud.create_project(session=session, project_in=project_in)

        response.status_code = status.HTTP_201_CREATED
        return {"message": f"successfully added project from user with user_id {project_in_user_id} to database"}

    review_project: Project = project_list[0]
    review_project_user_id = review_project.user_id

    if project_in_user_id == review_project_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"project from user with user_id {project_in_user_id} already exists"}
        )

    await crud.delete_project(
        session=session,
        user_id=review_project_user_id
    )

    await create_review(
        session=session,
        review_in_1=ReviewCreate(user_id=project_in_user_id, review_id=review_project_user_id),
        review_in_2=ReviewCreate(user_id=review_project_user_id, review_id=project_in_user_id)
    )

    return {"message": f"successfully found pair for user_id {project_in.user_id}",
            "user_data": project_in,
            "user for review": review_project}


@router.delete("/delete-project", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    await crud.delete_project(
        session=session,
        user_id=user_id
    )
    return {"message": f"successfully deleted project from user with user_id {user_id}"}
