# Master Pharma Outreach Rules (Balaji Rajput - Vadodara Pharma Corridor)

## 1. Core Objective
Autonomous daily research, vacancy monitoring, and cold outreach for:
* Entry-Level Quality Assurance (QA) Trainee
* Quality Control (QC) Chemist / Wet Analysis Analyst
* In-Process Quality Assurance (IPQA) Officer
* Production Officer Trainee (Tablet Compression / Oral Solid Dosage)
* Geographic Focus: Vadodara, Gujarat (Savli, Makarpura, Nandesari, Padra, Dabhasa, Halol Corridor).

## 2. Daily Target & Throughput
* **Goal:** Up to 200 new, verified contacts per day.
* **Deduplication:** Always cross-reference `sent_emails.txt` before any transmission.
* **Quality Assurance:** Never resend to previously contacted addresses; preserve sender domain reputation.

## 3. Lead Generation & Vacancy Standards
* **Source:** Official corporate career portals, public HR recruitment notices, GIDC directories, LinkedIn job postings, and Vadodara walk-in notices (e.g. Alembic Sanskriti Hall, BPC Alkapuri, Four Points by Sheraton).
* **Target Recipients:** Relevant HR Managers, Talent Acquisition Leads, Plant HR, and official company recruitment emails.
* **Prohibitions:**
  * NO invented or unverified email addresses.
  * NO personal, non-recruitment emails.
  * **STRICT EXCLUSION:** Skip every recipient address containing `elysiumpharma` (case-insensitive).

## 4. Application Assets & Dispatch
* **Candidate Resume:**
  * Remote URL: `https://raw.githubusercontent.com/balajirajput96/professional-resume-balaji-rajput/main/artifacts/Balaji_Rajput_Fresher_Resume.pdf`
  * Local File: `artifacts/Balaji_Rajput_Fresher_Resume.pdf`
* **Candidate Profile:**
  * Name: Balaji Dilipsingh Rajput
  * Qualification: Diploma in Biotechnology (Parul Institute of Technology & Engineering, GTU, Vadodara)
  * Location: Vadodara, Gujarat 390010 (Immediate Joiner, Any Shift)
  * Phone: +91 87808 61044
  * Candidate Email: balajirajput966@gmail.com
* **Subject Format:** `Application: Entry-Level QA/QC Trainee / Production Officer – Balaji Rajput (Vadodara resident | Immediate Joiner)`
* **Attachment:** Exactly one copy of `Balaji_Rajput_Fresher_Resume.pdf`.

## 5. Logging & Audit Requirements
* **Duplicate Log:** `sent_emails.txt` (append confirmed sent addresses).
* **Audit Trail:** `daily_outreach_log.md` (record timestamp, company, count, and run status).
* **Vacancy Registry:** `vadodara_active_vacancies.json` (track ongoing and upcoming walk-in drives).

## 6. Execution Schedule & Automation
* Automated bi-daily execution via GitHub Actions (`.github/workflows/daily_vadodara_pharma_outreach.yml`).
* Asynchronous maintenance, research expansion, and monitoring via Jules CLI (`jules new`).
