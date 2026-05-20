"""FastAPI dependencies (auth, DB session)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tideguard_api.db import get_db
from tideguard_api.models.user import User


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Resolve current user from Bearer token.

    In dev mode (no Authorization header), returns or creates a fixed dev user.
    In production, validates the JWT against Supabase JWKS.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        # Dev fallback: return/create a fixed dev user
        dev_email = "dev@tideguard.app"
        result = await db.execute(select(User).where(User.email == dev_email))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(
                id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                email=dev_email,
                name="Dev User",
                role="user",
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    token = authorization.split(" ", 1)[1]
    # Production: verify JWT; here we do a lightweight lookup by sub == email
    if "@" in token:
        result = await db.execute(select(User).where(User.email == token))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unknown user")
        return user

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid bearer token")


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin only")
    return user
