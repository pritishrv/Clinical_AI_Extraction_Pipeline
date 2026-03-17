from pathlib import Path
import pandas as pd
import os


ROOT_DIR = Path(__file__).resolve().parents[2]
BASELINE_SOLUTION_DIR = ROOT_DIR / "baseline-solution"
DEFAULT_GENERATED_WORKBOOK = BASELINE_SOLUTION_DIR / "output" / "generated-database-codex.xlsx"
DEFAULT_PROTOTYPE_WORKBOOK = ROOT_DIR / "data" / "hackathon-database-prototype.xlsx"

def validate(generated_path, prototype_path):
    print(f"--- Validating {generated_path} against {prototype_path} ---")
    
    if not os.path.exists(generated_path):
        print(f"Generated file not found: {generated_path}")
        return

    df_gen = pd.read_excel(generated_path)
    df_proto = pd.read_excel(prototype_path)

    print(f"Generated rows: {len(df_gen)}")
    print(f"Prototype rows: {len(df_proto)}")

    # Check columns
    gen_cols = set(df_gen.columns)
    proto_cols = set(df_proto.columns)
    
    missing_cols = proto_cols - gen_cols
    extra_cols = gen_cols - proto_cols
    
    if missing_cols:
        print(f"Missing columns in generated file: {len(missing_cols)}")
    else:
        print("All prototype columns present in generated file.")

    # Simple demographic check on first row (if both have data)
    if len(df_gen) > 0 and len(df_proto) > 0:
        # Key: NHS Number
        nhs_col = 'Demographics: \nNHS number(d)'
        # Drop NaNs for validation comparison or pick the first matching patient
        proto_nhs = str(df_proto[nhs_col].iloc[0]).strip()
        
        # Check if prototype patient exists in our generated set
        gen_nhs_list = df_gen[nhs_col].dropna().astype(str).tolist()
        # Clean up .0 from float conversion
        gen_nhs_list = [n.replace(".0", "") for n in gen_nhs_list]
        
        match_found = proto_nhs in gen_nhs_list
        print(f"Prototype NHS Number ({proto_nhs}) found in generated set: {match_found}")
        
        if match_found:
            print("Success: Baseline demographic extraction found the prototype patient.")
        else:
            print(f"Failure: Could not find prototype patient in first 10 extracted NHS numbers: {gen_nhs_list[:10]}")

if __name__ == "__main__":
    validate(DEFAULT_GENERATED_WORKBOOK, DEFAULT_PROTOTYPE_WORKBOOK)
