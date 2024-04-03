from typing import Any

from pydantic import BaseModel
from datetime import datetime


class PaymentSchema(BaseModel):
    amount: int
    recipient: Any
    sender: Any
    status: bool
