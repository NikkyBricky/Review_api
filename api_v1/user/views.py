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


# @router.post("/delete-user")
# async def delete_user(
#         user: User,
#         session: AsyncSession = Depends(db_helper.session_dependency)
# ):
#     await crud.delete_user_parameters(session=session, user=user)
#     return {"message": "success"}


@router.get("/check_user_exists")
async def check_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    result = await crud.get_user(
        session=session,
        user_id=user_id
    )
    return f"user_found: {result}"

