# Technical SEO Audit: Kopi Kita (kopikita.test)

> Audit date 2026-10-22 · Source: local site at http://localhost:8765/ · 18 URLs in the sitemap plus every internally linked URL, fetched with curl.

## Scope and limits

- **Not available in this session:** SE Ranking audit data, Firecrawl, Google Search Console, CrUX and PageSpeed. This is a manual crawl of raw HTML, headers and status codes only. Nothing here comes from SE Ranking's health score or from field data.
- **Not needed:** the pages contain no JavaScript, so JS-render checks (canonical drift, soft-404s) do not apply.
- **Dev-server caveat:** the site is served by Python's `SimpleHTTP/0.6`. Missing security headers, compression and caching headers are noted, but they may be set at the production edge. Verify them on production before acting.
- **URLs:** canonicals and the sitemap use `https://kopikita.test/`. All URLs below are shown as paths.

## Summary

| Severity | Count |
|---|---|
| Critical | 3 |
| High | 5 |
| Medium | 9 |
| Low | 7 |

Pages crawled: 22 URLs requested, 18 returned 200. Four were not served as 200: `/coffee/sumatra-mandheling/` (404), `/coffee/aceh-gayo/` (404), `/menu/` (301) and `/cafe/` (301).

## Priority fix list

| # | Issue | Severity | URL(s) | Effort |
|---|---|---|---|---|
| 1 | `/shop/` canonicalised to `/coffee/` | Critical | `/shop/` | S |
| 2 | `/wholesale/` is `noindex` but in the sitemap and main nav | Critical | `/wholesale/` | S |
| 3 | Sitemap lists a 404 page | Critical | `/coffee/sumatra-mandheling/` | S |
| 4 | Sitewide nav link to `/menu/` goes through a 2-hop redirect chain | High | every page | S |
| 5 | Broken internal link to a 404 | High | `/blog/how-to-brew-pour-over/` → `/coffee/aceh-gayo/` | S |
| 6 | Flores Bajawa product page is an orphan | High | `/coffee/flores-bajawa/` | S |
| 7 | `robots.txt` blocks `/assets/css/` | High | `/robots.txt` | S |
| 8 | Duplicate title across two different pages | High | `/coffee/`, `/subscriptions/` | S |
| 9 | Two near-duplicate pour-over posts compete | Medium | `/blog/how-to-brew-pour-over/`, `/blog/pour-over-coffee-guide/` | M |
| 10 | Heading structure errors (no H1 / two H1s) | Medium | `/visit/`, `/coffee/brewing-guide/` | S |
| 11 | Missing canonical | Medium | `/contact/` | S |
| 12 | Missing meta description | Medium | `/about/` | S |
| 13 | Structured data errors and gaps | Medium | `/coffee/bali-kintamani/`, `/coffee/flores-bajawa/`, `/coffee/`, `/visit/`, blog posts | M |
| 14 | 1.8 MB hero image, no responsive sizing | Medium | `/about/` | S |
| 15 | Year in URL and title of an evergreen post | Medium | `/blog/best-coffee-beans-2024/` | M |
| 16 | Overlong product title | Medium | `/coffee/bali-kintamani/` | S |
| 17 | Thin content | Medium | `/blog/cold-brew-at-home/`, `/shop/`, `/coffee/flores-bajawa/` | M |
| 18 | No Open Graph or Twitter tags anywhere | Medium | all pages | S |
| 19 | Missing alt text and image attributes | Low | `/` | S |
| 20 | No favicon | Low | `/favicon.ico` | S |
| 21 | Security headers absent (verify on production) | Low | all pages | S |
| 22 | Sitemap has no `lastmod` | Low | `/sitemap.xml` | S |
| 23 | Default, unbranded 404 page | Low | any 404 | S |
| 24 | No internal links from blog to products, and no cross-linking between posts | Low | blog posts | S |
| 25 | Brewing guide lives under the `/coffee/` product folder | Low | `/coffee/brewing-guide/` | M |

---

## Critical

