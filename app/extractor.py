# extractor.py
# Handles PDF text extraction
import pdfplumber
from app.errors import EmptyDocumentError, PDFExtractionError

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def extract_text_from_pdf(file_path: str) -> str:
    try:
        with pdfplumber.open(file_path) as pdf:
            # Check if PDF has pages at all
            if len(pdf.pages) == 0:
                raise EmptyDocumentError(
                    "PDF contains no pages."
                )

            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except EmptyDocumentError:
        raise
    except Exception as e:
        raise PDFExtractionError(
            f"Failed to read PDF file: {str(e)}"
        )

    # catch scanned/image PDFs with no extractable text
    if not text.strip():
        raise EmptyDocumentError(
            "Document contains no extractable text. "
            "Please upload a text-based PDF."
        )

    return text