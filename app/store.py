"""In-memory catalog and orders for the demo API.

Data lives in the process. Tests reset it; a real deployment would replace
this module with a database.
"""

from __future__ import annotations


class ConflictError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class MissingReferenceError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class MemoryStore:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.users: dict[int, dict] = {
            1: {
                "id": 1,
                "name": "Ada Lovelace",
                "username": "ada",
                "email": "ada@example.com",
            },
            2: {
                "id": 2,
                "name": "Grace Hopper",
                "username": "grace",
                "email": "grace@example.com",
            },
        }
        self.items: dict[int, dict] = {
            1: {
                "id": 1,
                "sku": "NB-100",
                "name": "Field notebook",
                "price_cents": 1299,
            },
            2: {
                "id": 2,
                "sku": "PN-010",
                "name": "Graphite pencil",
                "price_cents": 199,
            },
        }
        self.orders: dict[int, dict] = {
            1: {
                "id": 1,
                "user_id": 1,
                "item_id": 1,
                "quantity": 2,
                "status": "placed",
            },
        }
        self._user_seq = 3
        self._order_seq = 2

    def list_users(self) -> list[dict]:
        return [dict(self.users[key]) for key in sorted(self.users)]

    def get_user(self, user_id: int) -> dict | None:
        user = self.users.get(user_id)
        return dict(user) if user else None

    def create_user(self, *, name: str, username: str, email: str) -> dict:
        email_key = email.lower()
        username_key = username.lower()
        for user in self.users.values():
            if user["email"].lower() == email_key:
                raise ConflictError("Email already exists")
            if user["username"].lower() == username_key:
                raise ConflictError("Username already exists")
        user = {
            "id": self._user_seq,
            "name": name,
            "username": username,
            "email": email_key,
        }
        self.users[self._user_seq] = user
        self._user_seq += 1
        return dict(user)

    def list_items(self) -> list[dict]:
        return [dict(self.items[key]) for key in sorted(self.items)]

    def get_item(self, item_id: int) -> dict | None:
        item = self.items.get(item_id)
        return dict(item) if item else None

    def list_orders(self) -> list[dict]:
        return [dict(self.orders[key]) for key in sorted(self.orders)]

    def get_order(self, order_id: int) -> dict | None:
        order = self.orders.get(order_id)
        return dict(order) if order else None

    def create_order(self, *, user_id: int, item_id: int, quantity: int) -> dict:
        if user_id not in self.users:
            raise MissingReferenceError("User not found")
        if item_id not in self.items:
            raise MissingReferenceError("Item not found")
        order = {
            "id": self._order_seq,
            "user_id": user_id,
            "item_id": item_id,
            "quantity": quantity,
            "status": "placed",
        }
        self.orders[self._order_seq] = order
        self._order_seq += 1
        return dict(order)


store = MemoryStore()
