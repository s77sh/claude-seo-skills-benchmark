# SEO audit: Kopi Kita (kopikita.test)

Audit date: 22 October 2026. Search Console window: 22 July to 21 October 2026 (90 days).

## Summary

- **Fix first:** the wholesale page is set to `noindex` (a tag that tells Google to keep a page out of search). It is the page for the business's B2B line (30+ venues already supplied), and no Search Console query shows it.
- **Biggest traffic gap:** two pour over articles compete for the same queries. They sit at positions 14 to 21 and turn about 8,800 impressions into 36 clicks.
- **Cleanup that is cheap and clean:** 404s, a double redirect in the site-wide menu link, an orphaned product page, a robots.txt rule that hides the CSS, and a handful of title, heading and schema defects.
- **Already working, protect it:** brand searches ("kopi kita", "kopi kita ubud", "kopi kita coffee") rank #1 to #2 with 23% to 35% click-through. Don't touch the homepage title or the `/visit/` URL.

## Evidence and limits

- Sources: `crawl.csv` (27 URLs), raw HTML for all 17 pages, `robots.txt`, `sitemap.xml`, `gsc.csv` (27 query/page rows), and curl checks against localhost:8765.
- The localhost curl checks matched the crawl: `/menu/` returns 301, `/coffee/sumatra-mandheling/` returns 404, and robots.txt is as exported.
- No live Google results were checked, and no keyword-volume tool was available. Position and impressions come only from Search Console. Positions are averages over the 90 days.
- Search Console shows only queries Google reported. A page with no rows has no recorded data. That is not proof of zero rankings.
- Ranking causes are not proven here. Where I say "likely", it is a reading of the evidence.

---

## Priority 1: Revenue-blocking

### 1. Wholesale page is noindexed and still in the sitemap

- **URL:** https://kopikita.test/wholesale/
- **Found:** `<meta name="robots" content="noindex, follow">`. The crawl marks it Non-Indexable. The sitemap still lists it, and all 16 pages link to it from the main menu.
- **Why it matters:** the page is well written for the buyer (30+ partners, 5kg/week minimum, free training, next-day delivery in Ubud, Canggu, Seminyak and Sanur). `noindex` stops Google showing it for searches such as "wholesale coffee bali" or "coffee supplier for cafes ubud". Search Console has no wholesale query at all, which fits with that, though it is not proof. Wholesale accounts are likely worth far more per customer than a 250g bag. That is an inference from the page content, not a figure from the data.
- **Fix:**
  1. Remove the `noindex` tag, unless it was deliberate (for example the page was a draft). Nothing on the page suggests that.
  2. Keep the self-referencing canonical, which is already correct.
  3. Add a short contact form or direct WhatsApp link on the page. It currently only links to `/contact/`.
  4. After the change, request indexing in Search Console and watch for wholesale queries in the next report.
- **Expected benefit:** unknown in size. No demand data was available, so I am not estimating one. The direction is clear: a page that is blocked cannot rank.

### 2. Sitemap lists URLs that should not be there

- **URLs:** `/coffee/sumatra-mandheling/` (404), `/wholesale/` (noindex), `/shop/` (canonical points to `/coffee/`).
- **Why it matters:** a sitemap should list only live, indexable, canonical pages. Mixed signals waste crawl attention and make the Search Console coverage report noisy.
- **Fix:** remove the Sumatra 404 (or publish the product page, see item 4). Keep `/wholesale/` once indexable. Decide on `/shop/` under item 6. Add `<lastmod>` dates, which every entry currently lacks.

---

## Priority 2: Largest traffic opportunities

### 3. Two pour over articles compete for the same searches

- **URLs:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Found:** both pages rank for the same four queries, and Google swaps between them. Neither reaches page 1 (positions 14 to 21).

| Query (GSC, 22 Jul to 21 Oct 2026) | how-to-brew-pour-over: impr / pos | pour-over-coffee-guide: impr / pos |
|---|---|---|
| pour over coffee | 2,410 / 16.2 | 1,980 / 18.7 |
| how to make pour over coffee | 1,350 / 14.1 | 1,120 / 17.3 |
| pour over coffee guide | 610 / 19.4 | 820 / 13.9 |
| pour over ratio | 540 / 21.0 | (no row) |

