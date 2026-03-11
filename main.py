# main.py
from app.extractor import extract_text_from_pdf
from app.parser import analyze_contract
import json

# Step 1: Extract text from PDF
text = extract_text_from_pdf("test_contract.pdf")
print("=== TEXT EXTRACTED SUCCESSFULLY ===")
print(f"Characters extracted: {len(text)}")
print()

# Step 2: Send to Gemini and get structured JSON
print("=== SENDING TO GEMINI ===")
result = analyze_contract(text)
print()
print("=== STRUCTURED OUTPUT ===")
print(json.dumps(result, indent=2))