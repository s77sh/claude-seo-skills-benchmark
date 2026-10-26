#!/bin/bash
# run.sh NAME "SKILL_DIRS" "AGENT_DIRS" "EXTRA PROMPT"
# Fresh dir per run; evidence copied in; only the given skills installed (project scope).
set -e
LAB="${LAB:-$PWD/work/v2}"
NAME=$1; SKILLS=$2; AGENTS=$3; EXTRA=$4
R=$LAB/runs/$NAME; rm -rf "$R"; mkdir -p "$R/.claude/skills" "$R/.claude/agents"
# URL-only: no evidence folder
for s in $SKILLS; do
  if [ -d "$s" ]; then cp -r "$s" "$R/.claude/skills/"; else n=$(basename "$s" .md); mkdir -p "$R/.claude/skills/$n"; cp "$s" "$R/.claude/skills/$n/SKILL.md"; fi
done
for a in $AGENTS; do cp "$a" "$R/.claude/agents/"; done
PROMPT="Do a full SEO audit of the Kopi Kita website. It is running locally at http://localhost:8766/ (the production domain is kopikita.test), and you can fetch any URL on it with curl. Write the full audit to ./audit.md: every issue you find, the URL it affects, why it matters and how to fix it, in priority order. Don't ask me questions; work with what you can fetch. $EXTRA"
cd "$R"
START=$(date +%s)
claude -p "$PROMPT" --model sonnet --setting-sources project \
  --allowedTools "Read" "Glob" "Grep" "Write" "Edit" "Skill" "Task" "Agent" "Bash(curl:*)" \
  --disallowedTools "WebSearch" "WebFetch" \
  --max-budget-usd 6 --output-format stream-json --verbose > log.jsonl 2> err.txt || true
echo "$NAME $(( $(date +%s) - START ))s" > time.txt
python3 - "$R" <<'PY'
import json, sys
r = sys.argv[1]; skills = []; tools = {}; res = {}
for line in open(r + "/log.jsonl"):
    try: e = json.loads(line)
    except Exception: continue
    if e.get("type") == "assistant":
        for c in e["message"].get("content", []):
            if c.get("type") == "tool_use":
                tools[c["name"]] = tools.get(c["name"], 0) + 1
                if c["name"] == "Skill": skills.append(c["input"].get("skill") or c["input"].get("command"))
    if e.get("type") == "result": res = e
json.dump({"cost_usd": res.get("total_cost_usd"), "turns": res.get("num_turns"), "duration_s": (res.get("duration_ms") or 0) / 1000,
           "skills_loaded": skills, "tools": tools, "denials": len(res.get("permission_denials", [])),
           "subtype": res.get("subtype")}, open(r + "/summary.json", "w"), indent=1)
print(open(r + "/summary.json").read())
PY
