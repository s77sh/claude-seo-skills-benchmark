# SEO Audit: Kopi Kita (kopikita.test)

Audited 2026-10-22 against the local build at http://localhost:8765/. All 19 URLs were fetched: the 17 in the sitemap plus `/menu/` and `/cafe/` from the nav and redirects. Business type: local specialty coffee roaster, e-commerce, cafe and wholesale, in Ubud, Bali.

**Estimated health score: 62/100.** Content quality is good. Indexation and architecture problems hold the score down.

**Limits of this audit.**
- It was run over plain HTTP on a Python dev server, so I could not check HTTPS, HSTS, security headers, compression, caching headers or real Core Web Vitals. Re-check these on production.
- I did not see the CSS in use, so I made no visual or mobile rendering judgements. The only CSS size I fetched is 149 bytes.
- I did not check `/favicon.ico` or any rendering.
- No Google Search Console, analytics or backlink data was available.

---

## Critical

### 1. The wholesale page is `noindex` but is in the sitemap and main nav
- **URL:** `/wholesale/`
- **Evidence:** `<meta name="robots" content="noindex, follow">`. The URL is in sitemap.xml and linked from every page. The page is written to sell wholesale ("30+ cafes", free training, sample box).
- **Why it matters:** The page cannot rank for "wholesale coffee Bali" and similar queries, which is likely a high-value B2B line. The sitemap also contradicts the directive, and Search Console will flag "Submitted URL marked noindex".
- **Fix:** Remove the noindex tag, unless it was left on from staging on purpose. If you do want it hidden, remove it from the sitemap and nav as well. Add a `Service` or `LocalBusiness` offer block.

### 2. A sitemap URL returns 404 and has no internal links
- **URL:** `/coffee/sumatra-mandheling/` (404; listed in sitemap.xml)
- **Why it matters:** Submitting dead URLs wastes crawl budget and lowers Google's trust in the sitemap. The page is unreachable by navigation, and no page links to it.
- **Fix:** Either publish the page (with Product schema and links from `/coffee/` and `/shop/`) or remove it from the sitemap. Add a 404 check to the sitemap build.

### 3. `/shop/` canonicalises to `/coffee/`
- **URL:** `/shop/` (`<link rel="canonical" href="https://kopikita.test/coffee/">`)
- **Why it matters:** Google is told `/shop/` is a duplicate of `/coffee/`. It will probably drop `/shop/` from the index, losing the transactional page for "buy coffee beans / brewing gear" queries. The page has distinct content (gear, drip bags, shipping threshold).
- **Fix:** Set the canonical to `https://kopikita.test/shop/`. If you really do want one merged page, 301 `/shop/` to `/coffee/` and update the nav.

### 4. Duplicate title tags with a mismatched page
- **URLs:** `/coffee/` and `/subscriptions/` both use `Single-Origin Indonesian Coffee | Kopi Kita`
- **Why it matters:** The subscriptions page has a title that describes a different page. It will compete with `/coffee/` and does not target subscription queries. The title is also what appears in search results.
- **Fix:** Give `/subscriptions/` its own title, for example `Coffee Subscriptions in Indonesia: Fresh Beans Every 2 or 4 Weeks | Kopi Kita`.

---

## High

### 5. Broken internal link in a blog post
- **URL:** `/blog/how-to-brew-pour-over/` links to `/coffee/aceh-gayo/` (404).
- **Why it matters:** It is a dead end for users, wastes link equity and is a quality signal. The page also recommends a product that does not exist.
- **Fix:** Link to an existing coffee (`/coffee/flores-bajawa/` or `/coffee/bali-kintamani/`), or publish the Aceh Gayo page.

### 6. Redirect chain in the main navigation
- **URL:** The nav link "Visit the cafe" → `/menu/` → 301 `/cafe/` → 301 `/visit/` (final 200). This link is on every page.
- **Why it matters:** Two hops on every crawl and click. Link equity is diluted, and chained hops slow the page for users.
- **Fix:** Change the nav `href` to `/visit/` on all pages and point `/menu/` and `/cafe/` directly at `/visit/` with single 301s.

