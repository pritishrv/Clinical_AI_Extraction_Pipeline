import subprocess
import sys
import os
from pathlib import Path

def run_stage(script_name):
    print(f"\n>>> Running {script_name}...")
    script_path = Path(f"Git Folder/Clinical_AI_Extraction_Pipeline/OCR-NER-Pipeline-v3/src/{script_name}")
    try:
        subprocess.check_call([sys.executable, str(script_path)])
        print(f">>> {script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f">>> Error in {script_name}: {e}")
        return False
    return True

def main():
    print("=== Clinical AI Platinum Zonal Pipeline v5 Orchestrator ===")
    
    stages = [
        "stage1_zonal_segmentation.py",
        "stage2_platinum_mapper.py"
    ]
    
    for stage in stages:
        if not run_stage(stage):
            print("\n!!! Pipeline aborted due to stage failure. !!!")
            sys.exit(1)
            
    print("\n=== Platinum Pipeline Execution Complete ===")
    print("Final database is available at: OCR-NER-Pipeline-v3/output/generated-database-platinum.xlsx")

if __name__ == "__main__":
    main()
