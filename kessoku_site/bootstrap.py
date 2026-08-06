from __future__ import annotations

from collections.abc import Callable
from typing import Any

import streamlit as st

from .polish import POLISH_CSS


_CORE_THEME_MARKER = "--bg:#060709"


def install_polish_bridge() -> None:
    """Inject the final polish layer immediately after the core theme.

    The application intentionally owns page configuration and the main theme.
    This bridge keeps that public entry point stable while ensuring the V2.2
    finishing stylesheet is applied after, rather than before, the core CSS.
    """

    if getattr(st, "_kessoku_polish_bridge_installed", False):
        return

    original_markdown: Callable[..., Any] = st.markdown

    def polished_markdown(body: Any, *args: Any, **kwargs: Any) -> Any:
        result = original_markdown(body, *args, **kwargs)
        if (
            isinstance(body, str)
            and _CORE_THEME_MARKER in body
            and not getattr(st, "_kessoku_polish_injected", False)
        ):
            original_markdown(POLISH_CSS, unsafe_allow_html=True)
            st._kessoku_polish_injected = True
        return result

    st.markdown = polished_markdown  # type: ignore[assignment]
    st._kessoku_polish_bridge_installed = True
