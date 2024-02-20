import sqlalchemy
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.schemas import UserSchema, UserCreate
from core.models import db_helper, User
from api_v1.user import crud
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
    return {"success": await crud.log_in_user(session=session, user_in=user_in)}


# @router.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(
#         user: User = Depends(get_user_by_user_id),
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)
# ) -> None:
#     await crud.delete_user(session=session, user=user)


@router.get("/check_user_exists/{user_id}")
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

