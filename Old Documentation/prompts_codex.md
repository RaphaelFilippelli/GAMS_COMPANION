# Prompt Templates for Codex

Use these when generating/altering code. Always paste the relevant spec link(s).

## Template: Implement Module
```
You are Codex acting as Implementer.
Goal: Implement <module> per the spec.

Read:
- <repo-root>/agents.md
- <repo-root>/agents_v2.md
- <repo-root>/<spec-file>.md

Acceptance criteria:
- Unit tests in tests/<path>/test_<module>.py
- Ruff & pytest pass locally
- Function signatures and docstrings match spec
- No I/O at module import time

Now write the code for <module> in a single reply.
```
## Template: Add Feature
```
You are Codex acting as Implementer.
Goal: Add feature "<feature>" to <module>.

Constraints:
- Backward-compatible
- Update docs and examples
- Add tests covering success and failure modes
```
## Template: Reviewer
```
You are Codex acting as Reviewer.
Run static review on the following diff (paste diff).
List issues by severity, then propose minimal edits.
```
