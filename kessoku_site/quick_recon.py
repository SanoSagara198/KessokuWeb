from __future__ import annotations

from typing import Any
import streamlit as st

from kessoku_site.content import OPERATORS, WEAPONS
from kessoku_site.vehicles import HEIST_VEHICLES


def render_quick_recon_terminal(accent: str = "#76F3FF") -> None:
    """Render the Studio Quick Recon & Intelligence Terminal."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:4px solid {accent};border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <div style="font-size:18px;font-weight:900;color:#F4F2EB;letter-spacing:0.04em;">KESSOKU INTELLIGENCE TERMINAL &bull; TACTICAL RECON</div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:2px;">
                        Instant tactical lookup across both live simulation worlds: operatives, weapons, and city vehicles.
                    </div>
                </div>
                <div style="font-size:11px;font-family:monospace;color:{accent};background:rgba(255,255,255,0.04);padding:4px 10px;border-radius:6px;border:1px solid rgba(255,255,255,0.08);">
                    SYSTEM INDEX: 15 OPERATIVES &bull; 56 WEAPONS &bull; 35 VEHICLES
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_choice = st.segmented_control("Recon Dossier Channel", ["OPERATIVES (15)", "CORE FIREARMS (6)", "PURSUIT VEHICLES (15)"], default="OPERATIVES (15)", width="stretch") or "OPERATIVES (15)"

    if "OPERATIVES" in t_choice:
        op_names = [f"{op.name} ({op.division} &bull; {op.role})" for op in OPERATORS]
        sel_idx_op = st.selectbox("Select Operative Dossier", range(len(OPERATORS)), format_func=lambda i: op_names[i], key="qr_op")
        op = OPERATORS[sel_idx_op]
        is_monster = op.division == "MONSTERS"
        c_border = "#FF764D" if is_monster else "#76F3FF"
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-left:4px solid {c_border};border-radius:8px;padding:16px;margin-top:10px;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;">
                    <span style="font-size:20px;font-weight:900;color:#F4F2EB;">{op.name}</span>
                    <span style="font-size:11px;font-weight:800;color:{c_border};background:rgba(255,255,255,0.05);padding:2px 8px;border-radius:4px;border:1px solid {c_border};">{op.division}</span>
                </div>
                <div style="font-size:13px;font-weight:700;color:#AEB4BC;margin-top:2px;">{op.role} &bull; Dodge Technique: <strong style="color:#F4F2EB;">{op.dodge_ability}</strong></div>
                <div style="margin-top:8px;font-size:14px;color:#F4F2EB;">Base Health: <strong style="color:{c_border};">{op.base_hp:,} HP</strong> (+{op.hp_per_level:,}/lvl)</div>
                <div style="font-size:13px;color:#AEB4BC;margin-top:6px;line-height:1.5;">{op.description}</div>
                <div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;">
                    {"".join(f'<span style="background:rgba(255,255,255,0.04);color:#D9DCE1;font-size:11px;padding:2px 8px;border-radius:4px;border:1px solid rgba(255,255,255,0.08);">{t}</span>' for t in op.tactical_traits)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif "FIREARMS" in t_choice:
        w_names = [f"{w.name} ({w.role} &bull; {w.caliber})" for w in WEAPONS]
        sel_idx_w = st.selectbox("Select Ballistic Spec", range(len(WEAPONS)), format_func=lambda i: w_names[i], key="qr_w")
        w = WEAPONS[sel_idx_w]
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-left:4px solid #76F3FF;border-radius:8px;padding:16px;margin-top:10px;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;">
                    <span style="font-size:20px;font-weight:900;color:#F4F2EB;">{w.name}</span>
                    <span style="font-size:11px;font-weight:800;color:#76F3FF;background:rgba(255,255,255,0.05);padding:2px 8px;border-radius:4px;border:1px solid #76F3FF;">{w.role}</span>
                </div>
                <div style="margin-top:10px;display:grid;grid-template-columns:repeat(auto-fit, minmax(130px, 1fr));gap:8px;">
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">CALIBER</span><div style="font-size:14px;font-weight:800;color:#F4F2EB;">{w.caliber}</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">CYCLIC RATE</span><div style="font-size:14px;font-weight:800;color:#F4F2EB;">{w.rpm} RPM</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">BASE DAMAGE</span><div style="font-size:14px;font-weight:800;color:#76F3FF;">{w.base_damage:.0f} HP</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">MAG CAPACITY</span><div style="font-size:14px;font-weight:800;color:#F4F2EB;">{w.mag_size} Rnds</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">RELOAD SPEED</span><div style="font-size:14px;font-weight:800;color:#F4F2EB;">{w.reload_sec}s</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">HEADSHOT MULT</span><div style="font-size:14px;font-weight:800;color:#FF764D;">{w.head_mult}x</div></div>
                </div>
                <div style="font-size:13px;color:#AEB4BC;margin-top:10px;line-height:1.5;">{w.description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        v_names = [f"{v.name} ({v.category})" for v in HEIST_VEHICLES]
        sel_idx_v = st.selectbox("Select Vehicle Blueprint", range(len(HEIST_VEHICLES)), format_func=lambda i: v_names[i], key="qr_v")
        v = HEIST_VEHICLES[sel_idx_v]
        v_color = "#FF764D" if "SWAT" in v.category or "LAW" in v.category else "#76F3FF"
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-left:4px solid {v_color};border-radius:8px;padding:16px;margin-top:10px;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;">
                    <span style="font-size:20px;font-weight:900;color:#F4F2EB;">{v.name}</span>
                    <span style="font-size:11px;font-weight:800;color:{v_color};background:rgba(255,255,255,0.05);padding:2px 8px;border-radius:4px;border:1px solid {v_color};">{v.category}</span>
                </div>
                <div style="font-size:13px;font-weight:700;color:#AEB4BC;margin-top:2px;">{v.role} &bull; Capacity: <strong style="color:#F4F2EB;">{v.seats} Seats</strong></div>
                <div style="margin-top:10px;display:grid;grid-template-columns:repeat(auto-fit, minmax(130px, 1fr));gap:8px;">
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">SPEED CLASS</span><div style="font-size:13px;font-weight:800;color:#F4F2EB;">{v.speed_tier}</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">DURABILITY</span><div style="font-size:13px;font-weight:800;color:#F4F2EB;">{v.durability}</div></div>
                    <div style="background:rgba(255,255,255,0.02);padding:8px;border-radius:4px;"><span style="font-size:10px;color:#AEB4BC;">MASS CLASS</span><div style="font-size:13px;font-weight:800;color:#F4F2EB;">{v.mass_class}</div></div>
                </div>
                <div style="font-size:13px;color:#AEB4BC;margin-top:10px;line-height:1.5;">{v.description}</div>
                <div style="margin-top:10px;display:flex;gap:4px;flex-wrap:wrap;">
                    {"".join(f'<span style="background:rgba(255,255,255,0.04);color:#D9DCE1;font-size:10px;padding:2px 6px;border-radius:4px;border:1px solid rgba(255,255,255,0.08);">{feat}</span>' for feat in v.features)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
