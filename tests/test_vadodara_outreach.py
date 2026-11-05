import tempfile
import unittest
from pathlib import Path

from vadodara_outreach_engine import (
    CANDIDATE_PROFILE,
    filter_fresh_leads,
    generate_cover_letter,
    is_excluded_email,
    is_valid_email,
    load_sent_emails,
    run_outreach_cycle,
)
from vadodara_vacancy_monitor import get_active_vacancies, save_vacancies


class VadodaraOutreachTests(unittest.TestCase):
    def test_candidate_profile_attributes(self) -> None:
        self.assertEqual(CANDIDATE_PROFILE["name"], "Balaji Dilipsingh Rajput")
        self.assertIn("Vadodara", CANDIDATE_PROFILE["location"])
        self.assertEqual(CANDIDATE_PROFILE["phone"], "+91 87808 61044")
        self.assertEqual(CANDIDATE_PROFILE["email"], "balajirajput966@gmail.com")

    def test_email_validation(self) -> None:
        self.assertTrue(is_valid_email("hr@alembic.co.in"))
        self.assertTrue(is_valid_email("careers@sunpharma.com"))
        self.assertFalse(is_valid_email("invalid_email"))
        self.assertFalse(is_valid_email("hr@.com"))

    def test_exclusion_filter(self) -> None:
        self.assertTrue(is_excluded_email("hr@elysiumpharma.com"))
        self.assertTrue(is_excluded_email("ADMIN@ELYSIUMPHARMA.COM"))
        self.assertFalse(is_excluded_email("hr@alembic.co.in"))
        self.assertFalse(is_excluded_email("careers@zyduslife.com"))

    def test_cover_letter_generation(self) -> None:
        letter = generate_cover_letter("HR Manager", "Alembic Pharmaceuticals Ltd", "Gorwa, Vadodara")
        self.assertIn("Balaji Rajput", letter["subject"])
        self.assertIn("Alembic Pharmaceuticals Ltd", letter["body"])
        self.assertIn("Parul Institute of Technology", letter["body"])
        self.assertIn("+91 87808 61044", letter["body"])
        self.assertIn("Balaji_Rajput_Fresher_Resume.pdf", letter["body"])

    def test_filter_fresh_leads_and_deduplication(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sent_log = Path(tmpdir) / "sent.txt"
            sent_log.write_text("quality@alembic.co.in\n", encoding="utf-8")

            companies_file = Path(tmpdir) / "companies.json"
            companies_file.write_text(
                """[
                    {"company": "Alembic", "zone": "Vadodara", "emails": ["quality@alembic.co.in", "careers@alembic.co.in"]},
                    {"company": "Elysium", "zone": "Dabhasa", "emails": ["hr@elysiumpharma.com"]},
                    {"company": "Sun", "zone": "Halol", "emails": ["hr.halol@sunpharma.com"]}
                ]""",
                encoding="utf-8",
            )

            leads = filter_fresh_leads(
                companies_path=companies_file,
                sent_log_path=sent_log,
                limit=10,
            )
            lead_emails = [l["email"] for l in leads]
            # quality@alembic.co.in is in sent.txt -> skipped
            self.assertNotIn("quality@alembic.co.in", lead_emails)
            # hr@elysiumpharma.com is excluded -> skipped
            self.assertNotIn("hr@elysiumpharma.com", lead_emails)
            # careers@alembic.co.in and hr.halol@sunpharma.com should be included
            self.assertIn("careers@alembic.co.in", lead_emails)
            self.assertIn("hr.halol@sunpharma.com", lead_emails)

    def test_run_outreach_cycle_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sent_log = Path(tmpdir) / "sent.txt"
            audit_log = Path(tmpdir) / "audit.md"
            resume = Path(tmpdir) / "Balaji_Rajput_Fresher_Resume.pdf"
            resume.write_text("Dummy PDF content", encoding="utf-8")

            companies_file = Path(tmpdir) / "companies.json"
            companies_file.write_text(
                """[
                    {"company": "BDR", "zone": "Savli", "emails": ["hr.savli@bdrpharma.com"]}
                ]""",
                encoding="utf-8",
            )

            summary = run_outreach_cycle(
                dry_run=True,
                limit=10,
                companies_path=companies_file,
                sent_log_path=sent_log,
                audit_log_path=audit_log,
                resume_path=resume,
            )
            self.assertEqual(summary["mode"], "dry-run")
            self.assertEqual(summary["leads_targeted"], 1)
            self.assertTrue(summary["resume_exists"])
            self.assertTrue(audit_log.exists())
            # In dry-run, sent log is not modified
            self.assertEqual(len(load_sent_emails(sent_log)), 0)

    def test_vacancy_monitor(self) -> None:
        vacancies = get_active_vacancies()
        self.assertGreaterEqual(len(vacancies), 5)
        companies = [v["company"] for v in vacancies]
        self.assertIn("Alembic Pharmaceuticals Ltd", companies)
        self.assertIn("Sun Pharmaceutical Industries Ltd", companies)

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "vacancies.json"
            saved_path = save_vacancies(out_file)
            self.assertTrue(saved_path.exists())


if __name__ == "__main__":
    unittest.main()
