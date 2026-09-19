from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()
doc = SimpleDocTemplate("sample_reports/sample_cbc.pdf", pagesize=A4)

rows = [
    ["Test", "Result", "Unit", "Reference Range", "Flag"],
    ["Hemoglobin", "10.2", "g/dL", "12.0 - 15.5", "L"],
    ["WBC Count", "7800", "/cumm", "4000 - 11000", ""],
    ["Platelet Count", "2.4", "lakh/cumm", "1.5 - 4.5", ""],
    ["MCV", "72", "fL", "80 - 100", "L"],
    ["RDW", "16.5", "%", "11.5 - 14.5", "H"],
    ["Serum Ferritin", "8", "ng/mL", "13 - 150", "L"],
    ["Vitamin D (25-OH)", "14", "ng/mL", "30 - 100", "L"],
]

table = Table(rows, hAlign="LEFT")
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
]))

doc.build([
    Paragraph("SAMPLE DIAGNOSTIC LAB - Complete Blood Count", styles["Title"]),
    Paragraph("Patient: Test Patient | Age: 28 | Sex: Female | Date: 12-09-2026", styles["Normal"]),
    Spacer(1, 16),
    table,
])
print("Created sample_reports/sample_cbc.pdf")
