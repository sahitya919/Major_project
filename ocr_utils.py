try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None
import os

class OCRUtils:
    def __init__(self):
        self.enabled = False
        if Image and pytesseract:
            self.enabled = True
            # Optional: Specify tesseract cmd path if needed for Windows
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        else:
            print("[WARNING] PIL or pytesseract not installed. OCR will be disabled.")

    def extract_text(self, image_path):
        """
        Extracts text from an image file.
        """
        if not self.enabled:
            return ""
        
        try:
            if not os.path.exists(image_path):
                print(f"[ERROR] Image {image_path} not found.")
                return ""

            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            print(f"[ERROR] OCR failed: {e}")
            return ""
    
    def is_image(self, file_path):
        """
        Simple check if a file path points to an image.
        """
        if not os.path.exists(file_path):
            return False
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except:
            return False
