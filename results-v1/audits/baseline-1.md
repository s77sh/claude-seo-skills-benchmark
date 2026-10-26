# SEO Audit: Kopi Kita (kopikita.test)

Evidence: raw HTML of all 18 pages, `robots.txt` and `sitemap.xml` (`evidence/site/`), the crawl export (`crawl.csv`, 27 URLs) and the Search Console export (`gsc.csv`, 22 Jul to 21 Oct 2026). I spot-checked redirect and status behaviour against the local server (`/shop/` returns 200; `/menu/` returns 301 to `/cafe/`; `/cafe/` returns 301 to `/visit/`; the Sumatra URL returns 404).

Not verifiable from this evidence: HTTPS and www redirects, Core Web Vitals field data, backlinks, and what the pages look like rendered. Those are listed under "Not covered" at the end.

## What the data says in one paragraph

The GSC export has 27 query/page rows, **832 clicks and about 25,900 impressions**. About 574 clicks (69%) come from branded "kopi kita" queries, so the site is nearly invisible for non-brand search. The non-brand demand is real, though. Pour over queries alone show about 8,800 impressions for 36 clicks, and they are split across two competing articles. "coffee shop ubud" gets 2,240 impressions at position 13.5. "bali coffee beans" gets 1,890 impressions at position 11.4. Most of the work below is fixing structural problems (cannibalisation, a broken nav link, indexing signals that conflict with each other) and then going after those non-brand queries.

The GSC export is only 27 rows, so it is a sample or a top-N cut. Treat the totals as indicative.

## Priority summary

| # | Priority | Issue | URL(s) |
|---|---|---|---|
| 1 | Critical | Two near-identical pour over articles compete against each other | `/blog/how-to-brew-pour-over/`, `/blog/pour-over-coffee-guide/` |
| 2 | Critical | Sitewide nav links to a redirect chain (`/menu/` → `/cafe/` → `/visit/`) | every page, 17 inlinks |
| 3 | Critical | `/wholesale/` is `noindex` but linked sitewide and listed in the sitemap | `/wholesale/` |
| 4 | Critical | `/shop/` canonicalises to `/coffee/` although its content is different | `/shop/` |
| 5 | High | robots.txt blocks the CSS | `/robots.txt` |
| 6 | High | Broken URLs: a 404 in the sitemap and a 404 linked from an article | `/coffee/sumatra-mandheling/`, `/coffee/aceh-gayo/` |
| 7 | High | Orphan product page: `/coffee/flores-bajawa/` has 0 internal links | `/coffee/flores-bajawa/` |
| 8 | High | `/visit/` has no H1, thin content and no local schema, and it is the best local-search page | `/visit/` |
| 9 | High | Stale "2024" article that is still ranking | `/blog/best-coffee-beans-2024/` |
| 10 | High | Duplicate title on `/subscriptions/` and `/coffee/` | `/subscriptions/` |
| 11 | Medium | Cold brew article is thin and ranks at position 38 to 45 | `/blog/cold-brew-at-home/` |
| 12 | Medium | Structured data errors (FAQPage, Product, Article) | `/coffee/`, product pages, articles |
| 13 | Medium | 1.8 MB hero image | `/about/` |
| 14 | Medium | Missing meta description, missing alt text and a missing canonical | `/about/`, `/`, `/contact/` |
| 15 | Medium | Two H1s on the brewing guide | `/coffee/brewing-guide/` |
| 16 | Medium | Over-long title on Kintamani | `/coffee/bali-kintamani/` |
| 17 | Medium | Ranking opportunities not yet targeted | several |
| 18 | Low | No Open Graph tags, favicon or breadcrumbs | sitewide |
| 19 | Low | Smaller points | various |

---

## Critical

### 1. Two pour over articles cannibalise each other
**URLs:** `/blog/how-to-brew-pour-over/` (440 words) and `/blog/pour-over-coffee-guide/` (367 words)

**Evidence (gsc.csv):** both pages rank for the same four queries, and each takes a share of impressions on every one:

| Query | how-to-brew-pour-over | pour-over-coffee-guide |
|---|---|---|
| pour over coffee | pos 16.2, 2,410 impr | pos 18.7, 1,980 impr |
| how to make pour over coffee | 14.1, 1,350 | 17.3, 1,120 |
| pour over coffee guide | 19.4, 610 | 13.9, 820 |

Together the cluster has about 8,830 impressions and 36 clicks (CTR about 0.4%), with every position between 14 and 21. Google is swapping the two pages in and out and can't pick one. The "guide" page is even a better match for "pour over coffee guide" at 13.9, yet the other page also appears for it. The blog index links both with near-identical anchor text, and each article carries the same recipe (15g, 250g, 93°C, 30 s bloom, about 3 min).

**Why it matters:** links, clicks and relevance signals are split between two pages, so neither reaches page 1. Consolidating is the highest-leverage content fix on the site.

**Fix:**
1. Keep `/blog/how-to-brew-pour-over/`. It is older (published 2025-03-10), has more words and gets more clicks.
2. Merge in the unique parts of the guide page: the "which dripper (V60 vs Kalita)", paper filter, kettle, freshness and tasting sections, and the ratio "next steps".
3. Put the beginner angle in the H1 and title, for example "How to Make Pour Over Coffee: A Beginner's Guide". Add a short ratio table to target "pour over ratio" (pos 21.0, 540 impressions).
4. 301 redirect `/blog/pour-over-coffee-guide/` to the kept page. Remove it from the sitemap and from the blog index.
5. Add internal links to the kept page from the brewing guide, `/coffee/java-ijen/` and the homepage "New to specialty coffee?" paragraph. Today it has 2 inlinks.
6. Update `dateModified` in the Article schema and show a visible "Updated" date.

### 2. Sitewide navigation points at a redirect chain
**URL:** the header nav on every page links `Visit the cafe` to `/menu/`. `/menu/` returns 301 to `/cafe/`, which returns 301 to `/visit/`. The crawl shows 17 inlinks to `/menu/`.

**Why it matters:** this is a two-hop chain on the most-linked internal link on the site. It wastes crawl budget and delays users. Internal-link signals reach `/visit/` only after two hops. The result is that `/visit/` shows only 2 real inlinks in the crawl, even though it is the main local-intent page and the second-best page in GSC for branded queries. Redirect chains of 2 or more hops are also an audit flag in their own right.

**Fix:**
- Change the nav link in the shared header template to `/visit/` (so all 18 pages are fixed with one edit).
- Point the `/menu/` 301 straight to `/visit/` (one hop), and keep it, because old links may exist externally.
- Add `/visit/` links from the footer, the homepage ("pick up at the roastery cafe") and `/contact/`.

### 3. `/wholesale/` is noindexed but promoted everywhere
**URL:** `/wholesale/` has `<meta name="robots" content="noindex, follow">`, a self-canonical, a sitemap entry and 16 inlinks (nav). It has no GSC data, which is consistent with it not being indexed.

**Why it matters:** the page is a real commercial page ("more than 30 cafes, villas and hotels", free barista training, next-day delivery) with a title and description written to rank for B2B queries. Contradictory signals (noindex plus sitemap plus self-canonical) also show that this was probably not a deliberate choice. If it was left over from staging or a template, the business is losing wholesale leads from search.

**Fix:** if the page is meant to be public (it appears to be), remove the `noindex` tag and request indexing. Keep it in the sitemap and aim for queries such as "wholesale coffee bali" and "coffee supplier for cafes bali". If it is deliberately private, remove it from the sitemap and from the main navigation instead. Either way, make the signals agree. Also check whether the same `noindex` is sent as an `X-Robots-Tag` header. I only had the HTML.

### 4. `/shop/` canonicalises to a different page
**URL:** `/shop/` has `rel=canonical` pointing at `https://kopikita.test/coffee/`. The crawl marks it "Non-Indexable: Canonicalised". It is in the sitemap and has 16 inlinks.

**Why it matters:** canonical is meant for duplicates. `/shop/` is not a duplicate. It covers gear (V60s, filters, grinder, scale), drip bags and the free-shipping threshold, none of which appears on `/coffee/`. Google will drop `/shop/` from the index and consolidate it into `/coffee/`, so queries for brewing gear and drip bags have no page to land on. The sitemap also lists a URL that Google is told to ignore.

