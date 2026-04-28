"""OCR module - Image text extraction and barcode scanning"""
from .barcode_scanner import scan_barcodes
from .gemini_ocr import gemini_ocr

__all__ = ["scan_barcodes", "gemini_ocr"]
