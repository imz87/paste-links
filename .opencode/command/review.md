---
description: Review implemented task changes and move approved tasks through the lifecycle.
agent: sherlock-holmes-reviewer
---

Review request: $ARGUMENTS

# Review Command Notes

- Accept these `$ARGUMENTS` forms:
  - No arguments: select the first markdown task in `.docs/tasks/in-progress/` by filename sort order and review it.
  - `<task-markdown-path>` only: review that task.
  - `<task-markdown-path> <task-markdown-path> ...`: review the listed tasks sequentially in the argument order.
- If selecting from in-progress automatically, ignore non-markdown files and directories, and choose the lexicographically first `*.md` file.
- If no task path is provided and `.docs/tasks/in-progress/` has no markdown task files, stop and report that there is no task ready for review.
- The task markdown path must point to `.docs/tasks/in-progress/` unless the user explicitly asks for a different review target.
- Start the command with a clear best-effort session title hint using the selected task or task batch, for example: `Session title: Review 002 add conditional menu visibility`.
- Treat the session title hint as prompt guidance only; opencode custom commands do not provide a guaranteed session-title field.
- Read `AGENTS.md`, the selected task specification, and the implemented changes before judging the task.
- Review the implementation against the task acceptance criteria, out-of-scope constraints, architecture notes, and verification expectations.
- Ask `sherlock-holmes-reviewer` to review exactly the selected task and implemented changes.
- Instruct the reviewer to review for:
  - correctness
  - maintainability
  - security
  - simplicity
  - compliance with the task specification
- Instruct the reviewer to verify:
  - acceptance criteria are satisfied
  - requirements are implemented
  - out-of-scope items were not added
  - existing architecture is respected
  - no unnecessary abstractions were introduced
  - boundaries remain clear
  - clipboard and filesystem handling are intentional
  - user-visible Nautilus behavior remains coherent
  - user input is validated where relevant
  - manual verification expectations are reasonable
- Instruct the reviewer to prefer simple fixes, avoid personal style preferences, and prioritize correctness and security.
- Do not broaden scope beyond the selected task.
- Do not create git commits, stage files, stash files, push, or rewrite history.

## Review Outcomes

- If the task is approved:
  - Add a concise completion section to the task file with review verdict, summary, verification checked, and any residual risks.
  - Move the task markdown file from `.docs/tasks/in-progress/` to `.docs/tasks/done/`.
- If the task is rejected or approved with required changes:
  - Keep the task markdown file in `.docs/tasks/in-progress/`.
  - Report the blocking findings and concrete fixes required.
  - Do not move the task to `.docs/tasks/done/`.
- If evidence is insufficient to approve or reject:
  - Keep the task markdown file in `.docs/tasks/in-progress/`.
  - Report what is missing, such as verification results, changed-file context, or acceptance-criteria evidence.

## Final Response

Final response must include:

- Reviewed task file or files
- Verdict for each task: `Approve`, `Approve With Changes`, or `Reject`
- Findings
- Recommended fixes, if any
- Risk assessment: `Low`, `Medium`, or `High`, with a short explanation
- Verification commands or evidence reviewed
- Task lifecycle action taken, such as moved to `.docs/tasks/done/` or left in `.docs/tasks/in-progress/`
- Suggested commit message if the task is approved
