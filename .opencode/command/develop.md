---
description: Implement a planner task with the project task lifecycle.
agent: linus-torvalds-developer
---

Task file: $ARGUMENTS

# Develop Command Notes

- Accept these `$ARGUMENTS` forms:
  - No arguments: select the first markdown task in `.docs/tasks/backlog/` by filename sort order and implement it.
  - `<task-markdown-path>` only: use that task.
  - `<task-markdown-path> <task-markdown-path> ...`: run the listed tasks sequentially in the argument order.
- If selecting from backlog automatically, ignore non-markdown files and directories, and choose the lexicographically first `*.md` file.
- Never automatically select tasks from `.docs/tasks/blocked/`.
- If no task path is provided and `.docs/tasks/backlog/` has no markdown task files, stop and report that there is no backlog task to develop.
- If multiple task paths are provided, process them strictly one by one in the argument order.
- Read each selected task markdown file before implementing that task.
- Start the command with a clear best-effort session title hint using the selected task or task batch, for example: `Session title: Develop 002 add conditional menu visibility`.
- Treat the session title hint as prompt guidance only; opencode custom commands do not provide a guaranteed session-title field.
- The task markdown path may point to either `.docs/tasks/backlog/` or `.docs/tasks/in-progress/`.
- If the task starts in `.docs/tasks/backlog/`, move it to `.docs/tasks/in-progress/` before asking the developer to implement it.
- If the task already starts in `.docs/tasks/in-progress/`, keep it there.
- Before starting each task, record a git baseline for reporting:
  - `git status --short`
  - `git diff --name-status`
- Before implementation, ensure the developer context includes:
  - `AGENTS.md`
  - the selected task document
  - relevant project documentation referenced by the task
- Ask the configured developer agent to implement exactly that task.
- Instruct the developer to follow these implementation rules:
  - Prefer modifying existing code.
  - Do not rewrite working code without reason.
  - Do not introduce large abstractions.
  - Do not create new dependencies unless justified by the task.
  - Do not perform unrelated refactors.
  - Preserve existing behavior unless the task explicitly asks for a behavior change.
  - Reuse existing install, filesystem, and extension patterns where practical.
  - Keep manual verification steps focused and realistic.
  - When renaming a tracked file, use `git mv old-path new-path` instead of delete-and-recreate or copy-and-delete workflows.
- Ask the developer to report, for each task:
  - files changed
  - implementation summary
  - verification or manual verification steps
  - assumptions made
- Always record the task change group, even when only one task is processed.
- Do not ask `sherlock-holmes-reviewer` to review after implementation finishes.
- Do not run an automatic review/fix loop from this command.
- Review must be started manually as a separate phase after development.
- After each task finishes implementation, record the task change group before starting the next task:
  - task filename
  - implementation summary
  - manual review status, usually `pending manual review`
  - unresolved issues if any
  - verification commands run
  - files changed for that task, using the developer output plus `git diff --name-status` compared with the pre-task baseline where practical
- If the working tree already has changes before a task starts, list them as the pre-task baseline and do not silently attribute them to the current task.
- Do not create git commits, stage files, stash files, or use git to split changes unless the user explicitly asks for commits or staging.
- Git itself does not group uncommitted changes by task; maintain the grouping in the command's final report.
- After each task finishes implementation, keep its task markdown file in `.docs/tasks/in-progress/` for manual review.
- After all tasks are implemented, inform the user to run the `review` command to review and complete the task lifecycle. The `review` command handles moving approved tasks from `.docs/tasks/in-progress/` to `.docs/tasks/done/`.
- Final response must include a `Changes By Task` section that groups changed files by task filename, plus implementation summaries, manual review status, unresolved issues if any, verification commands run, and suggested commit messages.
- Do not broaden scope beyond the task file.
- Do not mark a task complete or reviewed from this command.
- Preserve task acceptance criteria.