### 7. Two blog posts compete for the same query
- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Evidence:** Both target "pour over coffee" and contain the same recipe (15g, 250g, 93C, 40g bloom, circles, 3 minutes). Titles are "How to Brew Pour Over Coffee at Home" and "Pour Over Coffee Guide for Beginners".
- **Why it matters:** Keyword cannibalisation. Google may swap which one ranks, and neither builds full authority.
- **Fix:** Pick one as the main page (the longer `how-to-brew-pour-over` one is stronger), merge the unique beginner content (dripper choice, filters, kettle) into it and 301 the other to it. If you keep both, differentiate: one a recipe, the other a gear and beginner mistakes page, with distinct titles, intents and a link between them.

### 8. Product pages missing from the catalogue pages
- **URLs:** `/coffee/flores-bajawa/`, `/coffee/` and `/shop/`
- **Evidence:** `/coffee/` links only to Kintamani and Ijen. `/shop/` links to the same two. Flores Bajawa is only in the sitemap and gets no contextual links.
- **Why it matters:** An orphan-like product page gets little internal PageRank and is crawled less often. The product listing is also incomplete for shoppers.
- **Fix:** List all coffees (Flores, plus Sumatra if published) on `/coffee/` and `/shop/` with prices, and link them from the homepage.

### 9. Homepage and key pages have little structural markup for a local business
- **URLs:** `/`, `/visit/`, `/contact/`
- **Evidence:** The only schema is a bare `Organization` (name, url, logo, address). No `LocalBusiness` / `CafeOrCoffeeShop`, phone, geo, opening hours, `sameAs` or `ContactPoint`. The Visit and Contact pages have no schema.
- **Why it matters:** Local pack and Maps features depend on consistent NAP and hours data. Hours (7am to 5pm daily) exist only in prose.
- **Fix:** Add `CafeOrCoffeeShop` JSON-LD (address, `geo`, `openingHoursSpecification`, `telephone` +62 812 0000 0000, `email`, `sameAs`, `image`, `priceRange`) on `/visit/` and the homepage. Create and link a Google Business Profile with the same NAP.

### 10. Visit page has no H1
- **URL:** `/visit/`
- **Evidence:** The page begins at `<h2>Opening hours</h2>`, followed by `<h2>Menu</h2>`.
- **Why it matters:** No primary topic heading for the page that targets local queries. The nav label is "Visit the cafe" while the title says "Visit Our Roastery Cafe in Ubud".
- **Fix:** Add `<h1>Visit our roastery cafe in Ubud</h1>`, and add the address, map embed and directions.

---

## Medium

### 11. Missing meta description and canonical
- **`/about/`:** no meta description (Google will pick arbitrary text).
- **`/contact/`:** no canonical tag (all other pages have one).
- **Fix:** Add a description to About and a self-referencing canonical to Contact.

### 12. Product schema is incomplete
- **URL:** `/coffee/bali-kintamani/`: the Product JSON-LD has no `name`. That is a required property, so the rich result is invalid.
- **URL:** `/coffee/java-ijen/`: has a name, but neither product has `sku`, `aggregateRating` / `review`, `priceValidUntil` or shipping/return details. `Flores Bajawa` (and Sumatra) have no Product schema at all.
- **Why it matters:** Product rich results (price, availability) are lost or ineligible.
- **Fix:** Add `name` and `sku`, and add Product + Offer markup to every product page, with `url`, `shippingDetails` and `hasMerchantReturnPolicy`. Add reviews only if real customer reviews are shown on the page. Prices in schema (145000 and 150000 IDR) do match the visible prices, which is correct.

### 13. FAQPage schema without visible FAQ content
- **URL:** `/coffee/`
- **Evidence:** The JSON-LD has two questions ("How fresh is your coffee?", "Do you ship outside Bali?"). The page has no visible Q&A section.
- **Why it matters:** Structured data must match visible content, or it risks a manual action. Google also restricts FAQ rich results to authoritative government and health sites, so there is no rich result benefit.
- **Fix:** Show the Q&A on the page or remove the markup. Showing the answers is a good idea for users anyway.

