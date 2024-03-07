from pydantic import BaseModel
from typing import Annotated
from annotated_types import MinLen, MaxLen


class ReviewBase(BaseModel):
    user_id: int


class ReviewCreate(ReviewBase):
    review_id: int


class ReviewSend(ReviewBase):
    review_text: Annotated[str, MinLen(70), MaxLen(2000)]


class ReviewDelete(ReviewBase):
    review_text: str = "no review"
