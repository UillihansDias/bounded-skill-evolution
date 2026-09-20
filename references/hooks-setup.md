# Optional reminder adapters
The adapters emit reminders only. They do not collect transcripts, modify skills, configure a scheduler, or initiate recursion.
Inspect the installed host's documented hook contract before integration. This package makes no claim that Claude Code, Codex, Copilot and OpenClaw share a settings format.

Local checks:
- bash scripts/activator.sh: prints a short reminder.
- bash scripts/error-detector.sh 2: prints a failure-triage reminder.
- bash scripts/error-detector.sh 0: prints nothing.
- node scripts/tests/hook.test.js: exercises the source-derived bootstrap event adapter.

error-detector.sh accepts an explicit numeric exit status. A host adapter must map its documented event to that argument; no undocumented environment variable is assumed. It never reads tool output. A nonzero status prompts diagnosis, not automatic rejection.

For OpenClaw consult references/openclaw-integration.md and scripts/hooks/openclaw/HOOK.md. TypeScript and JavaScript files are alternative entrypoints to one implementation, not two hooks.
When enabling/disabling any hook, preserve unrelated configuration and use the host's supported mechanism. Do not delete a settings file to disable one hook.
