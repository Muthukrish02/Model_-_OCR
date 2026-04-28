"""Image processing utilities"""
import base64
import cv2
from src.config import IMAGE_SIZE


def preprocess_image(image_path, output_size=IMAGE_SIZE):
    """
    Preprocess image: resize and save as temporary file
    
    Args:
        image_path (str): Path to input image
        output_size (int): Target size for resizing (default from config)
        
    Returns:
        str: Path to preprocessed image
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        img_resized = cv2.resize(img, (output_size, output_size))
        output_path = "temp_preprocessed.png"
        cv2.imwrite(output_path, img_resized)
        
        return output_path
    except Exception as e:
        print(f"❌ Image preprocessing error: {str(e)}")
        return image_path


def encode_image(image_path):
    """
    Encode image to base64 string for API transmission
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        str: Base64 encoded image string
    """
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        print(f"❌ Image encoding error: {str(e)}")
        return ""


def get_image_info(image_path):
    """
    Get basic information about an image
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: Image information (dimensions, type, etc.)
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        height, width = img.shape[:2]
        return {
            "width": width,
            "height": height,
            "path": image_path
        }
    except Exception as e:
        print(f"❌ Error getting image info: {str(e)}")
        return None
