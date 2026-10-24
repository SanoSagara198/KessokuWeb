"""Offline NewCity catalog inspection. No API calls, credentials or server writes.

The admin view accepts the PRIVATE NewCity ZIP by upload; no mission catalog is
checked into the public website repository.
"""
from __future__ import annotations

import io
import json
import zipfile
from collections import Counter
from dataclasses import dataclass
from typing import Any

MAX_ZIP_BYTES = 10 * 1024 * 1024
MAX_FILE_BYTES = 5 * 1024 * 1024
MISSION_SUFFIX = "/data/mission_seed_catalog.json"
FACILITY_SUFFIX = "/data/facility_program.json"
STATES = ("DRAFT", "REVIEW", "BLOCKED", "READY_FOR_IMPLEMENTATION", "IMPLEMENTED", "STUDIO_VERIFIED")


@dataclass(frozen=True)
class Catalog:
    missions: tuple[dict[str, Any], ...]
    issuers: tuple[str, ...]
    families: tuple[dict[str, Any], ...]
    schema: str
    version: int


def _read_json(zf: zipfile.ZipFile, suffix: str) -> dict[str, Any]:
    matches = [f for f in zf.infolist() if f.filename.endswith(suffix) and not f.is_dir()]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one file ending {suffix}, found {len(matches)}")
    member = matches[0]
    if member.file_size > MAX_FILE_BYTES or member.file_size <= 0:
        raise ValueError(f"Unsafe or empty catalog file: {member.filename}")
    with zf.open(member) as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("Catalog file exceeds size limit")
    doc = json.loads(data.decode("utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("Catalog root must be an object")
    return doc


def load_catalog_zip(payload: bytes) -> Catalog:
    if len(payload) > MAX_ZIP_BYTES or not payload:
        raise ValueError("ZIP exceeds 10 MB (or is empty)")
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as zf:
            if len(zf.infolist()) > 150:
                raise ValueError("Archive contains too many files")
            mission_doc = _read_json(zf, MISSION_SUFFIX)
            facility_doc = _read_json(zf, FACILITY_SUFFIX)
    except (zipfile.BadZipFile, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid NewCity archive: {exc}") from exc
    missions = mission_doc.get("missions")
    families = facility_doc.get("families")
    issuers = mission_doc.get("issuers")
    if not isinstance(missions, list) or not isinstance(families, list):
        raise ValueError("Required mission/facility arrays are missing")
    if not isinstance(issuers, list) or not all(isinstance(x, str) for x in issuers):
        raise ValueError("Issuer IDs are missing or invalid")
    missions = tuple(_validated_dicts(missions, "mission"))
    families = tuple(_validated_dicts(families, "facility"))
    normalized_issuers = tuple(issuers)
    identifiers = [m.get("templateId") for m in missions]
    if any(not isinstance(i, str) or not i for i in identifiers) or len(identifiers) != len(set(identifiers)):
        raise ValueError("Mission IDs must be nonempty and unique")
    facility_ids = [f.get("familyId") for f in families]
    if any(not isinstance(i, str) or not i for i in facility_ids) or len(facility_ids) != len(set(facility_ids)):
        raise ValueError("Facility family IDs must be nonempty and unique")
    return Catalog(missions=missions, issuers=normalized_issuers,
                   families=families, schema=str(mission_doc.get("schema", "unknown")),
                   version=int(mission_doc.get("version", 0)))


def _validated_dicts(items: Any, label: str):
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Invalid {label} #{index}: expected object")
        yield item


def mission_rows(catalog: Catalog, review: dict[str, dict[str, str]] | None = None) -> list[dict[str, Any]]:
    review = review or {}
    output = []
    for m in catalog.missions:
        mid = m["templateId"]
        row_review = review.get(mid, {})
        output.append({
            "ID": mid,
            "Title": str(m.get("title") or ""),
            "Issuer": str(m.get("issuerOrgId") or ""),
            "Campaign": str(m.get("campaignId") or ""),
            "Tier": m.get("tier", 0),
            "Mode": str(m.get("mode") or ""),
            "Facilities": ", ".join(m.get("facilityFamilies") or []),
            "Stages": len(m.get("stages") or []),
            "Review status": row_review.get("status", "DRAFT"),
            "Notes": row_review.get("notes", ""),
        })
    return output


def audit_catalog(catalog: Catalog) -> dict[str, Any]:
    known = {f["familyId"] for f in catalog.families}
    unknown = []
    no_stages = []
    no_witness = []
    story = Counter()
    mode_counts = Counter()
    for m in catalog.missions:
        mid = m["templateId"]
        unknown.extend((mid, fid) for fid in m.get("facilityFamilies", []) if fid not in known)
        stages = m.get("stages") or []
        if not stages:
            no_stages.append(mid)
        for st in stages:
            if not isinstance(st, dict) or not st.get("witnessType"):
                no_witness.append(mid)
        if m.get("campaignId"):
            story[str(m["campaignId"])] += 1
        mode_counts[str(m.get("mode", "UNCLASSIFIED"))] += 1
    # Facility families are design demand, NOT evidence of built sites.
    return {
        "mission_count": len(catalog.missions),
        "issuer_count": len(set(m.get("issuerOrgId") for m in catalog.missions)),
        "facility_families": len(catalog.families),
        "covered_families": len(known.intersection(
            fid for m in catalog.missions for fid in (m.get("facilityFamilies") or []))),
        "campaign_count": len(story),
        "unknown_facilities": unknown,
        "missing_stages": no_stages,
        "missing_witness": no_witness,
        "mode_counts": mode_counts,
        "issuer_counts": Counter(str(m.get("issuerOrgId")) for m in catalog.missions),
        "stage_witness_counts": Counter(str(s.get("witnessType")) for m in catalog.missions
                                        for s in m.get("stages", []) if isinstance(s, dict)),
    }


def review_export(catalog: Catalog, review: dict[str, dict[str, str]]) -> bytes:
    allowed_ids = {m["templateId"] for m in catalog.missions}
    records = []
    for mid in sorted(allowed_ids.intersection(review)):
        record = review[mid]
        state = record.get("status", "DRAFT")
        if state not in STATES:
            raise ValueError(f"Invalid status for {mid}")
        records.append({"templateId": mid, "status": state, "notes": str(record.get("notes", ""))[:1000]})
    return json.dumps({"schema": "NewCityMissionReviewOverlay", "version": 1,
                       "sourceMissionCount": len(catalog.missions), "reviews": records},
                      ensure_ascii=False, indent=2).encode("utf-8")