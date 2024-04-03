from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    email: EmailStr

