---
name: uscis-rfe-i765
description: >
  Full workflow for responding to a USCIS Request for Evidence (RFE) on a
  Form I-765 Application for Employment Authorization. Handles any I-765
  category — F-1 OPT (pre/post-completion), STEM OPT extension, CPT, DACA,
  asylum, adjustment of status, and others. Guides Claude through case
  intake, document inventory, tab-organized PDF packet assembly, fresh cover
  letter generation, and submission guidance. Use this skill whenever a user
  mentions an RFE, I-765, EAD, OPT, STEM OPT, CPT, employment authorization,
  or "USCIS sent me a letter asking for more evidence." Also trigger when a
  user uploads or pastes an I-797C notice or RFE letter and asks for help
  responding.
---

# USCIS I-765 RFE Response Skill

You are helping a user build a complete, professional response to a USCIS
Request for Evidence (RFE) on their Form I-765. This is high-stakes — their
ability to work legally in the United States depends on this response. Be
thorough, organized, and precise.

Read `references/i765_categories.md` to understand which category applies,
and `references/tab_structure.md` for document organization guidance before
starting. Read `references/cover_letter_guide.md` when you reach the cover
letter step.

---

## Phase 1 — Case Intake

Start by extracting or asking for the following. If the user has uploaded
their RFE letter (I-797C), read it carefully and extract these automatically:

**Required:**
- Receipt number (format: IOExxxxxxxxxxx or similar)
- A-Number (format: A-xxx-xxx-xxx)
- RFE date and response deadline
- I-765 category code (e.g., C03B, C03C, C09, A03, C14, C33)
- Service center (Texas, Nebraska, Potomac, etc.)
- Premium processing? (I-907 filed?)
- Specific items USCIS is requesting (numbered 1–N in the RFE)

**Applicant info:**
- Full legal name (exactly as on the application)
- Current mailing address
- Email address
- School/employer name (if F-1)
- Degree program or job title
- F-1 program start/end dates (if applicable)

**Address history** — for the past 5 years (a very common RFE request):
- Each address, the dates they lived there, and a brief note (e.g., "college dorm," "first job")

Once you have this info, create `case_config.json` in the user's working
directory. See the schema in `references/tab_structure.md`.

---

## Phase 2 — Document Inventory

Walk the user through what documents they have for each tab. The standard
tab structure for F-1 cases is in `references/tab_structure.md`. For other
categories, adapt based on the RFE's specific requests.

For each requested item in the RFE:
- Tell the user exactly what document(s) satisfy it
- Ask them to confirm they have it or help them identify what's needed
- Note which tab it belongs in

Create a checklist as you go. Flag any gaps so the user knows what to
gather before proceeding.

**For photo/image documents** (travel receipts, screenshots, etc.):
- Accept .jpg, .jpeg, .png, or .pdf
- The build script converts images to labeled PDF pages automatically
- Ask user to describe what each image shows (location, date, what it proves)

---

## Phase 3 — Build the Packet

Once documents are collected, populate `case_config.json` with file paths
and run the build script:

```bash
pip install reportlab pypdf Pillow --break-system-packages --quiet
python scripts/build_packet.py --config case_config.json
```

The script outputs everything to `USCIS_Packet/`:
- `00_Cover_Letter.pdf`
- `TabA_[title].pdf` through `Tab[X]_[title].pdf`
- `Envelope_Label.pdf`

Each tab PDF has a professional color-coded cover page followed by the
source documents in order.

**If the build fails**, check:
- All file paths in case_config.json exist and are correct
- pypdf version compatibility (`pip install "pypdf>=3.0"`)
- Pillow installed for image handling

---

## Phase 4 — Generate the Cover Letter

The cover letter is the most important document — it frames everything for
the officer. Generate it fresh using the case details. Do NOT use a
boilerplate template; write it specifically for this applicant.

Read `references/cover_letter_guide.md` for the required structure and
tone. Key principles:

- **Write in first person** from the applicant's voice
- **Address each RFE item explicitly** by number
- **Be factual and precise** — dates, addresses, and names must be exact
- **Include the address history table** if requested
- **End with a declaration under penalty of perjury**
- **Include a full enclosures list** matching the tab structure exactly

After generating the cover letter content, update `case_config.json` with
the `cover_letter` section and rebuild, or write the cover letter directly
to PDF using the script's `--cover-only` flag.

---

## Phase 5 — Quality Check

Before presenting the final packet to the user, verify:

- [ ] Cover letter address history matches exactly what's in supporting docs
- [ ] Every RFE item is addressed in the cover letter and has a corresponding tab
- [ ] All enclosure codes (A-1, A-2, B-1, etc.) match the actual PDFs
- [ ] Page counts are reasonable (flag if any tab is unexpectedly short/long)
- [ ] Signature block is present — remind user they must sign before submitting
- [ ] Deadline is within a safe window (flag if < 2 weeks away)

Use pdfplumber to extract and verify key sections of the cover letter PDF:
```bash
python -c "import pdfplumber; [print(p.extract_text()) for p in pdfplumber.open('USCIS_Packet/00_Cover_Letter.pdf').pages]"
```

---

## Phase 6 — Submission Guidance

Tell the user:

**Online (myaccount.uscis.gov) — preferred for premium processing:**
- Log in → Your Cases → find the receipt number → Respond to RFE
- Upload all tab PDFs + cover letter as one combined PDF, or separately
- Keep file sizes under USCIS limits (usually 6MB per file)
- You will receive a confirmation email

**Mail (if online not available):**
- Send via USPS Priority Mail Express or FedEx/UPS overnight with tracking
- Address: per the RFE letter (service center address)
- Keep the tracking number and a copy of everything submitted

**After submission:**
- The I-797C acknowledgment email is NOT the decision
- Check myaccount.uscis.gov for status updates
- Premium processing: 15 business days from receipt of RFE response
- Non-premium: variable, check processing times at uscis.gov/processing-times

**Remind the user:**
- Sign the cover letter before submitting (wet ink or "/s/ [Name]" typed
  signature are both acceptable for cover letters; not official USCIS forms)
- Keep a complete copy of everything submitted
- The physical I-797 Approval Notice that arrives by mail is the definitive
  work authorization document — give a copy to HR when it arrives

---

## Important Notes

**Do not provide immigration legal advice.** You can explain what documents
satisfy an RFE item and help organize a response, but if the user's
situation is complex (prior visa violations, criminal history, prior denials,
status gaps), recommend they consult an immigration attorney.

**Common pitfalls to avoid:**
- Address history must cover the full 5-year period with no gaps
- DSO letters must be on school letterhead and include the DSO's name/title
- Travel documentation for overnight trips should include both outbound
  and return receipts if possible
- Unofficial transcripts are acceptable but official transcripts are stronger
- Bank statements should show recurring tuition payments if possible

**F-1 / CPT / OPT specific:**
- The I-20 must show CPT/OPT authorization for the relevant period
- Full course of study means 9+ credit hours per semester (or school's
  full-time standard)
- Each residency/in-seat session is evidence of physical attendance
- Employment letter should confirm the position directly applies to
  the degree program curriculum
