# SEO Audit: Kopi Kita (https://kopikita.test/)

Audited 2026-10-22 against the local copy at http://localhost:8765/. I fetched all 19 sitemap URLs, `robots.txt`, `sitemap.xml`, `llms.txt`, the redirect targets and the main images.

**Scope and limits.** This is a static-HTML review. I did not run Lighthouse or a browser, so there are no Core Web Vitals field data, no rendered-DOM checks and no Search Console or backlink data. Python's SimpleHTTP server is serving the local copy, so response headers (HSTS, compression, caching, security headers) say nothing about production. Check those on the real host. Business type: local-led specialty coffee roaster and cafe with a small online shop (Ubud, Bali).

**Overall:** the on-page basics are mostly sound. Pages have unique titles, descriptions and canonicals, and the content is substantive. The site has a few high-impact crawl and indexation faults, and a cluster of content and schema problems.

---

## Critical (fix now)

### 1. Wholesale page is set to noindex
- **URL:** `/wholesale/`
- **Found:** `<meta name="robots" content="noindex, follow">`. The page is in the sitemap, linked from the main nav and the homepage, and has a self-canonical.
- **Why it matters:** It's the B2B landing page ("30+ cafes, villas and hotels", free training, next-day delivery). With noindex it can't rank for "wholesale coffee Bali", so one of the site's most valuable lead sources is invisible in search. The noindex also contradicts the sitemap and canonical.
- **Fix:** Remove the meta robots tag, or set `index, follow`. If it was a staging leftover, check the deploy template for the same tag elsewhere. Then request reindexing in Search Console.

### 2. Shop page canonicalises to /coffee/
- **URL:** `/shop/`
- **Found:** `<link rel="canonical" href="https://kopikita.test/coffee/">`. The page has its own title, description and unique content (gear, drip bags, free-shipping threshold).
- **Why it matters:** Google will likely treat `/shop/` as a duplicate and drop it from the index. It has no chance to rank for "buy coffee beans" or "brewing gear". It is also in the sitemap, which sends a mixed signal.
- **Fix:** Set the canonical to `https://kopikita.test/shop/`. If `/shop/` really is meant to be merged into `/coffee/`, 301-redirect it, and remove it from the sitemap and nav.

### 3. Sitemap lists a URL that returns 404
- **URL:** `/coffee/sumatra-mandheling/` (listed in `sitemap.xml`)
- **Found:** HTTP 404. No page links to it.
- **Why it matters:** Error URLs in a sitemap waste crawl budget, make the sitemap look unreliable and show up as "Submitted URL not found (404)" in Search Console.
- **Fix:** Publish the product page, or remove the entry. If the product exists under another URL, use that URL and 301 the old one.

### 4. Main nav link goes through a redirect chain, and the sitemap uses a different URL
- **URLs:** `/menu/` → `/cafe/` → `/visit/`. The nav uses `/menu/` on every page. The sitemap and the About page use `/visit/`.
- **Found:** Two chained 301s on a site-wide link. The cafe page is the one a local business most needs found.
- **Why it matters:** Every page sends internal link equity through two hops, and slows crawling. The extra hop adds latency for users. Chains longer than one hop are discouraged.
- **Fix:** Change the nav link to `/visit/` on every template. Point `/menu/` and `/cafe/` directly at `/visit/` with a single 301 each. Also check the no-trailing-slash version `/visit`.

---

## High (fix within a week)

### 5. Duplicate / cannibalising blog posts
- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Found:** Both target "how to make pour over coffee". Both give the same recipe (15g / 250g / 93C / 40g bloom / about 3 minutes) and the same advice. They're listed one after another on the blog index, and the second post has almost the same intro.
- **Why it matters:** Two posts competing for the same query split rankings, and Google often picks neither well.
- **Fix:** Pick one as the main page. Either merge the beginner material into the stronger one and 301 the other, or reposition one clearly (for example, "gear and beginner mistakes" vs "step-by-step recipe") and change its title, H1 and intro to match. Cross-link them with different anchor text.

