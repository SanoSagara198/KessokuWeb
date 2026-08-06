from __future__ import annotations

from html import escape

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from .models import DetailBlock, Game, StoryBeat


def topbar() -> None:
    st.markdown(
        """
        <div class="k-topline">
          <div class="k-brand"><div class="k-mark"><span>K</span></div><div><div class="k-word">KESSOKU</div><div class="k-sub">SYSTEMIC GAMES ON ROBLOX</div></div></div>
          <div class="k-live"><span class="k-dot"></span> DEVELOPMENT SIGNAL ACTIVE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, eyebrow: str, lede: str, accent: str, code: str) -> None:
    st.markdown(
        f"""
        <section class="k-hero" style="--hero-accent:{accent}">
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
    st.markdown(
        f"""
        <article class="k-game-card" style="--accent:{game.accent};--soft:rgba({game.accent_rgb[0]},{game.accent_rgb[1]},{game.accent_rgb[2]},.12)">
          <div class="k-game-grid"></div><div class="k-game-art"></div><div class="k-card-index">{number}</div>
          <div class="k-card-top"><span>PROJECT / {number}</span><span>{escape(game.status)}</span></div>
          <div class="k-card-body"><h3 class="k-card-title">{escape(game.title)}</h3><p class="k-card-copy">{escape(game.pitch)}</p><div class="k-tags">{tags}</div></div>
        </article>
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
    st.markdown(
        f'<div class="k-mode-panel" style="--accent:{accent}"><div class="k-mode-label">{escape(label)}</div><div class="k-mode-title">{escape(title)}</div>{fantasy_html}<p class="k-mode-copy">{escape(description)}</p>{objective_html}<div class="k-facts">{fact_html}</div></div>',
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
    st.markdown('<footer class="k-footer"><span>© 2026 KESSOKU GAMES</span><span>ONE WORLD / ONE TRUTH / MANY PLAYERS</span></footer>', unsafe_allow_html=True)
