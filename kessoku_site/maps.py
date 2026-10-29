from __future__ import annotations

from typing import Any
import plotly.graph_objects as go
import streamlit as st


BATTLEFIELDS = (
    {
        "id": "verdant_outpost",
        "name": "VERDANT OUTPOST",
        "type": "5V5 SQUAD ARENA",
        "scale": "MEDIUM (180 x 140 STUDS)",
        "tagline": "Overgrown industrial compound with bilateral trench sightlines and central fountain choke.",
        "description": "The primary competitive 5v5 battleground. Features high-visibility perimeter lanes, low concrete barricades for crouch-cover, and a contested central plaza where sightlines intersect.",
        "doctrine": "Establish crossfire angles across the central plaza. Use smoke deployables to traverse open trench lines without exposing flanks.",
        "recommended_weapons": ("M416 Rifle", "Barrett M82 Sniper", "SPAS-12 Shotgun", "Flashbang Grenade"),
        "key_callouts": (
            ("Alpha Spawn", "Protected courtyard with bilateral ramp exits"),
            ("Bravo Spawn", "Sub-station warehouse loading bay"),
            ("Mid Fountain", "Hard-cover perimeter with 360-degree crossfire risk"),
            ("Sniper Gantry", "Elevated single-ladder perch with dominant south corridor visibility"),
            ("Flank Trenches", "Depressed peripheral corridors shielding players from long-range sniper fire"),
        ),
        "accent": "#76F3FF",
        "poi_x": [20, 80, 50, 50, 15, 85],
        "poi_y": [50, 50, 50, 85, 20, 80],
        "poi_labels": ["Alpha Base", "Bravo Base", "Mid Fountain", "Sniper Gantry", "South Trench", "North Trench"],
        "poi_colors": ["#76F3FF", "#FF764D", "#FFB84D", "#8CFFAA", "#AEB4BC", "#AEB4BC"],
    },
    {
        "id": "rail_yard",
        "name": "DISTRICT 9 RAIL YARD",
        "type": "5V5 CQB ENCOUNTER",
        "scale": "COMPACT (130 x 110 STUDS)",
        "tagline": "Multi-tier shipping container maze and train cars built for high-tempo CQB ambushes.",
        "description": "An ultra-fast, close-quarters combat zone. Shipping containers create blind 90-degree corners where shotgun buckshot and high-RPM SMG sprays dominate engagement outcomes.",
        "doctrine": "Clear corners using combat roll slides. Avoid lingering inside open boxcars where bounce grenades inflict catastrophic squad wipe damage.",
        "recommended_weapons": ("Vector SMG", "Saiga-12 Automatic", "Katana Blade", "Frag Grenade"),
        "key_callouts": (
            ("Depot Gate", "Initial southern perimeter with container cover"),
            ("Locomotive Line", "Central train line dividing the map into two CQB quadrants"),
            ("Overhead Crane", "High-ground observation platform with narrow access gantry"),
            ("Boxcar Choke", "Interior train cars allowing stealth passage between lanes"),
            ("Container Alley", "Deadly point-blank shotgun engagement corridor"),
        ),
        "accent": "#FFB84D",
        "poi_x": [15, 85, 50, 50, 30, 70],
        "poi_y": [20, 80, 50, 80, 50, 50],
        "poi_labels": ["Depot Gate", "Terminal Gate", "Locomotive Mid", "Overhead Crane", "West Alley", "East Alley"],
        "poi_colors": ["#76F3FF", "#FF764D", "#FFB84D", "#8CFFAA", "#AEB4BC", "#AEB4BC"],
    },
    {
        "id": "descent_silo",
        "name": "SUBTERRANEAN SILO",
        "type": "10-FLOOR PVE & EXTRACTION",
        "scale": "VERTICAL DEEP GAUNTLET",
        "tagline": "Multi-level subterranean descent shaft with reinforced blast doors and hazardous drainage canals.",
        "description": "The staging facility for the Zombie Descent operation. Players descend through 10 progressively claustrophobic survival floors, managing ammo reserves and choke points.",
        "doctrine": "Anchor the heavy machine gun platform near blast door thresholds. Funnel swarms into gas-cleared kill zones.",
        "recommended_weapons": ("PKM LMG", "Minigun Prototype", "Claymore Mine", "Reinforced Shield"),
        "key_callouts": (
            ("Elevator Shaft", "Hydraulic central platform linking floor transitions"),
            ("Blast Bulkheads", "Reinforced doors with timed manual bypass switches"),
            ("Turbine Room", "High-noise generator hall with blind infected spawn vents"),
            ("Sewer Spillway", "Flooded drainage trench with movement slowdown penalties"),
            ("Apex Boss Arena", "Floors 5 and 10 circular extraction staging room"),
        ),
        "accent": "#FF5252",
        "poi_x": [50, 20, 80, 50, 50],
        "poi_y": [50, 50, 50, 20, 80],
        "poi_labels": ["Elevator Shaft", "West Bulkhead", "East Bulkhead", "Drainage Spillway", "Apex Arena"],
        "poi_colors": ["#FF5252", "#FF764D", "#FF764D", "#76F3FF", "#8CFFAA"],
    },
)


