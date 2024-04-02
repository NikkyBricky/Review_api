from typing import Annotated
from annotated_types import MinLen

from core.config import settings
from pydantic import BaseModel, Field
from pydantic import field_validator as validator
from .link_validator import CheckLink


class ProjectBase(BaseModel):
    project_link: str
    project_difficulty: int = Field(ge=1, le=10)
    user_id: int
    rules: Annotated[str, MinLen(30)] = settings.rules_for_review

    @validator('project_link')
    def link_checking(cls, value):
        return CheckLink(
            link=value,
            full=True
        ).check_link()


class ProjectCreate(ProjectBase):
    pass
