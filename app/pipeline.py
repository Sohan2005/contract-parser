# pipeline.py
# Connects the full pipeline: PDF -> text -> AI -> JSON
import os
from app.extractor import extract_text_from_pdf
from app.errors import (
    EmptyDocumentError,
    PDFExtractionError,
    AIParsingError,
    FileTooLargeError
)

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def run_pipeline(file_path: str) -> dict:
    # Check file size before doing anything
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(
            f"File exceeds maximum size of {MAX_FILE_SIZE_MB}MB. "
            f"Your file is {file_size / 1024 / 1024:.1f}MB."
        )

    # Step 1: Extract text from PDF
    print(f"Extracting text from: {file_path}")
    text = extract_text_from_pdf(file_path)
    print(f"Extracted {len(text)} characters")

    # Step 2: Analyze with Gemini
    from app.parser import analyze_contract
    print("Sending to Gemini for analysis...")
    result = analyze_contract(text)
    print("Analysis complete")

    return result