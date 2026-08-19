from __future__ import annotations

from io import BytesIO

import altair as alt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
from PIL import Image, ImageDraw, ImageFilter

from .models import Metric, SkillCategory, WeaponSpec


def metric_radar(metrics: tuple[Metric, ...], accent: str) -> go.Figure:
    labels = [metric.label.upper() for metric in metrics]
    values = [metric.value for metric in metrics]
    labels.append(labels[0])
    values.append(values[0])
    fig = go.Figure(
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill="toself",
            line=dict(color=accent, width=2),
            fillcolor=_hex_to_rgba(accent, 0.18),
            hovertemplate="%{theta}: %{r}<extra></extra>",
        )
    )
    fig.update_layout(
        height=430,
        margin=dict(l=35, r=35, t=35, b=35),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#D8DADF", size=11),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor="rgba(255,255,255,.10)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,.10)"),
        ),
        showlegend=False,
    )
    return fig


def combat_pressure_figure(mode_key: str, intensity: int, posture: str, accent: str) -> go.Figure:
    time = np.arange(0, 61, 5)
    mode_multiplier = 0.82 if mode_key == "arena" else 1.12
    posture_multiplier = {"AGGRESSIVE": 1.18, "BALANCED": 1.0, "DEFENSIVE": 0.86}[posture]
    phase = np.sin(np.linspace(0, 3.4 * np.pi, len(time))) * 12
    base = 28 + intensity * 4.8
    pressure = np.clip((base + phase) * mode_multiplier * posture_multiplier, 0, 100)
    capability = np.clip(92 - np.cumsum(np.maximum(pressure - 56, 0)) * 0.08, 18, 100)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=pressure, mode="lines", name="PRESSURE", line=dict(color=accent, width=4), fill="tozeroy", fillcolor=_hex_to_rgba(accent, .12)))
    fig.add_trace(go.Scatter(x=time, y=capability, mode="lines", name="SQUAD CAPABILITY", line=dict(color="#F4F2EB", width=2, dash="dot")))
    fig.add_hrect(y0=78, y1=100, fillcolor="rgba(255,118,77,.07)", line_width=0, annotation_text="DECISION CRITICAL", annotation_position="top left")
    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=35, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        font=dict(color="#C8CCD2", size=11),
        xaxis=dict(title="OPERATION SECONDS", gridcolor="rgba(255,255,255,.07)", zeroline=False),
        yaxis=dict(range=[0, 100], title="TACTICAL LOAD", gridcolor="rgba(255,255,255,.07)", zeroline=False),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    return fig


def city_pursuit_figure(stage: int, accent: str) -> go.Figure:
    rng = np.random.default_rng(1977)
    road_count = 9
    roads = np.arange(road_count)
    player_path = np.array([[1, 7], [2, 7], [3, 7], [3, 6], [4, 6], [5, 6], [5, 5], [6, 5], [7, 5]])
    police_a = np.array([[8, 2], [7, 2], [6, 2], [6, 3], [6, 4], [6, 5]])
    police_b = np.array([[2, 1], [2, 2], [2, 3], [3, 3], [4, 3], [5, 3], [5, 4], [5, 5]])
    idx = max(1, min(stage, len(player_path) - 1))
    fig = go.Figure()
    for x in roads:
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=road_count - 1, line=dict(color="rgba(255,255,255,.075)", width=12))
    for y in roads:
        fig.add_shape(type="line", x0=0, y0=y, x1=road_count - 1, y1=y, line=dict(color="rgba(255,255,255,.075)", width=12))
    blocks = rng.uniform(0.2, 0.8, size=(18, 2)) * (road_count - 1)
    fig.add_trace(go.Scatter(x=blocks[:, 0], y=blocks[:, 1], mode="markers", marker=dict(size=8, color="rgba(255,255,255,.12)"), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=player_path[: idx + 1, 0], y=player_path[: idx + 1, 1], mode="lines+markers", line=dict(color=accent, width=4), marker=dict(size=8), name="TARGET"))
    fig.add_trace(go.Scatter(x=police_a[: min(idx + 1, len(police_a)), 0], y=police_a[: min(idx + 1, len(police_a)), 1], mode="lines+markers", line=dict(color="#66A8FF", width=3, dash="dot"), name="UNIT 12"))
    fig.add_trace(go.Scatter(x=police_b[: min(idx + 1, len(police_b)), 0], y=police_b[: min(idx + 1, len(police_b)), 1], mode="lines+markers", line=dict(color="#9DC5FF", width=3, dash="dot"), name="UNIT 21"))
    fig.update_layout(
        height=470,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        xaxis=dict(visible=False, range=[-0.4, road_count - .6]),
        yaxis=dict(visible=False, range=[-0.4, road_count - .6], scaleanchor="x"),
        legend=dict(orientation="h", y=1.03, font=dict(color="#B8BDC5", size=10), bgcolor="rgba(0,0,0,0)"),
        hovermode=False,
    )
    return fig


