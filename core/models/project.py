from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import UserRelationMixin
from core.config import settings


class Project(UserRelationMixin, Base):
    _user_back_populates = "project"
    _user_id_unique: bool = True
    project_link: Mapped[str]
    project_difficulty: Mapped[int]
    rules: Mapped[str] = mapped_column(
        default=settings.rules_for_review,
        server_default=settings.rules_for_review)
