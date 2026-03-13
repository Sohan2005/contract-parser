# main.py
import json
from app.pipeline import run_pipeline

result = run_pipeline("test_contract.pdf")

print()
print("=== FINAL STRUCTURED OUTPUT ===")
print(json.dumps(result, indent=2))