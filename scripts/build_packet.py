#!/usr/bin/env python3
"""
USCIS I-765 RFE Response Packet Builder
========================================
Reads case_config.json and builds a complete response packet:
  - 00_Cover_Letter.pdf
  - Tab[X]_[Title].pdf for each configured tab
  - Envelope_Label.pdf

Usage:
    python build_packet.py [--config path/to/case_config.json] [--cover-only] [--tabs-only]

Requirements:
    pip install reportlab pypdf Pillow pdfplumber --break-system-packages
"""

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
MISSING = []
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    )
    from reportlab.platypus.flowables import HRFlowable
except ImportError:
    MISSING.append("reportlab")

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    MISSING.append("pypdf")

try:
    from PIL import Image as PILImage
except ImportError:
    MISSING.append("Pillow")

if MISSING:
    print(f"❌ Missing packages: {', '.join(MISSING)}")
    print(f"   Run: pip install {' '.join(MISSING)} --break-system-packages")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        return json.load(f)


def ensure_output_dir(config_path: Path) -> Path:
    out = config_path.parent / "USCIS_Packet"
    out.mkdir(exist_ok=True)
    return out


def safe_path(base: Path, file_str: str) -> Path:
    """Resolve a file path relative to the config directory."""
    p = Path(file_str)
    if p.is_absolute():
        return p
    resolved = base / p
    if resolved.exists():
        return resolved
    # Try relative to cwd
    if p.exists():
        return p
    raise FileNotFoundError(f"Cannot find file: {file_str} (tried {resolved} and {p})")


def merge_pdfs(sources: list, output_path: Path):
    """Merge a list of PDF paths into a single PDF. Converts images if needed."""
    writer = PdfWriter()
    for src in sources:
        src = Path(src)
        if not src.exists():
            print(f"  ⚠️  Skipping missing file: {src}")
            continue
        suffix = src.suffix.lower()
        if suffix in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"):
            # Convert image to a temporary single-page PDF in memory
            import io
            img = PILImage.open(src).convert("RGB")
            pdf_bytes = io.BytesIO()
            img.save(pdf_bytes, format="PDF", resolution=150)
            pdf_bytes.seek(0)
            reader = PdfReader(pdf_bytes)
        else:
            reader = PdfReader(str(src))
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)


def image_to_labeled_pdf(img_path: Path, label: str, sublabel: str = "") -> bytes:
    """Convert a single image to a PDF page with a label caption. Returns bytes."""
    import io
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                             leftMargin=0.5*inch, rightMargin=0.5*inch,
                             topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    # Label heading
    story.append(Paragraph(f"<b>{label}</b>", styles["Heading2"]))
    if sublabel:
        story.append(Paragraph(sublabel, styles["Normal"]))
    story.append(Spacer(1, 0.1*inch))

    # Image (fit to page width)
    img = PILImage.open(img_path)
    w, h = img.size
    max_w = 7.5 * inch
    max_h = 8.5 * inch
    ratio = min(max_w / w, max_h / h)
    story.append(RLImage(str(img_path), width=w * ratio, height=h * ratio))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# Cover page builder
# ---------------------------------------------------------------------------

