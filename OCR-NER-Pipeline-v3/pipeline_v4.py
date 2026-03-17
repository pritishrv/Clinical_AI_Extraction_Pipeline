import subprocess
import sys
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
    print("=== Clinical AI Hybrid Pipeline v4 Orchestrator ===")
    
    stages = [
        "stage1_table_extraction_v2.py",
        "stage2_clinical_ner_v4.py",
        "stage3_excel_assembly_v4.py",
        "validate_v3.py"
    ]
    
    for stage in stages:
        if not run_stage(stage):
            print("\n!!! Pipeline aborted due to stage failure. !!!")
            sys.exit(1)
            
    print("\n=== Pipeline Execution Complete ===")

if __name__ == "__main__":
    main()
