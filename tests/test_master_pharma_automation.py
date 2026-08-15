import tempfile
import unittest
from pathlib import Path

from master_pharma_automation import log_event, run_research


class PharmaOutreachSafetyTests(unittest.TestCase):
    def test_log_event_writes_auditable_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            audit_log = Path(directory) / "audit.log"
            line = log_event("Safety check", audit_log)
            self.assertIn("Safety check", line)
            self.assertEqual(audit_log.read_text(encoding="utf-8").strip(), line)

    def test_research_defaults_to_non_external_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            audit_log = Path(directory) / "audit.log"
            result = run_research(dry_run=True, audit_log=audit_log)
            self.assertEqual(result["status"], "dry-run")
            self.assertIn("no external research or email action", result["reason"].lower())

    def test_non_dry_run_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "BLOCKED"):
                run_research(dry_run=False, audit_log=Path(directory) / "audit.log")


if __name__ == "__main__":
    unittest.main()
