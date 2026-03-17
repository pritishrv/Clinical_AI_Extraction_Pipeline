# Work Diary - README.md Development Session
**Date:** March 13, 2026

## Session Objective
Prepare the hackathon repository with necessary and sufficient documentation for participant email distribution.

## File Organization

### Created Directory Structure
```
hackathon-baseline-solution/
├── docs/          # Background documentation
└── data/          # Dataset files
```

### Files Moved to docs/
- `specification.md` - Original clinical problem email
- `minutes_february_12.md` - Problem definition meeting
- `minutes_march_2nd.md` - Dataset and scope meeting
- `mdt_list.png` - Example MDT list format
- `mdt_outcome.png` - Example MDT outcome format

### Files Moved to data/
- `hackathon-mdt-outcome-proformas.docx` - Input data (50 synthetic MDT cases)
- `hackathon-database-prototype.xlsx` - Expected output format

### Formatting Applied
Applied consistent markdown formatting to meeting minutes:
- Added proper headers (# ## ###)
- Formatted attendees and dates
- Created bullet lists for minutes and action points
- Bold formatting for responsible parties

## README.md Development

### Key Principle Established
"Necessary and sufficient" - include only information required to understand and complete the task. Avoid motivational content, excessive background, or repetition.

### Initial Issue
First draft contained excessive context, motivational statements, and information duplicated between sections.

### Content Rationalization
Removed 3 redundant bullet points that duplicated Dataset section:
- Anonymised vs. Synthetic Data (repeated Input description)
- Longitudinal Patient Data (repeated Output description)
- Ground Truth (repeated in Output and Success Criteria)

Retained unique technical considerations:
- DTAC standards (with link added)
- Medical Device Compliance (SaMD)

### Final Structure
1. **Banner image** - `digital_screen_1.jpg` at 50% width for branding
2. **Problem Statement** - Attributed to Dr Anita Wale, copied from specification.md
3. **Dataset** - Input/output with visual examples (`mdt_outcome.png`, `prototype.png`)
4. **Success Criteria** - Concise statement from meeting minutes
5. **Technical Considerations** - DTAC and SaMD, attributed to Dr Alex Nicholls
6. **Repository Structure** - Simplified tree showing main directories
7. **Next Steps** - Meeting details with Teams link
8. **Workshops** - Monday 16 - Thursday 19, College Building rooms
9. **Final** - Friday 20 11:00-15:30, venue details

### Attributions Added
- Problem Statement: "by Dr Anita Wale"
- Technical Considerations: "to be further discussed by Dr Alex Nicholls"

### Links Added
- DTAC: https://www.digitalregulations.innovation.nhs.uk/regulations-and-guidance-for-developers/all-developers-guidance/using-the-digital-technology-assessment-criteria-dtac/

### Visual Elements
- Banner: `digital_screen_1.jpg` (50% width using HTML img tag)
- Example images: `mdt_outcome.png` and `prototype.png` added between Dataset and Success Criteria

## Design Decisions

### Information Flow
Problem → Data → Success Criteria → Technical Considerations → Logistics

Rationale: "This is what you have to do, then these are some technical things to consider"

### Content Placement
Technical considerations placed after Success Criteria rather than before Dataset to maintain focus on the core task before introducing additional context.

### Repetition Elimination
All dataset details consolidated into single Dataset section. Technical details consolidated into single Technical Considerations section. No information duplicated across sections.

## Files Ready for Distribution
- `README.md` - Main participant documentation
- `docs/` - Background materials (specification, meeting minutes, example images)
- `data/` - Input Word document and output Excel example

## Final Refinements

### Image Organization
Moved all image files from root to `docs/` directory for cleaner structure:
- `digital_screen_1.jpg` - Banner image (in use)
- `logo_asset_2.jpg` - Alternate banner
- `mdt_outcome.png` - Example MDT outcome
- `prototype.png` - Example prototype output

Updated README.md references to point to `docs/` for all images.

### Visual Adjustments
- Increased banner width from 50% to 80% for better visibility
- Converted data file paths to clickable markdown links:
  - `data/hackathon-mdt-outcome-proformas.docx`
  - `data/hackathon-database-prototype.xlsx`

### Repository Rename
Renamed repository from `hackathon-baseline-solution` to `clinical-ai-hackathon`:
- **Rationale**: Original name misleading as baseline solution not yet provided; new name accurately reflects main hackathon repository
- Updated git remote URL: `git@github.com:dsikar/clinical-ai-hackathon.git`
- Renamed local directory to match: `~/git/citystgeorges-hackathon/clinical-ai-hackathon`

## Final Repository Structure
```
clinical-ai-hackathon/
├── README.md                 # Main documentation with banner, problem statement, dataset info
├── data/
│   ├── hackathon-mdt-outcome-proformas.docx
│   └── hackathon-database-prototype.xlsx
└── docs/
    ├── specification.md
    ├── minutes_february_12.md
    ├── minutes_march_2nd.md
    ├── work-diary.md
    ├── room_bookings.md
    ├── digital_screen_1.jpg    # Banner
    ├── logo_asset_2.jpg        # Alternate banner
    ├── mdt_list.png            # From specification
    ├── mdt_outcome.png         # From specification + example
    └── prototype.png           # Example output
```

## Status
Repository ready for mass email distribution to 106 hackathon participants.

---

# Work Diary - Pre-Hackathon Preparation Session
**Date:** March 15, 2026

## Session Objective
Finalise repository content and communications materials ahead of the hackathon starting Monday 16 March.

## Changes Made

### README.md
- Added detailed workshop schedule (Tuesday–Thursday) with daily themes: AI Agents, Coding with LLM APIs, Documentation and Allnighter
- Added allnighter details: ELG08 Study Area, 23:00–09:00, Monster + Pizza
- Expanded Friday schedule with room-by-room breakdown and times
- Added Activities Meeting Link section (Teams loop for all online attendees)
- Added inline link to Activities Meeting Link from Workshops section
- Updated Current Repository Structure to reflect actual state
- Added authorship note (Daniel Sikar and Claude Code)
- Resolved merge conflict with upstream changes (updated Q&A attendees: Hitesh Patel, Ellie Hickey)

### comms/ (new directory)
- `welcome-email.txt` — draft welcome email for 106 participants
- `mc-script-maeve.md` — MC script for Maeve Hutchinson, opening and closing ceremonies
- `recipients.txt` — gitignored recipient list template

### docs/
- `judging-criteria.md` — Friday judging sheet for clinician judges, with scoring rubric (1–4) and team table

### .gitignore
- Added to exclude `comms/recipients.txt` from version control

## Credits Section
- Added Credits section to end of README.md
- Clinical problem statement credited to Dr Anita Wale (linked to St George's profile)
- Repository credited to Daniel Sikar with Claude Code, OpenAI Codex and Google Gemini

---

# Work Diary - Hackathon Day 1
**Date:** March 16, 2026

## Changes Made

### TODO.md (new file)
- Created at root with 24 items covering: standard solution, judging criteria, community website, MC notes, DeepInfra credits, timetabling, catering, judge emails, daily comms emails, AV booking, Gemini sign-up, repo policy, scoring rubrics, team assignment, merchandise, prizes scripts (Syed, Boh, Golnaz, Chris/Sanowar)

### README.md
- Updated repository structure section to reflect baseline-solution/ directory and TODO.md
- Added Baseline Solution section before Workshops
- Updated image subheadings to "Example MDT Outcome (Input - Word document)" and "Example Prototype (Output - Excel spreadsheet)"

### Workflow note
- Agreed convention: one instruction at a time to avoid misreads and ensure exact wording is applied
