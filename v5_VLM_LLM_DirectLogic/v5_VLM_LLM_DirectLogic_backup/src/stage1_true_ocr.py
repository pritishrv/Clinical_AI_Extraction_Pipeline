import os
import easyocr
import cv2
from pathlib import Path
from tqdm import tqdm

# Configuration
IMAGE_DIR = Path("v5_version_1/output/images")
OCR_OUT_DIR = Path("v5_version_1/output/ocr_raw")

def run_ocr_on_case(image_path, reader):
    """Performs true OCR and tries to preserve layout using coordinates."""
    results = reader.readtext(str(image_path))
    
    # Sort results by vertical (y) coordinate then horizontal (x)
    # results format: [([[x,y], [x,y], [x,y], [x,y]], 'text', confidence), ...]
    sorted_results = sorted(results, key=lambda x: (x[0][0][1], x[0][0][0]))
    
    lines = []
    current_line_y = -1
    line_threshold = 15 # pixels to consider same line
    
    current_line_text = []
    for (bbox, text, prob) in sorted_results:
        y_coord = bbox[0][1]
        
        if current_line_y == -1 or abs(y_coord - current_line_y) < line_threshold:
            current_line_text.append(text)
            current_line_y = y_coord
        else:
            lines.append("  ".join(current_line_text))
            current_line_text = [text]
            current_line_y = y_coord
            
    if current_line_text:
        lines.append("  ".join(current_line_text))
        
    return "\n".join(lines)

def main():
    if not os.path.exists(OCR_OUT_DIR): os.makedirs(OCR_OUT_DIR)
    
    print("Initializing EasyOCR (this will download models on first run)...")
    reader = easyocr.Reader(['en'], gpu=True) # Will use Metal on Mac if available
    
    image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")])
    
    print(f"Running True OCR on {len(image_files)} images...")
    for f_name in tqdm(image_files):
        img_path = IMAGE_DIR / f_name
        raw_text = run_ocr_on_case(img_path, reader)
        
        out_path = OCR_OUT_DIR / f_name.replace(".png", ".txt")
        with open(out_path, "w") as f:
            f.write(raw_text)

if __name__ == "__main__":
    main()
