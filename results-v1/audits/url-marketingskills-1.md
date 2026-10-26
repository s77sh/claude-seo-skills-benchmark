# SEO Audit: Kopi Kita (kopikita.test)

Audited: 2026-10-22, against the local copy at http://localhost:8765/ (all 18 sitemap URLs plus linked and redirected URLs, robots.txt, sitemap.xml, images and CSS fetched with curl).

## Scope and limits

- No Search Console, analytics, or ranking data was available. Impact ratings are based on what the pages and headers show, not on traffic.
- Structured data was read from the raw HTML. The JSON-LD on this site is static in the HTML, so curl sees it reliably. Run the final pages through Google's Rich Results Test before shipping schema changes.
- Core Web Vitals could not be measured. The local server is Python SimpleHTTP, so headers (compression, caching, HSTS) and HTTPS/www behaviour on the real domain are noted as items to verify on production, not as confirmed faults.
- This is a small site (about 17 pages) selling Indonesian single-origin coffee online, with a cafe in Ubud and a wholesale line. Local search and product pages are the main SEO opportunity.

## Executive summary

The content is clear, specific and well written, and the basics (titles, descriptions, canonicals, viewport) are mostly in place. The problems are mostly in indexing signals, which contradict each other on several of the money pages:

1. **The wholesale page is set to `noindex`** while sitting in the sitemap and the main nav.
2. **`/shop/` canonicalises to `/coffee/`**, so the shop page will not be indexed under its own URL.
3. **`/subscriptions/` has the same title as `/coffee/`.**
4. **The sitemap lists a 404 (`/coffee/sumatra-mandheling/`)**, and a blog post links to another 404 (`/coffee/aceh-gayo/`).
5. **The nav link "Visit the cafe" goes through a two-step redirect chain** on every page of the site.
6. **robots.txt blocks the CSS directory**, which stops Google rendering pages as users see them.

Quick wins (under an hour in total): remove `noindex` from wholesale, fix the `/shop/` canonical, rewrite the subscriptions title, fix the sitemap, change the nav link to `/visit/`, and delete the CSS Disallow line.

---

## Priority 1: Critical (blocking indexing or ranking)

### 1.1 Wholesale page is `noindex` but is in the sitemap and nav
- **URL:** https://kopikita.test/wholesale/
- **Evidence:** The page has `<meta name="robots" content="noindex, follow">`. It is also listed in sitemap.xml, linked from the main nav and the homepage, and has a self-referencing canonical.
- **Why it matters:** Google will drop the page from the index, so nobody can find the wholesale offer (30+ cafes and hotels, free training, next-day delivery) by searching "wholesale coffee Bali" and similar. This is likely a B2B revenue page. The sitemap and canonical say "index me" while the robots tag says the opposite; the noindex wins.
- **Fix:** Remove the `noindex` tag unless the block is deliberate. If it is deliberate (for example a staging leftover), remove the page from the sitemap and the nav instead, and tell the owner that wholesale then has no organic presence. After the fix, request indexing in Search Console.

### 1.2 `/shop/` canonicalises to `/coffee/`
- **URL:** https://kopikita.test/shop/
- **Evidence:** `<link rel="canonical" href="https://kopikita.test/coffee/">`, yet the page has its own title ("Shop Coffee Beans and Brewing Gear"), H1 ("Shop") and different content (gear, drip bags, free-shipping threshold). It is also in the sitemap as its own URL.
- **Why it matters:** Google is told to treat /shop/ as a duplicate of /coffee/. The page will not rank for gear or drip-bag searches, and the sitemap entry contradicts the canonical.
- **Fix:** Decide the role of each page and make them different (see 2.4). Then give `/shop/` a self-referencing canonical. If `/shop/` is meant to be a duplicate, remove it from the sitemap and 301 it to `/coffee/`, and drop it from the nav.

### 1.3 Sitemap contains a URL that returns 404
- **URL:** https://kopikita.test/coffee/sumatra-mandheling/ (listed in sitemap.xml)
- **Evidence:** HTTP 404.
- **Why it matters:** A sitemap should hold only live, indexable, canonical URLs. 404s waste crawl budget and make Search Console report errors, which reduces trust in the file.
- **Fix:** Remove the entry, or publish the page. If the Sumatra coffee is a real product, publish a page with the same structure as the other three origins (see 2.5).

