# SEO Audit: Kopi Kita (kopikita.test)

Method: crawled the local copy at http://localhost:8765/ with curl. I fetched every URL in the sitemap, the URLs linked from the pages, robots.txt, and a few images. Production URLs below use the kopikita.test domain.

Limits: I had no Search Console, analytics, PageSpeed or real-device data. I did not measure Core Web Vitals, HTTPS, HSTS, redirects from http or www, or compression, because the local server is plain HTTP (Python SimpleHTTP). JSON-LD was visible in the static HTML, so the schema findings below come from the source. I did not validate them in the Rich Results Test.

## Executive summary

The site is small (about 18 pages) and mostly clean. The titles, metas and canonicals are good on most pages. The serious problems are all in indexation and canonicals:

1. **Two money pages canonicalise to other URLs.** `/subscriptions/` canonicalises to `/coffee/` and `/shop/` canonicalises to `/coffee/`. Google will likely drop both from the index.
2. **`/wholesale/` is `noindex`** but sits in the sitemap and is the B2B lead page.
3. **Broken internal links.** The nav's "Visit the cafe" link goes through a redirect chain. The pour-over post links to a 404 (`/coffee/aceh-gayo/`).
4. **The sitemap lists a 404** (`/coffee/sumatra-mandheling/`).
5. **Two blog posts compete for the same query** (pour over).

Quick wins: fix the two canonicals, remove `noindex`, fix the 404 sitemap entry and the broken links, add the missing title and description tags. All of these are small template edits.

---

## Priority 1: critical (blocking indexation or ranking)

### 1. `/subscriptions/` canonicalises to `/coffee/` and has a duplicate title
- **URL:** https://kopikita.test/subscriptions/
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/">` (not self-referencing). The `<title>` is `Single-Origin Indonesian Coffee | Kopi Kita`, identical to `/coffee/`. The H1, description and content are about subscriptions.
- **Why it matters:** The canonical tells Google this page is a duplicate of `/coffee/`. The subscriptions page will probably be dropped from the index, so it can't rank for "coffee subscription Bali" and similar queries. The copied title makes it worse.
- **Fix:** Set the canonical to `https://kopikita.test/subscriptions/`. Give it its own title, for example `Coffee Subscription in Bali: Fresh Beans Every 2 or 4 Weeks | Kopi Kita`.
- *Note:* the canonical and the title look like a template copy and paste from `/coffee/`. The canonical value actually shown is `/coffee/`; I could not tell whether it is a CMS default. Check how the template builds it.

### 2. `/shop/` canonicalises to `/coffee/`
- **URL:** https://kopikita.test/shop/
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/">`. The title and description are unique to the shop.
- **Why it matters:** Same effect as above: the shop page is treated as a duplicate and is unlikely to be indexed or rank for "buy coffee beans" queries. The page is also very thin (see issue 12).
- **Fix:** Self-canonical to `/shop/`. If `/shop/` and `/coffee/` genuinely overlap, decide which one is the primary category page and 301 the other, rather than using a canonical.

### 3. `/wholesale/` is set to `noindex`
- **URL:** https://kopikita.test/wholesale/
- **Evidence:** `<meta name="robots" content="noindex, follow">`. The page is in the sitemap, is in the main nav, has a keyword-targeted title and is the page for the cafe and hotel segment.
- **Why it matters:** The page can't appear in search at all, so queries like "wholesale coffee Bali" can't reach it. The sitemap and the noindex tag also send conflicting signals.
- **Fix:** Remove the `noindex` tag unless it was intentional (for example a staging leftover). If it is intentional, remove the page from the sitemap and say so in the docs.

### 4. Sitemap contains a 404 URL
- **URL:** https://kopikita.test/coffee/sumatra-mandheling/ (listed in `sitemap.xml`)
- **Evidence:** returns HTTP 404. It is also the last entry, out of order with the rest of the list, which suggests it was added by hand.
- **Why it matters:** The sitemap should contain only live, indexable URLs. Errors waste crawl budget and show as "Submitted URL not found (404)" in Search Console.
- **Fix:** Remove it, or publish the page if it is a planned product. Generate the sitemap automatically so it can't drift.

