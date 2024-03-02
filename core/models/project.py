from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import UserRelationMixin


class Project(UserRelationMixin, Base):
    _user_back_populates = "project"
    _user_id_unique: bool = True
    project_link: Mapped[str]
    project_difficulty: Mapped[int]