- **Why it matters:** this is the largest block of impressions on the site that isn't brand-related. It earns 36 clicks, about 0.4% click-through. The two pages have near-identical recipes (15g coffee, 250g water, 93C, 40g bloom). Splitting relevance and links across two pages likely keeps both off page 1. Impressions of the same query on different pages overlap, so the unique pool is roughly 5,100 impressions (the largest row per query), not 8,800.
- **Fix:**
  1. Pick one winner. I suggest `/blog/how-to-brew-pour-over/` (440 words, better positions on three of four queries, two internal links already).
  2. Merge the best unique material from the other page into it: dripper choice (V60 vs Kalita Wave), filter rinsing, kettle tips, ratio variations (1:15 to 1:17), tasting notes.
  3. Add a ratio table and a short step list with timings so it can win "pour over ratio" and "how to make" queries.
  4. 301 redirect (a permanent redirect) `/blog/pour-over-coffee-guide/` to the winner. Remove it from the sitemap and blog index.
  5. Retitle the winner to cover both intents, for example "How to Brew Pour Over Coffee: Ratio, Recipe and Beginner Guide".
  6. Send the pages' supporting links (blog index, brewing guide, Ijen product page) to the one URL.
- **Hypothetical scenario (not a forecast):** if the merged page reached about position 8 on the queries above and earned about 2% click-through, 5,100 unique impressions would give about 100 clicks per 90 days, against about 36 now. The 2% figure is my assumption, taken from how this site's own position 7 to 9 pages perform (1.9% to 2.9%).
- **Risk:** consolidation can take weeks to settle. If the pages target different intents in the real results, merging could lose one of them. Watch both queries for a month.

### 4. Fix the broken product links and the orphaned product page

- **URLs:** `/coffee/aceh-gayo/` (404, linked from the pour over how-to post), `/coffee/sumatra-mandheling/` (404, in the sitemap, 0 inlinks), `/coffee/flores-bajawa/` (200, 0 internal links, only in the sitemap).
- **Why it matters:** a reader who takes the product recommendation in the pour over article, the site's best-linked blog post, lands on a 404. The Flores Bajawa page has no links from the homepage, `/coffee/` or `/shop/`, so Google only finds it through the sitemap, and visitors can't find it at all.
- **Fix:**
  1. In the pour over article, change the Aceh Gayo link to a live product (Bali Kintamani suits "heavier"), or create the Aceh Gayo page if you actually sell it.
  2. Delete the Sumatra Mandheling entry from the sitemap, or publish the page.
  3. Link Flores Bajawa from `/coffee/` and `/shop/`.
  4. The homepage and `/coffee/` show only two of the three live beans. Add the third.

### 5. Local searches: the cafe page and the roastery pages are underperforming

- **URLs:** https://kopikita.test/visit/ and https://kopikita.test/ (and `/about/`)
- **Found:**

| Query (GSC) | Page | Impressions | Position | CTR |
|---|---|---|---|---|
| coffee shop ubud | /visit/ | 2,240 | 13.5 | 0.7% |
| coffee roastery ubud | / | 1,320 | 6.8 | 3.1% |
| ubud coffee roaster | /about/ | 640 | 8.9 | 1.9% |
| coffee cupping ubud | /visit/ | 290 | 4.1 | 6.2% |

- **Why it matters:** "coffee shop ubud" is the biggest non-brand impression source for the cafe, and it is on page 2. People searching it are nearby or about to be, and are likely to walk in. The `/visit/` page has no H1 (it begins with H2s), 87 words, no map, no photos, and no local business markup. "Ubud coffee roaster" is answered by `/about/` instead of a page built for it, and `/about/` has no meta description.
- **Fix:**
  1. Add an H1 to `/visit/`, such as "Roastery cafe in Ubud: hours, menu and directions".
  2. Add a Google Maps embed, 2 to 3 photos with descriptive alt text, the full address, a phone/WhatsApp number, and a menu with prices.
  3. Add `CafeOrCoffeeShop` (or `LocalBusiness`) structured data with address, geo coordinates, opening hours (7am to 5pm daily) and the page URL. Today the site has only a bare `Organization` block on the homepage.
  4. Add a short section on the free Saturday cupping with a clear heading, since it already ranks at 4.1.
  5. Write a meta description for `/about/` and mention the roastery in the title.
  6. Make sure the Google Business Profile exists, matches the address `Jl. Raya Sayan 12`, and links to `/visit/`. That could not be checked from this evidence.
- **Benefit:** moving "coffee shop ubud" from 13.5 to the first page should lift click-through well above 0.7%. I won't put a number on it without volume data.

---

## Priority 3: Technical and on-page defects

### 6. The `/shop/` page canonicalises to `/coffee/`

