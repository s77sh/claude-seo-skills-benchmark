# SEO Audit: Kopi Kita (kopikita.test)

Method: crawled the local copy at http://localhost:8765/. I fetched all 18 sitemap URLs, plus /menu/, /cart/, robots.txt, a 404 URL and the key assets, and read the raw HTML and headers. I could not measure rendered performance, Core Web Vitals, HTTPS or real-world rankings. Findings are limited to what the raw HTML and headers show.

Priority: **P1** = fix now (lost indexing, broken pages, wrong signals), **P2** = fix soon, **P3** = polish.

---

## P1: Critical

### 1. /shop/ canonicalises to /coffee/ (the page deindexes itself)
- **URL:** https://kopikita.test/shop/
- **Found:** `<link rel="canonical" href="https://kopikita.test/coffee/">`. /shop/ is also listed in the sitemap.
- **Why it matters:** Google will most likely treat /shop/ as a duplicate of /coffee/ and drop it from the index. This page is the commercial head page for "buy coffee beans / brewing gear / drip bags". The sitemap and canonical contradict each other.
- **Fix:** Change the canonical to `https://kopikita.test/shop/`. If /shop/ really is meant to be merged into /coffee/, 301 it, remove it from the sitemap and the nav.

### 2. /wholesale/ is set to noindex but linked everywhere and in the sitemap
- **URL:** https://kopikita.test/wholesale/
- **Found:** `<meta name="robots" content="noindex, follow">`, a self-referencing canonical, a sitemap entry, and a sitewide nav link.
- **Why it matters:** The page has good B2B content ("wholesale coffee Bali", "cafes and hotels"), a unique title and a unique description. It can never rank while it is noindexed. This looks like a staging leftover.
- **Fix:** Remove the robots meta tag. If the page is intentionally private, remove it from the sitemap and nav instead (and then consider a login wall).

### 3. Sitemap URL /coffee/sumatra-mandheling/ returns 404
- **URL:** https://kopikita.test/coffee/sumatra-mandheling/ (listed in https://kopikita.test/sitemap.xml)
- **Found:** HTTP 404.
- **Why it matters:** 404s in the sitemap waste crawl budget, show up as errors in Search Console and reduce trust in the sitemap.
- **Fix:** Remove it from the sitemap, or publish the product page. If the product was discontinued, remove the entry and redirect to /coffee/.

### 4. Broken internal link to /coffee/aceh-gayo/
- **URL affected:** https://kopikita.test/blog/how-to-brew-pour-over/ (link target: /coffee/aceh-gayo/, 404)
- **Why it matters:** A dead end for users and crawlers, in a post that is also a top-of-funnel page.
- **Fix:** Create the product page, or link to an existing coffee such as /coffee/bali-kintamani/ and remove the link otherwise.

### 5. The nav "Visit the cafe" link goes via a redirect chain, and the old URL is still in use
- **URL:** /menu/ (linked in the main nav on every page) → 301 → /cafe/ → 301 → /visit/
- **Why it matters:** Every page links to a URL that takes two hops to reach the real page. Link equity decays across hops and crawlers may give up on chains. The sitemap and the About page use /visit/ directly, so internal linking is inconsistent.
- **Fix:** Change the nav link to `/visit/` on all pages. Make /menu/ and /cafe/ each 301 straight to `/visit/` (single hop).

### 6. Keyword cannibalisation: two near-identical pour over posts
- **URLs:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Found:** Both target the same intent ("how to make pour over coffee"): same recipe (15g/250g/93C/40g bloom/3 min), same Java Ijen CTA, similar titles, similar descriptions. Neither links to the other.
- **Why it matters:** The two pages compete with each other for the same queries, so neither ranks as well as one stronger page would.
- **Fix:** Pick one winner (probably /blog/how-to-brew-pour-over/, which is older and has more depth). Merge the best material from the other, 301 the loser to the winner and update the blog index and sitemap. If you keep both, differentiate them clearly (beginner gear guide vs. step-by-step recipe) and cross-link them.

---

## P2: Important

### 7. Duplicate title tag on two different pages
- **URLs:** https://kopikita.test/coffee/ and https://kopikita.test/subscriptions/
- **Found:** Both use `Single-Origin Indonesian Coffee | Kopi Kita`. The subscriptions title is clearly a copy-paste from /coffee/.
- **Why it matters:** The subscriptions page does not describe its own offering, so it won't rank for "coffee subscription Bali / Indonesia" and the SERP snippet is misleading.
- **Fix:** For example, `Coffee Subscriptions: Fresh Single-Origin Delivered | Kopi Kita`.

### 8. Missing meta description
- **URL:** https://kopikita.test/about/
- **Why it matters:** Google writes its own snippet, which is often weaker and less controlled.
- **Fix:** Add a 140–160 character description, e.g. "Kopi Kita started in 2019 with a 1kg roaster in Ubud. Meet the team and the farmer groups in Bali, Java and Flores we buy from."

