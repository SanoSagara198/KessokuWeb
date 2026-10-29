from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

from kessoku_site.components import (
    action_button,
    detail_accordions,
    devlog_feed_component,
    editorial_panel,
    feature_grid,
    footer,
    game_card,
    hero,
    hud_controls_bar,
    mode_panel,
    netcode_lab_component,
    playtest_enlistment_component,
    roadmap,
    section,
    skill_planner_component,
    stat_strip,
    story_timeline,
    topbar,
    update_card,
    weapon_lab_component,
    operators_roster_component,
    zombie_descent_intel_component,
    web_audio_synthesizer,
)
from kessoku_site.content import (
    ALIGNMENTS,
    DEVELOPMENT_UPDATES,
    DEVLOG_ENTRIES,
    HEIST_CITY,
    I18N,
    SKILL_CATEGORIES,
    STUDIO_PRINCIPLES,
    SUPER_MODES,
    SUPER_SOLDIERS,
    WEAPONS,
    OPERATORS,
)
from kessoku_site.city_atlas import render_city_atlas
from kessoku_site.auth import handle_oauth_flow, get_roblox_auth_url, login_as_demo
from kessoku_site.companion import render_player_companion
from kessoku_site.theorycrafter import render_loadout_theorycrafter
from kessoku_site.vehicles import render_heist_vehicle_showroom
from kessoku_site.quick_recon import render_quick_recon_terminal
from kessoku_site.mission_intel import render_operative_duel_matrix, render_zombie_descent_planner
from kessoku_site.dispatch_scanner import render_dispatch_scanner, render_vehicle_comparison
from kessoku_site.cluster_status import render_server_clusters_matrix
from kessoku_site.maps import render_battlefield_recon
from kessoku_site.theme import get_theme_css
from kessoku_site.visuals import (
    city_pursuit_figure,
    combat_pressure_figure,
    metric_radar,
    procedural_poster,
    pursuit_sandbox_figure,
    response_doctrine_figure,
    roadmap_chart,
    skill_tree_figure,
    system_topology_figure,
    zombie_escalation_figure,
)

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="Kessoku Games — Battle Builds & Heist City",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Kessoku Games — systemic Roblox worlds."},
)

# Process any pending Roblox OAuth 2.0 callback
handle_oauth_flow()

# Session State Initialization
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "cyan"
if "audio" not in st.session_state:
    st.session_state.audio = True
if "scanlines" not in st.session_state:
    st.session_state.scanlines = False

# Inject Theme CSS and Web Audio Synthesizer
st.markdown(get_theme_css(st.session_state.theme, st.session_state.scanlines), unsafe_allow_html=True)
web_audio_synthesizer(st.session_state.audio)


