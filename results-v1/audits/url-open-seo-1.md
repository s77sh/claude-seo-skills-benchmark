# SEO audit: Kopi Kita (kopikita.test)

Audited 22 Oct 2026 against the local copy at http://localhost:8765/. Every URL below is shown as its path on the production domain.

## Scope and limits

- The OpenSEO tools (site crawl, rankings, keyword volumes, search results, Search Console) were not connected in this session. This audit rests on fetching the site with curl.
- I fetched all 18 URLs in the sitemap, every navigation link, `robots.txt`, `sitemap.xml`, and the main images and stylesheet.
- I checked status codes, redirects, titles, meta descriptions, canonicals (the URL a page declares as its preferred version), robots directives, headings, structured data (machine-readable markup for search engines), images, internal links and page content.
- No ranking, traffic or search volume data was available. Nothing here claims a current position or a traffic number. Priorities are based on how directly each issue blocks pages from being found, indexed or clicked.
- The local server is a plain Python file server. Server-level items (HTTPS, compression, caching headers, response speed) were not testable and are left out.

## Summary

The site is small, clean and mostly well written. The biggest problems are self-inflicted signals that tell Google not to index or rank pages that earn money:

1. The wholesale page is set to `noindex` (Google is told not to show it).
2. The shop page tells Google that `/coffee/` is its preferred version.
3. A product page in the sitemap returns 404, and the blog has two competing pour over articles.

All are quick fixes.

---

## Priority 1: fix first (pages are blocked or lost)

### 1. Wholesale page is set to `noindex`

- **URL:** `/wholesale/`
- **Found:** `<meta name="robots" content="noindex, follow">`. The page is also in the sitemap and the main navigation, and has a title and description written to rank ("Wholesale Coffee for Cafes and Hotels in Bali").
- **Why it matters:** `noindex` tells Google to keep the page out of search results. Cafes and hotels searching for a wholesale coffee supplier in Bali can never find it. Wholesale is likely a high-value revenue line (30+ partners, weekly orders). The sitemap says "index this" while the page says "do not", which is a contradiction.
- **Fix:** Remove the `noindex` tag. If it was a leftover from staging, check that no other templates carry it. Resubmit the URL in Google Search Console after the change.
- **Also:** Add a contact or enquiry form on the page. It currently only says "contact us". Mention specific areas (Ubud, Canggu, Seminyak, Sanur) in the headings, as these are the searches the page should win.

### 2. Shop page canonicalised to the Coffee page

- **URL:** `/shop/` (canonical points to `https://kopikita.test/coffee/`)
- **Found:** `/shop/` has its own title, description and unique content (gear, drip bags, free shipping threshold), but its canonical tag names `/coffee/`. It is also listed in the sitemap.
- **Why it matters:** A canonical tells Google which page to show. Google will likely drop `/shop/` in favour of `/coffee/`, so searches for brewing gear, drip bags or "buy coffee beans" will not surface the shop page. The sitemap again conflicts with the page.
- **Fix:** Set the canonical on `/shop/` to `https://kopikita.test/shop/`. If the pages really are meant to be duplicates, instead redirect one to the other and remove it from the sitemap. Given the different content, keeping both is better.

### 3. Sumatra Mandheling page returns 404 but is in the sitemap

- **URL:** `/coffee/sumatra-mandheling/` (HTTP 404)
- **Found:** Listed in `sitemap.xml`. Not linked from anywhere on the site.
- **Why it matters:** Sitemaps should list only live, indexable pages. 404 entries waste crawl effort and show up as errors in Search Console. It lowers trust in the sitemap as a whole.
- **Fix:** Remove it from the sitemap, or publish the page if it is a planned product. If it once existed, 301 redirect it (a permanent redirect) to `/coffee/`.

### 4. Navigation "Visit the cafe" goes through a redirect chain

- **URL:** `/menu/` is linked in the main navigation of every page. It redirects `/menu/` to `/cafe/` (301), then `/cafe/` to `/visit/` (301).
- **Why it matters:** Every page on the site passes visitors and link value through two redirects to reach the cafe page. Redirect chains slow users down and can dilute signals. The sitemap correctly lists `/visit/`, so internal links disagree with it.
- **Fix:** Change the nav link on all pages to `/visit/` directly. Keep the old redirects, but make `/menu/` go straight to `/visit/` in one hop.

---

## Priority 2: content and ranking problems

### 5. Two near-identical pour over articles compete with each other

- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Found:** Both give the same recipe (15g coffee, 250g water at 93C, 40g bloom for 30 seconds, about three minutes) and target the same searches: "how to brew pour over coffee" and "pour over coffee guide". Their titles, descriptions and headings are close. The first is longer and has a newer `dateModified` (Aug 2026).
- **Why it matters:** When two pages answer the same query, Google tends to split ranking signals between them, or picks one at random, and neither ranks as well as one strong page would.
- **Fix:** Pick one winner (most likely `how-to-brew-pour-over`, which is longer and recently updated). Merge any unique material from the other (the dripper, filter and kettle advice) into it, then 301 redirect the weaker URL to the winner and remove it from the sitemap and blog index. If you want to keep both, differentiate them clearly: one a step-by-step recipe, the other a beginner gear guide with a different target query and title.

