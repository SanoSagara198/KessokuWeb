# Kessoku Games Website V2.1

A cinematic, interactive Streamlit portfolio for **Kessoku Games**, **Super Soldiers**, and **Heist City**.

## Current experience

### Global presentation

- Premium editorial dark-mode design system
- Sticky glass Kessoku identity bar
- Shareable query-backed navigation
- Responsive desktop and mobile layouts
- Reduced-motion accessibility support
- Cached procedural WebP art direction with no remote media dependency
- Explicit public roadmap and development-signal cards

### Super Soldiers

- Detailed 5v5 Arena and City of Zombies dossiers
- Player fantasy, objective, public facts and five-stage tactical loops
- Interactive tactical-profile radar
- Combat-pressure laboratory with threat intensity and squad posture
- Expandable combat-system descriptions
- Public server-authority topology

### Heist City

- Detailed Criminal, Police and Vigilante alignment dossiers
- Progression, methods, consequences and five-stage role loops
- Two-dimensional predictive pursuit visualization
- PyDeck synthetic 3D city grid
- Threat/evidence/mobility response-doctrine simulator
- Complete 24-skill Hacking, Combat, Driving and Intelligence catalog
- Interactive progression sunburst and category dossiers

### Studio

- Six operating principles
- Public server-authority topology
- Detailed package-responsibility catalog
- Truthful contact and media policy

## Python stack

- Streamlit
- streamlit-option-menu
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

Each library has a narrow responsibility. The site does not add packages solely for visual novelty.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Streamlit Community Cloud should use:

- Branch: `main` after review and merge
- Entry point: `app.py`
- Python: `3.12`

For preview testing, deploy `agent/pro-design-v2` as a separate temporary app.

## Repository structure

```text
app.py
assets/signal.json
kessoku_site/
  components.py
  content.py
  models.py
  theme.py
  visuals.py
docs/
  KESSOKU_WEBSITE_V2.md
  KESSOKU_WEBSITE_V2_1_FEATURES.md
```

## Public-data policy

Charts and simulators communicate design intent. They are not live telemetry, player counts, balance guarantees or release promises. Structural counts—two games, two Super Soldiers operations, three Heist City alignments and 24 planned skill nodes—are sourced directly from the published content model.

## Media policy

The current build uses procedural art-direction placeholders. Replace them with approved game screenshots, key art, logos and short gameplay loops as soon as those assets are available. Do not publish invented Roblox, Discord, YouTube, press or playtest links.
