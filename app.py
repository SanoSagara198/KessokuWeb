from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Callable

import streamlit as st


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    eyebrow: str
    tagline: str
    summary: str
    accent: str
    accent_soft: str
    status: str
    genre: str
    platform: str
    pillars: tuple[tuple[str, str], ...]
    roadmap: tuple[tuple[str, str], ...]


SUPER_SOLDIERS = Project(
    slug="super-soldiers",
    title="SUPER SOLDIERS",
    eyebrow="TACTICAL ACTION · MULTIPLAYER",
    tagline="Built for decisive combat.",
    summary=(
        "A server-authoritative Roblox combat experience combining competitive 5v5 arenas "
        "with a cooperative City of Zombies survival mode. Fast decisions, readable combat, "
        "and one simulation shared by players and bots."
    ),
    accent="#7CF7FF",
    accent_soft="rgba(124, 247, 255, 0.16)",
    status="IN DEVELOPMENT",
    genre="TACTICAL ACTION",
    platform="ROBLOX",
    pillars=(
        ("Server-owned combat", "Damage, ammo, cooldowns, movement state, score, bots, and players resolve through one authoritative simulation."),
        ("Two operational modes", "Competitive 5v5 PvP and cooperative survival create distinct tactical rhythms without fragmenting the core systems."),
        ("Mobile-first clarity", "Readable silhouettes, direct controls, and bounded effects preserve responsiveness across Roblox devices."),
    ),
    roadmap=(
        ("01", "Authority beta"),
        ("02", "Combat readability"),
        ("03", "PvE encounter depth"),
        ("04", "Public playtests"),
    ),
)

HEIST_CITY = Project(
    slug="heist-city",
    title="HEIST CITY",
    eyebrow="SYSTEMIC OPEN-WORLD · CRIME / LAW",
    tagline="Every street takes a side.",
    summary=(
        "A top-down open-world Roblox city where criminals, police, and vigilantes compete "
        "inside the same living simulation. Drive, chase, hack, investigate, and decide what "
        "power means in a city designed around consequence."
    ),
    accent="#FFC15A",
    accent_soft="rgba(255, 193, 90, 0.16)",
    status="IN DEVELOPMENT",
    genre="OPEN-WORLD ACTION",
    platform="ROBLOX",
    pillars=(
        ("A city with memory", "Traffic, police, pedestrians, wanted pressure, and missions react to the same server-authored world state."),
        ("Choose your alignment", "Build influence as a criminal, enforce order as police, or operate between both systems as a vigilante."),
        ("Systemic driving", "A measurable street grid supports dense traffic, calculated pursuits, roadblocks, ramming, and emergent escapes."),
    ),
    roadmap=(
        ("01", "Physical traffic beta"),
        ("02", "Police pursuit intelligence"),
        ("03", "Mission and faction loop"),
        ("04", "City optimization"),
    ),
)

PROJECTS = (SUPER_SOLDIERS, HEIST_CITY)


st.set_page_config(
    page_title="Kessoku Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Kessoku Games — systemic Roblox experiences.",
    },
)