### 14. Two H1s on the brewing guide
- **URL:** `/coffee/brewing-guide/`: `<h1>Coffee brewing guide</h1>` and `<h1>Brew methods</h1>`.
- **Fix:** Change the second to `<h2>`. Also make the bold run-in labels (Grind size chart, Water temperature, Troubleshooting) into `<h2>` / `<h3>` headings, and consider a `HowTo`-free table for the ratios so it is easier to scan.

### 15. Article schema is thin, and dates look inconsistent
- **URLs:** `/blog/how-to-brew-pour-over/`, `/blog/pour-over-coffee-guide/`, `/blog/best-coffee-beans-2024/`
- **Evidence:** There is no `image`, `publisher`, `mainEntityOfPage` or author `url`. `/blog/cold-brew-at-home/` has no Article schema at all. The best-beans post says "2024" in its URL and H1 and was published 2024-01-15, yet was modified 2026-09-01. The page says "Our picks this year".
- **Why it matters:** Visible dates are not shown on any post, so freshness and trust signals are weak. A "2024" label looks stale in 2026 and hurts CTR.
- **Fix:** Add `image`, `publisher` (Organization with logo) and an author `url` to a real author page. Show "Published / Updated" dates in the page. For the best-beans post, update the content and change the title and H1 to the current year (or drop the year), and 301 `/blog/best-coffee-beans-2024/` to a year-free URL such as `/blog/best-coffee-beans-bali/`. Keep the update to the visible text, not just `dateModified`.

### 16. Title tag problems
- `/coffee/bali-kintamani/` is about 88 characters (`Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita`) and will be truncated. Shorten to about 60 characters: `Bali Kintamani Natural Coffee Beans (250g) | Kopi Kita`.
- `/about/` has a title but no brand-consistent description (see issue 11).
- `/blog/best-coffee-beans-2024/` says "(2024 Guide)" (see issue 15), and the H1 and schema headline differ from the title.

### 17. Oversized, unoptimised images and a missing alt
- **`/about/`:** `/assets/img/roastery-hero.jpg` is **1.8 MB** and 2400×1600. It is a hero image, probably the LCP element, and has no `srcset` or `loading` hints.
- **`/` (homepage):** `/assets/img/hero-beans.jpg` has **no `alt` attribute** (width/height are set, which is good). It is the LCP image and is 13.8 KB, so size is fine.
- **Fix:** Add descriptive alt text to the hero. Convert the About image to WebP/AVIF at about 1600px wide, targeting under 200 KB, with `srcset`/`sizes`. Add `fetchpriority="high"` to the LCP image. Use `loading="lazy"` for images below the fold.

### 18. Blog post is thin and lacks structure
- **URL:** `/blog/cold-brew-at-home/`: about 70 words in one paragraph, no schema, no sub-headings, no images. It also duplicates the cold-brew recipe already in the brewing guide.
- **Fix:** Expand into a proper guide (ratios by strength, steeping time, storage, serving ideas, troubleshooting, FAQs) or merge into the brewing guide and redirect. Add Article schema.

### 19. Sitemap quality
- No `<lastmod>` on any URL, which is useful for crawl prioritisation. It includes a noindex page (issue 1) and a 404 (issue 2). `/shop/` is listed despite canonicalising elsewhere (issue 3).
- **Fix:** Generate the sitemap from the live site, include only indexable 200 URLs that are self-canonical, and add accurate `lastmod`.