**Fix:** if `/shop/` is a real page, give it a self-referencing canonical and keep it in the sitemap. Link it to each product page, including Flores Bajawa (issue 7), and add drip bag and gear pages over time. If it is meant to be only a duplicate of `/coffee/`, 301 it to `/coffee/` and remove it from the nav and sitemap. The first option fits the content better.

---

## High

### 5. robots.txt blocks the site's CSS
**URL:** `/robots.txt` contains `Disallow: /assets/css/`. The crawl shows `site.css` as "Blocked by robots.txt" with 17 inlinks.

**Why it matters:** Google needs CSS to render pages and judge mobile-friendliness and layout. Blocking it can hurt how pages are evaluated, and it is flagged in Search Console and Lighthouse. It saves nothing, because CSS is not something you need to hide.

**Fix:** delete the `Disallow: /assets/css/` line. `Disallow: /cart/` points at a path that does not exist in the crawl. Keep it only if a cart is planned. Keep the `Sitemap:` line.

### 6. Broken URLs (404)
| URL | Problem | Fix |
|---|---|---|
| `/coffee/sumatra-mandheling/` | Returns 404 but is listed in `sitemap.xml` (the crawl shows 0 inlinks, "In Sitemap: Yes") | Remove it from the sitemap. If the coffee is going to launch, publish the page first. |
| `/coffee/aceh-gayo/` | Returns 404. It is linked from `/blog/how-to-brew-pour-over/` ("If you like it heavier, try our Aceh Gayo") | Replace the link with `/coffee/bali-kintamani/` (heavy body, low acidity, per its own page), or restore the Aceh Gayo page. |

**Why it matters:** a 404 in the sitemap tells Google the sitemap is untrustworthy, and a dead link in your best-performing article is a bad experience and passes no value. Also, the pour over article tells readers to buy a product you do not sell.

**Prevent it:** generate the sitemap from the live published pages, not from a hand-kept list. After any change, the sitemap should only contain 200, indexable, self-canonical URLs. At the moment 3 of the 18 entries break that rule (Sumatra, `/shop/`, `/wholesale/`).

### 7. `/coffee/flores-bajawa/` is an orphan
**URL:** `/coffee/flores-bajawa/` has 0 inlinks in the crawl and is only reachable through the sitemap. `/coffee/` lists only Kintamani and Ijen. `/shop/` and the homepage do the same.

**Why it matters:** a product with a price, tasting notes and a product image is invisible to visitors and gets no link value. It also has no Product schema (the other two product pages do), and there is no GSC data for it.

**Fix:** add it to the product list on `/coffee/`, `/shop/` and the homepage, and add Product JSON-LD matching the other two (price Rp 155,000, 250g). If the product is discontinued, say so on the page and redirect or remove it.

### 8. `/visit/` is the main local page and is under-built
**URL:** `/visit/` has no `<h1>` (the crawl shows it blank; the page opens with an `<h2>Opening hours</h2>`), 87 words, no address on the page body, no map, no LocalBusiness schema.

**Evidence (gsc.csv):** it ranks for "kopi kita ubud" (96 clicks), "coffee cupping ubud" (pos 4.1, 290 impr) and "coffee shop ubud" (pos 13.5, **2,240 impressions**, CTR 0.7%). The last is the biggest non-brand impression pool on the site.

**Fix:**
- Add an H1 such as "Visit our roastery cafe in Ubud" and keep the existing H2s below it.
- Put the full address, hours, phone and a map embed in the body.
- Add `CafeOrCoffeeShop` (or `LocalBusiness`) JSON-LD with `address`, `geo`, `openingHoursSpecification`, `telephone`, `url`, `image` and `menu`. Today only an `Organization` on the homepage exists, and it has no phone number, hours or coordinates.
- Give cuppings their own section (and possibly their own page), since "coffee cupping ubud" already ranks at 4.1.
- Add "coffee shop" wording to the title or H1 ("Coffee Shop & Roastery Cafe in Ubud") to match "coffee shop ubud".
- Make sure the Google Business Profile has the same name, address and phone as the site.

