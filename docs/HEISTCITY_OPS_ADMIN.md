# HeistCity Operations Console (Streamlit)

This repository is public. **Do not commit the private `NewCity` catalog or Streamlit secrets.** Add `pages/HeistCity_Operations.py` and `kessoku_site/city_ops_catalog.py` to the existing KessokuWeb app. Multipage Streamlit exposes a page link; page contents are gated by `HEISTCITY_ADMIN_PASSWORD` set in Streamlit Community Cloud secrets or locally in `.streamlit/secrets.toml` (already gitignored). No configured password means no access.

Local testing:

```toml
# .streamlit/secrets.toml -- NEVER COMMIT
HEISTCITY_ADMIN_PASSWORD = "a-long-random-passphrase"
```

```bash
pip install -r requirements.txt
streamlit run app.py
```

Use the **NewCity_600_missions_2026-10-24.zip** in the upload widget; page validates mission IDs, facility IDs, archive sizes, and stages. It displays mission counts, issuers, campaigns, witness coverage, facility distribution, searchable catalog and in-session review status/notes. Download mission and facility review overlays as JSON when finished. **No web changes directly affect gameplay or Studio.** A developer must review the exported overlays and translate approved records into source-authorized content builds.

This password-only model is appropriate only for personal prototype use behind controlled deployment. Before real collaboration or write actions add per-user OIDC authentication, role-based authorization, access log, revision-safe persistence, approval workflow, separated stage/prod environments, explicit evidence required for operational facility status, and audited rollback. Streamlit session state is not a durable database and should not be used as one.