### 6. The "Best coffee beans" article has a stale year in its URL, title and heading

- **URL:** `/blog/best-coffee-beans-2024/`
- **Found:** Title "Best Coffee Beans in Bali (2024 Guide)", H1 "(2024 guide)", published January 2024 and modified Sep 2026. The structured data headline drops the year, so markup and page disagree.
- **Why it matters:** In late 2026 a "2024 guide" looks out of date in search results and lowers click-through, even if the content is current. The year is also baked into the URL, so renaming it means a redirect.
- **Fix:** Remove the year from the title and H1, or update it to the current year. Move to a year-free URL such as `/blog/best-coffee-beans-bali/` with a 301 from the old one, and update internal links and the sitemap. Make the page link to the product pages it recommends.

### 7. Duplicate title across `/coffee/` and `/subscriptions/`

- **URLs:** `/coffee/` and `/subscriptions/` both use "Single-Origin Indonesian Coffee | Kopi Kita".
- **Why it matters:** The titles are the main text in search results. Identical titles make the pages hard to tell apart for users and for Google, and the subscription page loses the chance to target subscription searches.
- **Fix:** Give `/subscriptions/` a unique title, for example "Coffee Subscription in Indonesia: Fresh Beans Every 2 or 4 Weeks | Kopi Kita".

### 8. Missing meta descriptions

- **URLs:** `/about/` has none.
- **Why it matters:** Without a description, Google writes its own snippet, which is often weaker and less persuasive.
- **Fix:** Add a unique description of about 150 characters to the about page.
- **Check:** `/contact/` has a description but no canonical (see item 12). The home page title and description are fine.

### 9. `/coffee/flores-bajawa/` is not linked from the Coffee page; Aceh Gayo is mentioned but does not exist

- **URLs:** `/coffee/` (lists only Kintamani and Ijen), `/shop/` (same two), `/blog/how-to-brew-pour-over/` (recommends "our Aceh Gayo" with no link and no product page).
- **Found:** Flores Bajawa is in the sitemap but only reachable through the sitemap itself, which makes it close to an orphan page (a page with no internal links). The `/coffee/` page says "three to five single origins" but links to two.
- **Why it matters:** Pages with no internal links get little crawl attention and no link value, and visitors never see the product. Mentioning a coffee that is not sold sends readers nowhere.
- **Fix:** List all current coffees on `/coffee/` and `/shop/` with links. Replace or remove the Aceh Gayo mention, or link it once a page exists.

### 10. Product pages are thin and inconsistently marked up

- **URLs:** `/coffee/bali-kintamani/`, `/coffee/java-ijen/`, `/coffee/flores-bajawa/`
- **Found:**
  - Bali Kintamani's Product markup has no `name` field.
  - Flores Bajawa has no Product markup at all, though it lists a price.
  - None of the product markup includes reviews or ratings, and none include SKU or weight.
  - The Kintamani title is very long (about 80 characters): "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita". It will be cut off in results.
- **Why it matters:** Product markup can make listings eligible for price and availability display. Missing `name` makes the existing markup invalid for rich results.
- **Fix:** Add `name` to Kintamani and add full Product markup to Flores. Shorten the Kintamani title to under 60 characters, for example "Bali Kintamani Natural Coffee Beans | Kopi Kita". Add a "Brew it with" link to the brewing guide from each product.

---

## Priority 3: technical and quality improvements

### 11. `robots.txt` blocks the stylesheet and a path that does not exist

- **URL:** `/robots.txt` (`Disallow: /assets/css/` and `Disallow: /cart/`).
- **Why it matters:** Google needs to load CSS to see pages the way visitors do. Blocking it can hurt how layout and mobile-friendliness are judged. `/cart/` currently returns 404, so that rule does nothing yet.
- **Fix:** Remove the `/assets/css/` rule. Keep `/cart/` only if a cart will exist, and then think about adding `noindex` rather than relying on `Disallow`, as blocked URLs can still appear in results.

### 12. Pages without a canonical tag

- **URL:** `/contact/` has no canonical. Every other page has one.
- **Fix:** Add a self-referencing canonical for consistency.

### 13. Trailing-slash and alias URLs

- **URLs:** `/coffee` redirects (301) to `/coffee/`, which is correct. `/menu/` and `/cafe/` are old aliases (see item 4).
- **Fix:** No action beyond item 4. Make sure all internal links use the final trailing-slash URLs.

### 14. Image issues

