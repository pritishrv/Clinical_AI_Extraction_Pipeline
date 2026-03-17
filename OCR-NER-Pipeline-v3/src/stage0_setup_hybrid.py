import subprocess
import sys

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("--- Stage 0: Hybrid Setup (PaddleOCR + MedSPaCy) ---")
    
    # Requirements for PaddleOCR and MedSPaCy
    packages = [
        "paddlepaddle",
        "paddleocr",
        "medspacy",
        "spacy",
        "pandas",
        "openpyxl",
        "python-docx",
        "img2pdf", # useful for doc to image conversion
        "pdf2image"
    ]
    
    for package in packages:
        try:
            install_package(package)
        except Exception as e:
            print(f"Error installing {package}: {e}")

    # Ensure en_core_web_sm is available
    print("Downloading spacy model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

    print("\n--- Hybrid Setup Complete ---")

if __name__ == "__main__":
    main()
