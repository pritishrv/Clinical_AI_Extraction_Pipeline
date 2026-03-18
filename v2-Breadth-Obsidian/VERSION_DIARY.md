# V2 - Breadth Obsidian Standard

### Implementation Steps:
1.  **Phase Classifier:** Implemented a keyword-based classifier to tag documents as Baseline, Restaging, or Surgical.
2.  **State Machine Router:** Created a routing table to direct data to specific chronological columns (e.g., T-Stage -> 2nd MRI: mrT).
3.  **Strict Validation:** Enforced specific mappings based on the clinical journey phase.

### Results:
- **Density:** 551 Clinical Cells.
- **Accuracy:** Maximum clinical safety and chronological integrity.

### Strategic Rationale:
Attempted to solve the "Temporal Conflict" problem. While extremely accurate, it was too strict for the messy clinical shorthand, causing a drop in density.