BASE_CSS = """
<style>
:root {
    --ink: #F5F5F2;
    --muted: #A8A8A2;
    --line: rgba(255,255,255,0.12);
    --panel: rgba(255,255,255,0.045);
    --page: #090A0C;
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    color: var(--ink);
    background:
        radial-gradient(circle at 12% 5%, rgba(124,247,255,0.08), transparent 27rem),
        radial-gradient(circle at 88% 17%, rgba(255,193,90,0.07), transparent 31rem),
        #090A0C;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { visibility: hidden; height: 0; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebar"] { background: #090A0C; }

.block-container {
    max-width: 1280px;
    padding-top: 1.35rem;
    padding-bottom: 1.5rem;
}

h1, h2, h3, p { letter-spacing: -0.015em; }

.k-nav-shell {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    min-height: 3.1rem;
    padding: 0.2rem 0 0.7rem;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1.2rem;
}

.k-logo {
    display: inline-grid;
    place-items: center;
    width: 2.35rem;
    height: 2.35rem;
    border: 1px solid rgba(255,255,255,0.75);
    font-size: 1.05rem;
    font-weight: 900;
    transform: rotate(45deg);
    background: rgba(255,255,255,0.04);
}

.k-logo > span { transform: rotate(-45deg); }
.k-wordmark { font-size: 0.9rem; font-weight: 900; letter-spacing: 0.22em; }
.k-nav-note { color: var(--muted); font-size: 0.74rem; letter-spacing: 0.08em; margin-left: 0.25rem; }

.stButton > button {
    width: 100%;
    min-height: 2.55rem;
    border-radius: 0;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.025);
    color: var(--ink);
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    transition: border-color 120ms ease, background 120ms ease, transform 120ms ease;
}
.stButton > button:hover {
    border-color: rgba(255,255,255,0.52);
    background: rgba(255,255,255,0.08);
    color: white;
    transform: translateY(-1px);
}
.stButton > button:focus:not(:active) { border-color: white; color: white; }

.k-hero {
    position: relative;
    overflow: hidden;
    min-height: 35rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: clamp(1.6rem, 4vw, 4rem);
    border: 1px solid var(--line);
    background: linear-gradient(135deg, rgba(255,255,255,0.065), rgba(255,255,255,0.015));
}
.k-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
    background-size: 46px 46px;
    mask-image: linear-gradient(to bottom, black, transparent 78%);
}
.k-hero-glow {
    position: absolute;
    top: -11rem;
    right: -8rem;
    width: 35rem;
    height: 35rem;
    border-radius: 50%;
    filter: blur(15px);
    opacity: 0.32;
}
.k-eyebrow {
    position: relative;
    z-index: 1;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    margin-bottom: 0.9rem;
}
.k-display {
    position: relative;
    z-index: 1;
    max-width: 920px;
    margin: 0;
    font-size: clamp(3.3rem, 9vw, 8.2rem);
    line-height: 0.82;
    font-weight: 950;
    letter-spacing: -0.075em;
}
.k-lede {
    position: relative;
    z-index: 1;
    max-width: 760px;
    margin: 1.4rem 0 0;
    color: #D4D4CF;
    font-size: clamp(1rem, 1.8vw, 1.28rem);
    line-height: 1.55;
}
.k-kicker {
    position: absolute;
    z-index: 1;
    right: clamp(1.6rem, 4vw, 4rem);
    top: clamp(1.6rem, 4vw, 4rem);
    text-align: right;
    color: var(--muted);
    font-size: 0.67rem;
    letter-spacing: 0.13em;
    line-height: 1.8;
}

.k-section { padding: 5rem 0 1.5rem; }
.k-section-head {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 2rem;
    margin-bottom: 1.7rem;
}
.k-section-title {
    margin: 0;
    max-width: 760px;
    font-size: clamp(2rem, 4.6vw, 4.7rem);
    line-height: 0.97;
    font-weight: 900;
    letter-spacing: -0.055em;
}
.k-section-copy { max-width: 560px; color: var(--muted); line-height: 1.7; }

.k-card-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}
.k-project-card {
    position: relative;
    min-height: 27rem;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1.6rem;
    border: 1px solid var(--line);
    background: linear-gradient(145deg, var(--card-soft), rgba(255,255,255,0.018) 58%);
}
.k-project-card::after {
    content: "";
    position: absolute;
    width: 17rem;
    height: 17rem;
    right: -7rem;
    bottom: -7rem;
    border: 1px solid var(--card-accent);
    transform: rotate(33deg);
    opacity: 0.35;
}
.k-project-number { color: var(--card-accent); font-size: 0.72rem; font-weight: 900; letter-spacing: 0.16em; }
.k-project-title { margin: 0; max-width: 8ch; font-size: clamp(2.4rem, 5vw, 5rem); line-height: 0.84; font-weight: 950; letter-spacing: -0.07em; }
.k-project-copy { max-width: 55ch; color: #C4C4BF; line-height: 1.6; margin-top: 1.1rem; }
.k-meta-row { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 1.1rem; }
.k-pill { border: 1px solid var(--line); padding: 0.42rem 0.58rem; color: #D6D6D1; font-size: 0.62rem; font-weight: 800; letter-spacing: 0.1em; }

.k-pillar-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
.k-pillar {
    min-height: 15rem;
    padding: 1.4rem;
    border-top: 2px solid var(--accent);
    border-right: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    border-left: 1px solid var(--line);
    background: rgba(255,255,255,0.025);
}
.k-pillar-index { color: var(--accent); font-size: 0.67rem; font-weight: 900; letter-spacing: 0.12em; }
.k-pillar h3 { margin: 3.2rem 0 0.8rem; font-size: 1.35rem; }
.k-pillar p { color: var(--muted); line-height: 1.65; }

.k-roadmap { border-top: 1px solid var(--line); }
.k-roadmap-item {
    display: grid;
    grid-template-columns: 5rem 1fr auto;
    align-items: center;
    gap: 1rem;
    padding: 1.2rem 0;
    border-bottom: 1px solid var(--line);
}
.k-roadmap-number { color: var(--accent); font-weight: 900; }
.k-roadmap-label { font-size: 1.05rem; font-weight: 760; }
.k-roadmap-state { color: var(--muted); font-size: 0.66rem; font-weight: 800; letter-spacing: 0.12em; }

.k-quote {
    padding: clamp(2rem, 5vw, 5rem);
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.025);
    font-size: clamp(1.6rem, 4.2vw, 4.2rem);
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: -0.05em;
}
.k-quote small { display: block; margin-top: 1.6rem; color: var(--muted); font-size: 0.67rem; letter-spacing: 0.13em; }

.k-studio-grid { display: grid; grid-template-columns: 1.25fr .75fr; gap: 1rem; }
.k-studio-panel { min-height: 18rem; padding: 1.6rem; border: 1px solid var(--line); background: rgba(255,255,255,.025); }
.k-studio-panel h3 { margin-top: 0; font-size: 1.7rem; }
.k-studio-panel p { color: var(--muted); line-height: 1.75; }
.k-rule { margin-top: 5rem; font-size: clamp(1.5rem, 3vw, 3rem); font-weight: 850; line-height: 1.1; letter-spacing: -0.04em; }

.k-footer {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 5rem;
    padding: 1.5rem 0 0.4rem;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 0.68rem;
    letter-spacing: 0.08em;
}

[data-testid="stRadio"] > div { gap: 0.35rem; }
[data-testid="stRadio"] label {
    border: 1px solid var(--line);
    padding: 0.52rem 0.72rem;
    background: rgba(255,255,255,0.025);
}
[data-testid="stRadio"] label:has(input:checked) { border-color: rgba(255,255,255,0.65); background: rgba(255,255,255,0.10); }
[data-testid="stRadio"] label p { font-size: 0.72rem; font-weight: 800; letter-spacing: 0.06em; }

@media (max-width: 760px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .k-nav-note { display: none; }
    .k-hero { min-height: 31rem; padding: 1.35rem; }
    .k-kicker { position: relative; top: auto; right: auto; text-align: left; margin-bottom: auto; }
    .k-card-grid, .k-pillar-grid, .k-studio-grid { grid-template-columns: 1fr; }
    .k-section-head { align-items: start; flex-direction: column; }
    .k-project-card { min-height: 24rem; }
    .k-roadmap-item { grid-template-columns: 3rem 1fr; }
    .k-roadmap-state { display: none; }
    .k-footer { flex-direction: column; }
}
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)


def set_page(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def render_nav() -> None:
    left, right = st.columns([1.55, 2.45])
    with left:
        st.markdown(
            """
            <div class="k-nav-shell">
                <div class="k-logo"><span>K</span></div>
                <div>
                    <div class="k-wordmark">KESSOKU</div>
                    <div class="k-nav-note">SYSTEMIC GAMES ON ROBLOX</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        cols = st.columns(4)
        labels = (("HOME", "home"), ("SUPER SOLDIERS", "super-soldiers"), ("HEIST CITY", "heist-city"), ("STUDIO", "studio"))
        for col, (label, target) in zip(cols, labels):
            with col:
                if st.button(label, key=f"nav-{target}", use_container_width=True):
                    set_page(target)


