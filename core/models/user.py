from sqlalchemy.orm import Mapped
from .base import Base


class User(Base):
    user_id: Mapped[int]
    password: Mapped[bytes]