# Technical SEO Audit: Kopi Kita (https://kopikita.test/)

Date: 2026-10-22
Data source: Fetched with curl from the local build at http://localhost:8765/ (no rendered crawl, no Search Console data)
Pages analysed: 18 sitemap URLs, plus `/menu/`, `/cafe/`, `/cart/`, `/index.html`, `/coffee`, `/favicon.ico` and the key assets. The site is small enough that every internal link was read.

**Not assessable from this data:** orphans beyond the link graph below, Core Web Vitals, real keyword cannibalisation (needs GSC), HTTPS and mixed content (local HTTP only), hreflang (none used), and rendering of JS (the pages are static HTML with no JS).

All "production" findings assume the localhost build matches kopikita.test.

---

## CRITICAL (fix this week)

### 1. `/wholesale/` is `noindex` but is in the sitemap and the main nav
- **URL:** https://kopikita.test/wholesale/
- **Evidence:** `<meta name="robots" content="noindex, follow">`; listed in sitemap.xml; linked from every page's nav and from the home page.
- **Why it matters:** The page is a lead-generation page (30+ cafes and hotels served) and the title and description are written to rank for wholesale queries. It can't rank while it is noindexed. The sitemap also sends Google contradictory signals.
- **Fix:** If the page is meant to rank, remove the `noindex` tag. If the noindex is deliberate, remove it from the sitemap and say so, but the page's copy suggests it was left over from staging.

### 2. `/shop/` canonicalises to `/coffee/`
- **URL:** https://kopikita.test/shop/
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/">`, yet `/shop/` is in the sitemap and in the nav with its own title, description and H1.
- **Why it matters:** Google is told `/shop/` is a duplicate of `/coffee/` and will usually drop it from the index. The shop page covers gear and drip bags that `/coffee/` doesn't, so those queries have no indexable page.
- **Fix:** Make the canonical self-referencing (`https://kopikita.test/shop/`). Then differentiate it from `/coffee/` (see issue 8).

### 3. A 404 page is in the sitemap, and blog posts link to 404s
- **URLs affected:**
  - `/coffee/sumatra-mandheling/`: returns 404 and is listed in sitemap.xml.
  - `/coffee/aceh-gayo/`: returns 404 and is linked from https://kopikita.test/blog/how-to-brew-pour-over/.
- **Why it matters:** Sitemap 404s waste crawl budget and make the sitemap untrustworthy in Search Console. The broken link sits in a body paragraph of a content page, where it loses the reader and the link equity.
- **Fix:** Remove `sumatra-mandheling` from the sitemap, or publish the page if the coffee exists. Replace the Aceh Gayo link with a live product (e.g. `/coffee/bali-kintamani/`) or publish the page. Also serve a real branded 404 page (the current one is the default Python error page).

---

## HIGH (fix this month)

### 4. Duplicate title tag on two commercial pages
- **URLs:** https://kopikita.test/coffee/ and https://kopikita.test/subscriptions/
- **Evidence:** Both are titled "Single-Origin Indonesian Coffee | Kopi Kita". The subscriptions page has a copied title that says nothing about subscriptions.
- **Why it matters:** The subscription page won't win subscription queries, and the two pages compete for the same snippet.
- **Fix:** Retitle `/subscriptions/`, e.g. "Coffee Subscription: Fresh Beans Every 2 or 4 Weeks | Kopi Kita".

### 5. Two blog posts target the same query (cannibalisation risk)
- **URLs:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Evidence:** Both give the same recipe (15g, 250g, 93C, 40g bloom, 3 minutes), have near-identical H1s and both link to the same coffee. Both are indexable and in the sitemap. I couldn't check GSC, so this is a risk and not a measured split.
- **Why it matters:** Two pages for one intent split links and clicks, and Google may keep switching which one it shows.
- **Fix:** Pick one winner (the `how-to-brew-pour-over` post is longer and has been updated more recently). Merge anything unique from the other (dripper and filter advice) into it, 301 the loser to it, and remove the loser from the sitemap and the blog index. Then check GSC for the shared queries before and after.

### 6. Internal links and nav point at a redirect chain
- **URL:** https://kopikita.test/menu/ (the "Visit the cafe" link in the nav on every page)
- **Evidence:** `/menu/` → 301 `/cafe/` → 301 `/visit/` → 200. The sitemap lists `/visit/`.
- **Why it matters:** Two hops on a sitewide link waste crawl budget and slow users, and the sitewide link never points at the canonical URL.
- **Fix:** Change the nav href to `/visit/` and 301 `/menu/` and `/cafe/` straight to `/visit/` in a single hop.

### 7. `/coffee/flores-bajawa/` has no internal links (orphan)
- **URL:** https://kopikita.test/coffee/flores-bajawa/
- **Evidence:** It is in the sitemap, but no page links to it. `/coffee/` and `/shop/` list only Kintamani and Ijen. This is the only way I could find it, so it is orphaned by link graph.
- **Why it matters:** Orphans get little crawl priority and no link equity, and visitors can't find a product that is for sale.
- **Fix:** Link it from `/coffee/`, `/shop/` and the home page's coffee blurb, and from a relevant blog post.

### 8. `/visit/` page has no H1
- **URL:** https://kopikita.test/visit/
- **Evidence:** The page has only `<h2>Opening hours</h2>` and `<h2>Menu</h2>`.
- **Why it matters:** It is the local-intent page for the cafe and has no primary heading to confirm its topic.
- **Fix:** Add `<h1>Visit our roastery cafe in Ubud</h1>`. Also add LocalBusiness/CafeOrCoffeeShop schema with hours (see issue 13).