- **`/` hero image** (`/assets/img/hero-beans.jpg`): the `<img>` has no `alt` text. Add a description, for example "Freshly roasted single-origin coffee beans".
- **`/about/` hero image** (`/assets/img/roastery-hero.jpg`): about 1.8 MB, displayed at 2400 by 1600 pixels. This is likely to slow page load, especially on mobile. Resize to the largest size actually displayed, compress, and serve a modern format (WebP or AVIF) with `srcset` for smaller screens.
- Other images (product bags) have alt text and dimensions, which is good.

### 15. Two H1 headings on the brewing guide

- **URL:** `/coffee/brewing-guide/` has "Coffee brewing guide" and "Brew methods" both as H1.
- **Fix:** Make "Brew methods" an H2. Use one H1 per page.

### 16. Structured data gaps

- **Home:** Organization markup is present. Add `sameAs` links (Instagram and other profiles) and consider `LocalBusiness` or `CafeOrCoffeeShop` markup on `/visit/` with opening hours (7am to 5pm daily), phone and geo coordinates. This supports local searches such as "coffee roastery Ubud".
- **Blog posts:** Article markup lacks `image`, `mainEntityOfPage` and author `url`.
- **`/coffee/`:** FAQPage markup is present. Google now shows FAQ rich results only for a small set of sites, so do not expect visible gains.
- **Cross-page:** There is no BreadcrumbList markup.

### 17. Sitemap and crawl hygiene

- **URL:** `/sitemap.xml` has no `<lastmod>` dates.
- **Fix:** Add accurate `lastmod` values. Do not list redirected or blocked pages (`/shop/` as it stands, `/sumatra-mandheling/`). Submit the sitemap in Search Console once the fixes are done.

### 18. No social sharing tags

- **URLs:** All pages. There are no Open Graph or Twitter Card tags (`og:title`, `og:image`).
- **Why it matters:** Links shared on WhatsApp, Instagram and Facebook show as bare URLs, which cuts clicks from social sharing. This is not a ranking factor.
- **Fix:** Add `og:title`, `og:description`, `og:image` and `og:url` to the shared page template.

### 19. Custom 404 page

- **URL:** Any missing URL returns the default server error page ("Error response").
- **Fix:** Add a branded 404 page with links to `/coffee/`, `/shop/` and `/blog/`. Make sure it still returns a 404 status.

---

## Priority 4: opportunities (content and internal links)

### 20. Link the money pages from the content

- The home page body does not link to `/subscriptions/`, `/shop/` or `/visit/`, only to the two coffees, the brewing guide, blog and wholesale. Add links to subscriptions and the cafe.
- Blog posts link to products only in passing. Add a clear "Try it with" product link at the end of each post, and link the cold brew post to the brewing guide and a suitable coffee.
- The brewing guide and the blog should link to each other (the guide already links to the pour over post; the post links back).
- Use descriptive anchor text such as "Java Ijen washed coffee" rather than "contact us" or "the brewing guide" alone where it helps.

### 21. Local search

- The cafe and roastery are the strongest local assets. Beyond item 16, make sure the name, address and phone are identical on the site, on Google Business Profile and in directories. Publish the Saturday public cupping as a dated event or its own section on `/visit/`.
- Consider pages for "coffee beans Bali" and "coffee subscription Indonesia" only after checking demand with a keyword tool, since none was available here.

### 22. Content gaps to test (needs demand data)

- Origin and process guides (natural vs washed vs honey) to support the product pages.
- A "how to choose coffee beans" guide that links to the three coffees.
- Wholesale content: a short pricing and onboarding FAQ and case studies from named partners.
- These are ideas, not verified opportunities. Check search volumes before writing.

---

## What is already working

- Every live page has a unique, descriptive H1, a title in the right format, and (apart from `/about/`) a meta description.
- Titles and descriptions are well written and mostly the right length.
- Self-referencing canonicals are correct on all pages except those named above.
- Product images have alt text and width and height attributes, which avoids layout shift.
- Copy is specific and shows real expertise (farmer groups, process types, brew ratios, named roaster and author).
- Site structure is shallow, with clear navigation and short, readable URLs.
- Home page has Organization markup, and blog posts have Article markup with author and dates.

## Suggested order of work

1. Remove `noindex` from `/wholesale/` (5 minutes).
2. Fix the `/shop/` canonical (5 minutes).
3. Remove `/coffee/sumatra-mandheling/` from the sitemap, and change the nav link from `/menu/` to `/visit/`.
4. Merge or differentiate the two pour over posts; rename the 2024 article.
5. Unique title for `/subscriptions/`, description for `/about/`, link all coffees from `/coffee/` and `/shop/`.
6. Product markup fixes, `robots.txt` CSS rule, image fixes, H1 on the brewing guide.
7. Local business markup, Open Graph tags, custom 404, `lastmod`, internal linking.
8. After deploying, submit the sitemap and request indexing of `/wholesale/` and `/shop/` in Search Console, and use real query data to judge the content ideas in item 22.