def city_deck(stage: int, accent: str) -> pdk.Deck:
    center_lat, center_lon = -31.42, -64.19
    delta = 0.00155
    blocks: list[dict[str, object]] = []
    rng = np.random.default_rng(42)
    for x in range(6):
        for y in range(6):
            west = center_lon + (x - 3) * delta
            south = center_lat + (y - 3) * delta
            inset = delta * .18
            tone = int(rng.integers(24, 58))
            blocks.append(
                {
                    "polygon": [
                        [west + inset, south + inset],
                        [west + delta - inset, south + inset],
                        [west + delta - inset, south + delta - inset],
                        [west + inset, south + delta - inset],
                    ],
                    "height": int(rng.integers(30, 155)),
                    "color": [tone, tone + 8, tone + 15, 210],
                }
            )
    target_route = [[center_lon - .0037, center_lat + .0036], [center_lon - .0017, center_lat + .0036], [center_lon - .0017, center_lat + .0018], [center_lon + .0015, center_lat + .0018], [center_lon + .0015, center_lat], [center_lon + .0032, center_lat]]
    police_route_a = [[center_lon + .0043, center_lat - .0035], [center_lon + .0029, center_lat - .0035], [center_lon + .0029, center_lat - .0002], [center_lon + .0015, center_lat]]
    police_route_b = [[center_lon - .0032, center_lat - .004], [center_lon - .0032, center_lat - .0018], [center_lon - .0002, center_lat - .0018], [center_lon - .0002, center_lat], [center_lon + .0015, center_lat]]
    route_index = max(1, min(stage, len(target_route) - 1))
    r, g, b = _hex_rgb(accent)
    layers = [
        pdk.Layer(
            "PolygonLayer",
            blocks,
            get_polygon="polygon",
            get_elevation="height",
            get_fill_color="color",
            get_line_color=[255, 255, 255, 32],
            line_width_min_pixels=1,
            extruded=True,
            wireframe=True,
            pickable=True,
        ),
        pdk.Layer("PathLayer", [{"path": target_route[: route_index + 1]}], get_path="path", get_color=[r, g, b, 255], width_min_pixels=5),
        pdk.Layer("PathLayer", [{"path": police_route_a[: min(route_index + 1, len(police_route_a))]}], get_path="path", get_color=[102, 168, 255, 230], width_min_pixels=4),
        pdk.Layer("PathLayer", [{"path": police_route_b[: min(route_index + 1, len(police_route_b))]}], get_path="path", get_color=[157, 197, 255, 210], width_min_pixels=4),
        pdk.Layer(
            "ScatterplotLayer",
            [{"position": target_route[route_index], "label": "TARGET"}],
            get_position="position",
            get_fill_color=[r, g, b, 255],
            get_radius=48,
            radius_min_pixels=8,
            pickable=True,
        ),
    ]
    return pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=14.35, pitch=56, bearing=-28),
        map_style=None,
        tooltip={"html": "<b>{label}</b><br/>Height: {height}", "style": {"backgroundColor": "#0b0d11", "color": "#f4f2eb"}},
    )


