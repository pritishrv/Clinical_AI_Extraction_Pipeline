import subprocess
import sys
import os
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
SRC_DIR = PROJECT_ROOT / "v6-Spatial-Reasoning-Implementation/src"

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
    print("=== Clinical AI v6 Spatial Reasoning Orchestrator ===")
    
    stages = [
        "stage1_spatial_harvester.py",
        "stage2_spatial_reasoner.py",
        "stage3_spatial_assembler.py"
    ]
    
    for stage in stages:
        if not run_stage(stage):
            print("\n!!! v6 Pipeline aborted due to stage failure. !!!")
            sys.exit(1)
            
    print("\n=== v6 Spatial Reasoning Implementation Complete ===")
    print("Final Database: v6-Spatial-Reasoning-Implementation/output/generated-database-v6-spatial.xlsx")

if __name__ == "__main__":
    main()
