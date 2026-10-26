#!/bin/bash
# round.sh N : one run of every config, 3 at a time
PACKS="${PACKS:-$PWD/packs}"   # one folder per pack, cloned at the versions in runs-log.md
N=$1; RUN=./run.sh
($RUN baseline-$N "" "" "" ; $RUN marketingskills-$N "$(ls -d $PACKS/marketingskills/skills/*)" "" "Use the seo-audit skill.") &
($RUN claude-seo-$N "$(ls -d $PACKS/claude-seo/skills/*)" "$(ls $PACKS/claude-seo/agents/*.md)" "Use the seo-audit skill." ; $RUN hawk-$N "$(ls $PACKS/hawk/*.md)" "" "Use the technical-seo-audit skill, plus any of the other installed skills that apply.") &
($RUN open-seo-$N "$(ls -d $PACKS/open-seo/plugins/openseo/skills/*)" "" "Use the seo-audit skill." ; $RUN seranking-$N "$(ls -d $PACKS/seo-skills/skills/*)" "" "Use the seo-technical-audit skill.") &
wait
echo "round $N done"
