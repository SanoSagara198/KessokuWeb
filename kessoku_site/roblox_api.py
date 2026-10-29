from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "kessoku_site" / "data"


def _get_secrets() -> dict[str, str]:
    """Retrieve secrets safely from st.secrets, local secrets.toml, or environment."""
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


def _load_local_json(filename: str) -> dict[str, Any] | None:
    """Load cached local verified snapshot JSON from data directory."""
    path = DATA_DIR / filename
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


@st.cache_data(ttl=300, show_spinner=False)
def fetch_weapon_catalog() -> tuple[dict[str, Any], str]:
    """Fetch live authored weapon configs from Open Cloud with local snapshot fallback.
    Returns: (data_dict, source_type) where source_type is 'live' or 'snapshot'.
    """
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    universe_id = sec.get("roblox_universe_id", "4046514670")

    if api_key:
        url = (
            f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/"
            f"standard-datastores/datastore/entries/entry"
            f"?datastoreName=AuthoredWeaponConfigOverridesV1&entryKey=global"
        )
        req = urllib.request.Request(url, headers={"x-api-key": api_key})
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, dict) and data:
                    return data, "live"
        except Exception:
            pass

    # Seamless fallback to verified local snapshot
    cached = _load_local_json("weapons_catalog.json")
    if cached:
        return cached, "snapshot"
    return {}, "none"


@st.cache_data(ttl=300, show_spinner=False)
def fetch_operator_catalog() -> tuple[dict[str, Any], str]:
    """Fetch live authored operator catalog from Open Cloud with local snapshot fallback.
    Returns: (data_dict, source_type) where source_type is 'live' or 'snapshot'.
    """
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    universe_id = sec.get("roblox_universe_id", "4046514670")

    if api_key:
        url = (
            f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/"
            f"standard-datastores/datastore/entries/entry"
            f"?datastoreName=AuthoredOperatorCatalogV1&entryKey=global"
        )
        req = urllib.request.Request(url, headers={"x-api-key": api_key})
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, dict) and data:
                    return data, "live"
        except Exception:
            pass

    cached = _load_local_json("operators_catalog.json")
    if cached:
        return cached, "snapshot"
    return {}, "none"


@st.cache_data(ttl=60, show_spinner=False)
def fetch_player_profile(user_id: str | int) -> tuple[dict[str, Any], str]:
    """Fetch live player profile from PlayerDataStore with local verified snapshot fallback.
    Returns: (profile_dict, source_type) where source_type is 'live', 'snapshot', or 'none'.
    """
    uid_str = str(user_id).strip()
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    universe_id = sec.get("roblox_universe_id", "4046514670")

    if api_key and uid_str:
        url = (
            f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/"
            f"standard-datastores/datastore/entries/entry"
            f"?datastoreName=PlayerDataStore&entryKey={uid_str}"
        )
        req = urllib.request.Request(url, headers={"x-api-key": api_key})
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, dict) and data:
                    return data, "live"
        except Exception:
            pass

    # Seamless fallback to verified player snapshot (e.g. 2725352577)
    cached = _load_local_json(f"player_{uid_str}.json")
    if cached:
        return cached, "snapshot"

    # Default fallback for testing if 2725352577 snapshot exists
    default_cached = _load_local_json("player_2725352577.json")
    if default_cached and (uid_str in {"2725352577", "demo", "0"} or not uid_str):
        return default_cached, "snapshot"

    return {}, "none"


@st.cache_data(ttl=60, show_spinner=False)
def fetch_heist_player_profile(user_id: str | int) -> tuple[dict[str, Any], str]:
    """Fetch live Heist City player profile from PlayerProgress_v1 with verified snapshot fallback.
    Returns: (profile_dict, source_type) where source_type is 'live', 'snapshot', or 'none'.
    """
    uid_str = str(user_id).strip()
    sec = _get_secrets()
    api_key = sec.get("roblox_open_cloud_api_key")
    heist_universe_id = sec.get("roblox_heist_universe_id", "10772507321")

    if api_key and uid_str:
        url = (
            f"https://apis.roblox.com/datastores/v1/universes/{heist_universe_id}/"
            f"standard-datastores/datastore/entries/entry"
            f"?datastoreName=PlayerProgress_v1&entryKey=u{uid_str}"
        )
        req = urllib.request.Request(url, headers={"x-api-key": api_key})
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, dict) and data:
                    return data, "live"
        except Exception:
            pass

    cached = _load_local_json(f"heist_player_{uid_str}.json")
    if cached:
        return cached, "snapshot"

    default_cached = _load_local_json("heist_player_2725352577.json")
    if default_cached and (uid_str in {"2725352577", "demo", "0"} or not uid_str):
        return default_cached, "snapshot"

    return {}, "none"