def make_tab_cover_page(tab_letter: str, tab_info: dict, case: dict, applicant: dict) -> bytes:
    """Build a professional cover page for a tab. Returns PDF bytes."""
    import io
    color = tab_info.get("color_rgb", [0.18, 0.31, 0.56])
    tab_color = colors.Color(*color)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                             leftMargin=0.75*inch, rightMargin=0.75*inch,
                             topMargin=0.5*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    s_tab = ParagraphStyle("tab_letter", fontSize=72, leading=80,
                            textColor=tab_color, fontName="Helvetica-Bold")
    s_title = ParagraphStyle("tab_title", fontSize=22, leading=28,
                              textColor=tab_color, fontName="Helvetica-Bold")
    s_subtitle = ParagraphStyle("tab_sub", fontSize=13, leading=18,
                                 textColor=colors.Color(0.3, 0.3, 0.3))
    s_meta = ParagraphStyle("meta", fontSize=9, leading=13,
                             textColor=colors.Color(0.4, 0.4, 0.4))
    s_enc = ParagraphStyle("enc", fontSize=10, leading=15,
                            leftIndent=12)
    s_enc_header = ParagraphStyle("enc_hdr", fontSize=11, leading=15,
                                   fontName="Helvetica-Bold",
                                   textColor=tab_color)

    story = []

    # Top rule
    story.append(HRFlowable(width="100%", thickness=4, color=tab_color,
                              spaceAfter=0.15*inch))

    # Header line
    receipt = case.get("receipt_number", "")
    deadline = case.get("deadline", "")
    premium = "PREMIUM PROCESSING | " if case.get("premium_processing") else ""
    story.append(Paragraph(
        f"RESPONSE TO REQUEST FOR EVIDENCE | FORM {case.get('form','I-765')} (EAD) | "
        f"RECEIPT {receipt} | {applicant.get('a_number_display', case.get('a_number',''))}",
        s_meta))
    if premium or deadline:
        story.append(Paragraph(f"{premium}DEADLINE: {deadline}", s_meta))

    story.append(Spacer(1, 0.3*inch))

    # Big tab letter
    story.append(Paragraph(f"TAB {tab_letter}", s_tab))
    story.append(Spacer(1, 0.1*inch))

    # Title
    story.append(Paragraph(tab_info.get("title", ""), s_title))
    subtitle = tab_info.get("subtitle", "")
    if subtitle:
        story.append(Spacer(1, 0.05*inch))
        story.append(Paragraph(subtitle, s_subtitle))

    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width="100%", thickness=1,
                              color=colors.Color(0.8, 0.8, 0.8),
                              spaceAfter=0.2*inch))

    # Enclosures list
    enclosures = tab_info.get("enclosures", [])
    if enclosures:
        story.append(Paragraph("ENCLOSURES", s_enc_header))
        story.append(Spacer(1, 0.1*inch))
        for enc in enclosures:
            code = enc.get("code", "")
            desc = enc.get("description", "")
            story.append(Paragraph(f"<b>{code}</b>  {desc}", s_enc))
        story.append(Spacer(1, 0.2*inch))

    # Applicant info at bottom
    story.append(HRFlowable(width="100%", thickness=1,
                              color=colors.Color(0.8, 0.8, 0.8),
                              spaceAfter=0.1*inch))
    name = applicant.get("name", "")
    a_num = case.get("a_number", "")
    story.append(Paragraph(
        f"{name}  |  A-Number: {a_num}  |  I-765 RFE Response",
        s_meta))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# Cover letter builder
# ---------------------------------------------------------------------------

