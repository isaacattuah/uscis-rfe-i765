# USCIS I-765 RFE Response — Gemini CLI Guide

> **Note:** Gemini CLI now supports the Agent Skills open standard! You can
> natively install this workflow as a skill using:
> `gemini skills install https://github.com/your-username/uscis-rfe-i765.git`
>
> Once installed, Gemini will automatically read `SKILL.md` and offer to
> activate it when relevant. This `GEMINI.md` file is preserved here for
> legacy setups, or if you prefer to use it as project context instead of a
> discoverable skill.

This file adapts the USCIS RFE response workflow for use with **Gemini CLI**
(`gemini` command-line tool). The overall workflow is identical to SKILL.md;
this file covers Gemini-specific tool usage and conventions.

---

## Setup

Before starting, confirm these Python packages are available:

```bash
pip install reportlab pypdf Pillow pdfplumber --break-system-packages
```

Gemini CLI tools used in this workflow:
- `read_file` — read PDFs, config files, and documents
- `write_file` — create case_config.json and output files
- `run_shell_command` — run Python scripts and pip installs
- `glob` / `list_directory` — find documents in user's folders
- `web_search` — look up service center addresses, processing times

---

## Phase 1 — Case Intake

Ask the user to upload or paste their RFE letter. Use `read_file` to extract:

```
read_file("path/to/RFE_letter.pdf")
```

Extract: receipt number, A-number, RFE date, deadline, category code,
service center, and all numbered requests.

Then gather applicant details (name, address, school, employer, address
history) through conversation.

Create `case_config.json`:

```
write_file("case_config.json", <json content>)
```

See the full schema below.

---

## Phase 2 — Document Inventory

Use `list_directory` or `glob` to find documents the user has already
organized:

```
list_directory("path/to/documents/folder")
```

Walk through each RFE item and confirm which file satisfies it. Build out
the `tabs` section of `case_config.json` as you go.

---

## Phase 3 — Build the Packet

Run the build script:

```
run_shell_command("python scripts/build_packet.py --config case_config.json")
```

Check stdout for any errors. The script creates `USCIS_Packet/` with all
tab PDFs, the cover letter, and the envelope label.

To verify the cover letter extracted correctly:

```
run_shell_command("python -c \"import pdfplumber; [print(p.extract_text()) for p in pdfplumber.open('USCIS_Packet/00_Cover_Letter.pdf').pages]\"")
```

---

## Phase 4 — Cover Letter

Generate the cover letter fresh using the applicant's case details. Write
the content to `cover_letter_content.json` (matching the schema in the
`cover_letter` section below), then rebuild:

```
run_shell_command("python scripts/build_packet.py --config case_config.json --cover-only")
```

---

## case_config.json Schema

```json
{
  "case": {
    "receipt_number": "IOE9191499596",
    "a_number": "A141-078-631",
    "form": "I-765",
    "category_code": "C03B",
    "category_description": "F-1 Student Post-Completion OPT",
    "rfe_date": "2026-02-07",
    "deadline": "2026-06-01",
    "premium_processing": true,
    "service_center": "Texas Service Center"
  },
  "applicant": {
    "name": "Full Legal Name",
    "address_line1": "507 Bishop St NW, Apt 4303",
    "city_state_zip": "Atlanta, GA 30318",
    "email": "email@example.com"
  },
  "background": {
    "visa_status": "F-1",
    "school_name": "University of the Cumberlands",
    "degree_program": "Master of Science in Artificial Intelligence",
    "employer": "Google LLC",
    "employer_location": "Atlanta, Georgia"
  },
  "address_history": [
    {
      "period": "2022 – 2023",
      "address": "450 16th St NW Apt 4007D\nAtlanta, GA 30363-1012",
      "notes": "First Atlanta address"
    },
    {
      "period": "July 2023 – Present",
      "address": "507 Bishop St NW, Apt 4303\nAtlanta, GA 30318-4485",
      "notes": "Current address"
    }
  ],
  "uscis_address": {
    "service_center": "Texas Service Center",
    "attn": "I-765 RFE PREMIUM PROCESSING",
    "street": "6046 N Belt Line Rd, Suite 765",
    "city_state_zip": "Irving, TX 75038"
  },
  "cover_letter": {
    "date": "2026-03-07",
    "introduction": "Paragraph introducing who you are and what you're submitting.",
    "rfe_responses": [
      {
        "item_number": 1,
        "item_title": "Full Course of Study Documentation",
        "response": "Response paragraph for item 1..."
      }
    ],
    "travel_section": "Paragraph describing each residency trip...",
    "address_section": "Paragraph contextualizing address history...",
    "conclusion": "Concluding paragraph with request for approval..."
  },
  "tabs": {
    "A": {
      "title": "USCIS Filing Documents",
      "subtitle": "(Requests 1, 2, 3)",
      "color_rgb": [0.18, 0.31, 0.56],
      "enclosures": [
        {"code": "A-1", "description": "Form I-797C Receipt Notice"},
        {"code": "A-2", "description": "Form I-797C RFE Notice"}
      ],
      "files": [
        "path/to/receipt_notice.pdf",
        "path/to/rfe_letter.pdf"
      ]
    }
  }
}
```

---

## Service Center Mailing Addresses

Always verify on uscis.gov — addresses change. Common addresses as of 2026:

**Texas Service Center (Premium Processing I-765):**
USCIS Texas Service Center
ATTN: I-765 RFE PREMIUM PROCESSING
6046 N Belt Line Rd, Suite 765
Irving, TX 75038

**Nebraska Service Center:**
USCIS Nebraska Service Center
850 S Street
Lincoln, NE 68508

**Potomac Service Center:**
USCIS Potomac Service Center
2200 Potomac Center Drive
Arlington, VA 22202

---

## Tips for Gemini CLI Users

**Reading large PDF files**: If `read_file` returns truncated content for a
long PDF, use pdfplumber via `run_shell_command` instead:
```bash
python -c "import pdfplumber; pdf=pdfplumber.open('file.pdf'); [print(p.extract_text()) for p in pdf.pages]"
```

**Verifying file paths**: Before adding a file to case_config.json, confirm
it exists:
```bash
ls -la "path/to/document.pdf"
```

**Checking output page counts**: After building, verify tabs have the
expected number of pages:
```bash
python -c "from pypdf import PdfReader; r=PdfReader('USCIS_Packet/TabA_USCIS_Filing_Documents.pdf'); print(len(r.pages), 'pages')"
```

**Large file handling**: USCIS online portal has a ~6MB per-file limit.
Check sizes before uploading:
```bash
ls -lh USCIS_Packet/*.pdf
```

If any file exceeds 6MB, compress images in that tab or split into
multiple uploads labeled clearly (e.g., "TabD_Part1", "TabD_Part2").

---

## What to Tell the User After the Packet Is Built

1. Review `USCIS_Packet/00_Cover_Letter.pdf` carefully — verify every
   fact, date, name, and address is correct.
2. **Sign the cover letter** — print page containing the signature block,
   sign in blue or black ink, scan, and replace or submit as supplement.
   (A typed `/s/ Full Name` is also acceptable for cover letters.)
3. Submit online at myaccount.uscis.gov if possible (faster and tracked).
4. Keep a complete copy of everything.
5. The physical I-797 Approval Notice mailed to your address is the actual
   work authorization document — share a copy with HR when it arrives.
