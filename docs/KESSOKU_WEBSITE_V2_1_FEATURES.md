# Kessoku Website V2.1 — Professional Design and Interaction Expansion

## Purpose

V2.1 moves the site beyond a polished portfolio shell and turns it into a deep public product presentation. The site must remain cinematic and editorial while giving visitors enough material to understand what each game asks the player to do, how the systems create consequence, and why Kessoku's engineering direction matters.

The governing rule remains unchanged: player fantasy leads; architecture explains why the fantasy can remain coherent.

## Design objectives

1. Increase visual hierarchy and rhythm without creating generic dashboard density.
2. Replace short descriptions with structured dossiers that explain player fantasy, objective, loop, progression, systems and consequences.
3. Add interactions that are native to each game rather than decorative widgets.
4. Keep all numerical outputs explicitly framed as design profiles, not live telemetry or promises.
5. Preserve a bounded Streamlit Community Cloud runtime with cached media and no remote API dependency.
6. Maintain mobile readability, keyboard access and reduced-motion behavior.

## New global design system

### Sticky glass navigation

The Kessoku identity remains visible while scrolling. The navigation surface uses a restrained translucent treatment, strong focus contrast and compact spacing. It must never obscure content or become a large application toolbar.

### Cinematic hero depth

The hero now combines:

- grid perspective
- local color atmosphere
- orbit motion
- crosshair geometry
- a verified-world-state signal panel
- editorial typography

All animation is disabled or reduced when the operating system requests reduced motion.

### Portfolio statistics

The site uses factual structural counts only: number of games, modes, alignments and planned skill nodes. It does not display fabricated player counts, revenue, engagement or release dates.

### Editorial dossiers

Detailed content is split into:

- player fantasy
- long-form description
- operational objective
- repeated player loop
- methods and consequences
- system explanations
- high-level development state

This structure keeps long copy scannable and makes future localization practical.

## Homepage expansion

The homepage now communicates:

- Kessoku portfolio scale and shared rule
- distinct world identities
- interactive world selection
- detailed long-form project descriptions
- public development updates
- roadmap state without dates

The homepage should answer four questions quickly:

1. Who is Kessoku?
2. What games are being built?
3. What does each game feel like?
4. Why should the worlds remain coherent under pressure?

## Super Soldiers expansion

### Operation dossiers

Both 5v5 Arena and City of Zombies now contain:

- player fantasy
- exhaustive mode description
- explicit objective
- four stable public facts
- tactical profile radar
- five-stage player loop
- detailed system dossiers

### Combat pressure laboratory

Visitors can adjust threat intensity and squad posture. The visualization shows the relationship between tactical load and squad capability. This is a design communication instrument, not live balance telemetry.

The feature exists to explain that difficulty is not simply enemy quantity. Pressure is produced by timing, position, composition, resource state and the team's chosen posture.

### Authority topology

A NetworkX-generated Plotly graph explains the intended ownership flow:

- player and bot intent
- server-authored input actions
- fixed simulation
- combat and vehicle resolution
- world state
- replication
- client presentation
- supervisory lifecycle ownership

The public diagram avoids implementation-sensitive names and shows only the architectural contract.

## Heist City expansion

### Alignment dossiers

Criminal, Police and Vigilante now each include:

- fantasy
- long-form role description
- objective
- progression model
- methods
- consequences
- tactical profile
- five-stage gameplay loop
- detailed system explanations

Alignment is presented as a different relationship with the same city, not as three disconnected game modes.

### Pursuit visualization

The existing two-dimensional pursuit model remains because it clearly communicates route prediction. It is supplemented by a PyDeck 3D synthetic city grid showing:

- bounded blocks
- independent target and police paths
- vertical city volume
- interception geometry

The grid is explicitly labeled as a design visualization, not a live map.

### Response doctrine simulator

Threat, evidence and mobility alter the relative emphasis assigned to:

- patrol
- pursuit
- containment
- investigation

The generated doctrine text explains why police behavior should change. This supports the goal of proportional, intelligent response instead of immediate maximum-force pursuit.

### 24-skill progression catalog

The Heist City skill architecture now contains four categories with six skills each:

- Hacking
- Combat
- Driving
- Intelligence

The Plotly sunburst gives visitors a complete portfolio view. A category dossier then explains every skill, its tier and the new decision it is intended to create.

Skills must not claim implementation status unless the game actually supports them. The website describes progression architecture and should be revised as production scope changes.

## Studio expansion

The Studio page now presents:

- six operating principles
- a public server-authority topology
- explicit package responsibilities
- the distinction between many bounded servers and one unbounded server
- truthful public contact status

The technology section must explain why each dependency exists. Libraries are not displayed as trophies; each one must own a narrow presentation or validation responsibility.

## Runtime and dependency policy

V2.1 adds:

- `pydeck` for 3D city presentation
- `networkx` for deterministic topology layout

Existing packages retain explicit responsibilities:

- Streamlit: runtime and layout
- Plotly: interactive domain visualizations
- Altair and Pandas: roadmap presentation
- NumPy and Pillow: cached deterministic WebP placeholders
- Pydantic: immutable content validation
- Lottie and option-menu: restrained motion and navigation

No remote data source, analytics SDK or unverified external media host is introduced.

## Content quality standard

Every public feature description must answer at least one of these:

- What does the player do?
- What decision becomes available?
- What pressure or consequence does the system create?
- Why does the system belong to this game?
- What architectural rule keeps the outcome trustworthy?

Avoid vague claims such as "advanced AI," "next-generation combat" or "immersive world" unless the page explains the concrete behavior that supports the claim.

## Validation checklist

Before merge:

- Preview all four routes.
- Test every segmented control and slider.
- Confirm Plotly, Altair and PyDeck render on Streamlit Community Cloud.
- Confirm `width="stretch"` is used instead of deprecated container-width arguments.
- Test mobile layout at narrow width.
- Test reduced-motion preference.
- Check that long descriptions remain readable and do not create clipped panels.
- Confirm no fake external links or unsupported implementation claims appear.
- Confirm procedural art is clearly treated as temporary presentation media.
