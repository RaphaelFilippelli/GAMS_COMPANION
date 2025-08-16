# SYNC_PROTOCOL.md — How we stay in sync

This repo is the **source of truth**. To keep the AI assistant in sync:

1) **Auto status on every push**
   - A GitHub Action writes `docs/AUTO_STATUS.md` with: timestamp, HEAD SHA, subject, author, and changed files.
   - The action commits that file back to `main` (and is configured to avoid infinite loops).

2) **Assistant check-in trigger**
   - In chat, say: **“sync repo”** (optionally add a commit SHA/branch). The assistant will browse:
     - Repo root & latest commits
     - `docs/AUTO_STATUS.md`
     - `tasks_backlog.md`
     - Any PRs/issues labeled `needs-assistant`

3) **Labeling for attention**
   - Tag issues/PRs with `needs-assistant` when you want the assistant to pick them up next.

4) **Single source of priorities**
   - Keep priorities in `tasks_backlog.md` (top to bottom). The assistant will treat it as the queue.

5) **Lightweight change log (optional)**
   - Append a one-liner to `docs/CHANGELOG.md` per meaningful change. This helps cross-session context.

**Note**: The assistant cannot watch the repo continuously; it checks only when you ask during a chat.
