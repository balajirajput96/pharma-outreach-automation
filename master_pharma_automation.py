#!/usr/bin/env python3
"""
Master Pharma Outreach Automation Script
Coordinates Vadodara pharma company outreach, vacancy tracking, and candidate application flow.
Candidate: Balaji Dilipsingh Rajput (Vadodara resident | Immediate Joiner | +91 87808 61044)
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

from vadodara_outreach_engine import run_outreach_cycle
from vadodara_vacancy_monitor import save_vacancies

PROJECT_ROOT = Path(__file__).resolve().parent
RULES_FILE = Path(os.environ.get("OUTREACH_RULES_FILE", PROJECT_ROOT / "daily_outreach_rules.md"))
SENT_LOG = Path(os.environ.get("OUTREACH_SENT_LOG", PROJECT_ROOT / "sent_emails.txt"))
AUDIT_LOG = Path(os.environ.get("OUTREACH_AUDIT_LOG", PROJECT_ROOT / "daily_outreach_log.md"))
RESUME_PATH = Path(os.environ.get("OUTREACH_RESUME_PATH", PROJECT_ROOT / "artifacts" / "Balaji_Rajput_Fresher_Resume.pdf"))


def log_event(message: str, audit_log: Path = AUDIT_LOG) -> str:
    """Append a timestamped event to the configured local audit log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{timestamp}] {message}"
    with audit_log.open("a", encoding="utf-8") as f:
        f.write(f"{line}\n")
    print(line)
    return line


def run_research(dry_run: bool = True, audit_log: Path = AUDIT_LOG) -> dict[str, str]:
    """Record an approved research handoff without executing unverified external outreach."""
    log_event("Starting deep research for new pharma leads...", audit_log)
    if not dry_run:
        raise RuntimeError(
            "BLOCKED: direct research and outreach execution require a separately approved provider integration."
        )
    status = {
        "status": "dry-run",
        "reason": "No external research or email action was executed.",
    }
    log_event("Dry-run complete: no external research or email action was executed.", audit_log)
    return status


def run_master_pipeline(dry_run: bool = True, limit: int = 200) -> dict:
    """Execute both vacancy scanning and Vadodara pharma outreach matching."""
    log_event("Master Automation Run Started.")

    # 1. Update active vacancies
    vacancies_file = save_vacancies()
    log_event(f"Synchronized active Vadodara walk-ins into {vacancies_file.name}")

    # 2. Run outreach cycle
    summary = run_outreach_cycle(
        dry_run=dry_run,
        limit=limit,
        sent_log_path=SENT_LOG,
        audit_log_path=AUDIT_LOG,
        resume_path=RESUME_PATH,
    )
    log_event(f"Outreach cycle finished: {summary['leads_targeted']} fresh leads processed (mode: {summary['mode']}).")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Master Pharma Outreach Automation Runner")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Record and simulate the coordination handoff safely (default).",
    )
    parser.add_argument(
        "--live",
        action="store_false",
        dest="dry_run",
        help="Execute live dispatch mode.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Maximum email contacts to process per cycle (default: 200).",
    )
    args = parser.parse_args()

    run_master_pipeline(dry_run=args.dry_run, limit=args.limit)


if __name__ == "__main__":
    main()
