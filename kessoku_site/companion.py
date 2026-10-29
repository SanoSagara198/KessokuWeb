from __future__ import annotations

import math
import time
from typing import Any

import streamlit as st

from kessoku_site.auth import logout_user
from kessoku_site.roblox_api import (
    fetch_operator_catalog,
    fetch_player_profile,
    fetch_weapon_catalog,
)


def _hash_seed(user_id_num: int, window: int) -> int:
    """Replicate deterministic ShopService seed generator for the 6-hour window."""
    text = f"shop|{user_id_num}|{window}"
    h = 5381
    for char in text:
        h = ((h * 33) + ord(char)) % 2147483647
    return h


def render_player_companion(user_info: dict[str, Any]) -> None:
    """Render the comprehensive, tactical offline companion dashboard."""
    raw_uid = str(user_info.get("user_id", "2725352577")).strip()
    user_id = raw_uid if raw_uid else "2725352577"
    username = user_info.get("username", "KessokuDev")
    display_name = user_info.get("display_name", username)
    avatar_url = user_info.get("avatar_url")
    is_demo = user_info.get("is_demo", False)

    # 1. Fetch player profile from API or verified local fallback
    profile, source = fetch_player_profile(user_id)
    weapons_catalog, _ = fetch_weapon_catalog()
    operators_catalog, _ = fetch_operator_catalog()

    # Header Profile Card
    badge_color = "#76F3FF" if source == "live" else "#FFB84D"
    badge_label = (
        "🟢 LIVE ROBLOX DATASTORE"
        if source == "live"
        else "⚡ VERIFIED PRODUCTION SNAPSHOT"
    )

    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(118,243,255,0.25);border-radius:14px;padding:22px;margin-bottom:24px;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
                <div style="display:flex;align-items:center;gap:18px;">
                    <img src="{avatar_url or 'https://tr.rbxcdn.com/30DAY-AvatarHeadshot-placeholder/150/150/AvatarHeadshot/Webp/noFilter'}" style="width:76px;height:76px;border-radius:50%;border:2px solid {badge_color};" />
                    <div>
                        <div style="font-size:24px;font-weight:900;color:#F4F2EB;letter-spacing:0.02em;">{display_name}</div>
                        <div style="font-size:13px;color:#AEB4BC;font-family:monospace;">@{username} &bull; Roblox ID: {user_id}</div>
                        <div style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap;">
                            <span style="background:rgba(118,243,255,0.12);color:{badge_color};border:1px solid {badge_color};border-radius:6px;padding:3px 10px;font-size:11px;font-weight:800;letter-spacing:0.05em;">
                                {badge_label}
                            </span>
                            {'<span style="background:rgba(255,255,255,0.06);color:#AEB4BC;border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700;">DEMO PROFILE</span>' if is_demo else ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_hdr_left, col_hdr_right = st.columns([5, 1])
    with col_hdr_right:
        if st.button("Sign Out", key="comp_logout_btn"):
            logout_user()

    if not profile:
        st.error(
            f"Unable to read profile for User ID {user_id}. Please verify the universe ID or Open Cloud permissions."
        )
        return

    # 2. Tactical Currencies Strip
    credits_bal = profile.get("currency", 0)
    jigsaw_bal = profile.get("JigsawPieces", 0)
    keys_bal = profile.get("Keys", 0)

    cur_c1, cur_c2, cur_c3 = st.columns(3)
    with cur_c1:
        st.metric(
            label="CREDITS BALANCE",
            value=f"{credits_bal:,}",
            help="Liquid operational currency for store items and tier upgrades.",
        )
    with cur_c2:
        st.metric(
            label="JIGSAW PIECES",
            value=f"{jigsaw_bal:,}",
            help="Mastery currency earned through high-tier matches and Zombie Descent.",
        )
    with cur_c3:
        st.metric(
            label="OPERATIONAL KEYS",
            value=f"{keys_bal:,}",
            help="Encrypted keys used for unlocking armory vaults.",
        )

    st.space("small")

    # 3. Companion Sub-Navigation Tabs
    comp_tabs = st.tabs(
        [
            "📊 Career Telemetry",
            "🎯 Active Loadouts",
            "🧬 Operator Roster (15)",
            "🔧 Gunsmith Bench (56)",
            "⏱️ 6-Hour Shop Radar",
            "🎖️ Accolades & Loadout Exporter",
        ]
    )

    # TAB 1: CAREER TELEMETRY
    with comp_tabs[0]:
        career = profile.get("CareerStats", {})
        if career:
            kills = career.get("kills", 0)
            deaths = max(1, career.get("deaths", 1))
            kd_ratio = kills / deaths
            matches_played = career.get("matchesPlayed", 0)
            matches_won = career.get("matchesWon", 0)
            win_rate = (matches_won / max(1, matches_played)) * 100
            assists = career.get("assists", 0)
            damage = career.get("damageDealt", 0)
            bounty = career.get("bounty", 1000)

            st.markdown("#### Operational Combat Record")
            stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)
            stat_c1.metric("CONFIRMED KILLS", f"{kills:,}")
            stat_c2.metric("K / D RATIO", f"{kd_ratio:.2f}")
            stat_c3.metric("VICTORY RATE", f"{win_rate:.1f}%", f"{matches_won} Wins")
            stat_c4.metric("TACTICAL ASSISTS", f"{assists:,}")

            stat_c5, stat_c6, stat_c7, stat_c8 = st.columns(4)
            stat_c5.metric("TOTAL DAMAGE DEALT", f"{damage:,}")
            stat_c6.metric("TOTAL MATCHES", f"{matches_played:,}")
            stat_c7.metric("ACTIVE BOUNTY", f"${bounty:,}")
            stat_c8.metric(
                "COMBAT TIME", f"{career.get('totalMatchSeconds', 0) // 60:,} Min"
            )
        else:
            st.info("No recorded career matches yet.")

    # TAB 2: ACTIVE LOADOUTS
    with comp_tabs[1]:
        st.markdown("#### Primary Battle Loadouts")
        st.caption(
            "Tri-slot tactical configurations synchronized with your in-game profile."
        )
        loadouts = profile.get("PlayerLoadouts", [])
        if loadouts:
            l_tabs = st.tabs([f"Loadout #{i+1}" for i in range(len(loadouts))])
            for idx, l_tab in enumerate(l_tabs):
                with l_tab:
                    lo = loadouts[idx]
                    op_data = lo.get("Operator", {})
                    main_w = lo.get("Main", {})
                    sec_w = lo.get("Secondary", {})
                    sp1 = lo.get("Special1", {})
                    sp2 = lo.get("Special2", {})

                    l_col1, l_col2, l_col3, l_col4 = st.columns(4)
                    with l_col1:
                        st.markdown("**OPERATIVE ARCHETYPE**")
                        st.success(
                            f"🧬 {op_data.get('TitleName', 'Operator')} ({op_data.get('id', 'N/A')})"
                        )
                    with l_col2:
                        st.markdown("**PRIMARY FIREARM**")
                        st.info(f"🔫 {main_w.get('id', 'Empty')}")
                    with l_col3:
                        st.markdown("**SECONDARY WEAPON**")
                        st.warning(f"🗡️ {sec_w.get('id', 'Empty')}")
                    with l_col4:
                        st.markdown("**TACTICAL SPECIALS**")
                        st.code(
                            f"1: {sp1.get('id', 'Empty')}\n2: {sp2.get('id', 'Empty')}"
                        )
        else:
            st.info("No loadout slots populated.")

    # TAB 3: OPERATOR ROSTER
    with comp_tabs[2]:
        st.markdown("#### Authored Operative Roster")
        st.caption(
            "15 biologically distinct operatives across the Mortals and Monsters divisions."
        )

        all_ops = operators_catalog.get("operators", [])
        player_levels = profile.get("OperatorLevels", {})

        # Categorize
        mortals = [op for op in all_ops if op.get("category") == "MORTALS"]
        monsters = [op for op in all_ops if op.get("category") == "MONSTERS"]

        st.markdown("##### 🎖️ Division: MORTALS (Military, Mercenary & Martial)")
        m_cols = st.columns(3)
        for i, op in enumerate(mortals):
            op_id = op.get("id", "")
            title = op.get("titleName", op_id)
            hp = op.get("hp", 4000)
            hp_per_lvl = op.get("hpPerLevel", 100)
            user_lvl = player_levels.get(op_id, 0)
            maxed = user_lvl >= 10

            with m_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid {'#76F3FF' if maxed else 'rgba(255,255,255,0.1)'};border-radius:10px;padding:14px;margin-bottom:14px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div style="font-size:16px;font-weight:800;color:#F4F2EB;">{title}</div>
                            <span style="font-size:11px;font-weight:700;color:{'#76F3FF' if maxed else '#AEB4BC'};background:rgba(255,255,255,0.05);padding:2px 6px;border-radius:4px;">
                                {'★ MAX RANK' if maxed else f'LVL {user_lvl}/10'}
                            </span>
                        </div>
                        <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">ID: <code>{op_id}</code></div>
                        <div style="font-size:13px;color:#76F3FF;margin-top:6px;font-weight:700;">Base HP: {hp:,} <span style="color:#AEB4BC;font-size:11px;font-weight:400;">(+{hp_per_lvl}/lvl)</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("##### 🧬 Division: MONSTERS (Biological, Mutated & Apex)")
        n_cols = st.columns(3)
        for i, op in enumerate(monsters):
            op_id = op.get("id", "")
            title = op.get("titleName", op_id)
            hp = op.get("hp", 5000)
            hp_per_lvl = op.get("hpPerLevel", 150)
            user_lvl = player_levels.get(op_id, 0)
            maxed = user_lvl >= 10

            with n_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid {'#FF764D' if maxed else 'rgba(255,255,255,0.1)'};border-radius:10px;padding:14px;margin-bottom:14px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div style="font-size:16px;font-weight:800;color:#F4F2EB;">{title}</div>
                            <span style="font-size:11px;font-weight:700;color:{'#FF764D' if maxed else '#AEB4BC'};background:rgba(255,255,255,0.05);padding:2px 6px;border-radius:4px;">
                                {'★ APEX TIER' if maxed else f'LVL {user_lvl}/10'}
                            </span>
                        </div>
                        <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">ID: <code>{op_id}</code></div>
                        <div style="font-size:13px;color:#FF764D;margin-top:6px;font-weight:700;">Base HP: {hp:,} <span style="color:#AEB4BC;font-size:11px;font-weight:400;">(+{hp_per_lvl}/lvl)</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # TAB 4: GUNSMITH BENCH
    with comp_tabs[3]:
        st.markdown("#### Authored Gunsmith & Ballistics Laboratory")
        st.caption(
            "Inspect live combat telemetry, cadence, and upgrade curves across all 56 authored weapons."
        )

        all_weapons = sorted([k for k in weapons_catalog.keys() if not k.startswith("__")])
        if all_weapons:
            # Category filter
            categories = sorted(
                list(
                    {
                        weapons_catalog[w].get("Subcategory")
                        or weapons_catalog[w].get("BaseCategory")
                        or weapons_catalog[w].get("Slot", "Main")
                        for w in all_weapons
                    }
                )
            )
            col_filter1, col_filter2 = st.columns([2, 3])
            with col_filter1:
                sel_cat = st.selectbox(
                    "Weapon Category",
                    ["ALL"] + categories,
                    index=0,
                    key="comp_cat_sel",
                )
            with col_filter2:
                filtered_weapons = (
                    all_weapons
                    if sel_cat == "ALL"
                    else [
                        w
                        for w in all_weapons
                        if (
                            weapons_catalog[w].get("Subcategory")
                            or weapons_catalog[w].get("BaseCategory")
                            or weapons_catalog[w].get("Slot", "Main")
                        )
                        == sel_cat
                    ]
                )
                sel_weapon = st.selectbox(
                    "Select Firearm / Equipment",
                    filtered_weapons,
                    index=0,
                    key="comp_weap_sel",
                )

            weap_spec = weapons_catalog.get(sel_weapon, {})
            if weap_spec:
                hit_dmg = weap_spec.get("HitDamage", 300)
                cooldown = weap_spec.get("ShotCooldown", 0.1)
                rpm = int(60 / cooldown) if cooldown > 0 else 0
                ammo_cap = weap_spec.get("AmmoCapacity", 30)
                reload_t = weap_spec.get("ReloadTime", 2.0)
                aim_cone = weap_spec.get("AimConeAngleDeg", 60)
                max_dist = weap_spec.get("MaxDistance", 100)
                melee_dmg = weap_spec.get("MeleeDamage", 1500)

                stat_w1, stat_w2, stat_w3, stat_w4 = st.columns(4)
                stat_w1.metric("BASE HIT DAMAGE", f"{hit_dmg:,}")
                stat_w2.metric("CYCLIC CADENCE", f"{rpm} RPM", f"{cooldown}s per shot")
                stat_w3.metric("MAGAZINE CAPACITY", f"{ammo_cap} Rounds")
                stat_w4.metric("RELOAD DOWNTIME", f"{reload_t}s")

                stat_w5, stat_w6, stat_w7, stat_w8 = st.columns(4)
                stat_w5.metric("AIM ACQUISITION CONE", f"{aim_cone}°")
                stat_w6.metric("EFFECTIVE DISTANCE", f"{max_dist} Studs")
                stat_w7.metric("MELEE BASH DAMAGE", f"{melee_dmg:,}")
                stat_w8.metric(
                    "KIND / SLOT",
                    f"{weap_spec.get('Kind', 'Firearm')} ({weap_spec.get('Slot', 'Main')})",
                )

                st.markdown("##### 10-Tier Upgrade Cost & TTK Projection")
                upg_lvl = st.slider(
                    "Target Upgrade Level", min_value=0, max_value=10, value=5, key="comp_upg_lvl"
                )
                req_credits = weap_spec.get(f"level{upg_lvl}Currency", upg_lvl * 250)
                req_jigsaw = weap_spec.get(f"level{upg_lvl}Jigsaw", upg_lvl * 3)
                dmg_boost_pct = upg_lvl * weap_spec.get("DamagePerLevelPercent", 5)
                projected_dmg = hit_dmg * (1 + (dmg_boost_pct / 100.0))

                uc1, uc2, uc3 = st.columns(3)
                uc1.metric("UPGRADE CREDITS", f"{req_credits:,}")
                uc2.metric("UPGRADE JIGSAW", f"{req_jigsaw:,}")
                uc3.metric(
                    "PROJECTED HIT DAMAGE",
                    f"{projected_dmg:.1f}",
                    f"+{dmg_boost_pct}% Lethality",
                )

    # TAB 5: 6-HOUR SHOP ROTATION RADAR
    with comp_tabs[4]:
        st.markdown("#### Deterministic 6-Hour Shop Rotation Radar")
        st.caption(
            "Every 6 hours, your personalized armory rotation regenerates deterministically based on your Roblox User ID."
        )

        try:
            uid_num = int(user_id) if user_id.isdigit() else 2725352577
        except Exception:
            uid_num = 2725352577

        current_window = int(time.time() // 21600)
        seed = _hash_seed(uid_num, current_window)
        hours_remaining = int(6 - ((time.time() % 21600) / 3600))
        minutes_remaining = int(60 - ((time.time() % 3600) / 60))

        st.info(
            f"Active Shop Window: #{current_window} &bull; Resets in approximately **{hours_remaining}h {minutes_remaining}m**"
        )

        all_w_keys = sorted([k for k in weapons_catalog.keys() if not k.startswith("__")])
        if all_w_keys:
            feat_idx = seed % len(all_w_keys)
            reg1_idx = (seed + 7) % len(all_w_keys)
            reg2_idx = (seed + 13) % len(all_w_keys)
            reg3_idx = (seed + 29) % len(all_w_keys)

            sh_c1, sh_c2, sh_c3, sh_c4 = st.columns(4)
            with sh_c1:
                st.markdown(
                    f"""
                    <div style="background:rgba(118,243,255,0.06);border:2px solid #76F3FF;border-radius:12px;padding:16px;">
                        <span style="background:#76F3FF;color:#090A0C;font-weight:900;font-size:10px;padding:2px 8px;border-radius:4px;">FEATURED DEAL</span>
                        <div style="font-size:18px;font-weight:800;color:#F4F2EB;margin-top:8px;">{all_w_keys[feat_idx]}</div>
                        <div style="font-size:12px;color:#76F3FF;margin-top:4px;">35% OFF CREDITS</div>
                        <div style="font-size:11px;color:#AEB4BC;margin-top:8px;">In-Game Credits Store</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with sh_c2:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:16px;">
                        <span style="background:rgba(255,255,255,0.1);color:#AEB4BC;font-weight:700;font-size:10px;padding:2px 8px;border-radius:4px;">SLOT 02</span>
                        <div style="font-size:18px;font-weight:800;color:#F4F2EB;margin-top:8px;">{all_w_keys[reg1_idx]}</div>
                        <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">STANDARD OFFER</div>
                        <div style="font-size:11px;color:#AEB4BC;margin-top:8px;">In-Game Credits Store</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with sh_c3:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:16px;">
                        <span style="background:rgba(255,255,255,0.1);color:#AEB4BC;font-weight:700;font-size:10px;padding:2px 8px;border-radius:4px;">SLOT 03</span>
                        <div style="font-size:18px;font-weight:800;color:#F4F2EB;margin-top:8px;">{all_w_keys[reg2_idx]}</div>
                        <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">STANDARD OFFER</div>
                        <div style="font-size:11px;color:#AEB4BC;margin-top:8px;">In-Game Credits Store</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with sh_c4:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:16px;">
                        <span style="background:rgba(255,255,255,0.1);color:#AEB4BC;font-weight:700;font-size:10px;padding:2px 8px;border-radius:4px;">SLOT 04</span>
                        <div style="font-size:18px;font-weight:800;color:#F4F2EB;margin-top:8px;">{all_w_keys[reg3_idx]}</div>
                        <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">STANDARD OFFER</div>
                        <div style="font-size:11px;color:#AEB4BC;margin-top:8px;">In-Game Credits Store</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # TAB 6: ACCOLADES & LOADOUT EXPORTER
    with comp_tabs[5]:
        st.markdown("#### Career Accolades & Tactical Badges")
        st.caption("Milestone medals unlocked via live gameplay telemetry.")

        career = profile.get("CareerStats", {})
        kills = career.get("kills", 0)
        deaths = max(1, career.get("deaths", 1))
        kd = kills / deaths
        wallet = profile.get("PlayerCurrencies", {})
        credits = wallet.get("credits", 0)
        jigsaw = wallet.get("jigsaw", 0)
        keys = wallet.get("keys", 0)

        medals = [
            ("APEX ELIMINATOR", f"{kills:,} Kills (Req: 750)", kills >= 750, "#76F3FF", "★ GOLD TIER"),
            ("COMBAT EFFICIENCY", f"{kd:.2f} K/D Ratio (Req: 2.50)", kd >= 2.5, "#8CFFAA", "★ LETHAL"),
            ("SYNDICATE FINANCIER", f"${credits:,} Credits (Req: 10M)", credits >= 10000000, "#FFB84D", "★ HIGH ROLLER"),
            ("JIGSAW CRYPTOGRAPHER", f"{jigsaw:,} Jigsaw (Req: 5,000)", jigsaw >= 5000, "#76F3FF", "★ MASTER"),
            ("VAULT KEYMASTER", f"{keys} Keys (Req: 50)", keys >= 50, "#FF764D", "★ ANCIENT"),
            ("DESCENT CONQUEROR", "Floor 10 Extraction", False, "#AEB4BC", "IN PROGRESS"),
        ]

        m_cols = st.columns(3)
        for i, (m_title, m_desc, unlocked, color, tier) in enumerate(medals):
            with m_cols[i % 3]:
                st.markdown(
                    f'''
                    <div style="background:rgba(255,255,255,0.02);border:1px solid {'rgba(118,243,255,0.4)' if unlocked else 'rgba(255,255,255,0.06)'};border-top:3px solid {color if unlocked else 'rgba(255,255,255,0.1)'};border-radius:10px;padding:14px;margin-bottom:12px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:14px;font-weight:900;color:#F4F2EB;">{m_title}</span>
                            <span style="font-size:9px;font-weight:800;color:{color if unlocked else '#AEB4BC'};background:rgba(255,255,255,0.05);padding:2px 6px;border-radius:4px;">{tier}</span>
                        </div>
                        <div style="font-size:12px;color:{'#D9DCE1' if unlocked else '#71767E'};margin-top:6px;">{m_desc}</div>
                        <div style="font-size:10px;font-weight:800;color:{'#8CFFAA' if unlocked else '#AEB4BC'};margin-top:8px;">
                            {'[UNLOCKED & VERIFIED]' if unlocked else '[LOCKED]'}
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )

        st.markdown("#### Shareable Loadout String Codes")
        st.caption("Generate copyable build strings to share tri-slot configurations with teammates.")
        
        loadouts = profile.get("PlayerLoadouts", [])
        if loadouts:
            for i, lo in enumerate(loadouts, 1):
                op_name = lo.get("Operator", {}).get("TitleName", "SOLDIER")
                pw = lo.get("Main", {}).get("id", "M416")
                sw = lo.get("Secondary", {}).get("id", "Katana")
                s1 = lo.get("Special1", {}).get("id", "C4")
                s2 = lo.get("Special2", {}).get("id", "Flashbang")
                code_str = f"BBUILDS-V1:OP_{op_name.upper()}|PRI_{pw.upper()}|SEC_{sw.upper()}|SP1_{s1.upper()}|SP2_{s2.upper()}"
                st.text_input(f"Loadout #{i} ({op_name} &bull; {pw})", value=code_str, key=f"code_lo_{i}", disabled=True)
        else:
            st.info("No loadout profiles found to export.")

        st.markdown("#### Quick Launch Direct Connect")
        st.markdown(
            f'''
            <div style="background:rgba(118,243,255,0.03);border:1px solid rgba(118,243,255,0.2);border-radius:10px;padding:16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                <div>
                    <div style="font-size:16px;font-weight:900;color:#F4F2EB;">LAUNCH BATTLE BUILDS ON ROBLOX</div>
                    <div style="font-size:12px;color:#AEB4BC;">Universe ID: 4046514670 &bull; Direct deep link to production arena.</div>
                </div>
                <a href="https://www.roblox.com/games/4046514670" target="_blank" style="background:#76F3FF;color:#090A0C;font-weight:900;font-size:13px;padding:10px 20px;border-radius:8px;text-decoration:none;letter-spacing:0.04em;">
                    OPEN IN ROBLOX &rarr;
                </a>
            </div>
            ''',
            unsafe_allow_html=True,
        )
