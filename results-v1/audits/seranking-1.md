# SEO Audit: Kopi Kita (kopikita.test)

Audit date 2026-10-22. Sources: raw HTML of all 18 pages in `evidence/site/`, `robots.txt`, `sitemap.xml`, `crawl.csv` (27 URLs incl. assets), `gsc.csv` (27 query/page rows, 22 Jul to 21 Oct 2026), and live spot-checks of the local server (redirects, 404s, headers).

**Scope and limits.** The SE Ranking, Firecrawl, CrUX and GSC URL Inspection tools were not used: the site is a local `.test` host and the brief said to work from the evidence provided. So there is no Core Web Vitals field data, no index-status check, and no JS-rendering check. The pages are plain static HTML with no JS, so the rendering risk is low. The local server (Python SimpleHTTP) sends no security headers; that tells us nothing about production, so headers are listed as "verify on production" rather than as a finding. The GSC export holds only 27 rows, so the search figures below are directional.

## Summary

| Severity | Count | Issues |
|---|---|---|
| Critical | 2 | #1 pour-over cannibalisation, #2 broken Sumatra/Aceh URLs (404s in sitemap and in body copy) |
| High | 5 | #3 wholesale noindex, #4 shop canonicalised to /coffee/, #5 internal redirect chain on site-wide nav link, #6 CSS blocked by robots.txt, #7 Visit page has no H1 and no local schema |
| Medium | 8 | #8 to #15 |
| Low | 10 | #16 to #25 |

Overall: the technical base is clean (all canonicals self-referencing and on https, titles and descriptions present on nearly every page, no JS dependency, sensible URLs, a valid sitemap). The biggest losses are in content architecture, not infrastructure: the site's largest impression pools sit on page 2 and below, split across competing pages, and several revenue pages are mis-signalled to Google.

## Priority fix list

| # | Issue | Severity | URLs | Effort |
|---|---|---|---|---|
| 1 | Two pour-over posts compete for the same queries | Critical | 2 | M |
| 2 | 404s: Sumatra in sitemap, Aceh Gayo linked from a post | Critical | 3 | S |
| 3 | /wholesale/ is `noindex` but is in the sitemap and linked sitewide | High | 1 | S |
| 4 | /shop/ canonicalises to /coffee/ despite distinct content | High | 1 | S |
| 5 | Sitewide nav links to `/menu/`, a two-hop redirect chain | High | 17 inlinks | S |
| 6 | `/assets/css/` blocked in robots.txt | High | all pages | S |
| 7 | /visit/ has no H1 and no LocalBusiness schema | High | 1 | S |
| 8 | Large impression pools with very low CTR | Medium | 6 | M |
| 9 | Duplicate title on /subscriptions/ and /coffee/ | Medium | 2 | S |
| 10 | /coffee/flores-bajawa/ is an orphan, with no Product schema | Medium | 1 | S |
| 11 | Cold brew post thin and not ranking | Medium | 1 | M |
| 12 | Structured data problems (Product, Article, FAQPage, Organization) | Medium | 6 | S |
| 13 | Oversized hero image (1.8 MB) and a missing alt | Medium | 2 | S |
| 14 | Sitemap hygiene (non-indexable and 404 entries, no lastmod) | Medium | sitemap | S |
| 15 | Year-stamped title and URL on an evergreen post | Medium | 1 | M |
| 16 to 25 | See "Low priority" | Low | various | S |

---

## Critical

### 1. Two pour-over posts cannibalise each other
- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Evidence (gsc.csv):** both URLs rank for the same four queries, and Google swaps between them:
  - "pour over coffee": 2,410 impressions at position 16.2 (how-to) and 1,980 at 18.7 (guide)
  - "how to make pour over coffee": 1,350 at 14.1 and 1,120 at 17.3
  - "pour over coffee guide": 820 at 13.9 (guide) and 610 at 19.4 (how-to)
  - Combined: about 8,800 impressions on this cluster (including "pour over ratio"), about 36 clicks, a blended CTR under 0.5%. Both sit on page 2.
