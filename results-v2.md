# Lab v2 results (2026-10-22): partial

Lab v2 has 20 harder issues (`answer-key-v2.md`). Every run got the URL and curl only. Model: claude-sonnet-5-5. **One run per config.** Round 2 never ran because the account hit its usage limit. Some grades are Codex only: the Opus grader hit the same limit.

| Config | Recall /20 (Codex; Opus) | Missed | Cost | Time |
|---|---|---|---|---|
| marketingskills (seo-audit) | 20; not graded | none | $0.54 | 2.1 min |
| SE Ranking (seo-technical-audit, no MCP) | 20; not graded | none | $0.50 | 2.1 min |
| plain Claude, no skill | 18; 18 | #1 X-Robots-Tag noindex header, #11 missing viewport | $0.40 | 2.1 min |
| claude-seo (seo-audit) | 18; 18 | #1, #11 | $0.45 | 1.7 min |
| open-seo (seo-audit, no MCP) | 16; 16 | #1, #6 JS-only content, #8 schema price mismatch, #11 | $0.57 | 2.4 min |
| Hawk (technical-seo-audit) | not graded | | $0.35 | 1.6 min |

**What it shows (one run each, so treat it as a lead, not a verdict)**
- The two checklist-style skills (marketingskills, SE Ranking) caught the two issues plain Claude missed: a noindex sent only in the HTTP header, and a missing viewport tag. That's the first place a skill added something over no skill.
- claude-seo matched plain Claude exactly.
- open-seo stays a "top 3 moves" prioritiser and misses more.
- Before publishing: run round 2 (6 runs, about $3), grade Hawk, and get Opus grades for marketingskills and SE Ranking.

## Hawk Academy (added 2026-10-22)

v2-hawk-1: 18/20 from both graders (Opus and Codex), $0.35, 1.6 min. Missed #1 (X-Robots-Tag noindex on /subscriptions/) and #18 (onclick-only link to /coffee/limited-release/). Codex logged 2 wrong findings (says every checked page has a meta description and a canonical; /gifts/ has neither). The audit was written to a mistyped path and recovered from the run log. No second runs: one run per pack is final.