### 1.4 Broken internal link to a 404 page
- **URL affected:** https://kopikita.test/blog/how-to-brew-pour-over/ links to https://kopikita.test/coffee/aceh-gayo/ (HTTP 404)
- **Why it matters:** It is a dead end for users and crawlers, and it sits in the sentence that is supposed to send readers to a product page.
- **Fix:** Link to a product that exists (for example `/coffee/bali-kintamani/` or `/coffee/flores-bajawa/`), or publish the Aceh Gayo page.

### 1.5 Redirect chain on the nav link used by every page
- **URL:** https://kopikita.test/menu/ (linked as "Visit the cafe" from the nav on all 17 pages)
- **Evidence:** `/menu/` 301 → `/cafe/` 301 → `/visit/` 200. The sitemap and canonical use `/visit/`.
- **Why it matters:** Every internal link to this page passes through two redirects, which slows crawling and dilutes link signals. Google follows chains but may stop after several hops, and the final URL is the only one that should be linked.
- **Fix:** Change the nav link to `/visit/`. Point `/menu/` straight to `/visit/` with a single 301 (or retire it), and do the same for `/cafe/`.

### 1.6 robots.txt blocks the site CSS
- **URL:** https://kopikita.test/robots.txt
- **Evidence:** `Disallow: /assets/css/`. The only stylesheet is `/assets/css/site.css`.
- **Why it matters:** Google renders pages and needs CSS to judge layout, mobile-friendliness and Core Web Vitals. Blocking it can lead to wrong mobile and layout assessments.
- **Fix:** Delete the `Disallow: /assets/css/` line. Keep `Disallow: /cart/` only if a cart exists at that path (it currently returns 404, so it is harmless but pointless). Keep the Sitemap line.

---

## Priority 2: High impact

### 2.1 `/subscriptions/` and `/coffee/` share the same title
- **URLs:** https://kopikita.test/subscriptions/ and https://kopikita.test/coffee/
- **Evidence:** Both are titled "Single-Origin Indonesian Coffee | Kopi Kita". The subscriptions page is about recurring deliveries (from Rp 165,000, pause or cancel any time).
- **Why it matters:** Duplicate titles make the pages compete for the same query. The subscriptions page gets no chance to rank for "coffee subscription Indonesia/Bali" and Google may rewrite the title.
- **Fix:** Retitle the subscriptions page, for example "Coffee Subscription in Indonesia: Fresh Beans Every 2 or 4 Weeks | Kopi Kita". Keep the description, which is already specific.

### 2.2 Flores Bajawa product page is effectively orphaned
- **URL:** https://kopikita.test/coffee/flores-bajawa/
- **Evidence:** It is linked only from the sitemap. The homepage, `/coffee/` and `/shop/` link only to Bali Kintamani and Java Ijen. `/shop/` mentions "seasonal lots" but does not link this one.
- **Why it matters:** Pages with no internal links get little crawl attention and no link equity. A full product page is wasted.
- **Fix:** Link it from `/coffee/` (add a third entry next to the other two), `/shop/`, and the homepage. The `/coffee/` page says "three to five single origins", so listing all current origins is accurate.

### 2.3 Two blog posts compete for the same query
- **URLs:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Evidence:** Both target "pour over coffee" for beginners. Both give the same recipe (15g coffee, 250g water, 93C, 40g bloom, about three minutes) and both recommend Java Ijen. Titles: "How to Brew Pour Over Coffee at Home" and "Pour Over Coffee Guide for Beginners".
- **Why it matters:** Keyword cannibalisation. Google must choose one, rankings can flip between them, and link signals are split.
- **Fix:** Merge into one definitive page (keep `how-to-brew-pour-over`, which is longer and was published earlier, and move the dripper/filter/kettle advice from the guide into it). 301 the other URL to the survivor, remove it from the sitemap and blog index, and update internal links. The brewing guide at `/coffee/brewing-guide/` links to the survivor already.

### 2.4 `/coffee/` and `/shop/` overlap and are thin
- **URLs:** https://kopikita.test/coffee/ and https://kopikita.test/shop/
- **Evidence:** Both are short lists (about 100 words) of links and one-line descriptions. `/shop/` mentions V60 drippers, a grinder, a scale and drip bags with no links to any product page, price or image. Neither page has images.
- **Why it matters:** These are the category-level pages that should rank for "buy coffee beans Bali/Indonesia". With no products, prices or images on them they have little to rank with and give users no way to buy.
- **Fix:** Make `/coffee/` the origin listing with a card per coffee (image, name, process, notes, price from, link). Make `/shop/` the gear and drip-bag listing, with a page or anchor for each item, or fold `/shop/` into `/coffee/` and redirect. Add a short buying guide (roast levels, process, bag sizes) to `/coffee/`.

