import os
import json
from docx import Document
from pdf2image import convert_from_path
from docx2pdf import convert
import pytesseract
from PIL import Image

# Configuration
DOCX_PATH = "../data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = "output/json_raw"

def segment_docx_to_images(docx_path):
    """
    In a real-world scenario, we would convert each case (table) to an image.
    For this prototype, we'll convert the document to PDF and then to images.
    """
    temp_pdf = "temp_proformas.pdf"
    print(f"Converting {docx_path} to PDF...")
    convert(docx_path, temp_pdf)
    
    print("Converting PDF to images...")
    images = convert_from_path(temp_pdf)
    
    # Cleanup temp PDF
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
    
    return images

def perform_ocr(images):
    """
    Perform OCR on each page/image and save as raw JSON.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for i, image in enumerate(images):
        print(f"Performing OCR on page {i+1}...")
        # Use PSM 6: Assume a single uniform block of text.
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        ocr_text = pytesseract.image_to_string(image)
        
        case_data = {
            "case_index": i,
            "raw_text": ocr_text,
            "ocr_metadata": ocr_data
        }
        
        output_path = os.path.join(OUTPUT_DIR, f"case_{i:03d}_raw.json")
        with open(output_path, "w") as f:
            json.dump(case_data, f, indent=4)
        
        print(f"Saved OCR output to {output_path}")

if __name__ == "__main__":
    # Ensure relative paths work from the script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")
    
    # Check if input exists
    if not os.path.exists(DOCX_PATH):
        print(f"Error: {DOCX_PATH} not found.")
    else:
        # Note: docx2pdf requires Microsoft Word on macOS/Windows.
        # If Word is not available, a different conversion method (like libreoffice) would be needed.
        try:
            images = segment_docx_to_images(DOCX_PATH)
            perform_ocr(images)
        except Exception as e:
            print(f"An error occurred during Stage 1: {e}")
            print("Tip: Stage 1 requires docx2pdf and Tesseract OCR installed on the system.")