@st.cache_data(show_spinner=False)
def load_lottie() -> dict:
    with (ROOT / "assets" / "signal.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


@st.cache_data(show_spinner=False)
def poster(accent_rgb: tuple[int, int, int], seed: int) -> bytes:
    return procedural_poster(accent_rgb, seed)


def route_from_query() -> str:
    route = st.query_params.get("view", "Home")
    if route == "Super Soldiers":
        route = "Battle Builds"
    valid = {"Home", "Battle Builds", "Heist City", "Studio", "Companion", "Privacy", "Terms"}
    return route if route in valid else "Home"


def companion_page() -> None:
    hero(
        "BATTLE BUILDS COMPANION",
        "OFFLINE ARMORY & PROGRESSION HUB",
        "Inspect verified live DataStore stats, loadouts, and upgrade curves without launching the game client.",
        "#76F3FF",
        "DATA / ROBLOX OPEN CLOUD<br>AUTH / OAUTH 2.0 VERIFIED<br>CURRENCIES / CREDITS + JIGSAW",
    )
    user = st.session_state.get("roblox_user")
    if user:
        render_player_companion(user)
    else:
        st.markdown(
            """
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(118,243,255,0.25);border-radius:12px;padding:24px;margin-bottom:20px;">
                <h3 style="color:#F4F2EB;margin-top:0;">Connect Your Roblox Identity</h3>
                <p style="color:#AEB4BC;font-size:14px;line-height:1.6;">
                    Sign in with your official Roblox account via <strong>Roblox OAuth 2.0</strong> to link your verified
                    in-game progression. The companion loads your active battle loadouts, wallet balances (Credits & Jigsaw pieces),
                    and operator levels directly from Roblox DataStore in read-only mode.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        auth_url = get_roblox_auth_url()
        col1, col2, _ = st.columns([2, 2, 4])
        with col1:
            st.link_button("🔑 Sign in with Roblox", auth_url)
        with col2:
            if st.button("👁️ Preview Roster (Demo Account)", key="demo_login_btn"):
                login_as_demo()


def privacy_page() -> None:
    hero(
        "PRIVACY POLICY",
        "KESSOKU GAMES / LEGAL",
        "How we handle player authentication and gameplay data via Roblox OAuth 2.0.",
        "#76F3FF",
        "POLICY / COPPA COMPLIANT<br>AUTH / ROBLOX OAUTH 2.0<br>STATUS / ACTIVE",
    )
    if st.button("← Back to Hub", key="back_from_priv"):
        st.query_params["view"] = "Home"
        st.rerun()
    p_file = ROOT / "docs" / "PRIVACY.md"
    if p_file.is_file():
        st.markdown(p_file.read_text(encoding="utf-8"))


def terms_page() -> None:
    hero(
        "TERMS OF SERVICE",
        "KESSOKU GAMES / LEGAL",
        "Terms governing the Kessoku Games platform and offline companion services.",
        "#76F3FF",
        "TERMS / ROBLOX COMPLIANT<br>COMMERCE / NO OFF-PLATFORM SALES<br>STATUS / ACTIVE",
    )
    if st.button("← Back to Hub", key="back_from_terms"):
        st.query_params["view"] = "Home"
        st.rerun()
    t_file = ROOT / "docs" / "TERMS.md"
    if t_file.is_file():
        st.markdown(t_file.read_text(encoding="utf-8"))


def set_route(route: str) -> None:
    st.query_params["view"] = route
    st.rerun()


def navigation() -> str:
    default = route_from_query()
    options = ["Home", "Battle Builds", "Heist City", "Studio", "Companion"]
    default_index = options.index(default) if default in options else 0
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=["house", "crosshair", "buildings", "diamond", "person-badge"],
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "margin-bottom": "1rem"},
            "icon": {"color": "#AEB4BC", "font-size": "14px"},
            "nav-link": {
                "font-size": "12px",
                "font-weight": "800",
                "letter-spacing": ".06em",
                "text-align": "center",
                "margin": "0 3px",
                "padding": "11px 13px",
                "border": "1px solid rgba(255,255,255,.10)",
                "border-radius": "999px",
                "background": "rgba(255,255,255,.025)",
                "color": "#D9DCE1",
            },
            "nav-link-selected": {"background": "#F3F1EA", "color": "#090A0C", "border": "1px solid #F3F1EA"},
        },
        key=f"main-nav-{default}",
    )
    if selected != default:
        st.query_params["view"] = selected
    return selected


def home() -> None:
    t = I18N.get(st.session_state.lang, I18N["EN"])
    hero(
        t["hero_title"],
        t["hero_eyebrow"],
        t["hero_lede"],
        "#F4F2EB",
        "PORTFOLIO / 02<br>SIMULATION / AUTHORITATIVE<br>STATUS / BUILDING",
    )
    section(
        "A compact portfolio with a clear identity.",
        "Kessoku is building two very different player fantasies on one shared discipline: server-owned consequence, responsive presentation and bounded autonomous simulation.",
        "KESSOKU / AT A GLANCE",
    )
    stat_strip(
        (
            ("02", t["active_worlds"], "Tactical combat and a systemic crime-and-law city."),
            ("02", t["operations"], "Competitive 5v5 and cooperative survival in Super Soldiers."),
            ("03", t["alignments"], "Criminal, police and vigilante roles inside Heist City."),
            ("01", t["shared_rule"], "The server owns truth; the client renders state and sends intent."),
        ),
        "#F4F2EB",
    )

    section(
        "Studio intelligence terminal & quick recon.",
        "Query authored specifications across all 15 operatives, 56 weapons, and 35 production pursuit vehicles.",
        "INTELLIGENCE / QUICK RECON",
    )
    render_quick_recon_terminal(SUPER_SOLDIERS.accent)

    section(
        "Two worlds. One shared discipline.",
        "Battle Builds compresses authority into immediate tactical combat. Heist City expands the same discipline across traffic, police, factions and an urban sandbox.",
        "PORTFOLIO / ACTIVE PROJECTS",
    )
    left, right = st.columns(2, gap="small")
    with left:
        game_card(SUPER_SOLDIERS, "01")
        if action_button(t["explore_ss"], "home-ss", SUPER_SOLDIERS.accent):
            set_route("Battle Builds")
    with right:
        game_card(HEIST_CITY, "02")
        if action_button(t["enter_hc"], "home-hc", HEIST_CITY.accent):
            set_route("Heist City")

    section(
        "The games are different because their consequences are different.",
        "The shared architecture does not flatten the portfolio. It gives each project enough coherence to express a distinct rhythm, visual language and player role.",
        "PORTFOLIO / CREATIVE DIRECTION",
    )
    world = st.segmented_control("World", ["BATTLE BUILDS", "HEIST CITY"], default="BATTLE BUILDS", label_visibility="collapsed", width="stretch") or "SUPER SOLDIERS"
    game = SUPER_SOLDIERS if world == "BATTLE BUILDS" else HEIST_CITY
    art, copy = st.columns([1.08, 0.92], gap="large")
    with art:
        st.image(poster(game.accent_rgb, 71 if game.slug == "super-soldiers" else 1987), width="stretch")
    with copy:
        editorial_panel(
            "PLAYER FANTASY / 01" if game.slug == "super-soldiers" else "LIVING CITY / 02",
            game.tagline,
            game.long_description,
            tuple(feature[0] for feature in game.features[:4]),
            game.accent,
        )

    section(
        "The world should remain coherent when players push against it.",
        "Security is not the marketing message. Consequence is. Server ownership is the mechanism that lets every chase, shot, collision and decision belong to one living world.",
        "STUDIO / MANIFESTO",
    )
    st.markdown(f'<div class="k-manifesto" style="--accent:#76F3FF">{t["studio_manifesto"]}</div>', unsafe_allow_html=True)

    section(
        "Development signal.",
        "The public site communicates meaningful direction without exposing unstable internal detail, fake dates or invented release promises.",
        "ROADMAP / PUBLIC VIEW",
    )
    st.altair_chart(roadmap_chart("#F4F2EB"), width="stretch")
    updates = st.columns(4, gap="small")
    for column, update in zip(updates, DEVELOPMENT_UPDATES):
        with column:
            update_card(update.state, update.project, update.title, update.description)


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
        "A tactical game built around decision quality.",
        SUPER_SOLDIERS.long_description,
        "BATTLE BUILDS / EXPERIENCE",
    )
    stat_strip(
        (
            ("5V5", "ARENA", "Ten combatants inside one authoritative match lifecycle."),
            ("PVE", "CITY OF ZOMBIES", "Cooperative survival with escalating composition and resource pressure."),
            ("01", "COMBAT MODEL", "Players and bots share damage, status, movement and score contracts."),
            ("MOBILE", "FIRST", "Camera, input and feedback are designed around touch clarity."),
        ),
        SUPER_SOLDIERS.accent,
    )

    section(
        "Built as one combat system, not two disconnected modes.",
        "Arena and survival use the same authoritative rules for damage, movement, cooldowns, bots, score and match state.",
        "BATTLE BUILDS / PILLARS",
    )
    feature_grid(SUPER_SOLDIERS)

    section(
        "Authored operatives & biological archetypes.",
        "Inspect all 15 playable operatives across the Mortals and Monsters divisions with distinct health pools, dodge profiles and combat traits.",
        "BATTLE BUILDS / OPERATIVES",
    )
    operators_roster_component(OPERATORS, SUPER_SOLDIERS.accent)

    section(
        "Operative tactical matrix: head-to-head duel simulator.",
        "Direct ballistic comparison between any two authored combatants across the Mortals and Monsters divisions with dynamic level scaling and hit-to-kill telemetry.",
        "INTERACTIVE / DUEL SIMULATOR",
    )
    render_operative_duel_matrix(SUPER_SOLDIERS.accent)

    section(
        "Select the operation.",
        "Each mode changes tempo, objectives and pressure while preserving the same combat language. The dossier below describes the player fantasy, objective, encounter rhythm and supporting systems.",
        "INTERACTIVE / MODE BRIEF",
    )
    labels = [mode.title for mode in SUPER_MODES]
    selected = st.segmented_control("Operation", labels, default=labels[0], label_visibility="collapsed", width="stretch") or labels[0]
    mode = next(item for item in SUPER_MODES if item.title == selected)
    panel, chart = st.columns([1.12, 0.88], gap="large")
    with panel:
        mode_panel(mode.strapline, mode.title, mode.description, mode.facts, SUPER_SOLDIERS.accent, fantasy=mode.player_fantasy, objective=mode.objective)
        st_lottie(load_lottie(), height=110, key=f"signal-{mode.key}", speed=0.7)
    with chart:
        st.plotly_chart(metric_radar(mode.metrics, SUPER_SOLDIERS.accent), width="stretch", config={"displayModeBar": False})

    section(
        "The operation unfolds through readable phases.",
        "These phases define the intended player decision sequence. They are not rigid cutscenes; they are the tactical rhythm the systems should consistently create.",
        "BATTLE BUILDS / PLAYER LOOP",
    )
    story_timeline(mode.loop, SUPER_SOLDIERS.accent)

    section(
        "Tactical weapon & ballistics laboratory.",
        "Inspect ballistic performance profiles, simulated dispersion bloom, and time-to-kill curves under varied target armor and precision parameters.",
        "INTERACTIVE / BALLISTICS LAB",
    )
    weapon_lab_component(WEAPONS, SUPER_SOLDIERS.accent)

    section(
        "Loadout theorycrafter & combat synergy lab.",
        "Construct custom builds across all 15 authored operatives and 56 weapons. Calculate live DPS, sustained throughput, mobility penalties, and exact Time-to-Kill (TTK) against every biological health pool.",
        "INTERACTIVE / SYNERGY LAB",
    )
    render_loadout_theorycrafter(SUPER_SOLDIERS.accent)

    section(
        "Battlefield tactical recon & callout blueprints.",
        "Architectural dossiers, sightline corridors, and strategic callouts for Verdant Outpost, District 9 Rail Yard, and Subterranean Silo.",
        "BATTLE BUILDS / MAP RECON",
    )
    render_battlefield_recon(SUPER_SOLDIERS.accent)

    section(
        "Combat pressure laboratory.",
        "Adjust operation intensity and squad posture to visualize how tactical load can rise while squad capability falls. This is a design profile, not live telemetry.",
        "INTERACTIVE / PRESSURE MODEL",
    )
    control_a, control_b = st.columns([1, 1], gap="small")
    with control_a:
        intensity = st.slider("Threat intensity", 1, 10, 6, width="stretch")
    with control_b:
        posture = st.segmented_control("Squad posture", ["AGGRESSIVE", "BALANCED", "DEFENSIVE"], default="BALANCED", width="stretch") or "BALANCED"
    chart_col, metrics_col = st.columns([1.35, 0.65], gap="large")
    with chart_col:
        st.plotly_chart(combat_pressure_figure(mode.key, intensity, posture, SUPER_SOLDIERS.accent), width="stretch", config={"displayModeBar": False})
    with metrics_col:
        peak = min(100, int(28 + intensity * 6.4 + (12 if posture == "AGGRESSIVE" else -7 if posture == "DEFENSIVE" else 0)))
        st.metric("PEAK TACTICAL LOAD", f"{peak}%", border=True, chart_data=[22, 31, 44, 58, peak], chart_type="line", width="stretch")
        st.metric("POSTURE", posture, border=True, width="stretch")
        st.metric("MODE", mode.title, border=True, width="stretch")

    section(
        "Zombie Descent: 10-floor encounter trajectory.",
        "Review authored enemy distributions, archetype mutations, and milestone boss gates across all 10 subterranean survival floors.",
        "BATTLE BUILDS / DESCENT INTEL",
    )
    zombie_descent_intel_component(SUPER_SOLDIERS.accent)

    section(
        "Zombie Descent: subterranean mission planner & swarm density.",
        "Interactive floor-by-floor encounter trajectory, enemy swarm mass calculation, and milestone boss warning gates across all 10 subterranean floors.",
        "INTERACTIVE / DESCENT PLANNER",
    )
    render_zombie_descent_planner(SUPER_SOLDIERS.accent)

    section(
        "Outbreak escalation simulation model.",
        "Simulate horde escalation, barricade durability decay, and ammunition exhaustion over 20 survival waves based on squad composition.",
        "INTERACTIVE / OUTBREAK MODEL",
    )
    zc1, zc2, zc3 = st.columns(3, gap="small")
    with zc1:
        sq_size = st.slider("Squad Size", 1, 4, 4, width="stretch")
    with zc2:
        bar_tier = st.slider("Barricade Reinforcement Tier", 0, 3, 2, width="stretch")
    with zc3:
        discipline = st.segmented_control("Ammunition Discipline", ["CONSERVATIVE", "BALANCED", "AGGRESSIVE"], default="BALANCED", width="stretch") or "BALANCED"
    st.plotly_chart(zombie_escalation_figure(sq_size, bar_tier, discipline, SUPER_SOLDIERS.accent), width="stretch", config={"displayModeBar": False})

    section(
        "System dossiers.",
        "The public description can explain why the experience should feel trustworthy without exposing implementation-sensitive detail or turning the page into API documentation.",
        "BATTLE BUILDS / SYSTEMS",
    )
    detail_accordions(mode.systems, SUPER_SOLDIERS.accent, mode.key)

    section(
        "One authoritative topology.",
        "Player and bot intent enter the same fixed simulation. World state is replicated outward for presentation; clients do not feed outcomes back as truth.",
        "BATTLE BUILDS / AUTHORITY",
    )
    st.plotly_chart(system_topology_figure(SUPER_SOLDIERS.accent), width="stretch", config={"displayModeBar": False})

    section(
        "Current development track.",
        "The public roadmap communicates sequence without exposing internal implementation detail or promising dates that are not yet fixed.",
        "BATTLE BUILDS / ROADMAP",
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


def _doctrine_text(threat: int, evidence: int, mobility: int) -> tuple[str, str]:
    if threat >= 4 and mobility >= 4:
        return "MOBILE CONTAINMENT", "Independent interceptors, rolling roadblocks and controlled intervention become more valuable than stacking units behind the target."
    if evidence >= 4 and threat <= 2:
        return "EVIDENCE-LED PRESSURE", "The city can reduce immediate force while increasing surveillance, identification and targeted follow-up around known assets."
    if threat >= 4:
        return "HIGH-RISK INTERVENTION", "The response prioritizes civilian separation, decisive containment and specialized units capable of ending movement quickly."
    if mobility >= 4:
        return "ROUTE CONTROL", "Units distribute across likely corridors and preserve cross-grid options before attempting direct contact."
    return "PROPORTIONAL RESPONSE", "Local patrol pressure and information gathering remain preferable to immediate maximum-force escalation."


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
        "A city that participates in the story.",
        HEIST_CITY.long_description,
        "HEIST CITY / EXPERIENCE",
    )
    stat_strip(
        (
            ("03", "ALIGNMENTS", "Criminal, police and vigilante play inside the same world."),
            ("24", "SKILLS", "Four six-skill progression families built around utility."),
            ("GRID", "CITY GEOMETRY", "Flat rectangular streets support measurable pursuit and interception."),
            ("01", "WORLD STATE", "Traffic, wanted pressure, missions and evidence remain shared."),
        ),
        HEIST_CITY.accent,
    )

    section(
        "A city that reacts instead of merely decorating the map.",
        "Traffic, police, civilians, missions and wanted pressure read the same world state and remain bounded under concurrency.",
        "HEIST CITY / PILLARS",
    )
    feature_grid(HEIST_CITY)

    section(
        "Choose where you stand.",
        "The simulation stays shared. Alignment changes the opportunities, information, progression and consequences available to the player.",
        "INTERACTIVE / ALIGNMENT DOSSIER",
    )
    labels = [alignment.title for alignment in ALIGNMENTS]
    selected = st.segmented_control("Alignment", labels, default=labels[0], label_visibility="collapsed", width="stretch") or labels[0]
    alignment = next(item for item in ALIGNMENTS if item.title == selected)
    panel, chart = st.columns([1.08, 0.92], gap="large")
    with panel:
        mode_panel(alignment.code, alignment.title, alignment.description, alignment.methods[:4], alignment.accent, fantasy=alignment.fantasy, objective=alignment.objective)
    with chart:
        st.plotly_chart(metric_radar(alignment.metrics, alignment.accent), width="stretch", config={"displayModeBar": False})

    progression, consequences = st.columns(2, gap="small")
    with progression:
        editorial_panel("PROGRESSION / PATH", "How capability grows", alignment.progression, alignment.methods, alignment.accent)
    with consequences:
        editorial_panel("CONSEQUENCE / PRESSURE", "What the city remembers", "Every alignment creates a signature. Greater capability produces stronger opportunity and clearer opposition.", alignment.consequences, alignment.accent)

    section(
        "The alignment loop creates a distinct relationship with the same city.",
        "The sequence below describes what the player repeatedly reads, decides and risks. It is the experiential contract each alignment must preserve.",
        "HEIST CITY / PLAYER LOOP",
    )
    story_timeline(alignment.loop, alignment.accent)

    section(
        "Alignment systems in detail.",
        "These dossiers describe the mechanics and tensions that make each role more than a cosmetic faction choice.",
        "HEIST CITY / SYSTEMS",
    )
    detail_accordions(alignment.systems, alignment.accent, alignment.key)

    section(
        "Dynamic pursuit strategy sandbox.",
        "Simulate police intercept corridors, roadblock cordons, and getaway vectors against various tactical doctrines.",
        "INTERACTIVE / PURSUIT SANDBOX",
    )
    sc1, sc2 = st.columns([1.2, 0.8], gap="small")
    with sc1:
        strat = st.segmented_control("Getaway Doctrine", ["GRID WEAVE", "HIGHWAY BURN", "ALLEY DIVE", "COUNTER-AMBUSH"], default="GRID WEAVE", width="stretch") or "GRID WEAVE"
    with sc2:
        pressure_lvl = st.slider("Police Dispatch Tier", 1, 5, 3, width="stretch")
    st.plotly_chart(pursuit_sandbox_figure(strat, pressure_lvl, alignment.accent), width="stretch", config={"displayModeBar": False})

    section(
        "NCPD tactical radio dispatch scanner.",
        "Live audio transcripts and interception radio calls across NewCity metropolitan sectors.",
        "INTERACTIVE / POLICE SCANNER",
    )
    render_dispatch_scanner(HEIST_CITY.accent)

    section(
        "Explore the streets of NewCity.",
        "Discover the city's actual layout: boulevards, sidewalks and perimeter junctions. Toggle layers and jump to a junction to explore the details.",
        "INTERACTIVE / NEWCITY ATLAS",
    )
    render_city_atlas()

    section(
        "NewCity vehicle fleet & pursuit catalog.",
        "Verified inventory of 35 production models cataloged in Studio across Law Enforcement, Armored SWAT, Heavy Logistics, and Apex Hypercars.",
        "HEIST CITY / FLEET SHOWROOM",
    )
    render_heist_vehicle_showroom(HEIST_CITY.accent)

    section(
        "Vehicle pursuit matrix: intercept comparison.",
        "Compare top speed, ramming mass, ballistic durability, and crew capacity between any two fleet vehicles.",
        "INTERACTIVE / INTERCEPT MATRIX",
    )
    render_vehicle_comparison(HEIST_CITY.accent)

    section(
        "Response doctrine simulator.",
        "Change threat, evidence and mobility to see how a proportional police response should redistribute effort. The model communicates design intent rather than live balance data.",
        "INTERACTIVE / CITY RESPONSE",
    )
    controls = st.columns(3, gap="small")
    with controls[0]:
        threat = st.slider("Threat severity", 1, 5, 3, width="stretch")
    with controls[1]:
        evidence = st.slider("Evidence confidence", 1, 5, 2, width="stretch")
    with controls[2]:
        mobility = st.slider("Target mobility", 1, 5, 4, width="stretch")
    doctrine, doctrine_copy = _doctrine_text(threat, evidence, mobility)
    response_chart, response_copy = st.columns([1.05, 0.95], gap="large")
    with response_chart:
        st.plotly_chart(response_doctrine_figure(threat, evidence, mobility, alignment.accent), width="stretch", config={"displayModeBar": False})
    with response_copy:
        editorial_panel(
            "DISPATCH / RECOMMENDATION",
            doctrine,
            doctrine_copy,
            (f"Threat classification: {threat}/5", f"Evidence confidence: {evidence}/5", f"Target mobility: {mobility}/5", "World state remains authoritative"),
            alignment.accent,
        )

    section(
        "Interactive 24-skill operative build planner.",
        "Allocate syndicate points across Hacking, Combat, Driving, and Intelligence to formulate your operative archetype and inspect tactical synergy perks.",
        "INTERACTIVE / BUILD PLANNER",
    )
    skill_planner_component(SKILL_CATEGORIES, HEIST_CITY.accent)

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
    stat_strip(
        (
            ("01", "SOURCE OF TRUTH", "The server owns gameplay and session outcomes."),
            ("FIXED", "SIMULATION", "Critical work runs on explicit bounded rails."),
            ("SHARED", "CONTRACTS", "Bots and players use the same system rules."),
            ("MANY", "SERVERS", "Scale comes from autonomous bounded instances."),
        ),
        "#F4F2EB",
    )

    section(
        "Six principles govern the work.",
        "A feature is not complete because it functions once. It must remain secure, deterministic, bounded, recoverable and understandable under concurrency.",
        "STUDIO / PRINCIPLES",
    )
    cols = st.columns(2, gap="small")
    for idx, (title, copy) in enumerate(STUDIO_PRINCIPLES):
        with cols[idx % 2]:
            st.markdown(
                f'<article class="k-feature" style="--accent:#F4F2EB;margin-bottom:1rem"><div class="k-feature-num">0{idx + 1} / PRINCIPLE</div><h3>{title}</h3><p>{copy}</p></article>',
                unsafe_allow_html=True,
            )

    section(
        "Global server clusters & authoritative topology.",
        "Low-latency regional edge instances executing fixed 60Hz tick loops with 250ms history rewind buffers.",
        "STUDIO / GLOBAL TOPOLOGY",
    )
    render_server_clusters_matrix("#76F3FF")

    section(
        "Authoritative server netcode & lag compensation laboratory.",
        "Test how Kessoku's 60Hz server tick loop and 250ms history rewind buffer reconcile in-flight client intent without granting peekers advantage.",
        "STUDIO / NETCODE LAB",
    )
    netcode_lab_component("#76F3FF")

    section(
        "The architecture is a supervised flow, not a collection of remotes.",
        "Intent enters through validated actions, advances through fixed simulation and becomes replicated presentation state. Supervisors own lifecycle, health and recovery.",
        "STUDIO / SYSTEM TOPOLOGY",
    )
    st.plotly_chart(system_topology_figure("#76F3FF"), width="stretch", config={"displayModeBar": False})

    section(
        "Technical devlog & engineering dispatches.",
        "Searchable public updates detailing netcode revisions, hitbox capsules, multi-agent pursuit AI, and mobile touch optimizations.",
        "STUDIO / DEVLOG FEED",
    )
    devlog_feed_component(DEVLOG_ENTRIES, "#76F3FF")

    section(
        "Closed flight playtest candidate enlistment.",
        "Submit your operative credentials to participate in upcoming private flight tests for Battle Builds and Heist City.",
        "STUDIO / PLAYTEST ENLISTMENT",
    )
    playtest_enlistment_component("#76F3FF")

    section(
        "Technology used deliberately.",
        "The site combines validated content, cached procedural media, interactive charts and custom presentation components while keeping the deployable surface understandable.",
        "WEBSITE / STACK",
    )
    stack = (
        ("STREAMLIT", "Application runtime, routing state, responsive layout primitives and Community Cloud deployment."),
        ("PLOTLY", "Interactive tactical profiles, pursuit diagrams, response doctrine, topology and progression exploration."),
        ("NEWCITY ATLAS", "An interactive map of captured NewCity geometry with layers, junction search and navigation."),
        ("ALTAIR + PANDAS", "Declarative public roadmap visualization and structured display data."),
        ("NUMPY + PILLOW", "Deterministic cached WebP art-direction placeholders without remote media dependencies."),
        ("PYDANTIC", "Immutable validated models for games, modes, alignments, skills, weapons and public devlog dispatches."),
        ("NETWORKX", "Deterministic topology layout for explaining the server-authoritative system flow."),
        ("LOTTIE + OPTION MENU", "Controlled local motion and compact navigation without a separate frontend build."),
    )
    rows = st.columns(2, gap="small")
    for index, (title, copy) in enumerate(stack):
        with rows[index % 2]:
            editorial_panel(f"STACK / {index + 1:02d}", title, copy, ("Explicit responsibility", "No invented external dependency", "Replaceable behind a stable content model"), "#F4F2EB")
            st.space("small")

    section(
        "Contact surfaces are intentionally pending.",
        "Official Roblox, Discord, YouTube, press and playtest destinations should be added only after their canonical URLs are confirmed.",
        "STUDIO / CONTACT",
    )
    st.info("No unofficial links or invented contact details are published.")


topbar()
lang, theme, audio, scanlines = hud_controls_bar(
    st.session_state.lang,
    st.session_state.theme,
    st.session_state.audio,
    st.session_state.scanlines,
)
if (lang, theme, audio, scanlines) != (st.session_state.lang, st.session_state.theme, st.session_state.audio, st.session_state.scanlines):
    st.session_state.lang = lang
    st.session_state.theme = theme
    st.session_state.audio = audio
    st.session_state.scanlines = scanlines
    st.rerun()

current_view = route_from_query()
if current_view == "Privacy":
    privacy_page()
elif current_view == "Terms":
    terms_page()
elif current_view == "Companion":
    companion_page()
else:
    view = navigation()
    if view == "Home":
        home()
    elif view in {"Battle Builds", "Super Soldiers"}:
        super_soldiers()
    elif view == "Heist City":
        heist_city()
    elif view == "Companion":
        companion_page()
    else:
        studio()
footer()

