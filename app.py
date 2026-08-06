from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

from kessoku_site.components import action_button, feature_grid, footer, game_card, hero, mode_panel, roadmap, section, topbar
from kessoku_site.content import ALIGNMENTS, HEIST_CITY, STUDIO_PRINCIPLES, SUPER_MODES, SUPER_SOLDIERS
from kessoku_site.theme import CSS
from kessoku_site.visuals import city_pursuit_figure, metric_radar, procedural_poster, roadmap_chart


ROOT = Path(__file__).parent

st.set_page_config(
    page_title="Kessoku Games",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Kessoku Games — systemic Roblox worlds."},
)

st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_lottie() -> dict:
    with (ROOT / "assets" / "signal.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


@st.cache_data(show_spinner=False)
def poster(accent_rgb: tuple[int, int, int], seed: int) -> bytes:
    return procedural_poster(accent_rgb, seed)


def route_from_query() -> str:
    route = st.query_params.get("view", "Home")
    valid = {"Home", "Super Soldiers", "Heist City", "Studio"}
    return route if route in valid else "Home"


def set_route(route: str) -> None:
    st.query_params["view"] = route
    st.rerun()


def navigation() -> str:
    default = route_from_query()
    options = ["Home", "Super Soldiers", "Heist City", "Studio"]
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=["house", "crosshair", "buildings", "diamond"],
        default_index=options.index(default),
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "margin-bottom": "1rem"},
            "icon": {"color": "#AEB4BC", "font-size": "14px"},
            "nav-link": {
                "font-size": "12px", "font-weight": "800", "letter-spacing": ".06em",
                "text-align": "center", "margin": "0 3px", "padding": "11px 13px",
                "border": "1px solid rgba(255,255,255,.10)", "border-radius": "999px",
                "background": "rgba(255,255,255,.025)", "color": "#D9DCE1",
            },
            "nav-link-selected": {"background": "#F3F1EA", "color": "#090A0C", "border": "1px solid #F3F1EA"},
        },
        key=f"main-nav-{default}",
    )
    if selected != default:
        st.query_params["view"] = selected
    return selected


def home() -> None:
    hero(
        "WORLDS WITH CONSEQUENCE.",
        "KESSOKU GAMES / ARGENTINA",
        "We build Roblox experiences where combat, vehicles, bots and the city obey the same rules. Two worlds. One engineering standard.",
        "#F4F2EB",
        "PORTFOLIO / 02<br>SIMULATION / AUTHORITATIVE<br>STATUS / BUILDING",
    )

    section(
        "Two worlds. One shared discipline.",
        "Super Soldiers compresses authority into immediate tactical combat. Heist City expands the same discipline across traffic, police, factions and an urban sandbox.",
        "PORTFOLIO / ACTIVE PROJECTS",
    )
    left, right = st.columns(2, gap="small")
    with left:
        game_card(SUPER_SOLDIERS, "01")
        if action_button("EXPLORE SUPER SOLDIERS", "home-ss", SUPER_SOLDIERS.accent):
            set_route("Super Soldiers")
    with right:
        game_card(HEIST_CITY, "02")
        if action_button("ENTER HEIST CITY", "home-hc", HEIST_CITY.accent):
            set_route("Heist City")

    section(
        "The world should remain coherent when players push against it.",
        "Security is not the marketing message. Consequence is. Server ownership is the mechanism that lets every chase, shot, collision and decision belong to one living world.",
        "STUDIO / MANIFESTO",
    )
    st.markdown(
        '<div class="k-manifesto" style="--accent:#76F3FF">SECURE ENOUGH TO TRUST.<br>FAST ENOUGH TO FEEL.<br><em>SYSTEMIC ENOUGH TO SURPRISE.</em></div>',
        unsafe_allow_html=True,
    )

    section(
        "Development signal.",
        "The site now exposes high-level development tracks without turning the studio homepage into an internal engineering dashboard.",
        "ROADMAP / PUBLIC VIEW",
    )
    st.altair_chart(roadmap_chart("#F4F2EB"), width="stretch")


def super_soldiers() -> None:
    hero(
        SUPER_SOLDIERS.title,
        SUPER_SOLDIERS.category,
        f"{SUPER_SOLDIERS.tagline} {SUPER_SOLDIERS.pitch}",
        SUPER_SOLDIERS.accent,
        "OPERATION / LIVE<br>COMBAT / SERVER-OWNED<br>PLATFORM / ROBLOX",
    )
    st.image(poster(SUPER_SOLDIERS.accent_rgb, 71), width="stretch")

    section(
        "Built as one combat system, not two disconnected modes.",
        "Arena and survival use the same authoritative rules for damage, movement, cooldowns, bots, score and match state.",
        "SUPER SOLDIERS / PILLARS",
    )
    feature_grid(SUPER_SOLDIERS)

    section(
        "Select the operation.",
        "Each mode changes tempo, objectives and pressure while preserving the same combat language.",
        "INTERACTIVE / MODE BRIEF",
    )
    labels = [mode.title for mode in SUPER_MODES]
    selected = st.segmented_control("Operation", labels, default=labels[0], label_visibility="collapsed") or labels[0]
    mode = next(item for item in SUPER_MODES if item.title == selected)
    panel, chart = st.columns([1.12, .88], gap="large")
    with panel:
        mode_panel(mode.strapline, mode.title, mode.description, mode.facts, SUPER_SOLDIERS.accent)
        st_lottie(load_lottie(), height=120, key=f"signal-{mode.key}", speed=.7)
    with chart:
        st.plotly_chart(metric_radar(mode.metrics, SUPER_SOLDIERS.accent), width="stretch", config={"displayModeBar": False})

    section(
        "Current development track.",
        "The public roadmap communicates sequence without exposing internal implementation detail or promising dates that are not yet fixed.",
        "SUPER SOLDIERS / ROADMAP",
    )
    roadmap(
        (
            ("01", "Server Authority Beta", "ACTIVE"),
            ("02", "Combat Readability", "ACTIVE"),
            ("03", "City of Zombies Depth", "NEXT"),
            ("04", "Public Playtests", "PLANNED"),
        ),
        SUPER_SOLDIERS.accent,
    )


