# 00 Prompt Starter

Author: Codex

## Prompt Purpose

Use this prompt as the required onboarding and handoff check before doing any further work in `baseline-solution/`.

## Prompt

You are the next AI agent working in the `baseline-solution/` directory of this repository.

Before doing any implementation work, you must:

1. Read `baseline-solution/work-diary.md`.
2. Confirm in your response that you understand what this directory is for.
3. Confirm in your response that you understand the task you are expected to carry forward.
4. Report which prompts or major actions have already been executed, based on the work diary.
5. Report that you are ready for work.
6. Ask the user what prompt or action should be carried out next.

Your confirmation should make clear that you understand:
- `baseline-solution/` is the baseline solution area for the Clinical AI Hackathon repository
- the repo currently contains the challenge brief and datasets, while this directory defines the implementation path
- the work diary is the record of what prompts and actions have already been carried out
- the next step must be explicitly confirmed with the user rather than assumed by the agent

After you complete any additional work, you must update:
- `baseline-solution/work-diary.md`

Your update to the work diary must be detailed enough that another AI agent can continue without re-discovering what changed.

At minimum, the work diary update should include:
- what you inspected
- what you changed
- why you made those changes
- if applicable, what prompt was followed to execute the tasks

Each work diary entry, or clearly grouped block of entries, must be signed by the agent that wrote it so authorship remains explicit for later handoff.

Do not skip the diary update. Treat it as part of the task, not optional documentation.

After completing this starter prompt:
- do not assume which prompt should run next
- do not assume that implementation has not started
- wait for the user to tell you what prompt or action should be carried out next

## Example Work Diary Entry

```md
### Entry

Followed prompt: `baseline-solution/prompts/00-prompt-starter.md`
**Date:** March 15, 2026
**Signed:** Codex
```

## Author Attribution

This starter prompt was authored by Codex.
