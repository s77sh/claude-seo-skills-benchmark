# SEO Audit: Kopi Kita (kopikita.test)

Audited 2026-10-22 against the local copy at http://localhost:8766/. The audit covers every URL in the sitemap (21), every internal link found, robots.txt, and the key assets. Findings come from raw HTML fetched with curl. No JavaScript rendering, Lighthouse or field data was available, so Core Web Vitals could not be measured (see "Not assessed").

**Business type:** local specialty coffee roaster with e-commerce (products, subscriptions, wholesale) and a physical cafe in Ubud, Bali. English site plus a small Indonesian page.

**Overall health: roughly 62/100.** The content is genuinely good: unique titles, clean canonicals on most pages, real expertise, and 700+ word articles. The score is dragged down by a handful of mistakes that cut off or contradict indexing signals: a broken canonical, a soft-404 linked from the nav, wrong hreflang, JS-only content and conflicting structured data.

Priority key: **Critical** = blocks indexing or sends wrong signals, fix now. **High** = fix within a week. **Medium** = within a month. **Low** = backlog.

---

## Critical

### 1. Java Ijen canonical points at a URL that redirects back
- **URL:** https://kopikita.test/coffee/java-ijen/ (also in the sitemap)
- **Found:** `<link rel="canonical" href="https://kopikita.test/coffee/ijen/">`. But `/coffee/ijen/` returns `301 → /coffee/java-ijen/`. The canonical and the redirect point at each other.
- **Why it matters:** this is one of two flagship products. Conflicting signals (the sitemap, internal links and the redirect say `java-ijen`; the canonical says `ijen`) force Google to guess. It may drop the page from the index or pick the redirecting URL, and a canonical that redirects is commonly ignored.
- **Fix:** set the canonical to `https://kopikita.test/coffee/java-ijen/` (self-referencing). Keep the 301 from `/coffee/ijen/`.

### 2. `/gifts/` is a soft 404 linked from every page's nav
- **URL:** https://kopikita.test/gifts/ (linked site-wide in the header)
- **Found:** HTTP 200, `<title>Page not found | Kopi Kita</title>`, with no canonical or description.
- **Why it matters:** a 200 on an error page is a soft 404. Google will flag it in Search Console, waste crawl budget, and treat a link on every page as pointing to junk. Users clicking "Gifts" hit a dead end.
- **Fix:** either build the page (the gift box at `/coffee/gift-box/` and gift subscriptions are the obvious content) or remove it from the nav. If a real page is not coming, return a true 404/410 status.

### 3. Hreflang on the Indonesian page is invalid and not reciprocal
- **URLs:** https://kopikita.test/id/ and https://kopikita.test/
- **Found:**
  - `/id/` declares `hreflang="in"`. The correct ISO 639-1 code is `id` (`in` is a deprecated legacy code that Google does not support).
  - The English homepage has **no** hreflang annotations at all, so `/id/` points to `/` but `/` does not point back. Hreflang requires return links or it is ignored.
  - No `x-default`.
- **Why it matters:** the Indonesian page will not be matched to Indonesian-language searchers, and the two pages may compete or be treated as duplicates.
- **Fix:** add the same set to both `/` and `/id/`:
  ```html
  <link rel="alternate" hreflang="en" href="https://kopikita.test/">
  <link rel="alternate" hreflang="id" href="https://kopikita.test/id/">
  <link rel="alternate" hreflang="x-default" href="https://kopikita.test/">
  ```
  Also add `/id/` equivalents to the sitemap with `xhtml:link` if you extend the Indonesian section. Note that `/id/` has only three short paragraphs; it is a stub, not a translated site.

### 4. Product schema contradicts the visible price
- **URL:** https://kopikita.test/coffee/bali-kintamani/
- **Found:** JSON-LD `offers.price` is `145000`, but the page body says "Rp 165,000 for 250g". (Subscriptions also quote Rp 165,000.)
- **Why it matters:** price mismatches between markup and page are a Merchant Listings / rich-result policy violation and can cause the product snippet to be suppressed or flagged.
- **Fix:** correct the schema to `165000` and generate JSON-LD from the same data source as the visible price so they cannot drift.

---

## High

### 5. Gift box description is injected by JavaScript
- **URL:** https://kopikita.test/coffee/gift-box/
- **Found:** raw HTML contains only `<div id="product-description"></div>`; all the text (what is in the box, Rp 295,000, shipping) is written in by an inline `innerHTML` script.
- **Why it matters:** the page is empty in the initial HTML. Google can render JS but indexing is delayed and less reliable, and many other crawlers and AI agents never run it. This is also a product page with no Product schema.
- **Fix:** put the description in the HTML. Add Product/Offer JSON-LD (price 295000 IDR).

