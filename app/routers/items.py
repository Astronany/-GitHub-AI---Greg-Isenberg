"""Product catalog. Read-only seed data for the demo shop."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas import Item
from app.store import store

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[Item])
def list_items() -> list[dict]:
    return store.list_items()


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> dict:
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
