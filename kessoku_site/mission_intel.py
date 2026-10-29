from __future__ import annotations

import math
from typing import Any

import plotly.graph_objects as go
import streamlit as st

from kessoku_site.content import OPERATORS
from kessoku_site.roblox_api import fetch_weapon_catalog


def render_operative_duel_matrix(accent: str) -> None:
    """Render side-by-side Operative head-to-head tactical comparison & duel simulator."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(118,243,255,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:900;color:#76F3FF;letter-spacing:0.02em;">OPERATIVE TACTICAL MATRIX: HEAD-TO-HEAD DUEL SIMULATOR</div>
            <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                Direct ballistic comparison between any two authored combatants across the Mortals and Monsters divisions.
                Adjust experience levels, evaluate health scaling, and calculate engagement outcomes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    op_names = [op.name for op in OPERATORS]
    c1, c2, c3 = st.columns([1.2, 1.2, 0.8], gap="medium")
    with c1:
        name_a = st.selectbox("Operative Alpha", op_names, index=op_names.index("SOLDIER") if "SOLDIER" in op_names else 0, key="op_a")
        op_a = next(op for op in OPERATORS if op.name == name_a)
        lvl_a = st.slider(f"{name_a} Level", 1, 10, 5, key="lvl_a", width="stretch")
    with c2:
        name_b = st.selectbox("Operative Bravo", op_names, index=op_names.index("WEREWOLF") if "WEREWOLF" in op_names else 1, key="op_b")
        op_b = next(op for op in OPERATORS if op.name == name_b)
        lvl_b = st.slider(f"{name_b} Level", 1, 10, 5, key="lvl_b", width="stretch")
    with c3:
        headshot_rate = st.slider("Headshot Precision %", 0, 100, 30, step=10, key="duel_hs", width="stretch")

    hp_a = op_a.base_hp + (lvl_a - 1) * op_a.hp_per_level
    hp_b = op_b.base_hp + (lvl_b - 1) * op_b.hp_per_level

    # Side-by-side dossiers
    card_col1, card_col2 = st.columns(2, gap="medium")
    for col, op, lvl, hp, side_color in (
        (card_col1, op_a, lvl_a, hp_a, "#76F3FF"),
        (card_col2, op_b, lvl_b, hp_b, "#FF764D"),
    ):
        with col:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:4px solid {side_color};border-radius:10px;padding:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-size:18px;font-weight:900;color:#F4F2EB;">{op.name} (LVL {lvl})</span>
                        <span style="font-size:11px;font-weight:800;color:{side_color};background:rgba(255,255,255,0.05);padding:2px 8px;border-radius:4px;border:1px solid {side_color};">{op.division}</span>
                    </div>
                    <div style="font-size:12px;font-weight:700;color:#AEB4BC;margin-top:2px;">{op.role} &bull; Dodge: <em>{op.dodge_ability}</em></div>
                    <div style="margin-top:10px;font-size:24px;font-weight:900;color:{side_color};">{hp:,} <span style="font-size:12px;color:#AEB4BC;font-weight:600;">MAX HP</span></div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:6px;line-height:1.4;">{op.description}</div>
                    <div style="margin-top:10px;display:flex;gap:4px;flex-wrap:wrap;">
                        {"".join(f'<span style="background:rgba(255,255,255,0.04);color:#D9DCE1;font-size:10px;padding:2px 6px;border-radius:4px;border:1px solid rgba(255,255,255,0.08);">{t}</span>' for t in op.tactical_traits)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Duel firearm test
    st.write("")
    weapons_dict, _ = fetch_weapon_catalog()
    duel_weapons = [
        "M416", "SPAS-12", "Barrett M82", "Vector", "PKM", "Deagle", "Katana"
    ]
    avail_duel_w = [w for w in duel_weapons if w in weapons_dict]
    if not avail_duel_w:
        avail_duel_w = list(weapons_dict.keys())[:6]

    sel_duel_w = st.segmented_control("Simulate Ballistic Engagement With Firearm", avail_duel_w, default=avail_duel_w[0], width="stretch") or avail_duel_w[0]
    w_data = weapons_dict.get(sel_duel_w, {})
    
    base_dmg = float(w_data.get("Damage", 450))
    hs_mult = float(w_data.get("HeadshotDamageMult", 1.5))
    cooldown = float(w_data.get("Cooldown", 0.1))
    rpm = int(60 / cooldown) if cooldown > 0 else 600

    effective_dmg = base_dmg * (1.0 + (hs_mult - 1.0) * (headshot_rate / 100.0))

    hits_to_kill_a = math.ceil(hp_a / max(1.0, effective_dmg))
    ttk_a_ms = int((hits_to_kill_a - 1) * cooldown * 1000)

    hits_to_kill_b = math.ceil(hp_b / max(1.0, effective_dmg))
    ttk_b_ms = int((hits_to_kill_b - 1) * cooldown * 1000)

    diff_ms = abs(ttk_a_ms - ttk_b_ms)
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-top:14px;">
            <div style="font-size:14px;font-weight:800;color:#F4F2EB;">SIMULATED ENGAGEMENT: {sel_duel_w} &bull; {effective_dmg:,.0f} DMG/HIT ({rpm} RPM)</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px;">
                <div style="background:rgba(118,243,255,0.05);padding:12px;border-radius:6px;border:1px solid rgba(118,243,255,0.2);">
                    <div style="font-size:12px;color:#76F3FF;font-weight:700;">TTK against {op_a.name}</div>
                    <div style="font-size:24px;font-weight:900;color:#F4F2EB;margin:4px 0;">{ttk_a_ms} ms</div>
                    <div style="font-size:11px;color:#AEB4BC;">Requires <strong>{hits_to_kill_a}</strong> direct impacts</div>
                </div>
                <div style="background:rgba(255,118,77,0.05);padding:12px;border-radius:6px;border:1px solid rgba(255,118,77,0.2);">
                    <div style="font-size:12px;color:#FF764D;font-weight:700;">TTK against {op_b.name}</div>
                    <div style="font-size:24px;font-weight:900;color:#F4F2EB;margin:4px 0;">{ttk_b_ms} ms</div>
                    <div style="font-size:11px;color:#AEB4BC;">Requires <strong>{hits_to_kill_b}</strong> direct impacts</div>
                </div>
            </div>
            <div style="font-size:12px;color:#AEB4BC;margin-top:12px;text-align:center;">
                Durability delta: <strong style="color:#F4F2EB;">{op_b.name if hp_b > hp_a else op_a.name}</strong> withstands {abs(hits_to_kill_b - hits_to_kill_a)} additional round(s), conferring a <strong>{diff_ms} ms</strong> window advantage in sustained crossfire.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_zombie_descent_planner(accent: str) -> None:
    """Render interactive 10-Floor Zombie Descent Mission Planner & Resource Calculator."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,118,77,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:900;color:#FF764D;letter-spacing:0.02em;">ZOMBIE DESCENT: 10-FLOOR SUBTERRANEAN MISSION PLANNER</div>
            <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                Plan subterranean assault routes, estimate ammunition depletion, and analyze infected swarm mutations across all 10 authored survival depths.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    floor_data = {
        1: {"title": "Outbreak Ground Zero", "weak": 77, "heavy": 20, "haste": 10, "rifle": 0, "gas": 0, "smoke": 0, "boss": 0, "lore": "Initial subterranean quarantine breach. Fast shamblers patrol service shafts."},
        2: {"title": "Transit Sector Bravo", "weak": 92, "heavy": 28, "haste": 16, "rifle": 0, "gas": 0, "smoke": 0, "boss": 0, "lore": "Collapsed metro rails. Heavies begin pushing squads into open corners."},
        3: {"title": "Sub-Level Pump Station", "weak": 110, "heavy": 35, "haste": 25, "rifle": 0, "gas": 0, "smoke": 0, "boss": 0, "lore": "Narrow catwalks over flooded sewer canals. Haste infected rush across railings."},
        4: {"title": "Hazardous Spillway", "weak": 120, "heavy": 58, "haste": 12, "rifle": 16, "gas": 12, "smoke": 0, "boss": 0, "lore": "Toxic Gas carriers burst on death, denying movement corridors. Rifle infected open fire from high ground."},
        5: {"title": "★ SUBTERRANEAN CHECKPOINT", "weak": 75, "heavy": 45, "haste": 19, "rifle": 0, "gas": 0, "smoke": 0, "boss": 1, "lore": "Milestone gate: The Subterranean Colossus spawns with massive ground cleave and stagger resistance."},
        6: {"title": "Abandoned Vault Antechamber", "weak": 130, "heavy": 64, "haste": 18, "rifle": 34, "gas": 16, "smoke": 12, "boss": 0, "lore": "Smoke infected obscure sightlines and cancel aim-cone acquisition until point-blank range."},
        7: {"title": "Deep Hydroelectric Turbine", "weak": 142, "heavy": 70, "haste": 32, "rifle": 48, "gas": 24, "smoke": 20, "boss": 0, "lore": "Multi-tiered turbine halls. Simultaneous ranged suppression and toxic gas clouds."},
        8: {"title": "Bunker Blast Doors", "weak": 155, "heavy": 76, "haste": 52, "rifle": 65, "gas": 30, "smoke": 32, "boss": 0, "lore": "High-velocity swarm clusters. Heavy Brutes charge through fortified barricades."},
        9: {"title": "Penultimate Quarantine Line", "weak": 165, "heavy": 80, "haste": 78, "rifle": 85, "gas": 39, "smoke": 45, "boss": 0, "lore": "Absolute chaos threshold. Over 450 total infected converge across converging hallways."},
        10: {"title": "★ EXTRACTION GAGE (THE CORE)", "weak": 140, "heavy": 80, "haste": 67, "rifle": 100, "gas": 35, "smoke": 40, "boss": 2, "lore": "Final extraction elevator. 2 Dual Apex Colossi deploy simultaneously alongside 460+ infected."},
    }

    selected_floor = st.slider("Select Subterranean Floor Depth", 1, 10, 5, format="Floor %02d", width="stretch")
    info = floor_data[selected_floor]
    is_boss = info["boss"] > 0

    # Total HP pool of this wave:
    # Weak: 600 HP, Heavy: 2500 HP, Haste: 450 HP, Rifle: 800 HP, Gas: 900 HP, Smoke: 750 HP, Boss: 35000 HP
    total_hp = (
        info["weak"] * 600
        + info["heavy"] * 2500
        + info["haste"] * 450
        + info["rifle"] * 800
        + info["gas"] * 900
        + info["smoke"] * 750
        + info["boss"] * 35000
    )
    total_count = (
        info["weak"] + info["heavy"] + info["haste"] + info["rifle"] + info["gas"] + info["smoke"] + info["boss"]
    )

    f_accent = "#FF764D" if is_boss else "#76F3FF"
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid {'rgba(255,118,77,0.5)' if is_boss else 'rgba(255,255,255,0.08)'};border-left:4px solid {f_accent};border-radius:10px;padding:18px;margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <span style="font-size:12px;font-weight:900;color:{f_accent};letter-spacing:0.08em;">FLOOR {selected_floor:02d} / SECTOR ANALYSIS</span>
                    <div style="font-size:20px;font-weight:900;color:#F4F2EB;margin-top:2px;">{info['title']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:20px;font-weight:900;color:{f_accent};">{total_hp:,} HP</div>
                    <div style="font-size:11px;color:#AEB4BC;">TOTAL HORDE MASS ({total_count} ENTITIES)</div>
                </div>
            </div>
            <div style="font-size:13px;color:#D9DCE1;margin-top:10px;line-height:1.5;">{info['lore']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Spawn distribution breakdown
    m1, m2, m3, m4, m5, m6 = st.columns(6, gap="small")
    m1.metric("WEAK SHAMBLERS", f"{info['weak']}", "600 HP Each", border=True, width="stretch")
    m2.metric("HEAVY BRUTES", f"{info['heavy']}", "2,500 HP Each", border=True, width="stretch")
    m3.metric("HASTE RUSHERS", f"{info['haste']}", "450 HP Fast", border=True, width="stretch")
    m4.metric("RANGED RIFLES", f"{info['rifle']}", "800 HP Distant", border=True, width="stretch")
    m5.metric("TOXIC / SMOKE", f"{info['gas'] + info['smoke']}", "Hazard Carriers", border=True, width="stretch")
    m6.metric("APEX BOSSES", f"{info['boss']}", "35,000 HP Gate", border=True, width="stretch")

    # Resource expenditure chart
    fig = go.Figure()
    categories = ["Weak", "Heavy", "Haste", "Rifles", "Hazards (Gas/Smoke)", "Apex Boss"]
    counts = [info["weak"], info["heavy"], info["haste"], info["rifle"], info["gas"] + info["smoke"], info["boss"]]
    colors = ["#76F3FF", "#FFB84D", "#8CFFAA", "#AEB4BC", "#C27BA0", "#FF5252"]

    fig.add_trace(go.Bar(
        x=categories,
        y=counts,
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.2)", width=1)),
        text=counts,
        textposition="auto",
    ))
    fig.update_layout(
        title=f"Floor {selected_floor:02d} Swarm Entity Density",
        height=280,
        margin=dict(l=30, r=30, t=40, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#AEB4BC", size=11),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
