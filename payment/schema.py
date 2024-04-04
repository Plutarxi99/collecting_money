from typing import Any

from pydantic import BaseModel


class PaymentSchema(BaseModel):
    amount: int
    recipient: Any
    sender: Any
    status: bool
