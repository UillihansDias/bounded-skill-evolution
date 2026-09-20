#!/usr/bin/env python3
"""Check report consistency, not the truth of external evidence."""
import argparse
import json
import math
from pathlib import Path

HARD = {"integrity", "fidelity", "regression", "gain", "independence"}
ALL = HARD | {"holdout", "adversarial", "distribution", "efficiency"}
DECISIONS = {"review", "reject", "inconclusive", "eligible", "promoted"}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def number(value):
    return type(value) in (int, float) and math.isfinite(value)

def string_list(value):
    return isinstance(value, list) and all(nonempty(x) for x in value)

def validate(d):
    require(isinstance(d, dict), "report must be an object")
    require(type(d.get("schema_version")) is int and d["schema_version"] == 1, "schema_version must be 1")
    decision = d.get("decision")
    require(decision in DECISIONS, "invalid decision")
    require(nonempty(d.get("reason")), "decision reason required")
    require(string_list(d.get("source_anchors")), "source_anchors must be string list")
    require(string_list(d.get("unknown_fields")), "unknown_fields must be string list")
    candidates = d.get("candidates")
    require(isinstance(candidates, list), "candidates must be list")
    partial_review = decision == "review" and not candidates
    for k in ("target", "objective", "parent", "rollback_target"):
        if partial_review and not nonempty(d.get(k)):
            require(k in d["unknown_fields"], "record unknown field: " + k)
        else:
            require(nonempty(d.get(k)), k + " required")
    require(partial_review or d["source_anchors"], "source anchors required")
    c = d.get("contract")
    require(isinstance(c, dict), "contract required")
    for k in ("mutable_paths", "protected_paths", "acceptance_criteria", "unresolved_conflicts"):
        require(string_list(c.get(k)), k + " must be string list")
    require(partial_review or c["acceptance_criteria"], "acceptance criteria required")
    require(not set(c["mutable_paths"]) & set(c["protected_paths"]), "mutable/protected collision")
    for k in ("cycle_cap", "candidate_cap"):
        require(type(c.get(k)) is int and c[k] > 0, k + " must be positive integer")
    for k in ("max_calls", "max_seconds"):
        if c.get(k) is None:
            require(partial_review and "contract." + k in d["unknown_fields"], "unknown limit only allowed in declared incomplete review")
        else:
            require(type(c.get(k)) is int and c[k] >= 0, k + " must be nonnegative integer")
    require(type(d.get("cycle")) is int and d["cycle"] >= 1, "cycle must be positive")
    usage = d.get("usage")
    require(isinstance(usage, dict), "usage required")
    within_budget = d["cycle"] <= c["cycle_cap"] and len(candidates) <= c["candidate_cap"]
    measured_usage = True
    for k, limit in (("calls", "max_calls"), ("seconds", "max_seconds")):
        value = usage.get(k)
        if value is None:
            require("usage." + k in d["unknown_fields"], "unknown usage must be declared")
            measured_usage = False
        else:
            require(number(value) and value >= 0, "invalid usage." + k)
            if k == "calls":
                require(type(value) is int, "calls must be integer")
            within_budget = within_budget and c[limit] is not None and value <= c[limit]
    require(type(c.get("consequential")) is bool, "consequential must be boolean")
    constraints = c.get("constraints")
    require(isinstance(constraints, list), "constraints must be list")
    constraint_names = set()
    for bound in constraints:
        require(isinstance(bound, dict) and nonempty(bound.get("metric")), "constraint metric required")
        require(bound["metric"] not in constraint_names, "duplicate constraint")
        constraint_names.add(bound["metric"])
        require(bound.get("operator") in (">=", "<=") and number(bound.get("bound")), "invalid constraint bound")
    baseline = d.get("baseline")
    require(isinstance(baseline, dict), "baseline required")
    ids = set()
    for candidate in candidates:
        require(isinstance(candidate, dict), "candidate must be object")
        for k in ("id", "parent", "hypothesis", "falsifier", "change", "risk", "evidence", "outcome_reason"):
            require(nonempty(candidate.get(k)), "candidate." + k + " required")
        require(candidate["id"] not in ids, "duplicate candidate id")
        ids.add(candidate["id"])
        require(candidate["parent"] == d["parent"], "candidate parent mismatch")
        require(candidate.get("kind") in ("ordinary", "meta"), "invalid candidate kind")
        require(candidate.get("outcome") in ("reject", "inconclusive", "eligible"), "candidate outcome required")
        require(string_list(candidate.get("changed_paths")) and candidate["changed_paths"], "changed_paths required")
        require(all(p in c["mutable_paths"] for p in candidate["changed_paths"]), "undeclared/protected changed path")
        require(string_list(candidate.get("prior_cases")), "prior_cases must be string list")
    require(isinstance(d.get("gates"), list), "gates must be list")
    seen = {}
    for gate in d["gates"]:
        require(isinstance(gate, dict), "gate must be object")
        require(isinstance(gate.get("candidate_id"),str) and gate["candidate_id"] in ids, "unknown gate candidate")
        require(isinstance(gate.get("name"),str) and gate["name"] in ALL, "unknown gate")
        key = (gate["candidate_id"], gate["name"])
        require(key not in seen, "duplicate gate")
        require(gate.get("result") in ("pass", "fail", "not_run", "not_applicable"), "invalid gate result")
        require(nonempty(gate.get("reason")), "gate reason required")
        if gate["result"] in ("pass", "fail"):
            require(nonempty(gate.get("evidence")), "executed gate evidence required")
        if gate["name"] in HARD:
            require(gate["result"] != "not_applicable", "hard gate cannot be not_applicable")
        seen[key] = gate
    for key in ("lineage", "rejected_patterns", "failure_classes", "lessons", "evidence", "historical_versions"):
        require(isinstance(d.get(key), list), key + " must be list")
    require(isinstance(d.get("meta_evolution"),dict), "meta_evolution required")
    for key in ("successful_edit_families", "unsuccessful_edit_families", "history"):
        require(isinstance(d["meta_evolution"].get(key),list), "meta history missing " + key)
    require(isinstance(d.get("metrics"),dict), "metrics required")
    for key in ("capability","fidelity","regressions","cost","latency","tool_calls","recursion_depth","distributional_quality"):
        require(isinstance(d["metrics"].get(key),list), "metric history missing " + key)
    require(isinstance(d.get("successor_state_notes"),dict), "successor notes required")

    eligible = set()
    for candidate in candidates:
        cid = candidate["id"]
        failed = any(g["result"] == "fail" for (i,n),g in seen.items() if i == cid)
        if failed:
            require(candidate["outcome"] == "reject", "failed gate requires candidate rejection")
        if candidate["outcome"] == "reject":
            require(failed or nonempty(candidate.get("rejection_evidence")), "rejection evidence required")
        available = candidate.get("constraint_measurements", {})
        require(isinstance(available,dict), "constraint_measurements must be object")
        for bound in constraints:
            if bound["metric"] not in available:
                continue
            observation = available[bound["metric"]]
            require(isinstance(observation,dict) and number(observation.get("value")) and nonempty(observation.get("evidence")), "invalid recorded constraint measurement")
            value = observation["value"]
            satisfied = value >= bound["bound"] if bound["operator"] == ">=" else value <= bound["bound"]
            if not satisfied:
                require(candidate["outcome"] == "reject", "known constraint violation requires rejection")
                require(any(seen.get((cid,k),{}).get("result") == "fail" for k in ("fidelity","regression")), "known constraint violation requires failed fidelity or regression gate")
        if candidate["outcome"] != "eligible":
            continue
        require(within_budget and measured_usage, "eligibility requires measured in-budget run")
        require(not c["unresolved_conflicts"] and not d["unknown_fields"], "unresolved conflict or unknown field")
        for k in ALL:
            require((cid,k) in seen, "missing gate " + k)
            result = seen[(cid,k)]["result"]
            require(result == "pass" if k in HARD else result in ("pass","not_applicable"), "gate did not pass: " + k)
        if c["consequential"]:
            require(seen[(cid,"holdout")]["result"] == "pass", "consequential candidate requires holdout")
            require(seen[(cid,"adversarial")]["result"] == "pass", "consequential candidate requires adversarial check")
        require(nonempty(baseline.get("metric")) and number(baseline.get("value")) and nonempty(baseline.get("evidence")), "measured baseline required")
        m = candidate.get("measurement")
        require(isinstance(m,dict), "measurement required")
        require(number(m.get("value")) and number(m.get("min_gain")) and m["min_gain"] > 0, "finite measurement and positive min_gain required")
        require(m.get("direction") in ("higher","lower"), "measurement direction required")
        require(c.get("metric") == baseline["metric"], "frozen metric mismatch")
        require(c.get("direction") == m["direction"], "frozen direction mismatch")
        require(number(c.get("min_gain")) and c["min_gain"] == m["min_gain"], "frozen threshold mismatch")
        delta = m["value"] - baseline["value"]
        if m["direction"] == "lower": delta = -delta
        require(delta >= m["min_gain"], "target gain below threshold")
        require(nonempty(m.get("evidence")), "measurement evidence required")
        require(type(m.get("sample_count")) is int and m["sample_count"] > 0, "sample_count required")
        require(type(m.get("critical_regressions")) is int and m["critical_regressions"] == 0, "critical regressions present")
        observations = candidate.get("constraint_measurements")
        require(isinstance(observations,dict) and set(observations) == constraint_names, "constraint measurement set mismatch")
        for bound in constraints:
            observation = observations[bound["metric"]]
            require(isinstance(observation,dict) and number(observation.get("value")) and nonempty(observation.get("evidence")), "constraint evidence required")
            value = observation["value"]
            ok = value >= bound["bound"] if bound["operator"] == ">=" else value <= bound["bound"]
            require(ok, "constraint violated: " + bound["metric"])
        if candidate["kind"] == "meta":
            require(len(set(candidate["prior_cases"])) >= 2, "meta requires distinct prior cases")
        eligible.add(cid)

    if decision in ("eligible", "promoted"):
        require(d.get("selected_candidate") in eligible, "selected candidate not eligible")
    elif decision == "inconclusive":
        require(not eligible and (not candidates or any(x["outcome"] == "inconclusive" for x in candidates)), "cycle should be eligible or reject")
    elif decision == "reject":
        require(candidates and all(x["outcome"] == "reject" for x in candidates), "cycle rejection requires all candidates rejected")
    publication = d.get("publication")
    require(isinstance(publication,dict) and type(publication.get("authorised")) is bool, "publication authority must be boolean")
    if decision == "promoted":
        require(publication["authorised"], "publication not authorised")
        for k in ("authority_reference", "receipt", "revision"):
            require(nonempty(publication.get(k)), "publication." + k + " required")
        require(any(isinstance(x,dict) and x.get("parent") == d["parent"] and x.get("child") == publication["revision"] and x.get("candidate_id") == d["selected_candidate"] for x in d["lineage"]), "publication lineage missing")
    else:
        require(not publication.get("receipt") and not publication.get("revision"), "non-promoted report cannot claim publication")
    return True

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("report")
    a = p.parse_args()
    try:
        validate(json.loads(Path(a.report).read_text(encoding="utf-8")))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        p.exit(1, "INVALID: " + str(exc) + "\n")
    print("VALID: structural and decision consistency only; evidence truth not verified.")

if __name__ == "__main__":
    main()
