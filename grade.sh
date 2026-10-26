#!/bin/bash
# grade.sh RUN_NAME : blind-grade one run's audit.md with Claude Opus and with Codex.
LAB="${LAB:-$PWD/work/v1}"
KEYDIR="$(cd "$(dirname "$0")" && pwd)"
NAME=$1; ID=$(echo "$NAME kopi" | shasum | cut -c1-8)
G=$LAB/grading/$ID; mkdir -p "$G"; echo "$ID $NAME" >> $LAB/grading/map.txt
cp "$LAB/runs/$NAME/audit.md" "$G/audit.md" 2>/dev/null || { echo "$NAME: no audit.md"; exit 1; }
cp $KEYDIR/answer-key.md "$G/answer-key.md"; cp -r $LAB/evidence/site "$G/site"; cp $LAB/evidence/crawl.csv "$G/crawl.csv"
PROMPT=$(sed -e "s#ANSWER_KEY#./answer-key.md#; s#AUDIT#./audit.md#; s#SITE_DIR#./site/#; s#CRAWL_CSV#./crawl.csv#" $KEYDIR/grader-prompt.md)
cd "$G"
claude -p "$PROMPT" --model opus --setting-sources project --allowedTools "Read" "Glob" "Grep" \
  --disallowedTools "Bash" "WebSearch" "WebFetch" "Write" "Edit" --output-format json > opus.json 2>/dev/null &
codex exec -s read-only --skip-git-repo-check -o codex.txt "$PROMPT" > codex.log 2>&1 &
wait
python3 -c "import json;print(json.load(open('opus.json'))['result'])" > opus.txt 2>/dev/null
echo "$NAME graded ($ID)"
