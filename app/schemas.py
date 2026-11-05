"""Request and response bodies for the demo shop API."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=32, pattern=r"^[A-Za-z0-9_]+$")
    email: str = Field(min_length=3, max_length=254)

    @field_validator("name", "username", "email")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("invalid email")
        return value.lower()


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str


class Item(BaseModel):
    id: int
    sku: str
    name: str
    price_cents: int


class OrderCreate(BaseModel):
    user_id: int = Field(ge=1)
    item_id: int = Field(ge=1)
    quantity: int = Field(ge=1, le=100)


class Order(BaseModel):
    id: int
    user_id: int
    item_id: int
    quantity: int
    status: str
