# Kessoku Games Website V2

A cinematic, interactive Streamlit site for **Kessoku Games**, **Super Soldiers**, and **Heist City**.

## What changed in V2

- Replaced the dashboard-like presentation with an editorial game-studio layout.
- Added distinct visual systems for Super Soldiers and Heist City.
- Added query-string-backed navigation so views can be shared.
- Added interactive operation and alignment selectors.
- Added Plotly radar profiles and a Heist City pursuit visualization.
- Added Altair roadmap visualization.
- Added cached procedural WebP art through Pillow and NumPy.
- Added Pydantic content validation.
- Added a local Lottie signal animation.
- Added reduced-motion support and a responsive mobile layout.

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
docs/KESSOKU_WEBSITE_V2.md
```

## Media policy

The current build uses procedural art-direction placeholders. Replace them with approved game screenshots, key art, logos, and short gameplay loops as soon as those assets are available. Do not publish invented Roblox, Discord, YouTube, press, or playtest links.
