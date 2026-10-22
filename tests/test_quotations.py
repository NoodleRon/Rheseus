import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "verify_quotations.py"
SPEC = importlib.util.spec_from_file_location("verify_quotations", SCRIPT)
UTILITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UTILITY)


class QuotationTests(unittest.TestCase):
    def test_literal_text(self):
        self.assertEqual(UTILITY.compare_quote("Payment is due.", "Section 3. Payment is due.")["status"], "exact")

    def test_typography_and_line_breaks(self):
        result = UTILITY.compare_quote('The "fee" is due - today.', 'The “fee” is\ndue — today.')
        self.assertEqual(result["status"], "normalized")

    def test_negation_is_not_normalized_away(self):
        self.assertEqual(UTILITY.compare_quote("The owner may assign.", "The owner may not assign.")["status"], "not_found")

    def test_amount_change_is_not_accepted(self):
        self.assertEqual(UTILITY.compare_quote("The fee is $500.", "The fee is $50.")["status"], "not_found")

    def test_case_is_preserved(self):
        self.assertEqual(UTILITY.compare_quote("Company", "company")["status"], "not_found")

    def test_word_fragments_are_not_accepted(self):
        self.assertEqual(UTILITY.compare_quote("assign", "assignment")["status"], "not_found")
        self.assertEqual(UTILITY.compare_quote("notice", "prenotice")["status"], "not_found")

    def test_unicode_composition_is_normalized(self):
        self.assertEqual(UTILITY.compare_quote("café", "cafe\u0301")["status"], "normalized")

    def test_ordered_ellipsis_requires_review(self):
        self.assertEqual(UTILITY.compare_quote("The owner … may assign.", "The owner, with consent, may assign.")["status"], "segmented_review")

    def test_reordered_ellipsis_does_not_match(self):
        self.assertEqual(UTILITY.compare_quote("may assign. ... The owner", "The owner may assign.")["status"], "not_found")

    def test_brackets_require_review(self):
        self.assertEqual(UTILITY.compare_quote("[It] may assign.", "The owner may assign.")["status"], "manual_review")

    def test_ellipsis_without_text_is_not_match(self):
        self.assertEqual(UTILITY.compare_quote("...", "Anything")["status"], "manual_review")

    def test_empty_quote_is_invalid(self):
        with self.assertRaises(ValueError):
            UTILITY.compare_quote(" ", "Anything")

    def write_case(self, folder, file="source.txt", text="The owner may not assign."):
        root = Path(folder)
        (root / "source.txt").write_text(text, encoding="utf-8")
        payload = {"authorities": [{"id": "a", "file": file}], "quotations": [{"id": "q", "authority_id": "a", "text": text}]}
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps(payload), encoding="utf-8")
        return manifest, payload

    def test_manifest_only_reads_the_cited_source(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest, payload = self.write_case(folder)
            (Path(folder) / "other.txt").write_text("A different quotation.")
            payload["quotations"][0]["text"] = "A different quotation."
            manifest.write_text(json.dumps(payload))
            self.assertEqual(UTILITY.audit_manifest(manifest)["results"][0]["status"], "not_found")

    def test_traversal_and_absolute_paths_are_rejected(self):
        for value in ("../outside.txt", "/tmp/outside.txt"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as folder:
                manifest, _ = self.write_case(folder, file=value)
                with self.assertRaises(ValueError):
                    UTILITY.audit_manifest(manifest)

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest, _ = self.write_case(folder, file="linked.txt")
            (Path(folder) / "linked.txt").symlink_to(Path(folder) / "source.txt")
            with self.assertRaises(ValueError):
                UTILITY.audit_manifest(manifest)

    def test_missing_source_is_not_fabrication(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest, _ = self.write_case(folder, file="absent.txt")
            self.assertEqual(UTILITY.audit_manifest(manifest)["results"][0]["status"], "missing_source")

    def test_invalid_utf8_and_oversized_input_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.txt"
            path.write_bytes(b"\xff")
            with self.assertRaises(ValueError):
                UTILITY.read_bounded(path, 10)
            path.write_bytes(b"12345")
            with self.assertRaises(ValueError):
                UTILITY.read_bounded(path, 4)

    def test_duplicate_ids_and_unknown_authorities_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest, payload = self.write_case(folder)
            payload["quotations"].append(dict(payload["quotations"][0]))
            manifest.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                UTILITY.audit_manifest(manifest)
            payload["quotations"] = [{"id": "q", "authority_id": "missing", "text": "text"}]
            manifest.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                UTILITY.audit_manifest(manifest)

    def test_cli_exit_codes_and_no_source_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest, payload = self.write_case(folder)
            source = Path(folder) / "source.txt"
            before = source.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(manifest)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["results"][0]["status"], "exact")
            payload["quotations"][0]["text"] = "The owner may assign."
            manifest.write_text(json.dumps(payload))
            result = subprocess.run([sys.executable, str(SCRIPT), str(manifest)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            manifest.write_text("not JSON")
            result = subprocess.run([sys.executable, str(SCRIPT), str(manifest)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
