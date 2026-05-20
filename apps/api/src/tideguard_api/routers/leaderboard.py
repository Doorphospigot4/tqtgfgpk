"""Leaderboard endpoint — top users by XP."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tideguard_api.db import get_db
from tideguard_api.models.user import User

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("")
async def leaderboard(
    scope: str = Query("global", pattern="^(global|school|region)$"),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    stmt = select(User).order_by(User.xp.desc()).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return [
        {
            "rank": i + 1,
            "user_id": str(u.id),
            "name": u.name or u.email.split("@")[0],
            "xp": u.xp,
            "school_id": str(u.school_id) if u.school_id else None,
        }
        for i, u in enumerate(rows)
    ]