### 1. `/shop/` canonicalises to `/coffee/`
- **URL:** `/shop/`
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/">`. The page is in the sitemap with its own title, description and unique content (gear, drip bags, free-shipping threshold).
- **Why it matters:** Google treats `/shop/` as a duplicate of `/coffee/` and is likely to drop it from the index. The page covers different content (gear and drip bags), so it can't rank for those searches. The sitemap also contradicts the canonical.
- **Fix:** Change the canonical to `https://kopikita.test/shop/`. If `/shop/` is meant to be merged into `/coffee/`, 301 redirect it and remove it from the sitemap and nav.

### 2. `/wholesale/` is `noindex` but listed in the sitemap and main nav
- **URL:** `/wholesale/`
- **Evidence:** `<meta name="robots" content="noindex, follow">`. The page is in `sitemap.xml`, linked from the nav on every page and from the homepage body.
- **Why it matters:** A B2B lead-generation page with commercial intent ("wholesale coffee Bali", "coffee supplier for cafes") is blocked from search. Sitemap and noindex also send Google conflicting signals, which Search Console reports as "Submitted URL marked noindex".
- **Fix:** If the page should rank, which is likely given the copy, remove the `noindex` tag. If it should stay private, remove it from the sitemap and keep `noindex`. Check whether the tag was left over from staging.

### 3. Sitemap lists a URL that returns 404
- **URL:** `/coffee/sumatra-mandheling/` (listed in `/sitemap.xml`)
- **Evidence:** `HTTP/1.0 404 File not found`.
- **Why it matters:** Dead URLs in the sitemap waste crawl budget and lower Google's trust in the file.
- **Fix:** Remove the entry. If a Sumatra Mandheling page is planned, publish it first, then add it. Generate the sitemap from the live routes so it can't drift.

---

## High

### 4. Sitewide nav link to `/menu/` goes through a redirect chain
- **URL:** every page (nav link "Visit the cafe" → `/menu/`)
- **Evidence:** `/menu/` → 301 → `/cafe/` → 301 → `/visit/` (200). The sitemap and canonical use `/visit/`. No page links to `/visit/` in the nav. Only `/about/` links to it in the body.
- **Why it matters:** The nav is the strongest internal-link signal on the site. It currently points at a redirecting URL through two hops, which dilutes link equity and slows users. The cafe page is among the most useful pages for local intent.
- **Fix:** Change the nav href to `/visit/`. Collapse the old redirects into single 301s (`/menu/` → `/visit/` and `/cafe/` → `/visit/`).

### 5. Broken internal link to a 404 page
- **URL:** `/blog/how-to-brew-pour-over/` links to `/coffee/aceh-gayo/` (404)
- **Evidence:** "If you like it heavier, try our Aceh Gayo" links to a page that doesn't exist. The shop sells no Aceh Gayo, only Kintamani, Ijen and Flores.
- **Why it matters:** Visitors who click it reach a dead end, which hurts conversion and the quality signal of an article that gets traffic.
- **Fix:** Link to a real product (`/coffee/bali-kintamani/` or `/coffee/flores-bajawa/`), or remove the sentence.

### 6. Orphan product page: `/coffee/flores-bajawa/`
- **URL:** `/coffee/flores-bajawa/`
- **Evidence:** No crawled page links to it. It appears only in `sitemap.xml`. `/coffee/` and `/shop/` list only Kintamani and Ijen.
- **Why it matters:** A product with no internal links gets little crawl priority and no link equity, and shoppers can't find it.
- **Fix:** Add it to the `/coffee/` listing, `/shop/`, the homepage, and relevant blog posts. Product pages should link to each other ("You may also like").

### 7. `robots.txt` blocks `/assets/css/`
- **URL:** `/robots.txt` (`Disallow: /assets/css/`)
- **Evidence:** Every page loads `/assets/css/site.css`.
- **Why it matters:** Googlebot needs CSS to render the page and judge mobile-friendliness and layout. Blocking it can produce a "page unrendered" or unfriendly-layout assessment.
- **Fix:** Delete the `Disallow: /assets/css/` line. `/cart/` can stay disallowed, though it currently returns 404.

### 8. Duplicate title across different pages
- **URLs:** `/coffee/` and `/subscriptions/`
- **Evidence:** Both use `Single-Origin Indonesian Coffee | Kopi Kita`. Their descriptions and content differ.
- **Why it matters:** Identical titles make the pages compete and give Google no way to tell them apart. The subscriptions page has no title targeting its own searches.
- **Fix:** Retitle `/subscriptions/`, for example `Coffee Subscription: Fresh Single-Origin Beans Delivered | Kopi Kita`.