- **Why it matters:** the two posts have near-identical intent (the same 15g/250g/93C recipe, the same bloom step, the same Java Ijen link). Google can't pick one, splits link and relevance signals, and neither reaches page 1. This is the largest organic opportunity on the site: page-1 CTR for these terms would be several times higher.
- **Fix:** pick the stronger page as the canonical target, which is `how-to-brew-pour-over` (more words, 440 vs 367, better positions on 3 of 4 queries, updated 2026-08-02). Merge the unique content of the guide (gear and dripper choice, the beginner mistakes, "next steps") into it. 301 `/blog/pour-over-coffee-guide/` to it, remove the guide from the sitemap and update the blog index. Retitle the merged page to something like "How to Make Pour Over Coffee: Beginner's Guide, Ratio and Recipe". If you'd rather keep both, differentiate hard: one a recipe, one a gear guide, with distinct titles, H1s and internal links, and have each link to the other with clear anchor text. Merging is the better option here.

### 2. Broken URLs: one in the sitemap, one linked from a post
- **URLs:** `/coffee/sumatra-mandheling/` (404, **listed in sitemap.xml**, 0 inlinks), `/coffee/aceh-gayo/` (404, linked from `/blog/how-to-brew-pour-over/`, the page with the most impressions on the site).
- **Why it matters:** a sitemap that lists a 404 tells Google the sitemap is unreliable, and reports it in Search Console. The Aceh link sends readers and crawlers from a page ranking for 4 queries to a dead end, and the post is recommending a product you don't sell.
- **Fix:** remove Sumatra from the sitemap. For both, either restore the product page if the coffee is coming back (with Product schema) or 301 to `/coffee/`. In the post, delete the Aceh Gayo sentence or point it at `/coffee/bali-kintamani/` ("heavier" fits: its page says "heavy body").

---

## High

### 3. /wholesale/ is `noindex` yet sitemapped and linked sitewide
- **URL:** `/wholesale/` (`<meta name="robots" content="noindex, follow">`).
- **Why it matters:** wholesale is a B2B revenue line (the about page cites 30+ wholesale partners), and the page is written to rank ("Wholesale Coffee for Cafes and Hotels in Bali", with a meta description). `noindex` makes it invisible to Google, and listing a noindex URL in the sitemap sends a contradictory signal. It looks like a leftover from staging or an intentional hide that was never revisited.
- **Fix:** if the page is meant to attract cafes and hotels, remove the `noindex` meta tag and expand the page (pricing tiers, minimum order, delivery area, a sample-box form, testimonials from partners). If it is intentionally private, remove it from the sitemap too. Confirm with the business which it is. My reading is that it should be indexed.

### 4. /shop/ canonicalises to /coffee/ although its content differs
- **URL:** `/shop/` has `<link rel="canonical" href="https://kopikita.test/coffee/">`. The crawl reports it as "Non-Indexable: Canonicalised", yet it is in the sitemap and has 16 inlinks.
- **Why it matters:** /shop/ describes beans, drip bags, brewing gear and free shipping over Rp 500,000. /coffee/ covers only the single-origin beans. Because the content is not a duplicate, Google may ignore the canonical, or honour it and drop the gear and drip-bag page from search. Either way the gear and drip-bag terms have no indexable home.
- **Fix:** set the canonical to self (`/shop/`). Differentiate it from /coffee/: make /shop/ the full product listing (beans, gear and drip bags with prices) and keep /coffee/ as the origin and coffee-education hub, or fold /shop/ into /coffee/ with a 301 and drop it from the nav. Pick one model; don't leave both.

### 5. Sitewide navigation uses a two-hop redirect chain
- **URLs:** `/menu/` → `/cafe/` → `/visit/`. Every page's nav links to `/menu/` ("Visit the cafe"), which accounts for 17 inlinks. `/cafe/` has 1 inlink (from the redirecting /menu/).
- **Why it matters:** the page that ranks for "kopi kita ubud" and "coffee shop ubud" receives its sitewide internal links through a 2-hop chain. Chains waste crawl budget, slow users down and may dilute equity; Google follows at most about 10 hops but recommends direct links. The destination `/visit/` itself only has 2 inlinks recorded in the crawl (both from the about page and one more), so the nav link is not credited to it directly.
- **Fix:** change the nav link, in the shared template, to `/visit/`. Make `/menu/` a single 301 to `/visit/` (and `/cafe/` likewise) and retain both redirects for old external links.

