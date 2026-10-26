# Lab runs log

- 2026-10-22: answer-key.md sha256 25b63162cb2f84eaa8e97e437d98ee96bc93dc936f8294afb84801c2b402b82c, logged before run 1.
- Model: claude-sonnet-5-5 (`--model sonnet`), Claude Code headless (`claude -p`), `--setting-sources project` (no user skills or CLAUDE.md), a fresh folder per run.
- Tools for every run: Read, Glob, Grep, Write, Edit, Skill, Task/Agent, `Bash(curl:*)`. No WebSearch or WebFetch. Pack scripts (Python etc.) can't run, so the test covers the skill instructions, not the scripts. The same rule applies to every pack.
- Pack versions: marketingskills e85f3cb, open-seo c5f8db1, claude-seo 23a2a81 (v2.4.2), seranking/seo-skills fd6d140, Hawk Academy .md files downloaded 2026-10-22 (7 skills: technical-seo-audit, cannibalization-detector, striking-distance-finder, schema-markup-auditor, internal-linking, title-tag-optimizer, screaming-frog-analyser).
- Installed as project skills (`.claude/skills/`), plus claude-seo's agents in `.claude/agents/`. The claude-seo plugin hook isn't installed.
- The same prompt for every run (see run.sh), plus one line naming the pack's audit skill.
- 2026-10-22: answer-key-v2.md sha256 08e9440f6c05a56cc59fabc71e1ba88f5cfab6c566b341d272f6499454ef9c1d, logged before the v2 build.
- 2026-10-22: lab v2 round 1 done (6 runs). Round 2 failed: usage limit (429). Stopped at the user's request to save credit.
