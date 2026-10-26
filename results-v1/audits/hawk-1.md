# TECHNICAL SEO AUDIT: https://kopikita.test/

**Date:** 22 October 2026
**Data sources:** Screaming Frog-style crawl export (27 URLs: 19 HTML pages, 1 CSS, 6 images, 2 redirects counted within), raw HTML of every page, robots.txt, sitemap.xml, GSC Performance export (queries × pages, 22 Jul – 21 Oct 2026, 27 rows), plus live `curl` of the redirects on localhost:8765.
**Pages analysed:** 22 HTML URLs (17 return 200, 2 are 301s, 2 are 404s, plus the 301 `/menu/` source), 6 images, 1 CSS file.

**Limits of the data (what I could not assess):**
- The crawl was not JavaScript-rendered; the site appears to be static HTML, so this matters little, but I haven't verified it.
- No response times, Core Web Vitals, or PageSpeed data. Page weight is only visible for the images.
- The GSC export has 27 rows only, so it is a top-rows sample. It has no Index Coverage / Page Indexing data, so I can't confirm which URLs Google has actually indexed.
- HTTP→HTTPS redirects, www/non-www, and trailing-slash handling can't be tested on a `.test` domain served over local HTTP. Check these on production.
- Backlinks, hreflang (single-language site, so not applicable), and mobile rendering were not in scope of the evidence.

---

## CRITICAL (fix this week)

### 1. Two pour-over articles cannibalise each other and neither ranks
**URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
**Evidence (GSC):** both pages appear for the same four queries, and Google is swapping between them:

| Query | how-to-brew-pour-over | pour-over-coffee-guide |
|---|---|---|
| pour over coffee | 2,410 impr, pos 16.2 | 1,980 impr, pos 18.7 |
| how to make pour over coffee | 1,350 impr, pos 14.1 | 1,120 impr, pos 17.3 |
| pour over coffee guide | 610 impr, pos 19.4 | 820 impr, pos 13.9 |
| pour over ratio | 540 impr, pos 21.0 | – |

Roughly 8,800 impressions across these queries produce only ~36 clicks (≈0.4% CTR), all on pages 2–3. The titles ("How to Brew Pour Over Coffee at Home" vs "Pour Over Coffee Guide for Beginners"), H1s, and body copy (both cover 15g/250g/93C, bloom, grind) target the same intent.
**Why it matters:** Two near-identical answers split links, clicks and relevance signals, so neither can break onto page 1. Consolidating is the single biggest ranking opportunity in the data.
**Fix:**
1. Keep `/blog/how-to-brew-pour-over/` (longer, 440 words, more clicks, older, `dateModified` 2026-08-02) as the winner.
2. Move the unique parts of `pour-over-coffee-guide` (dripper choice V60 vs Kalita, filters, kettle, tasting, the 1:15 / 1:17 ratio advice) into it, and add a headed "Pour over ratio" section for the 21-position query.
3. 301 `/blog/pour-over-coffee-guide/` → `/blog/how-to-brew-pour-over/`, remove it from `sitemap.xml` and from `/blog/` index, and update the `Article` schema.
4. Retitle the survivor to carry the head term, e.g. `Pour Over Coffee: How to Brew It at Home (Ratio & Recipe) | Kopi Kita`.
5. Link to it from `/coffee/brewing-guide/` with "pour over coffee" anchor text (it already links with "how to brew pour over").
If you'd rather keep both, split intent clearly (a beginner gear guide vs a recipe), retitle and rewrite both so no query overlaps, and cross-link them. Consolidation is the better option here.

### 2. Site-wide navigation links to a redirect chain (`/menu/` → `/cafe/` → `/visit/`)
**URLs:** the "Visit the cafe" link in the nav on every page points at `/menu/` (17 internal links in the crawl). Live check confirms `/menu/` → 301 `/cafe/` → 301 `/visit/`.
**Why it matters:** Every crawl of every page runs through two hops, wasting crawl requests and diluting the link equity going to `/visit/`. Meanwhile `/visit/` itself only has 2 inlinks counted in the crawl, and it is the page that ranks for "kopi kita ubud" (96 clicks) and "coffee shop ubud" (2,240 impressions at position 13.5, only 0.7% CTR).
**Fix:** Change the nav `href` to `/visit/` in the shared header template, so all ~16 pages link directly. Then collapse the redirects to a single hop (`/menu/` → `/visit/`, `/cafe/` → `/visit/`). Rename the anchor if you like ("Visit the cafe" is fine).

