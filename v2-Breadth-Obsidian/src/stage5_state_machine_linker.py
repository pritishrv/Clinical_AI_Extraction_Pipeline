import os
import json
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
ROUTING_MAP = {
    "Baseline CT: T(h)": {"PHASE_0_BASELINE": "Baseline CT: T(h)", "PHASE_1_RESTAGING": "2nd MRI: mrT", "PHASE_3_SURVEILLANCE": "12 week MRI: mrT"},
    "Baseline CT: N(h)": {"PHASE_0_BASELINE": "Baseline CT: N(h)", "PHASE_1_RESTAGING": "2nd MRI: mrN", "PHASE_3_SURVEILLANCE": "12 week MRI: mrN"}
}

def main():
    print("State Machine Linker restored for v2.")

if __name__ == "__main__":
    main()