### 9. The "2024" article is still the best non-brand performer, and it is stale
**URL:** `/blog/best-coffee-beans-2024/`: the URL, title and H1 all say 2024. The copy says "Our picks this year". The schema shows `datePublished` 2024-01-15 and `dateModified` 2026-09-01, so the content was touched recently, but nothing visible on the page says so. It has just 1 inlink (blog index).

**Evidence (gsc.csv):** "best coffee beans bali" pos 7.8 (22 clicks); "bali coffee beans" pos 11.4 (1,890 impressions, 14 clicks). Together this is the best non-brand opportunity after pour over.

**Why it matters:** searchers distrust a "2024" result in late 2026, which holds CTR down (0.7% to 2.3%). Dropping the year later without a redirect would lose the rankings.

**Fix:**
- Retitle to "Best Coffee Beans in Bali (2026 Guide)" and update the H1 to match. Show a visible "Updated" date and the author byline.
- Preferred: move to an evergreen URL (`/blog/best-coffee-beans-bali/`) with a 301 from the old URL, and update the sitemap and the blog index link. If you want to avoid any URL change, keep the URL and update the title and H1 only.
- Make the Article schema headline match the visible H1 (it currently drops "(2024 guide)").
- Link to it from `/coffee/`, `/coffee/bali-kintamani/` and the homepage. At the moment only the blog index links to it. Add a link to `/coffee/flores-bajawa/` and Ijen as well, since the page only recommends Kintamani.
- The "picks" section recommends "a washed Kintamani from any good local roaster". Consider naming a real second pick or a comparison table.

### 10. Duplicate title on `/subscriptions/`
**URL:** `/subscriptions/` has the title "Single-Origin Indonesian Coffee | Kopi Kita", which is an exact duplicate of `/coffee/`. The H1 and description are right ("Coffee subscriptions").

**Evidence (gsc.csv):** "coffee subscription bali" ranks at 5.9 with 310 impressions and 9 clicks (2.9% CTR) despite the wrong title.

**Fix:** change it to something like "Coffee Subscription in Bali: Fresh Beans Every 2 or 4 Weeks | Kopi Kita". The page already ranks, so a relevant title should raise CTR. It also removes the duplicate that makes `/coffee/` and `/subscriptions/` compete for "single origin indonesian coffee".

---

## Medium

### 11. Cold brew article is thin and invisible
**URL:** `/blog/cold-brew-at-home/` (67 words, one paragraph; 1 inlink).

**Evidence (gsc.csv):** "cold brew coffee at home" pos 38.2 (870 impr, 1 click) and "how to make cold brew coffee" pos 44.6 (640 impr, 0 clicks).

**Fix:** expand into a proper guide (at least 400 to 600 words, matching the depth of the pour over article): coarse grind and ratio, steeping time, concentrate versus ready-to-drink dilution, filtering, storage, a Kintamani/Ijen comparison, common mistakes, and a hot-vs-cold-brew note. Add Article schema (the other articles have it, this one does not). Link to it from `/coffee/brewing-guide/`, whose "Cold brew" line currently links nowhere, and from `/visit/` (cold brew is on the cafe menu). If you will not invest in it, consolidate it into the brewing guide and redirect.

### 12. Structured data problems
| Page | Problem | Fix |
|---|---|---|
| `/coffee/` | `FAQPage` markup: the page does not show these questions. One answer ("We roast within 48 hours of shipping") appears in prose, but "Do you ship outside Bali?" does not appear at all. Markup must reflect visible content. FAQ rich results are also limited to a few authoritative site types, so this markup is unlikely to produce anything. | Add a visible FAQ section matching the markup, or remove the JSON-LD. |
| `/coffee/bali-kintamani/` | `Product` has no `name` (required) | Add `"name": "Bali Kintamani natural coffee, 250g"`. |
| `/coffee/bali-kintamani/`, `/coffee/java-ijen/` | Offers have no `url` or `priceValidUntil`. There is no `sku`/`gtin`, reviews or ratings. | Add `url` and `sku`. Only add ratings if you have real reviews. |
| `/coffee/flores-bajawa/` | No Product markup at all | See issue 7. |
| `/blog/*` Articles | No `image`, `publisher` or `mainEntityOfPage`. The `headline` on the Bali article differs from the H1. `dateModified` is not visible on the page. The cold brew article has no Article schema at all. | Complete the schema. Show the date and author on the page. |
| `/` | `Organization` has no `sameAs`, `contactPoint` or phone | Add social profiles and contact details. |

