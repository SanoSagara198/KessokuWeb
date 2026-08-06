from __future__ import annotations

from .models import Alignment, Game, Metric, Mode


SUPER_SOLDIERS = Game(
    slug="super-soldiers",
    title="SUPER SOLDIERS",
    category="TACTICAL ACTION / PVP + PVE",
    tagline="Every second is a tactical decision.",
    pitch=(
        "A mobile-first Roblox combat game where players and bots fight through one "
        "server-owned simulation. Enter a focused 5v5 arena or hold the line in City of Zombies."
    ),
    accent="#76F3FF",
    accent_rgb=(118, 243, 255),
    status="AUTHORITY BETA",
    features=(
        ("One combat truth", "Damage, ammo, cooldowns, skills, bots and score resolve on the server."),
        ("Readable pressure", "Tight silhouettes, bounded effects and immediate feedback preserve clarity."),
        ("Two operations", "Competitive 5v5 and cooperative survival share one disciplined combat core."),
    ),
)

HEIST_CITY = Game(
    slug="heist-city",
    title="HEIST CITY",
    category="SYSTEMIC OPEN WORLD / CRIME + LAW",
    tagline="Every street takes a side.",
    pitch=(
        "A top-down city where traffic, police, criminals and vigilantes occupy the same world. "
        "Drive, chase, hack, investigate and decide what power means when the city pushes back."
    ),
    accent="#FFB84D",
    accent_rgb=(255, 184, 77),
    status="CITY SYSTEMS ALPHA",
    features=(
        ("A city with memory", "Wanted pressure, traffic and missions react to shared server-authored state."),
        ("Systemic pursuit", "Police predict routes, cut across the grid, ram, contain and coordinate."),
        ("Choose your alignment", "Crime, law and vigilantism expose different opportunities in one simulation."),
    ),
)

SUPER_MODES = (
    Mode(
        key="arena",
        title="5V5 ARENA",
        strapline="Ten combatants. One authoritative match.",
        description="Fast rounds, decisive positioning and a readable tactical objective loop designed for repeat play.",
        facts=("10 combatants", "4-minute core match", "6-second respawn", "Bot takeover on leave"),
        metrics=(
            Metric(label="Tempo", value=92),
            Metric(label="Teamplay", value=88),
            Metric(label="Precision", value=84),
            Metric(label="Pressure", value=79),
            Metric(label="Exploration", value=35),
        ),
    ),
    Mode(
        key="zombies",
        title="CITY OF ZOMBIES",
        strapline="Hold the city. Adapt to the horde.",
        description="A cooperative survival operation where threat density, rescue timing and resource discipline drive the run.",
        facts=("Cooperative survival", "Escalating waves", "Shared score pressure", "Adaptive bot support"),
        metrics=(
            Metric(label="Tempo", value=76),
            Metric(label="Teamplay", value=94),
            Metric(label="Precision", value=69),
            Metric(label="Pressure", value=96),
            Metric(label="Exploration", value=63),
        ),
    ),
)

ALIGNMENTS = (
    Alignment(
        key="criminal",
        title="CRIMINAL",
        code="UNDERWORLD / 01",
        description="Build a crew, exploit the city and turn small jobs into an organization the police must understand before they can stop it.",
        objective="Convert risk into influence without allowing the city to close around you.",
        accent="#FF764D",
        metrics=(
            Metric(label="Risk", value=94), Metric(label="Control", value=58),
            Metric(label="Mobility", value=88), Metric(label="Intel", value=64),
            Metric(label="Force", value=82),
        ),
    ),
    Alignment(
        key="police",
        title="POLICE",
        code="DISPATCH / 02",
        description="Read the grid, predict escape routes and coordinate containment without treating the city as a static racetrack.",
        objective="Turn information and positioning into a controlled arrest rather than a chaotic chase.",
        accent="#66A8FF",
        metrics=(
            Metric(label="Risk", value=69), Metric(label="Control", value=94),
            Metric(label="Mobility", value=81), Metric(label="Intel", value=90),
            Metric(label="Force", value=76),
        ),
    ),
    Alignment(
        key="vigilante",
        title="VIGILANTE",
        code="UNSANCTIONED / 03",
        description="Investigate, interfere and move between law and crime while deciding which systems deserve protection.",
        objective="Use asymmetric knowledge to disrupt both sides without becoming predictable.",
        accent="#9DE4B2",
        metrics=(
            Metric(label="Risk", value=86), Metric(label="Control", value=67),
            Metric(label="Mobility", value=91), Metric(label="Intel", value=96),
            Metric(label="Force", value=62),
        ),
    ),
)

STUDIO_PRINCIPLES = (
    ("SERVER OWNS TRUTH", "Clients render state and send intent. Outcomes remain authoritative."),
    ("SYSTEMS SHARE RULES", "Players, bots, traffic and world actors use the same simulation contracts."),
    ("WORK STAYS BOUNDED", "Every server remains autonomous, measurable and stable under concurrency."),
    ("CLARITY BEATS NOISE", "Presentation exists to reveal consequence, not obscure it."),
)