### 5. Broken internal link: `/coffee/aceh-gayo/` returns 404
- **URL affected:** https://kopikita.test/blog/how-to-brew-pour-over/ (links to `/coffee/aceh-gayo/`)
- **Evidence:** the link is in the body copy ("try our Aceh Gayo"). The target returns 404.
- **Why it matters:** A dead link in an article that has real traffic potential. It wastes link equity and sends users to an error page.
- **Fix:** Create the Aceh Gayo product page, or point the link at an existing coffee (for example `/coffee/bali-kintamani/`, which is the "heavier" option) and remove the sentence if there's no such product.

### 6. Navigation link goes through a redirect chain: `/menu/` → `/cafe/` → `/visit/`
- **URL affected:** every page (the "Visit the cafe" nav link points to `/menu/`)
- **Evidence:** `/menu/` returns 301 to `/cafe/`, which returns 301 to `/visit/`. The sitemap and canonical use `/visit/`.
- **Why it matters:** Every page carries a site-wide link that costs two redirects. Chains dilute link signals and slow users. The nav should point at the final URL.
- **Fix:** Change the nav link to `/visit/`. Point `/menu/` and `/cafe/` straight at `/visit/` with single 301s.

---

## Priority 2: high-impact improvements

### 7. Two pour-over articles target the same query (cannibalisation)
- **URLs:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Evidence:** titles "How to Brew Pour Over Coffee at Home" and "Pour Over Coffee Guide for Beginners"; near-identical intent (a recipe for pour over coffee for beginners). The blog index links them one after the other.
- **Why it matters:** The two pages split relevance and links for the same search intent, and Google may alternate between them or rank neither well.
- **Fix:** Pick one as the main pour-over page. Either merge the second into the first and 301 it, or differentiate them clearly (a step-by-step recipe versus a gear and mistakes page) with distinct titles and H1s, and link from the guide to the recipe with descriptive anchor text. The main `/coffee/brewing-guide/` page also overlaps and should link to whichever is primary.

### 8. Pages missing a meta description or canonical
- **URL `/about/`:** has a title and canonical but **no meta description**.
- **URL `/contact/`:** has a title and description but **no canonical** tag.
- **Why it matters:** Without a description Google writes its own snippet, which usually performs worse. Missing canonicals leave duplicate-URL handling (parameters, trailing slash) to chance.
- **Fix:** Add a unique description of about 150 to 160 characters to `/about/` (for example: roastery story, founded 2019, direct trade with farmer groups). Add `<link rel="canonical" href="https://kopikita.test/contact/">`. Make the canonical part of the base template so every page gets one.

### 9. Product schema is incomplete or invalid
- **URLs:** https://kopikita.test/coffee/bali-kintamani/ and https://kopikita.test/coffee/java-ijen/
- **Evidence:**
  - Kintamani `Product` JSON-LD has **no `name`** property (a required field) and no `sku`/rating/review.
  - Java Ijen has a name but no `sku`, and `offers` has no `url` or `priceValidUntil`.
  - `/coffee/flores-bajawa/` has **no Product schema at all**, though it has a price (Rp 155,000) on the page.
  - The Kintamani schema price is 145000 but I could not see the price in the visible page text; check the visible price matches the markup. The Flores page shows prices in visible text with no schema, so the reverse problem.
- **Why it matters:** A Product without a name is not eligible for product rich results. Rich results (price, availability) improve click-through for product queries.
- **Fix:** Add `name` to Kintamani and add Product markup to Flores Bajawa with name, image, description, brand, offers (price, currency, availability, url). Make sure the visible price matches. Test every product URL in the Rich Results Test.

### 10. FAQPage schema on `/coffee/` has no matching visible FAQ
- **URL:** https://kopikita.test/coffee/
- **Evidence:** the page source contains a `FAQPage` with two questions (freshness and shipping), but the visible page content has no FAQ section.
- **Why it matters:** Structured data should reflect content users can see. Marking up hidden content risks a manual action for misleading markup, and Google now shows FAQ rich results only for a few authoritative sites, so the upside is small.
- **Fix:** Either add a visible FAQ section with those questions and answers, or remove the markup. Adding the FAQ as visible content is also useful for users.

### 11. Duplicate H1s and missing H1 on key pages
- **`/coffee/brewing-guide/`:** two H1 tags ("Coffee brewing guide" and "Brew methods"). The second should be an H2, and the sections under it (grind size, water temperature, troubleshooting) are bold paragraph labels that should be H2/H3 headings.
- **`/visit/`:** **no H1**, only H2s ("Opening hours", "Menu"). Add `<h1>Visit our roastery cafe in Ubud</h1>`.
- **Why it matters:** Headings tell search engines what a page is about and how its sections relate. This is the page type that most often gets featured-snippet and jump-link treatment.
- **Fix:** One H1 per page, then H2s for sections and H3s for sub-points.

