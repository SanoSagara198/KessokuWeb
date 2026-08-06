from __future__ import annotations

POLISH_CSS = r"""
<style>
/* Kessoku V2.2: final presentation polish layered over the core design system. */
:root {
  --k-glass: rgba(10,12,15,.72);
  --k-glass-strong: rgba(13,16,20,.91);
  --k-soft-line: rgba(255,255,255,.075);
  --k-focus: #76f3ff;
}

html {
  scrollbar-color: rgba(255,255,255,.24) #07080a;
  scrollbar-width: thin;
}

::-webkit-scrollbar { width: 11px; height: 11px; }
::-webkit-scrollbar-track { background: #07080a; }
::-webkit-scrollbar-thumb {
  border: 3px solid #07080a;
  border-radius: 999px;
  background: rgba(255,255,255,.22);
}
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,.36); }

.block-container > div[data-testid="stVerticalBlock"] {
  animation: kPageReveal .48s cubic-bezier(.2,.8,.2,1) both;
}

.k-topline {
  isolation: isolate;
  overflow: hidden;
}
.k-topline:before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  background:
    linear-gradient(105deg, rgba(118,243,255,.055), transparent 32%),
    linear-gradient(255deg, rgba(255,184,77,.05), transparent 34%);
  pointer-events: none;
}
.k-topline:after {
  content: "";
  position: absolute;
  left: 5rem;
  right: 5rem;
  bottom: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.24), transparent);
}

.k-section {
  position: relative;
}
.k-section:before {
  content: "";
  position: absolute;
  top: 2.2rem;
  left: 0;
  width: min(9rem, 18vw);
  height: 1px;
  background: linear-gradient(90deg, rgba(255,255,255,.3), transparent);
}
.k-section:after {
  content: "";
  position: absolute;
  top: calc(2.2rem - 3px);
  left: 0;
  width: 7px;
  height: 7px;
  border: 1px solid rgba(255,255,255,.45);
  border-radius: 50%;
  background: #07080a;
}

/* Media becomes a deliberate campaign frame rather than a raw Streamlit image. */
[data-testid="stImage"] {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 22px;
  background: #090b0e;
  box-shadow: 0 26px 68px rgba(0,0,0,.3);
}
[data-testid="stImage"]:before {
  content: "KESSOKU / CAMPAIGN FRAME";
  position: absolute;
  z-index: 3;
  top: .8rem;
  left: .85rem;
  padding: .34rem .48rem;
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 999px;
  background: rgba(4,5,7,.62);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  color: rgba(255,255,255,.68);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .54rem;
  letter-spacing: .1em;
  pointer-events: none;
}
[data-testid="stImage"] img {
  display: block;
  transition: transform .7s cubic-bezier(.2,.8,.2,1), filter .4s ease;
}
[data-testid="stImage"]:hover img {
  transform: scale(1.012);
  filter: contrast(1.035) saturate(1.04);
}

/* Charts share one visual grammar without becoming dashboard cards. */
[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"],
[data-testid="stDeckGlJsonChart"] {
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.105);
  border-radius: 20px;
  background:
    linear-gradient(180deg, rgba(255,255,255,.022), transparent 24%),
    rgba(7,9,12,.52);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
}
[data-testid="stPlotlyChart"]:focus-within,
[data-testid="stVegaLiteChart"]:focus-within,
[data-testid="stDeckGlJsonChart"]:focus-within {
  border-color: rgba(118,243,255,.52);
  box-shadow: 0 0 0 2px rgba(118,243,255,.10);
}

/* Make metrics read as tactical readouts. */
[data-testid="stMetric"] {
  position: relative;
  overflow: hidden;
  min-height: 132px;
  border-color: rgba(255,255,255,.12) !important;
  border-radius: 16px !important;
  background:
    linear-gradient(135deg, rgba(255,255,255,.04), transparent 58%),
    rgba(8,10,13,.66);
}
[data-testid="stMetric"]:after {
  content: "";
  position: absolute;
  left: 0;
  right: 36%;
  bottom: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--k-focus), transparent);
  opacity: .55;
}
[data-testid="stMetricLabel"] {
  text-transform: uppercase;
  letter-spacing: .09em;
}
[data-testid="stMetricValue"] {
  letter-spacing: -.045em;
}

/* Native interactive controls receive a deliberate console-like treatment. */
[data-testid="stSegmentedControl"] > div,
[data-testid="stPills"] > div {
  gap: .42rem;
}
[data-testid="stSegmentedControl"] button,
[data-testid="stPills"] button {
  min-height: 2.7rem;
  border-radius: 12px !important;
  transition: border-color .16s ease, background .16s ease, transform .16s ease !important;
}
[data-testid="stSegmentedControl"] button:hover,
[data-testid="stPills"] button:hover {
  transform: translateY(-1px);
}
[data-testid="stSegmentedControl"] button:focus-visible,
[data-testid="stPills"] button:focus-visible,
.stButton > button:focus-visible {
  outline: 2px solid var(--k-focus) !important;
  outline-offset: 2px !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
  height: 3px;
}
[data-testid="stSlider"] [role="slider"] {
  box-shadow: 0 0 0 4px rgba(118,243,255,.10), 0 0 24px rgba(118,243,255,.18);
}

/* Expanders become readable dossier chapters. */
div[data-testid="stExpander"] {
  overflow: hidden;
  border-color: rgba(255,255,255,.105) !important;
  background: rgba(255,255,255,.013);
  transition: border-color .18s ease, background .18s ease;
}
div[data-testid="stExpander"]:hover {
  border-color: rgba(255,255,255,.24) !important;
  background: rgba(255,255,255,.022);
}
div[data-testid="stExpander"] summary {
  min-height: 3.4rem;
}
div[data-testid="stExpander"] summary p {
  font-weight: 720;
  letter-spacing: -.01em;
}

/* Information notes should look like deliberate public-status notices. */
[data-testid="stAlert"] {
  border: 1px solid rgba(118,243,255,.18);
  border-radius: 16px;
  background: linear-gradient(90deg, rgba(118,243,255,.055), rgba(255,255,255,.012));
}

.k-game-card,
.k-feature,
.k-editorial,
.k-mode-panel,
.k-update,
.k-stat-strip {
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
}

.k-game-card:focus-within,
.k-feature:focus-within,
.k-editorial:focus-within,
.k-mode-panel:focus-within {
  outline: 2px solid rgba(118,243,255,.48);
  outline-offset: 3px;
}

.k-footer {
  position: relative;
}
.k-footer:before {
  content: "";
  position: absolute;
  top: -1px;
  left: 0;
  width: 38%;
  height: 1px;
  background: linear-gradient(90deg, #76f3ff, transparent);
  opacity: .5;
}

@keyframes kPageReveal {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 760px) {
  .block-container { padding-top: .35rem; }
  .k-section:before, .k-section:after { display: none; }
  [data-testid="stImage"] { border-radius: 17px; }
  [data-testid="stImage"]:before {
    top: .55rem;
    left: .58rem;
    font-size: .48rem;
  }
  [data-testid="stMetric"] { min-height: 112px; }
}

@media (prefers-reduced-motion: reduce) {
  .block-container > div[data-testid="stVerticalBlock"] { animation: none !important; }
  [data-testid="stImage"] img,
  [data-testid="stSegmentedControl"] button,
  [data-testid="stPills"] button { transition: none !important; }
  [data-testid="stImage"]:hover img { transform: none !important; }
}
</style>
"""
