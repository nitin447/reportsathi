from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

styles = getSampleStyleSheet()
doc = SimpleDocTemplate("sample_reports/sample_ecg.pdf", pagesize=A4)

rows = [
    ["Parameter", "Value", "Unit", "Reference"],
    ["Heart Rate", "108", "bpm", "60 - 100"],
    ["PR Interval", "168", "ms", "120 - 200"],
    ["QRS Duration", "92", "ms", ""],
    ["QTc", "430", "ms", ""],
]
table = Table(rows, hAlign="LEFT")
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
]))

doc.build([
    Paragraph("SAMPLE CARDIAC CENTRE - 12 LEAD ECG REPORT", styles["Title"]),
    Paragraph("Patient: Test Patient | Age: 52 | Sex: Male | Date: 15-09-2026", styles["Normal"]),
    Spacer(1, 12),
    table,
    Spacer(1, 12),
    Paragraph("<b>Interpretation:</b> Sinus tachycardia. Normal axis. No ST-T wave changes. "
              "No evidence of acute ischemia.", styles["Normal"]),
    Spacer(1, 8),
    Paragraph("<b>Impression:</b> Sinus tachycardia, otherwise normal ECG. "
              "Clinical correlation advised.", styles["Normal"]),
])
print("Created sample_reports/sample_ecg.pdf")