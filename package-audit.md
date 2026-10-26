# Package audit (first pass, 2026-10-22)

What each pack contains, checked before installing. First pass only: counts and greps. Read the flagged files by hand before publishing.

| Pack | Version | Files | Scripts | `` !`cmd` `` shell injection in .md | Installer | Needs an account / MCP | Notes |
|---|---|---|---|---|---|---|---|
| marketingskills (skills/) | e85f3cb | 410 | 28 (helpers for tools like Cal.com, Calendly, Typeform) | 0 | `npx skills add` | No, for seo-audit | One integration doc suggests `curl -fsSL https://ploy.ai/install.sh \| sh` (tools/integrations/ploy.md; that's a third party, not the pack itself) |
| claude-seo | 23a2a81 (v2.4.2) | 470 | 170 (Python: render, PageSpeed, GSC, GA4, DataForSEO, Moz, IndexNow submit...) | 0 | install.sh: git clone to a temp dir, copies into ~/.claude/skills and ~/.claude/agents, rewrites script paths; its own uninstall line is `curl ... \| bash` | Optional Google / DataForSEO / Moz keys | A plugin hook (PostToolUse on Edit/Write) runs node + `validate-schema.py` on every file Claude writes. The promo footer instruction is in skills/seo/SKILL.md (lines 152 to 191 on main) |
| open-seo (plugins/openseo) | c5f8db1 | 18 | 0 | 0 | plugin / `npx skills add` | **Yes**: the OpenSEO MCP (self-hosted app or openseo.so). seo-audit says to stop if it's not connected | Prompt-only on top of its MCP |
| SE Ranking seo-skills | fd6d140 | 287 | 21 (Google API helpers) | 0 | install.sh, designed for `curl \| bash`: git clone to ~/.local/share/seo-skills, optional Firecrawl MCP, optional pip installs | **Yes**: the SE Ranking MCP (`claude mcp add --transport http se-ranking https://api.seranking.com/mcp`, OAuth) | The skills call `DATA_*` MCP tools |
| Hawk Academy (7 of 56 .md) | downloaded 2026-10-22 | 7 | 0 | 0 | a curl one-liner per skill into ~/.claude/skills (downloads one .md, nothing runs) | No | Pure prompts. Needs a Hawk Academy page visit per skill |
