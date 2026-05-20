"""Cleanups endpoints — events with collected mass + photos."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from tideguard_api.db import get_db
from tideguard_api.deps import get_current_user
from tideguard_api.models.cleanup import Cleanup
from tideguard_api.models.user import User

router = APIRouter(prefix="/cleanups", tags=["cleanups"])


class CleanupCreate(BaseModel):
    geom_wkt: str = Field(..., description="POLYGON WKT, EPSG:4326")
    kg_collected: float = Field(..., ge=0)
    participants: int = Field(..., ge=1)
    before_photo: str | None = None
    after_photo: str | None = None


@router.post("")
async def create_cleanup(
    payload: CleanupCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    if not payload.geom_wkt.upper().startswith("POLYGON"):
        raise HTTPException(400, "geom_wkt must be a POLYGON")
    cleanup = Cleanup(
        id=uuid.uuid4(),
        user_id=user.id,
        geom_wkt=payload.geom_wkt,
        kg_collected=payload.kg_collected,
        participants=payload.participants,
        before_photo=payload.before_photo,
        after_photo=payload.after_photo,
    )
    db.add(cleanup)
    user.xp = (user.xp or 0) + 100
    await db.commit()
    await db.refresh(cleanup)
    return {"id": str(cleanup.id), "xp": user.xp}


@router.get("/stats")
async def cleanup_stats(db: AsyncSession = Depends(get_db)) -> dict:
    """Aggregate KPIs for the landing page."""
    total_kg = (await db.execute(select(func.coalesce(func.sum(Cleanup.kg_collected), 0.0)))).scalar() or 0.0
    total_participants = (await db.execute(select(func.coalesce(func.sum(Cleanup.participants), 0)))).scalar() or 0
    total_events = (await db.execute(select(func.count(Cleanup.id)))).scalar() or 0
    return {
        "kg_collected": float(total_kg),
        "participants": int(total_participants),
        "events": int(total_events),
    }
