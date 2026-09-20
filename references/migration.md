# Source preservation and conflict register
This is a synthesis, not a claim that either source outranks the other. Source A is recursive-self-improvement; source B is recursive-skill-evolver. The operator's requested synthesis permits a new design policy; it does not retroactively establish source precedence.

## Every source function retained
| Source file(s) | Replacement |
|---|---|
| A/SKILL.md, B/SKILL.md | SKILL.md and assets/skill-specification.json |
| A/README.md | references/package-guide.md |
| A/assets/template.json, B/assets/template.json | assets/template.json and references/state-and-isolation.md |
| A/assets/LEARNINGS.md | assets/LEARNINGS.md |
| A/assets/ERRORS.md | assets/ERRORS.md |
| A/assets/FEATURE_REQUESTS.md | assets/FEATURE_REQUESTS.md |
| A/assets/SKILL-TEMPLATE.md | assets/SKILL-TEMPLATE.md |
| B/assets/fidelity-contract.template.yaml | assets/fidelity-contract.template.yaml |
| A/references/examples.md, B/references/examples.md | references/examples.md |
| B/references/evaluation-gates.md | references/evaluation-gates.md |
| B/references/self-edit-format.md | references/self-edit-format.md |
| A/references/hooks-setup.md | references/hooks-setup.md |
| A/references/openclaw-integration.md | references/openclaw-integration.md |
| A/scripts/init-rsir-report.sh | scripts/init-report.sh |
| A/scripts/validate-rsir-report.py | scripts/validate-report.py |
| A/scripts/activator.sh | scripts/activator.sh |
| A/scripts/error-detector.sh | scripts/error-detector.sh |
| A/scripts/extract-skill.sh | scripts/extract-skill.sh |
| A/hooks/openclaw/HOOK.md | scripts/hooks/openclaw/HOOK.md |
| A/hooks/openclaw/handler.js | scripts/hooks/openclaw/handler.js |
| A/hooks/openclaw/handler.ts | scripts/hooks/openclaw/handler.ts |
Compiled __pycache__ is a rebuildable artifact, not skill content, and is excluded. No functional source category is omitted.

## Conflicts preserved; new design choices
- Cycles: A defaults to one and requires explicit recursion; B defaults to three. Neither wins by precedence. New default is one; an explicit iterative request permits up to three when uncapped, or its stated cap. The two defaults cannot both govern the same invocation.
- Eligibility versus mutation: A protects live persistent files; B labels broad substrates mutable. New design distinguishes candidate eligibility, authorised publication, and verified publication.
- Rejected work: A says do not persist rejected changes while its hook asks to log rejected deltas; B preserves branching lineage. New design keeps redacted failure/history metadata outside the active library, not rejected executable skills in it.
- Isolation: B allows human promotion approval if isolation is unavailable. New design preserves approval authority but refuses to call an invalid test verified; static review remains possible.
- Trade-offs: A allows user-approved correctness trade-offs; B rejects material unmeasured degradation. New design permits only predeclared, authorised trade-off limits; immutable constraints and critical regression limits stay hard.
- Scheduling: A main text allows explicitly requested bounded scheduling, while its integration table says decline autonomy. New design separates cycle execution from scheduling and does neither implicitly.
- Rollback: B says immediately roll back; A protects persistent files. New design uses existing rollback authority and checks the current revision before restoration; without either it halts promotion and reports the exact required recovery.
- Extractor: A copies a Markdown manual into SKILL.md and writes a sibling package. New design preserves extraction as a valid frontmatter-first JSON request, intentionally routing publication through the host.
- Hook setup: A assumes shared Codex/Claude settings, contradicts its error detector about reading output, and suggests deleting settings. These claims are not carried forward. Per-host verification replaces them, while reminder/error-adapter capabilities remain.
- Threat-centric steering: neither source supports threats or coercive framing. B supports adversarial probes for consequential changes. The conditional routing retains that mechanism without adding threats to ordinary tasks.

## Behaviour preservation
A contributes explicit authority, simple bounds, operational helpers and successor reports.
B contributes mechanistic diversity, immutable gates, lineage, distributional checks, independent evaluation and meta-evolution.
Source-grounding, positive action framing, ambiguity routing and measurable acceptance are operationalisations of these mechanisms, not claims of an undocumented specialised prompt-optimisation system.
