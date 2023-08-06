"""
The package for extracting metadata from pdf files.
"""

import logging
from typing import Dict
from PyPDF2 import PdfReader


def get_pages(pdf_path: str) -> Dict[str, str]:
    """
    Returns a dictionary containing the number of
    pages the pdf found at `pdf_path` contains.
    """
    logging.info("Getting pdf pages")
    reader = PdfReader(pdf_path)
    return {"pages": str(len(reader.pages))}
