from __future__ import annotations

from io import BytesIO

import altair as alt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
from PIL import Image, ImageDraw, ImageFilter

from .models import Metric, SkillCategory


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
