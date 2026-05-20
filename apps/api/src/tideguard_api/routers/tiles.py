"""Map tile endpoint — serves a PNG heatmap tile for a given z/x/y."""

from __future__ import annotations

import io
import math

from fastapi import APIRouter, Response

router = APIRouter(prefix="/tiles", tags=["tiles"])


def _tile_to_lonlat(z: int, x: int, y: int) -> tuple[float, float, float, float]:
    n = 2.0**z
    lon_min = x / n * 360.0 - 180.0
    lon_max = (x + 1) / n * 360.0 - 180.0
    lat_max = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    lat_min = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n))))
    return lon_min, lat_min, lon_max, lat_max


def _generate_png_tile(z: int, x: int, y: int, day: int = 0) -> bytes:
    """Generate a synthetic PNG heatmap tile (256x256)."""
    try:
        from PIL import Image
    except ImportError:
        # Minimal 1x1 transparent PNG fallback
        return bytes.fromhex(
            "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4890000000D49444154789C636000000200010002B9F5180100000049454E44AE426082"
        )

    lon_min, lat_min, lon_max, lat_max = _tile_to_lonlat(z, x, y)
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    pixels = img.load()

    center_lon = 120.5 + 0.06 * day
    center_lat = 23.7 + 0.04 * day
    sigma = 0.5 + 0.05 * day

    for i in range(64):
        for j in range(64):
            lon = lon_min + (lon_max - lon_min) * (i / 64)
            lat = lat_min + (lat_max - lat_min) * (1 - j / 64)
            d2 = (lon - center_lon) ** 2 + (lat - center_lat) ** 2
            v = math.exp(-d2 / (2 * sigma**2))
            if v < 0.05:
                continue
            r = int(255 * min(1, v * 2))
            g = int(200 * (1 - v))
            b = int(140 * (1 - v) + 80)
            a = int(220 * v)
            pixels[i, j] = (r, g, b, a)

    img = img.resize((256, 256), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@router.get("/{z}/{x}/{y}.png")
def get_tile(z: int, x: int, y: int, day: int = 0) -> Response:
    png = _generate_png_tile(z, x, y, day=day)
    return Response(content=png, media_type="image/png", headers={"Cache-Control": "public, max-age=3600"})
