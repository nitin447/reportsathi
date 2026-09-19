import sys

from src.explainer import explain
from src.pipeline import analyze

path = sys.argv[1]
language = sys.argv[2] if len(sys.argv) > 2 else "English"

result = analyze(path)
out = explain(result, language)
e = out.explanation

print(f"URGENCY: {out.urgency.upper()} - {out.urgency_reason}\n")
print("SUMMARY:\n", e.summary, "\n")
print("KEY POINTS:")
for k in e.key_points:
    print(f" - {k.name} ({k.status}): {k.meaning}")
print("\nCONNECTING THE DOTS:")
for d in e.connect_the_dots:
    print(" -", d)
print("\nQUESTIONS FOR YOUR DOCTOR:")
for q in e.questions_for_doctor:
    print(" -", q)
print("\n" + out.disclaimer)