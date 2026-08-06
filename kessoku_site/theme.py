from __future__ import annotations

CSS = r"""
<style>
:root {
  --bg: #07080a;
  --panel: #0e1115;
  --panel-2: #12171d;
  --text: #f4f2eb;
  --muted: #9ea4ad;
  --line: rgba(255,255,255,.12);
  --line-strong: rgba(255,255,255,.30);
  --cyan: #76f3ff;
  --amber: #ffb84d;
  --radius: 18px;
}
html { scroll-behavior: smooth; }
body, .stApp {
  background:
    radial-gradient(circle at 16% -10%, rgba(118,243,255,.10), transparent 34rem),
    radial-gradient(circle at 92% 18%, rgba(255,184,77,.09), transparent 38rem),
    var(--bg);
  color: var(--text);
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display:none; }
[data-testid="stSidebar"] { background: #090b0e; }
.block-container { max-width: 1420px; padding-top: 1rem; padding-bottom: 4rem; }
* { box-sizing: border-box; }
::selection { background: rgba(118,243,255,.28); color: white; }
h1,h2,h3,p { letter-spacing: -.02em; }
a { color: inherit; }
.k-nav-anchor { height: 0; }
.k-topline { display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:.8rem 0 1rem; border-bottom:1px solid var(--line); margin-bottom:1rem; }
.k-brand { display:flex; align-items:center; gap:.85rem; }
.k-mark { width:38px; height:38px; border:1px solid rgba(255,255,255,.7); transform:rotate(45deg); display:grid; place-items:center; }
.k-mark span { transform:rotate(-45deg); font-weight:900; }
.k-word { font-size:.82rem; letter-spacing:.22em; font-weight:900; }
.k-sub { color:var(--muted); font-size:.62rem; letter-spacing:.11em; margin-top:.2rem; }
.k-live { display:flex; align-items:center; gap:.55rem; color:var(--muted); font-size:.68rem; letter-spacing:.10em; }
.k-dot { width:7px; height:7px; border-radius:99px; background:#8cffaa; box-shadow:0 0 18px #8cffaa; animation:kPulse 2s infinite; }
.k-hero { min-height:min(78vh,760px); position:relative; overflow:hidden; display:grid; grid-template-columns:1.18fr .82fr; align-items:end; gap:3rem; border:1px solid var(--line); border-radius:var(--radius); padding:clamp(1.5rem,5vw,5rem); background:linear-gradient(140deg,rgba(255,255,255,.065),rgba(255,255,255,.015)); isolation:isolate; }
.k-hero:before { content:""; position:absolute; inset:0; z-index:-2; background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px); background-size:46px 46px; mask-image:linear-gradient(to bottom,black,transparent 88%); }
.k-orbit { position:absolute; width:38rem; height:38rem; border:1px solid rgba(255,255,255,.12); border-radius:50%; right:-12rem; top:-12rem; animation:kRotate 28s linear infinite; z-index:-1; }
.k-orbit:after { content:""; position:absolute; width:10px; height:10px; border-radius:50%; background:var(--hero-accent); top:50%; left:-5px; box-shadow:0 0 25px var(--hero-accent); }
.k-eyebrow { color:var(--hero-accent); font-size:.72rem; font-weight:850; letter-spacing:.17em; margin-bottom:1.2rem; }
.k-display { font-size:clamp(4rem,9vw,9.2rem); line-height:.78; letter-spacing:-.085em; margin:0; font-weight:950; max-width:9ch; }
.k-lede { color:#c8ccd2; font-size:clamp(1rem,1.6vw,1.28rem); line-height:1.65; max-width:66ch; margin:1.6rem 0 0; }
.k-hero-side { align-self:stretch; display:flex; flex-direction:column; justify-content:space-between; }
.k-hero-code { color:var(--muted); font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.69rem; letter-spacing:.07em; line-height:1.8; text-align:right; }
.k-signal { border:1px solid var(--line); background:rgba(0,0,0,.20); backdrop-filter:blur(18px); padding:1rem; border-radius:14px; }
.k-signal-line { height:1px; background:linear-gradient(90deg,transparent,var(--hero-accent),transparent); animation:kSweep 3.2s ease-in-out infinite; }
.k-signal-label { display:flex; justify-content:space-between; gap:1rem; margin-top:.75rem; color:var(--muted); font-size:.64rem; letter-spacing:.1em; }
.k-section { padding:clamp(4rem,8vw,8rem) 0 1.2rem; }
.k-section-head { display:grid; grid-template-columns:1.1fr .9fr; gap:4rem; align-items:end; margin-bottom:2rem; }
.k-kicker { color:var(--muted); font-size:.68rem; letter-spacing:.14em; margin-bottom:.7rem; }
.k-title { margin:0; font-size:clamp(2.4rem,5vw,5.6rem); line-height:.92; letter-spacing:-.065em; max-width:13ch; }
.k-copy { color:var(--muted); line-height:1.75; max-width:62ch; margin:0; }
.k-showcase { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.k-game-card { min-height:570px; position:relative; overflow:hidden; border:1px solid var(--line); border-radius:var(--radius); padding:1.4rem; background:linear-gradient(155deg,var(--soft),rgba(255,255,255,.018) 60%); transition:transform .25s ease,border-color .25s ease; }
.k-game-card:hover { transform:translateY(-5px); border-color:var(--accent); }
.k-game-grid { position:absolute; inset:0; opacity:.48; background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px); background-size:31px 31px; transform:perspective(500px) rotateX(58deg) scale(1.6) translateY(18%); transform-origin:bottom; }
.k-game-art { position:absolute; width:25rem; height:25rem; border-radius:50%; right:-8rem; top:-8rem; background:radial-gradient(circle,var(--accent),transparent 68%); filter:blur(12px); opacity:.28; }
.k-card-top { display:flex; justify-content:space-between; position:relative; z-index:2; color:var(--muted); font-size:.67rem; letter-spacing:.11em; }
.k-card-body { position:absolute; left:1.4rem; right:1.4rem; bottom:1.4rem; z-index:2; }
.k-card-title { margin:0; font-size:clamp(3.2rem,6vw,6.7rem); line-height:.78; letter-spacing:-.08em; max-width:7ch; }
.k-card-copy { color:#c8ccd2; line-height:1.6; max-width:55ch; }
.k-tags { display:flex; flex-wrap:wrap; gap:.45rem; margin-top:1rem; }
.k-tag { padding:.38rem .56rem; border:1px solid var(--line); border-radius:99px; font-size:.58rem; letter-spacing:.09em; }
.k-feature-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
.k-feature { min-height:220px; border:1px solid var(--line); border-radius:15px; padding:1.25rem; background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.015)); }
.k-feature-num { color:var(--accent); font-family:ui-monospace,monospace; font-size:.65rem; letter-spacing:.10em; }
.k-feature h3 { margin:4rem 0 .75rem; font-size:1.35rem; }
.k-feature p { color:var(--muted); line-height:1.65; margin:0; }
.k-mode-panel { border:1px solid var(--line); border-radius:var(--radius); padding:clamp(1.3rem,3vw,2.2rem); background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012)); }
.k-mode-label { color:var(--accent); font-size:.65rem; letter-spacing:.13em; }
.k-mode-title { font-size:clamp(2.4rem,5vw,5.3rem); line-height:.86; letter-spacing:-.07em; margin:.9rem 0 1.2rem; }
.k-mode-copy { color:#c8ccd2; line-height:1.7; max-width:70ch; }
.k-facts { display:grid; grid-template-columns:repeat(4,1fr); gap:.65rem; margin-top:1.4rem; }
.k-fact { border-top:1px solid var(--line-strong); padding-top:.65rem; color:var(--muted); font-size:.7rem; letter-spacing:.06em; }
.k-manifesto { border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:clamp(2rem,5vw,5rem) 0; font-size:clamp(2rem,5vw,5.8rem); line-height:.97; font-weight:850; letter-spacing:-.06em; }
.k-manifesto em { color:var(--accent); font-style:normal; }
.k-roadmap { border-top:1px solid var(--line); }
.k-road { display:grid; grid-template-columns:90px 1fr 140px; gap:1rem; align-items:center; border-bottom:1px solid var(--line); padding:1.05rem 0; }
.k-road-num { color:var(--accent); font-family:ui-monospace,monospace; }
.k-road-title { font-weight:760; }
.k-road-state { color:var(--muted); font-size:.63rem; letter-spacing:.1em; text-align:right; }
.k-footer { margin-top:7rem; border-top:1px solid var(--line); padding:1.4rem 0; display:flex; justify-content:space-between; color:var(--muted); font-size:.63rem; letter-spacing:.1em; }
.stButton > button, [data-testid="stBaseButton-secondary"] { border-radius:999px!important; border:1px solid var(--line)!important; background:rgba(255,255,255,.035)!important; color:var(--text)!important; min-height:2.8rem; font-weight:800; letter-spacing:.07em; transition:.2s ease; }
.stButton > button:hover { border-color:var(--line-strong)!important; transform:translateY(-1px); background:rgba(255,255,255,.08)!important; }
[data-testid="stSegmentedControl"] { background:transparent; }
@keyframes kPulse { 0%,100%{opacity:.5; transform:scale(.9)} 50%{opacity:1; transform:scale(1.2)} }
@keyframes kRotate { to{transform:rotate(360deg)} }
@keyframes kSweep { 0%,100%{transform:translateX(-35%);opacity:.25} 50%{transform:translateX(35%);opacity:1} }
@media (prefers-reduced-motion: reduce) { *,*:before,*:after { animation-duration:.001ms!important; animation-iteration-count:1!important; scroll-behavior:auto!important; transition:none!important; } }
@media (max-width:900px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .k-hero { grid-template-columns:1fr; min-height:670px; }
  .k-hero-side { min-height:160px; }
  .k-hero-code { text-align:left; }
  .k-section-head,.k-showcase { grid-template-columns:1fr; gap:1.5rem; }
  .k-feature-grid { grid-template-columns:1fr; }
  .k-facts { grid-template-columns:1fr 1fr; }
  .k-game-card { min-height:500px; }
}
@media (max-width:560px) {
  .k-display { font-size:3.8rem; }
  .k-live { display:none; }
  .k-facts { grid-template-columns:1fr; }
  .k-road { grid-template-columns:50px 1fr; }
  .k-road-state { display:none; }
  .k-footer { flex-direction:column; gap:.7rem; }
}
</style>
"""