### 3. Broken internal link and a 404 in the sitemap
- **`/coffee/aceh-gayo/` returns 404.** It is linked from `/blog/how-to-brew-pour-over/` ("try our Aceh Gayo"), one of your best-performing articles. Fix: remove the link, or link to a product that exists (`/coffee/bali-kintamani/` for the "heavier" option, which matches its "heavy body" description).
- **`/coffee/sumatra-mandheling/` returns 404 but is listed in `sitemap.xml`** and has 0 inlinks. Fix: delete it from the sitemap (or, if the coffee was meant to exist, publish the page).
**Why it matters:** A sitemap should list only live, indexable 200 URLs; including a 404 erodes trust in the file and wastes crawl, and a broken link on a key article is a dead end for users.

---

## HIGH PRIORITY (fix this month)

### 4. `/shop/` is canonicalised to `/coffee/` but is in the sitemap and in the main nav
**URL:** `/shop/` (`rel=canonical` → `https://kopikita.test/coffee/`; crawl: Non-Indexable, Canonicalised; 16 inlinks; listed in `sitemap.xml`).
**Why it matters:** The sitemap and the nav tell Google `/shop/` is important while the canonical tag says "don't index me". Mixed signals. The page content is also genuinely different (gear, drip bags, free-shipping threshold), so the canonical is probably a mistake, though it only offers two products and duplicates the `/coffee/` hub.
**Fix (choose one):**
- **A. Keep it as a distinct page:** make the canonical self-referencing, retitle to target gear and drip bags (not "Coffee Beans", which collides with `/coffee/` for "buy coffee beans bali", currently position 10.2), add all three coffees including Flores Bajawa, and add real gear/drip-bag pages to link to.
- **B. Retire it:** 301 `/shop/` → `/coffee/`, drop it from the nav and sitemap.
Either way remove it from the sitemap until it is indexable.

### 5. `/wholesale/` is `noindex` but is in the sitemap and the main nav
**URL:** `/wholesale/` (`<meta name="robots" content="noindex, follow">`, in sitemap, 16 inlinks).
**Why it matters:** If wholesale is a revenue line (the About page says 30+ wholesale partners), it can't be found via Google, and no GSC impressions exist for it, consistent with it being excluded. If the noindex is intentional (e.g. a leftover from a staging build), the sitemap entry contradicts it.
**Fix:** I can't tell intent from the data, so confirm with the business. If it should rank: remove the `noindex` and target "wholesale coffee bali" (the title and H1 already do). If not: remove it from the sitemap. The `follow` directive is fine either way.

### 6. robots.txt blocks the site's CSS
**File:** `robots.txt` has `Disallow: /assets/css/`. The crawl shows `/assets/css/site.css` as "Blocked by robots.txt", and every page references it.
**Why it matters:** Googlebot renders pages like a browser; blocked CSS means it can't see the layout, so it can't judge mobile-friendliness or what is above the fold. Google explicitly advises against blocking CSS/JS.
**Fix:** Remove the line. `Disallow: /cart/` is harmless (no `/cart/` URL exists in the crawl) and can stay. Keep the `Sitemap:` line.

### 7. `/subscriptions/` has the same title as `/coffee/`
**URLs:** `/subscriptions/` and `/coffee/` both have the title "Single-Origin Indonesian Coffee | Kopi Kita" (43 chars). The subscription page's description and H1 are about subscriptions, so the title looks like a copy-paste error.
**Why it matters:** Duplicate titles blur which page answers which query. `/subscriptions/` already ranks at 5.9 for "coffee subscription bali" with 310 impressions and a 2.9% CTR, with a title that never mentions subscriptions.
**Fix:** `Coffee Subscription in Bali: Fresh Beans Every 2–4 Weeks | Kopi Kita` (≈66 chars; trim to `Coffee Subscription in Bali | Fresh Beans Delivered | Kopi Kita` if you want it under ~60).