def response_doctrine_figure(threat: int, evidence: int, mobility: int, accent: str) -> go.Figure:
    patrol = min(100, 18 + threat * 8)
    pursuit = min(100, 12 + threat * 10 + mobility * 5)
    containment = min(100, threat * 9 + evidence * 6 + mobility * 4)
    investigation = min(100, 8 + evidence * 15 + threat * 3)
    labels = ["PATROL", "PURSUIT", "CONTAINMENT", "INVESTIGATION"]
    values = [patrol, pursuit, containment, investigation]
    colors = ["#8D96A3", "#66A8FF", accent, "#9DE4B2"]
    fig = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=colors, text=[f"{value}%" for value in values], textposition="inside", hovertemplate="%{y}: %{x}%<extra></extra>"))
    fig.update_layout(
        height=330,
        margin=dict(l=15, r=15, t=15, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        font=dict(color="#C8CCD2", size=11),
        xaxis=dict(range=[0, 100], visible=False),
        yaxis=dict(autorange="reversed", gridcolor="rgba(255,255,255,.05)"),
        bargap=.42,
        showlegend=False,
    )
    return fig


def skill_tree_figure(categories: tuple[SkillCategory, ...]) -> go.Figure:
    labels = ["HEIST CITY"]
    parents = [""]
    values = [sum(len(category.skills) for category in categories)]
    colors = ["#11151A"]
    hover = ["24-skill progression architecture"]
    for category in categories:
        labels.append(category.title)
        parents.append("HEIST CITY")
        values.append(len(category.skills))
        colors.append(category.accent)
        hover.append(category.summary)
        for skill in category.skills:
            labels.append(skill.name)
            parents.append(category.title)
            values.append(1)
            colors.append(category.accent)
            hover.append(f"Tier {skill.tier} — {skill.description}")
    fig = go.Figure(go.Sunburst(labels=labels, parents=parents, values=values, branchvalues="total", marker=dict(colors=colors, line=dict(color="#090B0E", width=2)), customdata=hover, hovertemplate="<b>%{label}</b><br>%{customdata}<extra></extra>", insidetextorientation="radial"))
    fig.update_layout(height=560, margin=dict(l=5, r=5, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F4F2EB", size=11))
    return fig


def system_topology_figure(accent: str) -> go.Figure:
    graph = nx.DiGraph()
    edges = [
        ("PLAYER INTENT", "INPUT ACTIONS"),
        ("BOT INTENT", "INPUT ACTIONS"),
        ("INPUT ACTIONS", "FIXED SIMULATION"),
        ("FIXED SIMULATION", "COMBAT / VEHICLES"),
        ("FIXED SIMULATION", "WORLD STATE"),
        ("COMBAT / VEHICLES", "WORLD STATE"),
        ("WORLD STATE", "REPLICATION"),
        ("REPLICATION", "CLIENT PRESENTATION"),
        ("SUPERVISOR", "FIXED SIMULATION"),
        ("SUPERVISOR", "WORLD STATE"),
    ]
    graph.add_edges_from(edges)
    positions = nx.spring_layout(graph, seed=14, k=.95)
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color="rgba(255,255,255,.16)", width=1.5), hoverinfo="skip"))
    node_x, node_y, labels, node_colors = [], [], [], []
    for node in graph.nodes():
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)
        labels.append(node)
        node_colors.append(accent if node in {"FIXED SIMULATION", "WORLD STATE"} else "#1A2028")
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text", text=labels, textposition="bottom center", marker=dict(size=34, color=node_colors, line=dict(color="#F4F2EB", width=1)), textfont=dict(color="#D9DCE1", size=10), hovertemplate="%{text}<extra></extra>"))
    fig.update_layout(height=500, margin=dict(l=20, r=20, t=20, b=45), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#090c10", xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False)
    return fig


def roadmap_chart(accent: str) -> alt.Chart:
    data = pd.DataFrame(
        {
            "track": ["Core authority", "Presentation", "Game systems", "Public testing"],
            "start": [0, 18, 35, 64],
            "end": [28, 52, 78, 100],
            "state": ["active", "active", "next", "planned"],
        }
    )
    base = alt.Chart(data).encode(
        y=alt.Y("track:N", sort=None, title=None, axis=alt.Axis(labelColor="#B7BBC2", labelFontSize=12, ticks=False, domain=False)),
        x=alt.X("start:Q", scale=alt.Scale(domain=[0, 100]), axis=None),
        x2="end:Q",
        tooltip=["track:N", "state:N"],
    )
    return (base.mark_bar(cornerRadius=8, height=16).encode(color=alt.value(accent))).properties(height=170).configure_view(strokeOpacity=0)


def procedural_poster(accent_rgb: tuple[int, int, int], seed: int, width: int = 1400, height: int = 720) -> bytes:
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, height)[:, None]
    x = np.linspace(0, 1, width)[None, :]
    base = np.zeros((height, width, 3), dtype=np.float32)
    base[..., 0] = 6 + 10 * y
    base[..., 1] = 8 + 13 * y
    base[..., 2] = 11 + 18 * y
    cx, cy = .76, .28
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    glow = np.clip(1 - dist / .58, 0, 1) ** 2
    for channel, value in enumerate(accent_rgb):
        base[..., channel] += glow * value * .32
    noise = rng.normal(0, 4.3, size=(height, width, 1))
    base = np.clip(base + noise, 0, 255).astype(np.uint8)
    image = Image.fromarray(base, "RGB")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = (*accent_rgb, 82)
    for i in range(-4, 16):
        x0 = i * 110
        draw.line((x0, height, x0 + 470, 0), fill=(255, 255, 255, 18), width=2)
    for radius in (110, 180, 260):
        draw.ellipse((width * .76 - radius, height * .28 - radius, width * .76 + radius, height * .28 + radius), outline=accent, width=2)
    draw.rectangle((42, 42, width - 42, height - 42), outline=(255, 255, 255, 30), width=2)
    overlay = overlay.filter(ImageFilter.GaussianBlur(.35))
    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    out = BytesIO()
    image.save(out, format="WEBP", quality=88, method=6)
    return out.getvalue()


