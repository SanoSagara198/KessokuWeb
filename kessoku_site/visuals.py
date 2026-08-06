from __future__ import annotations

from io import BytesIO

import altair as alt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFilter

from .models import Metric


def metric_radar(metrics: tuple[Metric, ...], accent: str) -> go.Figure:
    labels = [m.label.upper() for m in metrics]
    values = [m.value for m in metrics]
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
        height=410,
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
        height=470, margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#090c10",
        xaxis=dict(visible=False, range=[-0.4, road_count - .6]), yaxis=dict(visible=False, range=[-0.4, road_count - .6], scaleanchor="x"),
        legend=dict(orientation="h", y=1.03, font=dict(color="#B8BDC5", size=10), bgcolor="rgba(0,0,0,0)"),
        hovermode=False,
    )
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
    return (base.mark_bar(cornerRadius=8, height=16).encode(color=alt.value(accent))).properties(height=160).configure_view(strokeOpacity=0)


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


def _hex_to_rgba(value: str, alpha: float) -> str:
    clean = value.lstrip("#")
    r, g, b = int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"
