from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import UserRelationMixin


class Review(UserRelationMixin, Base):
    _user_back_populates = "review"
    _user_id_unique: bool = True
    review_text: Mapped[str] = mapped_column(default="no review", server_default="no review")
    review_id: Mapped[int]
