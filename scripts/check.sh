#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

python3 -m compileall -q contracts tests
python3 -m unittest discover -s tests -v

if command -v genvm-lint >/dev/null 2>&1; then
  lint_cmd="genvm-lint"
elif [[ -x .venv/bin/genvm-lint ]]; then
  lint_cmd=".venv/bin/genvm-lint"
elif [[ -x ../invariant-lens/.venv/bin/genvm-lint ]]; then
  lint_cmd="../invariant-lens/.venv/bin/genvm-lint"
else
  echo "genvm-lint is required; install requirements-dev.txt" >&2
  exit 1
fi

"$lint_cmd" check contracts/precedent_protocol.py
"$lint_cmd" schema contracts/precedent_protocol.py --output /tmp/precedent-protocol.schema.json >/dev/null
diff -u contracts/contract-metadata/precedent_protocol.schema.json /tmp/precedent-protocol.schema.json