---

## Medium

### 9. Two near-duplicate pour-over posts compete
- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Evidence:** Same recipe (15g / 250g / 93C / 40g bloom), same advice, same product link (Java Ijen), same keyword target.
- **Why it matters:** The posts cannibalise each other, so neither ranks as well as one stronger page would. A third overlapping page, `/coffee/brewing-guide/`, adds to this.
- **Fix:** Merge the best material into one post (the longer `how-to-brew-pour-over`), 301 the other to it, and drop it from the sitemap. If both stay, differentiate them: one beginner gear guide, one step-by-step recipe.

### 10. Heading structure errors
- **URLs:** `/visit/` has no `<h1>` (only two `<h2>`). `/coffee/brewing-guide/` has two `<h1>` ("Coffee brewing guide" and "Brew methods").
- **Why it matters:** The H1 is a main relevance signal. The cafe page has none.
- **Fix:** Add an H1 such as "Visit our roastery cafe in Ubud" to `/visit/`. Change the second H1 on the brewing guide to an `<h2>`.

### 11. Missing canonical on `/contact/`
- **URL:** `/contact/`
- **Fix:** Add `<link rel="canonical" href="https://kopikita.test/contact/">`. Every other page has one.

### 12. Missing meta description on `/about/`
- **URL:** `/about/`
- **Why it matters:** Google writes its own snippet, often a poor one, and the page loses a chance to state its value (since 2019, farmer partnerships, 30+ wholesale partners).
- **Fix:** Add a 140–160 character description.

### 13. Structured data errors and gaps
- **`/coffee/bali-kintamani/`:** `Product` schema has no `name`, which Google requires. The page is not eligible for product rich results as it stands. Fix: add `"name": "Bali Kintamani natural coffee, 250g"`.
- **`/coffee/flores-bajawa/`:** no `Product` schema, although the other two product pages have one. Add it with `name`, `image`, `offers`, `brand`.
- **All `Product` blocks:** no `aggregateRating`, `review` or `sku`. Add them only if real review data exists. Don't fabricate ratings.
- **`/coffee/`:** `FAQPage` markup, but the two Q&As are not visible on the page. Google requires marked-up content to be visible. FAQ rich results are also limited to government and health sites, so this earns nothing. Either show the FAQ on the page or remove the markup.
- **`/visit/` and `/contact/`:** no `LocalBusiness` (`CafeOrCoffeeShop`) markup. The business is a physical cafe with hours (7am–5pm daily), a phone number and an address. Add it with `openingHoursSpecification`, `telephone`, `geo` and `sameAs`.
- **Homepage `Organization`:** valid, but add `sameAs` (social profiles) and `contactPoint`.
- **Blog `Article` markup:** missing `image` (recommended for rich results), and the author has no `url`. `/blog/best-coffee-beans-2024/` has a headline that doesn't match its H1 or title. `/blog/cold-brew-at-home/` has no `Article` schema.
- **Missing site-wide:** no `BreadcrumbList` on product or blog pages; no `WebSite` schema on the homepage.

### 14. Oversized hero image, no responsive sizing
- **URL:** `/about/` (`/assets/img/roastery-hero.jpg`)
- **Evidence:** 1,818,123 bytes (about 1.8 MB), declared 2400×1600. The other images are small (`hero-beans.jpg` is 14 KB). No `srcset`, `sizes` or `loading` attributes on any image.
- **Why it matters:** A 1.8 MB hero image is likely to hurt LCP, especially on mobile in Indonesia.
- **Fix:** Resize to 1200–1600 px wide, convert to WebP or AVIF, provide `srcset`/`sizes`, aim under 200 KB, and add `fetchpriority="high"` to the LCP image. Add `loading="lazy"` to below-the-fold images.

### 15. Year in URL and title of an evergreen post
- **URL:** `/blog/best-coffee-beans-2024/`
- **Evidence:** URL, title and H1 say 2024. The page says "Our picks this year", and the schema says `dateModified` 2026-09-01.
- **Why it matters:** In 2026 the page looks stale in the SERP, which lowers click-through. Changing the year later means changing the URL.
- **Fix:** Move to `/blog/best-coffee-beans-bali/` with a 301 from the old URL, update the sitemap and canonical, remove "2024" from the title and H1, and make the content and dates consistent.

