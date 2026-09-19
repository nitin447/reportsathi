import os
from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.explainer import ExplainedReport
from src.pipeline import AnalysisResult

URGENCY_LABEL = {
    "urgent": ("URGENT: seek medical attention", "#c62828"),
    "see_doctor_soon": ("See a doctor soon", "#ef6c00"),
    "routine_followup": ("Discuss at your next visit", "#b28704"),
    "all_normal": ("Nothing outside the normal range", "#2e7d32"),
}


def _range(c) -> str:
    if c.low is not None and c.high is not None:
        return f"{c.low:g} - {c.high:g}"
    if c.high is not None:
        return f"up to {c.high:g}"
    if c.low is not None:
        return f"at least {c.low:g}"
    return "not printed"


def build_pdf(result: AnalysisResult, explained: ExplainedReport, output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    styles = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=14)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=colors.grey)
    cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=11)
    white = ParagraphStyle("white", parent=body, textColor=colors.white, fontSize=11, leading=14)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=4)

    r = result.report
    e = explained.explanation
    story = []

    story.append(Paragraph("Health Report Summary for Doctor Visit", styles["Title"]))
    story.append(Paragraph(
        escape(f"Prepared by ReportSathi on {date.today().strftime('%d-%m-%Y')} | "
               f"Report type: {r.report_type.value} | Age: {r.patient_age or '-'} | "
               f"Sex: {r.patient_sex or '-'}"), small))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Name: ______________________________", body))
    story.append(Spacer(1, 8))

    label, hex_color = URGENCY_LABEL[explained.urgency]
    box = Table(
        [[Paragraph(f"<b>{escape(label)}</b><br/>{escape(explained.urgency_reason)}", white)]],
        colWidths=[180 * mm],
    )
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(hex_color)),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(box)

    story.append(Paragraph("Summary", h2))
    story.append(Paragraph(escape(e.summary), body))

    attention = [c for c in result.checked_values if c.status in ("low", "high")]
    if attention:
        story.append(Paragraph("Values needing attention", h2))
        rows = [[Paragraph(f"<b>{h}</b>", cell) for h in
                 ("Test", "Result", "Unit", "Printed range", "Status")]]
        for c in attention:
            color = "#c62828" if c.status == "high" else "#1565c0"
            status = f'<font color="{color}"><b>{c.status.upper()}</b></font>'
            if c.severity:
                status += f" ({escape(c.severity)})"
            rows.append([
                Paragraph(escape(c.name), cell),
                Paragraph(escape(c.value_text), cell),
                Paragraph(escape(c.unit or ""), cell),
                Paragraph(escape(_range(c)), cell),
                Paragraph(status, cell),
            ])
        table = Table(rows, colWidths=[55 * mm, 25 * mm, 25 * mm, 40 * mm, 35 * mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(table)
        normal_n = sum(1 for c in result.checked_values if c.status == "normal")
        unjudged = [c.name for c in result.checked_values if c.status in ("unknown", "not_numeric")]
        if normal_n or unjudged:
            note = f"{normal_n} other value(s) were within the printed range."
            if unjudged:
                note += " Could not be judged (no printed range): " + ", ".join(unjudged) + "."
            story.append(Spacer(1, 3))
            story.append(Paragraph(escape(note), small))

    n = result.narrative
    if n:
        story.append(Paragraph(escape(n.modality), h2))
        for f in n.findings:
            if f.significance in ("abnormal", "borderline"):
                story.append(Paragraph(escape(f"- {f.body_part + ': ' if f.body_part else ''}{f.finding}"), body))
        if n.impression:
            story.append(Spacer(1, 3))
            story.append(Paragraph("<b>Impression (from the report):</b> " + escape(n.impression), body))

    if e.connect_the_dots:
        story.append(Paragraph("Patterns worth discussing", h2))
        for d in e.connect_the_dots:
            story.append(Paragraph(escape(f"- {d}"), body))

    story.append(Paragraph("Questions to ask my doctor", h2))
    for i, q in enumerate(e.questions_for_doctor, 1):
        story.append(Paragraph(escape(f"{i}. {q}"), body))

    story.append(Paragraph("Fill in before your visit", h2))
    for line in ("Symptoms I have: ", "Medicines / supplements I take: ", "Allergies: "):
        story.append(Paragraph(line + "_" * 60, body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(Paragraph(escape(explained.disclaimer), small))

    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=15 * mm, bottomMargin=15 * mm)
    doc.build(story)
    return output_path