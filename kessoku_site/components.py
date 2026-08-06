from __future__ import annotations

import base64
from html import escape

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from .campaign import CAMPAIGN_CSS
from .editorial import EDITORIAL_CSS
from .media import campaign_asset, suppress_next_campaign_image
from .models import DetailBlock, Game, StoryBeat
from .polish import POLISH_CSS


_HERO_MEDIA = {
    "WORLDS WITH CONSEQUENCE.": ("kessoku-home-dual-world-hero.webp", False),
    "SUPER SOLDIERS": ("super-soldiers-hero.webp", True),
    "HEIST CITY": ("heist-city-hero.webp", True),
    "KESSOKU": ("kessoku-studio-manifesto.webp", False),
}

_CARD_MEDIA = {
    "SUPER SOLDIERS": "super-soldiers-hero.webp",
    "HEIST CITY": "heist-city-hero.webp",
}

_PANEL_MEDIA = {
    "5V5 ARENA": "super-soldiers-arena-operation.webp",
    "CITY OF ZOMBIES": "super-soldiers-city-of-zombies.webp",
    "CRIMINAL": "heist-city-criminal.webp",
    "POLICE": "heist-city-police.webp",
    "VIGILANTE": "heist-city-vigilante.webp",
}

_HERO_METADATA: dict[str, tuple[tuple[str, str], ...]] = {
    "WORLDS WITH CONSEQUENCE.": (
        ("PORTFOLIO", "02 ACTIVE WORLDS"),
        ("DISCIPLINE", "SERVER-OWNED TRUTH"),
        ("STUDIO", "ARGENTINA"),
        ("STATE", "IN DEVELOPMENT"),
    ),
    "SUPER SOLDIERS": (
        ("FORMAT", "5V5 + COOPERATIVE PVE"),
        ("PRIMARY FEEL", "PRESSURE / PRECISION"),
        ("PLATFORM", "ROBLOX / MOBILE FIRST"),
        ("STATE", "AUTHORITY BETA"),
    ),
    "HEIST CITY": (
        ("FORMAT", "SYSTEMIC OPEN WORLD"),
        ("PRIMARY FEEL", "OPPORTUNITY / CONSEQUENCE"),
        ("WORLD", "SHARED CRIME + LAW"),
        ("STATE", "CITY SYSTEMS ALPHA"),
    ),
    "KESSOKU": (
        ("MODEL", "INDEPENDENT STUDIO"),
        ("SPECIALTY", "BOUNDED SIMULATION"),
        ("PRINCIPLE", "ONE WORLD / ONE TRUTH"),
        ("LOCATION", "ARGENTINA"),
    ),
}

_GAME_SIGNATURES: dict[str, tuple[tuple[str, str], ...]] = {
    "super-soldiers": (
        ("PLAYER ROLE", "Elite combatant inside a readable tactical team."),
        ("CORE RHYTHM", "Acquire space, commit, convert advantage, reset."),
        ("SYSTEM PROMISE", "Players and bots resolve through one combat truth."),
    ),
    "heist-city": (
        ("PLAYER ROLE", "Criminal, police officer, or vigilante in one city."),
        ("CORE RHYTHM", "Read the grid, create pressure, escape or contain."),
        ("SYSTEM PROMISE", "Traffic, evidence, pursuit, and missions remember."),
    ),
}


def _campaign_background(filename: str | None, *, position: str = "center") -> str:
    if not filename:
        return ""
    payload = campaign_asset(filename)
    if not payload:
        return ""
    encoded = base64.b64encode(payload).decode("ascii")
    return (
        "background-image:"
        "linear-gradient(90deg,rgba(5,7,10,.97) 0%,rgba(5,7,10,.86) 42%,"
        "rgba(5,7,10,.38) 76%,rgba(5,7,10,.18) 100%),"
        "linear-gradient(180deg,rgba(5,7,10,.08),rgba(5,7,10,.68)),"
        f"url('data:image/webp;base64,{encoded}');"
        f"background-position:{position};background-size:cover;background-repeat:no-repeat;"
    )


def _hero_metadata(items: tuple[tuple[str, str], ...]) -> str:
    body = "".join(
        "<div class='k-hero-meta-item'>"
        f"<div class='k-hero-meta-label'>{escape(label)}</div>"
        f"<div class='k-hero-meta-value'>{escape(value)}</div>"
        "</div>"
        for label, value in items
    )
    return f"<div class='k-hero-meta'>{body}</div>"


def _project_signature(game: Game) -> str:
    items = _GAME_SIGNATURES.get(game.slug)
    if not items:
        return ""
    body = "".join(
        "<div class='k-project-signature-item'>"
        f"<div class='k-project-signature-label'>{escape(label)}</div>"
        f"<div class='k-project-signature-value'>{escape(value)}</div>"
        "</div>"
        for label, value in items
    )
    return f"<div class='k-project-signature' style='--accent:{game.accent}'>{body}</div>"


