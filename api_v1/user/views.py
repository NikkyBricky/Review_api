import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.schemas import UserSchema, UserCreate
from core.models import db_helper
from api_v1.user import crud

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
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return {"success": await crud.log_in_user(session=session, user_in=user_in)}
