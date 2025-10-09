import cv2
import numpy as np
from typing import Union
import io
from PIL import Image

def enhance_image(image: Union[np.ndarray, str, bytes]) -> np.ndarray:
    """
    Enhanced image processing function that can handle file paths, numpy arrays, or bytes
    """
    try:
        # Handle different input types
        if isinstance(image, str):
            # Input is file path
            image_array = cv2.imread(image)
        elif isinstance(image, bytes):
            # Input is bytes
            image_pil = Image.open(io.BytesIO(image))
            image_array = np.array(image_pil)
            # Convert RGB to BGR for OpenCV
            if len(image_array.shape) == 3:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        elif isinstance(image, np.ndarray):
            # Input is already numpy array
            image_array = image
        else:
            raise ValueError("Unsupported image input type")
        
        if image_array is None:
            raise ValueError("Could not load image")
        
        # Convert to grayscale if it's a color image
        if len(image_array.shape) == 3:
            image_gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image_array
        
        # Step 1: Contrast Limited Adaptive Histogram Equalization (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image_gray)
        
        # Step 2: Gaussian blur for noise reduction
        enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
        
        # Step 3: Sharpening filter
        kernel = np.array([[-1, -1, -1], 
                          [-1,  9, -1], 
                          [-1, -1, -1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        
        # Step 4: Normalize the image
        enhanced = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
        
        return enhanced
        
    except Exception as e:
        raise Exception(f"Image enhancement failed: {str(e)}")

def batch_enhance_images(images: list) -> list:
    """Process multiple images"""
    return [enhance_image(img) for img in images]

def compare_image_quality(original: np.ndarray, enhanced: np.ndarray) -> dict:
    """Compare original and enhanced image quality"""
    # Calculate quality metrics
    orig_std = np.std(original)
    enh_std = np.std(enhanced)
    
    return {
        "original_std_dev": float(orig_std),
        "enhanced_std_dev": float(enh_std),
        "contrast_improvement": float(enh_std - orig_std)
    }