# Tab Structure Reference

## Standard Tab Organization for F-1 OPT/CPT Cases

This is the default structure refined from a real I-765 RFE response.
Adapt it based on the specific items in the user's RFE.

| Tab | Title | Typical Contents | Color (RGB) |
|-----|-------|-----------------|-------------|
| A | USCIS Filing Documents | I-797C receipt, RFE letter, I-20s (all), passport bio page, prior EADs | 0.18, 0.31, 0.56 (Navy) |
| B | School Letters | Joint DSO/Registrar statement, Registrar enrollment letter, Attendance confirmation | 0.13, 0.49, 0.72 (Blue) |
| C | Full Course of Study Documentation | Unofficial/official transcripts, degree audit, current course schedule, program curriculum | 0.18, 0.55, 0.34 (Green) |
| D | Course Syllabi | Syllabi for each course taken, especially CPT-authorized courses | 0.45, 0.27, 0.60 (Purple) |
| E | Attendance Records | Residency sign-in sheets, class participation records, online login records if available | 0.62, 0.32, 0.18 (Brown) |
| F | Tuition Payment Receipts | Semester-by-semester payment receipts, student account summary | 0.75, 0.45, 0.0 (Orange) |
| G | Bank Statements | 3 months of checking, savings, credit card statements | 0.2, 0.2, 0.2 (Dark Gray) |
| H | Travel and Lodging Receipts | Flight confirmations, hotel reservations, transit receipts, explanations for unusual trips | 0.55, 0.0, 0.0 (Dark Red) |
| I | CPT/OPT and Employment Documentation | Employment verification, offer letter, job description, compensation confirmation, address proof | 0.0, 0.4, 0.55 (Teal) |

---

## Adapting the Tab Structure

**For STEM OPT extension:**
Add a Tab J or replace Tab I with:
- I-983 Training Plan
- E-Verify employer documentation
- Prior EAD card copy
- Evidence of continued enrollment (if applicable)

**For non-F1 categories:**
Simplify significantly. Most (c)(9), (a)(3), (a)(5) responses need only
2–4 tabs covering the status documents and supporting evidence.

**For cases without travel/residency:**
Remove Tab H entirely. Don't pad with empty tabs.

**For cases without employment:**
Remove or condense Tab I.

---

## Tab Cover Page Colors

Colors help USCIS officers quickly navigate the packet. Use distinct,
professional colors. The navy/blue range works well for the first few
tabs. Suggested full palette:

```
A: [0.18, 0.31, 0.56]  # Navy blue
B: [0.13, 0.49, 0.72]  # Medium blue
C: [0.18, 0.55, 0.34]  # Forest green
D: [0.45, 0.27, 0.60]  # Purple
E: [0.62, 0.32, 0.18]  # Brown
F: [0.75, 0.45, 0.00]  # Orange
G: [0.25, 0.25, 0.25]  # Dark gray
H: [0.55, 0.10, 0.10]  # Dark red
I: [0.00, 0.42, 0.55]  # Teal
J: [0.40, 0.55, 0.00]  # Olive green
```

---

## case_config.json Full Schema

