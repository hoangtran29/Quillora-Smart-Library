"""Visualize: excerpt -> image prompt -> Gemini / fal.ai / stub."""
from __future__ import annotations

import base64
import json
import logging
import time
import uuid
from pathlib import Path

import httpx
from fastapi import APIRouter, Request
from pydantic import BaseModel

from app import llm
from app.config import settings
from app.routers.auth import current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/visualize", tags=["visualize"])

GENERATED_DIR = settings.DATA_DIR / "generated"
VIZ_FILE = settings.DATA_DIR / "visualizations.json"


def _load_viz() -> list[dict]:
    if not VIZ_FILE.exists():
        return []
    with VIZ_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_viz(items: list[dict]) -> None:
    with VIZ_FILE.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def _persist_image(image_url: str, viz_id: str) -> str:
    """Save base64 data-URL or remote URL image to disk, return serving path."""
    if image_url.startswith("data:"):
        # data:<mime>;base64,<data>
        header, b64data = image_url.split(",", 1)
        ext = "png"
        if "svg" in header:
            ext = "svg"
        elif "jpeg" in header or "jpg" in header:
            ext = "jpg"
        filename = f"{viz_id}.{ext}"
        filepath = GENERATED_DIR / filename
        filepath.write_bytes(base64.b64decode(b64data))
        return f"/static/generated/{filename}"
    # Remote URL (e.g. fal.ai) — keep as-is
    return image_url


class VisualizeBody(BaseModel):
    excerpt: str
    book_id: int | None = None


GEMINI_IMAGE_MODELS = [
    "gemini-2.5-flash-image",
    "gemini-2.0-flash-preview-image-generation",
    "gemini-2.0-flash-exp-image-generation",
]


def _call_gemini_image(prompt: str) -> str | None:
    """Use Gemini's native image generation model to turn a prompt into a PNG.
    Tries several model aliases since Google rotates them frequently."""
    if not settings.GEMINI_API_KEY:
        return None
    try:
        from google import genai
        from google.genai import types
    except Exception as e:
        logger.warning("google.genai import failed: %s", e)
        return None

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    for model in GEMINI_IMAGE_MODELS:
        try:
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )
            for cand in resp.candidates or []:
                parts = getattr(cand.content, "parts", None) or []
                for part in parts:
                    inline = getattr(part, "inline_data", None)
                    if inline and getattr(inline, "data", None):
                        data = inline.data
                        b64 = data if isinstance(data, str) else base64.b64encode(data).decode("ascii")
                        mime = getattr(inline, "mime_type", None) or "image/png"
                        logger.info("Gemini image gen OK via %s", model)
                        return f"data:{mime};base64,{b64}"
            logger.info("Gemini image gen via %s returned no inline image part", model)
        except Exception as e:
            msg = str(e)
            # 404 = model not available in free tier → try next alias silently
            if "404" not in msg and "NOT_FOUND" not in msg:
                logger.warning("Gemini image gen failed via %s: %s", model, msg[:200])
    return None


FAL_MODELS = [
    # text-to-image, fast
    "fal-ai/fast-sdxl",
    "fal-ai/fast-lightning-sdxl",
    "fal-ai/fast-lcm-diffusion",
]


async def _call_fal(prompt: str) -> str | None:
    if not settings.FAL_API_KEY:
        return None
    headers = {
        "Authorization": f"Key {settings.FAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "image_size": "square_hd",
        "num_images": 1,
        "enable_safety_checker": False,
    }
    async with httpx.AsyncClient(timeout=90.0) as client:
        for model in FAL_MODELS:
            url = f"https://fal.run/{model}"
            try:
                r = await client.post(url, headers=headers, json=payload)
                if r.status_code >= 400:
                    logger.warning(
                        "fal.ai %s HTTP %s: %s", model, r.status_code, r.text[:250]
                    )
                    continue
                data = r.json()
                images = data.get("images") or []
                if images and images[0].get("url"):
                    logger.info("fal.ai OK via %s", model)
                    return images[0]["url"]
                logger.warning("fal.ai %s returned no images: %s", model, str(data)[:250])
            except Exception as e:
                logger.warning("fal.ai %s call failed: %r", model, e)
    return None


def _stub_svg_data_url(prompt: str) -> str:
    """Return a tasteful SVG data URL so the UI always has something to render."""
    import base64

    safe = prompt.replace("&", "&amp;").replace("<", "&lt;")[:120]
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>
  <defs>
    <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
      <stop offset='0%' stop-color='#FFF8E7'/>
      <stop offset='50%' stop-color='#E8F4FD'/>
      <stop offset='100%' stop-color='#FCE4EC'/>
    </linearGradient>
  </defs>
  <rect width='600' height='600' fill='url(#g)'/>
  <g opacity='0.7'>
    <circle cx='200' cy='220' r='80' fill='#FFCC80'/>
    <circle cx='400' cy='180' r='60' fill='#90CAF9'/>
    <circle cx='300' cy='350' r='100' fill='#CE93D8'/>
    <circle cx='150' cy='400' r='50' fill='#A5D6A7'/>
    <circle cx='450' cy='380' r='70' fill='#EF9A9A'/>
  </g>
  <text x='50%' y='540' text-anchor='middle' font-family='Georgia, serif'
        font-size='20' fill='#5D4037'>Quillora · minh hoạ tạm</text>
  <title>{safe}</title>
</svg>"""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


@router.get("/history")
async def list_visualizations(request: Request):
    """Return visualizations for the current user (newest first).
    Unauthenticated users see only anonymous (no user_id) entries."""
    user = current_user(request)
    user_id = user.get("sub") if user else None
    all_items = _load_viz()
    if user_id:
        filtered = [v for v in all_items if v.get("user_id") == user_id]
    else:
        filtered = [v for v in all_items if not v.get("user_id")]
    return filtered[::-1]


@router.post("")
async def visualize(body: VisualizeBody, request: Request):
    prompt = llm.excerpt_to_image_prompt(body.excerpt)

    # 1. Prefer fal.ai (saves Gemini quota for chat/LLM)
    image_url = await _call_fal(prompt)
    source = "fal"

    # 2. Fall back to Gemini image generation
    if image_url is None:
        image_url = _call_gemini_image(prompt)
        if image_url is not None:
            source = "gemini"

    # 3. Final fallback: an editorial SVG placeholder
    used_stub = image_url is None
    if used_stub:
        image_url = _stub_svg_data_url(prompt)
        source = "stub"

    viz_id = str(uuid.uuid4())

    # Persist image to disk and get a stable serving URL
    saved_url = _persist_image(image_url, viz_id)

    user = current_user(request)
    user_id = user.get("sub") if user else None

    record = {
        "id": viz_id,
        "prompt": prompt,
        "excerpt": body.excerpt[:500],
        "image_url": saved_url,
        "source": source,
        "stub": used_stub,
        "book_id": body.book_id,
        "user_id": user_id,
        "created_at": int(time.time()),
    }

    items = _load_viz()
    items.append(record)
    _save_viz(items)

    return record
