import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserSchema, UserCreate
from core.models import db_helper
from . import crud
from .dependencies import get_project_by_user_id, get_review_by_user_id, get_user_by_user_id

router = APIRouter(tags=["User"])


@router.post("/register-user",
             status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        await crud.create_user(session=session, user_in=user_in)
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail={"message": "successfully added user to database"}
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "user already exists"}
        )


@router.post("/login-user")
async def login_user(
        user_in: UserSchema,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await crud.log_in_user(session=session, user_in=user_in)
    return {"message": "password is correct"}


@router.delete("/delete-user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    user = await get_user_by_user_id(
        session=session,
        user_id=user_id
    )

    await get_project_by_user_id(
        session=session,
        user_id=user_id
    )

    await get_review_by_user_id(
        session=session,
        user_id=user_id
    )

    await crud.delete_user(session=session, user=user)