def build_cover_letter(config: dict, output_path: Path):
    """Build the cover letter PDF from config['cover_letter']."""
    case = config["case"]
    applicant = config["applicant"]
    cl = config.get("cover_letter", {})
    addr_history = config.get("address_history", [])
    tabs = config.get("tabs", {})

    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                             leftMargin=1*inch, rightMargin=1*inch,
                             topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    receipt = case.get("receipt_number", "")
    a_num = case.get("a_number", "")
    deadline = case.get("deadline", "")
    premium = "PREMIUM PROCESSING | " if case.get("premium_processing") else ""

    s_header = ParagraphStyle("cl_header", fontSize=8, leading=11,
                               textColor=colors.Color(0.4, 0.4, 0.4),
                               fontName="Helvetica")
    s_body = ParagraphStyle("cl_body", fontSize=11, leading=16,
                             spaceAfter=8)
    s_body_tight = ParagraphStyle("cl_body_t", fontSize=11, leading=15)
    s_h1 = ParagraphStyle("cl_h1", fontSize=13, leading=18,
                           fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6)
    s_h2 = ParagraphStyle("cl_h2", fontSize=11, leading=16,
                           fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
    s_bullet = ParagraphStyle("cl_bullet", fontSize=11, leading=16,
                               leftIndent=18, bulletIndent=0, spaceAfter=4)
    s_tbl = ParagraphStyle("cl_tbl", fontSize=9, leading=13, fontName="Helvetica-Bold")
    s_tbl_n = ParagraphStyle("cl_tbl_n", fontSize=9, leading=13)
    s_page = ParagraphStyle("cl_page", fontSize=8, leading=11,
                             textColor=colors.Color(0.5, 0.5, 0.5))

    hdr_text = (f"RESPONSE TO REQUEST FOR EVIDENCE | FORM {case.get('form','I-765')} (EAD) | "
                f"RECEIPT {receipt} | {a_num}")
    sub_text = f"{premium}DEADLINE: {deadline}"

    def header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColorRGB(0.5, 0.5, 0.5)
        canvas.drawString(inch, letter[1] - 0.45*inch, hdr_text)
        canvas.drawString(inch, letter[1] - 0.6*inch, sub_text)
        page_num = doc.page
        name = applicant.get("name", "")
        footer = f"{name}  |  {a_num}  |  I-765 RFE Response  |  Page {page_num}"
        canvas.drawCentredString(letter[0] / 2, 0.45*inch, footer)
        canvas.restoreState()

    story = []

    def add_page_header():
        story.append(Spacer(1, 0.25*inch))

    add_page_header()

    # Date
    letter_date = cl.get("date", datetime.today().strftime("%B %d, %Y"))
    story.append(Paragraph(letter_date, s_body))
    story.append(Spacer(1, 0.1*inch))

    # From address
    story.append(Paragraph(applicant.get("name", ""), s_body_tight))
    story.append(Paragraph(applicant.get("address_line1", ""), s_body_tight))
    if applicant.get("address_line2"):
        story.append(Paragraph(applicant["address_line2"], s_body_tight))
    story.append(Paragraph(applicant.get("city_state_zip", ""), s_body_tight))
    story.append(Paragraph(applicant.get("email", ""), s_body_tight))
    story.append(Spacer(1, 0.2*inch))

    # USCIS address
    uscis = config.get("uscis_address", {})
    story.append(Paragraph("U.S. Citizenship and Immigration Services", s_body_tight))
    if uscis.get("service_center"):
        story.append(Paragraph(uscis["service_center"], s_body_tight))
    if uscis.get("attn"):
        story.append(Paragraph(f"ATTN: {uscis['attn']}", s_body_tight))
    if uscis.get("street"):
        story.append(Paragraph(uscis["street"], s_body_tight))
    if uscis.get("city_state_zip"):
        story.append(Paragraph(uscis["city_state_zip"], s_body_tight))
    story.append(Spacer(1, 0.2*inch))

    # RE block
    story.append(Paragraph(f"RE: Response to Request for Evidence (I-797C)", s_body_tight))
    story.append(Paragraph(f"Form: {case.get('form','I-765')}, Application for Employment Authorization", s_body_tight))
    story.append(Paragraph(f"Receipt Number: {receipt}", s_body_tight))
    story.append(Paragraph(f"A-Number: {a_num}", s_body_tight))
    story.append(Paragraph(f"Date of RFE: {case.get('rfe_date', '')}", s_body_tight))
    if premium:
        story.append(Paragraph(f"USCIS Response Deadline: {deadline}", s_body_tight))
    story.append(Paragraph(f"Applicant: {applicant.get('name', '')}", s_body_tight))
    if case.get("premium_processing"):
        story.append(Paragraph("Processing Type: Premium Processing (I-907 Filed)", s_body_tight))
    story.append(Spacer(1, 0.25*inch))

    # Salutation
    story.append(Paragraph("Dear USCIS Officer:", s_body))
    story.append(Spacer(1, 0.1*inch))

    # Introduction
    intro = cl.get("introduction", "")
    if intro:
        for para in intro.split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), s_body))

    # RFE response items
    rfe_responses = cl.get("rfe_responses", [])
    if rfe_responses:
        story.append(Paragraph("I. RESPONSE TO REQUESTED EVIDENCE", s_h1))
        for item in rfe_responses:
            num = item.get("item_number", "")
            title = item.get("item_title", "")
            response = item.get("response", "")
            story.append(Paragraph(f"Request {num}: {title}", s_h2))
            for para in response.split("\n\n"):
                if para.strip():
                    # Handle bullet points in response text
                    if para.strip().startswith("•") or para.strip().startswith("-"):
                        for line in para.split("\n"):
                            line = line.strip().lstrip("•-").strip()
                            if line:
                                story.append(Paragraph(f"• {line}", s_bullet))
                    else:
                        story.append(Paragraph(para.strip(), s_body))

    # Travel section
    travel = cl.get("travel_section", "")
    if travel:
        story.append(Paragraph("II. TRAVEL HISTORY", s_h1))
        for para in travel.split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), s_body))

    # Address history section
    address_section_text = cl.get("address_section", "")
    if address_section_text:
        story.append(Paragraph("III. ADDRESS HISTORY", s_h1))
        for para in address_section_text.split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), s_body))

    # Address history table
    if addr_history:
        tbl_data = [
            [Paragraph("<b>Period</b>", s_tbl),
             Paragraph("<b>Address</b>", s_tbl),
             Paragraph("<b>Notes</b>", s_tbl)]
        ]
        for entry in addr_history:
            period = entry.get("period", "")
            address = entry.get("address", "").replace("\n", "<br/>")
            notes = entry.get("notes", "")
            tbl_data.append([
                Paragraph(period, s_tbl),
                Paragraph(address, s_tbl_n),
                Paragraph(notes, s_tbl_n),
            ])

        col_widths = [1.3*inch, 3.3*inch, 2.4*inch]
        tbl = Table(tbl_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.18, 0.31, 0.56)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.Color(0.8, 0.8, 0.8)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.96, 0.97, 0.99)]),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.2*inch))

    # Conclusion
    conclusion = cl.get("conclusion", "")
    if conclusion:
        story.append(Paragraph("IV. CONCLUSION", s_h1))
        for para in conclusion.split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), s_body))

    # Declaration
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "I declare under penalty of perjury under the laws of the United States "
        "that the foregoing is true and correct to the best of my knowledge and belief.",
        s_body))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Respectfully submitted,", s_body_tight))
    story.append(Spacer(1, 0.5*inch))  # Signature space
    story.append(Paragraph(f"<b>{applicant.get('name', '')}</b>", s_body_tight))
    story.append(Paragraph(f"A-Number: {a_num}", s_body_tight))
    story.append(Paragraph(f"Date: {letter_date}", s_body_tight))
    story.append(Paragraph(applicant.get("city_state_zip", ""), s_body_tight))
    if applicant.get("email"):
        story.append(Paragraph(applicant["email"], s_body_tight))
    story.append(PageBreak())

    # Enclosures list
    story.append(Spacer(1, 0.25*inch))
    story.append(Paragraph("ENCLOSURES", s_h1))
    story.append(Spacer(1, 0.1*inch))

    for tab_letter, tab_info in sorted(tabs.items()):
        story.append(Paragraph(
            f"<b>TAB {tab_letter} – {tab_info.get('title', '')}</b>  "
            f"{tab_info.get('subtitle', '')}",
            s_h2))
        for enc in tab_info.get("enclosures", []):
            code = enc.get("code", "")
            desc = enc.get("description", "")
            story.append(Paragraph(f"• {code}: {desc}", s_bullet))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"  ✅ 00_Cover_Letter.pdf")


