"""Admin endpoints — KPI dashboard data."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from tideguard_api.db import get_db
from tideguard_api.deps import require_admin
from tideguard_api.models.cleanup import Cleanup
from tideguard_api.models.lesson import LessonProgress
from tideguard_api.models.report import Report
from tideguard_api.models.school import School
from tideguard_api.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/kpi")
async def kpi(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict:
    """Return key impact + engagement metrics for the proposal/jury."""
    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
    total_reports = (await db.execute(select(func.count(Report.id)))).scalar() or 0
    approved_reports = (
        await db.execute(select(func.count(Report.id)).where(Report.status == "approved"))
    ).scalar() or 0
    total_cleanups = (await db.execute(select(func.count(Cleanup.id)))).scalar() or 0
    total_kg = (await db.execute(select(func.coalesce(func.sum(Cleanup.kg_collected), 0.0)))).scalar() or 0.0
    total_schools = (await db.execute(select(func.count(School.id)))).scalar() or 0
    lessons_completed = (await db.execute(select(func.count(LessonProgress.user_id)))).scalar() or 0

    return {
        "users": int(total_users),
        "reports_total": int(total_reports),
        "reports_approved": int(approved_reports),
        "cleanups": int(total_cleanups),
        "kg_collected": float(total_kg),
        "schools": int(total_schools),
        "lessons_completed": int(lessons_completed),
    }
