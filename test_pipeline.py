import sys
from src.pipeline import analyze

result = analyze(sys.argv[1])
r = result.report
print(f"Type: {r.report_type.value} | Age: {r.patient_age} | Sex: {r.patient_sex}\n")

if result.checked_values:
    print("--- VALUES ---")
    for c in result.checked_values:
        print(f"{c.name:<20} {c.value_text:>8} {c.unit or '':<10} {c.status.upper()}")

if result.narrative:
    n = result.narrative
    print(f"\n--- {n.modality} ---")
    print("Indication:", n.indication)
    for f in n.findings:
        print(f"[{f.significance.upper():<10}] {f.body_part or '-'}: {f.finding}")
    print("\nImpression:", n.impression)
    print("Report's own advice:", n.recommendations_in_report)
    print("Urgent wording:", n.urgent_language)