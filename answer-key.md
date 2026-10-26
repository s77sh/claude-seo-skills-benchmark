# Lab answer key (written before any run)

Written 2026-10-22, before the lab site was built and before any pack ran. Its sha256 is logged in `runs-log.md` before run 1.

Lab: a made-up Bali coffee roaster, "Kopi Kita" (kopikita.test), served locally at http://localhost:8765/. Every run gets the same evidence: the raw HTML of every page, robots.txt, sitemap.xml, a crawl export (`crawl.csv`, Screaming Frog-style columns, our own crawler) and a 3-month Search Console export (`gsc.csv`, made up for the lab).

Visibility: **P** = visible in the page's own HTML. **S** = site-level: needs the crawl, robots.txt, the sitemap or GSC.

## Scoring rules

- **Found (1 point):** the finding names the right page (or the site file) and states the specific problem the rule below asks for.
- **Half (0.5):** right page and right area, but vague ("review your titles", "check canonicals") or lumped into a generic list with no page named.
- **Missed (0):** not mentioned, or named on the wrong page only.
- If the same issue is reported twice, it counts once.
- **Fix advice** is marked right or wrong for every found issue (shown separately; it doesn't change the recall score).
- **Wrong findings:** any claim that's false about the lab (a problem that isn't there, or a wrong fact). Advice that goes against Google's AI guide (llms.txt, chunking, special AI schema) is logged separately as "GEO advice Google says to ignore".
- **Extra true findings:** real issues that weren't planted are logged and counted as true, never as wrong.

## The 20 planted issues

| # | Issue | Page | Vis | Counts as found if the finding says... |
|---|---|---|---|---|
| 1 | Missing canonical | /contact/ | P | /contact/ has no canonical tag |
| 2 | Wrong canonical | /shop/ canonicals to /coffee/ | P | /shop/'s canonical points to a different page (/coffee/) |
| 3 | noindex left on | /wholesale/ | P | /wholesale/ has noindex (and it's a page that should rank: in the nav and the sitemap) |
| 4 | Duplicate title | /subscriptions/ and /coffee/ | S | the two pages share the same title |
| 5 | Title too long | /coffee/bali-kintamani/ (title is over 70 characters) | P | the title is too long or will be cut off in results |
| 6 | Missing meta description | /about/ | P | /about/ has no meta description |
| 7 | Broken internal link | /blog/how-to-brew-pour-over/ links to /coffee/aceh-gayo/ (404) | S | a link to /coffee/aceh-gayo/ returns 404 (or a broken link from that post) |
| 8 | Orphan page | /coffee/flores-bajawa/ (in the sitemap, no internal links) | S | the page has no internal links pointing to it / is orphaned |
| 9 | Redirect chain | /menu/ 301 to /cafe/ 301 to /visit/; the nav links to /menu/ | S | /menu/ goes through two redirects / a chain (a single "redirect" mention = half) |
| 10 | robots.txt blocks CSS | `Disallow: /assets/css/` | S | robots.txt blocks CSS (rendering resources) |
| 11 | Sitemap lists a 404 | /coffee/sumatra-mandheling/ | S | the sitemap has a URL that returns 404 |
| 12 | Missing H1 | /visit/ | P | /visit/ has no H1 |
| 13 | Two H1s | /coffee/brewing-guide/ | P | the page has more than one H1 |
| 14 | Image without alt | home page hero product image | P | an image on the home page has no alt text |
| 15 | Oversized hero image | /about/ hero (about 2MB JPG) | S | the image is too heavy / about 2MB, slows the page |
| 16 | Thin page | /blog/cold-brew-at-home/ (about 80 words, how-to query) | P | the page is thin or too short for its topic |
| 17 | Invalid JSON-LD | Product on /coffee/bali-kintamani/ has no `name` | P | the Product schema is missing `name` / is invalid |
| 18 | FAQ schema on a non-FAQ page | FAQPage JSON-LD on /coffee/ with no visible questions | P | FAQ markup with no matching visible FAQ content (saying "FAQ rich results are gone" also counts) |
| 19 | Cannibalization | /blog/how-to-brew-pour-over/ and /blog/pour-over-coffee-guide/ for "pour over coffee" | S | the two posts compete for the same query |
| 20 | Stale year | /blog/best-coffee-beans-2024/ title says 2024 (dateModified is 2026) | P | the title or URL shows an outdated year |

P (12 issues): 1, 2, 3, 5, 6, 12, 13, 14, 16, 17, 18, 20. S (8 issues): 4, 7, 8, 9, 10, 11, 15, 19.

## Deliberately fine (decoys, to catch false findings)

- /blog/ index: good title, meta description, canonical, one H1.
- /coffee/java-ijen/: a complete, healthy product page with valid Product schema (name, offers, image).
- Every other image has alt text and is under 200KB.
- The home page has valid Organization JSON-LD.
- There is no llms.txt. Google says Search doesn't use it, so not having one isn't an issue.
