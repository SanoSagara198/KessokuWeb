# Kessoku Website V2 — Product, Design, and Implementation Specification

## 1. Objective

Kessoku Website V2 must present Kessoku as a credible independent Roblox game studio rather than a technical dashboard. The site must sell the player fantasy first, then reveal the engineering discipline that makes those fantasies coherent.

The website serves four purposes:

1. Establish Kessoku as the portfolio-level brand.
2. Give Super Soldiers and Heist City distinct identities.
3. Communicate active development without exposing unstable internal detail.
4. Create a foundation for screenshots, trailers, playtests, devlogs, press, and recruitment.

## 2. Non-negotiable product principles

- The homepage is a studio portfolio, not an architecture document.
- Player consequence is the public message; server authority is the supporting mechanism.
- Super Soldiers and Heist City must not look like color variants of one template.
- Navigation must remain understandable on desktop and mobile.
- Interactive features must support the games' narratives, not behave like unrelated dashboards.
- The site must remain deployable on Streamlit Community Cloud without a separate frontend build.
- No unofficial URLs, invented social destinations, fake metrics, or false release promises may be published.

## 3. Brand architecture

### 3.1 Kessoku

Kessoku is restrained, geometric, editorial, and premium.

- Base: near black, warm ivory, neutral steel greys.
- Motion: slow, deliberate, low-amplitude.
- Shape language: grids, circles, hard alignment, controlled asymmetry.
- Voice: direct, concise, consequential.
- Avoid: generic neon cyberpunk, excessive glassmorphism, cartoon gaming motifs, and gratuitous glitch.

### 3.2 Super Soldiers

- Accent: electric cyan with controlled warning red.
- Visual references: tactical overlays, operation codes, scan lines, arena diagrams, weapon silhouettes.
- Emotional target: speed, pressure, precision, teamwork.
- Copy should focus on player action, not implementation terminology.

### 3.3 Heist City

- Accent: amber, asphalt, police blue, selective criminal red.
- Visual references: street grids, dispatch displays, pursuit routes, surveillance, faction dossiers.
- Emotional target: opportunity, escalation, pursuit, ambiguity.
- Each alignment must alter the page's visual and information state.

## 4. Information architecture

### Home

- Cinematic Kessoku hero.
- Two large project showcases.
- Studio manifesto.
- High-level development signal.
- Final playtest/social CTA once official destinations exist.

### Super Soldiers

- Game hero and approved gameplay media.
- Combat pillars.
- 5v5 Arena / City of Zombies operation selector.
- Mode facts and tactical profile.
- Character, class, weapon, and ability modules when content is approved.
- Screenshots or short gameplay loops.
- Public roadmap and playtest CTA.

### Heist City

- City hero and approved gameplay media.
- Living-city pillars.
- Criminal / Police / Vigilante selector.
- Driving, pursuit, hacking, progression, and wanted-system modules.
- Interactive city/pursuit visualization.
- Screenshots, city map, and faction media.
- Public roadmap and playtest CTA.

### Studio

- Studio statement.
- Operating principles.
- Technology stack at a high level.
- Contact, press, and social destinations after confirmation.

## 5. Visual system

### Typography

Use three roles:

- Display: compressed, expressive, and used sparingly for game names and hero statements.
- Body: neutral sans-serif with excellent mobile readability.
- Technical labels: monospace or tracked uppercase for metadata only.

Do not use uppercase for every paragraph or control. Hierarchy depends on contrast between display, body, and metadata.

### Spacing

- Desktop content width: approximately 1,280–1,420 px.
- Hero height: 70–80 viewport height where practical.
- Major section spacing: 64–128 px depending on viewport.
- Card gaps: 12–20 px.
- Mobile edge padding: 16 px minimum.

### Components

- Sticky or persistent navigation with a compact mobile layout.
- Full-bleed or near-full-width game media.
- Editorial project panels rather than dashboard cards.
- Segmented mode/faction controls.
- Media-backed information modules.
- Distinct CTAs with game-specific accents.
- Visible keyboard focus and reduced-motion behavior.

## 6. Interaction system

Implemented in the initial V2 branch:

