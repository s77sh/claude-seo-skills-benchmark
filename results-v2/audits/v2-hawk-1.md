# TECHNICAL SEO AUDIT: Kopi Kita (https://kopikita.test/, audited at http://localhost:8766/)

Date: 2026-10-22
Data source: Fetched with curl (robots.txt, sitemap.xml, all 21 sitemap URLs, plus every URL linked from them). Raw HTML only, with no JavaScript rendering.
Pages analysed: 25 HTML URLs (21 in the sitemap, plus `/gifts/`, `/coffee/kintamani/`, `/coffee/ijen/` and a random 404 probe).

**Not assessed:** real HTTPS behaviour, the www/non-www and http→https redirects (local server only), page speed and Core Web Vitals, and Search Console data. Orphan pages were checked by comparing the sitemap against internal links, but I did not run a full crawl. The audit is limited to what I fetched, and I link-checked only the `<p>` body links and the shared nav.

---

## CRITICAL ISSUES (fix this week)

### 1. Java Ijen canonical points to a URL that 301-redirects back to it (canonical/redirect loop)
- **URL:** `https://kopikita.test/coffee/java-ijen/`. It is in the sitemap, is linked from the home page, shop and pour-over post, and returns 200.
- **Evidence:** its `<link rel="canonical">` is `https://kopikita.test/coffee/ijen/`. That URL returns `301 → /coffee/java-ijen/`.
- **Why it matters:** the canonical points at a redirecting URL and the redirect points back. Google gets contradictory signals and may ignore the canonical or index an unintended URL. This is one of the two main product pages, and its sitemap URL disagrees with its own canonical.
- **Fix:** set the canonical to `https://kopikita.test/coffee/java-ijen/` (self-referencing). Keep the 301 from `/coffee/ijen/`.

### 2. Sitewide nav link to `/gifts/` is a soft 404
- **URL:** `https://kopikita.test/gifts/`. It is linked from the main nav on every page.
- **Evidence:** HTTP 200 with `<title>Page not found | Kopi Kita</title>` and `<h1>Page not found</h1>`. A genuine missing URL (`/this-does-not-exist/`) correctly returns 404.
- **Why it matters:** a 200 on an error page is a soft 404. It wastes crawl budget, Search Console flags it, and every page on the site passes link equity to a dead page. Users who click "Gifts" hit an error.
- **Fix:** either build the page, or point the nav at `/coffee/gift-box/` (which exists), or remove the link. If the page stays missing, return a real 404 or 410 for `/gifts/`. Make sure your error template always sends a 404 status.

### 3. Key internal links go through a 302 redirect
- **URL:** `/coffee/kintamani/` → `302 /coffee/bali-kintamani/`.
- **Linked from:** the home page (best-seller link), `/blog/best-coffee-beans-bali/` (the "our picks" link) and `/blog/cold-brew-at-home/`.
- **Why it matters:** a 302 is a temporary redirect. Google may keep the redirecting URL and may not consolidate signals to the destination. The links also cost an extra request. The target is your best-selling product.
- **Fix:** change those internal links to `/coffee/bali-kintamani/`. Change the 302 to a 301 if the move is permanent.

---

## HIGH-PRIORITY ISSUES (fix this month)

### 4. Product schema price disagrees with the visible price (Kintamani 250g)
- **URL:** `/coffee/bali-kintamani/`.
- **Evidence:** JSON-LD `offers.price` is `145000`. The page text says "Rp 165,000 for 250g". The subscriptions page also says 250g starts at Rp 165,000.
- **Why it matters:** price mismatches between markup and page content breach Google's merchant listing and product rich result guidelines. They can cause Merchant Center or Search Console warnings or lose rich-result eligibility.
- **Fix:** set the schema price to `165000`, or correct the on-page price if 145000 is right. Generate both from the same data field.

### 5. Duplicate meta description (Flores copies Ijen)
- **URL:** `/coffee/flores-bajawa/`.
- **Evidence:** its description is "Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon and black tea…". That is the Java Ijen text. Flores is a honey-process lot from Bajawa.
- **Why it matters:** the description is factually wrong for the page. Google will likely rewrite it, and it hurts click-through.
- **Fix:** e.g. "Honey-process coffee from Bajawa, Flores. Notes of dark chocolate, red apple and clove. Roasted to order in Ubud."

### 6. Flores Bajawa and Gift Box have no Product schema, and Flores is poorly linked
- **URLs:** `/coffee/flores-bajawa/`, `/coffee/gift-box/`.
- **Evidence:** the Kintamani (250g and 1kg) and Ijen pages have Product JSON-LD. These two do not.
- **Flores internal links:** the only body link I found to it is in `/blog/how-to-brew-pour-over/` (and the sitemap). It is not linked from the home page or shop page, and I could not confirm a link from `/coffee/`.
- **Why it matters:** these are product pages, so they miss price and availability rich results. Flores is also nearly orphaned.
- **Fix:** add Product + Offer JSON-LD matching the page prices (Flores: Rp 155,000 for 250g). Link Flores from `/shop/`, the home page and the other coffee pages.