def topbar() -> None:
    st.markdown(POLISH_CSS, unsafe_allow_html=True)
    st.markdown(CAMPAIGN_CSS, unsafe_allow_html=True)
    st.markdown(EDITORIAL_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="k-topline">
          <div class="k-brand"><div class="k-mark"><span>K</span></div><div><div class="k-word">KESSOKU</div><div class="k-sub">SYSTEMIC GAMES ON ROBLOX</div></div></div>
          <div class="k-live"><span class="k-dot"></span> DEVELOPMENT SIGNAL ACTIVE</div>
        </div>
        <div class="k-world-marquee" aria-hidden="true">
          <div class="k-world-marquee-track">
            <span>SUPER SOLDIERS / TACTICAL PRESSURE</span>
            <span>HEIST CITY / URBAN CONSEQUENCE</span>
            <span>SERVER AUTHORITY / SHARED TRUTH</span>
            <span>KESSOKU / ARGENTINA</span>
            <span>SUPER SOLDIERS / TACTICAL PRESSURE</span>
            <span>HEIST CITY / URBAN CONSEQUENCE</span>
            <span>SERVER AUTHORITY / SHARED TRUTH</span>
            <span>KESSOKU / ARGENTINA</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, eyebrow: str, lede: str, accent: str, code: str) -> None:
    media_filename, suppress_legacy = _HERO_MEDIA.get(title, (None, False))
    media_style = _campaign_background(media_filename, position="center 42%")
    media_class = " k-hero--campaign" if media_style else ""
    if media_style and media_filename and suppress_legacy:
        suppress_next_campaign_image(media_filename)
    metadata = _hero_metadata(_HERO_METADATA.get(title, ()))
    st.markdown(
        f"""
        <section class="k-hero{media_class}" style="--hero-accent:{accent};{media_style}">
          <div class="k-hero-noise"></div><div class="k-orbit"></div><div class="k-crosshair"></div>
          <div>
            <div class="k-eyebrow">{escape(eyebrow)}</div>
            <h1 class="k-display">{escape(title)}</h1>
            <p class="k-lede">{escape(lede)}</p>
          </div>
          <div class="k-hero-side">
            <div class="k-hero-code">{code}</div>
            <div class="k-signal"><div class="k-signal-line"></div><div class="k-signal-label"><span>WORLD STATE / VERIFIED</span><span>CLIENT / PRESENTATION</span></div></div>
          </div>
        </section>
        {metadata}
        """,
        unsafe_allow_html=True,
    )


def section(title: str, copy: str, kicker: str = "KESSOKU / SYSTEM") -> None:
    st.markdown(
        f"""
        <div class="k-section"><div class="k-section-head">
          <div><div class="k-kicker">{escape(kicker)}</div><h2 class="k-title">{escape(title)}</h2></div>
          <p class="k-copy">{escape(copy)}</p>
        </div></div>
        """,
        unsafe_allow_html=True,
    )


def stat_strip(items: tuple[tuple[str, str, str], ...], accent: str) -> None:
    cards = "".join(
        f'<div class="k-stat"><div class="k-stat-value">{escape(value)}</div><div class="k-stat-label">{escape(label)}</div><div class="k-stat-copy">{escape(copy)}</div></div>'
        for value, label, copy in items
    )
    st.markdown(f'<div class="k-stat-strip" style="--accent:{accent}">{cards}</div>', unsafe_allow_html=True)


def game_card(game: Game, number: str) -> None:
    tags = "".join(f'<span class="k-tag">{escape(tag)}</span>' for tag in (game.status, game.category, "ROBLOX"))
    media_style = _campaign_background(_CARD_MEDIA.get(game.title), position="center")
    media_class = " k-game-card--campaign" if media_style else ""
    signature = _project_signature(game)
    st.markdown(
        f"""
        <article class="k-game-card{media_class}" style="--accent:{game.accent};--soft:rgba({game.accent_rgb[0]},{game.accent_rgb[1]},{game.accent_rgb[2]},.12);{media_style}">
          <div class="k-game-grid"></div><div class="k-game-art"></div><div class="k-card-index">{number}</div>
          <div class="k-card-top"><span>PROJECT / {number}</span><span>{escape(game.status)}</span></div>
          <div class="k-card-body"><h3 class="k-card-title">{escape(game.title)}</h3><p class="k-card-copy">{escape(game.pitch)}</p><div class="k-tags">{tags}</div></div>
        </article>
        {signature}
        """,
        unsafe_allow_html=True,
    )


def feature_grid(game: Game) -> None:
    body = []
    for i, (title, copy) in enumerate(game.features, 1):
        body.append(f'<article class="k-feature"><div class="k-feature-num">0{i} / PILLAR</div><h3>{escape(title)}</h3><p>{escape(copy)}</p></article>')
    st.markdown(f'<div class="k-feature-grid" style="--accent:{game.accent}">{"".join(body)}</div>', unsafe_allow_html=True)


