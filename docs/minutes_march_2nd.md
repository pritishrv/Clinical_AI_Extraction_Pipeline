# Health Hackathon Anonymised Dataset Meeting
**Date:** Monday 2nd March 12:00 - 12:30

**Attendees:** Alex (MOD), Anita (NHS), Daniel (City), Hitesh (NHS), Eleanor (City)
**Added for awareness:** Maeve (Hackathon Master of Ceremony), Marjahan (City/IWD Planning), Syed (Hackathon Planning)

## Meeting Agenda

1. Anonymised vs. Synthetic dataset status (Eleanor, Anita)
2. Information Governance and Ethics (Alex, Hitesh)
3. Software standards: DTAC and Medical Device compliance (Alex)
4. Hackathon logistics and longitudinal patient data (Daniel, Anita)

## Minutes

- **Anonymised vs. Synthetic Data**: 50 MDT cases have been anonymised using dummy NHS numbers (starting with "NNN") and date shifting to protect patient identity. To address remaining ethics concerns, the team will use ChatGPT to generate a fully synthetic dataset based on these anonymised examples, removing the need for formal ethics committee approval.

- **Longitudinal Patient Data**: The dataset will present patient history in a sequential (linear) format in Excel. Attributes will be populated as they appear in the documents; where information is missing or not discussed, the cells will be left null (empty).

- **Ground Truth**: The Excel spreadsheet created by the team serves as the "ground truth" or expected output for participants. Participants must extract clinical findings as prose directly from the MDT documents into this specific format.

- **Technical Standards (DTAC)**: Software developed should ideally align with Digital Technology Assessment Criteria (DTAC), specifically regarding clinical safety (DCB0129/DCB0160) and data residency.

- **Medical Device Compliance**: Depending on the level of risk and clinical decision support, the software could be classified as a Software as a Medical Device (SaMD), requiring specific regulatory adherence.

- **Logistics**: The hackathon can currently accommodate 106 students. Daniel will follow up with Alex regarding travel cost reimbursement.

- **Project Outlook**: This hackathon is viewed as the second iteration of an ongoing series, with the goal of establishing long-term research projects and UKRI project proposals.

## Action Points

- **Eleanor**: Create 50 synthetic MDT cases based on the 5-6 initial examples using ChatGPT
- **Daniel**: Formulate "baseline solution" pipeline to demonstrate to students how to structure the software
- **Eleanor**: Set up meeting for Monday 09.03.2026 at 11:00 to approve the synthetic set and discuss day-of planning
- **Anita**: The Kerridge Lecture confirmed for next week
