from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st


CLUSTERS = (
    {"region": "US-EAST", "location": "N. Virginia", "tick": "60.0 Hz", "ping": "18 ms", "status": "OPTIMAL", "shards": 1420, "color": "#76F3FF"},
    {"region": "US-WEST", "location": "Oregon", "tick": "60.0 Hz", "ping": "26 ms", "status": "OPTIMAL", "shards": 980, "color": "#76F3FF"},
    {"region": "EU-CENTRAL", "location": "Frankfurt", "tick": "60.0 Hz", "ping": "34 ms", "status": "OPTIMAL", "shards": 1840, "color": "#76F3FF"},
    {"region": "SA-EAST", "location": "São Paulo", "tick": "60.0 Hz", "ping": "14 ms", "status": "OPTIMAL", "shards": 820, "color": "#8CFFAA"},
    {"region": "ASIA-PACIFIC", "location": "Tokyo", "tick": "60.0 Hz", "ping": "58 ms", "status": "NOMINAL", "shards": 1120, "color": "#FFB84D"},
)


def render_server_clusters_matrix(accent: str) -> None:
    """Render the Studio Global Server Cluster & Network Authority Matrix."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <div style="font-size:20px;font-weight:900;color:#F4F2EB;letter-spacing:0.02em;">GLOBAL SERVER CLUSTERS & PRODUCTION TOPOLOGY</div>
                    <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                        Fixed-rate authoritative game instances deployed across low-latency global edge locations.
                    </div>
                </div>
                <div style="font-size:12px;font-weight:800;color:#76F3FF;background:rgba(118,243,255,0.08);padding:6px 14px;border-radius:999px;border:1px solid rgba(118,243,255,0.25);">
                    ALL CLUSTERS OPERATIONAL &bull; 60Hz TICK
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(5, gap="small")
    for i, cluster in enumerate(CLUSTERS):
        with cols[i]:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-top:3px solid {cluster['color']};border-radius:8px;padding:14px;text-align:center;">
                    <div style="font-size:13px;font-weight:900;color:#F4F2EB;">{cluster['region']}</div>
                    <div style="font-size:11px;color:#AEB4BC;">{cluster['location']}</div>
                    <div style="font-size:22px;font-weight:900;color:{cluster['color']};margin:8px 0;">{cluster['ping']}</div>
                    <div style="font-size:11px;color:#D9DCE1;">Tick: <strong>{cluster['tick']}</strong></div>
                    <div style="font-size:10px;color:#AEB4BC;margin-top:2px;">{cluster['shards']} Active Shards</div>
                    <div style="margin-top:8px;font-size:9px;font-weight:800;color:{cluster['color']};background:rgba(255,255,255,0.04);padding:2px 6px;border-radius:4px;display:inline-block;">
                        {cluster['status']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Telemetry pipeline details
    st.markdown(
        """
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:18px;margin-top:16px;">
            <div style="font-size:14px;font-weight:800;color:#F4F2EB;margin-bottom:12px;">AUTHORITATIVE RECONCILIATION LIFECYCLE (16.6ms TICK STEP)</div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:12px;">
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:6px;border:1px solid rgba(255,255,255,0.05);">
                    <div style="font-size:11px;font-weight:800;color:#76F3FF;">01 / CLIENT INTENT</div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">Client samples WASD movement, dodge roll inputs, and trigger pulls. Zero outcome logic computed locally.</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:6px;border:1px solid rgba(255,255,255,0.05);">
                    <div style="font-size:11px;font-weight:800;color:#76F3FF;">02 / UDP PACKET BURST</div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">Input delta transmitted with sub-frame microsecond timestamp to regional authoritative server cluster.</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:6px;border:1px solid rgba(255,255,255,0.05);">
                    <div style="font-size:11px;font-weight:800;color:#FFB84D;">03 / LAG REWIND & RAYCAST</div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">Server rewinds target hitbox position to sender's exact viewframe using 250ms circular history buffer.</div>
                </div>
                <div style="background:rgba(255,255,255,0.02);padding:12px;border-radius:6px;border:1px solid rgba(255,255,255,0.05);">
                    <div style="font-size:11px;font-weight:800;color:#8CFFAA;">04 / STATE REPLICATION</div>
                    <div style="font-size:12px;color:#AEB4BC;margin-top:4px;">Verified hitscan damage, recoil bloom increment, and ragdoll velocity broadcast to all match participants.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