def heist_city() -> None:
    hero(
        HEIST_CITY.title,
        HEIST_CITY.category,
        f"{HEIST_CITY.tagline} {HEIST_CITY.pitch}",
        HEIST_CITY.accent,
        "CITY / ONLINE<br>TRAFFIC / AUTHORITATIVE<br>ALIGNMENTS / 03",
    )
    st.image(poster(HEIST_CITY.accent_rgb, 1987), width="stretch")

    section(
        "A city that reacts instead of merely decorating the map.",
        "Traffic, police, civilians, missions and wanted pressure read the same world state and remain bounded under concurrency.",
        "HEIST CITY / PILLARS",
    )
    feature_grid(HEIST_CITY)

    section(
        "Choose where you stand.",
        "The simulation stays shared. Alignment changes the opportunities, information and pressure available to the player.",
        "INTERACTIVE / ALIGNMENT",
    )
    labels = [alignment.title for alignment in ALIGNMENTS]
    selected = st.segmented_control("Alignment", labels, default=labels[0], label_visibility="collapsed") or labels[0]
    alignment = next(item for item in ALIGNMENTS if item.title == selected)
    panel, chart = st.columns([1.08, .92], gap="large")
    with panel:
        mode_panel(alignment.code, alignment.title, f"{alignment.description} {alignment.objective}", ("Shared city", "Distinct intent", "Escalating consequence", "Server-owned response"), alignment.accent)
    with chart:
        st.plotly_chart(metric_radar(alignment.metrics, alignment.accent), width="stretch", config={"displayModeBar": False})

    section(
        "Pursuit intelligence, visualized.",
        "Move the scenario forward to see police units converge through independent routes rather than simply following the target's trail.",
        "HEIST CITY / CITY SIMULATION",
    )
    stage = st.slider("Pursuit progression", min_value=1, max_value=8, value=5, label_visibility="collapsed")
    st.plotly_chart(city_pursuit_figure(stage, alignment.accent), width="stretch", config={"displayModeBar": False})

    section(
        "Current development track.",
        "The city foundation comes before faction breadth: physical traffic, pursuit intelligence, mission loops, then city optimization and scale testing.",
        "HEIST CITY / ROADMAP",
    )
    roadmap(
        (
            ("01", "Physical Traffic Beta", "ACTIVE"),
            ("02", "Police Pursuit Intelligence", "ACTIVE"),
            ("03", "Mission and Faction Loop", "NEXT"),
            ("04", "City Optimization", "PLANNED"),
        ),
        HEIST_CITY.accent,
    )


def studio() -> None:
    hero(
        "KESSOKU",
        "INDEPENDENT ROBLOX STUDIO",
        "We make worlds that stay coherent under pressure. The server owns truth; the client renders state and sends intent.",
        "#F4F2EB",
        "SYSTEMS / SHARED<br>WORK / BOUNDED<br>SERVERS / AUTONOMOUS",
    )

    section(
        "A compact studio with an uncompromising architecture.",
        "Kessoku is organized around player-facing consequence and engineering discipline rather than marketing volume.",
        "STUDIO / OPERATING MODEL",
    )
    cols = st.columns(2, gap="small")
    for idx, (title, copy) in enumerate(STUDIO_PRINCIPLES):
        with cols[idx % 2]:
            st.markdown(
                f'<article class="k-feature" style="--accent:#F4F2EB;margin-bottom:1rem"><div class="k-feature-num">0{idx + 1} / PRINCIPLE</div><h3>{title}</h3><p>{copy}</p></article>',
                unsafe_allow_html=True,
            )

    section(
        "Technology used deliberately.",
        "The V2 site combines a validated content model, cached procedural media, interactive charts and custom presentation components while keeping the deployable surface understandable.",
        "WEBSITE / STACK",
    )
    stack = {
        "Presentation": ["Streamlit", "streamlit-option-menu", "streamlit-extras", "streamlit-lottie"],
        "Visual systems": ["Plotly", "Altair", "Pillow"],
        "Data and validation": ["Pandas", "NumPy", "Pydantic"],
        "Runtime": ["Python 3.12", "Streamlit Community Cloud", "GitHub"],
    }
    for category, items in stack.items():
        st.markdown(f"**{category}** — " + " · ".join(items))

    section(
        "Contact surfaces are intentionally pending.",
        "Official Roblox, Discord, YouTube, press and playtest destinations should be added only after their canonical URLs are confirmed.",
        "STUDIO / CONTACT",
    )
    st.info("No unofficial links or invented contact details are published.")


topbar()
view = navigation()

if view == "Home":
    home()
elif view == "Super Soldiers":
    super_soldiers()
elif view == "Heist City":
    heist_city()
else:
    studio()

footer()
