from __future__ import annotations

from typing import Any
import plotly.graph_objects as go
import streamlit as st

from kessoku_site.vehicles import HEIST_VEHICLES, VehicleSpec


DISPATCH_LOGS = (
    {
        "code": "10-33",
        "badge": "URGENT PURSUIT",
        "unit": "UNIT 4-CHARLIE (INTERCEPTOR)",
        "district": "CENTRAL FINANCIAL BOULEVARD",
        "time": "04:42:19 UTC",
        "audio_blip": "SQUELCH_HIGH",
        "message": "Suspect vehicle blacked-out sports coupe heading westbound at 115 MPH. Cleared intersection on 4th & Broad. Spike strip deployment requested at Highway 101 offramp.",
        "status": "PURSUIT IN PROGRESS",
        "accent": "#FF764D",
    },
    {
        "code": "10-99",
        "badge": "VAULT BREACH",
        "unit": "DISPATCH & NCPD CENTRAL",
        "district": "NEWCITY COMMERCIAL BANK - METRO SECTOR",
        "time": "04:39:05 UTC",
        "audio_blip": "SQUELCH_ALERT",
        "message": "Silent seismic alarm tripped in subterranean bullion vault. Heavy thermal lance signatures detected. Air-1 airborne with FLIR cameras; SWAT Bearcat mobilized.",
        "status": "FORTIFIED PERIMETER",
        "accent": "#FF5252",
    },
    {
        "code": "10-85",
        "badge": "SWAT DEPLOY",
        "unit": "SWAT SIERRA-9 (LENCO BEARCAT)",
        "district": "DOCKLANDS WAREHOUSE 14",
        "time": "04:31:40 UTC",
        "audio_blip": "SQUELCH_MID",
        "message": "Perimeter breach established. Heavy barricades breached with ramming prow. 8 tactical operatives moving in CQB formation. Automatic gunfire reported inside.",
        "status": "CONTAINMENT LIVE",
        "accent": "#76F3FF",
    },
    {
        "code": "10-54",
        "badge": "ROADBLOCK BREACH",
        "unit": "SHERIFF PATROL 2-BRAVO",
        "district": "NORTH BRIDGE SUSPENSION TOLL",
        "time": "04:22:12 UTC",
        "audio_blip": "SQUELCH_LOW",
        "message": "Suspect armored hauler smashed through cruiser roadblock at lane 3. PIT maneuver ineffective due to heavy gross mass. En route toward mountain bypass.",
        "status": "SECONDARY CORDON",
        "accent": "#FFB84D",
    },
    {
        "code": "10-21",
        "badge": "SURVEILLANCE",
        "unit": "AIR-1 FOXTROT (HELICOPTER)",
        "district": "FINANCIAL DISTRICT ROOFTOPS",
        "time": "04:14:58 UTC",
        "audio_blip": "SQUELCH_LOW",
        "message": "Visual contact maintained on rooftop escape team. Suspects ziplining to adjacent parking structure. Ground patrol units converging on lower exits.",
        "status": "SURVEILLANCE LOCKED",
        "accent": "#8CFFAA",
    },
)


