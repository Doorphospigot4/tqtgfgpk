"""Auth endpoints (Supabase delegation in prod, simple dev fallback otherwise)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from tideguard_api.deps import get_current_user
from tideguard_api.models.user import User

router = APIRouter(tags=["auth"])


@router.get("/me")
async def me(user: User = Depends(get_current_user)) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "xp": user.xp,
        "school_id": str(user.school_id) if user.school_id else None,
    }
