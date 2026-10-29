from __future__ import annotations

import math
from typing import Any

import plotly.graph_objects as go
import streamlit as st

from kessoku_site.content import OPERATORS
from kessoku_site.roblox_api import fetch_weapon_catalog


def render_loadout_theorycrafter(accent: str) -> None:
    """Render interactive Battle Builds Loadout Theorycrafter & Combat Synergy Calculator."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(118,243,255,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:900;color:#76F3FF;letter-spacing:0.02em;">BATTLE BUILDS: LOADOUT THEORYCRAFTER & SYNERGY LAB</div>
            <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                Construct custom tri-slot combat builds across all 15 authored operatives and 56 weapons. 
                Calculate live DPS, sustained throughput, mobility penalties, and exact Time-to-Kill (TTK) against every biological health pool.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    weapons_dict, _ = fetch_weapon_catalog()
    if not weapons_dict:
        st.warning("Weapons catalog unavailable.")
        return

    # Filter categories
    primary_weapons = [
        k for k, v in weapons_dict.items()
        if not k.startswith("__") and v.get("Slot") == "Main"
    ]
    secondary_weapons = [
        k for k, v in weapons_dict.items()
        if not k.startswith("__") and v.get("Slot") == "Secondary"
    ]
    special_weapons = [
        k for k, v in weapons_dict.items()
        if not k.startswith("__") and v.get("Slot") == "Special"
    ]

    # Selectors
    col_op, col_pri = st.columns(2, gap="medium")
    with col_op:
        op_names = [op.name for op in OPERATORS]
        sel_op_name = st.selectbox("1. Select Operative Archetype", op_names, index=op_names.index("GHOST") if "GHOST" in op_names else 0)
        selected_op = next(op for op in OPERATORS if op.name == sel_op_name)
        op_level = st.slider("Operative Level", min_value=0, max_value=10, value=10, key="tc_op_lvl")

    with col_pri:
        sel_primary = st.selectbox(
            "2. Select Primary Firearm",
            primary_weapons,
            index=primary_weapons.index("SPAS-12") if "SPAS-12" in primary_weapons else 0,
        )
        weap_level = st.slider("Primary Weapon Upgrade Level", min_value=0, max_value=10, value=5, key="tc_weap_lvl")

    col_sec, col_sp1, col_sp2 = st.columns(3, gap="medium")
    with col_sec:
        sel_sec = st.selectbox(
            "3. Select Secondary Weapon",
            secondary_weapons,
            index=secondary_weapons.index("Katana") if "Katana" in secondary_weapons else 0,
        )
    with col_sp1:
        sel_sp1 = st.selectbox(
            "4. Tactical Special 1",
            special_weapons,
            index=special_weapons.index("Taser") if "Taser" in special_weapons else 0,
        )
    with col_sp2:
        sel_sp2 = st.selectbox(
            "5. Tactical Special 2",
            special_weapons,
            index=special_weapons.index("Molotov") if "Molotov" in special_weapons else 1,
        )

    st.divider()

    # Calculations
    op_hp = selected_op.base_hp + (op_level * selected_op.hp_per_level)
    pw_spec = weapons_dict.get(sel_primary, {})
    hit_dmg = pw_spec.get("HitDamage", 300)
    dmg_boost = weap_level * pw_spec.get("DamagePerLevelPercent", 5)
    effective_dmg = hit_dmg * (1 + (dmg_boost / 100.0))
    cooldown = pw_spec.get("ShotCooldown", 0.1)
    rpm = int(60 / cooldown) if cooldown > 0 else 600
    ammo_cap = pw_spec.get("AmmoCapacity", 30)
    reload_time = pw_spec.get("ReloadTime", 2.0)

    # DPS calculations
    burst_dps = effective_dmg * (rpm / 60.0)
    mag_dump_time = (ammo_cap - 1) * cooldown
    total_cycle_time = mag_dump_time + reload_time
    cycle_damage = effective_dmg * ammo_cap
    sustained_dps = cycle_damage / max(0.1, total_cycle_time)

    # Mobility rating
    is_heavy = pw_spec.get("Subcategory") in {"MACHINEGUNS", "SNIPER RIFLES"} or "Shield" in {sel_sp1, sel_sp2}
    is_light = pw_spec.get("Subcategory") == "SMG" and "Katana" == sel_sec
    mobility_score = "TIER A+ (AGILE SPRINT)" if is_light else ("TIER C (HEAVY PLATFORM)" if is_heavy else "TIER B (TACTICAL BALANCED)")

    st.markdown("#### Live Combat Synergy Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("OPERATIVE TOTAL HP", f"{op_hp:,}", f"+{op_level * selected_op.hp_per_level:,} Level Bonus")
    m2.metric("BURST DPS", f"{burst_dps:,.0f} DMG/s", f"{effective_dmg:.0f} Per Hit")
    m3.metric("SUSTAINED DPS", f"{sustained_dps:,.0f} DMG/s", f"Reload: {reload_time}s")
    m4.metric("MOBILITY CLASS", mobility_score)

    st.write("")

    # Time To Kill Matrix
    st.markdown("##### Time-to-Kill (TTK) Benchmark Against Operative Tiers")
    target_roster = (
        ("Light Scout (GHOST)", 4000),
        ("Standard Assault (SOLDIER)", 4200),
        ("Heavy Brawler (PIRATE)", 5700),
        ("Predatory Enforcer (WEREWOLF)", 6300),
        ("Apex Harvester (REAPER)", 7500),
    )

    t_cols = st.columns(5)
    for idx, (target_name, target_hp) in enumerate(target_roster):
        shots_needed = math.ceil(target_hp / max(1.0, effective_dmg))
        time_to_kill_ms = int((shots_needed - 1) * cooldown * 1000)
        with t_cols[idx]:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px;text-align:center;">
                    <div style="font-size:11px;color:#AEB4BC;font-weight:700;">{target_name}</div>
                    <div style="font-size:20px;font-weight:900;color:#76F3FF;margin:4px 0;">{time_to_kill_ms} ms</div>
                    <div style="font-size:11px;color:#F4F2EB;"><strong>{shots_needed}</strong> Hits Needed</div>
                    <div style="font-size:10px;color:#AEB4BC;margin-top:2px;">Target: {target_hp:,} HP</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Synergy Radar
    st.space("small")
    rad_c1, rad_c2 = st.columns([1.2, 0.8], gap="medium")
    with rad_c1:
        # Calculate scores
        leth_score = min(100, int((burst_dps / 30000.0) * 100))
        def_score = min(100, int((op_hp / 17500.0) * 100))
        mob_score = 90 if is_light else (45 if is_heavy else 70)
        rng_score = min(100, int((pw_spec.get("MaxDistance", 100) / 100.0) * 100))
        util_score = 95 if "Turret" in {sel_sp1, sel_sp2} or "Taser" in {sel_sp1, sel_sp2} else 70

        fig = go.Figure(
            data=go.Scatterpolar(
                r=[leth_score, mob_score, rng_score, def_score, util_score, leth_score],
                theta=["Lethality", "Mobility", "Range", "Defense", "Utility", "Lethality"],
                fill="toself",
                fillcolor="rgba(118, 243, 255, 0.2)",
                line=dict(color="#76F3FF", width=2),
            )
        )
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", color="#AEB4BC"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", color="#F4F2EB"),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=40, r=40, t=25, b=25),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with rad_c2:
        st.markdown("##### Build Share Code")
        code = f"BB-{selected_op.name}-{sel_primary}-{sel_sec}-{sel_sp1}-{sel_sp2}".upper().replace(" ", "")
        st.code(code)
        st.caption("Copy your battle build string to share with your squad or preserve for upcoming matches.")
