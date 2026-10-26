# Technical SEO Audit: Kopi Kita (kopikita.test)

> Audit date 2026-10-22 · Source: live crawl of http://localhost:8765/ with curl · 18 sitemap URLs + 3 linked URLs checked · No health score (SE Ranking MCP was not connected)

## Method and limits

- I fetched `/robots.txt`, `/sitemap.xml`, all 18 sitemap URLs, every URL linked from the navigation and body copy, and the image, CSS and favicon assets.
- Without SE Ranking, Firecrawl, CrUX or Search Console, these checks were **not run**: JS-render comparison, Core Web Vitals field data, GSC indexation status and backlinks. The site serves static HTML, so JS rendering is a low risk.
- The local server is Python `SimpleHTTP`. Findings about headers, compression and caching (see "Informational: infrastructure") may come from that server rather than production. Re-check them against the live host.
- Absolute URLs in the sitemap and canonicals use `https://kopikita.test`. Paths below are relative to that domain.

## Summary

| Severity | Count |
|---|---|
| Critical | 4 |
| High | 5 |
| Medium | 8 |
| Low | 4 |

## Priority-ordered issues

### Critical

**1. Sitemap lists a URL that returns 404: `/coffee/sumatra-mandheling/`**
- Why it matters: the sitemap is telling Google to crawl a dead page. This wastes crawl budget and lowers trust in the sitemap. The page was probably also meant to be a product page that could earn traffic.
- Fix: publish the page, or remove it from `sitemap.xml`. Generate the sitemap from the live routes so this can't drift.

**2. `/shop/` canonicalises to `/coffee/`**
- Affects: `/shop/` (`<link rel="canonical" href="https://kopikita.test/coffee/">`).
- Why it matters: the Shop page tells Google it is a duplicate of `/coffee/`, so `/shop/` will not be indexed. The nav and sitemap both treat it as a primary page. It is the page that should rank for "buy coffee beans Bali" and "brewing gear". The sitemap also contains a URL that points its canonical elsewhere, which sends Google contradictory signals.
- Fix: change the canonical to `https://kopikita.test/shop/`. If the pages really are duplicates, 301 one to the other instead and drop it from the nav and sitemap.

**3. `/wholesale/` is `noindex` but is in the sitemap and main nav**
- Affects: `/wholesale/` (`<meta name="robots" content="noindex, follow">`).
- Why it matters: this is a B2B revenue page (30+ partners, free-sample CTA) and it is invisible to search. Search terms like "wholesale coffee Bali", "coffee supplier for cafes Ubud" and "hotel coffee supplier Bali" cannot reach it. A noindexed URL in the sitemap is also a conflicting signal. This looks like a staging leftover.
- Fix: remove the noindex tag. Then request indexing in Search Console.

**4. Primary nav links to a redirect chain: `/menu/` → `/cafe/` → `/visit/`**
- Affects: the "Visit the cafe" link on every page (21 URLs, sitewide).
- Why it matters: this is a two-hop 301 chain on an internal link in the header of every page. It wastes crawl budget and dilutes link equity. Each hop adds latency. The real page is `/visit/`.
- Fix: point the nav link at `/visit/`. Collapse the redirects to a single hop (`/menu/` → `/visit/` and `/cafe/` → `/visit/`).

### High

