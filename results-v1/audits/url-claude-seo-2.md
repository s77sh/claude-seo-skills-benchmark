# SEO Audit: Kopi Kita (kopikita.test)

Audited 2026-10-22 against the local copy at http://localhost:8765/. I fetched every URL in the sitemap plus the URLs the site links to or redirects to: 19 pages, robots.txt, sitemap.xml and the key assets.

**Business type:** Local specialty coffee roaster with e-commerce, a cafe, wholesale and a blog (Ubud, Bali).
**Estimated SEO Health Score: ~58/100.** The on-page basics are mostly sound: unique titles and descriptions, self-canonicals, viewport tag, sensible H1s and good body copy on most pages. The score is dragged down by indexation and canonicalisation errors on money pages, broken internal links and sitemap entries, and thin structured data and local signals.

## Not verifiable from the local environment
- HTTPS, HSTS, other security headers, HTTP/2, compression and caching. The local server is Python SimpleHTTP with no such headers, so check these on production.
- Core Web Vitals field data, backlinks, Search Console data and Google Business Profile. No access to any of these.
- www/non-www and http/https redirects on the real domain.

---

## CRITICAL (fix immediately)

### 1. Wholesale page is set to noindex
- **URL:** /wholesale/
- **Evidence:** `<meta name="robots" content="noindex, follow">`. The page is also in sitemap.xml and the main nav.
- **Why it matters:** It is a revenue page with a good keyword-targeted title and description ("Wholesale Coffee for Cafes and Hotels in Bali"). It cannot rank while noindexed. The sitemap contradicts the tag.
- **Fix:** Remove the robots meta tag (or set `index, follow`) unless the exclusion is deliberate. If it is deliberate, also drop it from the sitemap and update the nav and descriptions.

### 2. Shop page canonicalises to the Coffee page
- **URL:** /shop/
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/">` on /shop/. /shop/ is also listed in the sitemap.
- **Why it matters:** Google will treat /shop/ as a duplicate and drop it from the index. You lose rankings for "buy coffee beans / brewing gear" queries, and the gear and drip-bag content is never indexed on its own.
- **Fix:** Set the canonical to `https://kopikita.test/shop/`. The page content is already distinct (it covers gear and drip bags, not just beans).

### 3. Every page's nav link to the cafe goes through a two-step redirect chain
- **URL:** /menu/ (linked sitewide in the main nav as "Visit the cafe"), which redirects 301 to /cafe/, which redirects 301 to /visit/.
- **Why it matters:** Every page on the site links to a URL that redirects twice. That wastes crawl budget and dilutes link equity to the cafe page, and it slows users. The destination, /visit/, is only linked from /about/.
- **Fix:** Change the nav href to `/visit/` on every page (one template change). Then collapse the redirects so /menu/ and /cafe/ each go straight to /visit/ with a single 301.

### 4. robots.txt blocks the site's CSS
- **URL:** /robots.txt has `Disallow: /assets/css/`, and every page loads `/assets/css/site.css`.
- **Why it matters:** Googlebot cannot fetch the stylesheet, so it cannot render pages as users see them. That hurts mobile-friendliness and layout evaluation and can distort CLS/LCP signals.
- **Fix:** Remove the `Disallow: /assets/css/` line. Don't block CSS, JS or images. `Disallow: /cart/` is fine, but note /cart/ currently returns 404. Make sure the real cart/checkout URLs are the ones disallowed.

---

## HIGH (fix within a week)

### 5. Broken internal link to a 404 page
- **URL:** /blog/how-to-brew-pour-over/ links to /coffee/aceh-gayo/, which returns 404.
- **Why it matters:** It is a dead end for users and crawlers, and it is a link out of a post meant to drive product sales.
- **Fix:** Create the Aceh Gayo product page, or point the link at an existing coffee such as /coffee/bali-kintamani/ (the sentence recommends something heavier, and Kintamani is described as heavy-bodied).

### 6. Sitemap lists a 404 URL and indexing-conflicted URLs
- **URL:** /sitemap.xml
- **Evidence:** `/coffee/sumatra-mandheling/` returns 404. It also lists /wholesale/ (noindex) and /shop/ (canonical to another URL). No `<lastmod>` on any entry.
- **Why it matters:** A sitemap should contain only indexable, 200, self-canonical URLs. Conflicting signals reduce trust in the file, and Search Console will flag them.
- **Fix:** Remove or create the Sumatra page. After fixes 1 and 2 the wholesale and shop entries will be valid. Add accurate `<lastmod>` values.

