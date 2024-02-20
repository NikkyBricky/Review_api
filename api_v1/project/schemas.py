from pydantic import BaseModel
from typing import Annotated
from fastapi import Path


class ProjectBase(BaseModel):
    project_link: str
    project_difficulty: Annotated[int, Path(ge=1, le=10)]
    user_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectSchema(ProjectBase):
    pass