def render_battlefield_recon(accent: str) -> None:
    """Render the Interactive Battlefield Map Recon & Tactical Callouts module."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(118,243,255,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <div style="font-size:20px;font-weight:900;color:#76F3FF;letter-spacing:0.02em;">BATTLE BUILDS: BATTLEFIELD TACTICAL RECON & CALLOUTS</div>
                    <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                        Architectural dossiers, sightline corridors, and strategic callout blueprints across all authored combat zones.
                    </div>
                </div>
                <div style="font-size:11px;font-weight:800;color:#76F3FF;background:rgba(118,243,255,0.08);padding:6px 12px;border-radius:999px;border:1px solid rgba(118,243,255,0.25);">
                    3 OPERATIONAL ARENAS
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    map_names = [m["name"] for m in BATTLEFIELDS]
    sel_map_name = st.segmented_control("Select Battlefield Arena", map_names, default=map_names[0], width="stretch") or map_names[0]
    map_data = next(m for m in BATTLEFIELDS if m["name"] == sel_map_name)

    m_left, m_right = st.columns([1.1, 0.9], gap="large")
    with m_left:
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-left:4px solid {map_data['accent']};border-radius:10px;padding:18px;margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:18px;font-weight:900;color:#F4F2EB;">{map_data['name']}</span>
                    <span style="font-size:10px;font-weight:800;color:{map_data['accent']};background:rgba(255,255,255,0.05);padding:2px 8px;border-radius:4px;border:1px solid {map_data['accent']};">{map_data['type']}</span>
                </div>
                <div style="font-size:12px;color:#AEB4BC;margin-top:2px;font-weight:600;">Scale: {map_data['scale']}</div>
                <div style="font-size:13px;color:#F4F2EB;margin-top:10px;line-height:1.5;">{map_data['description']}</div>
                <div style="font-size:12px;color:#AEB4BC;margin-top:8px;line-height:1.4;">
                    <strong style="color:{map_data['accent']};">Tactical Doctrine:</strong> {map_data['doctrine']}
                </div>
                <div style="margin-top:12px;">
                    <div style="font-size:11px;font-weight:800;color:#D9DCE1;margin-bottom:4px;">OPTIMIZED ARMORY LOADOUT:</div>
                    <div style="display:flex;gap:6px;flex-wrap:wrap;">
                        {"".join(f'<span style="background:rgba(255,255,255,0.04);color:#F4F2EB;font-size:11px;padding:2px 8px;border-radius:4px;border:1px solid rgba(255,255,255,0.08);">{w}</span>' for w in map_data['recommended_weapons'])}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Tactical Callouts & Choke Points")
        for callout, note in map_data["key_callouts"]:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.015);border:1px solid rgba(255,255,255,0.05);border-radius:6px;padding:8px 12px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:12px;font-weight:800;color:{map_data['accent']};">{callout}</span>
                    <span style="font-size:11px;color:#AEB4BC;">{note}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with m_right:
        # Visual Blueprint Map using Plotly
        fig = go.Figure()

        # Background grid simulation
        fig.add_shape(
            type="rect",
            x0=0, y0=0, x1=100, y1=100,
            line=dict(color=map_data["accent"], width=2),
            fillcolor="rgba(10,14,20,0.85)",
        )

        # Crossfire lines
        fig.add_trace(go.Scatter(
            x=[map_data["poi_x"][0], map_data["poi_x"][1]],
            y=[map_data["poi_y"][0], map_data["poi_y"][1]],
            mode="lines",
            line=dict(color="rgba(255,255,255,0.15)", width=2, dash="dash"),
            hoverinfo="none",
            showlegend=False,
        ))

        # POI Callout points
        fig.add_trace(go.Scatter(
            x=map_data["poi_x"],
            y=map_data["poi_y"],
            mode="markers+text",
            text=map_data["poi_labels"],
            textposition="top center",
            textfont=dict(color="#F4F2EB", size=10, family="sans-serif"),
            marker=dict(
                size=14,
                color=map_data["poi_colors"],
                line=dict(color="rgba(255,255,255,0.8)", width=1.5),
                symbol="diamond",
            ),
            hoverinfo="text",
            showlegend=False,
        ))

        fig.update_layout(
            title=f"Tactical Blueprint: {map_data['name']}",
            height=430,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", range=[-5, 105], zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", range=[-5, 105], zeroline=False, showticklabels=False),
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