### 16. Overlong product title
- **URL:** `/coffee/bali-kintamani/`
- **Evidence:** "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita" is about 90 characters. Google will truncate it at roughly 60.
- **Fix:** `Bali Kintamani Natural Coffee Beans | Kopi Kita`. Move the roast and size into the description or body.

### 17. Thin content
- **`/blog/cold-brew-at-home/`:** a single paragraph (about 80 words). Compare 400+ words on the other posts. Expand with ratios, steeping options, storage, serving ideas, and an FAQ, or merge it into the brewing guide.
- **`/shop/`:** short copy with no product links beyond two coffees. It is a category page, so it should list real products with prices and links.
- **`/coffee/flores-bajawa/`:** a shorter page than its siblings with no brewing section or link to the brewing guide.

### 18. No Open Graph or Twitter Card tags
- **URL:** all pages
- **Why it matters:** Links shared on WhatsApp, Instagram or Facebook show no preview image or title. Social sharing is an important traffic route for a cafe in Bali.
- **Fix:** Add `og:title`, `og:description`, `og:image`, `og:url`, `og:type` and `twitter:card` to the shared template.

---

## Low

### 19. Missing alt text and image attributes on the homepage
- **URL:** `/` (`hero-beans.jpg`). Width and height are set (good, no layout shift), but there is no `alt`. Add descriptive alt text, for example "Freshly roasted single-origin coffee beans".

### 20. No favicon
- **URL:** `/favicon.ico` returns 404. Add a favicon and a `<link rel="icon">` tag. Google shows favicons in mobile search results.

### 21. Security headers absent (verify on production)
- **URL:** all pages
- **Evidence:** Responses carry no `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff` or `Referrer-Policy`. No `X-Frame-Options` either. No `Cache-Control` or compression either.
- **Why it matters:** These are not direct ranking factors, but they affect trust and security. HTTPS and HSTS in particular matter on production.
- **Fix:** Set them at the CDN or server. Confirm the canonical `https://` and `www`/non-`www` redirects on `kopikita.test`, which can't be tested locally.

### 22. Sitemap has no `lastmod`
- **URL:** `/sitemap.xml`. Add accurate `lastmod` dates (only when content actually changes). It helps Google prioritise recrawls, especially for blog posts.

### 23. Default 404 page
- **URL:** any missing path (for example `/nonexistent-page`). The status code is a correct 404, but the page is the bare server error page with no navigation. Add a branded 404 with links to the coffee, shop and blog sections.

### 24. Weak internal linking from content to products
- **URLs:** blog posts. `/blog/pour-over-coffee-guide/` links to Java Ijen, but the posts don't cross-link, `/blog/cold-brew-at-home/` is linked only from the blog index, and the footer has only a Contact link. Add related-post and related-product links with descriptive anchor text.

### 25. Brewing guide sits under the product folder
- **URL:** `/coffee/brewing-guide/`. An informational page in the product path. Consider `/blog/` or `/guides/brewing/` with a redirect. Low priority, so only move it if you will also fix the overlap in #9.

---

## What is working

- All 16 live pages have a unique title and a `viewport` tag, and every page has `lang="en"`. Two have shared-title or missing-description problems, as listed above.
- Self-referencing canonicals on 16 of 18 pages. `/shop/` and `/contact/` are the exceptions.
- Real 404 status codes (no soft-404s). Redirects are 301, not 302.
- `robots.txt` exists, declares the sitemap and doesn't block content directories (apart from CSS).
- Product pages have unique, descriptive copy and image alt text. `/about/` and the product pages set image dimensions.
- Clean, flat URL structure and a consistent site-wide nav.

## Recommended order of work

1. **Today (about an hour):** items 1, 2, 3, 4, 5, 7 and 8. They are one-line changes to a canonical, a robots tag, the sitemap, a nav link and `robots.txt`.
2. **This week:** items 6, 10, 11, 12, 13 (product `name`, Flores schema, `LocalBusiness`), 14 and 16.
3. **This month:** items 9, 15, 17 and 18, plus internal-linking work (24).
4. **Then:** re-crawl, submit the corrected sitemap in Search Console, and check the Page indexing report for `/shop/` and `/wholesale/`. Re-run this audit monthly.
