# Bounded Skill Evolution

A safety-bounded, evidence-gated workflow for improving reusable OpenClaw agent skills, diagnosing recurring execution failures, and retesting successor capabilities against measurable contracts.

Synthesizes recursive self-improvement and evolutionary skill development into a disciplined, bounded system that prevents uncontrolled recursion, unauthorized mutations, or unverified capability claims.

---

## Core Workflow

1. **Route and Establish Authority**: Confirm explicit trigger (repeated failures or explicit user request); classify into review, ordinary evolution, or meta-evolution; lock protected versus mutable files.
2. **Freeze Baseline**: Establish measurable acceptance criteria, trade-off boundaries, and baseline fidelity contracts before testing candidates.
3. **Diagnose and Propose**: Identify root causes from execution evidence rather than symptoms; develop targeted candidate changes.
4. **Isolated Evaluation**: Test proposed candidate skills in isolation without polluting active runtime configurations or workspace state.
5. **Measured Gates & Promotion**: Verify candidate against strict regression gates; promote only with verified proof.
6. **Successor Recording**: Log structured learnings and validation artifacts for successor runs.

---

## Directory Structure

```text
bounded-skill-evolution/
├── README.md                              # Package overview and usage
├── SKILL.md                               # Canonical skill specification and execution workflow
├── assets/
│   ├── fidelity-contract.template.yaml    # Baseline fidelity & regression contract
│   ├── skill-specification.json          # Machine-readable skill contract
│   ├── template.json                     # Cycle report schema
│   ├── ERRORS.md                          # Log template for error capture
│   ├── FEATURE_REQUESTS.md                # Log template for missing capabilities
│   ├── LEARNINGS.md                       # Log template for reusable insights
│   └── SKILL-TEMPLATE.md                  # Template for extracted skill candidates
├── references/
│   ├── evaluation-gates.md                # Verification thresholds & gates
│   ├── examples.md                        # Worked examples and scenarios
│   ├── hooks-setup.md                     # Optional hook integration guide
│   ├── migration.md                       # Lineage, conflict register, and design decisions
│   ├── openclaw-integration.md            # OpenClaw runtime bindings
│   ├── package-guide.md                   # Command reference & package documentation
│   ├── routing.md                         # Task classification and routing rules
│   ├── self-edit-format.md                # Candidate modification standards
│   └── state-and-isolation.md             # Context hygiene and isolation boundaries
└── scripts/
    ├── init-report.sh                     # Initialize a cycle report
    ├── validate-report.py                 # Validate schema and gate compliance
    ├── extract-skill.sh                   # Extract validated candidates into skills
    ├── self-test.py                       # Package test suite
    ├── activator.sh                       # Environment activation helper
    ├── error-detector.sh                  # Runtime failure detector
    └── hooks/                             # OpenClaw adapter hooks
```

---

## Key Scripts & Commands

From the repository root:

```bash
# Initialize a new cycle report
bash scripts/init-report.sh /path/to/report.json

# Validate a cycle report against schema and acceptance gates
python3 scripts/validate-report.py /path/to/report.json

# Extract a validated candidate as a new skill package
bash scripts/extract-skill.sh /path/to/report.json new-skill-name

# Run the package self-test suite
python3 -B scripts/self-test.py
```

---

## Safety & Invariant Boundaries

- **No Uncontrolled Self-Modification**: Does not modify global agent configurations, system prompts, credentials, or scheduler state without explicit human approval.
- **Strict Isolation**: Candidates are evaluated in isolated sandboxes; unverified changes are never merged into active skills.
- **Fail Closed**: A candidate failing any regression threshold or fidelity gate is rejected automatically.
- **No Hallucinated Verification**: Plausible logic or multiple LLM endorsements never substitute for runtime observation and test verification.

---

## Installation in OpenClaw

```bash
openclaw skills install ./bounded-skill-evolution --as bounded-skill-evolution
```

Skill entry point: [`SKILL.md`](SKILL.md).