Validate everything with Google's Rich Results Test after the changes.

### 13. 1.8 MB hero image on `/about/`
**URL:** `/assets/img/roastery-hero.jpg` is 1,818,123 bytes (2400×1600), the largest file in the crawl by two orders of magnitude (the next largest is 13.8 KB). It is the first image on `/about/` and will be its LCP element.

**Fix:** export at the largest displayed width (about 1200 to 1600 px), convert to WebP/AVIF, aim for under 200 KB, and use `srcset` with `sizes`. Keep the width/height attributes (already present, which is good). The `about` page ranks for "ubud coffee roaster" (pos 8.9, 640 impr), so a fast page there has direct value. Do not lazy-load the LCP image.

### 14. Missing meta description, alt text and canonical
- `/about/` has **no meta description** (crawl: length 0). It ranks for "ubud coffee roaster" at 8.9 with 640 impressions and a 1.9% CTR. Write about 150 characters, for example "Kopi Kita is an Ubud coffee roaster. Meet head roaster Wayan Sudarma and the farmer groups behind our Bali, Java and Flores beans."
- `/assets/img/hero-beans.jpg` on `/` has **no alt attribute** (the crawl shows "(missing)"). Add descriptive alt text, for example "Freshly roasted Indonesian coffee beans".
- `/contact/` has **no canonical tag** (the only page missing one). Add a self-referencing canonical, and use the same pattern in the shared template.
- `/contact/` meta description is short (77 characters). Lengthen it a little and include the phone/WhatsApp CTA.

### 15. Two H1s on the brewing guide
**URL:** `/coffee/brewing-guide/` has `<h1>Coffee brewing guide</h1>` and `<h1>Brew methods</h1>`. **Fix:** make "Brew methods" an H2, and give the other sections (grind size chart, water temperature, troubleshooting) H2s with `id` anchors.

The page ranks for "coffee grind size chart" (pos 15.5, 980 impr) and "coffee brewing guide" (pos 12.8, 1,240 impr). The grind chart is a single run-on paragraph. Turn it into an actual HTML table (method, grind, ratio, time) and put "grind size chart" into an H2. That is a realistic page-1 gain. Also link it to the cold brew and pour over articles.

### 16. Over-long title on Kintamani
**URL:** `/coffee/bali-kintamani/` has an 88-character title ("Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita") that Google will truncate (about 60 characters is safe). **Fix:** "Bali Kintamani Natural Coffee Beans | Kopi Kita" (about 47) or "Bali Kintamani Natural Coffee, 250g | Kopi Kita". It ranks at 8.2 to 9.6 for "bali kintamani coffee" and "kintamani coffee beans" (about 2,170 impressions combined), so keep "Kintamani coffee" near the start of the title.

### 17. Ranking opportunities not yet targeted
Pages are in positions 4 to 14 with large impression counts but low CTR:

| Query | Page | Pos | Impr | CTR | Action |
|---|---|---|---|---|---|
| coffee shop ubud | `/visit/` | 13.5 | 2,240 | 0.7% | Issue 8 |
| coffee roastery ubud | `/` | 6.8 | 1,320 | 3.1% | Add "Ubud coffee roaster" wording to the homepage title/H1 ("Specialty Coffee Roaster in Ubud, Bali"), plus a link to `/about/` and `/visit/` |
| ubud coffee roaster | `/about/` | 8.9 | 640 | 1.9% | Issue 14. Tell the roastery story (400 kg a week, 30+ partners) in more depth. Add the meta description. |
| bali coffee beans / best coffee beans bali | best-beans article | 11.4 / 7.8 | 1,890 / 960 | 0.7% / 2.3% | Issue 9 |
| buy coffee beans bali | `/coffee/` | 10.2 | 690 | 1.4% | The page is only 102 words. Add a product grid with prices, origin, process, roast level and links (including Flores) and a short buying guide. |
| single origin indonesian coffee | `/coffee/` | 9.3 | 560 | 1.3% | As above, and fix the `/subscriptions/` duplicate title (issue 10) |
| coffee brewing guide / grind size chart | `/coffee/brewing-guide/` | 12.8 / 15.5 | 1,240 / 980 | 0.6% | Issue 15 |
| pour over cluster | two pages | 14 to 21 | 8,830 | 0.4% | Issue 1 |
| cold brew | cold brew article | 38 to 45 | 1,510 | about 0% | Issue 11 |

