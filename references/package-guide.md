# Bounded Skill Evolution
A replacement design for recursive-self-improvement and recursive-skill-evolver, not an autonomous model-training engine.

Start at SKILL.md. The complete machine-readable interface is assets/skill-specification.json; supporting files remain part of the specification.
Python 3.10+ is required for the report tools. Shell wrappers require Bash. Optional bootstrap adapter tests require Node.js.

Commands (from the package root):
- bash scripts/init-report.sh /absolute/task/report.json
- python3 scripts/validate-report.py /absolute/task/report.json
- bash scripts/extract-skill.sh /absolute/task/report.json new-skill-name
- python3 -B scripts/self-test.py
- node scripts/tests/hook.test.js

Initial reports are deliberately incomplete and fail final validation. Fill them with observations, not invented results.
The extractor prints a JSON publication request to stdout and never installs a skill.
Read references/migration.md for every source-file mapping, conflicts, and explicit exclusions.
Hooks are optional and disabled until explicitly configured; no hook starts an evolution cycle or grants authority.