### 2.5 Sitemap and nav inconsistencies
- **URL:** https://kopikita.test/sitemap.xml
- **Evidence:** There are no `<lastmod>` values. It contains the 404 (1.3), and `/shop/` and `/wholesale/` whose signals conflict (1.1, 1.2). The article `best-coffee-beans-2024` is updated in 2026 but the sitemap has no date to show it.
- **Why it matters:** Accurate lastmod helps Google prioritise recrawls of updated pages.
- **Fix:** Generate the sitemap from the CMS, include `lastmod` that reflects real content changes, and include only 200, indexable, self-canonical URLs. Submit it in Search Console and Bing Webmaster Tools.

### 2.6 "2024" baked into the best-beans article
- **URL:** https://kopikita.test/blog/best-coffee-beans-2024/
- **Evidence:** The URL, title ("2024 Guide") and H1 ("2024 guide") say 2024, but the page claims "Our picks this year" and `dateModified` is 2026-09-01. The Article schema headline ("The best coffee beans in Bali") differs from the H1 and the page title.
- **Why it matters:** A dated title looks stale in 2026 and hurts click-through. A year in the URL means changing it later requires a redirect. The mismatch between schema headline, H1 and title is a weak consistency signal.
- **Fix:** Move the page to an evergreen URL such as `/blog/best-coffee-beans-bali/` with a 301 from the old one, drop the year from the title and H1 (or update it to 2026 if you want to keep a year), and make the Article headline match the H1. Add the update date visibly on the page.
- **Also:** The title says "Best Coffee Beans in Bali" but the article recommends the shop's own coffee plus "any good local roaster". That is acceptable, but add 2 or 3 named origins or farms to earn the "best" claim.

### 2.7 No LocalBusiness / cafe structured data or Google Business Profile signals
- **URLs:** https://kopikita.test/ (Organization schema only), https://kopikita.test/visit/, https://kopikita.test/contact/
- **Evidence:** The homepage has an Organization schema with an address but no phone, no `sameAs`, no opening hours, no geo. `/visit/` and `/contact/` have no schema at all. The opening hours (7am to 5pm daily), phone/WhatsApp and address are visible in the text of those pages.
- **Why it matters:** Kopi Kita has a physical cafe and roastery. "Coffee shop Ubud" style searches depend on the Business Profile and on consistent name, address and phone data. Without local markup the site gives Google less to confirm them with.
- **Fix:** Add `CafeOrCoffeeShop` (or `LocalBusiness`) JSON-LD on `/visit/` with name, address, geo coordinates, `openingHoursSpecification`, `telephone`, `image`, `url` and `sameAs` (Instagram, Google Maps profile). Reference the same entity from the Organization on the homepage. Claim and complete the Google Business Profile, and keep the name, address and phone identical on the site, the profile and any directories. Embed a map on `/visit/`.

### 2.8 `/visit/` has no H1
- **URL:** https://kopikita.test/visit/
- **Evidence:** The page has two H2s ("Opening hours", "Menu") and no H1. The nav calls the page "Visit the cafe".
- **Why it matters:** The H1 is the clearest topical statement on a page; this one is a primary local landing page.
- **Fix:** Add an H1 such as "Visit our roastery cafe in Ubud" above the hours. Also add an image and a short "getting there" section with directions and a map.

---

## Priority 3: Medium

### 3.1 Brewing guide has two H1s
- **URL:** https://kopikita.test/coffee/brewing-guide/
- **Evidence:** `<h1>Coffee brewing guide</h1>` and later `<h1>Brew methods</h1>`.
- **Fix:** Change the second to an H2, and consider H3s per method (pour over, French press, espresso, cold brew) so each can rank on its own. The page also shows its method list as plain paragraphs; a table of ratios and grind sizes would be easier to scan and more likely to earn featured snippets.

### 3.2 Product title too long and Product schema incomplete
- **URL:** https://kopikita.test/coffee/bali-kintamani/
- **Evidence:** The title is "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita" (about 88 characters), which will be truncated in results. The Product JSON-LD has no `name` property. Price is 145000 IDR but the page also sells a 1kg bag at Rp 520,000 with no matching offer.
- **Fix:** Shorten to about 55 characters: "Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita". Add `name`, `sku`, `url`, and an `Offer` per bag size. Consider adding `shippingDetails` and `hasMerchantReturnPolicy` for merchant listing eligibility, and add aggregate rating only when real reviews exist.
- **Also:** `/coffee/flores-bajawa/` has no Product schema at all (Bali and Ijen do). Add it in the same pattern. On `/coffee/java-ijen/` the schema is otherwise valid but also lacks the 1kg offer.