### 9. Missing canonical tag
- **URL:** https://kopikita.test/contact/
- **Why it matters:** Every other page has one. Without it, URL variants (tracking parameters, no trailing slash) are not consolidated.
- **Fix:** Add `<link rel="canonical" href="https://kopikita.test/contact/">`.

### 10. Heading structure on /visit/ has no H1
- **URL:** https://kopikita.test/visit/
- **Found:** Only `<h2>Opening hours</h2>` and `<h2>Menu</h2>`; no `<h1>`.
- **Why it matters:** The page's main topic is not stated to search engines or screen readers. It is the local-intent page ("cafe in Ubud").
- **Fix:** Add `<h1>Visit our roastery cafe in Ubud</h1>` at the top of `<main>`.

### 11. Multiple H1s on the brewing guide
- **URL:** https://kopikita.test/coffee/brewing-guide/
- **Found:** `<h1>Coffee brewing guide</h1>` and a second `<h1>Brew methods</h1>`. Later sections ("Grind size chart", "Water temperature", "Troubleshooting") are bold paragraphs, not headings.
- **Fix:** Change "Brew methods" to `<h2>`. Convert the bold lead-ins into `<h2>`/`<h3>` headings. The same applies to the bold-lead-in sections in the two pour over posts and the best-beans post: they should be `<h2>`s so search engines can see the structure and potentially surface jump links.

### 12. Hero image on /about/ is 1.8 MB and has no lazy loading or modern format
- **URL:** https://kopikita.test/about/ (`/assets/img/roastery-hero.jpg`, 1,818,123 bytes, declared 2400×1600)
- **Why it matters:** It is likely the LCP element and it is far too heavy, especially for mobile users in Indonesia. Slow LCP hurts Core Web Vitals and rankings.
- **Fix:** Resize to the displayed width (the layout is about 46rem wide, so ~1400px max with a 2x variant), compress, serve WebP/AVIF, and use `srcset`/`sizes`. The home hero (13.8 KB) is fine.

### 13. Home page hero image has no alt text
- **URL:** https://kopikita.test/ (`/assets/img/hero-beans.jpg`)
- **Why it matters:** Accessibility, and a lost image-search signal on the most important page.
- **Fix:** Add a descriptive `alt`, e.g. `alt="Freshly roasted single-origin coffee beans from Bali"`.

### 14. Product structured data is incomplete, and the Organization data is thin
- **URLs:** https://kopikita.test/coffee/bali-kintamani/ and https://kopikita.test/coffee/java-ijen/ (Product); https://kopikita.test/ (Organization)
- **Found:**
  - Kintamani Product JSON-LD has no `name` property (required by Google). Java Ijen has one.
  - Offers lack `url`, `priceValidUntil`, shipping/return details. Only the 250g price is marked up although a 1kg price exists on the page. Java Ijen's name says 250g but the page also sells 1kg.
  - Flores Bajawa has no Product markup at all, although it is a product page with a price.
  - Organization has no `sameAs` (social profiles), `contactPoint`, `telephone` or `email`. The cafe is a physical venue and could use `CafeOrCoffeeShop`/`LocalBusiness` markup with `openingHours`, `geo` and `telephone`.
- **Fix:** Add `name` to Kintamani; add Product markup to Flores Bajawa; add `url` to offers and consider an `offers` array for the 250g and 1kg sizes; add LocalBusiness/CafeOrCoffeeShop schema on /visit/ with hours (7am–5pm daily) and address; extend Organization with `sameAs` and `contactPoint`. Validate in the Rich Results Test.

### 15. FAQPage markup on /coffee/ with no visible FAQ
- **URL:** https://kopikita.test/coffee/
- **Found:** FAQPage JSON-LD (freshness, shipping outside Bali) but the page has no visible Q&A content. The answers only partly appear in body copy.
- **Why it matters:** Markup must match visible content, or it risks being ignored or treated as a structured-data policy violation. Also, Google now shows FAQ rich results only for a few authoritative sites, so there is little upside.
- **Fix:** Either add a visible FAQ section matching the markup, or remove the markup.

### 16. Article dates are inconsistent and the best-beans post is stale
- **URL:** https://kopikita.test/blog/best-coffee-beans-2024/
- **Found:** URL, `<title>` and H1 say "2024" but the JSON-LD headline says "The best coffee beans in Bali" (no year), `datePublished` is 2024-01-15 and `dateModified` is 2026-09-01. The date in the title and the URL is now almost three years out of date for a post that claims to be updated. The post says "Our picks this year".
- **Why it matters:** A "2024" label signals stale content to users and lowers click-through for "best coffee beans bali" queries. Changing the URL later costs equity.
- **Fix:** Retitle to an evergreen "Best Coffee Beans in Bali: How to Choose" or update to 2026. 301 `/blog/best-coffee-beans-2024/` to an evergreen slug (e.g. `/blog/best-coffee-beans-bali/`) and update the canonical, sitemap and blog link. Make sure the headline in JSON-LD matches the H1.