### 12. Thin pages
- **`/shop/`:** one sentence with two links, about 20 words of body copy. For a page meant to rank for "buy coffee beans" it has no product listing, no prices and no descriptions.
- **`/coffee/flores-bajawa/`:** reasonable text but not linked from `/coffee/`, `/shop/` or the homepage (see issue 14).
- **`/coffee/` category page:** short blurbs for only two of the three coffees.
- **`/blog/cold-brew-at-home/`:** one short paragraph (about 60 words); no headings, no author, no dates, no Article schema, and the same recipe is already on `/coffee/brewing-guide/`.
- **Why it matters:** Thin pages rarely rank and can pull down the site's perceived quality.
- **Fix:** Make `/shop/` a real category page with every product, price, short description and a link. Flesh out the cold brew post (equipment, ratio table, steeping time options, serving ideas, FAQ) or merge it into the brewing guide.

### 13. Over-long title tag on the Kintamani product page
- **URL:** https://kopikita.test/coffee/bali-kintamani/
- **Evidence:** `Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita` is about 90 characters.
- **Why it matters:** Google truncates around 60 characters (about 600px), so the brand and the tail would be cut and Google may rewrite it.
- **Fix:** Shorten to something like `Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita` (about 52 characters).

---

## Priority 3: medium

### 14. Orphan and weakly linked pages
- `/coffee/flores-bajawa/` is in the sitemap but no page on the site links to it. `/coffee/` and `/shop/` list only Kintamani and Ijen.
- `/coffee/brewing-guide/` is linked from the homepage and product pages but not from the nav.
- `/about/` and `/contact/` are in the nav and the footer, which is fine. `/wholesale/` is only reachable from the nav and homepage.
- **Fix:** Link every product from `/coffee/`, `/shop/` and the homepage. Add the third coffee to the "best sellers" copy. Consider a "Brewing guide" link in the footer.

### 15. Oversized image on `/about/`
- **URL:** https://kopikita.test/assets/img/roastery-hero.jpg (used on `/about/`)
- **Evidence:** 1.8 MB, 2400×1600 JPEG. The other images I checked are small (the homepage hero is about 14 KB).
- **Why it matters:** A 1.8 MB hero will slow LCP on mobile, especially in Bali and elsewhere in Indonesia where connections vary. Speed is a ranking and conversion factor.
- **Fix:** Resize to the largest displayed width (about 1200px for desktop), convert to WebP/AVIF, serve responsive `srcset` sizes and compress to under about 200 KB. Add `fetchpriority="high"` for a hero above the fold, and `loading="lazy"` for below-the-fold images.

### 16. Homepage hero image has no alt text
- **URL:** https://kopikita.test/ (`/assets/img/hero-beans.jpg`)
- **Evidence:** `<img src="/assets/img/hero-beans.jpg" width="1200" height="700">` with no `alt`. All other images I checked have alt text.
- **Fix:** Add descriptive alt text, for example `Freshly roasted single-origin coffee beans from Indonesia`. Also rename generic files where practical.

### 17. Stale year in a title and H1
- **URL:** https://kopikita.test/blog/best-coffee-beans-2024/
- **Evidence:** the URL, title and H1 say 2024, but the page was modified 2026-09-01 and the text says "our picks this year". The Article schema `headline` omits the year, which is inconsistent. The page recommends a competitor ("a washed Kintamani from any good local roaster").
- **Why it matters:** An old year in the title looks out of date to searchers and lowers click-through. Changing the URL later means a redirect.
- **Fix:** Drop the year from the title, H1 and URL (301 `/blog/best-coffee-beans-2024/` to `/blog/best-coffee-beans-bali/`), or update it to the current year consistently. Keep the page evergreen and update `dateModified` only on real changes.

### 18. Article schema gaps
- **URLs:** the three Article pages have `datePublished`, `dateModified` and an author but no `image`, no `publisher`, and no `mainEntityOfPage`. The cold brew post has no Article schema at all.
- The pour-over post's `dateModified` (2026-08-02) and the visible text should agree; I could not see a visible date on any post.
- **Fix:** Add `image`, `publisher` (the Organization) and a visible byline and date on each post. Add schema to the cold brew post.