### 9. Product schema errors on product pages
- **URLs:**
  - https://kopikita.test/coffee/bali-kintamani/: the Product JSON-LD has no `name`, which Google requires.
  - https://kopikita.test/coffee/flores-bajawa/: no Product schema at all.
  - https://kopikita.test/coffee/java-ijen/: has `name`, price and availability, which is valid. It could add `sku`, `aggregateRating` or `review` if real ones exist.
- **Why it matters:** Without a `name` the Kintamani markup is invalid and is not eligible for product rich results.
- **Fix:** Add `"name": "Bali Kintamani natural coffee, 250g"` to Kintamani. Add a Product block to Flores Bajawa (price 155000 IDR, image `/assets/img/bajawa.jpg`). Add `priceValidUntil` and `url` to all three if you want to be thorough.

---

## MEDIUM (roadmap)

### 10. Missing meta description and canonical on two pages
- **https://kopikita.test/about/**: no meta description (the title "About Kopi Kita: Our Roastery Story" is fine).
- **https://kopikita.test/contact/**: no canonical tag (it has a title and description).
- **Fix:** Write a description for About (~150 chars). Add a self-referencing canonical to Contact.

### 11. Brewing guide has two H1s
- **URL:** https://kopikita.test/coffee/brewing-guide/
- **Evidence:** `<h1>Coffee brewing guide</h1>` and later `<h1>Brew methods</h1>`.
- **Fix:** Change the second to an `<h2>`.

### 12. Oversized title and stale year in URLs
- **https://kopikita.test/coffee/bali-kintamani/**: the title is 78 characters ("Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita") and will be truncated. Trim to ~55 chars: "Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita".
- **https://kopikita.test/blog/best-coffee-beans-2024/**: the URL, title and H1 say 2024 but the post was updated 2026-09-01 and says "Our picks this year". The dated slug looks stale in 2026. Retitle to drop the year (or update to 2026) and 301 to an undated slug. Don't change the URL without the redirect.

### 13. Schema gaps and low-value schema
- **Home** has Organization with a logo and address. Valid. The logo URL (`/assets/img/logo.png`) returns 200.
- **/coffee/** has FAQPage markup. FAQ rich results are now only shown for well-known government and health sites, so it won't produce a rich result. It is harmless; keep it only if the FAQ is visible on the page. Neither question is visible in the page body I fetched, so either show the FAQ on the page or remove the markup (markup must match visible content).
- **Blog Articles** have no `image`, `publisher` or `mainEntityOfPage`. The `cold-brew-at-home` post has no Article schema.
- **/visit/** and **/contact/**: add LocalBusiness / CafeOrCoffeeShop schema (address, hours 07:00-17:00, phone, geo).

### 14. Images
- https://kopikita.test/ : the hero image `/assets/img/hero-beans.jpg` has no `alt` text.
- https://kopikita.test/about/ : `/assets/img/roastery-hero.jpg` is 1.8 MB at 2400×1600. Resize and compress to under ~250 KB and serve WebP/AVIF with `srcset`. Hero images that are the LCP element should not be lazy-loaded.

### 15. robots.txt and sitemap housekeeping
- robots.txt disallows `/assets/css/`. Google needs CSS to render the page. Remove this rule.
- `/cart/` is disallowed but returns 404 on this build. Fine if the cart lives elsewhere in production, otherwise remove.
- sitemap.xml has no `<lastmod>`. Add accurate lastmod values.
- No favicon: `/favicon.ico` returns 404, and there is no `<link rel="icon">`. Add one.

### 16. Duplicate URL variants
- `/index.html` returns 200 with the same content as `/` (the canonical tag does point to `/`, so risk is low). Better to 301 `/index.html` to `/`.
- `/?utm=x` also returns 200; the self-referencing canonical on the home page handles this.

### 17. Thin pages and weak internal linking from the cold-brew post
- https://kopikita.test/blog/cold-brew-at-home/ is one paragraph (~70 words), well under the rest of the blog, and has no Article schema. Expand it (ratios, steeping time, dilution, storage) or merge it into the brewing guide's cold brew section.
- Blog posts link to products, but products rarely link back to the blog or to each other. Add related links (Ijen ↔ pour-over post, Kintamani ↔ best beans post, Flores from `/coffee/`).

---

## TOP 5 QUICK WINS

1. Remove `noindex` from `/wholesale/` (one meta tag). **Impact: High.**
2. Change the `/shop/` canonical to itself. **Impact: High.**
3. Remove `/coffee/sumatra-mandheling/` from sitemap.xml and fix the `/coffee/aceh-gayo/` link in the pour-over post. **Impact: Medium.**
4. Retitle `/subscriptions/` and point the nav at `/visit/` instead of `/menu/`. **Impact: Medium.**
5. Link `/coffee/flores-bajawa/` from `/coffee/` and `/shop/`, and add `name` to the Kintamani Product schema. **Impact: Medium.**

## WHAT'S WORKING (leave alone)

- Every indexable page I checked returns 200 with a unique self-referencing canonical, except the ones listed above.
- Titles and meta descriptions exist and are unique on almost every page (the exceptions are listed above), with good lengths.
- Clean, readable URLs with trailing slashes, and `/coffee` correctly 301s to `/coffee/`.
- The site is plain static HTML, so all content and links are crawlable without JS.
- Organization schema on the home page and the Java Ijen Product schema are valid.
- Product and about images have descriptive alt text and explicit width/height (no layout shift).
- Content is original and specific (origins, altitudes, processes, prices).
- robots.txt declares the sitemap, and the sitemap is valid XML.

## BOTTOM LINE

Three pages that should earn revenue, `/wholesale/` (noindex), `/shop/` (canonicalised to `/coffee/`) and `/coffee/flores-bajawa/` (orphan), are being kept out of or hidden from Google by small, fixable tags and links, and fixing those makes them eligible to rank.
