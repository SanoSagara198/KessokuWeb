from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


def _get_secrets() -> dict[str, str]:
    """Retrieve secrets safely from st.secrets or local secrets.toml."""
    out: dict[str, str] = {}
    try:
        # Check Streamlit runtime secrets first
        for key in (
            "roblox_open_cloud_api_key",
            "roblox_universe_id",
            "roblox_client_id",
            "roblox_client_secret",
            "roblox_redirect_uri",
        ):
            if key in st.secrets:
                out[key] = str(st.secrets[key])
    except Exception:
        pass

    # Fallback to local secrets.toml if present
    secrets_file = ROOT / ".streamlit" / "secrets.toml"
    if secrets_file.is_file():
        for line in secrets_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k not in out:
                    out[k] = v
    return out


@st.cache_data(ttl=300, show_spinner=False)
def fetch_weapon_catalog() -> dict[str, Any]:
    """Fetch live authored weapon configs from Open Cloud with TTL caching."""
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    universe_id = sec.get("roblox_universe_id", "4046514670")

    if not api_key:
        return {}

    url = (
        f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/"
        f"standard-datastores/datastore/entries/entry"
        f"?datastoreName=AuthoredWeaponConfigOverridesV1&entryKey=global"
    )
    req = urllib.request.Request(url, headers={"x-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_operator_catalog() -> dict[str, Any]:
    """Fetch live authored operator catalog from Open Cloud with TTL caching."""
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    universe_id = sec.get("roblox_universe_id", "4046514670")

    if not api_key:
        return {}

    url = (
        f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/"
        f"standard-datastores/datastore/entries/entry"
        f"?datastoreName=AuthoredOperatorCatalogV1&entryKey=global"
    )
    req = urllib.request.Request(url, headers={"x-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


@st.cache_data(ttl=60, show_spinner=False)
def fetch_player_profile(user_id: str | int) -> dict[str, Any]:
    """Fetch live player profile from PlayerDataStore for the given user ID."""
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    universe_id = sec.get("roblox_universe_id", "4046514670")

    if not api_key or not user_id:
        return {}

    url = (
        f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/"
        f"standard-datastores/datastore/entries/entry"
        f"?datastoreName=PlayerDataStore&entryKey={user_id}"
    )
    req = urllib.request.Request(url, headers={"x-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}