### 6. Broken internal link to a missing product page
- **URL affected:** `/blog/how-to-brew-pour-over/` links to `/coffee/aceh-gayo/`, which returns 404.
- **Why it matters:** Broken links hurt users and waste link equity. It's in a conversion sentence ("try our Aceh Gayo").
- **Fix:** Remove the link or point it to a live coffee (for example `/coffee/flores-bajawa/`). Add a link check to the deploy process.

### 7. Contact page has no canonical; About page has no meta description
- **URLs:** `/contact/` (no canonical) and `/about/` (no meta description).
- **Why it matters:** Without a description Google writes its own snippet for `/about/`. Without a canonical, `/contact/` leaves duplicate-URL variants (trailing slash, query strings) unresolved, and it's a key local-intent page.
- **Fix:** Add `<link rel="canonical" href="https://kopikita.test/contact/">` to `/contact/`. Add a description of about 150 characters to `/about/` (for example, "Kopi Kita started in 2019 with a 1kg roaster in Ubud. We pay farmer groups in Bali, Java and Flores above market price, before harvest.").

### 8. Product schema is incomplete and invalid for rich results
- **URLs:** `/coffee/bali-kintamani/`, `/coffee/java-ijen/`. `/coffee/flores-bajawa/` has no schema at all.
- **Found:**
  - Kintamani's Product has no `name`. Ijen has one.
  - Neither has `sku`, `url`, review or rating data, or `priceValidUntil`, and the offers have no `url`.
  - Prices are written as plain strings and don't include 1kg variants, although the page lists them.
  - Flores Bajawa (a live, indexable product page) has no Product markup.
- **Why it matters:** Google requires `name` for Product, so the Kintamani markup is invalid and gets no merchant or product snippet.
- **Fix:** Add `name` to Kintamani, and add `sku`, `offers.url` and (once real reviews exist) `aggregateRating`. Add a full Product block to Flores Bajawa. Add `priceSpecification` or two Offers for the 250g and 1kg sizes. Validate in the Rich Results Test.

### 9. Homepage hero image has no alt text and is not optimised
- **URL:** `/` (`/assets/img/hero-beans.jpg`)
- **Found:** `<img>` has width and height (good, no layout shift) but no `alt`. The file is 13.8 KB, which is small, so the hero is possibly a placeholder.
- **Why it matters:** Missing alt is an accessibility failure and loses image-search context on the page that matters most.
- **Fix:** Add `alt="Freshly roasted Kopi Kita coffee beans"`. If this image is the LCP element, don't lazy-load it and consider `fetchpriority="high"`.

### 10. About page hero image is 1.8 MB
- **URL:** `/about/` (`/assets/img/roastery-hero.jpg`, 1,818,123 bytes, 2400x1600)
- **Why it matters:** It's a likely LCP element and a heavy download for mobile users in Indonesia. It will probably fail the 2.5 s LCP target on a typical mobile connection.
- **Fix:** Resize to the largest displayed width, serve WebP or AVIF (target under 200 KB), add `srcset`/`sizes`, and keep the explicit width and height.

### 11. Organization schema is thin, and no LocalBusiness / Cafe markup
- **URL:** `/` (and the contact and visit pages)
- **Found:** Organization with name, URL, logo and address only. There is no phone, `sameAs`, opening hours, geo, `priceRange` or `servesCuisine`.
- **Why it matters:** The business is a physical roastery cafe, and local features depend on consistent, machine-readable name, address and phone data. The phone `+62 812 0000 0000` and hours (7am-5pm daily) exist only as page text.
- **Fix:** Add a `CafeOrCoffeeShop` (LocalBusiness subtype) block on `/visit/` or the homepage with `telephone`, `openingHoursSpecification`, `geo`, `image`, `url` and `sameAs` (Instagram, Google Business Profile). Keep NAP identical to the Google Business Profile and the footer. Also confirm the logo is at least 112x112 and the file actually renders (it returns 200).

---

## Medium (fix within a month)

### 12. Duplicate title tags
- **URLs:** `/coffee/` and `/subscriptions/` both use "Single-Origin Indonesian Coffee | Kopi Kita".
- **Why it matters:** The subscriptions page has a title that doesn't describe it, which hurts relevance and click-through, and creates a cannibalisation signal.
- **Fix:** Change the subscriptions title to something like "Coffee Subscriptions: Fresh Beans Every 2 or 4 Weeks | Kopi Kita".