def editorial_panel(code: str, title: str, description: str, bullets: tuple[str, ...], accent: str) -> None:
    bullet_html = "".join(f'<li>{escape(item)}</li>' for item in bullets)
    st.markdown(
        f'<article class="k-editorial" style="--accent:{accent}"><div class="k-editorial-code">{escape(code)}</div><h3>{escape(title)}</h3><p>{escape(description)}</p><ul>{bullet_html}</ul></article>',
        unsafe_allow_html=True,
    )


def mode_panel(label: str, title: str, description: str, facts: tuple[str, ...], accent: str, *, fantasy: str | None = None, objective: str | None = None) -> None:
    fact_html = "".join(f'<div class="k-fact">{escape(fact)}</div>' for fact in facts)
    fantasy_html = f'<div class="k-mode-fantasy">{escape(fantasy)}</div>' if fantasy else ""
    objective_html = f'<div class="k-objective"><span>OPERATIONAL OBJECTIVE</span>{escape(objective)}</div>' if objective else ""
    media_style = _campaign_background(_PANEL_MEDIA.get(title), position="center")
    media_class = " k-mode-panel--campaign" if media_style else ""
    media_label = '<div class="k-mode-media-label">CAMPAIGN FRAME / APPROVED</div>' if media_style else ""
    st.markdown(
        f'<div class="k-mode-panel{media_class}" style="--accent:{accent};{media_style}">{media_label}<div class="k-mode-label">{escape(label)}</div><div class="k-mode-title">{escape(title)}</div>{fantasy_html}<p class="k-mode-copy">{escape(description)}</p>{objective_html}<div class="k-facts">{fact_html}</div></div>',
        unsafe_allow_html=True,
    )


def story_timeline(beats: tuple[StoryBeat, ...], accent: str) -> None:
    body = "".join(
        f'<article class="k-beat"><div class="k-beat-code">{escape(beat.code)}</div><h4>{escape(beat.title)}</h4><p>{escape(beat.description)}</p></article>'
        for beat in beats
    )
    st.markdown(f'<div class="k-beat-grid" style="--accent:{accent}">{body}</div>', unsafe_allow_html=True)


def detail_accordions(blocks: tuple[DetailBlock, ...], accent: str, key_prefix: str) -> None:
    for index, block in enumerate(blocks, 1):
        with st.expander(f"{index:02d} / {block.title} — {block.summary}", expanded=index == 1):
            st.markdown(f'<div class="k-expander-copy" style="--accent:{accent}">{escape(block.description)}</div>', unsafe_allow_html=True)
            cols = st.columns(2, gap="small")
            for bullet_index, bullet in enumerate(block.bullets):
                with cols[bullet_index % 2]:
                    st.markdown(f'<div class="k-mini-rule"><span>{key_prefix.upper()} / {bullet_index + 1:02d}</span>{escape(bullet)}</div>', unsafe_allow_html=True)


def roadmap(items: tuple[tuple[str, str, str], ...], accent: str) -> None:
    rows = "".join(
        f'<div class="k-road"><div class="k-road-num">{escape(num)}</div><div class="k-road-title">{escape(title)}</div><div class="k-road-state">{escape(state)}</div></div>'
        for num, title, state in items
    )
    st.markdown(f'<div class="k-roadmap" style="--accent:{accent}">{rows}</div>', unsafe_allow_html=True)


def action_button(label: str, key: str, accent: str) -> bool:
    with stylable_container(
        key=f"style-{key}",
        css_styles=f"""
        button {{ border-color:{accent}!important; box-shadow: inset 0 0 0 1px {accent}22; }}
        button:hover {{ background:{accent}18!important; border-color:{accent}!important; }}
        """,
    ):
        return st.button(label, key=key, width="stretch")


def update_card(state: str, project: str, title: str, description: str) -> None:
    st.markdown(
        f'<article class="k-update"><div class="k-update-meta"><span>{escape(state)}</span><span>{escape(project)}</span></div><h4>{escape(title)}</h4><p>{escape(description)}</p></article>',
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        """
        <footer class="k-footer-pro">
          <div>
            <div class="k-footer-mark">KESSOKU<br>GAMES.</div>
            <div class="k-footer-copy">Independent Roblox worlds built around readable consequence, bounded simulation, and one shared source of gameplay truth.</div>
          </div>
          <div>
            <div class="k-footer-heading">ACTIVE WORLDS</div>
            <div class="k-footer-line">Super Soldiers</div>
            <div class="k-footer-line">Heist City</div>
            <div class="k-footer-line">Studio systems</div>
          </div>
          <div>
            <div class="k-footer-heading">PUBLIC STATUS</div>
            <div class="k-footer-line">Development active</div>
            <div class="k-footer-line">Canonical links pending</div>
            <div class="k-footer-line">No invented release dates</div>
          </div>
          <div class="k-footer-base"><span>© 2026 KESSOKU GAMES / ARGENTINA</span><span>ONE WORLD / ONE TRUTH / MANY PLAYERS</span></div>
        </footer>
        """,
        unsafe_allow_html=True,
    )
