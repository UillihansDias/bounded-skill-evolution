#!/usr/bin/env python3
"""Deterministic contract/helper tests, not LLM behavioural efficacy tests."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT/"scripts/validate-report.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

def fixture():
    d = json.loads((ROOT/"assets/template.json").read_text())
    d.update(target="file-router",objective="Route supplied files correctly",source_anchors=["fixture:source"],parent="parent-v1",rollback_target="parent-v1",decision="eligible",reason="Measured improvement on fixed fixture",selected_candidate="c1")
    d["contract"].update(mutable_paths=["SKILL.md"],protected_paths=["evaluator.py"],acceptance_criteria=["accuracy gain >= 0.1; no critical regression"],max_calls=30,max_seconds=60,metric="accuracy",direction="higher",min_gain=0.1)
    d["baseline"]={"metric":"accuracy","value":0.5,"evidence":"fixture:baseline"}
    d["candidates"]=[{"id":"c1","parent":"parent-v1","kind":"ordinary","outcome":"eligible","outcome_reason":"fixed fixture gain","constraint_measurements":{},"hypothesis":"file-first routing fixes failure","falsifier":"file tasks still search first","change":"Add conditional file route","changed_paths":["SKILL.md"],"risk":"overroutes open-web tasks","evidence":"fixture:failure","prior_cases":[],"measurement":{"value":0.8,"min_gain":0.1,"direction":"higher","sample_count":10,"critical_regressions":0,"evidence":"fixture:comparison"}}]
    d["gates"]=[{"candidate_id":"c1","name":k,"result":"pass","evidence":"fixture:"+k,"reason":"Synthetic fixture assertion"} for k in sorted(v.ALL)]
    return d

class ContractTests(unittest.TestCase):
    def test_valid_eligible(self):
        self.assertTrue(v.validate(fixture()))
    def test_unfilled_template_rejected(self):
        with self.assertRaises(ValueError):
            v.validate(json.loads((ROOT/"assets/template.json").read_text()))
    def test_review_without_candidates(self):
        d=fixture();d.update(decision="review",selected_candidate=None,candidates=[],gates=[])
        self.assertTrue(v.validate(d))
    def test_meta_with_distinct_history(self):
        d=fixture();d["candidates"][0].update(kind="meta",prior_cases=["a","b"])
        self.assertTrue(v.validate(d))
    def test_promoted_with_receipt(self):
        d=fixture();d["decision"]="promoted"
        d["publication"]={"authorised":True,"authority_reference":"fixture:user","receipt":"fixture:receipt","revision":"child-v2"}
        d["lineage"]=[{"parent":"parent-v1","child":"child-v2","candidate_id":"c1"}]
        self.assertTrue(v.validate(d))
    def test_partial_review_unknown_target(self):
        d=fixture();d.update(decision="review",selected_candidate=None,candidates=[],gates=[],target=None,parent=None,rollback_target=None,objective=None,unknown_fields=["target","parent","rollback_target","objective"])
        self.assertTrue(v.validate(d))
    def test_zero_provider_budget(self):
        d=fixture();d["contract"]["max_calls"]=0
        self.assertTrue(v.validate(d))
    def test_unknown_usage_preserved(self):
        d=fixture();d.update(decision="inconclusive",selected_candidate=None,unknown_fields=["usage.seconds"])
        d["usage"]["seconds"]=None;d["candidates"][0]["outcome"]="inconclusive"
        self.assertTrue(v.validate(d))
    def test_budget_overrun_preserved(self):
        d=fixture();d.update(decision="inconclusive",selected_candidate=None)
        d["usage"]["calls"]=31;d["candidates"][0]["outcome"]="inconclusive"
        self.assertTrue(v.validate(d))
    def test_rejection_requires_evidence(self):
        d=fixture();d.update(decision="reject",selected_candidate=None)
        d["candidates"][0]["outcome"]="reject"
        with self.assertRaises(ValueError):v.validate(d)
        d["gates"][0]["result"]="fail"
        self.assertTrue(v.validate(d))
    def test_failed_gate_cannot_be_inconclusive(self):
        d=fixture();d.update(decision="inconclusive",selected_candidate=None)
        d["candidates"][0]["outcome"]="inconclusive";d["gates"][0]["result"]="fail"
        with self.assertRaises(ValueError):v.validate(d)
    def test_secondary_quality_floor(self):
        d=fixture();d["contract"]["constraints"]=[{"metric":"quality","operator":">=","bound":0.94}]
        d["candidates"][0]["constraint_measurements"]={"quality":{"value":0.8,"evidence":"fixture:quality"}}
        with self.assertRaises(ValueError):v.validate(d)
        d["candidates"][0]["constraint_measurements"]["quality"]["value"]=0.95
        self.assertTrue(v.validate(d))
    def test_consequential_requires_holdout(self):
        d=fixture();d["contract"]["consequential"]=True
        next(g for g in d["gates"] if g["name"]=="holdout")["result"]="not_applicable"
        with self.assertRaises(ValueError):v.validate(d)
    def test_historical_state_retained(self):
        d=fixture()
        for name in ("failure_classes","lessons","historical_versions","metrics"):
            self.assertIn(name,d)
        self.assertIn("successful_edit_families",d["meta_evolution"])
        self.assertTrue(v.validate(d))
    def test_known_constraint_failure_cannot_hide_as_inconclusive(self):
        d=fixture();d.update(decision="inconclusive",selected_candidate=None)
        d["candidates"][0]["outcome"]="inconclusive"
        d["contract"]["constraints"]=[{"metric":"quality","operator":">=","bound":0.94}]
        d["candidates"][0]["constraint_measurements"]={"quality":{"value":0.8,"evidence":"fixture:quality"}}
        with self.assertRaises(ValueError):v.validate(d)
        d["decision"]="reject";d["candidates"][0].update(outcome="reject",rejection_evidence="fixture:quality")
        with self.assertRaises(ValueError):v.validate(d)
        next(g for g in d["gates"] if g["name"]=="regression")["result"]="fail"
        self.assertTrue(v.validate(d))
    def test_declared_unknown_review_limit(self):
        d=fixture();d.update(decision="review",selected_candidate=None,candidates=[],gates=[],unknown_fields=["contract.max_calls"])
        d["contract"]["max_calls"]=None
        self.assertTrue(v.validate(d))
        d["unknown_fields"]=[]
        with self.assertRaises(ValueError):v.validate(d)
    def test_hard_gate_failures(self):
        for name in v.HARD:
            with self.subTest(name=name):
                d=fixture()
                next(g for g in d["gates"] if g["name"]==name)["result"]="fail"
                with self.assertRaises(ValueError):v.validate(d)
    def test_negative_contract_cases(self):
        mutations = {
          "placeholder result":lambda d:d["gates"][0].update(result="pass|fail|not_run"),
          "missing evidence":lambda d:d["gates"][0].update(evidence=""),
          "self-scored no gain":lambda d:d["candidates"][0]["measurement"].update(value=0.5),
          "tail regression":lambda d:d["candidates"][0]["measurement"].update(critical_regressions=1),
          "unknown candidate":lambda d:d["gates"][0].update(candidate_id="evil"),
          "duplicate candidate":lambda d:d["candidates"].append(copy.deepcopy(d["candidates"][0])),
          "duplicate gate":lambda d:d["gates"].append(copy.deepcopy(d["gates"][0])),
          "changed evaluator":lambda d:d["candidates"][0].update(changed_paths=["evaluator.py"]),
          "source conflict":lambda d:d["contract"].update(unresolved_conflicts=["different objectives"]),
          "cycle overrun":lambda d:d.update(cycle=2),
          "boolean budget":lambda d:d["contract"].update(max_calls=True),
          "nan measurement":lambda d:d["candidates"][0]["measurement"].update(value=float("nan")),
          "no independent check":lambda d:next(g for g in d["gates"] if g["name"]=="independence").update(result="not_run"),
          "missing gate":lambda d:d["gates"].pop(),
          "critical gate waived":lambda d:next(g for g in d["gates"] if g["name"]=="integrity").update(result="not_applicable"),
          "meta single case":lambda d:d["candidates"][0].update(kind="meta",prior_cases=["a"]),
          "meta repeated case":lambda d:d["candidates"][0].update(kind="meta",prior_cases=["a","a"]),
          "relaxed threshold":lambda d:d["candidates"][0]["measurement"].update(min_gain=0.01),
          "over budget":lambda d:d["usage"].update(calls=31),
          "wrong parent":lambda d:d["candidates"][0].update(parent="unknown"),
          "claim promotion without receipt":lambda d:d.update(decision="promoted"),
          "receipt without promotion":lambda d:d["publication"].update(receipt="unexpected"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                d=fixture();mutate(d)
                with self.assertRaises(ValueError):v.validate(d)

class HelperTests(unittest.TestCase):
    def test_init_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"report.json"
            cmd=["bash",str(ROOT/"scripts/init-report.sh"),str(path)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            before=path.read_bytes()
            self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertEqual(path.read_bytes(),before)
    def test_error_routing(self):
        script=str(ROOT/"scripts/error-detector.sh")
        self.assertEqual(subprocess.run(["bash",script,"0"],capture_output=True).stdout,b"")
        self.assertIn(b"environment",subprocess.run(["bash",script,"2"],capture_output=True).stdout)
        self.assertNotEqual(subprocess.run(["bash",script,"bad"],capture_output=True).returncode,0)
    def test_extractor_prints_without_writes(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"report.json";path.write_text(json.dumps(fixture()))
            cmd=["bash",str(ROOT/"scripts/extract-skill.sh"),str(path),"example-skill"]
            before={str(p):p.read_bytes() for p in ROOT.rglob("*") if p.is_file()}
            r=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(before,{str(p):p.read_bytes() for p in ROOT.rglob("*") if p.is_file()})
            result=json.loads(r.stdout)
            self.assertTrue(result["template"].startswith("---\nname: example-skill"))
            self.assertFalse(result["writes_performed"])
            self.assertEqual(list(Path(td).iterdir()),[path])
            r=subprocess.run(cmd[:-1]+["../../escape"],capture_output=True)
            self.assertNotEqual(r.returncode,0)

if __name__=="__main__":
    unittest.main(verbosity=2)
