---
description: Review changes, suggest a commit message, and commit only after confirmation.
agent: junio-hamano-committer
---

Commit request: $ARGUMENTS

# Commit Command Notes

- Inspect `git status --short --branch` and the upstream relationship first.
- Inspect staged changes before unstaged changes.
- Inspect unpushed commits (`HEAD` vs upstream).
- If the unpushed history is already clean enough, do not rewrite it: amend the last commit when the new changes belong there, or create one new commit for staged changes.
- If the unpushed history needs organization, propose a small rewrite of only the unpushed range (reword, squash, fixup, split, or amend) and ask for confirmation before doing it.
- If the working tree is clean and only unpushed commits remain, switch to history-cleanup mode and organize the full unpushed range.
- Prefer staged changes only.
- If files are staged, commit only the staged files unless the user explicitly asks for more.
- If nothing is staged, ask before staging anything.
- Summarize the scope, then suggest one best commit message and, if useful, up to two alternates.
- Use Conventional Commits v1.0.0 and include task IDs when relevant.
- When a task file exists, include only the task filename in the footer instead of the path or only the numeric task ID, for example `Refs: 003-add-fedora-packaging.md`.
- If only the task number and title are known, include both without a directory prefix, for example `Refs: task-003 add fedora packaging`.
- Commit message format must be `<type>[optional scope][optional !]: <description>` followed by an optional body and optional footer(s).
- Use `feat` only for new features and `fix` only for bug fixes. Other allowed types include `docs`, `chore`, `ci`, `build`, `style`, `refactor`, `perf`, `test`, and `revert`.
- Prefer a one-line commit message only for very small, obvious changes.
- Add a commit body when the change has meaningful implementation details, motivation, tradeoffs, risks, verification notes, or reviewer context.
- The body must begin one blank line after the subject and explain what changed and why, not merely repeat the subject.
- Add footers when useful for task IDs, issue references, co-authors, reviewed-by, or other trailer-style metadata.
- Use footer format compatible with git trailers, such as `Refs: task-003` or `Reviewed-by: Name`.
- Breaking changes must be marked with `!` in the type/scope prefix or with a `BREAKING CHANGE: <description>` footer. `BREAKING CHANGE` must be uppercase.
- Ask for explicit confirmation before any `git add`, `git commit`, `git commit --amend`, `git reset`, or history rewrite.
- Never push.

## Guardrails

- Be concise.
- Default to the smallest safe change.
- Do not rewrite unpushed history unless it clearly helps organization.
- Never push to any remote.

## Recommended Decision Flow

1. Check staged files.
2. Check unpushed commits.
3. If the working tree is clean, organize the full unpushed range.
4. If the latest unpushed commit already matches the new work, suggest amend.
5. If the unpushed commits are messy or overlapping, suggest a small rewrite plan for the unpushed range.
6. If neither applies, commit the staged files as a new commit.
7. Wait for confirmation before acting.

## Final Response

Final response must include:

- Upstream / unpushed commit status
- Staged files
- Short change summary
- Recommended action (`amend`, `new commit`, or `rewrite unpushed range`)
- If the tree is clean, recommended action should be `rewrite unpushed range`
- Suggested commit message
- Alternates if needed
- Commit hash after the action succeeds
