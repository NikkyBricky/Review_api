from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserSchema, UserCreate
from core.models import db_helper
from . import crud

router = APIRouter(tags=["User"])


@router.post("/register-user",
             status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):

    await crud.create_user(session=session, user_in=user_in),
    return {"message": "successfully added user to database"}


@router.post("/login-user", status_code=status.HTTP_200_OK)
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

    await crud.delete_user(session=session, user_id=user_id)
