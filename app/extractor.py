# extractor.py
# Handles PDF text extraction
import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Guard: catch scanned/image PDFs with no extractable text
    if not text.strip():
        raise ValueError(
            "Document contains no extractable text. "
            "Please upload a text-based PDF."
        )

    return text