```json
{
  "case": {
    "receipt_number": "IOE9191499596",
    "a_number": "A141078631",
    "form": "I-765",
    "category_code": "C03B",
    "category_description": "F-1 Post-Completion OPT",
    "rfe_date": "2026-02-07",
    "deadline": "2026-06-01",
    "premium_processing": true,
    "service_center": "Texas Service Center"
  },

  "applicant": {
    "name": "Isaac Kofi Ahema Attuah",
    "address_line1": "507 Bishop St NW, Apt 4303",
    "address_line2": null,
    "city_state_zip": "Atlanta, GA 30318",
    "email": "isaacattuah@gmail.com",
    "phone": "404-555-0100"
  },

  "background": {
    "visa_status": "F-1",
    "school_name": "University of the Cumberlands",
    "degree_program": "Master of Science in Artificial Intelligence",
    "degree_level": "Master's",
    "program_start": "2023-08",
    "program_end_expected": "2026-05",
    "employer": "Google LLC",
    "employer_location": "Atlanta, Georgia",
    "job_title": "Customer Engineer",
    "additional_context": "Executive Hybrid Format — in-seat residencies required each semester"
  },

  "address_history": [
    {
      "period": "2021 – 2022",
      "address": "123 College Ave, Room 101\nAnytown, ST 12345",
      "notes": "On-campus housing"
    },
    {
      "period": "2022 – 2023",
      "address": "456 Oak St, Apt 2B\nAtlanta, GA 30303",
      "notes": "First apartment"
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
    "date": "March 7, 2026",
    "introduction": "Introductory paragraph(s) explaining who you are and what you're submitting. Write 2–3 paragraphs covering: your name and status, your school and program, your employer and how it connects to your coursework, and a brief overview of what the packet contains.",

    "rfe_responses": [
      {
        "item_number": 1,
        "item_title": "Full Course of Study Documentation",
        "response": "Detailed response to this specific RFE item. Explain what you've provided and why it satisfies the request. Reference specific enclosures by their tab/enclosure code (e.g., 'See Tab C, Enclosure C-1')."
      },
      {
        "item_number": 2,
        "item_title": "DSO Statement",
        "response": "Response to item 2..."
      }
    ],

    "travel_section": "Only include this section if USCIS asked about travel or if you have receipts for trips that need explanation. Describe each trip chronologically: location, dates, purpose (e.g., 'MSAI 511 in-seat residency'), and what documentation is provided. If any trip looks unusual (different city, extended stay), explain it clearly.",

    "address_section": "Brief paragraph contextualizing your address history before the table appears. For example: 'My U.S. address history for the past five years is as follows. I have not resided outside the United States during my F-1 enrollment. Short-term residency travel did not constitute a change of domicile.'",

    "conclusion": "Closing paragraph(s) requesting approval, noting premium processing if applicable, and offering to provide additional information. If CPT expires soon, note the date and request expedited consideration."
  },

  "tabs": {
    "A": {
      "title": "USCIS Filing Documents",
      "subtitle": "(Requests 1, 2, 3)",
      "color_rgb": [0.18, 0.31, 0.56],
      "enclosures": [
        {"code": "A-1", "description": "Form I-797C Receipt Notice (I-765 filed Feb 7, 2026)"},
        {"code": "A-2", "description": "Form I-797C RFE Notice (issued Feb 7, 2026)"},
        {"code": "A-3", "description": "Current Form I-20 (University of the Cumberlands, Spring 2026)"},
        {"code": "A-4", "description": "Prior Form I-20s (all previous I-20s in chronological order)"},
        {"code": "A-5", "description": "Passport Bio Page"},
        {"code": "A-6", "description": "F-1 Visa Stamp"},
        {"code": "A-7", "description": "Form I-94 Arrival/Departure Record"}
      ],
      "files": [
        "documents/receipt_notice.pdf",
        "documents/rfe_letter.pdf",
        "documents/i20_current.pdf",
        "documents/i20_prior.pdf",
        "documents/passport_bio.pdf",
        "documents/f1_visa.pdf",
        "documents/i94.pdf"
      ]
    },
    "B": {
      "title": "School Letters",
      "subtitle": "(Request 2)",
      "color_rgb": [0.13, 0.49, 0.72],
      "enclosures": [
        {"code": "B-1", "description": "Joint DSO and Registrar Statement (Pamela Smith, DSO + Leah Gray, Registrar)"},
        {"code": "B-2", "description": "Registrar Verification Letter (Leah Gray, Registrar)"},
        {"code": "B-3", "description": "Attendance Confirmation Letter (Makalyn Peace, DSO)"}
      ],
      "files": [
        "documents/joint_dso_registrar_letter.pdf",
        "documents/registrar_letter.pdf",
        "documents/attendance_letter.pdf"
      ]
    }
  }
}
```

---

## Notes on File Ordering Within Tabs

Within each tab, maintain a logical order that matches the enclosures list
on the cover page. The cover page lists what's inside, so the actual
documents must appear in exactly that order.

For Tab B (school letters), the order established by the applicant in their
cover letter enclosures list is the authoritative order. Don't reorder
based on document date or importance — follow the enclosures list exactly.

For tabs with many documents (e.g., Tab D with 20+ syllabi), group by
semester and list them semester-by-semester in the enclosures list.

---

## Enclosure Code System

Use a consistent prefix + number system:
- Tab A → A-1, A-2, A-3...
- Tab B → B-1, B-2, B-3...
- etc.

Codes appear on the tab cover page and in the cover letter enclosures list.
They must match exactly. Any mismatch creates confusion for the USCIS officer.