def _hex_rgb(value: str) -> tuple[int, int, int]:
    clean = value.lstrip("#")
    return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)


def _hex_to_rgba(value: str, alpha: float) -> str:
    r, g, b = _hex_rgb(value)
    return f"rgba({r},{g},{b},{alpha})"


def ballistics_ttk_figure(weapon: WeaponSpec, armor_tier: int, headshot_pct: int, accent: str) -> go.Figure:
    distances = np.arange(2, 62, 2)
    ttks = []
    damages = []
    armor_factor = 1.0 - (armor_tier * 0.15)
    hs_ratio = headshot_pct / 100.0

    for d in distances:
        if d <= weapon.optimal_range:
            base_drop = 1.0
        else:
            slope = max(0.35, 1.0 - ((d - weapon.optimal_range) / max(1, (weapon.max_range - weapon.optimal_range))) * 0.65)
            base_drop = slope
        dmg = weapon.base_damage * base_drop
        eff_dmg = (dmg * (1.0 - hs_ratio) + dmg * weapon.head_mult * hs_ratio) * armor_factor
        damages.append(round(eff_dmg, 1))
        shots_to_kill = int(np.ceil(100.0 / max(1.0, eff_dmg)))
        ttk_ms = (shots_to_kill - 1) * (60.0 / weapon.rpm) * 1000.0
        ttks.append(round(ttk_ms, 0))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=distances,
            y=ttks,
            mode="lines+markers",
            name="TIME-TO-KILL (ms)",
            line=dict(color=accent, width=3.5),
            marker=dict(size=6, color=accent),
            hovertemplate="Distance: %{x}m<br>TTK: %{y}ms<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=distances,
            y=damages,
            mode="lines",
            name="EFF. DAMAGE / SHOT",
            line=dict(color="#F4F2EB", width=2, dash="dot"),
            yaxis="y2",
            hovertemplate="Distance: %{x}m<br>Damage: %{y} HP<extra></extra>",
        )
    )
    fig.add_vline(x=weapon.optimal_range, line_width=1.5, line_dash="dash", line_color="rgba(255,255,255,.3)", annotation_text="OPTIMAL CUTOFF", annotation_position="top right")

    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=35, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        font=dict(color="#C8CCD2", size=11),
        xaxis=dict(title="ENGAGEMENT DISTANCE (METERS)", gridcolor="rgba(255,255,255,.07)", zeroline=False),
        yaxis=dict(title="TIME-TO-KILL (ms)", gridcolor="rgba(255,255,255,.07)", zeroline=False),
        yaxis2=dict(title="DAMAGE / HIT (HP)", overlaying="y", side="right", showgrid=False, font=dict(color="#AEB4BC")),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    return fig


