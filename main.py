# main.py
from app.extractor import extract_text_from_pdf

text = extract_text_from_pdf("test_contract.pdf")
print(text)