### 3.3 FAQPage schema on `/coffee/` is not matched by visible content
- **URL:** https://kopikita.test/coffee/
- **Evidence:** The JSON-LD has two questions ("How fresh is your coffee?", "Do you ship outside Bali?"), but the page has no visible FAQ section.
- **Why it matters:** Markup should describe content users can see. FAQ rich results are also now limited to a small set of sites, so a commercial site is unlikely to get them.
- **Fix:** Either add the questions and answers to the page body as a visible FAQ (useful for users and for AI answers) or remove the schema.

### 3.4 About page: missing meta description, oversized hero image
- **URL:** https://kopikita.test/about/
- **Evidence:** No `<meta name="description">`. The hero image `/assets/img/roastery-hero.jpg` is 1,818,123 bytes (about 1.8MB) at 2400x1600, with no responsive sources.
- **Why it matters:** Google will write its own snippet. A 1.8MB image delays Largest Contentful Paint (the target is under 2.5s), especially on mobile connections in Indonesia.
- **Fix:** Add a description (about 150 characters, mention the 2019 start, farmer partnerships and Ubud roastery). Resize and compress the image (target under 200KB), serve WebP or AVIF with `srcset`, and keep the explicit width and height already set.

### 3.5 Homepage hero image has no alt text
- **URL:** https://kopikita.test/ (`/assets/img/hero-beans.jpg`)
- **Evidence:** `<img src="/assets/img/hero-beans.jpg" width="1200" height="700">` has no `alt`. The file name is acceptable.
- **Fix:** Add a descriptive alt, such as "Freshly roasted single-origin coffee beans from Bali". Do not lazy-load this image because it is the likely LCP element; consider `fetchpriority="high"`.

### 3.6 Contact page has no canonical
- **URL:** https://kopikita.test/contact/
- **Evidence:** All other pages have a self-referencing canonical; this one does not.
- **Fix:** Add `<link rel="canonical" href="https://kopikita.test/contact/">`. Add `ContactPage` or use the LocalBusiness data from 2.7.

### 3.7 Blog content depth and structure
- **URLs:** https://kopikita.test/blog/cold-brew-at-home/ and the blog index
- **Evidence:** The cold brew post is a single paragraph of about 80 words, with no headings, no list, no image and no schema, so it is unlikely to beat established results for a competitive query. The blog index is a bare list of four links with no dates, excerpts or categories.
- **Fix:** Expand the cold brew post (ratio table, steep time by roast, dilution, storage, troubleshooting, a photo) or fold it into the brewing guide and redirect. Add dates, short summaries and thumbnails to the blog index, and link each post to the related product and to the brewing guide.

### 3.8 Article schema is thin
- **URLs:** the three blog posts that have it
- **Evidence:** Article JSON-LD has headline, dates and author name only. No `image`, `publisher`, `mainEntityOfPage`, or author `url`.
- **Fix:** Add `image`, `publisher` (Organization with logo), `mainEntityOfPage`, and link the author to a short author profile (Wayan Sudarma, head roaster, 12 years, trained in Melbourne, which is already stated on `/about/`). That is a real experience signal and worth showing on each article with a byline.

---

## Priority 4: Low and housekeeping

### 4.1 No favicon
- **URL:** https://kopikita.test/favicon.ico returns 404, and no `<link rel="icon">` is declared. Add a favicon (and an Apple touch icon); it also appears next to the site name in mobile search results.

### 4.2 No Open Graph or Twitter Card tags
- **URLs:** all pages
- **Fix:** Add `og:title`, `og:description`, `og:image`, `og:url`, `og:type` and `twitter:card`. Product and blog pages should use their own images, so shares on WhatsApp and Instagram show a preview. This is relevant here because WhatsApp is the main contact channel.

### 4.3 Homepage content and linking
- **URL:** https://kopikita.test/
- **Evidence:** Good opening copy, but only coffee, brewing guide, blog and wholesale links in the body. No links to `/subscriptions/`, `/shop/`, `/visit/` or Flores Bajawa, no WebSite schema, and no testimonials or reviews.
- **Fix:** Add short sections linking to subscriptions, the cafe, and all three origins, and use descriptive anchor text. Add reviews with their source when available (also an E-E-A-T trust signal). Add `WebSite` schema.

