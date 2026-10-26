# SEO audit: Kopi Kita (kopikita.test)

Method: crawled the local site at http://localhost:8766/ with curl. That covered the home page, every URL in `sitemap.xml`, every internal link found, `robots.txt`, the redirects and a 404 URL. I read the raw HTML, which is what a non-rendering crawler sees. I did not run Lighthouse, check real rankings or check the production server.

Issues are in priority order. P0 means content or indexing is broken, P1 means a significant ranking or crawl loss, P2 is worth fixing, and P3 is polish.

---

## P0: Critical

### 1. `/gifts/` is a soft 404 and sits in the main nav
- **URL:** `/gifts/`, linked from the nav on every page.
- **Found:** It returns **HTTP 200** with the "Page not found" template (title "Page not found | Kopi Kita").
- **Why it matters:** Google treats this as a soft 404. Every page links to it, so crawl budget is wasted and the site looks low quality. Visitors who want gifts get a dead end.
- **Fix:** The real gift page is `/coffee/gift-box/`. 301-redirect `/gifts/` to it, or build a real `/gifts/` page. Update the nav link either way. The 404 template must also return a real 404 status. This one happens to be a 200 and should be checked server-wide.

### 2. Canonical tags point at the wrong URLs on several pages
Each page's canonical should be its own URL. These are not:

| Page | Canonical it declares | Problem |
|---|---|---|
| `/coffee/java-ijen/` | `/coffee/ijen/` | `/coffee/ijen/` is a 301 redirect back to `/coffee/java-ijen/`, so this is a canonical/redirect loop. Google will probably ignore the tag, and it is a mixed signal at best. |
| `/blog/page/2/` | `/blog/` | Page 2 tells Google it duplicates page 1. The cold-brew post is linked only from here, so it can lose discovery and indexing. |

**Fix:**
- Set the Ijen canonical to `https://kopikita.test/coffee/java-ijen/`.
- Make `/blog/page/2/` self-canonical.
- Audit canonicals automatically in the build or template. A check that the canonical equals the request URL, except where that is deliberate, would catch all of these.

### 3. Duplicate product pages: the 1kg page copies the 250g page
- **URLs:** `/coffee/bali-kintamani/` and `/coffee/bali-kintamani-1kg/`.
- **Found:** The body copy is identical. The meta description is identical, and the 250g page already lists both sizes and prices (Rp 165,000 / Rp 520,000). Both are self-canonical and both are in the sitemap, so they compete for the same queries.
- **Why it matters:** Keyword cannibalisation and diluted link equity.
- **Fix:** Fold sizes into one product page as variants and 301 the 1kg URL to it. If the 1kg page is kept, canonical it to the main page, or give it genuinely different content aimed at cafes and large households. Remove it from the sitemap if it is canonicalised away.

### 4. Product pages disagree about price, in the structured data and on the page
- **URLs:** `/coffee/bali-kintamani/`, `/coffee/java-ijen/`.
- **Found:**
  - Kintamani 250g: the Product JSON-LD says **145000**, the visible text says **Rp 165,000**.
  - Ijen 250g (150000) and Kintamani 1kg (520000) match their visible prices.
- **Why it matters:** Google can suppress or flag rich results when structured-data prices differ from visible prices. It also confuses buyers and can trigger merchant-listing policy problems.
- **Fix:** Generate the JSON-LD from the same price source as the visible page, and correct Kintamani.

### 5. The gift-box and subscription pages inject copy with JavaScript
- **URLs:** `/coffee/gift-box/` and `/subscriptions/`.
- **Found:** In the raw HTML, `<div id="product-description"></div>` is empty, and `innerHTML = "..."` fills it. On the gift box this is the entire description, including the price (Rp 295,000), shipping and the ordering deadline. On `/subscriptions/` the same script appears to render the **gift-box description** (three 100g bags, handwritten note), which looks like a copy-paste error.
- **Why it matters:** Google can render JavaScript, but rendering is deferred and less reliable, and other crawlers and AI crawlers often do not execute it. The key commercial content on the gift box is not in the HTML. The subscriptions page also shows gift-box copy under a subscriptions title.
- **Fix:** Put the description in the server-rendered HTML. Fix the subscriptions page so it shows subscription details such as pricing, intervals and sizes, not the gift box.

---

## P1: High

