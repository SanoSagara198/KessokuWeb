from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import streamlit as st


NAVIGATION_CSS = r"""
<style>
/* Native primary navigation. The widget key is exposed by Streamlit as a
   st-key-* class, which lets the navigation be styled without DOM mutation. */
[class*="st-key-main-nav-"] {
  position: sticky;
  top: 4.6rem;
  z-index: 49;
  padding: .5rem;
  margin: 0 0 1rem;
  border: 1px solid rgba(255,255,255,.11);
  border-radius: 18px;
  background: rgba(7,8,10,.84);
  -webkit-backdrop-filter: blur(24px) saturate(135%);
  backdrop-filter: blur(24px) saturate(135%);
  box-shadow: 0 16px 44px rgba(0,0,0,.25);
}

[class*="st-key-main-nav-"] [data-testid="stPills"] > div {
  display: flex;
  flex-wrap: wrap;
  gap: .42rem;
  width: 100%;
}

[class*="st-key-main-nav-"] [data-testid="stPills"] button {
  flex: 1 1 10.5rem;
  min-height: 2.65rem;
  justify-content: center;
  border: 1px solid rgba(255,255,255,.10) !important;
  border-radius: 12px !important;
  background: rgba(255,255,255,.025) !important;
  color: #cfd3d9 !important;
  font-size: .70rem !important;
  font-weight: 850 !important;
  letter-spacing: .075em !important;
  transition: transform .16s ease, border-color .16s ease,
              background .16s ease, color .16s ease !important;
}

[class*="st-key-main-nav-"] [data-testid="stPills"] button:hover {
  transform: translateY(-1px);
  border-color: rgba(255,255,255,.36) !important;
  background: rgba(255,255,255,.075) !important;
  color: #fff !important;
}

[class*="st-key-main-nav-"] [data-testid="stPills"] button[aria-pressed="true"] {
  border-color: #f4f2eb !important;
  background: #f4f2eb !important;
  color: #07080a !important;
  box-shadow: 0 8px 24px rgba(0,0,0,.26);
}

[class*="st-key-main-nav-"] [data-testid="stPills"] button:focus-visible {
  outline: 2px solid #76f3ff !important;
  outline-offset: 2px !important;
}

@media (max-width: 760px) {
  .k-topline {
    position: relative !important;
    top: auto !important;
    border-radius: 18px !important;
  }

  [class*="st-key-main-nav-"] {
    position: relative;
    top: auto;
    padding: .42rem;
    border-radius: 16px;
  }

  [class*="st-key-main-nav-"] [data-testid="stPills"] button {
    flex-basis: calc(50% - .25rem);
    min-width: 0;
    font-size: .64rem !important;
    letter-spacing: .045em !important;
  }
}

@media (max-width: 420px) {
  [class*="st-key-main-nav-"] [data-testid="stPills"] button {
    flex-basis: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  [class*="st-key-main-nav-"] [data-testid="stPills"] button {
    transition: none !important;
  }
}
</style>
"""


def option_menu(
    menu_title: str | None,
    options: Sequence[str],
    icons: Sequence[str] | None = None,
    menu_icon: str | None = None,
    default_index: int = 0,
    orientation: str = "vertical",
    styles: dict[str, Any] | None = None,
    key: str | None = None,
    **_: Any,
) -> str:
    """Render Kessoku's primary navigation with Streamlit's native pills.

    This intentionally accepts the former streamlit-option-menu call shape so
    the site can migrate without coupling its route logic to a third-party
    frontend component. Decorative icon/style arguments are ignored; visual
    behavior is owned by the Kessoku design system above.
    """

    del icons, menu_icon, orientation, styles

    if not options:
        raise ValueError("Primary navigation requires at least one route.")
    if default_index < 0 or default_index >= len(options):
        raise ValueError("default_index is outside the navigation options.")

    st.markdown(NAVIGATION_CSS, unsafe_allow_html=True)
    default = options[default_index]
    selection = st.pills(
        menu_title or "Primary navigation",
        options,
        selection_mode="single",
        default=default,
        key=key,
        label_visibility="collapsed" if menu_title is None else "visible",
        width="stretch",
    )
    return selection or default