### 8. `/coffee/flores-bajawa/` is an orphan, and the hub pages leave it out
**URL:** `/coffee/flores-bajawa/` has 0 inlinks in the crawl and is in the sitemap. Neither `/coffee/` (lists only Kintamani and Ijen) nor `/shop/` links to it, and no blog post does. It is also thin (75 words) and has no Product schema.
**Why it matters:** With no internal links, the page gets no equity and relies solely on the sitemap; it is also a sellable product.
**Fix:** Add it to `/coffee/` and `/shop/` and mention it on the homepage ("Kintamani, Ijen and Flores" already appears in the intro, so link "Flores"). Add roast, price, brewing suggestion, and farm detail (the Kintamani page is the template), plus Product schema (see #12).

### 9. Pages that should be getting links have very few
From the crawl (Inlinks): the four blog posts have **1** inlink each (from `/blog/`), except `how-to-brew-pour-over` which has 2; `/visit/` has 2 (before fixing #2); the product pages and the brewing guide have 5. Every page gets 16 from the nav and footer, so the table above only reflects contextual links.
**Fix (contextual links in body copy):**
- `/coffee/bali-kintamani/` → `/blog/best-coffee-beans-2024/` ("how to choose Bali coffee beans"); `/coffee/` → the same.
- `/coffee/java-ijen/` and `/coffee/brewing-guide/` → `/blog/how-to-brew-pour-over/` and `/blog/cold-brew-at-home/` (the brewing guide covers cold brew but doesn't link to the post).
- `/blog/cold-brew-at-home/` and `/blog/best-coffee-beans-2024/` → the relevant products and `/subscriptions/`.
- `/about/` → `/visit/` already exists; add `/visit/` links from the homepage and `/contact/` ("pick up at the roastery cafe" on the homepage currently has no link).

### 10. `/visit/` has no H1 and is under-optimised for its biggest query
**URL:** `/visit/`: crawl shows an empty H1 (the HTML uses only two `<h2>`s: "Opening hours" and "Menu"). It gets 2,240 impressions for "coffee shop ubud" at position 13.5 (0.7% CTR), 410 for "kopi kita ubud" and 290 for "coffee cupping ubud".
**Fix:** Add `<h1>Visit our roastery cafe in Ubud</h1>`, expand the body (87 words) with address, a map embed, photos, the menu, and the Saturday cupping, and use "coffee shop" naturally. See schema in #12 (CafeOrCoffeeShop + opening hours).

---

## MEDIUM PRIORITY (roadmap)

### 11. Thin content on pages with search demand
Word counts from the crawl: `/blog/cold-brew-at-home/` **67**, `/coffee/flores-bajawa/` 75, `/shop/` 86, `/visit/` 87, `/coffee/java-ijen/` 98, `/coffee/` 102, `/about/` 108, `/` 132, `/blog/` 43, `/contact/` 61.
Most matter little (index/contact pages), but two are real problems:
- **`/blog/cold-brew-at-home/`**: 870 and 640 impressions for "cold brew coffee at home" / "how to make cold brew coffee" at positions 38 and 44, which is invisible. 67 words can't compete with pages that cover ratios, steep times, grind, concentrate vs ready-to-drink, and storage. Expand to 600+ words (or fold into the brewing guide, which has a cold-brew line) and add FAQs.
- **Product pages (`/coffee/java-ijen/` 98, flores 75)** are shorter than Kintamani's; add farm story, tasting notes, brew suggestions and delivery information. Kintamani is already ranking for 31 + 17 clicks.

### 12. Structured data issues
Extracted from the HTML:
- **`/coffee/bali-kintamani/`: `Product` has no `name`** (required for Product rich results). Add `"name": "Bali Kintamani natural coffee, 250g"`; also add `sku`, `url`, `priceValidUntil` (recommended), and `aggregateRating`/`review` only if you have real reviews.
- **`/coffee/flores-bajawa/`: no Product schema at all**, unlike its siblings. Add one (price Rp 155,000 per the page).
- **`/coffee/`: `FAQPage` markup, but the page body shows no FAQ**: the questions "How fresh is your coffee?" and "Do you ship outside Bali?" aren't visible (only a freshness line appears). Markup must match visible content, and Google only shows FAQ rich results for a narrow set of authoritative sites, so there is little upside. Either add a visible FAQ section or remove the block.
- **`Article` on all three blog posts:** missing `image` and `publisher`; `author` has no `url`. `/blog/best-coffee-beans-2024/` headline is "The best coffee beans in Bali", not the on-page H1. `/blog/cold-brew-at-home/` has no schema at all.
- **Organization on `/`:** fine; add `sameAs` (Instagram/Google Business Profile), `contactPoint`.
- **Missing: local business markup.** There is a physical cafe (7am–5pm daily, Jl. Raya Sayan 12). Add `CafeOrCoffeeShop` (or `LocalBusiness`) schema with `openingHoursSpecification`, `geo`, `telephone` to `/visit/` and `/contact/`. Also consider `BreadcrumbList` across the site.
All of the above should be tested with Google's Rich Results Test after deploy.

### 13. Stale "2024" on a page that is edited in 2026
`/blog/best-coffee-beans-2024/`: URL, title ("Best Coffee Beans in Bali (2024 Guide)"), and H1 contain 2024, but the schema `dateModified` is 2026-09-01 and the body says "Our picks this year". It ranks 7.8 for "best coffee beans bali" (22 clicks) and 11.4 for "bali coffee beans" (1,890 impressions, 0.7% CTR).
**Why it matters:** An out-of-date year in the SERP snippet reduces CTR.
**Fix:** Retitle to `Best Coffee Beans in Bali: How to Choose & Our Picks (2026)`, change the H1, and keep the URL (or, if you change it, 301 it). Better long-term: use a year-less slug.

### 14. `/coffee/brewing-guide/` has two H1s
H1-1 "Coffee brewing guide", H1-2 "Brew methods". Make the second an `<h2>`. The page ranks at positions 12.8 and 15.5 for "coffee brewing guide" (1,240 impressions) and "coffee grind size chart" (980); the grind-size chart is a paragraph, so turn it into a real `<table>` under its own `<h2>`, which can improve both rankings and rich-snippet eligibility.

### 15. Title and meta description clean-up
- **`/coffee/bali-kintamani/`**: title is 88 characters ("Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita"), will truncate in the SERP. Suggestion: `Bali Kintamani Natural Coffee Beans | Kopi Kita` (≈47).
- **`/about/`**: no meta description (crawl length 0); add one. Title (35 chars) is OK but could carry "Ubud coffee roaster" because the page ranks 8.9 for "ubud coffee roaster" (640 impressions, 1.9% CTR).
- **Short descriptions** (under ~120 chars, leaving SERP space unused): `/blog/cold-brew-at-home/` (83), `/contact/` (77), `/blog/` (95), `/coffee/` (96), `/shop/` (95).
- **Homepage**: "coffee roastery ubud" is at position 6.8 with 1,320 impressions and 3.1% CTR. The title ("Kopi Kita | Specialty Coffee Roasted in Ubud, Bali") never uses "roastery"; try `Kopi Kita | Specialty Coffee Roastery in Ubud, Bali`.

### 16. Overlap between `/` and `/about/` for "ubud coffee roaster"
`/` ranks 6.8 for "coffee roastery ubud" while `/about/` ranks 8.9 for "ubud coffee roaster", near-synonyms. It's a mild case (not harmful yet), but pick `/` as the target for these terms and keep `/about/` focused on brand story, with a link to the homepage using "coffee roastery in Ubud".

### 17. Image issues
- **`/assets/img/hero-beans.jpg`** (homepage hero, 1200×700) has **no alt attribute** at all; crawl reports "(missing)". Add descriptive alt text.
- **`/assets/img/roastery-hero.jpg`** is **1.8 MB** (2400×1600), shown on `/about/`. Compress / resize and serve WebP/AVIF at ≤200 KB with `srcset`; add `loading="lazy"` if below the fold.
- All other images have alt text and explicit width/height, which is good.

### 18. `sitemap.xml` hygiene
It lists 18 URLs: includes the 404 (#3), the canonicalised `/shop/` (#4), the noindexed `/wholesale/` (#5), and after #1 will list a redirected URL. No `<lastmod>` values. Fix: list only canonical indexable 200 URLs, and add accurate `<lastmod>` (only if it's genuinely updated by your CMS). Resubmit in Search Console after fixing.

### 19. `/contact/` has no canonical tag
Every other indexable page has a self-referencing canonical. Add `<link rel="canonical" href="https://kopikita.test/contact/">` for consistency. Low risk.

---

## TOP 5 QUICK WINS

1. **Fix the nav link `/menu/` → `/visit/` in the shared header** (all pages; one template change). Impact: **High** (removes a double redirect from 17 pages and gives `/visit/` ~14 more contextual-and-nav links).
2. **Merge the two pour-over posts** into `/blog/how-to-brew-pour-over/` with a 301, new title, and a ratio section. Impact: **High** (≈8,800 impressions currently stuck at positions 14–21).
3. **Fix the three 404 problems:** remove the `/coffee/aceh-gayo/` link, remove `/coffee/sumatra-mandheling/` from the sitemap. Impact: **Medium**.
4. **Retitle `/subscriptions/`** to a unique title that includes "coffee subscription" (and `/coffee/bali-kintamani/` to under 60 chars). Impact: **Medium**.
5. **Remove `Disallow: /assets/css/` from robots.txt** and resolve the `/shop/` canonical-vs-sitemap conflict. Impact: **Medium** (rendering + clean indexation signals).

---

## WHAT'S WORKING (don't change)
- **Clean click depth:** every page is within 2 clicks of the homepage; nav links to all key sections.
- **Self-referencing canonicals on all indexable pages** (except `/contact/`), absolute HTTPS URLs, `lang="en"`, viewport meta tag on every page.
- **Unique titles and descriptions on almost every page**, mostly in the 40–57 character range, with the brand last. Titles are descriptive and aligned with the H1s.
- **Branded search is strong:** "kopi kita" at position 1.2 (412 clicks), "kopi kita ubud" at 1.6, with a 23–35% CTR.
- **Product pages already rank on page 1–2 for their own names:** Kintamani 8.2/9.6, Ijen 7.1.
- **Valid `Organization` schema** with logo and address on the homepage; Product pages already carry price, currency, and availability.
- **Images have dimensions** (no layout shift) and, except one, alt text.
- **robots.txt has a `Sitemap:` line**, and the sitemap's URL set otherwise matches the crawlable pages.

## STRIKING-DISTANCE TARGETS (positions 8–21, from GSC)
Beyond the fixes above, these are the queries where on-page work is likeliest to move the needle:
| Query | Page | Impr | Pos | Action |
|---|---|---|---|---|
| coffee shop ubud | /visit/ | 2,240 | 13.5 | H1, expanded content, schema (#10) |
| bali coffee beans | /blog/best-coffee-beans-2024/ | 1,890 | 11.4 | Title refresh (#13), link from product pages |
| bali kintamani coffee | /coffee/bali-kintamani/ | 1,450 | 8.2 | shorter title (#15), more content (#11) |
| coffee roastery ubud | / | 1,320 | 6.8 | "roastery" in title (#15) |
| coffee brewing guide | /coffee/brewing-guide/ | 1,240 | 12.8 | one H1, table for grind size (#14) |
| coffee grind size chart | /coffee/brewing-guide/ | 980 | 15.5 | table (#14) |
| buy coffee beans bali | /coffee/ | 690 | 10.2 | resolve `/shop/` overlap (#4) |

## BOTTOM LINE
The single biggest issue is that the two pour-over articles compete with each other (≈8,800 impressions, page 2–3); merging them, and fixing the nav's double redirect to `/visit/`, will do more for rankings than anything else here.
