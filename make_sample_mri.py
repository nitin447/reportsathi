from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

styles = getSampleStyleSheet()
doc = SimpleDocTemplate("sample_reports/sample_mri_spine.pdf", pagesize=A4)

doc.build([
    Paragraph("SAMPLE DIAGNOSTIC CENTRE - MRI LUMBOSACRAL SPINE", styles["Title"]),
    Paragraph("Patient: Test Patient | Age: 45 | Sex: Male | Date: 14-09-2026", styles["Normal"]),
    Spacer(1, 12),
    Paragraph("<b>Clinical history:</b> Low back pain radiating to the left leg for 3 months.", styles["Normal"]),
    Spacer(1, 8),
    Paragraph("<b>Findings:</b>", styles["Normal"]),
    Paragraph("Vertebral body heights and alignment are maintained. "
              "Mild diffuse disc bulge at L4-L5 indenting the thecal sac, causing mild narrowing "
              "of the left neural foramen. No significant central canal stenosis. "
              "L5-S1 disc shows mild desiccation without herniation. "
              "Conus medullaris appears normal in signal and position. "
              "Paraspinal soft tissues are unremarkable.", styles["Normal"]),
    Spacer(1, 8),
    Paragraph("<b>Impression:</b> Mild diffuse disc bulge at L4-L5 with mild left neural foraminal "
              "narrowing. Mild disc desiccation at L5-S1. Clinical correlation is advised.",
              styles["Normal"]),
])
print("Created sample_reports/sample_mri_spine.pdf")