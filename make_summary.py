import sys
from pathlib import Path

from src.explainer import explain
from src.pdf_report import build_pdf
from src.pipeline import analyze

path = sys.argv[1]
result = analyze(path)
explained = explain(result)
out = build_pdf(result, explained, f"outputs/{Path(path).stem}_summary.pdf")
print("Saved", out)