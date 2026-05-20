"""FastAPI application entry point."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from tideguard_api.db import Base, engine
from tideguard_api.routers import (
    admin,
    auth,
    cleanups,
    education,
    forecast,
    leaderboard,
    reports,
    tiles,
)
from tideguard_api.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # In dev (sqlite), auto-create schema. In prod, use Alembic migrations.
    settings = get_settings()
    if settings.database_url.startswith("sqlite"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="TideGuard API",
        description="Backend API for TideGuard AI — marine debris forecasting + community cleanup.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz", tags=["health"])
    def healthz() -> dict:
        return {"status": "ok", "service": "tideguard-api", "version": "0.1.0"}

    @app.get("/", tags=["health"])
    def root() -> dict:
        return {"name": "TideGuard API", "docs": "/docs", "health": "/healthz"}

    app.include_router(auth.router)
    app.include_router(forecast.router)
    app.include_router(reports.router)
    app.include_router(cleanups.router)
    app.include_router(education.router)
    app.include_router(leaderboard.router)
    app.include_router(tiles.router)
    app.include_router(admin.router)

    @app.exception_handler(ValueError)
    async def value_error_handler(_request, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    return app


app = create_app()
