# V3 - Fluke Grid Mapper

### Implementation Steps:
1.  **Coordinate Extractor:** Attempted to pull data from fixed table cells (e.g., Row 7 always equals Outcome).
2.  **Deterministic Mapping:** Bypassed NLP/NER in favor of raw positional extraction.

### Results:
- **Density:** 283 Clinical Cells.
- **Accuracy:** Very poor.

### Strategic Rationale:
A "Fluke" iteration. We hypothesized that the proformas followed a strict visual grid. In reality, merged cells and non-standard row shifts made coordinate-based extraction too brittle for the 50-case dataset. Discarded in favor of hybrid approaches.