- **URL:** https://kopikita.test/shop/
- **Found:** `<link rel="canonical" href="https://kopikita.test/coffee/">` while the page content covers gear and drip bags, which `/coffee/` doesn't. The crawl reports it as Non-Indexable (Canonicalised). It is also in the sitemap and the main menu.
- **Why it matters:** the canonical tells Google to drop `/shop/` in favour of `/coffee/`. Gear and drip bag searches then have no page of their own.
- **Fix:** if `/shop/` is meant to be a separate category, make it self-canonical and list gear and drip bags with product links. If it duplicates `/coffee/`, 301 it to `/coffee/` and remove it from the menu and sitemap. Don't leave the two signals in conflict.

### 7. Site-wide menu link goes through a redirect chain

- **URLs:** `/menu/` → `/cafe/` → `/visit/` (two 301s). The "Visit the cafe" link on all 16 linking pages points to `/menu/`.
- **Why it matters:** every visit pays two extra hops, and `/visit/` ranks for the brand and local queries above. Internal links should point at the final URL.
- **Fix:** change the nav link to `/visit/` in the template. Point `/menu/` straight to `/visit/` with a single 301 (or drop the old redirects once nothing links to them).

### 8. robots.txt blocks the CSS

- **File:** `Disallow: /assets/css/`
- **Why it matters:** Google renders pages to judge layout and mobile usability, and it needs the stylesheet to do that. The crawl reports `site.css` as "Blocked by robots.txt" with 17 inlinks.
- **Fix:** remove the line. `Disallow: /cart/` is harmless, but no `/cart/` exists in the crawl, so remove it too unless a cart is planned. Keep the Sitemap line.

### 9. Titles, descriptions and headings

| URL | Issue | Fix |
|---|---|---|
| `/subscriptions/` | Title "Single-Origin Indonesian Coffee \| Kopi Kita" is identical to `/coffee/`, and matches no subscription query. It ranks 5.9 for "coffee subscription bali". | "Coffee Subscription in Bali: Fresh Beans Every 2 or 4 Weeks \| Kopi Kita" |
| `/about/` | No meta description (crawl length 0). | Write one of 120 to 155 characters. |
| `/coffee/bali-kintamani/` | Title is 88 characters and will be cut off in results. | "Bali Kintamani Natural Coffee Beans, 250g \| Kopi Kita" |
| `/visit/` | No H1. | See item 5. |
| `/coffee/brewing-guide/` | Two H1s ("Coffee brewing guide" and "Brew methods"). | Make "Brew methods" an H2. |
| `/contact/` | No canonical tag. | Add a self-referencing canonical. |
| `/blog/best-coffee-beans-2024/` | "2024" in the URL, title and H1 though the page was updated on 1 Sep 2026. It is at 7.8 to 11.4. | Remove the year from the title and H1 or make it 2026. Keep the URL to avoid a redirect, or move to an undated URL with a 301. |
| `/coffee/bali-kintamani/` and others | Titles and metas are otherwise unique and within length. | None. |
| Meta descriptions | `/blog/` (95), `/blog/cold-brew-at-home/` (83) and `/contact/` (77) are short but valid. | Optional. |

### 10. Structured data (schema markup) errors

- **`/coffee/`** has `FAQPage` markup, but the questions ("How fresh is your coffee?", "Do you ship outside Bali?") are not visible on the page. Google requires marked-up content to be visible, and FAQ rich results are now limited to a few site types. **Fix:** remove the markup, or add a visible FAQ section.
- **`/coffee/bali-kintamani/`** `Product` markup has no `name` field. **Fix:** add `name`, `sku`, and the price valid-until date. The other product pages (Ijen, Bajawa) have no markup at all, so add it there too.
- **Blog posts:** `Article` markup exists on two of four posts. Add it to the other two and add the author's page URL. The `pour-over-coffee-guide` post shows a publish date but no sign of an update.
- **Homepage `Organization`:** the `logo.png` file isn't in the crawl, so check that it resolves.
- **Fix, one at a time:** validate each page with Google's Rich Results Test after changing it.

### 11. Images

- `/assets/img/roastery-hero.jpg` is 1.8 MB (2400×1600) on `/about/`, the largest file in the crawl. Compress it to under 300 KB, serve at roughly display width, and consider WebP.
- `/assets/img/hero-beans.jpg` on the homepage has no alt text (the crawl shows "(missing)") and is 13 KB. Add a descriptive alt.
- All other images have clear alt text. Add `loading="lazy"` for anything below the first screen.

---

## Priority 4: Lower-impact opportunities

### 12. Cold brew post is too thin to rank

