# Technical SEO Audit: kopikita.test

> Audit date 2026-10-22 · Source: live curl crawl of http://localhost:8766/ (28 URLs: every sitemap URL, every nav/body link, robots.txt, sample assets) · Run via the `seo-technical-audit` skill.

## Scope and limits

- **Not run:** SE Ranking audit/MCP, Firecrawl (JS render), CrUX, GSC and PageSpeed data were not available in this session. Findings come from raw HTML and HTTP headers only. There is no health score or field Core Web Vitals data.
- **Environment caveat:** the site is served by Python's `SimpleHTTP` dev server over HTTP. Items that depend on production infrastructure (HTTPS and www redirects, compression, caching, security headers) are marked **verify on production**. The production domain can't be reached from here.
- **JS-rendered content:** I read the JS by hand and didn't execute it. I describe what raw HTML contains versus what scripts inject.

## Summary

| Severity | Count |
|---|---|
| Critical | 3 |
| High | 6 |
| Medium | 9 |
| Low | 6 |

## Priority fix list

| # | Issue | Sev | URL(s) | Effort |
|---|---|---|---|---|
| 1 | Revenue page `/subscriptions/` sends `X-Robots-Tag: noindex` | Critical | /subscriptions/ | S |
| 2 | Canonical loop on Java Ijen product page | Critical | /coffee/java-ijen/ | S |
| 3 | `/gifts/` is a soft 404 and is linked from every page | Critical | /gifts/ (sitewide nav) | S |
| 4 | Sitemap is contradictory (noindex, robots-blocked, canonicalised and future-dated URLs) | High | /sitemap.xml | S |
| 5 | Gift-box content exists only in JS | High | /coffee/gift-box/ | S |
| 6 | Internal links to a 302 redirect | High | /coffee/kintamani/ | S |
| 7 | Limited-release page is orphaned (button `onclick`, not in sitemap) | High | /coffee/limited-release/ | S |
| 8 | Product schema price disagrees with page; Article JSON-LD is invalid | High | /coffee/bali-kintamani/, /blog/how-to-brew-pour-over/ | S |
| 9 | Hreflang is broken (`in`, no return tag, no x-default) | High | /id/, / | S |
| 10 | Duplicate and wrong meta descriptions | Medium | Flores, Kintamani 250g/1kg | S |
| 11 | Near-duplicate Kintamani 250g/1kg pages | Medium | /coffee/bali-kintamani/, /coffee/bali-kintamani-1kg/ | M |
| 12 | Blog pagination canonicalised to page 1 | Medium | /blog/page/2/ | S |
| 13 | Mixed content (http image and iframe) | Medium | /contact/ | S |
| 14 | `/visit/` has no viewport meta | Medium | /visit/ | S |
| 15 | Hero image is lazy-loaded (LCP); About gallery is lazy-loaded via JS only | Medium | /, /about/ | S |
| 16 | `rel="nofollow"` on an internal link in the global nav | Medium | /wholesale/ (sitewide) | S |
| 17 | Missing LocalBusiness and other structured data | Medium | /visit/, /contact/, / | M |
| 18 | `/coffee/samples/` is robots-blocked but in the sitemap, thin and indexable | Medium | /coffee/samples/ | S |
| 19 | Security headers absent | Low | all | S |
| 20 | Other low-priority items (OG tags, favicon, thin hubs, breadcrumbs, 404 page) | Low | various | S–M |

---

## Critical

### 1. `/subscriptions/` is noindexed by an HTTP header
- **URL:** https://kopikita.test/subscriptions/
- **Evidence:** the response carries `X-Robots-Tag: noindex`. The HTML has no robots meta, so the directive is easy to miss in a view-source check. The page is a main nav item and a sitemap URL, has a self-canonical, and sells a recurring product ("from Rp 165,000 per delivery").
- **Why it matters:** Google will drop the page from the index, or never index it. You lose all organic traffic for "coffee subscription Bali / Indonesia" queries on your highest-LTV offer. The sitemap and nav tell Google to index it while the header tells it not to.
- **Fix:** remove the header at the server, CDN or app level. Look for a leftover staging rule or a path-based header rule. Re-test with `curl -I`, then request indexing in Search Console. Add a monitor or CI check that fails if any sitemap URL returns `X-Robots-Tag: noindex`.

