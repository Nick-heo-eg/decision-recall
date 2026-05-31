#!/usr/bin/env bash
# Register the decision-recall Stop hook in Claude Code's settings.json.
#
# What this does:
#   - Adds a Stop hook entry that runs hooks/auto_capture.py after every
#     Claude response
#   - Captures markers (결정/판단/원칙 or decision/analysis/principle)
#     into ~/decision-recall/state/recall_trace.jsonl automatically
#
# Run from anywhere — script resolves paths via $(dirname).
# Idempotent: re-running won't add duplicate entries.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_PATH="${SCRIPT_DIR}/auto_capture.py"
SETTINGS="${HOME}/.claude/settings.json"

if [[ ! -f "$HOOK_PATH" ]]; then
  echo "ERROR: auto_capture.py not found at $HOOK_PATH"
  exit 1
fi

mkdir -p "${HOME}/.claude"

if [[ ! -f "$SETTINGS" ]]; then
  echo "{}" > "$SETTINGS"
fi

python3 - "$SETTINGS" "$HOOK_PATH" <<'PY'
import json
import sys
from pathlib import Path

settings_path = Path(sys.argv[1])
hook_path = sys.argv[2]

s = json.loads(settings_path.read_text())
s.setdefault("hooks", {}).setdefault("Stop", [])

new_entry = {
    "type": "command",
    "command": f"python3 {hook_path}",
    "timeout": 5,
}

# Check if already registered (idempotent)
for group in s["hooks"]["Stop"]:
    for h in group.get("hooks", []):
        if h.get("command") == new_entry["command"]:
            print(f"Hook already registered at {hook_path}. Nothing to do.")
            sys.exit(0)

# Append as its own group (matcher-less = always runs on Stop)
s["hooks"]["Stop"].append({"hooks": [new_entry]})
settings_path.write_text(json.dumps(s, indent=2, ensure_ascii=False))
print(f"Registered Stop hook → {hook_path}")
PY

echo ""
echo "Done. Restart Claude Code so the hook takes effect."
echo ""
echo "To verify: trigger Claude to write a marker like:"
echo "  decision: test | This is a self-test of decision-recall hook"
echo "Then check:"
echo "  tail -1 ${HOME}/decision-recall/state/recall_trace.jsonl"
