"""Photo upload service (S3-compatible storage)."""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import UploadFile

from tideguard_api.settings import get_settings

_settings = get_settings()


async def upload_photo(photo: UploadFile, user_id: uuid.UUID) -> str:
    """Upload a photo to S3/R2 (or local dir in dev) and return its public URL."""
    suffix = Path(photo.filename or "image.jpg").suffix or ".jpg"
    object_key = f"reports/{user_id}/{uuid.uuid4().hex}{suffix}"

    if _settings.s3_endpoint and _settings.s3_access_key:
        import boto3

        client = boto3.client(
            "s3",
            endpoint_url=_settings.s3_endpoint,
            aws_access_key_id=_settings.s3_access_key,
            aws_secret_access_key=_settings.s3_secret_key,
        )
        body = await photo.read()
        client.put_object(
            Bucket=_settings.s3_bucket_photos,
            Key=object_key,
            Body=body,
            ContentType=photo.content_type or "image/jpeg",
        )
        return f"{_settings.s3_endpoint}/{_settings.s3_bucket_photos}/{object_key}"

    # Dev fallback: save to local uploads dir
    local_dir = Path("uploads") / "photos"
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / object_key.replace("/", "_")
    body = await photo.read()
    local_path.write_bytes(body)
    return f"/uploads/photos/{local_path.name}"
