import sys
from src.extractor import extract_report
from src.flagger import check_report

report = extract_report(sys.argv[1])
results = check_report(report)

print(f"Report: {report.report_type.value} | Sex: {report.patient_sex} | Age: {report.patient_age}\n")
for r in results:
    line = f"{r.name:<20} {r.value_text:>8} {r.unit or '':<10} {r.status.upper():<10} [{r.range_source}]"
    if r.severity:
        line += f" {r.severity} ({r.deviation_pct}% outside range)"
    if r.note:
        line += f"  ! {r.note}"
    print(line)