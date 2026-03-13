# pipeline.py
# Connects the full pipeline: PDF -> text -> AI -> JSON

from app.extractor import extract_text_from_pdf
from app.parser import analyze_contract

def run_pipeline(file_path: str) -> dict:
    # Step 1: Extract text from PDF
    print(f"Extracting text from: {file_path}")
    text = extract_text_from_pdf(file_path)
    print(f"Extracted {len(text)} characters")

    # Step 2: Analyze with Gemini
    print("Sending to Gemini for analysis...")
    result = analyze_contract(text)
    print("Analysis complete")

    return result