def render_footer() -> None:
    st.markdown(
        """
        <footer class="k-footer">
            <span>© 2026 KESSOKU GAMES</span>
            <span>DESIGNED FOR ROBLOX · BUILT AROUND SERVER-OWNED SYSTEMS</span>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, eyebrow: str, lede: str, accent: str, kicker: str) -> None:
    st.markdown(
        f"""
        <section class="k-hero">
            <div class="k-hero-glow" style="background:{accent};"></div>
            <div class="k-kicker">{kicker}</div>
            <div class="k-eyebrow" style="color:{accent};">{escape(eyebrow)}</div>
            <h1 class="k-display">{escape(title)}</h1>
            <p class="k-lede">{escape(lede)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="k-section">
            <div class="k-section-head">
                <h2 class="k-section-title">{escape(title)}</h2>
                <p class="k-section-copy">{escape(copy)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project_cards() -> None:
    cards = []
    for idx, project in enumerate(PROJECTS, start=1):
        cards.append(
            f"""
            <article class="k-project-card" style="--card-accent:{project.accent}; --card-soft:{project.accent_soft};">
                <div class="k-project-number">PROJECT / 0{idx}</div>
                <div>
                    <h3 class="k-project-title">{escape(project.title)}</h3>
                    <p class="k-project-copy">{escape(project.summary)}</p>
                    <div class="k-meta-row">
                        <span class="k-pill">{escape(project.status)}</span>
                        <span class="k-pill">{escape(project.genre)}</span>
                        <span class="k-pill">{escape(project.platform)}</span>
                    </div>
                </div>
            </article>
            """
        )
    st.markdown(f'<div class="k-card-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
    action_a, action_b = st.columns(2)
    with action_a:
        if st.button("ENTER SUPER SOLDIERS", key="home-super", use_container_width=True):
            set_page("super-soldiers")
    with action_b:
        if st.button("ENTER HEIST CITY", key="home-heist", use_container_width=True):
            set_page("heist-city")


def render_home() -> None:
    hero(
        "GAMES WITH CONSEQUENCE.",
        "KESSOKU GAMES PRESENTS",
        "We build Roblox experiences where players, bots, vehicles, combat, and the city obey the same rules. Two worlds. One engineering standard.",
        "#F5F5F2",
        "INDEPENDENT STUDIO<br>ROBLOX SYSTEMS<br>ARGENTINA",
    )

    section_heading(
        "Two worlds. One shared discipline.",
        "Super Soldiers compresses authority into immediate combat. Heist City expands it across traffic, police, factions, and an entire urban sandbox.",
    )
    render_project_cards()

    section_heading(
        "The world should not negotiate with the client.",
        "Kessoku projects are designed around bounded, deterministic server ownership. Clients render state and send intent; they do not author gameplay truth.",
    )
    st.markdown(
        """
        <div class="k-quote">
            SECURE ENOUGH TO TRUST.<br>FAST ENOUGH TO FEEL.<br>SYSTEMIC ENOUGH TO SURPRISE.
            <small>KESSOKU / DEVELOPMENT PRINCIPLE 001</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pillars(project: Project) -> None:
    items = []
    for index, (title, copy) in enumerate(project.pillars, start=1):
        items.append(
            f"""
            <article class="k-pillar" style="--accent:{project.accent};">
                <div class="k-pillar-index">0{index} / PILLAR</div>
                <h3>{escape(title)}</h3>
                <p>{escape(copy)}</p>
            </article>
            """
        )
    st.markdown(f'<div class="k-pillar-grid">{"".join(items)}</div>', unsafe_allow_html=True)


def render_roadmap(project: Project) -> None:
    items = []
    for number, label in project.roadmap:
        items.append(
            f"""
            <div class="k-roadmap-item">
                <div class="k-roadmap-number">{escape(number)}</div>
                <div class="k-roadmap-label">{escape(label)}</div>
                <div class="k-roadmap-state">ACTIVE DEVELOPMENT</div>
            </div>
            """
        )
    st.markdown(
        f'<div class="k-roadmap" style="--accent:{project.accent};">{"".join(items)}</div>',
        unsafe_allow_html=True,
    )


def render_super_soldiers_interactive() -> None:
    section_heading(
        "Select the operation.",
        "This interactive brief demonstrates how the project page can expose modes, features, updates, trailers, or playtest calls without becoming a conventional dashboard.",
    )
    mode = st.radio(
        "Operation",
        options=("5V5 ARENA", "CITY OF ZOMBIES"),
        horizontal=True,
        label_visibility="collapsed",
        key="ss-mode",
    )
    if mode == "5V5 ARENA":
        st.markdown(
            f"""
            <div class="k-quote" style="border-color:{SUPER_SOLDIERS.accent};">
                TEN COMBATANTS.<br>ONE AUTHORITATIVE MATCH.<br>NO CLIENT-OWNED OUTCOMES.
                <small>5V5 ARENA / COMPETITIVE OPERATION</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="k-quote" style="border-color:{SUPER_SOLDIERS.accent};">
                HOLD THE CITY.<br>ADAPT TO THE HORDE.<br>MAKE EVERY SECOND COUNT.
                <small>CITY OF ZOMBIES / COOPERATIVE SURVIVAL</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_heist_interactive() -> None:
    section_heading(
        "Choose where you stand.",
        "Alignment changes the lens through which players read the same city. The simulation remains shared; intent, pressure, and opportunity do not.",
    )
    alignment = st.radio(
        "Alignment",
        options=("CRIMINAL", "POLICE", "VIGILANTE"),
        horizontal=True,
        label_visibility="collapsed",
        key="heist-alignment",
    )
    briefs = {
        "CRIMINAL": "Build a crew, exploit the city, evade escalating police intelligence, and turn small jobs into an underworld operation.",
        "POLICE": "Read traffic, predict escape routes, coordinate pursuit tactics, and contain threats without treating the city as a static racetrack.",
        "VIGILANTE": "Operate between law and crime. Investigate, interfere, and decide which systems deserve protection—and which deserve disruption.",
    }
    st.markdown(
        f"""
        <div class="k-quote" style="border-color:{HEIST_CITY.accent};">
            {escape(briefs[alignment])}
            <small>{escape(alignment)} / ALIGNMENT BRIEF</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project(project: Project, interactive: Callable[[], None]) -> None:
    hero(
        project.title,
        project.eyebrow,
        project.tagline + " " + project.summary,
        project.accent,
        f"{project.status}<br>{project.genre}<br>{project.platform}",
    )

    section_heading(
        "Designed as a system, not a collection of tricks.",
        "Every feature must strengthen security, determinism, bounded execution, and autonomous server operation under concurrency.",
    )
    render_pillars(project)

    interactive()

    section_heading(
        "Current development track.",
        "A public-facing roadmap can stay intentionally high-level while still communicating the engineering sequence and the project’s present focus.",
    )
    render_roadmap(project)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    if st.button("RETURN TO ALL PROJECTS", key=f"return-{project.slug}", use_container_width=True):
        set_page("home")


def render_studio() -> None:
    hero(
        "KESSOKU",
        "INDEPENDENT ROBLOX STUDIO",
        "We make worlds that remain coherent when the player pushes against them. The server owns truth. The client renders state and sends intent.",
        "#F5F5F2",
        "SYSTEMIC DESIGN<br>SERVER AUTHORITY<br>RESPONSIVE CLIENTS",
    )
    section_heading(
        "A compact studio with an uncompromising architecture.",
        "The website is intentionally structured around projects and principles rather than marketing volume. It can expand later with devlogs, jobs, press material, and playtest registration.",
    )
    st.markdown(
        """
        <div class="k-studio-grid">
            <article class="k-studio-panel">
                <h3>What Kessoku builds</h3>
                <p>Systemic Roblox games with shared simulation rules, legible player choices, and strong visual identities. The current portfolio spans tactical combat and an urban crime-and-law sandbox.</p>
                <div class="k-rule">ONE WORLD.<br>ONE TRUTH.<br>MANY PLAYERS.</div>
            </article>
            <article class="k-studio-panel">
                <h3>Operating principles</h3>
                <p>Server-owned outcomes.<br>Deterministic simulation rails.<br>Bounded work per server.<br>Clients dedicated to presentation.<br>Players and bots using the same rules.<br>Scalability through autonomous servers.</p>
            </article>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading(
        "Contact surface, ready when needed.",
        "Replace the placeholder configuration with the studio’s Roblox group, Discord, press email, social profiles, and playtest forms before publishing.",
    )
    st.info("External links are deliberately omitted from this starter because no official Kessoku URLs were provided.")


if "page" not in st.session_state:
    st.session_state.page = "home"

render_nav()

page = st.session_state.page
if page == "home":
    render_home()
elif page == "super-soldiers":
    render_project(SUPER_SOLDIERS, render_super_soldiers_interactive)
elif page == "heist-city":
    render_project(HEIST_CITY, render_heist_interactive)
elif page == "studio":
    render_studio()
else:
    st.session_state.page = "home"
    st.rerun()

render_footer()