### 7. Product schema is invalid or missing on product pages
- **URLs:** /coffee/bali-kintamani/, /coffee/flores-bajawa/, /coffee/java-ijen/
- **Evidence:** The Kintamani Product JSON-LD has no `name` (required for Product rich results). Flores Bajawa has no schema at all. Ijen has a name, price, currency and availability but no `sku`, `url` or review data.
- **Why it matters:** Without a name the Kintamani markup cannot qualify for product rich results (price and availability in search). Flores misses them entirely.
- **Fix:** Add `name`, `sku`, `url` and `offers.url` to every product page. Add the 1kg offers (prices are on the page). Add Flores Bajawa with price Rp 155,000. Only add `aggregateRating`/`review` if there are real reviews on the page.

### 8. Duplicate / cannibalising blog posts
- **URLs:** /blog/how-to-brew-pour-over/ and /blog/pour-over-coffee-guide/ (also overlapping with /coffee/brewing-guide/ and /blog/cold-brew-at-home/)
- **Evidence:** Both posts give the same recipe (15g coffee, 250g water, 93C, 40g bloom, ~3 minutes) and target the same query ("pour over coffee").
- **Why it matters:** Two pages compete for one query, and neither is likely to rank well. The cold brew recipe is repeated across two further pages.
- **Fix:** Merge them. Keep the stronger one (the longer, how-to post), 301 the other to it, and differentiate the rest: beginner gear guide vs. recipe, or make the guide a hub that links to separate method posts. Have the brewing guide link to the single canonical pour-over post.

### 9. Missing heading / meta elements
- **/visit/:** no `<h1>`. The page uses only `<h2>`s ("Opening hours", "Menu"). Add an H1 such as "Visit the Kopi Kita roastery cafe in Ubud".
- **/coffee/brewing-guide/:** two `<h1>` tags ("Coffee brewing guide" and "Brew methods"). Change the second to `<h2>`.
- **/about/:** no meta description. Add one (~150 characters).
- **/contact/:** no canonical tag. Add `<link rel="canonical" href="https://kopikita.test/contact/">`.
- **Why it matters:** Headings give Google and users the page topic, a missing description lets Google pick arbitrary snippet text, and a missing canonical leaves duplicate-URL variants unresolved.

### 10. Orphaned and under-linked pages
- **/coffee/flores-bajawa/** is not linked from any page (not /coffee/, /shop/ or the homepage), so it is reachable only through the sitemap. The /coffee/ page says "three to five single origins" but lists only two.
- **/blog/cold-brew-at-home/** is linked only from the blog index.
- **/subscriptions/** and **/visit/** get little contextual linking (/subscriptions/ only from the nav).
- **Why it matters:** Orphan pages get little crawl priority or link equity, and a product no one can click to is a lost sale.
- **Fix:** Link Flores Bajawa from /coffee/, /shop/ and the homepage. Link the cafe page from the footer and homepage, and link subscriptions from product pages. Add breadcrumbs (with BreadcrumbList schema) and a fuller footer nav.

### 11. Duplicate title tag
- **URLs:** /coffee/ and /subscriptions/ share the identical title "Single-Origin Indonesian Coffee | Kopi Kita".
- **Why it matters:** Identical titles blur the pages' topics, and /subscriptions/ is not about single-origin coffee in general.
- **Fix:** Retitle /subscriptions/, for example "Coffee Subscription from Rp 165,000 | Fresh Roasted in Bali | Kopi Kita".

---

## MEDIUM (fix within a month)

### 12. Oversized, unoptimised images and a missing alt attribute
- **/ (homepage):** hero image `/assets/img/hero-beans.jpg` has no `alt` attribute. It is the LCP element.
- **/about/:** `/assets/img/roastery-hero.jpg` is 1.8 MB at 2400x1600.
- **Fix:** Add descriptive alt text to the hero. Compress and resize to the displayed size, serve WebP/AVIF with `srcset`/`sizes`, and use `fetchpriority="high"` (no lazy-loading) on the homepage hero. Width and height are already set, which is good for CLS.

### 13. Over-long title on the Kintamani product page
- **URL:** /coffee/bali-kintamani/
- **Evidence:** "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita" is about 88 characters, and Google will truncate it.
- **Fix:** Shorten to roughly 55-60 characters, such as "Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita".

### 14. Stale year in blog URL, title and H1
- **URL:** /blog/best-coffee-beans-2024/
- **Evidence:** The slug, title and H1 say 2024. The schema says datePublished 2024-01-15 and dateModified 2026-09-01. The article text says "Our picks this year".
- **Why it matters:** The page looks out of date to users in 2026 and is a poor match for current-year queries. A year in the slug locks you into a URL change each refresh.
- **Fix:** Move to an evergreen URL (/blog/best-coffee-beans-bali/) with a 301 from the old one, update the title and H1, and show a visible "Updated" date. Update the content and the pricing.