### 20. Robots.txt blocks CSS and disallows a non-existent path
- **URL:** `/robots.txt` has `Disallow: /assets/css/` and `Disallow: /cart/`.
- **Why it matters:** Blocking CSS stops Googlebot rendering pages the way users see them, which can harm mobile-friendliness and layout assessment. `/cart/` returns 404, so that rule does nothing today.
- **Fix:** Remove the CSS disallow (and don't block JS/images). Keep `/cart/` only if a cart exists, and prefer noindex on cart and checkout pages. The `Sitemap:` line is present and correct. `https://kopikita.test/sitemap.xml` matches the production domain.

---

## Low

### 21. No Open Graph or Twitter Card tags on any page
Links shared on WhatsApp, Instagram, Facebook and X will show no image or controlled title. Add `og:title`, `og:description`, `og:image` (use the product and hero images), `og:type`, `og:url` and `twitter:card`.

### 22. Weak internal linking and anchor text
- Nav is the same 9 links everywhere, and there is no breadcrumb. Blog posts do not link to each other, and the blog index lists only titles with no excerpts or dates.
- The footer has only a Contact link.
- **Fix:** Add breadcrumbs (with `BreadcrumbList` schema), "related reading" blocks, and link the product pages from relevant blog posts (the pour over posts link well to Ijen, so keep that pattern). Add footer links to Shop, Wholesale and Visit.

### 23. E-E-A-T and authorship
- All three authored posts credit "Wayan Sudarma" in schema, but there is no visible byline or author page. The About page mentions him as head roaster (12 years, trained in Melbourne), which is a strong experience signal worth surfacing.
- **Fix:** Add a visible byline linking to an author bio page, and add `Person` schema with `sameAs`. Add customer reviews, farmer photos and certifications if available.

### 24. AI search readiness
- No `/llms.txt` (404). This is optional and Google ignores it. robots.txt does not restrict AI crawlers (it allows `*`), which is good for citation.
- Positives: short, quotable factual passages (recipes with specific numbers, prices, altitudes).
- **Fix:** Optionally add `llms.txt`. More useful: put question-style H2s on guides ("What ratio should I use for pour over?") with a direct answer first.

### 25. Language and i18n
`<html lang="en">` is set. If you serve Indonesian customers, consider an `id` version with hreflang. Currently all content is English only.

### 26. Minor technical hygiene
- 404 page is the Python default, with no site navigation. Create a branded 404 that links to key pages.
- Redirects use 301 (correct). Trailing-slash URLs are consistent across the site.
- Responses carry no caching or compression headers (dev-server limitation): verify `Cache-Control`, gzip/brotli and HTTP/2 in production.

---

## What is working well

- Every page except About has a unique, well-written meta description, and most titles are under about 65 characters with the brand at the end.
- Canonical tags are present on 15 of 16 indexable pages. Most are correct self-references (the exceptions are `/shop/` and the missing one on `/contact/`).
- A single H1 on nearly every page, with the keyword in it.
- Viewport meta and `lang` are set. Image dimensions are declared, preventing layout shift. Product and about images have meaningful alt text.
- Product prices in schema match the on-page prices.
- Content is original, specific and experience-based (altitudes, varieties, processes, recipes with measurements), with sound topical depth in the longer blog posts.
- Clean, keyword-readable URL structure with consistent trailing slashes. Robots.txt declares the sitemap.

---

## Priority action list

| # | Action | Priority |
|---|--------|----------|
| 1 | Remove `noindex` from `/wholesale/` (or remove from sitemap and nav) | Critical |
| 2 | Fix or remove the `/coffee/sumatra-mandheling/` 404 in the sitemap | Critical |
| 3 | Set `/shop/` canonical to itself | Critical |
| 4 | Write a unique title for `/subscriptions/` | Critical |
| 5 | Fix the `/coffee/aceh-gayo/` link | High |
| 6 | Change nav to `/visit/` and collapse the redirect chain | High |
| 7 | Merge or differentiate the two pour over posts | High |
| 8 | Link Flores Bajawa from `/coffee/`, `/shop/` and home | High |
| 9 | Add `CafeOrCoffeeShop` schema with hours, phone and geo | High |
| 10 | Add an H1 to `/visit/` | High |
| 11 to 20 | Metadata, schema, headings, images, sitemap and robots fixes above | Medium |
| 21 to 26 | OG tags, internal links, authorship, llms.txt, 404 page | Low |