### 6. About-page gallery images only load via JS and IntersectionObserver
- **URL:** https://kopikita.test/about/
- **Found:** three farm photos use `data-src` with no `src`; a script sets `src` on scroll.
- **Why it matters:** crawlers that do not scroll never see these images, so they are not indexed for image search, and they have no `src` fallback or `<noscript>`.
- **Fix:** use real `src` plus native `loading="lazy"` (width and height are already set, which is good).

### 7. Mixed content on the contact page
- **URL:** https://kopikita.test/contact/
- **Found:** `<img src="http://kopikita.test/assets/img/storefront.jpg">` and `<iframe src="http://maps.example.com/embed?...">` over plain HTTP, on an HTTPS site.
- **Why it matters:** browsers block or warn on insecure subresources, so the map and photo may not appear. It also undermines the HTTPS signal on the page that carries your NAP details.
- **Fix:** change both to `https://` (or protocol-relative root-relative paths for the image). Replace the `maps.example.com` placeholder with the real Google Maps embed.

### 8. Internal links go through redirects to the wrong URL
- **URLs:** https://kopikita.test/coffee/kintamani/ (302 → `/coffee/bali-kintamani/`); linked from the homepage, `/blog/cold-brew-at-home/` and `/blog/best-coffee-beans-bali/`
- **Found:** the homepage "best seller" link, and two blog posts, link to the redirecting URL. It is also a 302 (temporary), not a 301.
- **Why it matters:** every internal link pays a redirect hop, and a 302 tells Google the old URL may remain the canonical one, so link equity from your best content is not consolidated cleanly onto the product page.
- **Fix:** update the three links to `/coffee/bali-kintamani/`, and change the redirect to a 301 (or remove it).

### 9. Duplicate / wrong meta description on Flores Bajawa
- **URL:** https://kopikita.test/coffee/flores-bajawa/
- **Found:** description is "Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon and black tea..." which is the Java Ijen copy. Bajawa is a honey-process Flores coffee.
- **Why it matters:** the snippet misdescribes the product and duplicates another page, so it is likely to be rewritten by Google and will mislead searchers.
- **Fix:** write a unique one, e.g. "Honey-process coffee from Bajawa, Flores. Notes of dark chocolate, red apple and clove. Roasted to order in Ubud."

### 10. Two sitemap entries contradict robots.txt/canonicals
- **URLs:** https://kopikita.test/sitemap.xml
- **Found:**
  - `/coffee/samples/` is listed but blocked by `Disallow: /coffee/samples/` in robots.txt.
  - `/blog/page/2/` is listed, but its canonical points to `/blog/`.
- **Why it matters:** sitemaps should contain only indexable, canonical URLs. Blocked URLs trigger "Indexed, though blocked by robots.txt" / "Submitted URL blocked" warnings; the paginated page sends mixed signals.
- **Fix:** remove both from the sitemap. For pagination, give page 2 a self-referencing canonical rather than pointing it at page 1 (see issue 14). Decide whether the samples page should rank; if so, lift the robots block and add `noindex` only if you do not want it indexed (do not use both).

### 11. Sitemap `lastmod` dates are in the future and identical
- **URL:** https://kopikita.test/sitemap.xml
- **Found:** every URL has `<lastmod>2027-03-01</lastmod>`, which is after today (2026-10-22). Page content itself references 2026 dates (e.g. article `dateModified` 2026-08-02 and 2026-09-01).
- **Why it matters:** impossible dates make Google distrust the field, and identical values on every URL carry no information about what actually changed.
- **Fix:** emit the real last-modified date per page, from content changes, not build time.

### 12. Hero image is lazy-loaded
- **URL:** https://kopikita.test/ (homepage)
- **Found:** the 1200x700 hero `<img>` has `loading="lazy"` and is above the fold, so it is almost certainly the LCP element.
- **Why it matters:** lazy-loading the LCP image delays it and hurts the LCP score, a Core Web Vitals metric.
- **Fix:** remove `loading="lazy"` from the hero and add `fetchpriority="high"`. Keep lazy-loading for below-the-fold images.

### 13. Invalid JSON-LD on the pour-over article
- **URL:** https://kopikita.test/blog/how-to-brew-pour-over/
- **Found:** `"author": {...},}` has a trailing comma before the closing brace, so the block fails to parse. Article schema is therefore not recognised on one of the best-performing content pages.
- **Fix:** remove the trailing comma. Validate all JSON-LD in CI. Also add `image`, `publisher` and `mainEntityOfPage` to both Article blocks.

