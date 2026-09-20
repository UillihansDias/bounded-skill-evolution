# State and isolation
Use a task-local directory selected by the user, or a newly allocated temporary directory. Keep reports and logs outside the installed skill.
State represents y (parent skill revision) and z (evidence, candidates, failed hypotheses, metrics, lineage and meta-policy history). Store references to artifacts, hashes and redacted summaries rather than broad transcript copies.

Before running candidate code, snapshot the declared parent files using the host versioning service or a reviewed copy operation into a separate task directory. Record identities for parent, candidate, evaluator and held-out fixture manifest. Reject symlinks or out-of-scope files unless explicitly resolved and included. The candidate may write only its sandbox; evaluator and protected data remain outside that write surface.
This package does not implement an OS sandbox. Use available runtime enforcement; ordinary filesystem copies only isolate edits, not code execution privileges.

Preserve immutable baseline records and create a new cycle report for a new cycle. Record failed trials rather than overwriting them. Use unique candidate IDs and explicit parent links. Keep a rollback target before publication; do not claim a rollback was tested unless exercised.

Before promotion and rollback re-read live revision identity. A mismatch is a concurrent edit, not permission to overwrite. The publication host owns transactionality and revision history; record its actual receipt. Missing capabilities leave a reviewable proposal, not a simulated success.

Log templates are optional. Fill them only from observed evidence and redact sensitive content; never copy templates over existing logs. Retention of useful failures does not require retaining secrets or every raw trace.

## Structured source-field migration
A.target_capability -> target; A.baseline_problem -> baseline + contract;
A.candidate_improvements -> candidates; A.fidelity_checks -> gates;
A.accepted_changes -> candidate outcome + selected_candidate + publication;
A.rejected_changes -> rejected_patterns + candidate rejection evidence;
A.successor_state_notes -> successor_state_notes.
B.skill.active_version -> parent; B.skill.name -> target; fidelity contract version remains in its contract artifact;
B.lineage -> lineage; B.evidence -> evidence; B.failure_classes -> failure_classes;
B.lessons -> lessons; B.candidates -> candidates; B.evaluations -> gates and referenced comparison artifacts;
B.metrics -> metrics (all eight history categories retained);
B.rejected_patterns -> rejected_patterns; B.meta_evolution -> meta_evolution (policy version, edit families, history);
B.rollback.last_known_good -> rollback_target.
historical_versions records branch revision, artifact reference, capability/cost trade-offs and comparison evidence.
For meaningful trade-offs, compare against relevant strong historical branches as well as the parent.

Reports may retain unknowns or overruns without claiming eligibility. A target-unknown review lists its unknown fields explicitly; zero provider calls is a valid budget. Populate per-candidate outcomes before aggregating the cycle decision.
Frozen secondary constraints use {metric, operator: >= or <=, bound}; each eligible candidate supplies matching constraint_measurements with value and evidence. The validator cannot discover an omitted real-world constraint: the contract review must check completeness.

An incomplete review may declare unknown budget limits through unknown_fields; it authorises no execution. For executable cycles choose concrete limits, including zero calls for offline review. Evidence of overrun remains reportable but cannot establish eligibility.
