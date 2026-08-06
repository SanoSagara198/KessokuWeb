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
- Public content must explain the player fantasy, objective, tactical phases, shared combat authority and mode-specific pressure.

### 3.3 Heist City

- Accent: amber, criminal red, police blue and vigilante green.
- Visual references: street grids, surveillance, pursuit routes, dispatch language, evidence, infrastructure and vehicle movement.
- Emotional target: opportunity, escalation, prediction, consequence.
- Public content must explain the shared city, three alignments, pursuit doctrine, evidence, progression and systemic response.

## 4. Information architecture

### Home

- Kessoku hero and portfolio statement
- factual structural statistics
- project showcases
- interactive world comparison
- studio manifesto
- public development signal

### Super Soldiers

- cinematic hero and project art
- long-form experience statement
- six design pillars
- operation selector
- tactical profile
- five-stage player loop
- combat-pressure laboratory
- system dossiers
- public authority topology
- roadmap

### Heist City

- cinematic hero and project art
- long-form living-city statement
- six design pillars
- alignment dossiers
- alignment progression and consequences
- five-stage player loops
- system dossiers
- 2D pursuit visualization
- 3D synthetic city grid
- proportional response simulator
- 24-skill progression catalog
- roadmap

### Studio

- Kessoku operating model
- six architectural principles
- public system topology
- package-responsibility catalog
- truthful contact state

## 5. Interaction policy

Every interaction must do one of the following:

- compare player roles
- expose a tactical or systemic relationship
- explain progression
- show consequence
- clarify architecture

Interactions must not exist solely to make the page move. Charts and simulators are design communication instruments, not live telemetry.

## 6. Content model

The site uses immutable Pydantic models for:

- games
- modes
- alignments
- metrics
- story beats
- system detail blocks
- skill categories and skills
- public development updates

Long-form descriptions are organized around:

- fantasy
- objective
- repeated loop
- progression
- methods
- consequences
- system ownership

This structure supports future localization and prevents page layout code from becoming the source of product truth.

## 7. Visual system

### Typography

- Display typography carries the identity.
- Body typography prioritizes long-form readability.
- Monospace is reserved for system labels, codes and metadata.
- Uppercase is not applied to all prose.

### Layout

The page alternates between:

- full-width hero moments
- editorial splits
- stat rails
- interactive visualizations
- compact feature grids
- five-stage story sequences
- expandable system dossiers

The site must avoid a continuous wall of equally weighted cards.

### Motion

- slow orbit and signal motion
- subtle hover elevation
- restrained chart transitions
- no mandatory animation for comprehension
- complete reduced-motion override

## 8. Accessibility

- Maintain keyboard-visible focus.
- Preserve readable contrast.
- Do not encode meaning only with color.
- Keep descriptions available outside charts.
- Stack multi-column structures on mobile.
- Disable or reduce motion when requested.
- Avoid hover-only essential content.

## 9. Performance and runtime

- Procedural media is cached.
- No remote API is required to render a page.
- No analytics SDK is embedded.
- PyDeck uses a synthetic grid with no external map style.
- Plotly and Altair figures remain bounded in size.
- No unbounded dataframe or live game-server query enters the public site.

## 10. Dependency responsibilities

- Streamlit: runtime, layout, state and deployment.
- streamlit-option-menu: compact portfolio navigation.
- streamlit-extras: narrowly scoped CTA styling.
- streamlit-lottie: local restrained motion.
- Plotly: tactical, pursuit, doctrine, topology and skill visualizations.
- Altair and Pandas: public roadmap presentation.
- PyDeck: synthetic 3D city volume.
- NetworkX: deterministic public topology layout.
- NumPy and Pillow: cached procedural WebP art direction.
- Pydantic: immutable validated content.

## 11. Media policy

The procedural posters are placeholders. They must eventually be replaced with approved:

- Kessoku wordmark
- Super Soldiers key art
- Heist City key art
- screenshots
- short muted gameplay loops
- mode and alignment icons
- Open Graph image

Do not invent Roblox, Discord, YouTube, press, playtest or social URLs.

## 12. Public-claim policy

The site may publish structural facts represented by the content model, such as two projects, two Super Soldiers operations, three Heist City alignments and a 24-node progression design.

The site must not publish fabricated:

- concurrent users
- retention
- revenue
- release dates
- performance claims
- live balance data
- implementation status not supported by the projects

## 13. Definition of done

Before merge:

- all four routes render
- navigation survives refresh
- all selectors and sliders update correctly
- Plotly, Altair and PyDeck render on Community Cloud
- no deprecated `use_container_width` calls remain
- mobile layout is reviewed
- reduced-motion behavior is reviewed
- long copy is not clipped
- procedural media is identified as temporary
- no unsupported external links or product claims are present

## 14. V2.1 extension

The detailed V2.1 feature, content and validation specification is stored in `docs/KESSOKU_WEBSITE_V2_1_FEATURES.md`.
