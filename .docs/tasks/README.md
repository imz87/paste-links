# Tasks

This directory stores planner-generated task specifications.

Workflow:

- Planner writes new task specs to `backlog/`.
- When a task starts, move it from `backlog/` to `in-progress/`.
- Implementation reads the task file from `in-progress/` and applies the change.
- Review is a separate manual phase after development.
- When implementation and manual review are complete, move the task from `in-progress/` to `done/`.
- Task specs must end with a concise commit message.

Directory meanings:

- `backlog/` - planned tasks that are not currently being implemented
- `in-progress/` - the task currently being implemented or reviewed
- `blocked/` - tasks that need clarification, approval, or another dependency first
- `done/` - completed task history

Blocked task rules:

- Do not start blocked tasks until the blocker is resolved.
- Explain the blocker under `# Questions`, `# Risks`, or `# Blocked Reason`.

Keep task files small, focused, and clearly named.
Preferred filename format: `NNN-short-title.md` with stable zero-padded numbering.
