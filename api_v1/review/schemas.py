from pydantic import BaseModel
from typing import Annotated
from annotated_types import MinLen, MaxLen


class ReviewBase(BaseModel):
    review_text: Annotated[str, MinLen(70), MaxLen(2000)]
    review_id: int
    user_id: int


class ReviewCreate(ReviewBase):
    review_text: None = None


class ReviewSend(ReviewBase):
    review_id: None = None


class ReviewSchema(ReviewBase):
    review_text: str = "no review"
    review_id: None = None
    user_id: int