**5. Broken internal link: `/coffee/aceh-gayo/` (404)**
- Affects: the link sits in `/blog/how-to-brew-pour-over/`, one of the blog's two pour-over posts.
- Why it matters: a dead link in body copy is a poor user experience and passes no equity. The product it names doesn't appear anywhere else on the site.
- Fix: remove the link, or create the Aceh Gayo product page. Sumatra Mandheling (#1) may be the same story: a product that was planned or retired but not cleaned up.

**6. Two blog posts compete for the same query: `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`**
- Why it matters: both target "how to make pour over coffee", with near-identical recipes (15g / 250g / 93°C / bloom 40g). Google has to pick one and the other will rank poorly. Their page signals are split, as are internal links and any future backlinks.
- Fix: merge them. Keep the stronger one (the "how to" post has 2025 content and more depth), 301 the other to it and move any unique material across. Or differentiate them clearly: one as a beginner's gear guide, one as the recipe.

**7. `/subscriptions/` has the same title tag as `/coffee/`: "Single-Origin Indonesian Coffee | Kopi Kita"**
- Why it matters: the title is the strongest on-page signal and this one doesn't describe the page. It is a duplicate of `/coffee/`, so the two pages compete and neither gets a good snippet. The subscription page can't rank for "coffee subscription Bali".
- Fix: e.g. `Coffee Subscriptions in Bali: Fresh Beans Every 2 or 4 Weeks | Kopi Kita`.

**8. `/coffee/flores-bajawa/` and `/coffee/sumatra-mandheling/` have no internal links from the site**
- Why it matters: `/coffee/` and `/shop/` only link to Bali Kintamani and Java Ijen, so Flores Bajawa is reachable only through the sitemap. Pages with no internal links get little equity and are crawled less. A buyer browsing the site can't find the third coffee.
- Fix: list every coffee on `/coffee/` and `/shop/`, and add related-product links from the product pages.

**9. `/visit/` has no `<h1>`**
- Why it matters: the page starts with `<h2>Opening hours</h2>`. It lacks a primary heading with the target topic ("Visit our roastery cafe in Ubud"), which is the page to rank for local searches like "coffee shop Ubud".
- Fix: add `<h1>Visit our roastery cafe in Ubud</h1>`.

### Medium

**10. `/coffee/brewing-guide/` has two `<h1>` tags ("Coffee brewing guide" and "Brew methods")**
- Why it matters: it dilutes the page's main topic and breaks the heading outline for accessibility.
- Fix: change the second to `<h2>`. Use `<h2>` for each method too.

**11. Missing local business structured data for the cafe, and the Organization schema is thin**
- Affects: `/`, `/visit/`, `/contact/`.
- Why it matters: a physical cafe with opening hours (7am–5pm daily), a free Saturday cupping and a street address is a strong local SEO opportunity. There is no `LocalBusiness`/`CafeOrCoffeeShop` markup, no `openingHoursSpecification`, no `geo`, no phone and no `sameAs` links. The Organization schema on `/` has only name, url, logo and address.
- Fix: add `CafeOrCoffeeShop` JSON-LD on `/visit/` and `/contact/` with address, `geo`, `openingHoursSpecification`, `telephone` (+62 812 0000 0000) and `sameAs`. Claim and match the Google Business Profile to the same NAP. Add `telephone`/`contactPoint` and `sameAs` to Organization.

**12. Product schema problems**
- `/coffee/bali-kintamani/`: the `Product` has no `name`, a required field. It will be ineligible for product rich results.
- `/coffee/flores-bajawa/`: no Product schema at all.
- `/coffee/java-ijen/`: valid, but name says "250g" while the page also sells 1kg.
- None of the three has `sku`, `aggregateRating`/`review`, `priceValidUntil` or `shippingDetails`. Offers have no `url`.
- Fix: add `name` to Kintamani and add Product schema to Flores Bajawa. Use two `Offer`s (250g and 1kg) per product, with prices that match the page text. Add reviews only if real reviews are on the page.

**13. `FAQPage` schema on `/coffee/` doesn't match the visible page**
- Why it matters: neither question is shown on the page. Google also limits FAQ rich results to a small set of authoritative sites, so there is little upside and a risk of a markup/content mismatch.
- Fix: either add a visible FAQ section with these Q&As or remove the schema. Prefer the visible FAQ: it is useful to buyers.

**14. Article schema is incomplete, and one article's dates and title are stale**
- Affects: the three blog posts with schema. Missing `image`, `publisher`, `mainEntityOfPage` and author `url`. `/blog/cold-brew-at-home/` has no schema at all.
- `/blog/best-coffee-beans-2024/`: the URL, title tag and H1 say "2024" but `dateModified` is 2026-09-01. Schema `headline` ("The best coffee beans in Bali") doesn't match the H1 ("... (2024 guide)"). Readers see an outdated year in the search result, and Google sees conflicting freshness signals. The "our picks this year" line is also undated.
- Fix: complete the Article schema. Retitle to "Best Coffee Beans in Bali (2026 Guide)" and keep the schema headline the same as the H1. 301 `/blog/best-coffee-beans-2024/` to an evergreen URL such as `/blog/best-coffee-beans-bali/`, update the sitemap and internal links.

**15. No Open Graph or Twitter Card tags on any page**
- Affects: all 21 pages.
- Why it matters: shares on WhatsApp, Instagram, Facebook, LinkedIn and X show a bare link with no image or tailored title. WhatsApp is a primary channel here (the contact page uses it).
- Fix: add `og:title`, `og:description`, `og:image` (1200×630), `og:url`, `og:type` and `twitter:card` to the template. Use the page's own image for product and article pages.

**16. Over-long title tag on `/coffee/bali-kintamani/`, and thin metadata elsewhere**
- `/coffee/bali-kintamani/`: title is about 85 characters ("Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita"). Google will truncate it at roughly 60. Shorten: `Bali Kintamani Natural Coffee Beans (250g) | Kopi Kita`.
- `/about/`: no meta description. Google will invent one.
- Fix: write a description for `/about/` (about 150 characters) and fix the title.

**17. Thin content: `/blog/cold-brew-at-home/` (about 70 words)**
- Why it matters: it's a single paragraph with no sections, no schema and no image. It can't compete for "how to make cold brew", a high-volume query. `/coffee/brewing-guide/` already covers the same recipe in a line.
- Fix: expand it to 600+ words (ratios, steep times, hot-bloom variation, storage, troubleshooting, a recommended coffee) or fold it into the brewing guide and redirect.

### Low

**18. `robots.txt` blocks `/assets/css/`**
- Why it matters: Google needs to fetch CSS to render pages and judge mobile-friendliness. Blocking it can make pages look unstyled to Googlebot. It does no harm to search that `/cart/` is disallowed, but `/cart/` returns 404 today.
- Fix: remove `Disallow: /assets/css/`. Keep `/cart/` blocked if a cart will exist. Consider adding `/checkout/` and `/account/`.

**19. `/contact/` has no canonical tag**
- Every other page has a self-referencing canonical. Add `<link rel="canonical" href="https://kopikita.test/contact/">`.

**20. Images**
- `/` (`/assets/img/hero-beans.jpg`): no `alt` attribute. It is the home page hero.
- `/about/` (`/assets/img/roastery-hero.jpg`): the file is 1.8 MB at 2400×1600. This is a likely LCP/page-weight problem on mobile. Add `srcset`/`sizes`, serve WebP/AVIF at 1200px or less and compress to under 200 KB.
- All images are `.jpg`/`.png` with no `srcset`, `loading="lazy"` below the fold or `fetchpriority="high"` on the hero. The three product pages and the hero have `width`/`height`, which is good (no layout shift).
- Fix: add alt text (e.g. "Freshly roasted coffee beans in the Kopi Kita roastery"), responsive images and modern formats.

**21. Sitemap has no `<lastmod>` values, and blog dates are not exposed**
- Google uses accurate `lastmod` to schedule recrawls. Several posts were updated in 2026 (see Article `dateModified`). Add `lastmod` from real modification dates (not the build time).

### Informational: infrastructure (verify on production)

- **Security headers**: none present on any page (no `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, HSTS). They are a trust and hygiene signal rather than a ranking factor. Add them at the CDN/web server. This is a `localhost` check over HTTP, so HSTS and HTTPS redirects need to be tested on `kopikita.test`.
- **Caching/compression**: no `Cache-Control`, `ETag` or `Content-Encoding` headers on HTML, CSS or images. Enable gzip/brotli and long-lived caching on `/assets/`.
- **404 page**: unknown URLs return the server's default "Error response" with a correct 404 status. Add a branded 404 page that links to `/coffee/`, `/shop/` and `/blog/`.
- **Favicon**: `/favicon.ico` returns 404. Add a favicon and `<link rel="icon">`.
- **Internationalisation**: the site is English only (`lang="en"`) and sells across Indonesia. If an Indonesian-language version is planned, use `hreflang` with `x-default`. Not a defect today.
- **Good**: HTTPS canonicals, a self-referencing canonical on 17 of 18 live pages, a viewport tag, `lang` attribute, unique titles on all pages except #7, descriptions on 17 of 18, clean URL structure, and descriptive internal anchor text.

## Top 10 fixes (impact × effort)

| Rank | Issue | Severity | Pages | Fix | Effort |
|---|---|---|---|---|---|
| 1 | `/shop/` canonicalised to `/coffee/` | Critical | 1 | Self-canonical | S |
| 2 | `/wholesale/` noindexed but in sitemap and nav | Critical | 1 | Remove noindex | S |
| 3 | Nav link → `/menu/` → `/cafe/` → `/visit/` chain | Critical | 21 | Link to `/visit/`, single redirect | S |
| 4 | Sitemap lists 404 `/coffee/sumatra-mandheling/` | Critical | 1 | Publish or remove | S |
| 5 | Broken link `/coffee/aceh-gayo/` | High | 1 | Remove or build | S |
| 6 | `/subscriptions/` duplicate title | High | 1 | Rewrite title | S |
| 7 | Duplicate pour-over posts | High | 2 | Merge and 301 | M |
| 8 | Orphaned `flores-bajawa` page | High | 2 | Link from `/coffee/` and `/shop/` | S |
| 9 | `/visit/` missing H1 | High | 1 | Add H1 | S |
| 10 | Local business, Product and Article schema gaps | Medium | 8 | Add/repair JSON-LD | M |

## Recommended cadence

Fix ranks 1–9 first: they are small template or content edits, and ranks 1–3 affect indexing of revenue pages. Then re-run this audit. Add a CI check that fails the build on sitemap URLs that don't return 200, canonicals that don't point to the page itself, and internal links that redirect or 404. Re-run monthly, and confirm the infrastructure items on the production host.
