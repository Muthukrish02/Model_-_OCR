"""Barcode scanning module using pyzbar"""
from pyzbar.pyzbar import decode
from PIL import Image


def scan_barcodes(image_path):
    """
    Scan for barcodes in an image using pyzbar
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        list: List of barcode dictionaries with type, data, and position
    """
    try:
        img = Image.open(image_path)
        barcodes = decode(img)
        
        if not barcodes:
            return []
        
        results = []
        for barcode in barcodes:
            results.append({
                "type": barcode.type,
                "data": barcode.data.decode("utf-8"),
                "rect": barcode.rect
            })
        return results
    except Exception as e:
        print(f"❌ Barcode scanning error: {str(e)}")
        return []