---

## Medium

### 14. Pagination and the cold-brew post are weakly linked
- **URLs:** https://kopikita.test/blog/, https://kopikita.test/blog/page/2/, https://kopikita.test/blog/cold-brew-at-home/
- **Found:** `/blog/` lists only 2 posts; `cold-brew-at-home` is reachable only via "Older posts" on page 2 (2 clicks deep), and page 2 canonicalises to `/blog/`, so Google may never treat page 2, and the links on it, as a discoverable path.
- **Fix:** link all three posts from `/blog/`, give page 2 a self-referencing canonical, and link the cold-brew post from the brewing guide and the Kintamani product page.

### 15. "Limited release" page is only reachable by a JavaScript button
- **URLs:** https://kopikita.test/coffee/ (button), https://kopikita.test/coffee/limited-release/
- **Found:** the only link is `<button onclick="location.href='/coffee/limited-release/'">`. There is no `<a href>`, and the page is not in the sitemap.
- **Why it matters:** Googlebot does not follow `onclick` navigation, so a live product page is effectively orphaned.
- **Fix:** use `<a href="/coffee/limited-release/">`, add it to the sitemap, and add Product schema (Rp 210,000 / 200g).

### 16. `rel="nofollow"` on an internal link to wholesale
- **URL:** https://kopikita.test/wholesale/ (nav link, every page)
- **Found:** the wholesale link in the site-wide nav has `rel="nofollow"`, yet the page is indexable and in the sitemap, and is a revenue page.
- **Why it matters:** it signals that you do not vouch for your own page and withholds internal link equity from it.
- **Fix:** remove `rel="nofollow"`.

### 17. Missing Open Graph / Twitter card tags and favicon
- **URLs:** all pages; https://kopikita.test/favicon.ico returns 404
- **Found:** no `og:*`, no `twitter:*`, no `<link rel="icon">`.
- **Why it matters:** shared links (WhatsApp, Instagram, Slack) show a bare URL with no image or description; Google's SERP favicon is missing.
- **Fix:** add `og:title`, `og:description`, `og:image` (1200x630), `og:url`, `og:type`, `twitter:card`, plus a favicon set. Product pages should use their product photo.

### 18. No LocalBusiness / CafeOrCoffeeShop schema, and a thin Organization block
- **URLs:** https://kopikita.test/, /visit/, /contact/
- **Found:** the only entity markup is an `Organization` on the homepage (name, logo, address). A physical cafe with opening hours, phone, and a map has no `LocalBusiness`/`CafeOrCoffeeShop`, no `openingHours` (7am to 5pm daily), `telephone` (+62 812 0000 0000), `geo`, `sameAs` or `priceRange`.
- **Why it matters:** local pack and Maps eligibility, and consistent NAP signals, rely on this. The Indonesian-market local queries ("kopi Ubud") are the site's most natural search demand.
- **Fix:** add `CafeOrCoffeeShop` JSON-LD on `/visit/` and `/contact/` with the above fields; add `sameAs` for social profiles and Google Business Profile. Make sure the Google Business Profile NAP matches exactly.

### 19. Product pages missing key schema properties; other product pages have none
- **URLs:** /coffee/bali-kintamani/, /coffee/java-ijen/, /coffee/bali-kintamani-1kg/ (present but incomplete); /coffee/flores-bajawa/, /coffee/gift-box/, /coffee/limited-release/ (none)
- **Found:** the Product blocks lack `sku`, `url`, `priceValidUntil`, `itemCondition`, `aggregateRating`/`review`, and `shippingDetails`/`hasMerchantReturnPolicy`. Flores Bajawa, gift box and limited release have no Product markup at all.
- **Fix:** add Product + Offer to all product pages with the full property set. Only add ratings if you have real reviews on the page.

### 20. Variant pages risk duplication
- **URLs:** https://kopikita.test/coffee/bali-kintamani/ vs https://kopikita.test/coffee/bali-kintamani-1kg/
- **Found:** the two pages share the same meta description and near-identical body copy (both list both sizes and prices); only title, H1 and price schema differ.
- **Why it matters:** two near-duplicate pages split ranking signals for "Bali Kintamani coffee".
- **Fix:** either fold sizes into one page with a size selector (preferred), or canonicalise the 1kg page to the main page, or differentiate the 1kg page (cafe/bulk use case, unique copy and description). The Java Ijen and Flores pages already handle both sizes in one page, so consolidating matches the rest of the catalogue.

