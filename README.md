# Kessoku Games Website V2.3

A cinematic, interactive Streamlit portfolio for **Kessoku Games**, **Super Soldiers**, and **Heist City**.

## Current experience

### Global presentation

- Premium editorial dark-mode design system
- Sticky glass Kessoku identity surface
- Native query-backed navigation using `st.pills`
- Responsive desktop, tablet, and phone layouts
- Keyboard-visible focus states and reduced-motion support
- Cinematic campaign heroes with deterministic procedural fallbacks
- Hero metadata rails and project-signature panels
- Scroll-progress indicator and restrained studio marquee
- Public roadmap and development-signal cards
- Expanded studio footer with truthful public status

### Super Soldiers

- Detailed 5v5 Arena and City of Zombies dossiers
- Player fantasy, objective, public facts, and five-stage tactical loops
- Interactive tactical-profile radar
- Combat-pressure laboratory with threat intensity and squad posture
- Expandable combat-system descriptions
- Public server-authority topology
- Dedicated campaign-media slots for the project hero and both operations

### Heist City

- Detailed Criminal, Police, and Vigilante alignment dossiers
- Progression, methods, consequences, and five-stage role loops
- Two-dimensional predictive pursuit visualization
- PyDeck synthetic 3D city grid
- Threat/evidence/mobility response-doctrine simulator
- Complete 24-skill Hacking, Combat, Driving, and Intelligence catalog
- Interactive progression sunburst and category dossiers
- Campaign-media slots for the project hero and all three alignments

### Studio

- Six operating principles
- Public server-authority topology
- Detailed package-responsibility catalog
- Truthful contact and media policy
- Dedicated studio-manifesto campaign slot

## Python stack

- Streamlit
- streamlit-extras
- streamlit-lottie
- Plotly
- Altair
- PyDeck
- NetworkX
- Pandas
- NumPy
- Pillow
- Pydantic

Each library has a narrow responsibility. Primary navigation no longer depends on `streamlit-option-menu`; a local compatibility surface delegates to native Streamlit pills while preserving the route API.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Validate the repository

```bash
python scripts/validate_site.py
```

The validator checks Python syntax, deprecated Streamlit width usage, dependency cleanup, required files, media-manifest integrity, WebP payload validity, and the 1.5 MB media budget.

## Deploy

Streamlit Community Cloud should use:

- Branch: `main` after review and merge
- Entry point: `app.py`
- Python: `3.12`

For preview testing, deploy `agent/pro-design-v2` as a separate temporary app.

## Repository structure

```text
app.py
assets/
  signal.json
  media/
    manifest.json
kessoku_site/
  campaign.py
  components.py
  content.py
  editorial.py
  media.py
  models.py
  navigation.py
  polish.py
  theme.py
  visuals.py
scripts/
  validate_site.py
docs/
  IMAGE_ASSET_PROMPTS.md
  IMAGE_SHOT_LIST.md
  KESSOKU_WEBSITE_V2.md
  KESSOKU_WEBSITE_V2_1_FEATURES.md
  KESSOKU_WEBSITE_V2_3_EDITORIAL.md
  MEDIA_INTEGRATION.md
```

## Media behavior

Approved WebP files are loaded from `assets/media/`. The runtime also supports connector-safe Base64 representations and deterministic procedural fallback art. Missing or malformed media does not prevent the application from starting.

Use the exact filenames and placement rules in `assets/media/manifest.json`. Generation direction, continuity requirements, crops, and rejection criteria are documented in `docs/IMAGE_ASSET_PROMPTS.md` and `docs/IMAGE_SHOT_LIST.md`.

## Public-data policy

Charts and simulators communicate design intent. They are not live telemetry, player counts, balance guarantees, or release promises. Structural counts—two games, two Super Soldiers operations, three Heist City alignments, and 24 planned skill nodes—are sourced directly from the published content model.

## Public-link policy

Do not publish invented Roblox, Discord, YouTube, press, playtest, or contact destinations. Canonical links should be added only after they are confirmed.
