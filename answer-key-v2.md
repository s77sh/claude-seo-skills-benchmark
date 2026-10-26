# Lab v2 answer key (written before the v2 build and before any v2 run)

Written 2026-10-22. Why there's a v2: in lab v1, plain Claude Code (no skill) caught 19 to 20 of the 20 issues, and so did nearly every pack. The issues were too easy for Sonnet 5.5 to separate the packs. v2 keeps the same Kopi Kita site, fixes all 20 v1 issues, and plants 20 harder ones: issues that only show up in HTTP headers, that need reasoning across several pages, or that the usual checklists skip.

The test: **URL only.** Every run gets http://localhost:8766/ and curl, with no crawl export and no Search Console data. The production domain is https://kopikita.test.

The scoring rules are the same as v1 (`answer-key.md`): 1 = right page plus the specific problem, 0.5 = right area but vague or no page named, 0 = missed or wrong page. Duplicates count once. Wrong findings, GEO advice Google says to ignore, and unrequested additions are logged separately.

## The 20 planted issues

| # | Issue | Where | Counts as found if the finding says... |
|---|---|---|---|
| 1 | noindex sent only as an HTTP header | /subscriptions/ responds with `X-Robots-Tag: noindex` (its HTML has no robots meta) | /subscriptions/ is noindexed via the X-Robots-Tag header |
| 2 | Canonical points to a redirecting URL | /coffee/java-ijen/ canonical = /coffee/ijen/, which 301s back to /coffee/java-ijen/ | the canonical target redirects (canonical should be the final URL) |
| 3 | Soft 404 | /gifts/ returns 200 with a "Page not found" body; linked in the nav | /gifts/ is a soft 404 / a not-found page served with 200 |
| 4 | 302 used for a permanent move | /coffee/kintamani/ 302 to /coffee/bali-kintamani/ | the redirect is a 302 (temporary) and should be a 301 |
| 5 | hreflang errors | /id/ uses `hreflang="in"` (not a valid code; Indonesian is `id`), and the English home page has no return hreflang link | either: invalid hreflang code "in", or missing return (reciprocal) hreflang tags |
| 6 | Main content needs JavaScript | /coffee/gift-box/: the description is injected by a script; the raw HTML has an empty container | the content isn't in the raw HTML / depends on JS rendering |
| 7 | nofollow on internal links | nav links to /wholesale/ have `rel="nofollow"` | internal links to /wholesale/ are nofollow |
| 8 | Schema price doesn't match the page | /coffee/bali-kintamani/: Product offers price 145000; the page shows Rp 165,000 | the structured-data price differs from the visible price |
| 9 | JSON-LD syntax error | /blog/how-to-brew-pour-over/ Article JSON-LD has a trailing comma (invalid JSON) | the JSON-LD on that post is invalid / won't parse |
| 10 | Lazy-loaded LCP image | the home page hero image has `loading="lazy"` | the above-the-fold hero is lazy-loaded (hurts LCP) |
| 11 | Missing viewport meta | /visit/ has no `<meta name="viewport">` | /visit/ has no viewport tag / isn't mobile-friendly |
| 12 | Paginated page canonical to page 1 | /blog/page/2/ canonical = /blog/ | page 2 canonicalises to page 1 (should self-canonicalise) |
| 13 | Sitemap lists a URL that robots.txt blocks | /coffee/samples/ is in the sitemap and under `Disallow: /coffee/samples/` | the sitemap includes a robots-blocked URL |
| 14 | Sitemap lastmod in the future | every `<lastmod>` is 2027-03-01 | lastmod dates are in the future / not trustworthy |
| 15 | Near-duplicate page | /coffee/bali-kintamani-1kg/ repeats /coffee/bali-kintamani/'s copy, with a self canonical | the 1kg page duplicates the 250g page (canonicalise, merge or differentiate) |
| 16 | Copy-pasted meta description | /coffee/flores-bajawa/'s meta description describes Java Ijen | the Flores meta description is about the wrong coffee / doesn't match the page |
| 17 | Images with no src | /about/ gallery images use `data-src` only, with no `src` | the gallery images have no src / lazy-load script dependency, so they can't be indexed |
| 18 | Link that can't be crawled | /coffee/limited-release/ is reachable only through a `<button onclick=...>` on /coffee/ (not in the sitemap) | the link to limited-release isn't a real `<a href>` / can't be crawled |
| 19 | Internal links to a redirect | the home page and two posts link to /coffee/kintamani/ (redirects) instead of /coffee/bali-kintamani/ | internal links point at a redirecting URL |
| 20 | Mixed content | /contact/ loads an image and an iframe over `http://` on an https site | insecure http:// resources / mixed content on /contact/ |

## Decoys (fine on purpose)
- All the v1 fixes are in: unique titles, meta descriptions, canonicals, one H1 each, alt text, small images, a valid sitemap otherwise, a clean robots.txt otherwise.
- /coffee/samples/ being blocked is fine on its own; only its sitemap listing is the issue.
- /blog/tag/ is blocked in robots.txt and isn't in the sitemap. That's fine.
- No llms.txt. That's fine.
