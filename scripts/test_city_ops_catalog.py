"""Pure offline tests for the KessokuWeb NewCity catalog importer."""
import io
import json
import unittest
import zipfile

from kessoku_site.city_ops_catalog import load_catalog_zip, audit_catalog, review_export


def sample():
    root = "NewCity/docs/planning/living-city/data/"
    docs = {
        root + "mission_seed_catalog.json": {"schema": "NewCityMissionCatalog", "version": 1,
            "issuers": ["crime.dark_eye"], "missions": [{
                "templateId": "demo.01", "title": "Test",
                "issuerOrgId": "crime.dark_eye", "facilityFamilies": ["civic"],
                "stages": [{"witnessType": "SERVER_VERIFIED"}]}]},
        root + "facility_program.json": {"families": [{"familyId": "civic", "label": "Civic center"}]},
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path, obj in docs.items():
            z.writestr(path, json.dumps(obj))
    return buf.getvalue()


class CityOpsCatalogTests(unittest.TestCase):
    def test_import_audit(self):
        cat = load_catalog_zip(sample())
        self.assertEqual(len(cat.missions), 1)
        self.assertEqual(audit_catalog(cat)["unknown_facilities"], [])

    def test_invalid_zip_rejected(self):
        with self.assertRaises(ValueError):
            load_catalog_zip(b"invalid")

    def test_review_only_known_missions(self):
        cat = load_catalog_zip(sample())
        out = json.loads(review_export(cat, {"demo.01": {"status": "REVIEW"},
                                          "injected": {"status": "IMPLEMENTED"}}))
        self.assertEqual(len(out["reviews"]), 1)
        self.assertEqual(out["reviews"][0]["templateId"], "demo.01")


if __name__ == "__main__":
    unittest.main()
