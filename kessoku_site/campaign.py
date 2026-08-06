from __future__ import annotations


CAMPAIGN_CSS = r"""
<style>
.k-hero--campaign {
  background-color: #06080b;
  background-blend-mode: normal;
}
.k-hero--campaign:after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    linear-gradient(90deg, rgba(4,6,9,.35), transparent 58%),
    linear-gradient(180deg, transparent 54%, rgba(4,6,9,.52));
}
.k-hero--campaign .k-hero-noise { opacity: .055; }
.k-hero--campaign .k-display {
  max-width: 7.6ch;
  text-shadow: 0 8px 38px rgba(0,0,0,.72);
}
.k-hero--campaign .k-lede {
  color: rgba(244,242,235,.88);
  text-shadow: 0 2px 18px rgba(0,0,0,.78);
}
.k-hero--campaign .k-hero-code,
.k-hero--campaign .k-signal {
  background: rgba(4,6,9,.58);
  -webkit-backdrop-filter: blur(16px);
  backdrop-filter: blur(16px);
}

.k-mode-panel--campaign {
  position: relative;
  min-height: 610px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
  isolation: isolate;
  border-color: rgba(255,255,255,.18);
  box-shadow: 0 34px 90px rgba(0,0,0,.42);
}
.k-mode-panel--campaign:after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    linear-gradient(180deg, rgba(255,255,255,.035), transparent 18%),
    linear-gradient(90deg, transparent 68%, rgba(255,255,255,.03));
}
.k-mode-media-label {
  align-self: flex-start;
  margin-bottom: auto;
  padding: .38rem .58rem;
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px;
  background: rgba(4,6,9,.56);
  -webkit-backdrop-filter: blur(14px);
  backdrop-filter: blur(14px);
  color: rgba(244,242,235,.72);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .56rem;
  letter-spacing: .11em;
}
.k-mode-panel--campaign .k-mode-title {
  max-width: 8ch;
  text-shadow: 0 8px 34px rgba(0,0,0,.72);
}
.k-mode-panel--campaign .k-mode-fantasy,
.k-mode-panel--campaign .k-mode-copy,
.k-mode-panel--campaign .k-objective,
.k-mode-panel--campaign .k-facts {
  max-width: 72%;
}
.k-mode-panel--campaign .k-objective {
  background: rgba(4,6,9,.58);
  -webkit-backdrop-filter: blur(14px);
  backdrop-filter: blur(14px);
}
.k-mode-panel--campaign .k-fact {
  color: rgba(244,242,235,.72);
  text-shadow: 0 2px 12px rgba(0,0,0,.75);
}

@media (max-width: 900px) {
  .k-hero--campaign {
    background-position: 58% center !important;
  }
  .k-mode-panel--campaign {
    min-height: 560px;
    background-position: 60% center !important;
  }
  .k-mode-panel--campaign .k-mode-fantasy,
  .k-mode-panel--campaign .k-mode-copy,
  .k-mode-panel--campaign .k-objective,
  .k-mode-panel--campaign .k-facts {
    max-width: 86%;
  }
}

@media (max-width: 560px) {
  .k-hero--campaign {
    min-height: 720px;
    background-position: 64% center !important;
  }
  .k-mode-panel--campaign {
    min-height: 680px;
    justify-content: flex-end;
    background-position: 66% center !important;
  }
  .k-mode-panel--campaign .k-mode-fantasy,
  .k-mode-panel--campaign .k-mode-copy,
  .k-mode-panel--campaign .k-objective,
  .k-mode-panel--campaign .k-facts {
    max-width: 100%;
  }
  .k-mode-media-label {
    margin-bottom: 7rem;
  }
}
</style>
"""