def recoil_pattern_figure(weapon: WeaponSpec, burst_mode: bool, accent: str) -> go.Figure:
    rng = np.random.default_rng(42)
    shots = weapon.mag_size if not burst_mode else min(6, weapon.mag_size)
    spread_mod = 0.42 if burst_mode else 1.0

    x_points = [0.0]
    y_points = [0.0]
    curr_x, curr_y = 0.0, 0.0

    for i in range(1, shots):
        vert_climb = (weapon.recoil_vert * 0.45 * (1.0 + (i * 0.04))) * spread_mod
        horiz_drift = (rng.normal(0, weapon.recoil_horiz * 0.35)) * spread_mod
        curr_y += vert_climb
        curr_x += horiz_drift
        x_points.append(round(curr_x, 2))
        y_points.append(round(curr_y, 2))

    fig = go.Figure()
    # Bullseye target rings
    for r in [2, 4, 6, 8, 10]:
        fig.add_shape(type="circle", x0=-r, y0=-r, x1=r, y1=r, line=dict(color="rgba(255,255,255,.08)", width=1))

    fig.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            mode="lines+markers+text",
            line=dict(color="rgba(255,255,255,.25)", width=1.5, dash="dot"),
            marker=dict(
                size=[14] + [10] * (len(x_points) - 1),
                color=[accent] + ["#FF764D" if burst_mode else "#FF4D4D"] * (len(x_points) - 1),
                symbol="circle",
                line=dict(color="#FFF", width=1),
            ),
            text=[f"#{i+1}" for i in range(len(x_points))],
            textposition="top center",
            textfont=dict(size=9, color="#AEB4BC"),
            name="SHOT DISPERSION",
            hovertemplate="Shot %{text}: (%{x}, %{y})<extra></extra>",
        )
    )

    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        xaxis=dict(title="HORIZONTAL DEVIATION (MOA)", range=[-12, 12], gridcolor="rgba(255,255,255,.06)", zerolinecolor="rgba(255,255,255,.15)"),
        yaxis=dict(title="VERTICAL CLIMB (MOA)", range=[-3, 15], gridcolor="rgba(255,255,255,.06)", zerolinecolor="rgba(255,255,255,.15)", scaleanchor="x"),
        showlegend=False,
    )
    return fig


def netcode_rollback_figure(ping_ms: int, jitter_ms: int, packet_loss_pct: int, accent: str) -> go.Figure:
    fig = go.Figure()
    # Timelines for Client Prediction vs Server 60Hz Authority
    ticks = np.arange(0, 13)
    tick_times = ticks * 16.6  # 60Hz tick intervals (~16.6ms)

    # Server tick grid
    for tt in tick_times:
        fig.add_vline(x=tt, line_width=1, line_dash="solid", line_color="rgba(255,255,255,.04)")

    client_send = 33.2
    travel_time = (ping_ms / 2.0) + jitter_ms
    server_receive = client_send + travel_time
    rollback_window_start = max(0.0, server_receive - 250.0)

    # Rewind buffer region on server
    fig.add_vrect(
        x0=rollback_window_start,
        x1=server_receive,
        fillcolor="rgba(118,243,255,.08)",
        line_width=1,
        line_dash="dot",
        line_color=accent,
        annotation_text="250ms SERVER REWIND BUFFER",
        annotation_position="top left",
        annotation_font=dict(size=10, color=accent),
    )

    # Client Intent Vector
    fig.add_trace(go.Scatter(x=[client_send], y=[3], mode="markers+text", marker=dict(size=14, color=accent, symbol="diamond"), text=["CLIENT INTENT T_0"], textposition="top right", name="Client Event"))
    # Packet In-Flight Vector
    fig.add_trace(go.Scatter(x=[client_send, server_receive], y=[3, 1], mode="lines", line=dict(color=accent, width=2.5, dash="dash"), name="In-Flight Intent"))
    # Server Rewind & Verification
    fig.add_trace(go.Scatter(x=[server_receive], y=[1], mode="markers+text", marker=dict(size=14, color="#FFB84D", symbol="square"), text=[f"SERVER VALIDATION (+{int(travel_time)}ms)"], textposition="bottom right", name="Server Tick"))

    # ACK Return
    ack_receive = server_receive + travel_time
    is_dropped = packet_loss_pct > 20
    if not is_dropped:
        fig.add_trace(go.Scatter(x=[server_receive, ack_receive], y=[1, 3], mode="lines", line=dict(color="#8CFFAA", width=2.5, dash="dot"), name="Authoritative ACK"))
        fig.add_trace(go.Scatter(x=[ack_receive], y=[3], mode="markers+text", marker=dict(size=12, color="#8CFFAA", symbol="circle"), text=["STATE RECONCILED"], textposition="top right", name="Reconciliation"))
    else:
        fig.add_trace(go.Scatter(x=[server_receive + (travel_time * 0.5)], y=[2], mode="markers+text", marker=dict(size=16, color="#FF4D4D", symbol="x"), text=["PACKET LOSS (EXTRAPOLATE)"], textposition="top center", name="Dropped Packet"))

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=35, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        font=dict(color="#C8CCD2", size=11),
        xaxis=dict(title="SIMULATION TIME ELAPSED (MILLISECONDS)", range=[-10, max(280, ack_receive + 30)], gridcolor="rgba(255,255,255,.07)", zeroline=False),
        yaxis=dict(
            tickvals=[1, 2, 3],
            ticktext=["SERVER 60Hz AUTHORITY", "ROBLOX NETWORK", "CLIENT PREDICTION"],
            gridcolor="rgba(255,255,255,.07)",
            zeroline=False,
            range=[0.5, 3.8],
        ),
        showlegend=False,
    )
    return fig


