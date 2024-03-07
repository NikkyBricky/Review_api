from pydantic import BaseModel, Field
from typing import Annotated
from annotated_types import MinLen

from core.config import settings


class ProjectBase(BaseModel):
    project_link: str
    project_difficulty: int = Field(ge=1, le=10)
    user_id: int
    rules: Annotated[str, MinLen(30)] = settings.rules_for_review


class ProjectCreate(ProjectBase):
    pass


class ProjectSchema(ProjectBase):
    pass
