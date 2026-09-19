import sys
from src.extractor import extract_report

path = sys.argv[1]
report = extract_report(path)
print(report.model_dump_json(indent=2))