# ---------------------------------------------------------------------------
# Tab builder
# ---------------------------------------------------------------------------

def build_tab(tab_letter: str, tab_info: dict, config: dict,
              base_dir: Path, out_dir: Path):
    """Build a single tab PDF: cover page + merged source documents."""
    import io
    case = config["case"]
    applicant = config["applicant"]

    # Sanitize title for filename
    title = tab_info.get("title", f"Tab_{tab_letter}")
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip().replace(" ", "_")
    out_name = f"Tab{tab_letter}_{safe_title}.pdf"
    out_path = out_dir / out_name

    writer = PdfWriter()

    # 1. Tab cover page
    cover_bytes = make_tab_cover_page(tab_letter, tab_info, case, applicant)
    cover_reader = PdfReader(io.BytesIO(cover_bytes))
    for page in cover_reader.pages:
        writer.add_page(page)

    # 2. Source files
    files = tab_info.get("files", [])
    for file_str in files:
        try:
            fp = safe_path(base_dir, file_str)
        except FileNotFoundError as e:
            print(f"  ⚠️  {e}")
            continue

        suffix = fp.suffix.lower()
        if suffix in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"):
            # Image: convert to labeled PDF page
            label = tab_info.get("image_labels", {}).get(str(fp.name), fp.name)
            pdf_bytes = image_to_labeled_pdf(fp, label)
            reader = PdfReader(io.BytesIO(pdf_bytes))
        else:
            reader = PdfReader(str(fp))

        for page in reader.pages:
            writer.add_page(page)

    with open(out_path, "wb") as f:
        writer.write(f)

    page_count = len(writer.pages)
    print(f"  ✅ {out_name} ({page_count} pages)")


# ---------------------------------------------------------------------------
# Envelope label builder
# ---------------------------------------------------------------------------