### 7. Gift Box description is injected with JavaScript
- **URL:** `/coffee/gift-box/`.
- **Evidence:** the raw HTML has an empty `<div id="product-description"></div>`. All body copy is written by `innerHTML = "..."` in an inline script.
- **Why it matters:** Google renders JS, but rendering is deferred and less reliable, and other crawlers and AI bots may see an empty page. The raw HTML has no indexable content.
- **Fix:** put the text in the HTML on the server.

### 8. Invalid hreflang setup
- **URLs:** `/id/` and `/`.
- **Evidence:** `/id/` declares `hreflang="in"`, which is the retired language code, so use `id`. It also declares `hreflang="en"` pointing at `/`. The home page has no hreflang tags at all, so the pair is not reciprocal. Hreflang needs return links.
- **Also:** the Indonesian page's nav and footer are in English ("Home", "Coffee", "Contact"), and `/id/` is a single page rather than a translated site.
- **Why it matters:** Google ignores hreflang annotations with invalid codes or missing return links.
- **Fix:** on both `/` and `/id/` add:
  ```html
  <link rel="alternate" hreflang="en" href="https://kopikita.test/">
  <link rel="alternate" hreflang="id" href="https://kopikita.test/id/">
  <link rel="alternate" hreflang="x-default" href="https://kopikita.test/">
  ```
  Translate the `/id/` nav and footer. Add `<link rel="alternate">` to the sitemap if you prefer.

### 9. Mixed content (http resources on an https site)
- **URL:** `/contact/`.
- **Evidence:** `<img src="http://kopikita.test/assets/img/storefront.jpg">` and `<iframe src="http://maps.example.com/embed?...">`.
- **Why it matters:** browsers block or warn on http resources on https pages. The map iframe is likely blocked, which breaks the page's main function, and the image may be auto-upgraded or blocked.
- **Fix:** use `https://` URLs (or protocol-relative or root-relative paths) for both. Confirm the map embed host supports https.

### 10. Sitemap contains URLs that should not be there
- **URLs:** `/coffee/samples/` and `/blog/page/2/`.
- `/coffee/samples/` is in the sitemap but blocked by `Disallow: /coffee/samples/` in robots.txt. Those signals conflict: Google can't crawl the page, so it can't see its content or any noindex, and it may still index the bare URL.
- `/blog/page/2/` is in the sitemap but its canonical points to `/blog/`. Sitemaps should list only canonical, indexable URLs.
- **Fix:** remove both from the sitemap. For samples, decide: if it should not be indexed, remove the robots block and add `<meta name="robots" content="noindex">`. If it should rank, remove the block and link to it.
- **Related:** `/coffee/samples/` has no internal links to it from the pages I checked. It is an orphan, found only through the sitemap.

### 11. Invalid JSON-LD on the pour-over article
- **URL:** `/blog/how-to-brew-pour-over/`.
- **Evidence:** the script ends `"author": {"@type": "Person", "name": "Wayan Sudarma"},}`. The trailing comma makes it invalid JSON, so parsers drop the whole block.
- **Fix:** remove the comma. Also add `image` (recommended for Article) and `publisher`. The other article (`/blog/best-coffee-beans-bali/`) is valid but also has no image.

---

## MEDIUM-PRIORITY ISSUES (roadmap)

### 12. Sitemap `lastmod` dates are in the future and identical
- **Evidence:** every URL has `<lastmod>2027-03-01</lastmod>`. Today is 2026-10-22.
- **Why it matters:** future dates look like errors, and identical dates on every URL teach Google to distrust `lastmod`.
- **Fix:** output the real last-modified date per URL, or drop `lastmod`.

### 13. Near-duplicate product pages: Kintamani 250g and 1kg
- **URLs:** `/coffee/bali-kintamani/` and `/coffee/bali-kintamani-1kg/`.
- **Evidence:** the same meta description, near-identical body copy and the same image. The 1kg page lists both prices. Both are self-canonical and in the sitemap.
- **Why it matters:** two pages compete for the same queries and split signals.
- **Fix:** best option is one page with a size selector (250g/1kg) and one Product schema with two Offers, with the 1kg URL 301ing to it. If you keep both, canonicalise 1kg to the 250g page, or give it distinct copy (cafes and households).
- Ijen and Flores also list 1kg prices in their text but have no 1kg pages, so the Kintamani 1kg page is the odd one out.

### 14. Hero image is lazy-loaded
- **URL:** `/` (`hero-beans.jpg`, `loading="lazy"`).
- **Why it matters:** it is almost certainly the LCP element, and lazy-loading delays it.
- **Fix:** remove `loading="lazy"`, add `fetchpriority="high"`. Not measured here, so confirm with PageSpeed Insights.

