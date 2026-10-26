# Lab v1 results (2026-10-22)

19 audit runs, every one on claude-sonnet-5-5, each graded blind by two graders: Claude Opus and Codex. Scoring rules: `answer-key.md`. Raw audits: `results-v1/audits/`. Grades: `results-v1/grades/`.

**Conditions**
- **full:** the URL plus a crawl export, the raw HTML and a Search Console CSV.
- **url:** the URL and curl only.

**Headline: plain Claude Code with no skill caught 19 to 20 of the 20 planted issues.** So did every pack except open-seo (17 and 20 in its two URL-only runs; Opus grades). Lab v1 is too easy to separate them, so we built lab v2, with harder issues (`answer-key-v2.md`).

**What did differ**
- **Cost:** $0.26 to $0.49 per audit. Time: 1.3 to 2.5 minutes. No pack cost much more than plain Claude.
- **open-seo** is built to "recommend selectively" (1 to 3 big moves), not to work through a checklist. In one URL-only run it skipped the missing H1 and the thin post, and it wrongly said every page has an H1.
- **claude-seo** was the only pack whose audits got flagged for AI-search advice: "question-style H2s for AI answers" (Opus flagged 4 items across its 4 runs). It was mild, not llms.txt.
- **The promo footer:** the claude-seo `/seo` router skill loaded the Community Footer instruction (it's in the run log), but Sonnet 5.5 didn't print it in our one `/seo audit` run, in either the file or the chat reply. The `seo-audit` sub-skill doesn't contain the instruction at all. One headless run isn't proof that it never prints.
- **No pack recommended llms.txt.** Most flagged the FAQ markup correctly, noting that FAQ rich results are gone.
- **The SE Ranking and open-seo skills** are written for their paid MCP tools, but both still produced full audits from the raw site without them. The open-seo seo-audit text says to stop if OpenSEO isn't connected; it didn't stop.
- **"Wrong claims"** are noisy between the graders (for example 4 vs 0 for the same audit). Check them by hand before quoting any single number.

| Pack | Condition | Runs | Recall /20 (Opus; Codex) | Wrong claims (Opus; Codex) | GEO advice flagged | Promo added | Avg cost | Avg time |
|---|---|---|---|---|---|---|---|---|
| baseline | full | 1 | 20; 20 | 2; 1 | 0; 0 | 0 | $0.48 | 2.5 min |
| baseline | url | 2 | 20 / 19; 20 / 19 | 2 / 3; 2 / 2 | 0 / 0; 0 / 0 | 0 | $0.30 | 1.4 min |
| claude-seo | full | 1 | 20; 20 | 1; 2 | 1; 3 | 0 | $0.47 | 2.2 min |
| claude-seo | url | 2 | 20 / 20; 18.5 / 20 | 1 / 0; 2 / 0 | 2 / 0; 2 / 0 | 0 | $0.40 | 1.6 min |
| claude-seo-router | url | 1 | 19; 19 | 2; 3 | 1; 1 | 0 | $0.38 | 1.5 min |
| hawk | full | 1 | 20; 20 | 1; 5 | 0; 0 | 0 | $0.33 | 1.9 min |
| hawk | url | 2 | 20 / 20; 20 / 20 | 2 / 3; 0 / 0 | 0 / 0; 0 / 0 | 0 | $0.33 | 1.5 min |
| marketingskills | full | 1 | 20; 20 | 4; 0 | 0; 0 | 0 | $0.43 | 2.3 min |
| marketingskills | url | 2 | 20 / 20; 20 / 20 | 2 / 7; 1 / 3 | 0 / 0; 1 / 0 | 0 | $0.39 | 1.6 min |
| open-seo | full | 1 | 20; 20 | 3; 4 | 0; 0 | 0 | $0.35 | 1.8 min |
| open-seo | url | 2 | 17.0 / 20; 16.5 / 19 | 6 / 2; 4 / 4 | 0 / 0; 0 / 0 | 0 | $0.32 | 1.5 min |
| seranking | full | 1 | 20; 20 | 3; 0 | 0; 0 | 0 | $0.49 | 2.1 min |
| seranking | url | 2 | 20 / 20; 20 / 20 | 1 / 4; 1 / 3 | 0 / 0; 0 / 0 | 0 | $0.43 | 1.6 min |