"""Orders. Every route requires the demo bearer token."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_token
from app.schemas import Order, OrderCreate
from app.store import store

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(require_token)],
)


@router.get(
    "",
    response_model=list[Order],
    responses={401: {"description": "Missing or invalid bearer token"}},
)
def list_orders() -> list[dict]:
    return store.list_orders()


@router.get(
    "/{order_id}",
    response_model=Order,
    responses={
        401: {"description": "Missing or invalid bearer token"},
        404: {"description": "Order not found"},
    },
)
def get_order(order_id: int) -> dict:
    order = store.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post(
    "",
    response_model=Order,
    status_code=201,
    responses={
        400: {"description": "User or item does not exist"},
        401: {"description": "Missing or invalid bearer token"},
    },
)
def create_order(body: OrderCreate) -> dict:
    return store.create_order(
        user_id=body.user_id,
        item_id=body.item_id,
        quantity=body.quantity,
    )