### 2. Canonical loop on Java Ijen
- **URL:** https://kopikita.test/coffee/java-ijen/
- **Evidence:** the page returns 200 and declares `<link rel="canonical" href="https://kopikita.test/coffee/ijen/">`. `/coffee/ijen/` returns a 301 back to `/coffee/java-ijen/`. The sitemap, the nav and homepage links, and the Product schema all use `/coffee/java-ijen/`.
- **Why it matters:** canonical points to a URL that redirects to the page itself. Google gets contradictory signals and may ignore the canonical, or may pick the wrong URL as the indexed version. One of your two flagship products is exposed to this.
- **Fix:** change the canonical to `https://kopikita.test/coffee/java-ijen/` (self-referencing). Check for a template that builds canonicals from an old slug. Keep the 301 from `/coffee/ijen/`.

### 3. `/gifts/` is a soft 404 and sits in the global nav
- **URL:** https://kopikita.test/gifts/ (linked from every page in the header nav)
- **Evidence:** it returns `200 OK` with the title "Page not found | Kopi Kita" and a "Sorry, we couldn't find the page" body. It has no canonical and no meta description. A truly missing URL (`/nonexistent/`) returns a correct 404, so the 404 template is being served with a 200 for this route. The real gift page is `/coffee/gift-box/`.
- **Why it matters:** Google reports it as a soft 404 and wastes crawl budget on it. Sitewide internal links point users and link equity to an error page, and users who click "Gifts" land on a dead end.
- **Fix:** pick one. Either 301 `/gifts/` to `/coffee/gift-box/` (the simplest), or build a real gifts landing page (gift box, gift subscriptions, which the subscriptions page mentions). Then fix the route so it returns the correct status. Update the nav link.

## High

### 4. Sitemap is contradictory and carries bad dates
- **URL:** https://kopikita.test/sitemap.xml
- **Evidence:**
  - Every `<lastmod>` is `2027-03-01`, which is in the future (today is 2026-10-22). They are all identical, so they carry no information.
  - It lists `/subscriptions/` (noindex header), `/coffee/samples/` (disallowed in robots.txt), and `/blog/page/2/` (canonical points to `/blog/`). None of these belong in a sitemap.
  - It omits `/coffee/limited-release/`, an indexable, canonical page.
- **Why it matters:** Google treats sitemap URLs as "I want this indexed", so conflicting signals erode trust in the file. Invalid or untrustworthy lastmod values make Google ignore lastmod across the whole site. A real page you want found is missing.
- **Fix:** generate lastmod from the real last-modified date of each page. Include only 200, indexable, self-canonical URLs. Remove `/subscriptions/` (after un-noindexing it, put it back), `/coffee/samples/` and `/blog/page/2/`; add `/coffee/limited-release/`.

