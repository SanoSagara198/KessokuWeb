from __future__ import annotations

import base64
import hashlib
from collections.abc import Callable
from pathlib import Path
from typing import Any

import streamlit as st


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MEDIA_ROOT = REPOSITORY_ROOT / "assets" / "media"

# The current application requests deterministic procedural posters through
# ``st.image``. Their hashes let the presentation layer substitute approved
# campaign media without coupling page code to filenames or removing the
# procedural fallback.
_PROCEDURAL_TO_MEDIA = {
    "8dff92b1fa0e46ff07531c00800905d425df22d0b8f060f030de579888bde3e5": (
        "super-soldiers-city-of-zombies.webp"
    ),
    "002ae6f5879b8d7ee27d0a967b60ee0498c03c1efc3e0574e4f850511d3c463d": (
        "heist-city-hero.webp"
    ),
}


def campaign_asset(filename: str) -> bytes | None:
    """Return campaign-media bytes when the repository contains the asset.

    Production uses normal binary WebP files. During connector-only publishing,
    the same bytes may be stored as one ``.b64`` file or deterministic numbered
    ``.b64.partNN`` files; those representations are decoded transparently.
    """

    binary_path = MEDIA_ROOT / filename
    if binary_path.is_file():
        return binary_path.read_bytes()

    encoded_path = MEDIA_ROOT / f"{filename}.b64"
    if encoded_path.is_file():
        return _decode_base64(encoded_path.read_text(encoding="ascii"))

    parts = sorted(MEDIA_ROOT.glob(f"{filename}.b64.part[0-9][0-9]"))
    if parts:
        encoded = "".join(part.read_text(encoding="ascii") for part in parts)
        return _decode_base64(encoded)

    return None


def suppress_next_campaign_image(filename: str) -> None:
    """Suppress one legacy ``st.image`` call after media becomes a background."""

    st._kessoku_suppress_next_campaign_image = filename


def install_media_bridge() -> None:
    """Make existing ``st.image`` calls prefer approved campaign media."""

    if getattr(st, "_kessoku_media_bridge_installed", False):
        return

    original_image: Callable[..., Any] = st.image

    def campaign_aware_image(image: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(image, (bytes, bytearray, memoryview)):
            raw = bytes(image)
            filename = _PROCEDURAL_TO_MEDIA.get(hashlib.sha256(raw).hexdigest())
            if filename:
                if getattr(st, "_kessoku_suppress_next_campaign_image", None) == filename:
                    delattr(st, "_kessoku_suppress_next_campaign_image")
                    return None
                replacement = campaign_asset(filename)
                if replacement:
                    image = replacement
        return original_image(image, *args, **kwargs)

    st.image = campaign_aware_image  # type: ignore[assignment]
    st._kessoku_media_bridge_installed = True


def _decode_base64(value: str) -> bytes | None:
    try:
        return base64.b64decode("".join(value.split()), validate=True)
    except (ValueError, base64.binascii.Error):
        return None
