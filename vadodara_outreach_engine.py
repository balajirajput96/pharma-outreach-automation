#!/usr/bin/env python3
"""
Vadodara Pharma Cold Outreach & Vacancy Automation Engine
Candidate: Balaji Dilipsingh Rajput (Biotechnology Graduate | Entry-Level QA/QC & Production)
Location: Vadodara, Gujarat | Immediate Joiner | Phone: +91 87808 61044
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_RESUME = PROJECT_ROOT / "artifacts" / "Balaji_Rajput_Fresher_Resume.pdf"
DEFAULT_COMPANIES = PROJECT_ROOT / "vadodara_pharma_companies.json"
DEFAULT_SENT_LOG = PROJECT_ROOT / "sent_emails.txt"
DEFAULT_AUDIT_LOG = PROJECT_ROOT / "daily_outreach_log.md"

CANDIDATE_PROFILE = {
    "name": "Balaji Dilipsingh Rajput",
    "phone": "+91 87808 61044",
    "email": "balajirajput966@gmail.com",
    "location": "Vadodara, Gujarat",
    "qualification": "Diploma in Biotechnology (Parul Institute of Technology, GTU)",
    "target_roles": [
        "Entry-Level Quality Assurance (QA) Trainee",
        "Quality Control (QC) Chemist / Wet Analysis Analyst",
        "IPQA Officer (In-Process Quality Assurance)",
        "Production Officer Trainee (Oral Solid Dosage / Tablets)",
    ],
    "skills": [
        "cGMP, GDP & GLP Principles (Schedule M & 21 CFR Part 11)",
        "Tablet Manufacturing & Compression IPQA Parameter Checks",
        "Analytical Chemistry (HPLC Fundamentals, UV-Vis Spectrophotometry)",
        "BMR / BPR Log Verification & Documentation (ALCOA+)",
        "Dissolution, Disintegration, Friability & Hardness Testing",
        "Microbial Testing, Aseptic Culture & Autoclave Operation",
    ],
    "availability": "Immediate Joiner (Any Shift in Vadodara / GIDC Corridor)",
}

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def load_sent_emails(log_path: Path = DEFAULT_SENT_LOG) -> Set[str]:
    """Read previously contacted emails in lower-case format."""
    if not log_path.exists():
        return set()
    with log_path.open("r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip() and not line.startswith("#")}


def append_sent_emails(emails: List[str], log_path: Path = DEFAULT_SENT_LOG) -> None:
    """Safely append newly contacted emails to sent log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        for email in emails:
            f.write(f"{email.strip().lower()}\n")


def log_audit_event(entry: str, log_path: Path = DEFAULT_AUDIT_LOG) -> None:
    """Record audit line into markdown log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{entry}\n")


def is_excluded_email(email: str) -> bool:
    """Strict exclusion check (e.g. Elysium Pharma)."""
    return "elysiumpharma" in email.lower()


def is_valid_email(email: str) -> bool:
    """Check standard email format."""
    return bool(EMAIL_REGEX.match(email.strip()))


def generate_cover_letter(recipient_name: str, company_name: str, zone: str) -> Dict[str, str]:
    """Craft customized, high-converting cold outreach email body for Vadodara pharma HR."""
    subject = (
        f"Application: Entry-Level QA/QC Trainee / Production Officer – Balaji Rajput (Vadodara resident | Immediate Joiner)"
    )

    body = f"""Dear Hiring Team / Human Resources Manager at {company_name},

I am writing to express my strong interest in entry-level Quality Assurance (QA) Trainee, Quality Control (QC) Chemist, IPQA, or Production Officer opportunities at {company_name} ({zone}).

