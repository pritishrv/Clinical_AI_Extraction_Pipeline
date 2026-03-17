import subprocess
import sys
import os

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_spacy_model(model_url):
    print(f"Downloading model from {model_url}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", model_url])

def main():
    print("--- Stage 0: Environment Setup ---")
    
    # Required packages
    packages = [
        "medspacy",
        "scispacy",
        "pandas",
        "openpyxl",
        "python-docx",
        "spacy"
    ]
    
    for package in packages:
        try:
            install_package(package)
        except Exception as e:
            print(f"Error installing {package}: {e}")

    # Best-in-class clinical models from scispaCy
    models = [
        "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz",
        "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz"
    ]
    
    for model_url in models:
        try:
            download_spacy_model(model_url)
        except Exception as e:
            print(f"Error downloading model {model_url}: {e}")

    print("\n--- Setup Complete ---")

if __name__ == "__main__":
    main()