### 15. Thin blog content
- **URL:** /blog/cold-brew-at-home/
- **Evidence:** One short paragraph (~80 words), no schema, no author or date, and the recipe duplicates the brewing guide.
- **Fix:** Expand into a real guide (ratios, steep time by roast, storage, troubleshooting, a Kopi Kita bean recommendation), or fold it into the brewing guide and redirect.

### 16. Article schema is incomplete and the FAQ schema does not match the page
- **Articles** (/blog/how-to-brew-pour-over/, /blog/pour-over-coffee-guide/, /blog/best-coffee-beans-2024/): no `image`, `publisher` or author `url`. No other blog or content page has Article schema (cold brew, brewing guide).
- **/coffee/:** FAQPage schema with two Q&As, but those questions are not visible anywhere on the page. Markup must reflect visible content. Google also now shows FAQ rich results only for a narrow set of authoritative sites, so there is little upside.
- **Fix:** Add image, publisher (Organization) and an author profile URL to Articles. Either show the FAQ on /coffee/ or remove the markup.

### 17. Local and organisation schema is thin
- **Evidence:** Only the homepage has Organization schema (name, url, logo, address). There is no `sameAs`, `contactPoint`, `telephone`, `geo` or `openingHoursSpecification`, and nothing on /visit/ or /contact/. /assets/img/logo.png exists (200).
- **Why it matters:** The business is a physical cafe in Ubud. Local rich results and Maps eligibility depend on consistent entity data.
- **Fix:** Add `CafeOrCoffeeShop`/`LocalBusiness` schema on /visit/ with hours (07:00-17:00 daily), address, geo, phone (+62 812 0000 0000) and `sameAs` links. Keep name, address and phone identical to Google Business Profile, and embed a map and directions on /visit/ (the meta description promises "directions", but the page has none).

### 18. No social sharing metadata
- **URLs:** All pages
- **Evidence:** No `og:*` or `twitter:*` tags anywhere.
- **Fix:** Add og:title, og:description, og:image, og:url, og:type and twitter:card, with a unique image for key pages.

### 19. Weak E-E-A-T signals on content
- **Evidence:** Blog posts name the author only in JSON-LD. No visible byline, date or bio on the page. The head roaster (Wayan Sudarma) is mentioned only on /about/ and has no profile page.
- **Fix:** Show visible author byline, published and updated dates and a short bio with credentials (Melbourne training, 12 years) on each post. Link the byline to an author page, and mirror this in schema.

---

## LOW (backlog)

### 20. No favicon
- /favicon.ico returns 404 and no `<link rel="icon">` is declared. Add one (it also appears in mobile search results).

### 21. Product pages lack a purchase path or trust content
- Product pages show prices in text but have no visible add-to-cart, shipping/returns information, reviews or related products, and the /cart/ URL referenced in robots.txt 404s. This is a conversion issue as well as a schema one (add `shippingDetails` and `hasMerchantReturnPolicy` when available).

### 22. Hreflang / language
- The site is English-only and targets Indonesia and tourists. If you add an Indonesian version, implement hreflang with x-default. Currently only `<html lang="en">` is set, which is correct.

### 23. AI-search readiness
- No /llms.txt (optional, and Google ignores it), but robots.txt has no AI-crawler policy. The content is well suited to citation (concise factual answers on brewing and sourcing), so make sure AI crawlers are allowed. Adding author bylines, dates and sources (see #19) helps most.

### 24. Missing custom 404 page
- Unknown URLs return the server default error page. Provide a branded 404 with links to coffee, shop and the blog (return a real 404 status).

---

## What is working
- Unique, descriptive titles and meta descriptions on almost every page (exceptions above).
- Self-referencing canonicals on most pages, valid viewport meta, `lang="en"`.
- Clear single H1 on most pages and substantial, original, expert body copy on the product, brewing and about pages.
- Image width/height attributes are set, and product images have good alt text.
- Sitemap exists and is declared in robots.txt.
- Clean, readable URL structure.

## Suggested fix order
1. Week 1: items 1-4 (noindex on wholesale, /shop/ canonical, nav redirect chain, CSS block).
2. Week 1-2: items 5-11 (broken link, sitemap, Product schema, merge duplicate posts, headings, orphan pages, duplicate title).
3. Month 1: items 12-19 (images, titles, stale content, schema, OG tags, E-E-A-T).
4. Backlog: items 20-24.
