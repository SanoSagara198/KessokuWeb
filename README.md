# Kessoku Games — Streamlit website

A responsive, deployable studio website for **Kessoku Games**, featuring dedicated pages for **Super Soldiers** and **Heist City**.

## Included

- Kessoku landing page
- Super Soldiers project page with interactive mode brief
- Heist City project page with interactive alignment brief
- Studio principles page
- Responsive layout for desktop and mobile
- Custom CSS visual system with no external asset dependency
- Streamlit Community Cloud configuration

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app from the repository.
3. Set the entry point to `app.py`.

## Content changes

Project copy is defined near the top of `app.py` in the `SUPER_SOLDIERS` and `HEIST_CITY` data objects. Update those objects to change descriptions, pillars, status, and roadmap entries.

Official Roblox, Discord, press, social, or playtest URLs were not supplied, so this starter does not invent public links. Add them only after confirming the canonical destinations.

## Architecture note

This is a presentation site. It does not connect to Roblox DataStores, game servers, or private operational systems. Public live statistics should be exposed through a separate validated API rather than embedded credentials or direct data access in Streamlit.
