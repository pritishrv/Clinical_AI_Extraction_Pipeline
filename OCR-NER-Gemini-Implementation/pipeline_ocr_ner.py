import os
import subprocess
import sys

def run_stage(stage_name, script_path):
    """
    Run a single stage of the pipeline as a subprocess.
    """
    print(f"\n--- Starting {stage_name} ---")
    try:
        # Run the stage script using the same python interpreter
        subprocess.run([sys.executable, script_path], check=True)
        print(f"--- {stage_name} completed successfully ---")
    except subprocess.CalledProcessError as e:
        print(f"Error during {stage_name}: {e}")
        return False
    return True

def main():
    # Set the working directory to the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check for Stage 1 dependencies
    try:
        subprocess.run(["tesseract", "--version"], check=True, capture_output=True)
    except:
        print("Warning: Tesseract OCR not found in system path. Stage 1 may fail.")

    # Run the pipeline stages
    if not run_stage("Stage 1 (OCR Extraction)", "src/stage1_ocr_extraction.py"):
        sys.exit(1)
        
    if not run_stage("Stage 2 (Clinical NER)", "src/stage2_clinical_ner.py"):
        sys.exit(1)
        
    if not run_stage("Stage 3 (Excel Assembly)", "src/stage3_excel_assembly.py"):
        sys.exit(1)

    print("\nOCR-NER Pipeline completed successfully.")
    print("Output available at output/final_database_v3.xlsx")

if __name__ == "__main__":
    main()
