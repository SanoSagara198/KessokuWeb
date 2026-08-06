from __future__ import annotations

import ast
import base64
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_MEDIA_BYTES = int(1.5 * 1024 * 1024)


def fail(message: str) -> None:
    raise RuntimeError(message)


def validate_python() -> int:
    checked = 0
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")
        checked += 1
    return checked


def validate_source_policy() -> None:
    forbidden = {
        "use_container_width": "deprecated Streamlit width argument",
        "streamlit-option-menu": "removed navigation dependency",
    }
    searchable = [
        *ROOT.rglob("*.py"),
        *ROOT.rglob("*.md"),
        ROOT / "requirements.txt",
    ]
    for path in searchable:
        if not path.is_file() or path.name == "validate_site.py":
            continue
        text = path.read_text(encoding="utf-8")
        for token, reason in forbidden.items():
            if token in text:
                fail(f"{reason} remains in {path.relative_to(ROOT)}: {token}")


def validate_manifest() -> tuple[dict[str, object], ...]:
    path = ROOT / "assets" / "media" / "manifest.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    slots = tuple(payload.get("slots", ()))
    if not slots:
        fail("Media manifest has no slots")

    ids: set[str] = set()
    filenames: set[str] = set()
    for slot in slots:
        slot_id = str(slot.get("id", "")).strip()
        filename = str(slot.get("filename", "")).strip()
        if not slot_id or not filename:
            fail("Every media slot needs a non-empty id and filename")
        if slot_id in ids:
            fail(f"Duplicate media slot id: {slot_id}")
        if filename in filenames:
            fail(f"Duplicate media filename: {filename}")
        if not filename.endswith(".webp"):
            fail(f"Media slot is not WebP: {filename}")
        ids.add(slot_id)
        filenames.add(filename)
    return slots


def decode_media(filename: str) -> bytes | None:
    root = ROOT / "assets" / "media"
    binary = root / filename
    if binary.is_file():
        return binary.read_bytes()

    encoded = root / f"{filename}.b64"
    if encoded.is_file():
        try:
            return base64.b64decode("".join(encoded.read_text(encoding="ascii").split()), validate=True)
        except ValueError as exc:
            fail(f"Invalid Base64 media payload {encoded.name}: {exc}")

    parts = sorted(root.glob(f"{filename}.b64.part[0-9][0-9]"))
    if parts:
        joined = "".join(part.read_text(encoding="ascii") for part in parts)
        try:
            return base64.b64decode("".join(joined.split()), validate=True)
        except ValueError as exc:
            fail(f"Invalid Base64 media parts for {filename}: {exc}")
    return None


def validate_media(slots: tuple[dict[str, object], ...]) -> tuple[int, int]:
    present = 0
    missing = 0
    for slot in slots:
        filename = str(slot["filename"])
        payload = decode_media(filename)
        if payload is None:
            missing += 1
            continue
        if len(payload) > MAX_MEDIA_BYTES:
            fail(f"Media exceeds 1.5 MB budget: {filename} ({len(payload)} bytes)")
        if len(payload) < 16 or payload[:4] != b"RIFF" or payload[8:12] != b"WEBP":
            fail(f"Media is not a valid WebP container: {filename}")
        present += 1
    return present, missing


def validate_required_files() -> None:
    required = (
        "app.py",
        "requirements.txt",
        ".streamlit/config.toml",
        "kessoku_site/components.py",
        "kessoku_site/editorial.py",
        "kessoku_site/media.py",
        "kessoku_site/navigation.py",
        "assets/media/manifest.json",
        "docs/KESSOKU_WEBSITE_V2_3_EDITORIAL.md",
    )
    for relative in required:
        if not (ROOT / relative).is_file():
            fail(f"Missing required file: {relative}")


def main() -> int:
    validate_required_files()
    python_files = validate_python()
    validate_source_policy()
    slots = validate_manifest()
    present, missing = validate_media(slots)
    print(
        "Kessoku validation passed: "
        f"{python_files} Python files, {len(slots)} media slots, "
        f"{present} media assets present, {missing} using fallback."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
