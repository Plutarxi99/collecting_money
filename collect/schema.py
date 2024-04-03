from typing import Any

from pydantic import BaseModel
from datetime import datetime

from users.models import User


class CollectSchema(BaseModel):
    author: Any
    title: str
    reason: int
    description: str | None = None
    amount: int
    amount_now: int | None = 0
    count_people: int | None = 0
    photo: str | None = None
    end_of_event: datetime
    # donates: set | None = None