### 6. `/assets/css/` is blocked by robots.txt
- **URL:** `robots.txt` has `Disallow: /assets/css/`. The crawl shows `/assets/css/site.css` as "Blocked by robots.txt" (17 inlinks, effectively every page).
- **Why it matters:** Googlebot renders pages like a browser. If it can't fetch the CSS it can't evaluate layout, mobile-friendliness or what's visible above the fold. Google's guidelines say not to block CSS or JS. Search Console will report "Googlebot cannot access CSS".
- **Fix:** delete the `Disallow: /assets/css/` line. `Disallow: /cart/` is harmless but refers to a path that doesn't exist; keep it only if a cart is planned. Add a `Disallow` for the real private paths (checkout, account) once they exist.

### 7. /visit/ has no H1 and no local-business structured data
- **URL:** `/visit/`. The page has two H2s ("Opening hours", "Menu") and no H1. The crawl shows an empty H1 column.
- **Evidence (gsc.csv):** this page matters for local intent. "kopi kita ubud" 96 clicks, "coffee cupping ubud" 18 clicks (position 4.1), and "coffee shop ubud" has 2,240 impressions at position 13.5 with a 0.7% CTR.
- **Why it matters:** no H1 gives Google and screen readers no primary heading, a missed place to use "coffee shop in Ubud". The page is also the physical-location page, but there is no LocalBusiness / CafeOrCoffeeShop markup: no hours, no geo coordinates, no phone, no map. The Organization JSON-LD exists only on the homepage.
- **Fix:** add `<h1>Visit the Kopi Kita roastery cafe in Ubud</h1>`. Add `CafeOrCoffeeShop` JSON-LD with `openingHours` (Mon-Sun 07:00-17:00), `address`, `geo`, `telephone`, `url` and `servesCuisine`. Embed a map, add the Saturday 10am cupping as an `Event` if it recurs, and add a Google Business Profile link. Expand the copy (menu highlights, how to get there, parking) and use "coffee shop in Ubud" naturally to target the 2,240-impression query.

---

## Medium

### 8. Large impression pools with very low CTR
Page-1 or near-page-1 queries that earn few clicks. These are where snippet and content work pays fastest.

