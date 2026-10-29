from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ASSET_ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'maps'


@st.cache_data(show_spinner=False)
def atlas_html() -> str:
    template = (ASSET_ROOT / 'atlas.html').read_text(encoding='utf-8')
    return template.replace('<!-- CITY_GEOMETRY -->', (ASSET_ROOT / 'newcity.svg').read_text(encoding='utf-8'))


def render_city_atlas() -> None:
    components.html(atlas_html(), height=760, scrolling=False)
    st.caption('Geometry snapshot · 28 October 2026 · Mesh surfaces shown as projected bounds. Planning overlays are optional; this atlas is not live gameplay or a collision certification.')
