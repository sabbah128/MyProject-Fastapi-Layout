from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=150, description="Username of the user")
    password: str = Field(..., description="password of the user")


class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=150, description="Username of the user")
    password: str = Field(..., description="password of the user")
    password_confirm: str = Field(..., description="confirm password of the user")

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not password_confirm ==validation.data.get("password"):
            raise ValueError("Password doesnt match!")
        return password_confirm
