import os
import pandas as pd
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
GENERATED_WORKBOOK = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/generated-database-v3.xlsx"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"

def validate():
    print("--- Stage 4: Validation (v3) ---")
    
    if not os.path.exists(GENERATED_WORKBOOK):
        print(f"Error: Generated workbook not found at {GENERATED_WORKBOOK}")
        return

    df_gen = pd.read_excel(GENERATED_WORKBOOK)
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)

    print(f"Generated rows: {len(df_gen)}")
    print(f"Prototype rows: {len(df_proto)}")

    # Check non-empty cells density
    total_cells = df_gen.size
    non_empty_cells = df_gen.notna().sum().sum() - (df_gen == "").sum().sum()
    print(f"Total non-empty cells in generated: {non_empty_cells}")

    # Column alignment check
    gen_cols = list(df_gen.columns)
    proto_cols = list(df_proto.columns)
    
    if gen_cols == proto_cols:
        print("Success: 100% Column alignment matched.")
    else:
        print(f"Warning: Column mismatch. Generated: {len(gen_cols)}, Prototype: {len(proto_cols)}")

    # NHS Number matching
    nhs_col = 'Demographics: \nNHS number(d)'
    gen_nhs = df_gen[nhs_col].astype(str).str.replace(".0", "").tolist()
    proto_nhs_val = str(df_proto[nhs_col].iloc[0]).split(".")[0]
    
    if proto_nhs_val in gen_nhs:
        print(f"Success: Prototype NHS Number ({proto_nhs_val}) found in generated data.")
    else:
        print(f"Failure: Prototype NHS Number ({proto_nhs_val}) NOT found.")

    # Density comparison with baseline reports
    # Claude reported 675 cells
    if non_empty_cells > 675:
        print(f"Success: v3 density ({non_empty_cells}) exceeds Claude v1 baseline (675).")
    else:
        print(f"Info: v3 density ({non_empty_cells}) is below Claude v1 baseline (675). Further NER tuning required.")

if __name__ == "__main__":
    validate()
