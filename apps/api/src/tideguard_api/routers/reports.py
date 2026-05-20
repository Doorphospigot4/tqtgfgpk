"""Citizen reports endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tideguard_api.db import get_db
from tideguard_api.deps import get_current_user, require_admin
from tideguard_api.models.report import Report
from tideguard_api.models.user import User
from tideguard_api.services.storage import upload_photo

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("")
async def create_report(
    photo: UploadFile = File(...),
    lat: float = Form(...),
    lng: float = Form(...),
    severity: int = Form(...),
    debris_type: str = Form("plastic_bottle"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise HTTPException(400, "Invalid coordinates")
    if not (1 <= severity <= 5):
        raise HTTPException(400, "severity must be 1..5")

    photo_url = await upload_photo(photo, user.id)
    report = Report(
        id=uuid.uuid4(),
        user_id=user.id,
        lat=lat,
        lng=lng,
        photo_url=photo_url,
        severity=severity,
        debris_type=debris_type,
    )
    db.add(report)
    user.xp = (user.xp or 0) + 10
    await db.commit()
    await db.refresh(report)
    return {"id": str(report.id), "photo_url": photo_url, "xp": user.xp}


@router.get("")
async def list_reports(
    bbox: str = Query(..., description="lon_min,lat_min,lon_max,lat_max"),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    try:
        lon_min, lat_min, lon_max, lat_max = map(float, bbox.split(","))
    except Exception as exc:
        raise HTTPException(400, f"Invalid bbox: {exc}") from exc

    stmt = (
        select(Report)
        .where(
            Report.status == "approved",
            Report.lng >= lon_min,
            Report.lng <= lon_max,
            Report.lat >= lat_min,
            Report.lat <= lat_max,
        )
        .limit(1000)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "lat": r.lat,
            "lng": r.lng,
            "photo_url": r.photo_url,
            "severity": r.severity,
            "debris_type": r.debris_type,
        }
        for r in rows
    ]


@router.patch("/{report_id}")
async def update_report(
    report_id: uuid.UUID,
    status: str,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict:
    if status not in ("pending", "approved", "rejected"):
        raise HTTPException(400, "Invalid status")
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    report.status = status
    await db.commit()
    return {"id": str(report.id), "status": report.status}
