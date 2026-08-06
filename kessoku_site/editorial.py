from __future__ import annotations


EDITORIAL_CSS = r"""
<style>
/* Kessoku V2.3 — editorial presentation layer. */
@supports (animation-timeline: scroll()) {
  html {
    scroll-timeline-name: --k-page-scroll;
    scroll-timeline-axis: block;
  }
  .stApp:after {
    content: "";
    position: fixed;
    z-index: 999;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    transform-origin: left;
    transform: scaleX(0);
    background: linear-gradient(90deg, #76f3ff, #f4f2eb 48%, #ffb84d);
    box-shadow: 0 0 18px rgba(118,243,255,.42);
    animation: kReadingProgress linear;
    animation-timeline: --k-page-scroll;
  }
}
.k-world-marquee {
  position: relative;
  overflow: hidden;
  margin: -.25rem 0 1rem;
  border: 1px solid rgba(255,255,255,.075);
  border-radius: 14px;
  background: rgba(255,255,255,.014);
}
.k-world-marquee-track {
  display: flex;
  width: max-content;
  gap: 2.2rem;
  padding: .62rem 1rem;
  color: rgba(244,242,235,.55);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .56rem;
  letter-spacing: .13em;
  white-space: nowrap;
  animation: kMarquee 30s linear infinite;
}
.k-world-marquee-track span:before {
  content: "";
  display: inline-block;
  width: 5px;
  height: 5px;
  margin-right: .72rem;
  border-radius: 50%;
  background: currentColor;
  vertical-align: 1px;
  opacity: .72;
}
.k-hero-meta {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin-top: .8rem;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.105);
  border-radius: 17px;
  background: rgba(7,9,12,.64);
  -webkit-backdrop-filter: blur(18px);
  backdrop-filter: blur(18px);
}
.k-hero-meta-item {
  min-height: 92px;
  padding: 1rem 1.1rem;
  border-right: 1px solid rgba(255,255,255,.08);
}
.k-hero-meta-item:last-child { border-right: 0; }
.k-hero-meta-label {
  color: rgba(244,242,235,.42);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .54rem;
  letter-spacing: .12em;
}
.k-hero-meta-value {
  margin-top: .72rem;
  color: #f4f2eb;
  font-size: clamp(.82rem, 1.2vw, 1.02rem);
  font-weight: 760;
  letter-spacing: -.015em;
}
.k-project-signature {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin: .65rem 0 1rem;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(255,255,255,.025), rgba(255,255,255,.009));
}
.k-project-signature-item {
  min-height: 92px;
  padding: .92rem 1rem;
  border-right: 1px solid rgba(255,255,255,.075);
}
.k-project-signature-item:last-child { border-right: 0; }
.k-project-signature-label {
  color: var(--accent);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .54rem;
  letter-spacing: .12em;
}
.k-project-signature-value {
  margin-top: .65rem;
  color: rgba(244,242,235,.78);
  font-size: .72rem;
  line-height: 1.45;
  letter-spacing: .035em;
}
.k-footer-pro {
  position: relative;
  display: grid;
  grid-template-columns: 1.25fr .75fr .75fr;
  gap: 2rem;
  margin-top: 8rem;
  padding: 2.4rem 0 1.6rem;
  border-top: 1px solid rgba(255,255,255,.11);
}
.k-footer-pro:before {
  content: "";
  position: absolute;
  top: -1px;
  left: 0;
  width: min(28rem, 55%);
  height: 1px;
  background: linear-gradient(90deg, #76f3ff, rgba(255,184,77,.72), transparent);
}
.k-footer-mark {
  font-size: clamp(2.2rem, 5vw, 5.8rem);
  font-weight: 930;
  line-height: .82;
  letter-spacing: -.075em;
}
.k-footer-copy {
  max-width: 42rem;
  margin-top: 1rem;
  color: rgba(244,242,235,.5);
  line-height: 1.65;
}
.k-footer-heading {
  margin-bottom: .9rem;
  color: rgba(244,242,235,.38);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .56rem;
  letter-spacing: .13em;
}
.k-footer-line {
  padding: .42rem 0;
  color: rgba(244,242,235,.72);
  font-size: .78rem;
  border-bottom: 1px solid rgba(255,255,255,.055);
}
.k-footer-base {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: .7rem;
  padding-top: 1.1rem;
  border-top: 1px solid rgba(255,255,255,.065);
  color: rgba(244,242,235,.35);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .54rem;
  letter-spacing: .1em;
}
@keyframes kReadingProgress { to { transform: scaleX(1); } }
@keyframes kMarquee { to { transform: translateX(-50%); } }
@media (max-width: 760px) {
  .k-world-marquee { display: none; }
  .k-hero-meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .k-hero-meta-item:nth-child(2) { border-right: 0; }
  .k-hero-meta-item:nth-child(-n+2) { border-bottom: 1px solid rgba(255,255,255,.08); }
  .k-project-signature { grid-template-columns: 1fr; }
  .k-project-signature-item {
    min-height: 0;
    border-right: 0;
    border-bottom: 1px solid rgba(255,255,255,.075);
  }
  .k-project-signature-item:last-child { border-bottom: 0; }
  .k-footer-pro { grid-template-columns: 1fr; }
  .k-footer-base { grid-column: 1; flex-direction: column; }
}
@media (prefers-reduced-motion: reduce) {
  .k-world-marquee-track { animation: none !important; }
  .stApp:after { display: none; }
}
</style>
"""