### 13. Visit page has no H1 and a thin heading structure
- **URL:** `/visit/`
- **Found:** The page starts with `<h2>Opening hours</h2>`. No `<h1>`. Content is short (about 100 words), with no address block, map or phone number.
- **Why it matters:** The page is a primary local-intent page and has no primary heading for the query "coffee roastery Ubud". Content is thin for the page type.
- **Fix:** Add `<h1>Visit our roastery cafe in Ubud</h1>`. Add the full address, phone, an embedded map link, parking and getting-there notes, and the Saturday cupping details with a date schema if you run it as an event.

### 14. Brewing guide has two H1s
- **URL:** `/coffee/brewing-guide/` ("Coffee brewing guide" and "Brew methods")
- **Fix:** Demote the second to `<h2>`. Use `<h2>`/`<h3>` for the grind, water and troubleshooting subsections that are currently bold paragraphs.

### 15. Blog post and title/date inconsistencies
- **URL:** `/blog/best-coffee-beans-2024/`
- **Found:** The URL and title say "2024 Guide", while the schema headline says "The best coffee beans in Bali", the body says "Our picks this year" and the page was modified 2026-09-01.
- **Why it matters:** An out-of-date year in the title and URL signals stale content to users, and lowers click-through in late 2026.
- **Fix:** Remove the year from title and H1, or update to 2026. Keep the URL, or move to `/blog/best-coffee-beans-bali/` with a 301 and update the sitemap. Add visible "Updated" dates.

### 16. Thin blog post
- **URL:** `/blog/cold-brew-at-home/`
- **Found:** About 80 words and one paragraph. No schema, no author, no date, no images. Compare the other posts at 400+ words with Article markup.
- **Fix:** Expand to a real guide (ratios, steeping time, concentrate vs ready to drink, storage, troubleshooting) of at least 600 words, with an author and dates, plus Article schema. Link to it from the brewing guide, which mentions cold brew.

### 17. Article schema gaps
- **URLs:** the three posts that have schema (`/blog/how-to-brew-pour-over/`, `/blog/pour-over-coffee-guide/`, `/blog/best-coffee-beans-2024/`)
- **Found:** No `image`, no `publisher`, no `mainEntityOfPage`, and the author has no `url` (no author page exists). Headlines differ from the on-page H1s ("Pour over coffee: a guide for beginners" vs title tag).
- **Fix:** Add `image`, `publisher` (the Organization), `mainEntityOfPage`, and an author URL pointing to a short author bio on `/about/` (Wayan Sudarma has real credentials: 12 years of roasting, Melbourne training). That also supports E-E-A-T.

### 18. Sitemap quality
- **URL:** `/sitemap.xml`
- **Found:** No `<lastmod>` on any entry. It contains the 404 URL (issue 3) and a noindex page (issue 1) and a page whose canonical points elsewhere (issue 2). `/coffee/flores-bajawa/` is present but is unlinked from any page I fetched.
- **Fix:** Generate the sitemap from the site's real indexable, 200, self-canonical URLs only, with accurate `lastmod` dates. Fix the issues above first, then resubmit.

### 19. Orphaned / under-linked pages
- **URLs:** `/coffee/flores-bajawa/` (no inbound links from the pages I fetched; the Coffee and Shop pages link only to Kintamani and Ijen), and `/blog/cold-brew-at-home/` (only from the blog index).
- **Fix:** Link Flores Bajawa from `/coffee/`, `/shop/` and the homepage. Add contextual links from blog posts to the relevant product, and from product pages to the relevant guides.

### 20. Non-descriptive homepage and anchor patterns
- **URL:** `/`
- **Found:** The homepage body links only to a few pages. It has no link to `/shop/` or `/subscriptions/` outside the nav, and no clear call to action. Some anchor text is generic ("blog", "Contact").
- **Fix:** Add a short product/feature section with descriptive links to the best sellers, the subscription and the cafe page.