### 15. About-page images are hidden from crawlers
- **URL:** `/about/`.
- **Evidence:** three farm images use `data-src` and are only set to `src` by a JS IntersectionObserver. The raw HTML has no `src`. (A further bug: the observer is created inside `forEach`, with `e[0]` referring to the entry for its own image, which is fine, but it only works with JS.)
- **Fix:** use native `<img src="..." loading="lazy">`.

### 16. `/visit/` has no viewport meta tag
- **Evidence:** every other page has `<meta name="viewport" ...>`. `/visit/` does not.
- **Why it matters:** mobile rendering is broken and mobile-friendliness is a ranking input. This page serves local visitors, mostly on phones.
- **Fix:** add `<meta name="viewport" content="width=device-width, initial-scale=1">`. Add `LocalBusiness`/`CafeOrCoffeeShop` schema with address, hours and phone to `/visit/` and `/contact/`.

### 17. Wholesale is `rel="nofollow"` in the site nav
- **URL:** `/wholesale/`.
- **Why it matters:** a nofollow on an internal link tells Google not to pass equity to a page you want to rank for B2B terms. In-body links to it from the home page are followed, so equity still reaches it, but the nav is the strongest link.
- **Fix:** remove `rel="nofollow"`.

### 18. Thin pages and weak internal linking
- `/coffee/samples/` has about 35 words, and `/shop/` and `/subscriptions/` are short (roughly 80 to 100 words). Review whether they need more content or should be merged. `/coffee/samples/` should probably just be part of `/wholesale/`.
- `/blog/cold-brew-at-home/` is linked only from `/blog/page/2/`, which is canonicalised to `/blog/`. Link it from the brewing guide (which has a cold brew section) and from the pour-over post. The home page links to few deeper pages, and product pages do not cross-link.
- The footer contains only a Contact link. Add links to key pages.
- The brewing guide links to pour over only. Add links to the product pages.

### 19. Blog pagination canonical
- **URL:** `/blog/page/2/`. Its canonical points to `/blog/`, which tells Google that page 2 is a duplicate of page 1. Use a self-referencing canonical for each paginated page, or put all posts on one page while there are only 2.

### 20. Minor on-page items
- `/about/` title ("About Kopi Kita: Our Roastery Story") is the only title without the "| Kopi Kita" suffix. This is fine, just inconsistent.
- The home page Organization schema could add `sameAs` (social profiles) and `contactPoint`.
- `/blog/` post titles differ slightly from their H1/schema headlines ("The best coffee beans in Bali" vs "…: a buyer's guide"). Align the schema headline with the H1.
- No Open Graph or Twitter card tags on any page. Add `og:title`, `og:description`, `og:image`.
- Add `BreadcrumbList` schema on `/coffee/*` and `/blog/*`.

---

## TOP 5 QUICK WINS

1. **Fix the Ijen canonical** (`/coffee/java-ijen/` → self). One line. Impact: High.
2. **Fix the `/gifts/` nav link** (point to `/coffee/gift-box/` or return a real 404). One template change. Impact: High.
3. **Repoint `/coffee/kintamani/` internal links** on the home page and two blog posts to `/coffee/bali-kintamani/`. Impact: Medium to High.
4. **Correct the Kintamani schema price and the Flores meta description.** Two text edits. Impact: Medium.
5. **Clean the sitemap** (remove `/coffee/samples/` and `/blog/page/2/`, fix `lastmod`) and add the missing viewport tag on `/visit/`. Impact: Medium.

---

## WHAT'S WORKING

- robots.txt is valid, small and blocks only low-value paths (`/cart/`, `/blog/tag/`, `/coffee/samples/`), and it declares the sitemap.
- Every page checked has a unique title in a sensible length, a single H1, a self-referencing canonical (except the two problems above) and a meta description (apart from the duplicate on Flores).
- A real 404 returns a proper 404 status.
- `lang="en"` and the viewport tag are set on all pages but `/visit/`. Images have alt text with width and height set.
- Product schema on Kintamani and Ijen is otherwise complete (name, image, brand, offer with price, currency and availability). The Organization schema on the home page is valid.
- Content is original, specific and useful (brewing, sourcing, tasting notes), with clear E-E-A-T signals (named roaster, farmer groups).
- The `/coffee/ijen/` 301 is a correct permanent redirect, and there are no redirect chains (all redirects are a single hop).

## BOTTOM LINE

The biggest issue is conflicting URL signals around your two key product pages: the Ijen canonical loop and the 302 on `/coffee/kintamani/`, plus a sitewide link to a soft-404 `/gifts/`. Fixing those, and the mismatched Kintamani price, lets Google consolidate on the right product URLs and qualify for product rich results.
