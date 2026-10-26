#!/bin/bash
# round-url.sh N : URL-only run of every config, 3 at a time
PACKS="${PACKS:-$PWD/packs}"   # one folder per pack, cloned at the versions in runs-log.md
N=$1; RUN=./run-v2.sh
($RUN v2-baseline-$N "" "" "" ; $RUN v2-marketingskills-$N "$(ls -d $PACKS/marketingskills/skills/*)" "" "Use the seo-audit skill.") &
($RUN v2-claude-seo-$N "$(ls -d $PACKS/claude-seo/skills/*)" "$(ls $PACKS/claude-seo/agents/*.md)" "Use the seo-audit skill." ; $RUN v2-hawk-$N "$(ls $PACKS/hawk/*.md)" "" "Use the technical-seo-audit skill, plus any of the other installed skills that apply.") &
($RUN v2-open-seo-$N "$(ls -d $PACKS/open-seo/plugins/openseo/skills/*)" "" "Use the seo-audit skill." ; $RUN v2-seranking-$N "$(ls -d $PACKS/seo-skills/skills/*)" "" "Use the seo-technical-audit skill.") &
wait
echo "v2 round $N done"
