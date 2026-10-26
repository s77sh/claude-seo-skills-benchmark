# SEO Audit: Kopi Kita (kopikita.test)

Audited from the local build at http://localhost:8766/ on 2026-10-22. I fetched every page linked from the nav, the sitemap and the body copy (25 URLs, plus assets). Production URLs below use the `https://kopikita.test` domain that the canonicals and sitemap declare.

**Not available to me:** Search Console, analytics, rankings, real Core Web Vitals, and the production HTTP stack (HTTPS, compression, caching and HSTS can't be judged on the local Python dev server). Structured data was read from static HTML, where it is present as inline JSON-LD (not JS-injected), so the schema findings are reliable. Validate fixes in the Rich Results Test.

## Executive summary

Kopi Kita is a small site (about 20 real pages) with good basics. Every page has a unique title, a description, a canonical, a single H1 and alt text on its images. The content is genuinely useful and specific. The problems are mostly indexation and canonical wiring, and several of them hit revenue pages:

1. **`/subscriptions/` is sent `X-Robots-Tag: noindex`**, so the subscription page can't rank, yet it sits in the nav and sitemap.
2. **`/coffee/java-ijen/` canonicalises to `/coffee/ijen/`, which 301-redirects back to it.** This is a canonical/redirect loop on a core product page.
3. **`/gifts/` is a soft 404** (HTTP 200 with a "Page not found" body), linked from the nav of every page.
4. **hreflang on `/id/` is broken**: the invalid code `in`, no self-reference, and no return tag from the English page.
5. **The `/coffee/limited-release/` page is reachable only through a JS `onclick` button** and isn't in the sitemap.

Quick wins (under an hour each): remove the noindex header, fix the Ijen canonical, delete or build `/gifts/`, fix hreflang, clean the sitemap, correct the Kintamani schema price.

---

## Priority 1: Critical (blocks indexing or ranking)

### 1.1 `/subscriptions/` is noindexed
- **URL:** https://kopikita.test/subscriptions/
- **Evidence:** the response carries `X-Robots-Tag: noindex`. The HTML has no meta robots tag, so the header is easy to miss in a template review. The page is still in the main nav, in `sitemap.xml`, and has a self-canonical.
- **Why it matters:** Google will drop the page and never rank it for "coffee subscription Bali" or similar. The sitemap and canonical tell Google to index it while the header says the opposite.
- **Fix:** remove the header (check the server, CDN or app config for a rule matching `/subscriptions/`, probably left over from staging). Then request indexing in Search Console. If the noindex is intentional, remove the page from the sitemap and nav, but this looks like a mistake.

### 1.2 Ijen product page canonical points to a redirect that points back
- **URL:** https://kopikita.test/coffee/java-ijen/ (canonical target: `/coffee/ijen/`)
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/ijen/">`. `GET /coffee/ijen/` returns `301` to `/coffee/java-ijen/`. The sitemap and every internal link use `/coffee/java-ijen/`.
- **Why it matters:** the canonical nominates a URL that redirects back, so the signals contradict each other. Google will likely ignore the canonical and choose for itself, and the page's product schema, links and reviews may consolidate on an unintended URL. This is one of the three main products.
- **Fix:** change the canonical to `https://kopikita.test/coffee/java-ijen/`. Keep the 301 from the old URL.

### 1.3 `/gifts/` is a soft 404 linked from every page
- **URL:** https://kopikita.test/gifts/
- **Evidence:** HTTP 200, `<title>Page not found | Kopi Kita</title>`, `<h1>Page not found</h1>`, no canonical or description. It is linked from the nav on every page and is not in the sitemap.
- **Why it matters:** Google treats this as a soft 404, which wastes crawl budget and signals a poorly maintained site. Users clicking "Gifts" hit an error, which hurts conversions. The real gift page is `/coffee/gift-box/`, and gift subscriptions are on `/subscriptions/`.
- **Fix:** either build a real `/gifts/` landing page (gift box, gift subscriptions, gift cards) to target "coffee gifts Indonesia", or remove the nav link. If the URL stays unbuilt, it must return a real `404`/`410`.

### 1.4 Broken hreflang between English and Indonesian
- **URLs:** https://kopikita.test/ and https://kopikita.test/id/
- **Evidence:** `/id/` declares `hreflang="in"` (invalid; Indonesian is `id`) and `hreflang="en"` pointing to `/`. It has no self-referencing entry beyond that wrongly coded one. The homepage has no hreflang at all, so there is no return link. There is no `x-default`. `/id/` also has `<html lang="en">`.
- **Why it matters:** hreflang only works when reciprocal. As it stands Google will ignore it, and Indonesian searchers can land on the English page (or the reverse).
- **Fix:** put the same set on both pages: `hreflang="en"` → `/`, `hreflang="id"` → `/id/`, and `hreflang="x-default"` → `/`. Set `<html lang="id">` on `/id/`. Also list them in the sitemap if you prefer sitemap-based hreflang, but don't mix methods that disagree.

---

## Priority 2: High impact

### 2.1 Limited-release page is only linked by JavaScript and missing from the sitemap
- **URL:** https://kopikita.test/coffee/limited-release/ (linked from `/coffee/`)
- **Evidence:** the only link is `<button onclick="location.href='/coffee/limited-release/'">`. There is no `<a href>` to it anywhere, and it is not in `sitemap.xml`. The page itself is fine (title, description, canonical, H1).
- **Why it matters:** Google doesn't treat `onclick` handlers as links, so the page is effectively orphaned and won't be discovered or pass/receive link equity.
- **Fix:** use a real `<a href="/coffee/limited-release/">` link, add it to the sitemap, and link it from the home page and shop. Because it's a monthly, scarce item, consider a stable URL that you update rather than a new URL each month.

### 2.2 `/blog/page/2/` canonicalises to `/blog/` and sits in the sitemap
- **URL:** https://kopikita.test/blog/page/2/
- **Evidence:** canonical is `https://kopikita.test/blog/`. It is listed in `sitemap.xml`.
- **Why it matters:** canonicalising page 2 to page 1 tells Google not to index page 2 and can stop it following links to posts only listed there. The cold-brew post is linked **only** from page 2 (and the sitemap), so it effectively depends on the sitemap for discovery. The sitemap also lists a URL that points elsewhere.
- **Fix:** give page 2 a self-referencing canonical. Better, show all posts on `/blog/` (there are only three) so no post sits behind pagination. Link `cold-brew-at-home` from `/blog/`, the brewing guide and the pour-over post.

### 2.3 Sitemap contains non-indexable and redirecting-adjacent URLs, and invalid dates
- **URL:** https://kopikita.test/sitemap.xml
- **Evidence:**
  - `/subscriptions/` (noindex header), `/coffee/samples/` (blocked in robots.txt), and `/blog/page/2/` (canonical elsewhere) are listed.
  - Every `<lastmod>` is `2027-03-01`, a date in the future relative to today (2026-10-22), and identical for all URLs.
  - Missing: `/coffee/limited-release/`.
- **Why it matters:** the sitemap should list only canonical, indexable 200 URLs. A uniform or future `lastmod` teaches Google to ignore the field entirely.
- **Fix:** remove the three URLs above (after fixing the subscriptions noindex, keep that one). Generate `lastmod` from each page's real last-modified date. Add the limited-release page.

### 2.4 Mixed content and an `http://` URL on the contact page
- **URL:** https://kopikita.test/contact/
- **Evidence:** `<img src="http://kopikita.test/assets/img/storefront.jpg">` and `<iframe src="http://maps.example.com/embed?...">`.
- **Why it matters:** on HTTPS these are mixed-content: browsers will block or warn about the iframe (the map won't load) and can upgrade or block the image. It undermines the trust page and the address/NAP signal for local search.
- **Fix:** use `https://` (or root-relative `/assets/img/storefront.jpg`) for the image and an HTTPS map embed (Google Maps embed). Also check no other absolute `http://` URLs remain.

### 2.5 Product schema price does not match the page (Kintamani 250g)
- **URL:** https://kopikita.test/coffee/bali-kintamani/
- **Evidence:** JSON-LD `offers.price` is `145000`; the page text says `Rp 165,000 for 250g`.
- **Why it matters:** a price mismatch between markup and visible content can make the product rich result ineligible or trigger a Merchant Center/Search Console warning.
- **Fix:** set the schema price to 165000 and generate it from the same data as the page. Also add `url`, `sku` and `availability` consistency checks for all products.

### 2.6 Invalid JSON-LD on the pour-over article
- **URL:** https://kopikita.test/blog/how-to-brew-pour-over/
- **Evidence:** the Article JSON ends `"author": {...},}`. The trailing comma makes the block invalid JSON, so it will be ignored.
- **Fix:** remove the trailing comma and validate in the Rich Results Test. Add a CI check that parses every JSON-LD block.

### 2.7 Near-duplicate product pages: 250g vs 1kg Kintamani
- **URLs:** https://kopikita.test/coffee/bali-kintamani/ and https://kopikita.test/coffee/bali-kintamani-1kg/
- **Evidence:** the body copy is identical (and so is the meta description, the image and schema description). Both mention both sizes and prices. Only the title and H1 differ.
- **Why it matters:** the two pages compete for the same queries ("Bali Kintamani coffee beans") and split links. Google may pick either as canonical.
- **Fix:** merge into one product page with a size selector and a single Product schema with two offers, then 301 the 1kg URL. If you keep both, differentiate the 1kg page (who it's for, price per 100g, wholesale/household use) and canonicalise it to the main page.

### 2.8 Redirecting internal links (302) to the Kintamani product
- **URLs:** `/coffee/kintamani/` is linked from `/` (homepage), `/blog/best-coffee-beans-bali/` and `/blog/cold-brew-at-home/`.
- **Evidence:** `GET /coffee/kintamani/` returns `302 Found` to `/coffee/bali-kintamani/`.
- **Why it matters:** the homepage and two blog posts send link equity through a redirect, and a 302 is temporary, so Google may keep the old URL. It's the best-seller.
- **Fix:** update the links to `/coffee/bali-kintamani/` and change the redirect to a 301.

---

## Priority 3: Medium

### 3.1 Duplicate meta description on Flores Bajawa
- **URL:** https://kopikita.test/coffee/flores-bajawa/
- **Evidence:** the description reads "Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon and black tea..." (the Java Ijen text). The page is a honey-process coffee from Flores.
- **Fix:** write a unique one, e.g. "Honey-process coffee from Bajawa, Flores. Notes of dark chocolate, red apple and clove. Roasted to order in Ubud." (about 120 characters; add a call to action).

### 3.2 Flores Bajawa is poorly linked and has no schema
- **URL:** https://kopikita.test/coffee/flores-bajawa/
- **Evidence:** `/coffee/` (the category hub), `/shop/` and the homepage list only Kintamani and Ijen. Flores is linked only from the pour-over blog post and the sitemap. It has no Product JSON-LD, unlike the other two origins.
- **Fix:** add it to the `/coffee/` hub, `/shop/` and the homepage; add Product schema (price 155000 IDR).

### 3.3 Content injected or loaded only by JavaScript
- **URLs:** https://kopikita.test/coffee/gift-box/ and https://kopikita.test/about/
- **Evidence:** the gift box description is written into `#product-description` via `innerHTML` (the static HTML has an empty div, only the H1 and title). The About page's three farm photos use `data-src` and an IntersectionObserver, with no `src` or `<noscript>` fallback.
- **Why it matters:** Google can render JS, but it is delayed and less reliable, and other crawlers (Bing, AI crawlers, social previews) often don't. Right now the gift-box page looks empty to a non-rendering fetch, and the farm images (with good alt text) may not be indexed in image search.
- **Fix:** render the gift box copy in the server HTML, and use native `loading="lazy"` with a real `src` for the farm images.

### 3.4 Hero image is lazy-loaded (LCP)
- **URL:** https://kopikita.test/
- **Evidence:** the hero is the first element in `<main>` and has `loading="lazy"`.
- **Why it matters:** lazy-loading the likely LCP image delays it. Width and height are set, which is good for CLS.
- **Fix:** remove `loading="lazy"` from the hero, add `fetchpriority="high"`, and serve WebP/AVIF at an appropriate size.

### 3.5 Internal `nofollow` on the Wholesale link
- **URL:** https://kopikita.test/wholesale/ (nofollow in the nav on every page)
- **Evidence:** `<a href="/wholesale/" rel="nofollow">`. The wholesale page is in the sitemap, indexable, and a revenue page.
- **Fix:** remove `rel="nofollow"` from internal links. Add a followed link from the homepage (one already exists in the body) and from the About page.

### 3.6 Missing viewport meta on the Visit page
- **URL:** https://kopikita.test/visit/
- **Evidence:** no `<meta name="viewport">`, unlike every other page. The 404 template has one.
- **Why it matters:** under mobile-first indexing the page renders at desktop width, which hurts mobile usability for a page whose audience is people on their phones looking for hours and directions.
- **Fix:** add `<meta name="viewport" content="width=device-width, initial-scale=1">`.

### 3.7 Thin and under-built pages
- **URLs:** /shop/ (about 95 words), /visit/ (about 90), /coffee/samples/ (about 35), /wholesale/ (about 100), /id/ (about 60), /coffee/flores-bajawa/, `/blog/` index.
- **Evidence:** the pages contain a few short paragraphs, no H2s (except Visit), no product listing, and the Shop page doesn't link to the gear or drip bag products it describes.
- **Fix:**
  - **Shop:** list actual products with links, prices and images; add links to each category.
  - **Visit:** add the full address, a map, a gallery and FAQs ("Do you do cuppings?", "Is there parking?").
  - **Wholesale:** add pricing tiers, delivery zones, a short case study and an enquiry form.
  - **`/coffee/samples/`:** it duplicates the wholesale page's offer. Either fold it into `/wholesale/` or make it indexable and linked, but not both blocked in robots.txt and in the sitemap.
  - **`/id/`:** expand into a real Indonesian site section, or the translated homepage alone will stay thin.

### 3.8 Article and Organization schema are incomplete
- **URLs:** /blog/best-coffee-beans-bali/, /blog/how-to-brew-pour-over/, /
- **Evidence:** Article lacks `image` and `publisher`, and the best-beans `headline` ("The best coffee beans in Bali") differs from the H1 ("...: a buyer's guide"). `author` has no `url`. Organization has no `sameAs`, contact point or opening hours.
- **Fix:** add `image`, `publisher` and an author page; match the headline to the H1. The cafe is a physical place, so add `CafeOrCoffeeShop` / `LocalBusiness` schema with `openingHours` (7am-5pm daily), geo, `telephone` and `priceRange` on `/visit/` or the homepage.

---

## Priority 4: Low / quick wins

| # | Issue | URL(s) | Fix |
|---|---|---|---|
| 4.1 | No Open Graph / Twitter Card tags, so shared links show no image or tailored preview | all pages | add `og:title`, `og:description`, `og:image`, `og:url`, `twitter:card` |
| 4.2 | No favicon (`/favicon.ico` returns 404) | site-wide | add a favicon and `<link rel="icon">` |
| 4.3 | Unknown URLs return the server's bare default 404, not the branded 404 template (that template is served with a 200 at `/gifts/`) | e.g. /nonexistent | serve the branded page with a 404 status for all missing URLs |
| 4.4 | Case and index variants resolve with a 200: `/Coffee/`, `/index.html`. The canonical tags cover it, but add 301s | /Coffee/, /index.html | redirect to the lowercase canonical URL |
| 4.5 | Flat heading structure: most pages have one H1 and no H2s | most pages | break the long posts and guides into H2 sections (cold brew, pour over and best-beans posts are long single-block pages) |
| 4.6 | Brewing-guide and blog posts don't cross-link well (cold brew isn't linked from the brewing guide, which has a cold-brew recipe) | /coffee/brewing-guide/, /blog/cold-brew-at-home/ | link both ways with descriptive anchors |
| 4.7 | Titles lack the location/keyword on some pages ("About Kopi Kita: Our Roastery Story", "Shop Coffee Beans and Brewing Gear") | /about/, /shop/ | optional: "Shop Specialty Coffee Beans in Bali" style titles |
| 4.8 | No breadcrumbs (and no BreadcrumbList schema) | /coffee/*, /blog/* | add breadcrumbs |
| 4.9 | `robots.txt` disallows `/cart/` and `/blog/tag/` (both 404 today); fine, but `Disallow: /coffee/samples/` conflicts with the sitemap | robots.txt | align with the sitemap fix in 2.3 |
| 4.10 | The footer is minimal and omits links to key pages (shop, subscriptions, wholesale) | all pages | add a fuller footer with address, hours and key links |

## Production-only checks I could not do locally
- HTTPS certificate, HTTP→HTTPS redirect, a single hostname (www vs non-www), HSTS.
- Gzip/Brotli compression and cache headers (the dev server sends none; images and CSS have `Last-Modified` only).
- Real Core Web Vitals (use PageSpeed Insights / CrUX after launch). Pages are tiny, so TTFB and page weight should be good, but the hero image (13.8 KB here) may not be representative.
- Search Console coverage, index counts, queries and positions. After the fixes above, submit the sitemap and use URL Inspection on `/subscriptions/`, `/coffee/java-ijen/` and `/coffee/limited-release/`.

## Prioritised action plan
1. **This week (critical):** remove the noindex on `/subscriptions/`; fix the Ijen canonical; resolve `/gifts/`; fix hreflang (`id`, reciprocal, `x-default`, `lang="id"`).
2. **Next (high):** real link + sitemap entry for limited-release; blog pagination canonical/post visibility; clean the sitemap (urls and `lastmod`); fix the HTTP assets on `/contact/`; fix the schema price and the JSON-LD syntax error; merge or differentiate the 1kg Kintamani page; update the 302 links.
3. **Then (medium):** the Flores description and links; server-render gift box copy and farm images; un-lazy the hero; remove internal nofollow; add the viewport to `/visit/`; build out thin pages; extend schema (LocalBusiness, Article).
4. **Long term:** content plan around "best coffee beans Bali", "coffee subscription Indonesia", wholesale/cafe supply and brewing guides, with Indonesian-language equivalents; build local links (Ubud/Bali directories, Google Business Profile, tourism sites) and set up Search Console and analytics to track the changes.
