from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from kessoku_site.auth import logout_user
from kessoku_site.roblox_api import fetch_player_profile, fetch_weapon_catalog, fetch_operator_catalog


def render_player_companion(user_info: dict[str, Any]) -> None:
    """Render the authenticated offline player companion dashboard."""
    user_id = str(user_info.get("user_id", ""))
    username = user_info.get("username", "Robloxian")
    display_name = user_info.get("display_name", username)
    avatar_url = user_info.get("avatar_url")
    is_demo = user_info.get("is_demo", False)

    # 1. Header Profile Banner
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.03);border:1px solid rgba(118,243,255,0.25);border-radius:14px;padding:20px;margin-bottom:24px;">
            <div style="display:flex;align-items:center;gap:18px;">
                <img src="{avatar_url or 'https://tr.rbxcdn.com/30DAY-AvatarHeadshot-placeholder/150/150/AvatarHeadshot/Webp/noFilter'}" style="width:72px;height:72px;border-radius:50%;border:2px solid #76F3FF;" />
                <div>
                    <div style="font-size:22px;font-weight:800;color:#F4F2EB;letter-spacing:0.02em;">{display_name}</div>
                    <div style="font-size:13px;color:#AEB4BC;font-family:monospace;">@{username} &bull; Roblox ID: {user_id}</div>
                    <div style="margin-top:4px;">
                        <span style="background:rgba(118,243,255,0.15);color:#76F3FF;border:1px solid rgba(118,243,255,0.4);border-radius:6px;padding:2px 8px;font-size:11px;font-weight:700;">
                            {'VERIFIED DEMO PROFILE' if is_demo else 'ROBLOX OAUTH 2.0 CONNECTED'}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn1, col_btn2 = st.columns([6, 1])
    with col_btn2:
        if st.button("Sign Out", key="comp_logout"):
            logout_user()

    # 2. Fetch live data from PlayerDataStore
    profile = fetch_player_profile(user_id)
    if not profile:
        st.warning(f"No DataStore profile found for User ID {user_id}. Join Battle Builds in Roblox to initialize your profile!")
        return

    # 3. Currency Strip
    credits_bal = profile.get("currency", 0)
    jigsaw_bal = profile.get("JigsawPieces", 0)
    keys_bal = profile.get("Keys", 0)

    cur_c1, cur_c2, cur_c3 = st.columns(3)
    with cur_c1:
        st.metric(label="CREDITS BALANCE", value=f"{credits_bal:,}")
    with cur_c2:
        st.metric(label="JIGSAW PIECES", value=f"{jigsaw_bal:,}")
    with cur_c3:
        st.metric(label="OPERATIONAL KEYS", value=f"{keys_bal:,}")

    st.divider()

    # 4. Career Performance
    career = profile.get("CareerStats", {})
    if career:
        st.markdown("### Career Performance Record")
        kills = career.get("kills", 0)
        deaths = max(1, career.get("deaths", 1))
        kd_ratio = kills / deaths
        matches_played = career.get("matchesPlayed", 0)
        matches_won = career.get("matchesWon", 0)
        win_rate = (matches_won / max(1, matches_played)) * 100

        stat_c1, stat_c2, stat_c3, stat_c4, stat_c5 = st.columns(5)
        stat_c1.metric("ELIMINATIONS", f"{kills:,}")
        stat_c2.metric("K/D RATIO", f"{kd_ratio:.2f}")
        stat_c3.metric("MATCHES WON", f"{matches_won} / {matches_played}")
        stat_c4.metric("WIN RATE", f"{win_rate:.1f}%")
        stat_c5.metric("TOTAL DAMAGE", f"{career.get('damageDealt', 0):,}")

    st.divider()

    # 5. Equipped Loadouts & Operator Roster
    st.markdown("### Equipped Battle Loadouts")
    loadouts = profile.get("PlayerLoadouts", [])
    if loadouts:
        loadout_tabs = st.tabs([f"Loadout #{i+1}" for i in range(len(loadouts))])
        for idx, tab in enumerate(loadout_tabs):
            with tab:
                lo = loadouts[idx]
                op_data = lo.get("Operator", {})
                main_weap = lo.get("Main", {})
                sec_weap = lo.get("Secondary", {})
                sp1 = lo.get("Special1", {})
                sp2 = lo.get("Special2", {})

                lc1, lc2, lc3, lc4 = st.columns(4)
                with lc1:
                    st.markdown("**OPERATOR**")
                    st.info(f"{op_data.get('TitleName', 'Operator')} ({op_data.get('id', 'N/A')})")
                with lc2:
                    st.markdown("**PRIMARY FIREARM**")
                    st.success(f"{main_weap.get('id', 'Empty')}")
                with lc3:
                    st.markdown("**SECONDARY**")
                    st.warning(f"{sec_weap.get('id', 'Empty')}")
                with lc4:
                    st.markdown("**TACTICAL SPECIALS**")
                    st.code(f"{sp1.get('id', 'Empty')} & {sp2.get('id', 'Empty')}")

    st.divider()

    # 6. Operator Mastery & Weapon Bench
    st.markdown("### Operator Roster & Mastery Levels")
    op_levels = profile.get("OperatorLevels", {})
    if op_levels:
        op_cols = st.columns(4)
        for i, (op_id, lvl) in enumerate(op_levels.items()):
            with op_cols[i % 4]:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px;margin-bottom:12px;">
                        <div style="font-size:12px;color:#AEB4BC;font-family:monospace;">{op_id}</div>
                        <div style="font-size:16px;font-weight:700;color:#F4F2EB;">LEVEL {lvl} / 10</div>
                        <div style="font-size:11px;color:#76F3FF;">{'★ MAX RANK' if lvl >= 10 else 'TRAINING'}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()

    # 7. Live Gunsmith Upgrade Calculator
    st.markdown("### Gunsmith Upgrade Calculator")
    st.caption("Calculate upgrade costs in Credits and Jigsaw pieces across the 10-level weapon curve.")

    weapons_catalog = fetch_weapon_catalog()
    if weapons_catalog:
        weapon_keys = sorted([k for k in weapons_catalog.keys() if not k.startswith("__")])
        selected_weap = st.selectbox("Select Authored Weapon", weapon_keys, index=0 if "AK-47" not in weapon_keys else weapon_keys.index("AK-47"))
        weap_data = weapons_catalog.get(selected_weap, {})

        if weap_data:
            target_level = st.slider("Target Upgrade Level", min_value=0, max_value=10, value=5)
            curr_cost = weap_data.get(f"level{target_level}Currency", target_level * 250)
            jig_cost = weap_data.get(f"level{target_level}Jigsaw", target_level * 3)
            base_dmg = weap_data.get("HitDamage", 300)
            bonus_pct = target_level * weap_data.get("DamagePerLevelPercent", 5)
            projected_dmg = base_dmg * (1 + bonus_pct / 100.0)

            c_calc1, c_calc2, c_calc3 = st.columns(3)
            c_calc1.metric("REQUIRED CREDITS", f"{curr_cost:,}")
            c_calc2.metric("REQUIRED JIGSAW", f"{jig_cost:,}")
            c_calc3.metric("PROJECTED HIT DAMAGE", f"{projected_dmg:.1f}", f"+{bonus_pct}%")
