from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.project.schemas import ProjectCreate
from core.models import db_helper, Project
from api_v1.project import crud, dependencies
# TODO Я на самом деле не любитель относительных импортов, как по мне лучше сделать тут все абсолютным
from ..user.dependencies import get_user_by_user_id
from ..review.crud import create_review
from ..review.schemas import ReviewCreate
router = APIRouter(tags=["Projects"])


@router.post("/find-pair-or-create-project")
async def find_pair_or_create_project(
        project_in: ProjectCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
        ):
    # TODO Вообще не понял что такое project_in
    project_in_difficulty = project_in.project_difficulty
    project_in_user_id = project_in.user_id
    # TODO Я бы всю эту логику вынес в еще один класс-сервис. Это конечно уже не MVC, но мне кажется это будет куда удобней. Так же именование файле dependencies мне не очень нравится, вообще не понял сразу что там лежит
    # UPD Так у вас же не исопользуются два нижних запроса, или это чисто для того, чтобы он ошибку швырнул? Тогда зачем эти функции что-то могут возвращать?
    await get_user_by_user_id(
        session=session,
        user_id=project_in_user_id
    )

    await dependencies.get_review_by_user_id(
        session=session,
        user_id=project_in_user_id
    )

    project_list = await dependencies.get_project_by_project_difficulty(
        session=session,
        project_difficulty=project_in_difficulty,
    )
    # TODO Вот тут, чтобы уменьшить вложенность можно поменять местами else и if, инвертировав условие. В таком случае на три порядка меньше
    if project_list:
        # TODO А если проектов несколько? Это стоило рандомизировать видимо
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
        # TODO Для возвращаемых значений так же можно делать пайдэнтик модели
        return {"message": f"successfully found pair for user_id {project_in.user_id}",
                "user_data": project_in,
                "user for review": review_project}

    else:

        await crud.create_project(session=session, project_in=project_in)
        # TODO Я чет заржал с этого, логически вообще мем, вы рэйзите ошибку, что все хорошо создалось
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail={"message": f"successfully added project from user "
                    f"with user_id {project_in_user_id} to database"}
        )


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
