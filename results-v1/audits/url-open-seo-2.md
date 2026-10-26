# SEO Audit: Kopi Kita (kopikita.test)

Audited 2026-10-22 against the local copy at http://localhost:8765/. I fetched every page in the sitemap, plus the pages linked from them and `robots.txt`.

## Limits of this audit

- The OpenSEO tools (site crawl, rankings, search volumes, Search Console) were not connected. This audit covers only what curl can see: status codes, HTML, structured data and links.
- No ranking or traffic figures are included. I have not checked any live position or search volume, so I make no claims about current rankings.
- Priority reflects likely business impact judged from the page content. Where I say a page "would" rank or "may" lose traffic, that is inference, not measurement.
- Terms: a *canonical* is the tag that tells search engines which URL is the preferred version of a page. A *noindex* tag tells them to keep the page out of search results. A *301* is a permanent redirect.

## Summary

The site is small (18 sitemap URLs), fast to read and mostly clean. The biggest problems are self-inflicted indexing signals: the wholesale page is set to noindex, the shop page names a different page as its preferred version, and the sitemap lists a page that returns 404. Fixing the top five items is about an hour of work.

What is working: every page has a unique `<title>` except one, canonicals are present on most pages, product pages carry specific content (altitude, process, varieties, price), Product schema prices match the visible prices, and the blog has real depth on the pour over posts.

---

## Priority 1: Fix these first (blocking or likely losing traffic)

### 1. Wholesale page is set to noindex
- **URL:** https://kopikita.test/wholesale/
- **Found:** `<meta name="robots" content="noindex, follow">`. The same page is in the sitemap, linked from the main navigation and from the home page.
- **Why it matters:** `noindex` keeps the page out of Google. This is the page for cafes and hotels, the highest-value buyers on the site (the page says 30+ partners and a 5kg per week minimum). It cannot rank for searches such as wholesale coffee in Bali while this tag is present. The sitemap and the tag also contradict each other.
- **Fix:** Remove the robots meta tag (or change it to `index, follow`). Re-request indexing in Search Console. If the tag was left from staging, check for other staging leftovers.

### 2. Shop page declares /coffee/ as its canonical
- **URL:** https://kopikita.test/shop/
- **Found:** `<link rel="canonical" href="https://kopikita.test/coffee/">`. /shop/ is also in the sitemap.
- **Why it matters:** The canonical tells Google to treat /shop/ as a duplicate of /coffee/ and index only /coffee/. /shop/ covers things /coffee/ does not (brewing gear, drip bags, free shipping threshold), so searches for those products have no page to land on.
- **Fix:** Change the canonical to `https://kopikita.test/shop/`. If you really want one page, 301 redirect /shop/ to /coffee/ and remove it from the sitemap and navigation instead. Given the distinct content, keeping /shop/ is the better option.

### 3. Sitemap lists a page that returns 404
- **URL:** https://kopikita.test/coffee/sumatra-mandheling/
- **Found:** In `sitemap.xml`, but the server returns 404. Nothing links to it.
- **Why it matters:** Error URLs in a sitemap waste crawl attention and lower trust in the sitemap. If the coffee is meant to exist, a product page is missing.
- **Fix:** Remove it from the sitemap, or publish the page (with Product schema and a link from /coffee/) if the coffee is real.

### 4. Broken internal link on the top blog post
- **URL affected:** https://kopikita.test/blog/how-to-brew-pour-over/ links to https://kopikita.test/coffee/aceh-gayo/ (404).
- **Why it matters:** The link sits in the paragraph that recommends a coffee, which is the purchase prompt in the post. Visitors hit a dead end and the page loses a path to a product.
- **Fix:** Link to an existing coffee (for example /coffee/bali-kintamani/), or create the Aceh Gayo page if it is a real product.

### 5. Main navigation sends every visitor through a redirect chain
- **URL:** The "Visit the cafe" link on every page points to /menu/, which 301s to /cafe/, which 301s to /visit/.
- **Why it matters:** Two hops on a sitewide link slows users and wastes crawl effort, and dilutes the signal to the real URL. The sitemap and the about page already use /visit/.
- **Fix:** Change the nav link to `/visit/`. Then make /menu/ and /cafe/ each 301 straight to /visit/ in one step.

---

## Priority 2: Content and search-intent problems

