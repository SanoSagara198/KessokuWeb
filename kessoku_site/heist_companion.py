from __future__ import annotations

import streamlit as st
from typing import Any

from kessoku_site.roblox_api import fetch_heist_player_profile
from kessoku_site.vehicles import HEIST_VEHICLES


def render_heist_companion(user_info: dict[str, Any]) -> None:
    """Render the Heist City: NewCity Syndicate Offline Companion Dashboard."""
    raw_uid = str(user_info.get("user_id", "2725352577")).strip()
    user_id = raw_uid if raw_uid else "2725352577"
    username = user_info.get("username", "KessokuDev")

    profile_data, source = fetch_heist_player_profile(user_id)
    progress = profile_data.get("Progress", {})
    skills = profile_data.get("Skills", {})

    # Top Header
    badge_color = "#FF764D" if source == "live" else "#FFB84D"
    badge_label = "🟢 LIVE ROBLOX DATASTORE" if source == "live" else "⚡ VERIFIED PRODUCTION SNAPSHOT"

    money = progress.get("Money", 450000)
    bank = progress.get("BankBalance", 1850000)
    dirty = progress.get("DirtyCash", 120000)
    wanted = progress.get("WantedLevel", 2)
    alignment = progress.get("CurrentAlignment", "criminal").upper()

    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,118,77,0.3);border-radius:14px;padding:22px;margin-bottom:24px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
                <div>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="font-size:24px;font-weight:900;color:#F4F2EB;">{username}</span>
                        <span style="background:rgba(255,118,77,0.15);color:#FF764D;font-size:11px;font-weight:800;padding:3px 10px;border-radius:4px;border:1px solid #FF764D;">
                            ALIGNMENT: {alignment}
                        </span>
                    </div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:4px;font-family:monospace;">
                        HEIST CITY UNIVERSE: <strong>10772507321</strong> &bull; PLACE ID: <strong>103267062013348</strong> &bull; USER ID: {user_id}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:10px;font-weight:800;color:{badge_color};letter-spacing:0.08em;margin-bottom:4px;">{badge_label}</div>
                    <div style="font-size:18px;font-weight:900;color:#FF5252;">
                        {'★' * wanted}{'☆' * (5 - wanted)} <span style="font-size:12px;color:#AEB4BC;font-weight:600;">({wanted}-STAR WANTED)</span>
                    </div>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));gap:12px;margin-top:18px;">
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);">
                    <div style="font-size:11px;color:#AEB4BC;font-weight:700;">ON-HAND WALLET</div>
                    <div style="font-size:22px;font-weight:900;color:#76F3FF;margin-top:2px;">${money:,}</div>
                    <div style="font-size:10px;color:#AEB4BC;">Liquid cash</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);">
                    <div style="font-size:11px;color:#AEB4BC;font-weight:700;">SECURE BANK VAULT</div>
                    <div style="font-size:22px;font-weight:900;color:#8CFFAA;margin-top:2px;">${bank:,}</div>
                    <div style="font-size:10px;color:#AEB4BC;">Clean laundered funds</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);">
                    <div style="font-size:11px;color:#AEB4BC;font-weight:700;">UNLAUNDERED CASH</div>
                    <div style="font-size:22px;font-weight:900;color:#FFB84D;margin-top:2px;">${dirty:,}</div>
                    <div style="font-size:10px;color:#AEB4BC;">Needs laundering drop</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);">
                    <div style="font-size:11px;color:#AEB4BC;font-weight:700;">HEAT SIGNATURE</div>
                    <div style="font-size:22px;font-weight:900;color:#FF764D;margin-top:2px;">{progress.get('HeatDecaySecondsRemaining', 24)}s</div>
                    <div style="font-size:10px;color:#AEB4BC;">Decay window remaining</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    h_tabs = st.tabs(
        [
            "🏢 Faction Standing & Treasury",
            "🚗 Syndicate Garage",
            "🧠 24-Skill Tree Allocation",
            "📋 Heist Receipts & Contracts",
            "🚀 Roblox Launch Portal",
        ]
    )

    # TAB 1: FACTION & REPUTATION
    with h_tabs[0]:
        st.markdown("#### Faction Alignment & Underworld Standing")
        st.caption("Consequence reputation tracked across the three dynamic urban factions.")
        rep = progress.get("Reputation", {})
        f_cols = st.columns(3)
        with f_cols[0]:
            st.metric("CRIMINAL REPUTATION", f"{rep.get('Criminal', 0):,} REP", "Underworld Kingpin Tier", border=True)
        with f_cols[1]:
            st.metric("POLICE TRUST INDEX", f"{rep.get('Police', 0):,} REP", "Undercover Suspicion", border=True)
        with f_cols[2]:
            st.metric("VIGILANTE STREET-CRED", f"{rep.get('Vigilante', 0):,} REP", "Independent Operative", border=True)

        st.markdown("##### Active Citations & Traffic Ledger")
        fines = progress.get("TrafficFines", [])
        if fines:
            for fine in fines:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,82,82,0.05);border:1px solid rgba(255,82,82,0.3);border-radius:8px;padding:12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#FF5252;">{fine.get('citation')}</strong>: {fine.get('violation')}
                        </div>
                        <div style="text-align:right;">
                            <span style="font-weight:900;color:#F4F2EB;">${fine.get('fine', 0):,}</span> &bull; <span style="color:#FF764D;font-weight:700;">{fine.get('status')}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No active citations recorded.")

    # TAB 2: GARAGE
    with h_tabs[1]:
        st.markdown("#### Syndicate Fleet & Impound Ledger")
        st.caption("Vehicles owned and tuned in NewCity.")
        owned_names = progress.get("VehiclesOwned", [])
        g_cols = st.columns(3)
        for i, v_name in enumerate(owned_names):
            # Find vehicle spec if available
            spec = next((v for v in HEIST_VEHICLES if v.name == v_name), None)
            role = spec.role if spec else "Personal Transport"
            dur = spec.durability if spec else "Standard"
            speed = spec.speed_tier if spec else "Tier 2"
            seats = spec.seats if spec else 4

            with g_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:3px solid #76F3FF;border-radius:8px;padding:14px;margin-bottom:12px;">
                        <div style="font-size:15px;font-weight:800;color:#F4F2EB;">{v_name}</div>
                        <div style="font-size:11px;color:#76F3FF;font-weight:700;margin-top:2px;">{role}</div>
                        <div style="margin-top:8px;display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:11px;color:#AEB4BC;">
                            <div>Speed: <strong style="color:#F4F2EB;">{speed}</strong></div>
                            <div>Armor: <strong style="color:#F4F2EB;">{dur}</strong></div>
                            <div>Seats: <strong style="color:#F4F2EB;">{seats}</strong></div>
                            <div>Status: <strong style="color:#8CFFAA;">Ready</strong></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # TAB 3: SKILLS
    with h_tabs[2]:
        st.markdown("#### 24-Skill Syndicate Progression")
        st.caption("Authoritative allocation from HaistSkillProgression_v2.")
        s_m1, s_m2, s_m3 = st.columns(3)
        s_m1.metric("AVAILABLE SKILL POINTS", f"{skills.get('availablePoints', 0)} PTS", "Unallocated", border=True)
        s_m2.metric("CURRENT SKILL XP", f"{skills.get('skillXP', 0):,} XP", "Toward Next Point", border=True)
        s_m3.metric("LIFETIME POINTS EARNED", f"{skills.get('lifetimePointsEarned', 0)} PTS", "Career Mastery", border=True)

        alloc = skills.get("allocatedSkills", {})
        s_cols = st.columns(4)
        categories = ("Hacking", "Combat", "Driving", "Intelligence")
        cat_colors = {"Hacking": "#76F3FF", "Combat": "#FF5252", "Driving": "#FFB84D", "Intelligence": "#8CFFAA"}
        for idx, cat in enumerate(categories):
            cat_alloc = alloc.get(cat, {})
            with s_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-top:3px solid {cat_colors[cat]};border-radius:8px;padding:14px;">
                        <div style="font-size:14px;font-weight:900;color:{cat_colors[cat]};">{cat.upper()}</div>
                        <div style="margin-top:10px;">
                            {"".join(f'<div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:6px;"><span style="color:#AEB4BC;">{s_name}</span><strong style="color:#F4F2EB;">Tier {s_lvl}/3</strong></div>' for s_name, s_lvl in cat_alloc.items())}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # TAB 4: CONTRACTS & RECEIPTS
    with h_tabs[3]:
        st.markdown("#### Bounded Heist Receipts & Payouts")
        st.caption("Idempotent completed transaction history.")
        jobs = progress.get("CompletedJobs", [])
        for job in jobs:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:4px solid #8CFFAA;border-radius:8px;padding:14px;margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-size:14px;font-weight:800;color:#F4F2EB;">[{job.get('id')}] {job.get('title')}</span>
                        <span style="font-size:16px;font-weight:900;color:#8CFFAA;">+${job.get('payout', 0):,}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:11px;color:#AEB4BC;margin-top:4px;">
                        <span>Sector: {job.get('district')}</span>
                        <span>Status: <strong style="color:#8CFFAA;">{job.get('status')}</strong></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # TAB 5: ROBLOX LAUNCH PORTAL
    with h_tabs[4]:
        st.markdown("#### Direct Launch: Heist City on Roblox")
        st.markdown(
            f"""
            <div style="background:rgba(255,118,77,0.04);border:1px solid rgba(255,118,77,0.3);border-radius:12px;padding:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;">
                <div>
                    <div style="font-size:20px;font-weight:900;color:#F4F2EB;">LAUNCH NEWCITY HEIST EXPERIENCE</div>
                    <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                        Universe ID: <strong>10772507321</strong> &bull; Production Place ID: <strong>103267062013348</strong>
                    </div>
                    <div style="font-size:12px;color:#D9DCE1;margin-top:8px;">
                        Direct launch into live police pursuit, traffic simulation, and syndicate crime network.
                    </div>
                </div>
                <a href="https://www.roblox.com/games/103267062013348" target="_blank" style="background:#FF764D;color:#090A0C;font-weight:900;font-size:14px;padding:12px 24px;border-radius:8px;text-decoration:none;letter-spacing:0.04em;">
                    PLAY HEIST CITY &rarr;
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
