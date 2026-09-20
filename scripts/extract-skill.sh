#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 2 ]]; then echo "Usage: extract-skill.sh REPORT NAME (prints request only)" >&2; exit 2; fi
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -B - "$root" "$1" "$2" <<'PY'
import importlib.util, json, pathlib, re, sys
root, report, name = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name):
    raise SystemExit("Invalid skill name")
spec = importlib.util.spec_from_file_location("validator", root/"scripts/validate-report.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
try:
    data = json.loads(report.read_text(encoding="utf-8"))
    module.validate(data)
    if data["decision"] not in ("eligible", "promoted"):
        raise ValueError("Extraction requires an eligible candidate")
except (ValueError, KeyError, TypeError, OSError) as exc:
    raise SystemExit(str(exc))
template = (root/"assets/SKILL-TEMPLATE.md").read_text(encoding="utf-8").replace("replacement-name",name)
print(json.dumps({"name":name,"source_report":str(report.resolve()),"candidate_id":data["selected_candidate"],"template":template,"complete":False,"action":"complete_from_verified_evidence_then_use_host_publication","writes_performed":False},indent=2))
PY