### 6. Internal links go through redirects, and some use the wrong URLs
- `/coffee/kintamani/` is a **302** (temporary) redirect to `/coffee/bali-kintamani/`. It is linked from the home page ("Bali Kintamani natural"), from `/blog/cold-brew-at-home/` and from `/blog/best-coffee-beans-bali/`. The best-beans post is a key commercial article.
- `/coffee/ijen/` is a 301 to `/coffee/java-ijen/`, and the Ijen canonical points at it (see issue 2).
- **Why it matters:** A 302 tells Google the move is temporary, so link equity may not consolidate. Every click or crawl pays an extra redirect hop.
- **Fix:** Link directly to `/coffee/bali-kintamani/` and `/coffee/java-ijen/` everywhere, and make the `/coffee/kintamani/` redirect a 301.

### 7. The sitemap contains URLs that should not be in it
- **URL:** `/sitemap.xml`.
- **Found:**
  - `/coffee/samples/` is in the sitemap but **disallowed in `robots.txt`** (`Disallow: /coffee/samples/`). The two files contradict each other, and Google reports this in Search Console.
  - `/blog/page/2/` is in the sitemap, but its canonical points elsewhere (see issue 2).
  - `/coffee/bali-kintamani-1kg/` is a duplicate (see issue 3).
  - Every `<lastmod>` is **2027-03-01**, which is in the future (today is 2026-10-22), and identical for every page. Google discards `lastmod` values it cannot trust.
  - The sitemap omits `/gifts/` (broken, so it should be) and has no `/id/` alternates.
- **Fix:** The sitemap should list only indexable, canonical, 200 URLs. Remove `/coffee/samples/`, page 2 and the 1kg page. Use real last-modified dates. Optionally add `xhtml:link` hreflang alternates for `/` and `/id/`.

### 8. Duplicate meta description and a mismatched title on the Flores page
- **URL:** `/coffee/flores-bajawa/`.
- **Found:** The meta description is copied from the Ijen page ("Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon...") although the page is a honey-process coffee from Flores.
- **Why it matters:** The snippet in search results will be wrong or rewritten by Google. It also reads as a duplicate. The Kintamani 250g and 1kg pages share a description too.
- **Fix:** Write a unique description for the Flores page, for example "Honey-process coffee from Bajawa, Flores. Notes of dark chocolate, red apple and clove. Roasted to order in Ubud." Give the 1kg page its own, or resolve it per issue 3.

### 9. The Indonesian page has a wrong hreflang code and no return tags
- **URL:** `/id/`, and `/` for the missing reciprocal links.
- **Found:** `/id/` declares `hreflang="in"`. The valid code is **`id`**. (`in` was a retired ISO code and is not accepted by Google.) `/id/` lists both `en` and itself, but the English home page has **no hreflang tags at all**, so there is no return link and Google may ignore the pair. Neither page has `x-default`. Hreflang must be reciprocal to work.
- **Also:** The Indonesian page links to `/coffee/` and `/visit/`, which are English pages, so the Indonesian version is a dead-end island. It is a short page, but that is acceptable for a landing page.
- **Fix:** Change `in` to `id`. Add `hreflang="en"`, `hreflang="id"` and `hreflang="x-default"` to both `/` and `/id/`. Consider localised versions of the key pages if Indonesian search is a target.

### 10. `/coffee/` and `/shop/` overlap in purpose and target the same queries
- **URLs:** `/coffee/` ("Single-Origin Indonesian Coffee") and `/shop/` ("Shop Coffee Beans and Brewing Gear").
- **Found:** Both are self-canonical and both list the same two coffees. `/shop/` is a thin text page with a short list of links. Neither links to `/coffee/flores-bajawa/`, which is one of three products, so that page is only discoverable from one blog post and the sitemap.
- **Fix:** Pick a single product hub (for example `/coffee/`, with the shop as an alias or a distinct gear/drip-bag page). Link all three coffees from it. Add `/coffee/flores-bajawa/` to the home page and the hub.

### 11. A key internal link exists only as a JavaScript button
- **URL:** `/coffee/` contains `<button onclick="location.href='/coffee/limited-release/'">See this month's limited release</button>`.
- **Why it matters:** Crawlers do not follow `onclick` handlers, so `/coffee/limited-release/` is invisible to them and receives no link equity. (I did not fetch that URL, so I cannot say whether it exists.)
- **Fix:** Use a real `<a href="/coffee/limited-release/">`, styled as a button if needed.

