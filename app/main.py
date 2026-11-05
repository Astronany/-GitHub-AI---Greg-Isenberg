"""Demo shop API entrypoint.

Run it with:
    uvicorn app.main:app --host 127.0.0.1 --port 8000

pytest imports the same ``app`` object and serves it in-process.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import items, orders, users
from app.store import ConflictError, MissingReferenceError


def create_app() -> FastAPI:
    app = FastAPI(
        title="Demo Business API",
        version="1.0.0",
        summary="Controllable shop API used as the system under test.",
    )

    @app.exception_handler(ConflictError)
    async def conflict_handler(
        _request: Request, exc: ConflictError
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.detail})

    @app.exception_handler(MissingReferenceError)
    async def missing_reference_handler(
        _request: Request, exc: MissingReferenceError
    ) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", tags=["meta"])
    def root() -> dict[str, str]:
        return {
            "name": "Demo Business API",
            "health": "/health",
            "docs": "/docs",
        }

    app.include_router(users.router)
    app.include_router(items.router)
    app.include_router(orders.router)
    return app


app = create_app()