### 21. Missing 404 page design and soft signals
- **URL:** any missing URL (for example `/nope-xyz`)
- **Found:** It returns a correct 404 status, but with the server's default error page, with no navigation or links back into the site.
- **Fix:** Serve a branded 404 with the nav and links to the shop, coffee and blog. Keep the 404 status.

---

## Low (backlog)

### 22. robots.txt blocks CSS
- **URL:** `/robots.txt` has `Disallow: /assets/css/`
- **Why it matters:** Google needs CSS to render pages and judge mobile-friendliness. It's a small file today, but it's a known anti-pattern. (`Disallow: /cart/` is fine; the cart does not exist yet.)
- **Fix:** Remove the CSS disallow. Keep the sitemap line.

### 23. No Open Graph or Twitter card tags
- **URLs:** every page
- **Fix:** Add `og:title`, `og:description`, `og:image`, `og:url`, `og:type` and `twitter:card`. Make a branded 1200x630 share image. Social previews affect click-through from WhatsApp, Instagram and Facebook, which matter for a local cafe.

### 24. No favicon and a missing icon link
- **URL:** every page. No `<link rel="icon">`, and `/favicon.ico` was not tested. The logo file exists at `/assets/img/logo.png`.
- **Fix:** Add a favicon set (32x32, 180x180 Apple touch icon) and link it in the head.

### 25. FAQPage markup on /coffee/
- **URL:** `/coffee/` (informational)
- **Found:** FAQPage JSON-LD with two questions. The questions and answers do not appear visibly on the page, which breaks the rule that markup must match visible content.
- **Note:** Google retired FAQ rich results for all sites on 7 May 2026, so there's no SERP benefit. It's harmless but not worth maintaining. Either show the Q&A on the page (it's useful content) or leave the markup as is. I'm not recommending adding any new FAQ markup for Google.

### 26. Language / region signals
- **URL:** every page. `lang="en"` is set. The audience is in Indonesia, and the shipping and contact copy speaks to Indonesian buyers.
- **Fix:** Consider an Indonesian version (`/id/`) with hreflang if there is demand. Not needed if all customers read English. Skip otherwise.

### 27. AI / agent readiness
- **URLs:** `/llms.txt` returns 404.
- **Found:** `robots.txt` has no AI-crawler rules. There's no Markdown version of pages.
- **Why it matters:** `llms.txt` is optional and Google Search ignores it, so this is low value. The pages are server-rendered plain HTML with clear text and descriptive headings, so they're easy for AI systems to read.
- **Fix:** Optional. If you want it, add a short `llms.txt` listing the main pages. Decide on a deliberate policy for AI crawlers in `robots.txt`.

### 28. Production-only checks I couldn't do locally
Confirm on the live host: HTTPS with a valid certificate and HTTP→HTTPS redirect, a single canonical host (www vs non-www), HSTS, compression (gzip/Brotli), long-lived cache headers on `/assets/`, and the trailing-slash policy (`/visit` vs `/visit/`). The canonical and sitemap URLs use `https://kopikita.test/`, which matches the stated production domain.

---

## What's working
- Every page has a unique, sensible `<title>`, apart from the duplicate in issue 12.
- All pages except `/contact/` have a self-referencing canonical, and `/shop/` is the exception for the wrong reason.
- Meta viewport and `lang` are set everywhere.
- Images have explicit width and height, so there is no layout shift, and product images have descriptive alt text.
- Content is original, specific and experience-based (named farmer groups, altitudes, varieties, recipes).
- Pages are server-rendered HTML, so crawling doesn't depend on JavaScript.
- Product pages have clear prices and tasting notes, and the nav is crawlable plain links.

## Suggested fix order
1. Remove the wholesale noindex (1), fix the `/shop/` canonical (2).
2. Fix the sitemap (3, 18) and the nav redirect chain (4). Fix the broken Aceh Gayo link (6).
3. Resolve the two pour-over posts (5), then the schema (8, 11, 17).
4. Image and alt fixes (9, 10), then the titles, H1s and thin pages (12 to 16).
5. Everything under Low.

After the critical fixes, recrawl, resubmit the sitemap in Search Console, and watch the Pages report for `/wholesale/` and `/shop/` moving to "Indexed". If neither appears within about two weeks, the fix hasn't taken effect.