### 21. Weak title on About; thin shop page; no `/coffee/` product depth
- **URLs:** https://kopikita.test/about/ (title "About Kopi Kita: Our Roastery Story" is fine but has no location), https://kopikita.test/shop/
- **Found:** `/shop/` is about 90 words, only text links, no product images, prices or schema, and duplicates much of `/coffee/`. It does not link to the gift box, subscriptions or the limited release.
- **Fix:** make `/shop/` a real category page: product cards with image, name, price and links to every product, with short unique intro copy. Differentiate `/shop/` and `/coffee/` roles (coffee = beans, shop = all products).

### 22. Branded 404 page is missing for real 404s
- **URL:** any missing path, e.g. https://kopikita.test/nonexistent/
- **Found:** real 404s return the server's default "Error response" page, with no navigation, branding or links. The pretty "Page not found" page exists only as the soft-404 at `/gifts/`.
- **Fix:** configure the server's 404 handler to serve the branded page with a true 404 status.

---

## Low

### 23. No `llms.txt`, no AI-crawler policy
- **URLs:** https://kopikita.test/llms.txt (404), https://kopikita.test/robots.txt
- **Found:** robots.txt is `User-agent: *` only, with no explicit AI crawler rules. `llms.txt` is optional and ignored by Google Search, so this is low priority.
- **Fix:** decide on a policy for GPTBot, ClaudeBot, PerplexityBot and Google-Extended and state it in robots.txt. Optionally add a short `llms.txt`.

### 24. robots.txt: `/cart/` and `/blog/tag/` do not exist
- **URLs:** https://kopikita.test/cart/ (404), https://kopikita.test/blog/tag/ (404)
- **Found:** harmless, but confirm these paths are real when the shop and tags launch. Also consider disallowing internal search and filter parameters if they appear later.

### 25. Security and caching headers absent
- **URL:** all
- **Found:** the dev server sends no HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, `Cache-Control` or compression. This is the local Python server, so verify on the production host before treating it as a real problem.
- **Fix:** set these at the production web server/CDN; enable Brotli/gzip and long-lived caching for `/assets/`.

### 26. Internal linking and content opportunities
- **URLs:** various
- **Found / fix:**
  - No breadcrumbs or `BreadcrumbList` schema on product and blog pages.
  - The footer has only a Contact link; add a fuller footer (shop, subscriptions, blog, visit, wholesale) so important pages are linked from every page by crawlable text.
  - Blog posts have no author byline, bio page or visible dates, even though schema names Wayan Sudarma. Showing the author, credentials (the About page has strong ones: 12 years roasting, trained in Melbourne) and dates supports E-E-A-T.
  - `/blog/best-coffee-beans-bali/` recommends "a washed Kintamani from any good local roaster", which is a competitor mention with no product link; consider linking to your own offer.
  - The homepage is short (about 200 words) with no H2s; add sections for best sellers, subscriptions and the cafe with image links.
  - Add FAQ-style sections (shipping, roast dates, grind options) that answer common queries in short, quotable passages.

---

## What is working well
- Every page has a unique, correctly sized `<title>` (except the shared pattern issues above), a meta description, `lang`, viewport and exactly one H1.
- Canonicals are self-referencing and absolute on all pages except Java Ijen and blog page 2.
- Content is original, specific and experience-led (farm groups, altitudes, brew ratios), with 400 to 700+ words on the articles.
- Image `alt` text is descriptive and `width`/`height` are set, which prevents layout shift. Assets (logo, hero, product images) return 200.
- robots.txt is valid and references the sitemap; the sitemap is well-formed XML.
- The Article schema on `best-coffee-beans-bali` parses correctly and includes dates and author.

## Not assessed
- Core Web Vitals (LCP, INP, CLS): needs a real browser or field data. Run PageSpeed/CrUX after fixing issues 5, 6 and 12.
- HTTPS, redirects from `http://` and `www`, and TLS: the local server is plain HTTP and `kopikita.test` is a test domain, so none of this could be checked.
- Backlinks, rankings, Google Search Console indexation: no data source was available.
- Rendered (JavaScript) DOM: only raw HTML was fetched. Issues 5, 6 and 15 should be re-checked in a rendered view.

## Suggested order of work
1. **This week:** issues 1, 2, 3, 4 (canonical, soft 404, hreflang, price schema), then 7, 8, 9.
2. **Next:** 5, 6, 10, 11, 12, 13 (rendering, sitemap hygiene, LCP, JSON-LD).
3. **Within a month:** 14 to 22 (linking, schema depth, social tags, duplication, 404 page).
4. **Backlog:** 23 to 26.
