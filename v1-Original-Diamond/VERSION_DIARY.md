# V1 - Original Diamond Standard

### Implementation Steps:
1.  **Exhaustive Harvester:** Used regex to mine all T/N/M markers from the Word tables.
2.  **Semantic Mapper:** Implemented `all-MiniLM-L6-v2` embeddings to map clinical shorthand to Excel columns.
3.  **Greedy Linker:** Merged multiple documents for the same patient into one row using a "First-Found" priority.

### Results:
- **Density:** 1,102 Clinical Cells.
- **Accuracy:** High recall, but potential for temporal misallocation (e.g., Post-chemo data filling Baseline slots).

### Strategic Rationale:
Our first major breakthrough. Proved that longitudinal patient linking could break the "Claude Code Ceiling" of 675 cells.
