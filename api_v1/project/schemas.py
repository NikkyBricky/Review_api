from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    project_link: str
    project_difficulty: int = Field(ge=1, le=10)
    user_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectSchema(ProjectBase):
    pass
