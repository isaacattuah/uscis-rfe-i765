# Cover Letter Writing Guide

The cover letter is the most important document in the RFE response. It
frames the entire packet for the officer, connects the documents to the
specific RFE requests, and creates a narrative that makes the case for
approval. A well-written cover letter can compensate for gaps in
documentation; a weak one can undermine strong evidence.

---

## Tone and Voice

- Write in **first person** ("I am submitting...", "My address history...")
- **Formal but direct** — no flowery language, no hedging
- **Specific, not vague** — use names, dates, dollar amounts, addresses
- **Confident but not combative** — assume good faith from the officer
- **Factual** — every claim must be backed by an enclosed document

Avoid: "I believe," "I think," "hopefully," "as you can see"
Use: "The enclosed evidence establishes," "As documented in Tab C," "The record reflects"

---

## Required Sections

### 1. Header
Appears at the top of every page (built automatically by the script):
- Case: RESPONSE TO REQUEST FOR EVIDENCE | FORM I-765 (EAD) | RECEIPT [#] | A[#]
- Second line: PREMIUM PROCESSING | DEADLINE: [date] (if applicable)

### 2. Date, Addresses, RE Block
Standard letter format. Include:
- Today's date (date of submission)
- Applicant's name and current mailing address
- USCIS service center address (from the RFE letter)
- RE: line with receipt number, A-number, RFE date, deadline

### 3. Salutation
"Dear USCIS Officer:" — simple, standard

### 4. Introduction (1–2 paragraphs)
Cover:
- Who you are (name, visa status, school, degree program)
- What you're applying for and why (OPT/CPT, employer name, connection to degree)
- Brief statement that you've reviewed the RFE and are providing all requested evidence
- That evidence is organized by tab corresponding to each request

Example opening:
> I respectfully submit this Response to the Request for Evidence (RFE) dated
> [date], issued in connection with my Form I-765 Application for Employment
> Authorization based on [OPT/CPT]. I am currently enrolled as a full-time
> F-1 student at [School], [City], [State], pursuing a [Degree Program]. I am
> employed as a [Job Title] at [Employer] in [City], where my work directly
> applies and extends the curriculum of my degree program.

### 5. Section I — Response to Requested Evidence
Address each numbered RFE item explicitly:

```
I. RESPONSE TO REQUESTED EVIDENCE

Request 1: [Title from RFE]
[2–4 sentence response explaining what you've provided and where it is.
Reference specific enclosures. Connect the document to the request.]

Request 2: [Title from RFE]
[Same structure]
```

**Do not merge multiple RFE items into a single paragraph.** Each item
gets its own subsection, even if the same document satisfies multiple items
(in that case, say so and cross-reference).

### 6. Section II — Travel History (if requested)
Describe each trip mentioned in the evidence:
- Location and dates
- Purpose (residency name, course number)
- Documents enclosed (flight, hotel, transit receipts)

If any trip looks unusual (different city, extended stay, visiting someone),
explain it clearly and preemptively. Don't let an officer draw an incorrect
conclusion from an unexplained receipt.

Example for an unusual trip:
> One enclosed flight receipt shows travel from Atlanta to Rochester, NY. This
> trip was taken to assist a friend, [Name], a former student at [School], who
> was relocating. An enclosed moving company order in [friend's name]'s name
> confirms the rental was contracted by [friend], not the applicant. This trip
> does not reflect any change of domicile; my permanent residence has been at
> [current address] throughout my enrollment.

### 7. Section III — Address History (if requested)
Brief paragraph before the table:
> Below is my complete U.S. address history for the past five years, provided
> in response to the address history request included with the RFE. I have not
> resided outside the United States since commencing my F-1 status...

Then the address table (generated automatically by the script from the
`address_history` array in case_config.json).

**The address table must:**
- Cover the full 5-year period with no gaps
- Use exact addresses (street number, apartment, ZIP)
- Include a "Notes" column explaining each address briefly
- Be consistent with the address on the I-20, DSO letters, and Tab I documents

### 8. Section IV — Conclusion (1–2 paragraphs)
Cover:
- Summary of compliance (GPA, attendance, full-time enrollment)
- Connection between employment and curriculum
- Request for approval
- If premium processing: note that I-907 was filed and CPT/authorization expires on [date]
- Offer to provide additional information if needed

### 9. Declaration Under Penalty of Perjury
This is legally required. Use this exact language (do not paraphrase):

> I declare under penalty of perjury under the laws of the United States
> that the foregoing is true and correct to the best of my knowledge and belief.

### 10. Signature Block
```
Respectfully submitted,

[SIGNATURE SPACE — leave blank for physical signature, or type /s/ Full Name]

[Full Legal Name]
A-Number: A-xxx-xxx-xxx
Date: [date]
[Current address]
[Email]
```

**Remind the user:** The letter MUST be signed before submission. A typed
`/s/ Full Legal Name` is acceptable for cover letters. Physical wet-ink
signature is the gold standard.

### 11. Enclosures List (separate page)
Every single document in the packet must appear here, organized by tab:

```
ENCLOSURES

TAB A – USCIS Filing Documents (Requests 1, 2, 3)
• A-1: [Description]
• A-2: [Description]
...

TAB B – School Letters (Request 2)
• B-1: [Description]
...
```

The enclosures list must match the tab cover pages exactly. Check three
times: cover letter enclosures → tab cover pages → actual documents in
the PDF.

---

## Page Count Target

A complete F-1 OPT/CPT RFE response cover letter is typically 6–9 pages:
- Pages 1–2: Date, addresses, introduction, first few RFE responses
- Pages 3–4: Remaining RFE responses, travel section
- Pages 5–6: Address section + address table, conclusion, signature
- Pages 7–9: Enclosures list

Shorter is fine if there are fewer RFE items. Don't pad. Don't truncate
important explanations just to hit a page target.

---

## Common Mistakes to Avoid

**Address mismatches**: The address in the cover letter must match the I-20,
the DSO letters, and the documents in Tab I exactly. Even a minor variation
(missing "Apt", different ZIP+4) can trigger follow-up questions.

**Vague document descriptions**: In the enclosures list, don't write
"Bank Statement" — write "Chase Bank Checking Account Statement — December
2025, January 2026, February 2026."

**Missing date ranges**: Every address, every travel period, every document
should include specific dates. "2023–present" is weak; "July 2023 – present"
is better; "July 2023 – present (since July 15, 2023)" is best.

**Not explaining unusual documents**: Any document that doesn't obviously
connect to the RFE request should be explained. If a flight receipt shows
travel to a city not associated with a residency, explain it.

**Skipping RFE items**: Read the RFE numbered list carefully. Every numbered
item must be addressed in Section I. If you genuinely cannot provide a
document for an item, explain why and provide the best available substitute.

**Wrong service center address**: USCIS changes service center addresses.
Always verify against the actual RFE letter. The RFE letter itself usually
includes submission instructions. For premium processing, the ATTN: line
is critical.