### 6. Two pour over posts target the same query
- **URLs:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Found:** Both give the same recipe (15g coffee, 250g water, 93C, 40g bloom, about three minutes) and compete for "how to make pour over coffee" searches. The brewing guide at /coffee/brewing-guide/ also repeats the recipe.
- **Why it matters:** When two pages answer one query, Google picks one and the other adds little; links and signals are split between them.
- **Fix:** Pick one as the main page (the how-to post is longer and more recently updated). Either merge the beginner material (dripper choice, filter rinse) into it and 301 the other, or reposition the beginner guide around a clearly different query (gear for beginners, common mistakes). Cross-link the pages with distinct anchor text.

### 7. "Best coffee beans" post has a stale year in the URL and title
- **URL:** https://kopikita.test/blog/best-coffee-beans-2024/
- **Found:** Slug, title and H1 say 2024, but `dateModified` is 2026-09-01 and the body says "our picks this year". The Article schema headline omits the year, which does not match the H1.
- **Why it matters:** The year signals out-of-date content to searchers and lowers click-through. Changing the slug later costs a redirect, so it is cheapest to fix now.
- **Fix:** Move to an evergreen URL such as `/blog/best-coffee-beans-in-bali/` with a 301 from the old one. Drop the year from the title and H1, or update it to the current year. Align the schema headline with the H1. Also link to more than one of your own coffees: the post only links Kintamani and recommends "any good local roaster" for washed coffee, which sends the buyer away.

### 8. Subscriptions page reuses the Coffee page title
- **URL:** https://kopikita.test/subscriptions/
- **Found:** Title is "Single-Origin Indonesian Coffee | Kopi Kita", identical to /coffee/.
- **Why it matters:** The title is the main ranking and click signal. This one does not describe the offer, and it competes with the /coffee/ page for the same wording.
- **Fix:** Use something like "Coffee Subscription in Bali and Indonesia: Fresh Beans Every 2 or 4 Weeks | Kopi Kita".

### 9. Flores Bajawa is not linked from the coffee pages
- **URL:** https://kopikita.test/coffee/flores-bajawa/
- **Found:** Linked only from the sitemap. /coffee/ and /shop/ link to Kintamani and Ijen only, and /coffee/ meta description says it sells Flores coffee.
- **Why it matters:** Pages with no internal links are discovered late and get little authority. This is a priced product with no route to it for shoppers either.
- **Fix:** Add a link and a one-line description on /coffee/ and /shop/, and link it from the home page. Add Product schema (see item 14).

### 10. Cold brew post is thin
- **URL:** https://kopikita.test/blog/cold-brew-at-home/
- **Found:** About 80 words in a single paragraph, no structured data, no further sections.
- **Why it matters:** Other posts here run to several hundred words and cover troubleshooting, equipment and variations. A one-paragraph recipe is unlikely to be competitive for a popular query.
- **Fix:** Expand with ratio variations, steep time and its effect on taste, which coffees work best, storage, and how to serve. Add Article schema like the other posts.

### 11. Blog posts and guides rarely lead to a purchase
- **URLs:** Blog posts, /coffee/brewing-guide/
- **Found:** The pour over posts mention one or two coffees; none link to /shop/ (gear) or /subscriptions/. The pour over posts recommend a grinder and scale without linking to the shop page that sells them.
- **Fix:** Add contextual links to /shop/ (grinder, scale, V60), /subscriptions/ and the relevant coffee page.

---

## Priority 3: On-page and technical fixes

### 12. Contact and About pages lack metadata
- **URLs:** https://kopikita.test/contact/ (no canonical), https://kopikita.test/about/ (no meta description)
- **Fix:** Add a canonical to Contact and a meta description to About. Without one, Google writes its own snippet from page text.

