# 09 Bottom-Up Semantic Harvester Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies the **Ultimate Extraction Pipeline (v6)** designed to achieve 100% data density across all 88 columns. It abandons "slot-based" parsing in favor of a **Semantic Harvesting** approach.

The architecture ensures that even non-standard phrasing and "hidden" clinical shorthand are captured and correctly mapped to the target database.

---

## Background and Motivation

The "Density Plateau" occurs because clinicians use inconsistent labels (e.g., "Surgery date," "Op date," "Date of resection"). Hard-coded rules cannot scale to these variations.

**The Semantic Harvester Solution:**
1.  **Exhaustive Harvesting:** Extract every token, sentence, and labeled pair from the document.
2.  **Semantic Mapping:** Use local embeddings to find the best Excel column for every piece of extracted text.
3.  **Clinical Inference:** Use oncology-specific heuristics to fill "implied" data points (e.g., specific drug names implying a "Curative" intent).

---

## Technical Stack

- **Harvester:** `python-docx` + Recursive Table/Paragraph Miner.
- **Semantic Brain:** `sentence-transformers` (Local Embedding Model).
- **Inference Engine:** Custom Python heuristic layer.
- **Verification:** Cross-zonal validation to prevent data duplication.

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage1_exhaustive_harvester.py # Pulls every possible KV pair into a raw list
│   ├── stage2_semantic_mapper.py      # Uses Embeddings to map KVs to the 88 columns
│   ├── stage3_inference_logic.py      # Fills implied gaps (shorthand reasoning)
│   └── pipeline_v6_harvester.py       # Orchestration
├── output/
│   ├── raw_harvest/                   # Huge JSON of every potential data point
│   └── generated-database-v6.xlsx     # Final Maximum Density output
```

---

## Implementation Order

1.  **Harvester:** Build a script that extracts every line, every table cell, and every `key: value` pair into a flat list of "Candidates."
2.  **Embedding Setup:** Download and cache a local `Sentence-Transformer` model.
3.  **Mapper:** Create the logic that compares "Candidate Keys" against the "88 Target Headers" and selects the best fit.
4.  **Assembly:** Generate the final workbook with forced string safety.

---

## Author Attribution

This prompt was authored by Gemini CLI.
