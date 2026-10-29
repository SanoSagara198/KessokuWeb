from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go
from typing import Any

from kessoku_site.vehicles import HEIST_VEHICLES


HEIST_TARGETS = (
    {
        "id": "fed_vault",
        "name": "FEDERAL RESERVE SUBTERRANEAN VAULT",
        "district": "Central Financial Boulevard",
        "base_haul": 500000,
        "base_heat": 5,
        "base_dispatch_sec": 45,
        "required_skills": "Hacking Lv 3 (Security Override) & Combat Lv 3 (Armor)",
        "description": "The most secure subterranean gold bullion vault in NewCity. Guarded by seismic sensors and fortified blast gates. Guaranteed SWAT mobilization upon breach.",
        "accent": "#FF5252",
    },
    {
        "id": "convoy",
        "name": "ARMORED CASH CONVOY INTERCEPT",
        "district": "North Bridge Highway Bypass",
        "base_haul": 320000,
        "base_heat": 4,
        "base_dispatch_sec": 40,
        "required_skills": "Driving Lv 3 (Ramming Momentum) & Combat Lv 2",
        "description": "High-risk mobile heist. Ambush an armored SWAT transport in transit across highway lanes. Requires heavy ramming vehicle and spike strips.",
        "accent": "#FF764D",
    },
    {
        "id": "harbor",
        "name": "MARINA CONTRABAND SHIPMENT",
        "district": "Docklands Basin - Pier 14",
        "base_haul": 180000,
        "base_heat": 3,
        "base_dispatch_sec": 75,
        "required_skills": "Hacking Lv 2 (Crane Override) & Driving Lv 2",
        "description": "Steal high-value shipping container cargo under cover of night. Perimeter patrolled by dock security and harbor police boats.",
        "accent": "#FFB84D",
    },
    {
        "id": "jewelry",
        "name": "DOWNTOWN DIAMOND & JEWELRY BOUTIQUE",
        "district": "Metro Shopping Arcade",
        "base_haul": 95000,
        "base_heat": 2,
        "base_dispatch_sec": 60,
        "required_skills": "Driving Lv 1 (Agile Sprint) & Combat Lv 1",
        "description": "Fast-paced retail smash and grab. Glass display alarms trigger local patrol units. Escape through pedestrian alleys before cruisers establish a perimeter.",
        "accent": "#76F3FF",
    },
)


def render_heist_planner(accent: str) -> None:
    """Render interactive Heist Operation Planning & Payout Simulator."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,118,77,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:900;color:#FF764D;letter-spacing:0.02em;">HEIST CITY: TACTICAL OPERATION PLANNER & PAYOUT SIMULATOR</div>
            <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                Select target facility, coordinate crew size, configure tactical approach, and calculate projected net haul and police dispatch response.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_names = [t["name"] for t in HEIST_TARGETS]
    sel_name = st.selectbox("1. Target Objective Facility", t_names, index=0)
    target = next(t for t in HEIST_TARGETS if t["name"] == sel_name)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        crew_size = st.slider("Crew Size (Operatives)", 1, 4, 3, width="stretch")
    with c2:
        approach = st.segmented_control("Tactical Approach", ["STEALTH / SILENT", "LOUD / ASSAULT", "SMASH & GRAB"], default="STEALTH / SILENT", width="stretch") or "STEALTH / SILENT"
    with c3:
        car_names = [v.name for v in HEIST_VEHICLES]
        sel_car = st.selectbox("Getaway Fleet Vehicle", car_names, index=3 if len(car_names) > 3 else 0)

    # Calculations
    is_stealth = "STEALTH" in approach
    is_smash = "SMASH" in approach
    
    dispatch_bonus = 35 if is_stealth else (-15 if "LOUD" in approach else 10)
    dispatch_eta = max(20, target["base_dispatch_sec"] + dispatch_bonus)
    heat_stars = max(1, target["base_heat"] - (1 if is_stealth else 0) + (1 if "LOUD" in approach else 0))

    gross_haul = target["base_haul"] * (0.85 if is_smash else 1.0)
    laundering_fee_pct = 0.15 if is_stealth else 0.25
    net_haul = gross_haul * (1.0 - laundering_fee_pct)
    per_crew_payout = int(net_haul / crew_size)

    # Display Operation Summary
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:4px solid {target['accent']};border-radius:10px;padding:18px;margin-top:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <span style="font-size:11px;font-weight:900;color:{target['accent']};letter-spacing:0.08em;">SECTOR: {target['district'].upper()}</span>
                    <div style="font-size:18px;font-weight:900;color:#F4F2EB;margin-top:2px;">{target['name']}</div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:22px;font-weight:900;color:#8CFFAA;">${per_crew_payout:,}</span>
                    <div style="font-size:11px;color:#AEB4BC;">ESTIMATED CUT PER OPERATIVE ({crew_size} CREW)</div>
                </div>
            </div>
            <div style="font-size:12px;color:#AEB4BC;margin-top:8px;line-height:1.4;">{target['description']}</div>
            <div style="font-size:11px;color:#D9DCE1;margin-top:6px;"><strong>Prerequisites:</strong> {target['required_skills']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("GROSS TAKE", f"${gross_haul:,.0f}", f"Total Loot Vault", border=True, width="stretch")
    m2.metric("NET CLEAN FUNDS", f"${net_haul:,.0f}", f"-{laundering_fee_pct*100:.0f}% Laundering Fee", border=True, width="stretch")
    m3.metric("POLICE DISPATCH ETA", f"{dispatch_eta} Seconds", f"Window To Escape", border=True, width="stretch")
    m4.metric("PURSUIT HEAT", f"{'★' * min(5, heat_stars)}", f"{heat_stars}-Star Response", border=True, width="stretch")