| Query | URL | Impr. | Pos. | CTR | Action |
|---|---|---|---|---|---|
| coffee roastery ubud | `/` | 1,320 | 6.8 | 3.1% | Title says "Specialty Coffee Roasted in Ubud"; use "Coffee Roastery in Ubud" and add roastery/visit copy and a link to /visit/ |
| ubud coffee roaster | `/about/` | 640 | 8.9 | 1.9% | About has **no meta description** (see #16); write one with "roaster in Ubud" |
| bali coffee beans | `/blog/best-coffee-beans-2024/` | 1,890 | 11.4 | 0.7% | Query is commercial; the page is a blog. Add a buy CTA, and consider a landing page for "Bali coffee beans" |
| bali kintamani coffee | `/coffee/bali-kintamani/` | 1,450 | 8.2 | 2.1% | Title is 88 chars and truncated (see #17); shorten; add Product rich-result fixes (#12) |
| coffee shop ubud | `/visit/` | 2,240 | 13.5 | 0.7% | See #7 |
| coffee brewing guide | `/coffee/brewing-guide/` | 1,240 | 12.8 | 0.6% | Has two H1s (#17); add a ratio table and anchor links |

### 9. Duplicate title tag
- **URLs:** `/subscriptions/` and `/coffee/` both use "Single-Origin Indonesian Coffee | Kopi Kita".
- **Why it matters:** the subscriptions page doesn't say what it is, so it can't win "coffee subscription bali" (position 5.9, 310 impressions, 9 clicks) as well as it could, and the two pages compete.
- **Fix:** retitle subscriptions to "Coffee Subscription in Bali: Fresh Beans Every 2 or 4 Weeks | Kopi Kita".

### 10. /coffee/flores-bajawa/ is an orphan with no structured data
- **URL:** `/coffee/flores-bajawa/` has 0 inlinks. `/coffee/` lists only Kintamani and Ijen, and /shop/ doesn't link to it either. It is in the sitemap, so it is discoverable, but receives no internal equity. It also has no Product JSON-LD (the other two origin pages do), and the intro copy on `/coffee/` ("three to five single origins") mentions none of Flores.
- **Fix:** add it to `/coffee/` and `/shop/` and to the homepage "Kintamani, Ijen and Flores" sentence as a link. Add Product schema (name, image, price Rp 155,000, availability, brand).

### 11. Cold-brew post is thin and ranks far off page 1
- **URL:** `/blog/cold-brew-at-home/`: 67 words, 870 and 640 impressions at position 38.2 and 44.6, 1 click in total.
- **Why it matters:** it is the shortest page on the site, against competitors with detailed recipes. It also isn't linked from anywhere except the blog index (1 inlink).
- **Fix:** expand to 600+ words in the structure of the pour-over post: ratio table, grind size, steep time, concentrate vs ready-to-drink, storage, troubleshooting, a bean recommendation with links to a product page. Add Article schema (it has none) and link it from the brewing guide, which already covers cold brew.

### 12. Structured data errors and gaps
| Page | Problem | Fix |
|---|---|---|
| `/coffee/bali-kintamani/` Product | **no `name`**, a required property, so ineligible for product rich results | add `"name": "Bali Kintamani natural coffee, 250g"` |
| `/coffee/java-ijen/` Product | valid but missing `sku`, `url`, `priceValidUntil`, shipping/return details | add `sku`, `url`, `hasMerchantReturnPolicy`, `shippingDetails` |
| `/coffee/flores-bajawa/` | no schema | see #10 |
| All 3 Articles | no `image`, no `publisher`, author has no `url`; also no `mainEntityOfPage` | add a 1200px image, `publisher` (Organization + logo), author profile URL |
| `/coffee/` FAQPage | markup is valid, but Google restricts FAQ rich results to well-known government and health sites, so no rich result will show. The FAQ content is also not visible on the page. | Show the Q&A as visible on-page text (markup must match visible content) or remove the schema; low value either way |
| Organization (home) | missing `sameAs` (Instagram, Google Business Profile), `contactPoint`; `logo.png` exists | add them |
| Sitewide | no `BreadcrumbList`, no `WebSite` | add breadcrumbs on blog and product pages |

### 13. Oversized and missing images
- `/assets/img/roastery-hero.jpg` is 1,818,123 bytes (1.8 MB), used at 2400×1600 on `/about/`. It is 100× the size of other images and is probably the LCP element. Resize to about 1600px wide, convert to WebP/AVIF (target under 200 KB), and use `srcset`.
- `/assets/img/hero-beans.jpg` on the **homepage has no `alt`** (crawl: "(missing)"). It is the homepage hero. Add descriptive alt ("Freshly roasted single-origin coffee beans from Bali"). It also has no `fetchpriority="high"` for LCP.
- Product images are all about 6.4 KB and almost identical in size (6405 / 6405 / 6404 bytes), which suggests placeholders. Check these aren't generic stand-ins before launch.
- No image has `loading="lazy"` (fine for the hero, add it below the fold). Width/height are set (good for CLS).

### 14. Sitemap hygiene
- Lists a 404 (`/coffee/sumatra-mandheling/`), a `noindex` page (`/wholesale/`) and a canonicalised page (`/shop/`). The sitemap should list only indexable, 200, self-canonical URLs. Fix per #2, #3 and #4.
- No `<lastmod>` on any entry. Add accurate lastmod dates (only change them for real edits). Blog posts carry `dateModified` in schema (2026-08-02, 2026-09-01), so the data exists.
- `/` is reachable at both `/` and `/index.html` (both return 200); `/about` redirects to `/about/` (good). Redirect `/index.html` to `/` or make sure the canonical covers it (the canonical does, so this is low risk).
- robots.txt does reference the sitemap, correctly.

### 15. Year-stamped title and URL on an evergreen post
- **URL:** `/blog/best-coffee-beans-2024/` titled "(2024 Guide)", yet last modified 2026-09-01. Today's date is October 2026.
- **Why it matters:** searchers and Google read "2024" as stale; it pulls CTR down (0.7% at position 11.4, 1,890 impressions). The URL carries the year, so renewing the title later means a redirect.
- **Fix:** retitle to "Best Coffee Beans in Bali (2026 Guide)" now, with the real update date visible on the page. Move to a year-free URL, `/blog/best-coffee-beans-bali/`, with a 301 from the old one, and update the Article schema headline (it already omits the year). The body says "Our picks this year" but names only one of your own products and one generic suggestion; add 3 to 5 real picks.

---

## Low priority

16. **`/about/` has no meta description** (crawl: length 0). Write one (about 150 chars) with "roastery in Ubud". Also lengthen the title: "About Kopi Kita: Our Roastery Story" has no location.
17. **Title and heading length/structure.**
    - `/coffee/bali-kintamani/` title is 88 characters (truncated at about 60): "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita". Shorten to "Bali Kintamani Natural Coffee Beans | Kopi Kita".
    - `/coffee/brewing-guide/` has **two H1s** ("Coffee brewing guide", "Brew methods"). Make the second an H2.
    - Meta descriptions are short on `/blog/cold-brew-at-home/` (83), `/blog/` (95) and `/contact/` (77). Lengthen toward 120 to 155 and add a call to action.
18. **`/contact/` has no canonical tag** (every other page does). Add a self-canonical.
19. **Thin pages:** `/blog/cold-brew-at-home/` (67 words), `/blog/` (43), `/contact/` (61), `/coffee/flores-bajawa/` (75), `/shop/` (86), `/visit/` (87). The homepage has only 132 words. Index and category pages can be short, but the homepage and `/coffee/` should say more about origins, process and delivery.
20. **Blog index** is a bare list of links: add dates, excerpts and the author, and pagination later. Blog pages show no visible author or publish date, though the schema has them (E-E-A-T). Add bylines linking to an author page for Wayan Sudarma (head roaster, per the about page).
21. **Internal linking depth:** blog posts have 1 to 2 inlinks each (only the blog index and one cross-link). Link from the homepage, product pages and the brewing guide. `/blog/best-coffee-beans-2024/` and the pour-over posts should link to the relevant product pages with descriptive anchors; "Kopi Kita Kintamani natural" is a good model.
22. **No `lang` alternates / hreflang:** single-language English site (`<html lang="en">` is present). Fine; no action unless you add Bahasa Indonesia, which could be worthwhile for the domestic market ("kopi" queries).
23. **AI crawlers:** robots.txt has no rules for GPTBot, ClaudeBot, PerplexityBot, Google-Extended and the like, so they are allowed by default. Make a deliberate decision and state it in robots.txt.
24. **Security and delivery headers (verify on production):** the local server sends none. On the live host check HTTPS with HSTS, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and `Cache-Control` on assets, and that `http://` and `www` variants 301 to the canonical https host.
25. **Branded-search strength is good; protect it.** "kopi kita" (412 clicks, 34.9% CTR, position 1.2) and the other branded queries produce about 69% of all clicks in the export. Non-brand traffic is the weak spot (everything outside the brand/visit queries averages below 1% CTR). This is why #1, #8 and #11 matter most.

---

## Things that are working
- All indexable pages have a unique, in-range title (bar #9), a self-referencing absolute https canonical (bar #18) and a viewport tag; `lang="en"` is set.
- Clean, readable URLs with trailing-slash consistency; the sitemap is valid XML and declared in robots.txt.
- Product images mostly have descriptive alt text and explicit width/height.
- Good commercial copy on product pages (tasting notes, process, price). Product pages have JSON-LD with price in IDR.
- No JavaScript dependency, so there is no rendering risk.

## Recommended order of work
1. **Week 1 (S effort):** #2, #3 decision, #4, #5, #6, #14 (sitemap), #16, #17, #18, #9. All are template or config edits.
2. **Weeks 2 to 3:** #1 merge, #7, #10, #12 schema, #13 images.
3. **Weeks 3 to 6:** #8 snippet and content work, #11 cold brew rewrite, #15 retitle/move.
4. **Then:** re-crawl, resubmit the sitemap in Search Console, and compare the 22 Jul to 21 Oct baseline (about 830 clicks in this export) against the next 90 days, with the pour-over cluster (about 8,800 impressions) as the headline metric.
