import subprocess
import sys
import os
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
SRC_DIR = PROJECT_ROOT / "v4-Baseline-Master/src"

def run_stage(script_name):
    print(f"\n>>> Running {script_name}...")
    script_path = SRC_DIR / script_name
    try:
        subprocess.check_call([sys.executable, str(script_path)])
        print(f">>> {script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f">>> Error in {script_name}: {e}")
        return False
    return True

def main():
    print("=== Clinical AI v4 Precision Master Orchestrator ===")
    
    stages = [
        "stage1_exhaustive_harvester.py",
        "stage2_semantic_mapper.py",
        "stage4_longitudinal_linker.py",
        "stage5_evidence_assembler.py"
    ]
    
    for stage in stages:
        if not run_stage(stage):
            print("\n!!! Pipeline aborted due to stage failure. !!!")
            sys.exit(1)
            
    print("\n=== v4 Precision Pipeline Execution Complete ===")
    print("Final Precision Database: v4-Baseline-Master/output/v4-master-baseline-1130.xlsx")

if __name__ == "__main__":
    main()