---

## P2: Medium

### 12. Structured data is missing, invalid or incomplete
- **Article JSON-LD on `/blog/how-to-brew-pour-over/`** ends with a **trailing comma** (`"author": {...},}`), so it is invalid JSON and ignored entirely. Fix the syntax.
- **Product schema** on the Kintamani and Ijen pages is valid but minimal: no `sku`, `url` or `priceValidUntil`. Add them. Do not add fake ratings.
- **`/coffee/flores-bajawa/`, `/coffee/gift-box/`, `/subscriptions/`** have **no Product schema** at all although they are products.
- **Article** on `/blog/best-coffee-beans-bali/`: the headline ("The best coffee beans in Bali") differs from the H1 and title ("...: a buyer's guide"). Make them consistent. `/blog/cold-brew-at-home/` has no Article schema. Add `image` to all articles, which Google recommends.
- **Organization schema** is on the home page only. It is missing `sameAs` (social profiles) and `contactPoint`. Because the business has a physical cafe, **add `LocalBusiness` / `CafeOrCoffeeShop` schema** with `openingHours`, `telephone`, `geo` and `priceRange` on `/visit/` and `/contact/`. This is the biggest local-SEO opportunity.
- **Fix:** Validate everything in Google's Rich Results Test after the changes.

### 13. Mixed content and a non-HTTPS resource on the contact page
- **URL:** `/contact/`.
- **Found:** The storefront image is `http://kopikita.test/assets/img/storefront.jpg`, and the map iframe is `http://maps.example.com/embed?...`. Both are insecure. The production site will be served over HTTPS (all canonicals are `https://`), so browsers will block or warn on them. The `maps.example.com` host looks like a placeholder, not a real map embed.
- **Fix:** Use relative or `https://` URLs and a real map provider embed. Check that the whole site forces HTTPS with a 301 and HSTS.

### 14. Lazy-loading mistakes hurt performance and hide images
- **`/` hero image** (the LCP element) has `loading="lazy"`. It is above the fold, which delays Largest Contentful Paint. Remove `loading="lazy"` and consider `fetchpriority="high"`.
- **`/about/` gallery** uses `data-src` plus a custom IntersectionObserver script, with no `src`. The three farm photos are absent from the raw HTML, so Google may not index them, and they do not show at all without JavaScript. Also, the script creates a separate observer per image and uses only `e[0]`. Use native `loading="lazy"` with a real `src`.

### 15. Thin content on key commercial pages
- **`/shop/`** is a short list with no product detail.
- **`/coffee/samples/`** is two sentences. It is blocked in robots.txt anyway.
- **`/id/`** is short.
- **`/wholesale/`** is around 100 words. Wholesale is a commercial page with real B2B search demand ("wholesale coffee Bali"), and it deserves more content such as pricing tiers, minimums, delivery zones and a form.
- **Fix:** Expand the wholesale and shop pages, and add FAQs where useful. Do not pad.

### 16. `/wholesale/` is `rel="nofollow"` in the site navigation
- **Found:** The nav link carries `rel="nofollow"` on every page.
- **Why it matters:** It withholds internal link equity from a page that earns revenue, and it is the only way the page is linked. There is no reason to nofollow your own page.
- **Fix:** Remove the `rel="nofollow"`.

### 17. Orphan and weakly linked pages
- `/coffee/samples/` is not linked from anywhere I found, and is blocked by robots.txt. The wholesale page tells people to use the contact page instead.
- `/coffee/flores-bajawa/` is linked only from one blog post (see issue 10).
- `/blog/cold-brew-at-home/` is linked only from `/blog/page/2/`, which has a wrong canonical.
- **Fix:** Add contextual links from related pages, and show all posts on the blog index or a paginated list with working canonicals.

### 18. Duplicate URL variants are served
- `/index.html` returns 200 with the same content as `/`. Redirect it to `/` with a 301.
- `/coffee` (no trailing slash) correctly 301s to `/coffee/`, so slash handling is mostly fine.
- Check upper-case and `www` variants on production.

### 19. Custom 404 page quality
- The nonexistent path `/nope` returns the server's default 404 page, the Python default "Error response", with no site navigation and no links back. Yet the site has a custom "Page not found" template that is being served with a 200 status at `/gifts/` (issue 1).
- **Fix:** Serve the branded template with a real 404 status for unknown URLs.

