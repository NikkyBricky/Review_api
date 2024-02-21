import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserSchema, UserCreate
from core.models import db_helper
from . import crud
from .crud import get_user_by_user_id
router = APIRouter(tags=["User"])


@router.post("/register-user",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        return await crud.create_user(session=session, user_in=user_in)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists"
        )


@router.post("/login-user")
async def login_user(
        user_in: UserSchema,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await crud.log_in_user(session=session, user_in=user_in)
    return "password is correct"


@router.delete("/delete-user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await get_user_by_user_id(
        session=session,
        user_id=user_id
    )
    await crud.delete_user(session=session, user=user)


@router.get("/check_user_exists")
async def check_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    found_user = await crud.get_user_by_user_id(
        session=session,
        user_id=user_id
    )
    if found_user:
        result = True
    else:
        result = False
    return f"user_found: {result}"
