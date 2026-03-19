import subprocess
import sys
import os
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
SRC_DIR = PROJECT_ROOT / "v9-Holistic-Structural-Attention/src"

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
    print("=== Clinical AI v9 Holistic Structural Attention Orchestrator ===")
    
    stages = [
        "stage1_holistic_harvester.py",
        "stage2_holistic_reasoner.py",
        "stage3_longitudinal_assembler.py"
    ]
    
    for stage in stages:
        if not run_stage(stage):
            print("\n!!! v9 Pipeline aborted due to stage failure. !!!")
            sys.exit(1)
            
    print("\n=== v9 Holistic Implementation Complete ===")
    print("Final Database: v9-Holistic-Structural-Attention/output/generated-database-v15-holistic.xlsx")

if __name__ == "__main__":
    main()