### 17. Thin content: cold brew post, Flores Bajawa and Shop pages
- **URLs:** https://kopikita.test/blog/cold-brew-at-home/ (one paragraph, ~75 words, no Article schema, no author, no date); https://kopikita.test/coffee/flores-bajawa/ (no brewing link, no schema); https://kopikita.test/shop/ (no product listings, only text and 2 links).
- **Why it matters:** Compared with the 400-600 word pour over posts, the cold brew post is too thin to rank for a competitive query, and it is the only blog post without Article schema and bylines.
- **Fix:** Expand the cold brew post into a proper guide (ratios, steeping time, dilution, storage, which beans), add an author, date and Article JSON-LD. Add links from /shop/ to all products (it omits Flores Bajawa) and to the 1kg options. Add a brewing-guide link to the Flores page.

### 18. robots.txt blocks the CSS directory
- **URL:** https://kopikita.test/robots.txt (`Disallow: /assets/css/`)
- **Why it matters:** Google needs CSS to render pages and evaluate mobile-friendliness. Blocking it can cause Google to see the page unstyled. (The current CSS is only 149 bytes, so there is little risk today, but the rule will matter as the site grows.)
- **Fix:** Remove `Disallow: /assets/css/`. `Disallow: /cart/` is fine (that path 404s locally; make sure it exists in production, or drop the rule).

---

## P3: Polish

### 19. Sitemap has no `<lastmod>` values
- **URL:** https://kopikita.test/sitemap.xml
- **Fix:** Add accurate `<lastmod>` values (especially for blog posts), and keep the sitemap limited to indexable, 200, canonical URLs (see issues 1–3 and 6).

### 20. Custom 404 page missing
- **URL:** any missing URL, e.g. https://kopikita.test/nonexistent-xyz/
- **Found:** The default server error page, with no navigation, and no noindex needed (the status is a correct 404).
- **Fix:** Serve a branded 404 with the site nav and links to the coffee, shop and blog pages. Keep the 404 status code. (This may be a local dev-server artefact.)

### 21. Title tag length and keyword on a couple of pages
- **URLs:** https://kopikita.test/coffee/bali-kintamani/ (title ~95 characters: "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita", will be truncated in results); https://kopikita.test/about/ (no keyword beyond brand).
- **Fix:** Shorten the Kintamani title to ≤60 characters, e.g. `Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita`.

### 22. Internal linking gaps
- **URLs:** https://kopikita.test/shop/, /contact/, /coffee/flores-bajawa/, /coffee/
- **Found:** Flores Bajawa is linked from nowhere except the sitemap (an orphan for crawl purposes: /coffee/ and /shop/ do not mention it). /coffee/ describes only two of the three coffees. The blog index has plain link text with no descriptions. Blog posts do not link to /shop/ or /subscriptions/, and /wholesale/ is only reachable from the home page and the nav.
- **Fix:** Link Flores Bajawa from /coffee/ and /shop/, add it to the coffee list copy, add contextual links from blog posts to the product pages and /subscriptions/, and add a short excerpt under each post on /blog/.

### 23. Sitewide: no social/Open Graph tags, favicon, or hreflang
- **URLs:** all pages
- **Found:** No `og:title`, `og:description`, `og:image`, `twitter:card` or favicon links in the head. The site targets Bali and Indonesia but is only in English, with no `hreflang` and no Indonesian version.
- **Fix:** Add OG/Twitter tags (use the product and hero images), a favicon, and consider an Indonesian (`id`) version with hreflang if you want to capture Indonesian-language searches.

### 24. Home page: thin internal linking to categories
- **URL:** https://kopikita.test/
- **Found:** Body copy links to the brewing guide, blog, wholesale and two products, but not to /shop/, /subscriptions/ or /visit/ except via the nav. Home title and H1 are good.
- **Fix:** Add contextual links to these pages in the body copy.

### 25. Image dimensions and alt are set, but file naming and formats are basic
- **URLs:** product pages
- **Fix:** Fine for now; consider WebP and descriptive file names (`bali-kintamani-natural-250g.jpg`).

---

## What looks fine
- Unique titles and descriptions on most pages (with the exceptions above), correct `lang="en"` and viewport tags.
- Clean, descriptive URL structure with trailing slashes. Self-referencing canonicals on most pages and absolute URLs.
- robots.txt points to the sitemap. Valid Article schema (with author and dates) on three of four posts.
- /coffee redirects to /coffee/ with a 301; logo and product images resolve.

## Recommended order of work
1. Fix the /shop/ canonical, remove noindex from /wholesale/ (issues 1, 2).
2. Clean the sitemap and the dead links (3, 4), and point the nav at /visit/ (5).
3. Resolve the pour over duplicate (6) and the duplicate title (7).
4. Fill in the metadata gaps: about description, contact canonical, /visit/ H1, headings (8–11).
5. Compress images, fix alt text and structured data (12–16).
6. Content and linking improvements, robots.txt and polish (17–25).
