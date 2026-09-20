---
name: bounded-skill-evolution
description: "Optional bounded evolution bootstrap reminder; no automatic edits."
metadata: {"openclaw":{"events":["agent:bootstrap"]}}
---
# Bootstrap reminder
The adapter only appends its owned virtual reminder, skips subagents and avoids duplicate injection.
Use one entrypoint (handler.js or handler.ts), not both. Confirm the installed host API before enabling; local tests are not live integration proof.