### 5. Gift-box content is rendered only by JavaScript
- **URL:** https://kopikita.test/coffee/gift-box/
- **Evidence:** in the raw HTML, `<div id="product-description"></div>` is empty. All the copy (what's in the box, the Rp 295,000 price, shipping) is written by an inline script via `innerHTML`. The raw HTML has only the `<h1>`. There is no Product schema.
- **Why it matters:** the raw HTML is thin, and everything indexable depends on render. Google usually renders JS, but later and less reliably. Other crawlers (Bing's AI features, most LLM crawlers, social scrapers) don't execute JS and see an empty page.
- **Fix:** put the text in the HTML server-side. Add Product + Offer JSON-LD. If the script is only a demo, remove it.

### 6. Internal links point to a 302 redirect
- **URL:** https://kopikita.test/coffee/kintamani/ (302 to `/coffee/bali-kintamani/`)
- **Linked from:** the homepage ("Bali Kintamani natural" in the best-seller paragraph), `/blog/cold-brew-at-home/`, `/blog/best-coffee-beans-bali/`.
- **Why it matters:** a 302 is a temporary redirect, so Google may keep the old URL and not consolidate signals. Every click and crawl costs an extra hop. The links come from the homepage and two blog posts, so the redirect adds hops on important paths.
- **Fix:** change the three links to `/coffee/bali-kintamani/`. If the old URL is permanently retired, make the redirect a 301.

### 7. Limited-release page is orphaned
- **URL:** https://kopikita.test/coffee/limited-release/
- **Evidence:** the only reference is a `<button onclick="location.href='/coffee/limited-release/'">` on `/coffee/`. It is not an `<a href>`, not in the sitemap and not linked anywhere else. The page itself is fine (200, canonical, description).
- **Why it matters:** Google doesn't reliably follow `onclick` navigation, so the page is effectively undiscoverable. A seasonal drop with scarcity messaging and a price has no way to rank or earn link equity.
- **Fix:** replace the button with `<a href="/coffee/limited-release/">`, add the URL to the sitemap and link it from `/shop/`. When the release ends, keep the URL and mark it sold out rather than deleting it.

### 8. Structured data errors
- **URLs:** /coffee/bali-kintamani/, /blog/how-to-brew-pour-over/, plus gaps on other pages.
- **Evidence:**
  - `/coffee/bali-kintamani/` Product schema has `"price": "145000"`. The visible page says Rp 165,000 for 250g (Rp 520,000 for 1kg). This is a price mismatch (the Ijen and 1kg pages match).
  - `/blog/how-to-brew-pour-over/` Article JSON-LD ends `"author": {...},}` with a trailing comma. That is invalid JSON, so the whole block fails to parse and the page gets no Article markup.
  - Both Article blocks have no `image` or `publisher`. Product blocks have no `sku` and the Offers have no `url`, `shippingDetails`, `hasMerchantReturnPolicy`, or `priceValidUntil`.
  - `/coffee/flores-bajawa/` has a product page but no Product schema, and `/blog/cold-brew-at-home/` has no Article schema.
- **Why it matters:** a price in the markup that differs from the page can lead to a Merchant Center / rich-result policy flag and a loss of price rich results. Invalid JSON means no rich result at all.
- **Fix:** correct the Kintamani price to 165000 and generate the schema price from the same source as the visible price. Remove the trailing comma and validate every block in the Rich Results Test. Add the missing properties and add Product/Article schema to the pages that lack it.

### 9. Hreflang is wrong and incomplete
- **URLs:** https://kopikita.test/id/ and https://kopikita.test/
- **Evidence:** `/id/` declares `hreflang="in"` (legacy, deprecated code for Indonesian; the valid code is `id`) and `hreflang="en"`. The English homepage has no hreflang tags at all, so there are no return links. There is no self-reference on the English page and no `x-default`. The Indonesian page nav is in English and links to English pages; it is a one-page translation.
- **Why it matters:** hreflang only works when both pages reference each other, and Google ignores an invalid code. Google may show the wrong language version to Indonesian searchers.
- **Fix:** on both `/` and `/id/` add the full set: `hreflang="en"` (self on `/`), `hreflang="id"` (not `in`) and `hreflang="x-default"` pointing at `/`. Either translate the nav and key pages (shop, coffee, visit) or drop the Indonesian page until there is more content. Add `/id/` to the sitemap with `xhtml:link` alternates if you keep it.

## Medium

### 10. Duplicate and incorrect meta descriptions
- **/coffee/flores-bajawa/** uses the Java Ijen description verbatim ("Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon and black tea…"), but this page is a honey-process coffee from Flores. It is both a duplicate and factually wrong.
- **/coffee/bali-kintamani/ and /coffee/bali-kintamani-1kg/** share the same description.
- **Why it matters:** Google may rewrite them, and the snippet will mislead searchers.
- **Fix:** write unique descriptions. For Flores: "Honey-process coffee from Bajawa, Flores. Notes of dark chocolate, red apple and clove. Roasted to order in Ubud."

### 11. Kintamani 250g and 1kg are near-duplicate pages
- **URLs:** https://kopikita.test/coffee/bali-kintamani/ and https://kopikita.test/coffee/bali-kintamani-1kg/
- **Evidence:** the body text, image and description are identical. Both pages list both prices ("Rp 165,000 for 250g. Rp 520,000 for 1kg."), and each self-canonicals. The other coffees keep both sizes on one page.
- **Why it matters:** two pages compete for the same queries and split links. It's also inconsistent with Ijen and Flores.
- **Fix:** best option is one product page with a size selector (variants), with the 1kg URL 301-redirecting to it. If you keep separate pages, canonicalise the 1kg to the main page or differentiate its content (cafe/household use, price per kg).

### 12. Blog pagination canonicalised to page 1
- **URL:** https://kopikita.test/blog/page/2/
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/blog/">`. Page 1 lists only two posts; `/blog/cold-brew-at-home/` is linked only from page 2. Page 2 is also in the sitemap.
- **Why it matters:** canonicalising paginated pages to page 1 can stop Google from following links on page 2, so posts that only appear there may get discovered slowly or not at all. Mixed signals with the sitemap.
- **Fix:** give page 2 a self-referencing canonical. With so few posts, show all posts on `/blog/` and drop the pagination. Link every post from the blog index.

### 13. Mixed content on Contact
- **URL:** https://kopikita.test/contact/
- **Evidence:** `<img src="http://kopikita.test/assets/img/storefront.jpg">` and `<iframe src="http://maps.example.com/embed?...">` use `http://` on a site served over https in production.
- **Why it matters:** browsers block the insecure iframe (map doesn't load) and may block or warn on the image. Mixed content weakens the security signal and breaks the main local-intent page.
- **Fix:** use https (or protocol-relative/root-relative for the image) and an https embed URL. Note `maps.example.com` looks like a placeholder; replace it with the real Google Maps embed.

### 14. No viewport meta on /visit/
- **URL:** https://kopikita.test/visit/
- **Evidence:** the head has charset, description and canonical, but no `<meta name="viewport">`. Every other page has one.
- **Why it matters:** Google indexes mobile-first. Without a viewport the page renders at desktop width on phones, and it fails mobile-friendliness checks. This is the page people use to find the cafe on their phones.
- **Fix:** add `<meta name="viewport" content="width=device-width, initial-scale=1">` (fix it in the shared head template).

### 15. Image loading issues
- **/**: the hero image (`hero-beans.jpg`, the first and largest element) has `loading="lazy"`. Lazy-loading the LCP image delays LCP. Fix: remove `loading="lazy"` and add `fetchpriority="high"`; reserve lazy for below-the-fold images.
- **/about/**: three gallery images have no `src`, only `data-src`, and a custom IntersectionObserver sets the source. Crawlers that don't scroll or run the script won't see the images, so they won't be indexed in image search. The script also creates one observer per image and disconnects the observer on the first intersection. Fix: use plain `<img src=… loading="lazy" width height>` and delete the script.
- Images have good alt text and width/height attributes, which is a plus. No `srcset` or modern formats (WebP/AVIF) are in use; add them when you can.

### 16. Internal `nofollow` on Wholesale in the global nav
- **URL:** /wholesale/ (every page's nav has `<a href="/wholesale/" rel="nofollow">`)
- **Why it matters:** nofollow on your own pages wastes internal link equity and tells Google you don't trust a page that is a lead-gen revenue page. The homepage body links to it without nofollow, so the signals are inconsistent.
- **Fix:** remove `rel="nofollow"`.

### 17. Missing structured data for local business and site entities
- **URLs:** /visit/, /contact/, / (and sitewide)
- **Evidence:** only the homepage has Organization schema (name, logo, address; no `sameAs`, phone, email). The cafe has hours, an address, a phone number and weekly events, but no `LocalBusiness`/`CafeOrCoffeeShop` markup. No `BreadcrumbList`, `WebSite`, or Open Graph/Twitter tags on any page.
- **Why it matters:** local pack and knowledge-panel eligibility, plus better entity understanding for AI search.
- **Fix:** add `CafeOrCoffeeShop` JSON-LD with `openingHoursSpecification` (07:00–17:00 daily), `telephone`, `geo` and `sameAs` (Google Business Profile, Instagram). Add `BreadcrumbList` to the product and blog pages and OG/Twitter tags to the templates. Make sure NAP (Jl. Raya Sayan 12) matches Google Business Profile exactly.

### 18. `/coffee/samples/` conflicts across robots, sitemap and content
- **URL:** https://kopikita.test/coffee/samples/
- **Evidence:** robots.txt has `Disallow: /coffee/samples/`, yet it's in the sitemap, is indexable (no noindex) and has a self-canonical. It's about 35 words and is not linked from anywhere (the wholesale page tells people to use the contact form instead). The URL sits in `/coffee/` even though it's a wholesale offer.
- **Why it matters:** a robots-disallowed URL can still be indexed from links (with no snippet), and Google can't see any noindex on a blocked page. A sitemap URL that can't be crawled shows up as a Search Console warning.
- **Fix:** decide whether the page should exist. If not, delete it (410) and remove the robots rule and sitemap entry. If it should be found, remove the Disallow, link it from `/wholesale/` and expand it. If it should be hidden, keep the Disallow, drop it from the sitemap and use `noindex` on a crawlable page instead.

## Low

### 19. Security headers (verify on production)
No response header shows `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy` or `X-Frame-Options`. The `Server: SimpleHTTP/0.6 Python/3.9.6` header discloses versions. This is probably the dev server, so confirm on production. Add HSTS (and preload once stable), `nosniff`, a `strict-origin-when-cross-origin` Referrer-Policy, and a CSP with `frame-ancestors`. Mostly a trust and security point rather than a direct ranking factor.

### 20. Other items
- **Thin hubs:** `/shop/` (~100 words) names drip bags, V60 drippers, a grinder and a scale, but has no product links or product pages for any of them; it doesn't link Flores Bajawa either. `/coffee/` lists only two of the three coffees; **Flores Bajawa is linked only from a blog post**, so it is nearly orphaned. Add all three coffees to `/coffee/` and `/shop/`.
- **`/id/`:** about 50 words and a nav that links to English pages.
- **Blog:** posts don't show an author or date on the page (only in schema), and only one post has a Person author with no profile URL. Add visible bylines and dates and link authors to `/about/` for E-E-A-T. `/blog/` only lists two posts.
- **No breadcrumbs** on product or blog pages, and the footer has no navigation links.
- **No favicon:** `/favicon.ico` returns 404 and there's no `<link rel="icon">`.
- **404 page:** a missing URL returns a correct 404, but the server's default error page has no nav or branding. Serve the branded 404 template (the one currently leaking onto `/gifts/`) with a 404 status.
- **robots.txt:** valid, and the Sitemap line is correct. `/cart/` is disallowed but doesn't exist. There are no AI-crawler rules (GPTBot, ClaudeBot, etc.), so they are allowed by default; decide whether that's intended.
- **Performance and delivery (verify on production):** responses show no `Content-Encoding`, `Cache-Control` or `ETag`. Confirm gzip/brotli and long-lived caching for `/assets/` in production, and get real Core Web Vitals from CrUX/PageSpeed once the site is live.
- **HTTPS/www redirects:** couldn't be tested against `.test`. Confirm that http→https and the non-canonical host both 301 to `https://kopikita.test/`.

## What's working

- Every page has a unique, well-sized `<title>` and a single H1. `<html lang>` is set.
- Self-referencing absolute canonicals on all pages except the two noted (Ijen, blog page 2).
- Internal links use clean, descriptive, trailing-slash URLs. `/coffee/ijen/` → `/coffee/java-ijen/` is a proper 301. Real 404s work.
- Image alt text and dimensions are present on all content images (all asset URLs I tested return 200).
- robots.txt is reachable and doesn't block anything important (aside from the samples conflict), and it declares the sitemap.
- Content on the blog and brewing guide is substantive (hundreds of words, specific numbers, internal links to products).

## Recommended order of work

1. **Today (1–3 hours):** items 1–3 (remove noindex header, fix Ijen canonical, fix `/gifts/`), then rebuild the sitemap (4) and request indexing for `/subscriptions/` in Search Console.
2. **This week:** items 5–9 (gift-box HTML, 302 links, limited-release link, schema fixes, hreflang).
3. **Next two weeks:** items 10–18 (descriptions, Kintamani consolidation, pagination, mixed content, viewport, images, nofollow, local schema, samples page).
4. **Ongoing:** security headers, content depth on hubs, and a monthly re-run of this audit. Add automated checks for noindex headers, canonical targets and sitemap validity to CI.