def build_envelope_label(config: dict, out_dir: Path):
    """Build a two-page envelope label (front and back)."""
    import io
    case = config["case"]
    applicant = config["applicant"]
    uscis = config.get("uscis_address", {})

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                             leftMargin=1*inch, rightMargin=1*inch,
                             topMargin=1*inch, bottomMargin=1*inch)

    styles = getSampleStyleSheet()
    s_center_big = ParagraphStyle("env_big", fontSize=18, leading=26,
                                   fontName="Helvetica-Bold",
                                   alignment=1)
    s_center = ParagraphStyle("env", fontSize=14, leading=22, alignment=1)
    s_small = ParagraphStyle("env_sm", fontSize=10, leading=14, alignment=1,
                              textColor=colors.Color(0.4, 0.4, 0.4))
    s_attn = ParagraphStyle("env_attn", fontSize=12, leading=18,
                             fontName="Helvetica-Bold", alignment=1,
                             textColor=colors.Color(0.7, 0.1, 0.1))

    story = []

    # --- Front label ---
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("TO:", s_small))
    story.append(Spacer(1, 0.1*inch))
    if uscis.get("service_center"):
        story.append(Paragraph(f"USCIS {uscis['service_center']}", s_center_big))
    if uscis.get("attn"):
        story.append(Paragraph(f"ATTN: {uscis['attn']}", s_attn))
    story.append(Spacer(1, 0.15*inch))
    if uscis.get("street"):
        story.append(Paragraph(uscis["street"], s_center))
    if uscis.get("city_state_zip"):
        story.append(Paragraph(uscis["city_state_zip"], s_center))
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width="60%", thickness=1, color=colors.Color(0.7, 0.7, 0.7)))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Re: I-765 RFE Response | {case.get('receipt_number', '')}", s_small))
    story.append(Paragraph(f"A-Number: {case.get('a_number', '')}", s_small))
    story.append(Paragraph(f"Deadline: {case.get('deadline', '')}", s_small))

    story.append(PageBreak())

    # --- Back/return label ---
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("RETURN ADDRESS:", s_small))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(applicant.get("name", ""), s_center_big))
    story.append(Paragraph(applicant.get("address_line1", ""), s_center))
    if applicant.get("address_line2"):
        story.append(Paragraph(applicant["address_line2"], s_center))
    story.append(Paragraph(applicant.get("city_state_zip", ""), s_center))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(applicant.get("email", ""), s_small))

    doc.build(story)
    buf.seek(0)

    out_path = out_dir / "Envelope_Label.pdf"
    with open(out_path, "wb") as f:
        f.write(buf.read())
    print("  ✅ Envelope_Label.pdf")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build USCIS I-765 RFE response packet")
    parser.add_argument("--config", default="case_config.json",
                        help="Path to case_config.json (default: ./case_config.json)")
    parser.add_argument("--cover-only", action="store_true",
                        help="Rebuild only the cover letter")
    parser.add_argument("--tabs-only", action="store_true",
                        help="Rebuild only the tab PDFs (skip cover letter)")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        print("   Create case_config.json first (see SKILL.md for schema).")
        sys.exit(1)

    config = load_config(config_path)
    base_dir = config_path.parent
    out_dir = ensure_output_dir(config_path)

    applicant = config.get("applicant", {})
    # Normalize A-number display (add dashes if not present)
    a_num = config.get("case", {}).get("a_number", "")
    if a_num and "-" not in a_num:
        # Format: A-xxx-xxx-xxx
        digits = a_num.lstrip("Aa")
        if len(digits) == 9:
            a_num = f"A{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    applicant["a_number_display"] = a_num

    case_name = applicant.get("name", "Applicant")
    receipt = config.get("case", {}).get("receipt_number", "")
    print(f"\n🗂  Building USCIS I-765 RFE Packet")
    print(f"   Applicant : {case_name}")
    print(f"   Receipt   : {receipt}")
    print(f"   Output    : {out_dir}\n")

    # Cover letter
    if not args.tabs_only:
        cover_path = out_dir / "00_Cover_Letter.pdf"
        print("Building 00_Cover_Letter.pdf...")
        build_cover_letter(config, cover_path)

    # Tabs
    if not args.cover_only:
        tabs = config.get("tabs", {})
        if not tabs:
            print("⚠️  No tabs defined in case_config.json")
        else:
            print(f"\nBuilding {len(tabs)} tab(s)...")
            for tab_letter in sorted(tabs.keys()):
                tab_info = tabs[tab_letter]
                build_tab(tab_letter, tab_info, config, base_dir, out_dir)

        # Envelope label
        print("\nBuilding Envelope_Label.pdf...")
        build_envelope_label(config, out_dir)

    print(f"\n✅ All done. Files saved to: {out_dir}\n")


if __name__ == "__main__":
    main()