def zombie_escalation_figure(squad_size: int, barricade_tier: int, resource_discipline: str, accent: str) -> go.Figure:
    waves = np.arange(1, 21)
    # Exponential horde pressure
    horde_pressure = np.clip(12 + (waves ** 1.55) * 1.65, 0, 100)
    # Barricade health decay
    barricade_decay_rate = 5.5 - (barricade_tier * 0.9)
    barricades = np.clip(100 - (waves * barricade_decay_rate) + (squad_size * 2.2), 0, 100)
    # Ammo depletion
    discipline_mult = {"CONSERVATIVE": 0.72, "BALANCED": 1.0, "AGGRESSIVE": 1.45}[resource_discipline]
    ammo_depletion = np.clip(100 - (waves * 4.6 * discipline_mult / max(1, squad_size * 0.4)), 0, 100)
    # Survival Probability %
    survival_prob = np.clip(100 - (horde_pressure * 0.5) - ((100 - barricades) * 0.3) - ((100 - ammo_depletion) * 0.35) + (squad_size * 4), 0, 100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=waves, y=horde_pressure, mode="lines", name="HORDE THREAT", line=dict(color="#FF4D4D", width=3)))
    fig.add_trace(go.Scatter(x=waves, y=barricades, mode="lines", name="BARRICADE HEALTH", line=dict(color="#FFB84D", width=2.5, dash="dash")))
    fig.add_trace(go.Scatter(x=waves, y=ammo_depletion, mode="lines", name="AMMO RESERVES", line=dict(color=accent, width=2.5, dash="dot")))
    fig.add_trace(go.Scatter(x=waves, y=survival_prob, mode="lines+markers", name="SURVIVAL CHANCE %", line=dict(color="#F4F2EB", width=3.5), marker=dict(size=6)))
    fig.add_hrect(y0=0, y1=25, fillcolor="rgba(255,77,77,.08)", line_width=0, annotation_text="CRITICAL COLLAPSE ZONE", annotation_position="bottom right")

    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=35, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        font=dict(color="#C8CCD2", size=11),
        xaxis=dict(title="OUTBREAK WAVE STAGE", tickmode="linear", tick0=1, dtick=2, gridcolor="rgba(255,255,255,.07)", zeroline=False),
        yaxis=dict(title="SIMULATED CAPACITY (%)", range=[0, 105], gridcolor="rgba(255,255,255,.07)", zeroline=False),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    return fig