- Query-string-backed route state.
- Horizontal option menu.
- Super Soldiers mode selector.
- Heist City alignment selector.
- Plotly radar profiles.
- Interactive pursuit progression.
- Altair roadmap.
- Local Lottie signal animation.
- Cached procedural media generation.

Future interactions:

- Full-screen media viewer.
- Short muted gameplay loops with poster fallback.
- Interactive Heist City district map.
- Devlog filtering.
- Playtest registration form.
- Optional lightweight analytics.

## 7. Python implementation architecture

### Streamlit

Owns application composition, state, caching, deployment, and responsive content flow.

### streamlit-option-menu

Provides compact portfolio navigation while the project remains inside one Streamlit entry point.

### streamlit-extras

Provides scoped component styling without globally coupling every button to one visual treatment.

### streamlit-lottie

Provides a lightweight local signal animation without loading remote animation assets.

### Plotly

Used for game-state visualizations requiring hover and dynamic updates:

- Tactical profile radar.
- Heist City pursuit simulation.

### Altair

Used for compact declarative development-track visualization.

### Pandas and NumPy

Used to construct visualization data and deterministic procedural layouts.

### Pillow

Generates cached local WebP art-direction placeholders until approved key art and screenshots are supplied.

### Pydantic

Validates all game, mode, alignment, and metric content at import time. Invalid content must fail early rather than render partially.

## 8. Performance budget

- Initial Python dependencies should remain below the level that materially harms Streamlit cold start.
- Procedural images must be cached.
- No high-frequency autorefresh loop.
- No continuous server-side animation reruns.
- Prefer CSS or client-rendered Lottie motion.
- Approved images should use WebP or AVIF where browser support permits.
- Hero images should normally remain below 500 KB.
- Gallery images should be lazy-loaded or rendered only on the active view.
- Avoid loading large datasets, maps, or external APIs on the landing page.

## 9. Accessibility

- Maintain WCAG AA contrast for body copy and controls.
- Preserve visible keyboard focus.
- Do not encode meaning by color alone.
- Respect `prefers-reduced-motion`.
- Keep body copy at readable sizes on narrow mobile screens.
- Provide alt text for every final screenshot and piece of key art.
- Captions or transcripts are required for trailers with meaningful audio.

## 10. Content policy

Public copy should describe player experience. Internal architecture terminology belongs in the Studio section, devlogs, or technical documentation.

Preferred:

> Every chase, shot and collision belongs to the same living city.

Avoid as primary marketing copy:

> All gameplay state is processed by a deterministic fixed-step server-authority rail.

Both statements can be true; only the first sells the fantasy.

## 11. Required approved assets

Priority 0:

- Kessoku logo and wordmark.
- Super Soldiers hero screenshot or key art.
- Heist City hero screenshot or key art.
- Favicon and Open Graph image.

Priority 1:

- Three to six screenshots per game.
- One short muted gameplay loop per game.
- Super Soldiers mode art.
- Heist City alignment art.

Priority 2:

- Character/class art.
- Weapon/ability icons.
- City map or district diagram.
- Press kit assets.

## 12. Delivery phases

### Phase A — implemented in this branch

- Modular codebase.
- New visual system.
- Interactive game pages.
- Data validation.
- Procedural placeholder media.
- Responsive and reduced-motion support.
- Updated dependencies and documentation.

### Phase B — approved media integration

- Replace procedural posters.
- Add logos and favicon.
- Add screenshot galleries.
- Add short video loops.
- Tune copy against actual gameplay visuals.

### Phase C — publishing surface

- Add official Roblox, Discord, YouTube, press, and playtest URLs.
- Add devlog content model.
- Add Open Graph metadata and custom domain.
- Add privacy terms if user data is collected.

### Phase D — frontend migration decision

Remain on Streamlit while the site is primarily a portfolio and interactive product prototype. Re-evaluate Astro or Next.js when SEO, advanced page transitions, large editorial archives, structured analytics, or highly controlled browser rendering become business requirements.

## 13. Definition of done for V2

- The site communicates both games within three seconds.
- Each game has a distinct identity.
- Navigation works on desktop and mobile.
- Interactive controls materially change the content state.
- No invented links or release claims exist.
- The app starts cleanly on Python 3.12.
- Dependencies are pinned to compatible major versions.
- Procedural assets are cached.
- The branch has a documented replacement path for all placeholder media.
