# errors.py
# Custom exception classes for the contract parser

class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails"""
    pass

class EmptyDocumentError(Exception):
    """Raised when PDF contains no extractable text"""
    pass

class AIParsingError(Exception):
    """Raised when AI returns malformed or unexpected response"""
    pass

class FileTooLargeError(Exception):
    """Raised when uploaded file exceeds size limit"""
    pass