---

## P3: Low / polish

### 20. Title tag details
- Most titles are fine, around 40 to 60 characters, and unique. Exception: `/about/` and `/contact/` do not follow the pattern, and `/about/` omits the "| Kopi Kita" suffix in a different position ("About Kopi Kita: Our Roastery Story"). It is a minor inconsistency.
- The blog titles are descriptive. The titles for `/` and the product pages are good.

### 21. Product and content pages lack heading structure
- Most pages have only an H1 and paragraphs. Long guides such as `/blog/how-to-brew-pour-over/` and `/blog/cold-brew-at-home/` use `<strong>` run-in headings (**Grind size.**, **Water.**) where H2s should be. The brewing guide does the same for the grind chart, water temperature and troubleshooting.
- **Fix:** Turn them into `<h2>` elements. This helps featured snippets, accessibility and scanning. The pour-over steps (`1. 2. 3.` in one paragraph) should be an `<ol>`, and it could carry `HowTo`-style markup, though Google has largely dropped HowTo rich results.

### 22. Missing `<meta>` and social tags
- No Open Graph or Twitter Card tags on any page (`og:title`, `og:description`, `og:image`, `og:url`), so social shares look bare.
- No favicon is linked.
- No `<meta name="robots">`, which is fine as the default, but there is no `max-image-preview:large` either.
- **Fix:** Add OG and Twitter tags using the existing product, hero and logo images.

### 23. Image alt text and file hints
- Alt text is present on the images I checked. Good. The hero and product shots have good descriptions.
- The logo (`logo.png`) is referenced in the Organization schema. It exists and returns 200.
- Consider WebP/AVIF, and confirm the 1200x700 hero is compressed. I have not measured file sizes beyond the hero.

### 24. Breadcrumbs and navigation
- There are no breadcrumbs and no `BreadcrumbList` schema. Product and blog pages would benefit (Home > Coffee > Bali Kintamani).
- The footer contains only the address and a Contact link. Add links to the main sections.

### 25. `robots.txt` housekeeping
- The file is valid and lists the sitemap. `Disallow: /cart/` and `/blog/tag/` are reasonable. Neither path exists in the crawl, so they are harmless.
- Fix the contradiction with `/coffee/samples/` (see issue 7). If you want those pages kept out of the index, use `noindex` and leave them crawlable, because a robots.txt block alone does not remove a URL from the index.

### 26. Content freshness and date signals
- Article `dateModified` values (2026-08-02 and 2026-09-01) are plausible. The sitemap's 2027 dates are not (see issue 7).
- Blog content is solid (grounded in specifics), but there are only three posts. A content plan around "best coffee beans Bali", "Kintamani coffee", "Bali coffee roaster" and "buy coffee beans online Indonesia" would help.

---

## What is working well
- Titles and meta descriptions exist on every page, are mostly unique and are the right length.
- Every page has one H1 and `lang="en"`, which is wrong on `/id/` if it is still `en` (not checked). Viewport meta is present.
- Canonical tags exist on all pages and mostly match their URL (exceptions above).
- `robots.txt` exists and references the sitemap.
- Images have descriptive alt text and explicit width and height (which prevents layout shift).
- Clean, readable URLs, with trailing-slash redirects working.
- Original, specific, experience-based copy (farm groups, altitudes, process, roast dates), which is good for E-E-A-T.
- Organisation schema with address on the home page.

---

## Suggested order of work
1. Fix `/gifts/` (issue 1) and the canonical errors (issue 2).
2. Resolve the duplicate Kintamani 1kg page (3), the price mismatch (4) and the JS-injected content (5).
3. Fix the redirected internal links (6), the sitemap/robots conflicts (7), hreflang (9) and the `onclick` button (11).
4. Then the schema fixes and local-business markup (12), mixed content (13) and lazy-loading (14).
5. Finally the content depth, heading structure, social tags and breadcrumbs.

## Limits of this audit
Only the HTML and headers served locally were checked. Not covered: real page speed and Core Web Vitals, HTTPS and HSTS behaviour on production, server logs, Search Console data, backlinks, and whether `/coffee/limited-release/` exists. Production behaviour may differ from this local Python test server.
