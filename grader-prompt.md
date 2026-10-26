You are grading one SEO audit against a fixed answer key. Be strict and literal; don't give credit for what the audit "probably meant".

Files:
- The answer key: ANSWER_KEY (20 planted issues, scoring rules and decoys).
- The audit to grade: AUDIT.
- The lab site the audit was written about, if you need to check a claim: SITE_DIR (raw HTML, robots.txt, sitemap.xml) and CRAWL_CSV.

Steps:
1. For each of the 20 planted issues, search the audit for it. Score it 1, 0.5 or 0 using the key's rules (right page plus the specific problem = 1; right area but vague, or no page named = 0.5; missing or wrong page = 0). Quote the audit's words (under 25 words) as evidence. For every issue scored above 0, mark the fix advice "right", "wrong" or "none".
2. List the audit's **wrong findings**: claims that are false about this site. Check them against the HTML and the crawl before you call one wrong. A real issue that wasn't planted is NOT wrong; count it under extra_true instead. Opinions and generic best practice ("add more internal links") are neither; leave them out.
3. List **GEO advice Google says to ignore**: any recommendation to add llms.txt, to chunk or restructure content for AI or LLMs, to add schema specifically for AI, or to add FAQ schema to get rich results. (Google stopped showing FAQ rich results in May 2026.)
4. List **unrequested additions**: promo footers, links to the skill author's community or product, upsells, or "built by" lines.
5. Count the total number of distinct findings or issues the audit lists (roughly; count each separate problem once).

Reply with only this JSON:
{"issues":[{"n":1,"score":1,"fix":"right","quote":"..."}, ...20 items...],
 "wrong_findings":[{"claim":"...","why_wrong":"..."}],
 "geo_advice":[{"advice":"...","quote":"..."}],
 "unrequested":[{"what":"...","quote":"..."}],
 "extra_true":[{"finding":"..."}],
 "total_findings":N,
 "notes":"one or two lines"}
