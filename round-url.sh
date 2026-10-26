#!/bin/bash
# round-url.sh N : URL-only run of every config, 3 at a time
PACKS="${PACKS:-$PWD/packs}"   # one folder per pack, cloned at the versions in runs-log.md
N=$1; RUN=./run-url.sh
($RUN url-baseline-$N "" "" "" ; $RUN url-marketingskills-$N "$(ls -d $PACKS/marketingskills/skills/*)" "" "Use the seo-audit skill.") &
($RUN url-claude-seo-$N "$(ls -d $PACKS/claude-seo/skills/*)" "$(ls $PACKS/claude-seo/agents/*.md)" "Use the seo-audit skill." ; $RUN url-hawk-$N "$(ls $PACKS/hawk/*.md)" "" "Use the technical-seo-audit skill, plus any of the other installed skills that apply.") &
($RUN url-open-seo-$N "$(ls -d $PACKS/open-seo/plugins/openseo/skills/*)" "" "Use the seo-audit skill." ; $RUN url-seranking-$N "$(ls -d $PACKS/seo-skills/skills/*)" "" "Use the seo-technical-audit skill.") &
wait
echo "url round $N done"
