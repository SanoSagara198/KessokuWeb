from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import streamlit as st

from kessoku_site.roblox_api import _get_secrets


def get_oauth_config() -> dict[str, str]:
    """Retrieve OAuth 2.0 client config."""
    sec = _get_secrets()
    return {
        "client_id": sec.get("roblox_client_id", "4804387660956036838"),
        "client_secret": sec.get("roblox_client_secret", ""),
        "redirect_uri": sec.get("roblox_redirect_uri", "http://localhost:8501/"),
    }


def get_roblox_auth_url(redirect_uri: str | None = None) -> str:
    """Generate the Roblox OAuth 2.0 authorization URL."""
    cfg = get_oauth_config()
    target_redirect = redirect_uri or cfg["redirect_uri"]
    params = {
        "client_id": cfg["client_id"],
        "response_type": "code",
        "redirect_uri": target_redirect,
        "scope": "openid profile",
        "state": "kessoku_auth_state",
    }
    return f"https://apis.roblox.com/oauth/v1/authorize?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(code: str, redirect_uri: str | None = None) -> dict[str, Any] | None:
    """Exchange authorization code for an OAuth 2.0 access token."""
    cfg = get_oauth_config()
    target_redirect = redirect_uri or cfg["redirect_uri"]
    token_url = "https://apis.roblox.com/oauth/v1/token"

    payload = {
        "client_id": cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": target_redirect,
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        token_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        st.session_state["auth_error"] = str(e)
        return None


def fetch_roblox_userinfo(access_token: str) -> dict[str, Any] | None:
    """Fetch authenticated Roblox user details from userinfo endpoint."""
    userinfo_url = "https://apis.roblox.com/oauth/v1/userinfo"
    req = urllib.request.Request(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


@st.cache_data(ttl=600, show_spinner=False)
def fetch_avatar_headshot(user_id: str | int) -> str | None:
    """Fetch public avatar circular headshot URL from Roblox Thumbnails API."""
    url = (
        f"https://thumbnails.roblox.com/v1/users/avatar-headshot"
        f"?userIds={user_id}&size=150x150&format=Png&isCircular=true"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("data", [])
            if items and items[0].get("state") == "Completed":
                return items[0].get("imageUrl")
    except Exception:
        pass
    return None


def handle_oauth_flow() -> None:
    """Inspect query parameters and handle OAuth 2.0 callback."""
    if "roblox_user" not in st.session_state:
        st.session_state["roblox_user"] = None

    # Check for OAuth callback code in query parameters
    code = st.query_params.get("code")
    if code:
        token_resp = exchange_code_for_token(code)
        if token_resp and "access_token" in token_resp:
            info = fetch_roblox_userinfo(token_resp["access_token"])
            if info:
                user_id = str(info.get("sub", ""))
                avatar_url = fetch_avatar_headshot(user_id) or info.get("picture")
                st.session_state["roblox_user"] = {
                    "user_id": user_id,
                    "username": info.get("preferred_username", "Robloxian"),
                    "display_name": info.get("name", "Robloxian"),
                    "avatar_url": avatar_url,
                    "is_demo": False,
                }
        # Clear code from URL
        if "code" in st.query_params:
            del st.query_params["code"]
        if "state" in st.query_params:
            del st.query_params["state"]
        st.rerun()


def login_as_demo() -> None:
    """Sign in as verified developer demo account (User 2725352577)."""
    user_id = "2725352577"
    avatar = fetch_avatar_headshot(user_id)
    st.session_state["roblox_user"] = {
        "user_id": user_id,
        "username": "KessokuDev",
        "display_name": "Kessoku Lead",
        "avatar_url": avatar,
        "is_demo": True,
    }
    st.rerun()


def logout_user() -> None:
    """Clear user session."""
    st.session_state["roblox_user"] = None
    st.rerun()
