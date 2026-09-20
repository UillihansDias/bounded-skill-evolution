#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 1 ]]; then echo "Usage: init-report.sh OUTPUT" >&2; exit 2; fi
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - "$root/assets/template.json" "$1" <<'PY'
import pathlib, sys
source, target = map(pathlib.Path, sys.argv[1:])
try:
    with target.open("x", encoding="utf-8") as out:
        out.write(source.read_text(encoding="utf-8"))
except OSError as exc:
    raise SystemExit("Cannot initialise report: " + str(exc))
print("Created incomplete report:", target)
PY
