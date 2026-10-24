"""Private planning console for KessokuWeb (Streamlit multipage).

No canonical mission data in the public repository. ZIP uploads are validated
in memory, review results exported explicitly, no Roblox/GitHub write access.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from collections import Counter

import pandas as pd
import streamlit as st

from kessoku_site.city_ops_catalog import (
    STATES,
    audit_catalog,
    load_catalog_zip,
    mission_rows,
    review_export,
)

st.set_page_config(page_title="HeistCity Operations · Kessoku Games", page_icon="🗺️", layout="wide")


def required_password() -> str | None:
    # Community Cloud: configure in App Settings -> Secrets, not source control.
    try:
        secret = st.secrets.get("HEISTCITY_ADMIN_PASSWORD")
    except Exception:
        secret = None
    if secret:
        return str(secret)
    return os.environ.get("HEISTCITY_ADMIN_PASSWORD") or None


secret = required_password()
if not secret:
    st.error("Operations console disabled: configure HEISTCITY_ADMIN_PASSWORD in Streamlit secrets.")
    st.stop()
if not st.session_state.get("heistcity_ops_authenticated", False):
    st.title("HeistCity · Operations Console")
    st.caption("Private planning workspace. No production access; no telemetry or live asset control.")
    with st.form("heistcity_login", clear_on_submit=True):
        supplied = st.text_input("Admin passphrase", type="password")
        submitted = st.form_submit_button("Unlock")
    if submitted:
        if hmac.compare_digest(hashlib.sha256(supplied.encode("utf-8")).digest(),
                               hashlib.sha256(secret.encode("utf-8")).digest()):
            st.session_state.heistcity_ops_authenticated = True
            st.rerun()
        st.error("Incorrect credentials")
    st.stop()

head, logout_col = st.columns([6, 1])
with head:
    st.title("HeistCity · Living City Operations")
    st.caption("Design inventory, dependency audit and authoring review. Not live Roblox state.")
with logout_col:
    if st.button("Sign out", width="stretch"):
        for k in ("heistcity_ops_authenticated", "hc_catalog", "hc_upload_hash", "hc_mission_review", "hc_facility_review"):
            st.session_state.pop(k, None)
        st.rerun()

with st.expander("Data provenance and security", expanded=False):
    st.write("Upload the private **NewCity_600_missions** ZIP from your machine. The website repository contains **no** private mission dataset, passwords, or Studio tokens. All data stays in this server session; review edits download as JSON. The tool cannot publish a Roblox place, update GitHub, or attest that a facility is built.")
    st.warning("The shared-passphrase gate is a prototype, not individual accounts, MFA, audit logging, or production authorization. Use private deployment and proper identity controls before broader access.")

archive = st.file_uploader("Import private NewCity catalog ZIP", type=["zip"], help="ZIP must contain the canonical facility_program.json and mission_seed_catalog.json.")
if archive is not None:
    raw = archive.getvalue()
    digest = hashlib.sha256(raw).hexdigest()
    if st.session_state.get("hc_upload_hash") != digest:
        try:
            model = load_catalog_zip(raw)
        except ValueError as exc:
            st.error(f"Import rejected: {exc}")
            st.stop()
        st.session_state.hc_catalog = model
        st.session_state.hc_upload_hash = digest
        st.session_state.hc_mission_review = {}
        st.session_state.hc_facility_review = {}
        st.success(f"Catalog loaded: {len(model.missions)} mission proposals and {len(model.families)} facility families")

catalog = st.session_state.get("hc_catalog")
if catalog is None:
    st.info("Upload the NewCity ZIP to inspect the mission and facility program. No catalog is publicly hosted.")
    st.stop()

report = audit_catalog(catalog)
summary = st.columns(5)
for column, (title, value) in zip(summary, [
    ("Missions", report["mission_count"]), ("Issuers", report["issuer_count"]),
    ("Campaign arcs", report["campaign_count"]), ("Facility families", report["facility_families"]),
    ("Referenced families", report["covered_families"]),
]):
    column.metric(title, value)

mission_tab, facility_tab, quality_tab = st.tabs(["Mission board", "Facility program", "Quality and dependencies"])
with mission_tab:
    records = mission_rows(catalog, st.session_state.hc_mission_review)
    issuer_options = sorted({r["Issuer"] for r in records})
    types = sorted({r["Mode"] for r in records})
    a, b, c = st.columns([1.3, 1, 1])
    with a:
        query = st.text_input("Search missions, IDs, facility or campaign", placeholder="e.g. Derby, rail, Obsessives...")
    with b:
        issuer_filter = st.selectbox("Issuing organization", ["All", *issuer_options])
    with c:
        mode_filter = st.selectbox("Mode", ["All", *types])
    visible = [r for r in records if
        (issuer_filter == "All" or r["Issuer"] == issuer_filter) and
        (mode_filter == "All" or r["Mode"] == mode_filter) and
        (not query or query.casefold() in " ".join(str(x) for x in r.values()).casefold())]
    st.caption(f"Showing {min(250, len(visible)):,} of {len(visible):,} matching missions. Filter to edit another subset. Edit status is **planning only**.")
    view = pd.DataFrame(visible[:250])
    if not view.empty:
        edited = st.data_editor(
            view,
            width="stretch",
            hide_index=True,
            key="hc_mission_editor",
            disabled=["ID", "Title", "Issuer", "Campaign", "Tier", "Mode", "Facilities", "Stages"],
            column_config={"Review status": st.column_config.SelectboxColumn("Review status", options=list(STATES)),
                           "Notes": st.column_config.TextColumn("Notes", max_chars=1000)},
        )
        if st.button("Save visible mission reviews in session"):
            changes = st.session_state.hc_mission_review
            for row in edited.to_dict(orient="records"):
                mid = row["ID"]
                changes[mid] = {"status": str(row["Review status"]), "notes": str(row["Notes"] or "")[:1000]}
            st.success(f"Saved {len(edited)} reviewed rows in this session. Download below to persist.")
    st.download_button("Download mission review overlay (JSON)",
                       data=review_export(catalog, st.session_state.hc_mission_review),
                       file_name="newcity_mission_review_overlay.json", mime="application/json")

with facility_tab:
    st.write("These are **planned facility families** and coverage targets, not verified placed buildings.")
    regions = Counter(str(region) for f in catalog.families for region in f.get("preferredRegions", []))
    st.bar_chart(pd.DataFrame([{"Region": k, "Family references": v} for k, v in sorted(regions.items())]).set_index("Region"))
    families = []
    for f in catalog.families:
        families.append({"ID": f["familyId"], "Family": f.get("label", ""),
                         "Group": f.get("group", ""), "Min": f.get("desiredRange", {}).get("min", 0),
                         "Max": f.get("desiredRange", {}).get("max", 0),
                         "Phase": f.get("phase", ""), "Regions": ", ".join(f.get("preferredRegions", [])),
                         "Review status": st.session_state.hc_facility_review.get(f["familyId"], {}).get("status", "NOT_VERIFIED"),
                         "Notes": st.session_state.hc_facility_review.get(f["familyId"], {}).get("notes", "")})
    facility_search = st.text_input("Search facility program", placeholder="e.g. hospital, stadium, fire...")
    shown = [f for f in families if not facility_search or facility_search.casefold() in " ".join(str(x) for x in f.values()).casefold()]
    if shown:
        facility_edit = st.data_editor(pd.DataFrame(shown), width="stretch", hide_index=True,
            key="hc_facility_editor", disabled=["ID", "Family", "Group", "Min", "Max", "Phase", "Regions"],
            column_config={"Review status": st.column_config.SelectboxColumn("Review status", options=["NOT_VERIFIED", "SITE_RESERVED", "EXTERIOR_ONLY", "ACCESS_VERIFIED", "OPERATIONAL", "ADVANCED"]),
                           "Notes": st.column_config.TextColumn("Notes", max_chars=1000)})
        if st.button("Save visible facility reviews in session"):
            for row in facility_edit.to_dict(orient="records"):
                st.session_state.hc_facility_review[row["ID"]] = {"status": str(row["Review status"]), "notes": str(row["Notes"] or "")[:1000]}
            st.success("Facility review saved in this session")
    facility_download = {"schema": "NewCityFacilityReviewOverlay", "version": 1,
                         "reviews": [{"familyId": k, **v} for k, v in sorted(st.session_state.hc_facility_review.items())]}
    import json
    st.download_button("Download facility review overlay (JSON)", data=json.dumps(facility_download, indent=2),
                       file_name="newcity_facility_review_overlay.json", mime="application/json")

with quality_tab:
    issues = [
        ("Unknown facility dependencies", len(report["unknown_facilities"]), report["unknown_facilities"][:15]),
        ("Missions without stages", len(report["missing_stages"]), report["missing_stages"][:15]),
        ("Stages missing completion witness", len(report["missing_witness"]), report["missing_witness"][:15]),
    ]
    for title, count, examples in issues:
        if count:
            st.error(f"{title}: {count}. Examples: {examples}")
        else:
            st.success(f"{title}: none detected")
    st.subheader("Missions by issuer")
    st.bar_chart(pd.DataFrame([{"Issuer": k, "Missions": v} for k, v in report["issuer_counts"].most_common()]).set_index("Issuer"))
    st.subheader("Objective completion witnesses")
    st.bar_chart(pd.DataFrame([{"Witness": k, "Stages": v} for k, v in report["stage_witness_counts"].most_common()]).set_index("Witness"))
    st.warning("Passing these checks does NOT mean a facility is authored, an AI system is wired, a mission is playable, or a server payout has been tested. Review the integration prerequisites before setting READY_FOR_IMPLEMENTATION.")