Also consider: the brand is Indonesian ("Kopi Kita" means "our coffee") and the site is English only with `lang="en"`. Indonesian-language queries ("kopi bali", "biji kopi kintamani", "langganan kopi") are not covered. An Indonesian version with `hreflang` is a longer-term option, not a quick fix.

---

## Low

### 18. Missing sitewide extras
- No Open Graph / Twitter Card tags on any page, so link shares have no image or title control. Add `og:title`, `og:description`, `og:image`, `og:url`, `og:type`.
- No favicon link in `<head>`.
- No breadcrumbs or `BreadcrumbList` schema on `/coffee/*` or `/blog/*`.
- Blog index has no dates, excerpts or pagination structure, and article pages show no visible byline or date even though the schema claims an author and dates.

### 19. Smaller points
- Title lengths are fine apart from Kintamani (30 to 57 characters), and descriptions run 77 to 129. Several descriptions (blog 95, `/shop/` 95, `/coffee/` 96, cold brew 83) are on the short side and could carry a call to action.
- The nav label "Visit the cafe" and page title "Visit Our Roastery Cafe" are fine, but `/visit/` has no on-page text link from `/about/` other than one contextual link. Add more (issue 2).
- `site.css`, JS and images have no cache or compression details in the evidence. Confirm `Cache-Control` and gzip/brotli are set on production. The local Python server used for the crawl does not tell us anything here.
- The contact page shows a placeholder-looking phone number (`+62 812 0000 0000`) and an email on the test domain. Confirm the real values go live. They matter for local SEO and for NAP consistency with the Google Business Profile.
- `robots.txt` has a single `User-agent: *` group, which is fine. After removing the CSS block, resubmit the sitemap in Search Console.

---

## Working well (leave alone)
- Every indexable page has a unique title and H1 (except the issues above), correct self-referencing canonicals (except `/shop/` and `/contact/`) and a meta description (except `/about/`).
- Clean, trailing-slash URL structure with no parameters. 200 status on every live page.
- Product images have descriptive alt text and explicit width/height. Product prices in the schema match the visible prices (Rp 145,000 and Rp 150,000).
- Strong internal anchor text on the product links. Strong brand rankings (positions 1.1 to 1.6) and healthy branded CTR.

## Suggested order of work
1. **This week (about 1 to 2 hours of template/config changes):** fix the nav link (2), remove the CSS block (5), remove Sumatra from the sitemap and fix the Aceh link (6), decide on `/wholesale/` noindex (3) and the `/shop/` canonical (4), fix the `/subscriptions/` title (10), add the `/about/` description and the hero alt (14), turn the second H1 into an H2 (15).
2. **Next 2 weeks:** merge the pour over articles with a 301 (1), rebuild `/visit/` with an H1, schema and map (8), refresh the Bali beans article (9), link the Flores page (7), shorten the Kintamani title (16), compress the hero (13).
3. **Next month:** expand the cold brew article (11), extend `/coffee/` and the brewing guide (15, 17), clean up structured data (12), add Open Graph tags and breadcrumbs (18).
4. **Measure:** re-export GSC after 4 to 6 weeks and check the pour over cluster (target: one page in the top 10), `coffee shop ubud`, `bali coffee beans` and `/wholesale/` indexing status.

## Not covered by this evidence
HTTPS/www/non-slash redirects on production, Core Web Vitals (field data), backlink profile and competitors, rendered-page review, XML sitemap submission status and Search Console Coverage/Indexing reports, the `X-Robots-Tag` headers and server compression/caching on production.
