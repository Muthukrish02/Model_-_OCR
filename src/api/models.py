"""
API Models for request/response validation and documentation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class BarcodeResult(BaseModel):
    """Barcode detection result"""
    type: str = Field(..., description="Barcode type (e.g., CODE128, QR_CODE)")
    data: str = Field(..., description="Decoded barcode data")
    rect: Optional[dict] = Field(None, description="Barcode position in image")


class ImageProcessingRequest(BaseModel):
    """Request for image processing"""
    image_path: str = Field(..., description="Path to image file")
    use_local_model: bool = Field(False, description="Use local VL model instead of Gemini")
    prompt: Optional[str] = Field(None, description="Custom prompt for OCR (optional)")


class BarcodeResponse(BaseModel):
    """Response for barcode scanning"""
    success: bool
    source: str = "barcode"
    barcodes: List[BarcodeResult]
    count: int
    processing_time_ms: float


class OCRResponse(BaseModel):
    """Response for OCR processing"""
    success: bool
    source: str  # "gemini_ocr" or "local_ocr"
    text: str
    processing_time_ms: float


class SmartProcessingResponse(BaseModel):
    """Response for smart processing (barcode + OCR fallback)"""
    success: bool
    source: str  # "barcode" or "gemini_ocr" or "local_ocr"
    barcodes: Optional[List[BarcodeResult]] = None
    text: Optional[str] = None
    processing_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "ok"
    gemini_configured: bool
    llama_server_running: bool
    services: dict


class TTSRequest(BaseModel):
    """Request for text-to-speech"""
    text: str = Field(..., description="Text to convert to speech")
    filename: Optional[str] = Field("output.mp3", description="Output filename")


class TTSResponse(BaseModel):
    """Response for text-to-speech"""
    success: bool
    filename: str
    message: str


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    details: Optional[str] = None