### 13. Heading structure
- **/visit/** has no `<h1>`; the page starts at `<h2>Opening hours</h2>`. Add `<h1>Visit our roastery cafe in Ubud</h1>`.
- **/coffee/brewing-guide/** has two `<h1>` elements ("Coffee brewing guide" and "Brew methods"). Change the second to `<h2>`.

### 14. Structured data gaps and mismatches
- **Bali Kintamani** Product schema has no `name`. Add it, along with `sku` or `mpn` where possible.
- **Flores Bajawa** has no Product schema, while the other two coffees do. Add it.
- **/coffee/** has FAQPage schema, but the FAQ is not visible on the page. The "Do you ship outside Bali?" answer appears nowhere in the visible text. Schema content should match what users see. Either add the FAQ to the page or remove the markup. (Google now shows FAQ rich results only for a few types of site, so the gain is small either way.)
- **Home** has Organization schema only. Add `LocalBusiness` or `CafeOrCoffeeShop` markup with opening hours (7am to 5pm daily), phone, geo coordinates and `sameAs` links to social profiles and the Google Business Profile. This supports Maps and local results for Ubud searches.
- **Blog index and cold brew post** have no Article or `ItemList` markup; the other three posts do. Add `image` to Article schema.
- Consider `BreadcrumbList` on product and blog pages.

### 15. Titles
- Bali Kintamani title is 83 characters ("Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita"). It will be truncated. Shorten to about 60 characters, such as "Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita".
- Home, wholesale and a few others are close to the limit; keep new titles under about 60 characters.

### 16. Images
- Home hero image `/assets/img/hero-beans.jpg` has no `alt` text.
- `/assets/img/roastery-hero.jpg` on /about/ is 1.8 MB and 2400 px wide. Compress it (aim for under 200 KB, WebP or AVIF) and add `srcset`. Large images slow load and affect Core Web Vitals.
- Add `loading="lazy"` to images below the fold; do not lazy-load the main hero.

### 17. robots.txt blocks CSS
- **URL:** https://kopikita.test/robots.txt
- **Found:** `Disallow: /assets/css/`.
- **Why it matters:** Google renders pages the way a browser does, and blocked stylesheets can stop it seeing the layout correctly. There is no benefit to blocking CSS.
- **Fix:** Remove that line. Keep `Disallow: /cart/`. Check that the sitemap URL is the production one (it already is).

### 18. Social sharing tags are missing
- **URLs:** All pages.
- **Fix:** Add Open Graph and Twitter Card tags (`og:title`, `og:description`, `og:image`, `og:url`, `twitter:card`). Links shared on WhatsApp and Instagram, which matter for this audience, otherwise show a plain preview.

### 19. Sitemap quality
- No `<lastmod>` dates. Add them, kept accurate to real edits.
- Fix the 404 entry (item 3) and make sure only indexable, canonical URLs are listed (items 1 and 2).

### 20. Error page
- Unknown URLs return Python's generic "Error response" page with status 404. The status is correct, but add a branded 404 page with links to the shop, coffees and blog so visitors can recover.

---

## Priority 4: Opportunities and housekeeping

- **Language and market:** The site is English only and targets Indonesia and Bali. If a meaningful share of buyers search in Indonesian (for example "kopi Bali", "beli kopi Kintamani"), consider Indonesian pages with `hreflang`. Not testable without keyword data.
- **Local presence:** Make sure the Google Business Profile for the Ubud cafe uses the same name, address and phone as the footer and /contact/ ("Jl. Raya Sayan 12"). Add an embedded map and directions on /visit/.
- **About page trust signals:** Name the farmer groups and link to photos; add the team and roaster credentials (Wayan Sudarma is named as author on posts, so add an author bio page and link to it from the Article schema).
- **Shipping and policy content:** Free shipping thresholds (Rp 500,000, Bali free on subscriptions) appear on some pages only. A short shipping and returns page would answer a common pre-purchase question and link support content.
- **Blog index:** Add dates, summaries and categories, not just four bare links, as the blog grows.
- **Wholesale page:** Once indexable, add a simple enquiry form and venue examples or testimonials, and mention the delivery areas (Ubud, Canggu, Seminyak, Sanur) in headings.
- **Verify after fixes:** Resubmit the sitemap in Search Console and check the Pages report for "Excluded by noindex" and "Alternate page with proper canonical" on /wholesale/ and /shop/.

## Suggested order of work

1. Remove noindex from /wholesale/ (item 1).
2. Fix /shop/ canonical (item 2).
3. Clean the sitemap and fix the broken link and nav redirect chain (items 3, 4, 5).
4. Rewrite the subscriptions title and fix missing metadata and headings (items 8, 12, 13).
5. Link Flores Bajawa and add schema (items 9, 14).
6. Consolidate the pour over posts and refresh the best beans post (items 6, 7).
7. Everything else as time allows.