### 4.4 Weak anchor text and no breadcrumbs
- **Evidence:** The nav says "Visit the cafe" while the page is titled "Visit Our Roastery Cafe"; the footer has only a Contact link. Product and blog pages have no breadcrumbs.
- **Fix:** Add `BreadcrumbList` markup and visible breadcrumbs (Home › Coffee › Bali Kintamani). Add footer links to the main sections.

### 4.5 Meta descriptions slightly short on a few pages
- **Evidence:** `/coffee/` (about 105 characters) and `/blog/cold-brew-at-home/` (about 85 characters) are under the 150 to 160 target. All others are within range and unique.
- **Fix:** Extend them with a benefit and a call to action.

### 4.6 Custom 404 page
- **Evidence:** Missing URLs return a correct 404 status, but the page is the bare server default with no navigation.
- **Fix:** Create a branded 404 page with the nav and links to coffee, shop and blog. Keep the 404 status code.

### 4.7 Language and market targeting
- **Evidence:** The site is English only (`<html lang="en">`), with no hreflang. That is correct for a single-language site and is not an error. Many customers in Indonesia search in Indonesian ("kopi Bali", "biji kopi Kintamani", "beli kopi online").
- **Fix (strategic):** Consider an Indonesian version under `/id/` with fully translated content, self-referencing canonicals, reciprocal hreflang with `x-default`, and sitemap annotations. Only do this if there is demand and you can translate the main content, not just the navigation.

---

## Verify on production (not testable locally)

- HTTP to HTTPS 301, and a single canonical host (www vs non-www). All canonicals already use `https://kopikita.test/` without www.
- Compression (gzip/brotli), long cache lifetimes on `/assets/` files, HSTS, a CDN. The local server sends none of these.
- Core Web Vitals in PageSpeed Insights and Search Console after the image work in 3.4 and 3.5. `site.css` is only 149 bytes, so CSS delivery is not a concern.
- Mixed content, TLS certificate, and that `https://kopikita.test/robots.txt` and the sitemap are reachable at the production domain.

## What is working

- Every page has a unique title under about 65 characters (except the two noted), a viewport tag and a self-referencing canonical (except `/contact/`).
- Meta descriptions are present, unique and specific on 15 of 17 pages.
- URLs are short, lowercase, hyphenated and logically grouped (`/coffee/…`, `/blog/…`). Trailing-slash redirects work (`/coffee` → `/coffee/`).
- Content is specific and credible: named farmer groups, altitudes, harvest dates, prices, a named head roaster, a physical address.
- Images have alt text and explicit dimensions (except the homepage hero), which prevents layout shift.
- Product pages for Bali Kintamani and Java Ijen have valid Product and Offer markup and good internal links to the brewing guide.
- robots.txt includes the sitemap reference; the sitemap is valid XML.

## Prioritised action plan

| # | Action | URL(s) | Effort |
|---|--------|--------|--------|
| 1 | Remove `noindex` from wholesale (or remove from nav and sitemap) | /wholesale/ | 5 min |
| 2 | Fix `/shop/` canonical; differentiate from `/coffee/` | /shop/, /coffee/ | 15 min, then content work |
| 3 | Remove 404 from sitemap; fix the dead Aceh Gayo link | sitemap.xml, /blog/how-to-brew-pour-over/ | 10 min |
| 4 | Point nav to `/visit/`, collapse the redirect chain | all pages, /menu/, /cafe/ | 10 min |
| 5 | Delete the CSS Disallow in robots.txt | /robots.txt | 2 min |
| 6 | Rewrite the subscriptions title | /subscriptions/ | 5 min |
| 7 | Link Flores Bajawa from coffee, shop and home | /coffee/flores-bajawa/ | 15 min |
| 8 | Merge the two pour-over posts, 301 one to the other | /blog/… | 1 to 2 hours |
| 9 | Add LocalBusiness schema, H1 and map to `/visit/`; complete Google Business Profile | /visit/ | 1 to 2 hours |
| 10 | Product schema fixes, shorter Bali Kintamani title, Flores Product schema | /coffee/… | 1 hour |
| 11 | About: meta description, compress hero image; homepage hero alt | /about/, / | 30 min |
| 12 | Remove the year from the best-beans URL/title, with 301 | /blog/best-coffee-beans-2024/ | 30 min |
| 13 | Brewing guide second H1 to H2; contact canonical; FAQ visible or removed | various | 30 min |
| 14 | OG tags, favicon, breadcrumbs, branded 404, blog index upgrade | site-wide | half a day |
| 15 | Expand the cold brew post; consider an Indonesian-language version | long-term | ongoing |
