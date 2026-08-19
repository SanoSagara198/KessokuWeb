from __future__ import annotations

import base64
from html import escape

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from .campaign import CAMPAIGN_CSS
from .content import ARCHETYPES, I18N, calculate_build_archetype
from .editorial import EDITORIAL_CSS
from .media import campaign_asset, suppress_next_campaign_image
from .models import (
    ArchetypeResult,
    DetailBlock,
    DevelopmentUpdate,
    DevlogEntry,
    Game,
    SkillCategory,
    StoryBeat,
    WeaponSpec,
)
from .polish import POLISH_CSS
from .visuals import (
    ballistics_ttk_figure,
    netcode_rollback_figure,
    pursuit_sandbox_figure,
    recoil_pattern_figure,
    skill_build_radar,
    zombie_escalation_figure,
)


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


def web_audio_synthesizer(enabled: bool = True) -> None:
    if not enabled:
        return
    st.markdown(
        """
        <script>
        (function() {
            if (window._kessokuAudioBound) return;
            window._kessokuAudioBound = true;
            let audioCtx = null;
            function getCtx() {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
                return audioCtx;
            }
            function playBeep(freq1, freq2, duration, type='sine', vol=0.06) {
                try {
                    const ctx = getCtx();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq1, ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(freq2, ctx.currentTime + duration);
                    gain.gain.setValueAtTime(vol, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + duration);
                } catch(e) {}
            }
            document.addEventListener('click', function(e) {
                const target = e.target;
                if (target.closest('button') || target.closest('[data-testid="stPills"] button') || target.closest('[data-testid="stSegmentedControl"] button')) {
                    playBeep(520, 880, 0.05, 'sine', 0.05);
                } else if (target.closest('div[data-testid="stExpander"]')) {
                    playBeep(340, 480, 0.07, 'triangle', 0.05);
                }
            }, true);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def hud_controls_bar(current_lang: str, current_theme: str, audio_enabled: bool, scanlines_enabled: bool) -> tuple[str, str, bool, bool]:
    with st.expander("⚡ HUD PROTOCOL DECK / THEME & SYSTEM PREFERENCES", expanded=False):
        c1, c2, c3, c4 = st.columns([1, 1.4, 1, 1], gap="small")
        with c1:
            lang = st.segmented_control("LANGUAGE", ["EN", "ES"], default=current_lang, width="stretch") or current_lang
        with c2:
            theme_keys = ["cyan", "amber", "titanium", "crimson"]
            theme_labels = ["Cyan", "Amber", "Titanium", "Crimson"]
            current_idx = theme_keys.index(current_theme) if current_theme in theme_keys else 0
            selected_label = st.segmented_control("THEME", theme_labels, default=theme_labels[current_idx], width="stretch") or theme_labels[current_idx]
            theme = theme_keys[theme_labels.index(selected_label)]
        with c3:
            audio_opt = st.segmented_control("TACTICAL SFX", ["ACTIVE", "MUTED"], default="ACTIVE" if audio_enabled else "MUTED", width="stretch") or ("ACTIVE" if audio_enabled else "MUTED")
            audio = audio_opt == "ACTIVE"
        with c4:
            crt_opt = st.segmented_control("CRT SCANLINES", ["OFF", "ON"], default="ON" if scanlines_enabled else "OFF", width="stretch") or ("ON" if scanlines_enabled else "OFF")
            scanlines = crt_opt == "ON"
    return lang, theme, audio, scanlines


def weapon_lab_component(weapons: tuple[WeaponSpec, ...], accent: str) -> None:
    weapon_names = [w.name for w in weapons]
    selected_name = st.segmented_control("Select Weapon", weapon_names, default=weapon_names[0], label_visibility="collapsed", width="stretch") or weapon_names[0]
    weapon = next(w for w in weapons if w.name == selected_name)

    m1, m2, m3, m4 = st.columns(4, gap="small")
    with m1:
        st.metric("CALIBER / ROLE", weapon.caliber, weapon.role, border=True, width="stretch")
    with m2:
        st.metric("CYCLIC RATE", f"{weapon.rpm} RPM", f"Mag: {weapon.mag_size} Rnds", border=True, width="stretch")
    with m3:
        st.metric("BASE DAMAGE", f"{weapon.base_damage:.0f} HP", f"Headshot: {weapon.head_mult}x", border=True, width="stretch")
    with m4:
        st.metric("OPTIMAL RANGE", f"{weapon.optimal_range}m", f"Max: {weapon.max_range}m", border=True, width="stretch")

    ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 1], gap="small")
    with ctrl1:
        armor = st.segmented_control("Target Armor Tier", ["TIER 0 (NONE)", "TIER 1 (KEVLAR 15%)", "TIER 2 (PLATE 30%)"], default="TIER 0 (NONE)", width="stretch") or "TIER 0 (NONE)"
        armor_tier = 0 if "0" in armor else 1 if "1" in armor else 2
    with ctrl2:
        headshot_pct = st.slider("Headshot Precision %", 0, 100, 30, step=5, width="stretch")
    with ctrl3:
        burst = st.segmented_control("Fire Discipline", ["CONTROLLED BURST", "SUSTAINED AUTO"], default="CONTROLLED BURST", width="stretch") or "CONTROLLED BURST"
        burst_mode = burst == "CONTROLLED BURST"

    chart_left, chart_right = st.columns([1.2, 0.8], gap="large")
    with chart_left:
        st.plotly_chart(ballistics_ttk_figure(weapon, armor_tier, headshot_pct, accent), width="stretch", config={"displayModeBar": False})
    with chart_right:
        st.plotly_chart(recoil_pattern_figure(weapon, burst_mode, accent), width="stretch", config={"displayModeBar": False})


def skill_planner_component(categories: tuple[SkillCategory, ...], accent: str) -> None:
    if "skill_points" not in st.session_state:
        st.session_state.skill_points = {"hacking": 2, "combat": 3, "driving": 3, "intelligence": 2}

    points = st.session_state.skill_points
    total_allocated = sum(points.values())
    max_budget = 10
    remaining = max_budget - total_allocated

    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:1rem 1.4rem;border:1px solid rgba(255,255,255,.12);border-radius:16px;background:rgba(12,15,20,.6);margin-bottom:1.2rem;">
            <div>
                <span style="color:var(--muted);font-size:.65rem;letter-spacing:.12em;">SYNDICATE POINT BUDGET</span>
                <div style="font-size:1.6rem;font-weight:900;color:#F4F2EB;">{total_allocated} / {max_budget} <span style="font-size:.85rem;color:{'#8CFFAA' if remaining >= 0 else '#FF4D4D'};font-weight:700;">({remaining} REMAINING)</span></div>
            </div>
            <div style="text-align:right;">
                <span style="color:var(--muted);font-size:.65rem;letter-spacing:.12em;">OPERATIVE ARCHETYPE</span>
                <div style="font-size:1.1rem;font-weight:850;color:{accent};">{escape(calculate_build_archetype(points).name)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4, gap="small")
    for idx, cat in enumerate(categories):
        with cols[idx]:
            val = st.slider(f"{cat.title} ({points[cat.key]}/6)", 0, 6, points[cat.key], key=f"sp_{cat.key}", width="stretch")
            st.session_state.skill_points[cat.key] = val

    archetype = calculate_build_archetype(points)
    arc_col, radar_col = st.columns([1.15, 0.85], gap="large")
    with arc_col:
        st.markdown(
            f"""
            <div style="padding:1.4rem;border:1px solid rgba(255,255,255,.14);border-radius:18px;background:linear-gradient(150deg,rgba(255,255,255,.05),rgba(255,255,255,.015));min-height:100%;">
                <div style="display:inline-block;padding:.25rem .55rem;border:1px solid {archetype.accent};border-radius:999px;color:{archetype.accent};font-size:.6rem;letter-spacing:.12em;font-weight:800;margin-bottom:.8rem;">
                    SYNDICATE CLASSIFICATION / {escape(archetype.badge)}
                </div>
                <h3 style="margin:0 0 .5rem;font-size:1.8rem;letter-spacing:-.04em;">{escape(archetype.name)}</h3>
                <p style="color:#AEB4BC;font-size:.9rem;line-height:1.65;margin-bottom:1.2rem;">{escape(archetype.description)}</p>
                <div style="padding:.8rem;border:1px solid rgba(255,255,255,.08);border-radius:12px;background:rgba(0,0,0,.25);font-family:ui-monospace,monospace;font-size:.72rem;color:#D8DADF;">
                    SHARE HASH: <span style="color:{archetype.accent};">KESSOKU-H{points['hacking']}-C{points['combat']}-D{points['driving']}-I{points['intelligence']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with radar_col:
        st.plotly_chart(skill_build_radar(points, archetype.accent), width="stretch", config={"displayModeBar": False})


def devlog_feed_component(entries: tuple[DevlogEntry, ...], accent: str) -> None:
    categories = ["ALL", "NETCODE", "COMBAT", "TRAFFIC AI", "BALANCE", "MOBILE UI"]
    selected_cat = st.segmented_control("Filter Category", categories, default="ALL", width="stretch") or "ALL"
    filtered = [e for e in entries if selected_cat == "ALL" or e.category == selected_cat]

    for entry in filtered:
        highlights_html = "".join(f"<li style='margin-bottom:.35rem;'>{escape(h)}</li>" for h in entry.highlights)
        cat_badge_color = "#76F3FF" if entry.category == "NETCODE" else "#FF764D" if entry.category == "COMBAT" else "#FFB84D" if entry.category == "TRAFFIC AI" else "#9DE4B2"
        st.markdown(
            f"""
            <article style="padding:1.3rem;border:1px solid rgba(255,255,255,.11);border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.01));margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.7rem;">
                    <div style="display:flex;gap:.5rem;align-items:center;">
                        <span style="background:{cat_badge_color}22;color:{cat_badge_color};border:1px solid {cat_badge_color}55;padding:.2rem .5rem;border-radius:999px;font-size:.6rem;font-weight:800;letter-spacing:.1em;">{escape(entry.category)}</span>
                        <span style="font-family:ui-monospace,monospace;font-size:.72rem;color:var(--muted);">{escape(entry.version)}</span>
                    </div>
                    <span style="font-family:ui-monospace,monospace;font-size:.68rem;color:var(--muted);">{escape(entry.date)}</span>
                </div>
                <h4 style="margin:0 0 .5rem;font-size:1.25rem;letter-spacing:-.03em;">{escape(entry.title)}</h4>
                <p style="color:#C8CCD2;font-size:.88rem;line-height:1.65;margin:0 0 .8rem;">{escape(entry.summary)}</p>
                <ul style="color:var(--muted);font-size:.82rem;line-height:1.6;padding-left:1.1rem;margin:0;">
                    {highlights_html}
                </ul>
            </article>
            """,
            unsafe_allow_html=True,
        )


def playtest_enlistment_component(accent: str) -> None:
    if "playtest_submitted" not in st.session_state:
        st.session_state.playtest_submitted = False

    if st.session_state.playtest_submitted:
        st.success("CONFIDENTIAL CLEARANCE ACCEPTED: Your operative handle has been logged into the closed playtest dispatch queue.")
        return

    with st.form("playtest_enlistment_form"):
        st.markdown(
            f"""
            <div style="margin-bottom:1rem;">
                <div style="color:{accent};font-size:.65rem;letter-spacing:.14em;font-weight:800;">RECRUITMENT PROTOCOL / V2.3</div>
                <h3 style="margin:.3rem 0;font-size:1.5rem;">Closed Playtest Candidate Enlistment</h3>
                <p style="color:var(--muted);font-size:.85rem;line-height:1.6;">Join private flight tests for authoritative combat, physical traffic stress tests, and netcode benchmarking.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2, gap="small")
        with c1:
            callsign = st.text_input("Operative Call-Sign (Roblox Username)", placeholder="e.g. GhostOperator_99")
            platform = st.selectbox("Primary Test Hardware", ["Mobile (iOS / iPadOS)", "Mobile (Android Snapdragon/Dimensity)", "PC (Windows 11 / DirectX 12)", "PC (macOS Metal)", "Console (PlayStation / Xbox)"])
        with c2:
            role = st.selectbox("Combat Discipline Interest", ["Tactical Assaulter (5v5 Arena)", "Horde Defense Specialist (City of Zombies)", "Getaway Wheelman (Heist City)", "Infiltrator / Hacker (Heist City)", "Netcode & Exploitation Bug Hunter"])
            region = st.selectbox("Primary Test Region", ["South America (Buenos Aires / São Paulo)", "North America (US East / US West)", "Europe (Frankfurt / London)", "Asia-Pacific (Tokyo / Sydney)"])

        nda = st.checkbox("I agree to report telemetry, reproducible desync steps, and maintain confidentiality during closed flights.", value=True)
        submitted = st.form_submit_button("SUBMIT CLEARANCE APPLICATION", width="stretch")
        if submitted:
            if callsign.strip():
                st.session_state.playtest_submitted = True
                st.rerun()
            else:
                st.warning("Please enter a valid call-sign / Roblox username.")


def netcode_lab_component(accent: str) -> None:
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3, gap="small")
    with ctrl_col1:
        ping = st.slider("Simulated Round-Trip Latency (Ping)", 20, 250, 60, step=5, format="%d ms", width="stretch")
    with ctrl_col2:
        jitter = st.slider("Network Jitter Variation", 0, 40, 6, step=2, format="%d ms", width="stretch")
    with ctrl_col3:
        loss = st.slider("Packet Loss %", 0, 30, 0, step=5, format="%d%%", width="stretch")

    st.plotly_chart(netcode_rollback_figure(ping, jitter, loss, accent), width="stretch", config={"displayModeBar": False})
    
    t1, t2, t3, t4 = st.columns(4, gap="small")
    with t1:
        st.metric("SERVER TICK FREQ", "60 Hz", "16.6 ms step", border=True, width="stretch")
    with t2:
        st.metric("HISTORY BUFFER", "250 ms", "15 circular frames", border=True, width="stretch")
    with t3:
        st.metric("VALIDATION LATENCY", f"{(ping/2)+jitter:.1f} ms", "One-way delay", border=True, width="stretch")
    with t4:
        st.metric("RECONCILIATION", "100% SECURE" if loss < 15 else "EXTRAPOLATED", "No client spoofing", border=True, width="stretch")