### 19. Organization/LocalBusiness schema
- **URL:** https://kopikita.test/ (Organization JSON-LD)
- **Evidence:** the homepage has an Organization with address, but no phone, `sameAs` profiles, opening hours or geo coordinates. The business has a physical cafe in Ubud.
- **Fix:** Use `CafeOrCoffeeShop` / `LocalBusiness` (a subtype of Organization) with telephone (+62 812 0000 0000), openingHours (daily 07:00 to 17:00), geo and `sameAs`. Put it on `/visit/` and `/contact/` as well. Make sure the name, address and phone match exactly across the footer, contact page, schema and Google Business Profile.

---

## Priority 4: low and housekeeping

### 20. robots.txt
- **Evidence:** `Disallow: /assets/css/` and `Disallow: /cart/`. Sitemap is declared.
- **Issue:** Blocking CSS stops Google from rendering the pages properly, which can hurt mobile-friendliness evaluation. `/cart/` returns 404 on the local site, so that rule is currently pointless.
- **Fix:** Remove the `/assets/css/` rule. Keep `/cart/` only if a cart exists in production (also consider `/checkout/` and `/account/`).

### 21. Sitemap has no `lastmod`
- **Evidence:** every `<url>` has only `<loc>`.
- **Fix:** Add accurate `<lastmod>` values, generated automatically from content changes. Don't set every page to today's date.

### 22. Title tag details
- `/about/` title `About Kopi Kita: Our Roastery Story` has no location or keyword (fine for a brand page, though "specialty roaster in Ubud, Bali" would help).
- The `/coffee/` and `/subscriptions/` titles are identical (see issue 1). Every other title is unique and within about 60 characters except Kintamani (issue 13).
- Homepage title is good (`Kopi Kita | Specialty Coffee Roasted in Ubud, Bali`).

### 23. Content and E-E-A-T opportunities
- Posts are authored by a named person (Wayan Sudarma) but there is no author page or bio. Add one linked from each byline, using the credentials already on `/about/` (trained in Melbourne, twelve years roasting).
- `/about/` and `/contact/` have contact and ownership details, which is good for trust. Add a privacy policy and shipping/returns pages if the shop takes orders; I found none linked.
- Add an embedded map, photos and review links on `/visit/`, and create or claim the Google Business Profile for local pack visibility ("coffee Ubud").
- The site targets Bali/Indonesia but is only in English. If Indonesian-language search is a goal, consider `/id/` pages with hreflang. Not necessary otherwise.
- Content gaps to consider: individual origin guides, "how to choose coffee beans", espresso and French press recipes (each linking to the products), and a glossary.

### 24. Items I could not check
- Core Web Vitals, TTFB, caching headers and compression (local server only).
- HTTPS, certificate, HTTP-to-HTTPS and www redirects, HSTS (the production domain isn't reachable).
- Trailing-slash consistency on production, and index status in Google.
- Whether the JSON-LD I saw in the HTML is the only schema (nothing is injected by JavaScript that I can see, but I did not render the pages).

---

## Prioritised action plan

**Do first (critical, about an hour of template work):**
1. Self-canonical `/subscriptions/` and `/shop/`; give `/subscriptions/` its own title.
2. Remove `noindex` from `/wholesale/`.
3. Remove `/coffee/sumatra-mandheling/` from the sitemap (or publish it).
4. Fix the nav link `/menu/` to `/visit/`; collapse the redirect chain.
5. Fix or remove the `/coffee/aceh-gayo/` link.

**Then (high impact):**
6. Resolve the pour-over cannibalisation.
7. Add `/about/` description and `/contact/` canonical; make both template defaults.
8. Fix Product schema (name on Kintamani; add Flores Bajawa); fix or remove the FAQ markup.
9. Fix headings on `/coffee/brewing-guide/` and `/visit/`.
10. Build out `/shop/` and the cold brew post.
11. Shorten the Kintamani title.

**Quick wins:**
12. Alt text on the homepage hero. Compress the 1.8 MB about image.
13. Remove the CSS block from robots.txt. Add `lastmod` to the sitemap.
14. Link Flores Bajawa from `/coffee/`, `/shop/` and the homepage.

**Longer term:**
15. Evergreen the "2024" post, add author pages, LocalBusiness schema and Google Business Profile, and extend the blog with a keyword map so posts don't compete.
16. After deployment, run Search Console (coverage, sitemap, Core Web Vitals) and PageSpeed Insights on production and re-audit.
