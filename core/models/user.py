from sqlalchemy.orm import Mapped, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .project import Project
    from .review import Review


class User(Base):
    user_id: Mapped[int]
    password: Mapped[bytes]

    project: Mapped["Project"] = relationship(back_populates="user", cascade="all, delete")
    review: Mapped["Review"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id}, password={self.password})"

    def __repr__(self):
        return str(self)
