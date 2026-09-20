#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 1 || ! "$1" =~ ^[0-9]+$ ]]; then echo "Usage: error-detector.sh NUMERIC_EXIT_STATUS" >&2; exit 2; fi
if [[ "$1" =~ [1-9] ]]; then
  printf '%s\n' 'Classify the failed command: candidate defect, environment failure, expected negative test, or evaluator failure. Record redacted evidence and keep eligibility unresolved until valid checks complete.'
fi
