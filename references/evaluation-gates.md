# Evaluation gates
Freeze criteria before generation. Run integrity and fidelity checks before spending on behavioural trials.
1. Integrity: parent and candidate identities, declared changes, untouched protected files/evaluator/holdout, intact history.
2. Fidelity: preserved objective, permissions, promotion authority, rollback, and contract. Failed hard constraints are terminal.
3. Regression: replay known tasks and prior failures under matched conditions. Reject critical regressions even if mean quality rises.
4. Holdout: evaluate on cases not used for generation. Missing holdout lowers confidence; consequential changes require it or a separately authorised experimental deployment explicitly not claimed verified.
5. Adversarial diversity: only where routing justifies it; otherwise relevant boundary cases. Record not_applicable with a reason for conditional gates.
6. Gain: compare actual target measurements to a predeclared minimum gain and quality floor. Equal scores are not improvement unless a frozen efficiency objective improves while quality remains within its declared bounds.
7. Distribution: inspect variance, worst cases, failure concentration and calibration when enough samples exist. Report sample limitations rather than manufacture tail statistics.
8. Efficiency: calls, delegated calls, tokens where available, latency, retries and cycle count. Unknown measurements remain unknown.

For each gate store candidate_id, name, result (pass/fail/not_run/not_applicable), evidence locator or redacted observation, and reason. Integrity, fidelity, regression, gain and independence are mandatory. The full set additionally requires holdout, adversarial, distribution and efficiency records. Conditional not_applicable is never a hard-gate pass.

Proposer, executor, verifier and publisher may be different programs, agents or people. A frozen deterministic test can supply independent evidence; a second model alone does not. Test validity matters more than nominal verifier category. A formal checker proves only its encoded property.

Distinguish infrastructure error from candidate failure: investigate a missing executable, unavailable tool, expected negative-test exit, or contaminated fixture before attributing it to the candidate. Rerun only after a meaningful correction; preserve both attempts.

Promotion requires every hard gate passed, no unresolved source conflict affecting execution, existing publication authority, immutable parent identity, and a verified publication receipt. Authority cannot waive failed evaluation or convert missing evidence into passing evidence. Experimental installation, if separately requested, is labelled as such.

## Candidate and cycle decisions
Each candidate is reject, inconclusive or eligible, with an outcome reason.
Any failed gate makes that candidate reject. Rejection without a failed gate requires separate rejection evidence.
An eligible cycle selects an eligible candidate; other rejected candidates remain recorded.
When all candidates are rejected the cycle is reject; when none is eligible and at least one is unresolved the cycle is inconclusive.
Review can record unresolved target/authority without inventing values. Exceeded budgets and unknown measurements remain valid historical observations but block eligibility.

Evaluate every available constraint measurement even for inconclusive candidates: a known violation requires rejection and a matching failed fidelity/regression gate. Missing measurements are different from measured failures.