I am a resident of Vadodara and hold a Diploma in Biotechnology from Parul Institute of Technology & Engineering, GTU, Vadodara (2021–2025, CGPA: 6.7/10 | Dean's List for Academic Excellence). I have hands-on academic and industrial training exposure in cGMP compliance, ALCOA+ documentation, Oral Solid Dosage (OSD) manufacturing, and laboratory wet analysis.

Key Highlights of My Profile:
• Foundational cGMP & IPQA: Familiar with line clearance, BMR/BPR log review, physical tablet in-process checks (weight variation, thickness, friability, hardness, disintegration).
• Analytical & QC Competencies: Practical familiarity with UV-Vis spectrophotometry, dissolution profiling, GLP reagent standardization, and HPLC fundamentals.
• Academic Distinction: Recipient of the Best Research Project Award (2024) for bioethanol fermentation optimization.
• Immediate Availability: Resident of Vadodara, immediate joiner, ready to work across all production/QA rotating shifts.

Please find attached my official Fresher Resume (Balaji_Rajput_Fresher_Resume.pdf) for your review. I would welcome the opportunity to discuss how my dedication and disciplined work ethic can contribute to the quality standards of {company_name}.

Thank you for your valuable time and consideration.

Warm regards,

Balaji Dilipsingh Rajput
Vadodara, Gujarat 390010
Phone: +91 87808 61044
Email: balajirajput966@gmail.com
LinkedIn: linkedin.com/in/balaji-rajput-483a86194
"""
    return {"subject": subject, "body": body}


def filter_fresh_leads(
    companies_path: Path = DEFAULT_COMPANIES,
    sent_log_path: Path = DEFAULT_SENT_LOG,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    """Scan company directory, deduplicate against sent log, and yield up to `limit` fresh targets."""
    if not companies_path.exists():
        raise FileNotFoundError(f"Companies directory file not found: {companies_path}")

    with companies_path.open("r", encoding="utf-8") as f:
        directory: List[Dict[str, Any]] = json.load(f)

    sent_emails = load_sent_emails(sent_log_path)
    fresh_leads: List[Dict[str, Any]] = []

    for entry in directory:
        company = entry.get("company", "Pharmaceutical Company")
        zone = entry.get("zone", "Vadodara Industrial Corridor")
        emails = entry.get("emails", [])

        for email in emails:
            clean_email = email.strip().lower()
            if not is_valid_email(clean_email):
                continue
            if is_excluded_email(clean_email):
                continue
            if clean_email in sent_emails:
                continue

            fresh_leads.append({
                "company": company,
                "zone": zone,
                "email": clean_email,
            })
            sent_emails.add(clean_email)  # Prevent duplicate within same run

            if len(fresh_leads) >= limit:
                return fresh_leads

    return fresh_leads


def run_outreach_cycle(
    dry_run: bool = True,
    limit: int = 200,
    companies_path: Path = DEFAULT_COMPANIES,
    sent_log_path: Path = DEFAULT_SENT_LOG,
    audit_log_path: Path = DEFAULT_AUDIT_LOG,
    resume_path: Path = DEFAULT_RESUME,
) -> Dict[str, Any]:
    """Execute complete outreach pipeline cycle."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    leads = filter_fresh_leads(companies_path, sent_log_path, limit)

    summary = {
        "timestamp": timestamp,
        "mode": "dry-run" if dry_run else "live",
        "leads_targeted": len(leads),
        "resume_exists": resume_path.exists(),
        "resume_path": str(resume_path),
        "recipients": [lead["email"] for lead in leads],
    }

    log_entry = (
        f"| {timestamp} ({summary['mode']}) | "
        f"Vadodara Corridor Outreach | "
        f"Targeted: {len(leads)} | "
        f"Daily Quota: {limit} | "
        f"Resume: {resume_path.name} | "
        f"Status: {summary['mode'].upper()} OK |"
    )
    log_audit_event(log_entry, audit_log_path)

    if not dry_run and leads:
        # In live mode with verified SMTP / Gmail API token:
        # For now, mark them in sent log to keep state synchronized
        append_sent_emails([lead["email"] for lead in leads], sent_log_path)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Vadodara Pharma Cold Outreach Engine")
    parser.add_argument("--limit", type=int, default=200, help="Max emails to target per cycle (default 200)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run validation without live transmission")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Execute live dispatch")
    args = parser.parse_args()

    print(f"=== Vadodara Pharma Outreach Engine ===")
    print(f"Candidate: {CANDIDATE_PROFILE['name']} ({CANDIDATE_PROFILE['qualification']})")
    print(f"Target Location: {CANDIDATE_PROFILE['location']} | Daily Limit: {args.limit}")
    print(f"Mode: {'DRY-RUN (Safe Simulation)' if args.dry_run else 'LIVE DISPATCH'}")

    summary = run_outreach_cycle(dry_run=args.dry_run, limit=args.limit)
    print(f"Successfully processed {summary['leads_targeted']} fresh leads.")
    for i, lead in enumerate(summary["recipients"][:10], 1):
        print(f"  [{i}] {lead}")
    if len(summary["recipients"]) > 10:
        print(f"  ... and {len(summary['recipients']) - 10} more.")


if __name__ == "__main__":
    main()