- **URL:** https://kopikita.test/blog/cold-brew-at-home/
- **Found:** 67 words, a single paragraph. Position 38.2 for "cold brew coffee at home" (870 impressions) and 44.6 for "how to make cold brew coffee" (640 impressions). One click in 90 days.
- **Fix:** expand to a real guide (ratio table for concentrate and ready-to-drink, grind, steeping time, storage, serving ideas, a troubleshooting section) using the same structure as the pour over post (about 440 words). Link it from `/coffee/brewing-guide/`, which lists the cold brew ratio but does not link out.
- **Priority reason:** about 1,500 impressions at positions 38 to 45 is a long climb to page 1, in a crowded topic where the brand has little authority. It is cheaper to win the pour over cluster first.

### 13. Brewing guide and grind size queries

- **URL:** https://kopikita.test/coffee/brewing-guide/
- **Found:** "coffee brewing guide" at 12.8 (1,240 impressions) and "coffee grind size chart" at 15.5 (980 impressions). The grind chart is one bolded sentence inside the page.
- **Fix:** turn the grind chart into a real table with a heading ("Coffee grind size chart"), add photos or a visual, and add a short section for each method linking to a dedicated post. Fix the double H1 (item 9). Keep the pour over section short and link to the merged article from item 3 so that the two don't overlap.

### 14. Best coffee beans in Bali

- **URL:** https://kopikita.test/blog/best-coffee-beans-2024/
- **Found:** "best coffee beans bali" at 7.8, "bali coffee beans" at 11.4 (1,890 impressions, 0.7% CTR). Its main CTA is a link to Kintamani.
- **Fix:** don't rewrite. Refresh the title and H1 (item 9), add a comparison table of the three beans and a prominent product card or button to the Kintamani product page. Add a link to the Ijen and Bajawa pages too, since the article currently pushes visitors toward a washed coffee "from any good local roaster". That competitor mention sends buyers elsewhere. It would be better to point at your own Ijen (washed).

### 15. Product pages

- `/coffee/bali-kintamani/` ranks 8.2 for "bali kintamani coffee" and 9.6 for "kintamani coffee beans" (about 2,200 impressions together, 2.1% to 2.4% CTR). It is a reasonable page. Add customer reviews, a photo gallery, a grind or size selector and an FAQ so it stands out in results.
- `/coffee/java-ijen/` ranks 7.1 for "java ijen coffee". Fine as it is.
- `/coffee/` ranks 9.3 for "single origin indonesian coffee" and 10.2 for "buy coffee beans bali". Add a short intro paragraph above the product list with those phrases, and make the page list the beans with prices and links instead of prose.

### 16. Internal linking

- Blog posts have 1 or 2 internal links each. `/blog/best-coffee-beans-2024/`, `/blog/cold-brew-at-home/` and `/blog/pour-over-coffee-guide/` are linked only from the blog index.
- Link the blog posts to each other and into products where relevant. `/subscriptions/` has 16 links but they are all from the navigation. Add contextual links to it from the product pages ("Subscribe and save") and `/coffee/`.
- Add breadcrumbs to blog and product pages.

### 17. Other minor items

- No Open Graph or Twitter card tags on any page. Add `og:title`, `og:description` and `og:image`, so links shared on social and chat apps look right.
- Nothing is marked up for language or region. The site is English-only and targets Indonesia, so `hreflang` isn't required. Skip it unless an Indonesian version is planned.
- Footer repeats the address but not a phone number. Add one, matching the `/contact/` page and the schema.
- HTTPS, the www/non-www variants and page speed could not be checked (the evidence is a local copy). Check them on the production domain before launch.

---

## What is fine

- Every page has a unique title under about 60 characters, except the items listed in item 9.
- Every indexable page has a canonical tag except `/contact/`, and each one points to itself apart from `/shop/`.
- No page is blocked from indexing except the wholesale page.
- Viewport tags and `lang="en"` are present on every page.
- Brand queries rank first and convert at 20% to 35%.
- Product page content is specific (altitude, farmer group, varieties, harvest date, prices), which is what ranks.

## Suggested order of work

1. Remove `noindex` from `/wholesale/` and request indexing (minutes).
2. Fix links: nav `/menu/` → `/visit/`, Aceh Gayo link, sitemap 404, orphaned Bajawa page (an hour).
3. Resolve the `/shop/` canonical, robots.txt CSS rule and the title/H1/meta fixes in item 9 (an hour or two).
4. Merge the two pour over articles and set up the 301 (half a day).
5. Rebuild `/visit/` with an H1, map, menu and local schema (half a day).
6. Fix schema, images, and the lower-priority content items.
7. Re-pull Search Console after 4 to 6 weeks and compare the pour over, "coffee shop ubud" and wholesale queries against the baseline above.
