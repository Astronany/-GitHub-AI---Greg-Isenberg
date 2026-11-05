"""Customer accounts. Reads are public; creating an account requires a token."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_token
from app.schemas import User, UserCreate
from app.store import store

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
def list_users() -> list[dict]:
    return store.list_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int) -> dict:
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "",
    response_model=User,
    status_code=201,
    responses={401: {"description": "Missing or invalid bearer token"}},
)
def create_user(body: UserCreate, _: str = Depends(require_token)) -> dict:
    return store.create_user(name=body.name, username=body.username, email=body.email)
