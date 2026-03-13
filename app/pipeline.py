# pipeline.py
# Connects the full pipeline: PDF -> text -> AI -> JSON
import json
from app.extractor import extract_text_from_pdf
from app.parser import analyze_contract

def run_pipeline(file_path: str) -> dict:
    # Step 1: Extract text from PDF
    print(f"Extracting text from: {file_path}")

    try:
        text = extract_text_from_pdf(file_path)
        print(f"Extracted {len(text)} characters")
    except ValueError as e:
        # Catches scanned/image PDFs with no extractable text
        print(f"Extraction failed: {e}")
        raise

    # Step 2: Analyze with Gemini
    print("Sending to Gemini for analysis...")

    try:
        result = analyze_contract(text)
        print("Analysis complete")
        return result
    except json.JSONDecodeError as e:
        # Catches when Gemini returns malformed or unexpected output
        print(f"Failed to parse Gemini response as JSON: {e}")
        raise ValueError(
            "AI returned an unexpected response format. Please try again."
        )
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise