from fastapi import APIRouter
from .user.views import router as user_router
from .project.views import router as project_router
from .review.views import router as review_router
router = APIRouter()
router.include_router(router=user_router, prefix="/users")
router.include_router(router=project_router, prefix="/projects")
router.include_router(router=review_router, prefix="/reviews")