def skill_build_radar(points: dict[str, int], accent: str) -> go.Figure:
    categories = ["HACKING", "COMBAT", "DRIVING", "INTELLIGENCE"]
    values = [points.get(cat.lower(), 0) * 16.6 for cat in categories]
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            line=dict(color=accent, width=3),
            fillcolor=_hex_to_rgba(accent, 0.22),
            marker=dict(size=8, color=accent),
            hovertemplate="%{theta}: %{r:.0f}%<extra></extra>",
        )
    )
    fig.update_layout(
        height=370,
        margin=dict(l=35, r=35, t=35, b=35),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#D8DADF", size=11),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor="rgba(255,255,255,.10)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,.10)"),
        ),
        showlegend=False,
    )
    return fig


def pursuit_sandbox_figure(strategy: str, police_pressure: int, accent: str) -> go.Figure:
    road_count = 9
    roads = np.arange(road_count)

    # Strategy paths
    if strategy == "HIGHWAY BURN":
        player_path = np.array([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]])
        police_a = np.array([[3, 4], [4, 3], [5, 2], [6, 1]])
        police_b = np.array([[8, 6], [8, 4], [8, 2], [8, 1]])
        roadblocks = np.array([[7, 1], [8, 2]])
    elif strategy == "ALLEY DIVE":
        player_path = np.array([[1, 7], [2, 7], [2, 5], [3, 5], [4, 5], [4, 3], [5, 3], [6, 3]])
        police_a = np.array([[1, 4], [2, 4], [3, 4], [4, 4], [4, 3]])
        police_b = np.array([[7, 7], [6, 7], [5, 5], [5, 3]])
        roadblocks = np.array([[3, 7], [5, 4]])
    elif strategy == "COUNTER-AMBUSH":
        player_path = np.array([[4, 8], [4, 6], [4, 4], [5, 4], [6, 4], [7, 4], [7, 2]])
        police_a = np.array([[2, 4], [3, 4], [4, 4]])
        police_b = np.array([[7, 7], [7, 5], [7, 4]])
        roadblocks = np.array([[4, 2], [6, 5]])
    else:  # GRID WEAVE
        player_path = np.array([[1, 2], [2, 2], [2, 4], [4, 4], [4, 6], [6, 6], [7, 6], [7, 7]])
        police_a = np.array([[6, 2], [5, 3], [4, 5], [5, 6], [6, 6]])
        police_b = np.array([[2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7]])
        roadblocks = np.array([[5, 5], [7, 5]])

    fig = go.Figure()
    for x in roads:
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=road_count - 1, line=dict(color="rgba(255,255,255,.07)", width=10))
    for y in roads:
        fig.add_shape(type="line", x0=0, y0=y, x1=road_count - 1, y1=y, line=dict(color="rgba(255,255,255,.07)", width=10))

    # Roadblock hazards
    fig.add_trace(go.Scatter(x=roadblocks[:, 0], y=roadblocks[:, 1], mode="markers+text", marker=dict(size=14, color="#FF4D4D", symbol="cross"), text=["ROADBLOCK", "SPIKES"][: len(roadblocks)], textposition="top right", name="POLICE CORDON"))

    # Player and Police vectors
    fig.add_trace(go.Scatter(x=player_path[:, 0], y=player_path[:, 1], mode="lines+markers", line=dict(color=accent, width=4.5), marker=dict(size=9, color=accent), name="GETAWAY PATH"))
    fig.add_trace(go.Scatter(x=police_a[:, 0], y=police_a[:, 1], mode="lines+markers", line=dict(color="#66A8FF", width=3, dash="dash"), marker=dict(size=7, color="#66A8FF"), name="INTERCEPT UNIT 01"))
    if police_pressure >= 3:
        fig.add_trace(go.Scatter(x=police_b[:, 0], y=police_b[:, 1], mode="lines+markers", line=dict(color="#FF8C8C", width=3, dash="dot"), marker=dict(size=7, color="#FF8C8C"), name="CONTAINMENT UNIT 02"))

    fig.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090c10",
        xaxis=dict(visible=False, range=[-0.5, road_count - 0.5]),
        yaxis=dict(visible=False, range=[-0.5, road_count - 0.5], scaleanchor="x"),
        legend=dict(orientation="h", y=1.04, font=dict(color="#B8BDC5", size=10), bgcolor="rgba(0,0,0,0)"),
        hovermode=False,
    )
    return fig