def render_dispatch_scanner(accent: str) -> None:
    """Render the NCPD Tactical Radio Dispatch Scanner & Live Police Transcripts."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,118,77,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <div style="font-size:20px;font-weight:900;color:#FF764D;letter-spacing:0.02em;">NCPD TACTICAL DISPATCH: LIVE RADIO SCANNER</div>
                    <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                        Interception audio transcripts and emergency tactical calls across NewCity metropolitan grid.
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:6px;background:rgba(255,118,77,0.1);padding:6px 12px;border-radius:999px;border:1px solid rgba(255,118,77,0.3);">
                    <span style="width:8px;height:8px;border-radius:50%;background:#FF764D;display:inline-block;animation:k-pulse 1.4s infinite;"></span>
                    <span style="font-size:11px;font-weight:800;color:#FF764D;letter-spacing:0.08em;">SCANNER ONLINE &bull; 460.125 MHz</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filter_choice = st.segmented_control("Incident Filter", ["ALL INCIDENTS (5)", "10-33 (PURSUIT)", "10-99 (VAULT)", "10-85 (SWAT)", "10-54 (ROADBLOCK)"], default="ALL INCIDENTS (5)", width="stretch") or "ALL INCIDENTS (5)"

    filtered_logs = DISPATCH_LOGS
    if "10-33" in filter_choice:
        filtered_logs = [log for log in DISPATCH_LOGS if log["code"] == "10-33"]
    elif "10-99" in filter_choice:
        filtered_logs = [log for log in DISPATCH_LOGS if log["code"] == "10-99"]
    elif "10-85" in filter_choice:
        filtered_logs = [log for log in DISPATCH_LOGS if log["code"] == "10-85"]
    elif "10-54" in filter_choice:
        filtered_logs = [log for log in DISPATCH_LOGS if log["code"] == "10-54"]

    for item in filtered_logs:
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:4px solid {item['accent']};border-radius:8px;padding:14px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px;">
                    <div>
                        <span style="font-size:11px;font-weight:900;color:{item['accent']};letter-spacing:0.08em;">[{item['code']}] {item['badge']}</span>
                        <span style="font-size:13px;font-weight:800;color:#F4F2EB;margin-left:8px;">{item['unit']}</span>
                    </div>
                    <div style="font-size:11px;color:#AEB4BC;font-family:monospace;">{item['district']} &bull; {item['time']}</div>
                </div>
                <div style="font-size:13px;color:#D9DCE1;margin-top:8px;line-height:1.5;font-family:monospace;background:rgba(0,0,0,0.25);padding:8px 12px;border-radius:6px;border:1px solid rgba(255,255,255,0.04);">
                    &gt; "{item['message']}"
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;">
                    <span style="font-size:10px;font-weight:800;color:{item['accent']};letter-spacing:0.06em;">STATUS: {item['status']}</span>
                    <span style="font-size:10px;color:#AEB4BC;">NCPD ENCRYPTED RADIO COMM</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_vehicle_comparison(accent: str) -> None:
    """Render side-by-side vehicle pursuit & intercept comparison."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(118,243,255,0.3);border-radius:12px;padding:20px;margin-top:20px;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:900;color:#76F3FF;letter-spacing:0.02em;">VEHICLE PURSUIT MATRIX: INTERCEPT COMPARISON</div>
            <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                Evaluate pursuit dynamics, ramming momentum, and ballistic resistance between any two fleet vehicles.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    car_names = [v.name for v in HEIST_VEHICLES]
    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        sel_a = st.selectbox("Vehicle Alpha (Pursuit / Intercept)", car_names, index=0, key="car_a")
        car_a = next(v for v in HEIST_VEHICLES if v.name == sel_a)
    with col_b:
        sel_b = st.selectbox("Vehicle Bravo (Target / Getaway)", car_names, index=1 if len(car_names) > 1 else 0, key="car_b")
        car_b = next(v for v in HEIST_VEHICLES if v.name == sel_b)

    # Score attributes (1-100 scale)
    def get_stats(car: VehicleSpec) -> tuple[int, int, int, int]:
        # Speed, Mass, Armor, Capacity
        is_hyper = "SUPER" in car.category
        is_swat = "SWAT" in car.name or "Bearcat" in car.name
        is_law = "LAW" in car.category
        is_heavy = "Heavy" in car.mass_class or "Utility" in car.category
        
        speed = 95 if is_hyper else (82 if is_law else (55 if is_swat else (50 if is_heavy else 70)))
        mass = 98 if is_swat else (90 if is_heavy else (65 if is_law else (45 if is_hyper else 60)))
        armor = 95 if is_swat else (70 if is_law else (40 if is_hyper else 60))
        cap = min(100, car.seats * 12)
        return speed, mass, armor, cap

    spd_a, mass_a, arm_a, cap_a = get_stats(car_a)
    spd_b, mass_b, arm_b, cap_b = get_stats(car_b)

    fig = go.Figure()
    categories = ["Top Speed", "Ramming Mass", "Ballistic Armor", "Crew Capacity"]
    fig.add_trace(go.Scatterpolar(
        r=[spd_a, mass_a, arm_a, cap_a, spd_a],
        theta=categories + [categories[0]],
        fill="toself",
        name=car_a.name,
        line=dict(color="#76F3FF", width=2),
        fillcolor="rgba(118,243,255,0.2)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=[spd_b, mass_b, arm_b, cap_b, spd_b],
        theta=categories + [categories[0]],
        fill="toself",
        name=car_b.name,
        line=dict(color="#FF764D", width=2),
        fillcolor="rgba(255,118,77,0.2)",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.08)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=40, r=40, t=20, b=20),
        font=dict(color="#AEB4BC", size=11),
        legend=dict(orientation="h", y=-0.1, x=0.2),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    # Tactical intercept assessment
    if spd_a > spd_b and mass_a >= mass_b:
        verdict = f"<strong>{car_a.name}</strong> holds decisive pursuit intercept superiority. Higher top speed prevents getaway escape; superior mass ensures successful PIT maneuver."
    elif spd_b > spd_a:
        verdict = f"<strong>{car_b.name}</strong> has a significant straight-line velocity advantage. Intercept requires advance roadblock cordons or Air-1 air support."
    else:
        verdict = f"<strong>{car_a.name}</strong> and <strong>{car_b.name}</strong> are evenly matched in pursuit kinetics. Outcome will depend on urban cornering and alleyway navigation."

    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px;font-size:12px;color:#D9DCE1;text-align:center;">
            {verdict}
        </div>
        """,
        unsafe_allow_html=True,
    )
