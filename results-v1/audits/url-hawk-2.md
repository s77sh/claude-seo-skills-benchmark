# TECHNICAL SEO AUDIT: Kopi Kita (https://kopikita.test/)

Date: 2026-10-22
Data source: Fetched with curl from the local build at http://localhost:8765/. This covers robots.txt, sitemap.xml, every page in the sitemap, the pages linked from the nav, and the key assets. URLs below use the production domain; the paths are what I fetched.
Pages analysed: 19 HTML URLs (17 in the sitemap, plus /menu/, /cafe/ and /cart/), plus 3 assets.

**Not checked.** None of these can be assessed against a local Python dev server.
- http→https and www/non-www redirects
- Response headers (X-Robots-Tag, caching, compression)
- Real page speed and Core Web Vitals
- Rendered JavaScript. The pages are static HTML with no JS.
- hreflang. The site is single-language, so it isn't needed.
- Search Console data. I can't confirm indexing, cannibalisation or which pages get clicks.

---

## CRITICAL ISSUES (fix this week)

### 1. Sitemap lists a 404: /coffee/sumatra-mandheling/
- **Affects:** https://kopikita.test/sitemap.xml, https://kopikita.test/coffee/sumatra-mandheling/ (404)
- **Why it matters:** Sitemaps should contain only indexable 200 URLs. A 404 wastes crawl budget and lowers Google's trust in the sitemap. It also suggests a product page was removed or never launched.
- **Fix:** If the Sumatra coffee is real, publish the page with a title, H1, canonical and Product schema, and link it from /coffee/ and /shop/. If not, remove it from the sitemap.

### 2. /shop/ canonicalises to /coffee/, so the Shop page can't rank
- **Affects:** https://kopikita.test/shop/ (`<link rel="canonical" href="https://kopikita.test/coffee/">`)
- **Why it matters:** The canonical tells Google that /shop/ is a duplicate of /coffee/. Google will probably drop /shop/ from the index, and the "buy coffee beans / brewing gear / drip bags" intent has no page to rank. The two pages have different titles, H1s and content, so this looks like a copy-paste error.
- **Fix:** Set the canonical on /shop/ to `https://kopikita.test/shop/`.
- **Check:** After the fix, search `site:kopikita.test/shop/` and run URL Inspection on /shop/. Confirm that the user-declared and Google-selected canonicals match.

### 3. Wholesale page is `noindex` but is in the sitemap and the main nav
- **Affects:** https://kopikita.test/wholesale/ (`<meta name="robots" content="noindex, follow">`)
- **Why it matters:** The sitemap and the nav both say "index this", while the meta tag says the opposite. The page is a B2B lead-gen page with a keyword-rich title ("Wholesale Coffee for Cafes and Hotels in Bali"), so it should be searchable. The page's own copy and the nav suggest it's meant to rank.
- **Fix:** Remove the `noindex` tag if the page should rank. That is almost certainly the intent, since it is a commercial page with a clear target query. If it is deliberately private, remove it from the sitemap instead. Check whether the tag was left over from staging.

---

## HIGH-PRIORITY ISSUES (fix this month)

### 4. Broken redirect chain on the nav link: /menu/ → /cafe/ → /visit/
- **Affects:** the "Visit the cafe" link (`/menu/`) in the header of every page, https://kopikita.test/menu/, https://kopikita.test/cafe/
- **Why it matters:** Every page links to /menu/ (about 19 internal links), which takes two 301 hops to reach the real page. Each hop costs crawl budget and some link equity, and slows users down. Meanwhile /visit/ (the canonical, sitemap URL) gets almost no internal links: only /about/ links to it directly.
- **Fix:** Change the nav href to `/visit/`. Also redirect /menu/ straight to /visit/ in a single 301, and /cafe/ straight to /visit/. Update the About page link if it points anywhere else.

### 5. /coffee/aceh-gayo/ is linked from a blog post but returns 404
- **Affects:** https://kopikita.test/blog/how-to-brew-pour-over/ (link "Aceh Gayo")
- **Why it matters:** This is a broken internal link on a content page. It sends users and crawlers to a dead end, and it points at a product that isn't on the site.
- **Fix:** Link to a live coffee such as /coffee/bali-kintamani/ or /coffee/flores-bajawa/. Or publish the Aceh Gayo page. This may be the same missing-product problem as issue 1.

### 6. Orphan page: /coffee/flores-bajawa/
- **Affects:** https://kopikita.test/coffee/flores-bajawa/
- **Why it matters:** It's in the sitemap but no page links to it. /coffee/ and /shop/ list only Kintamani and Ijen. A product page with no internal links gets no equity and is hard to discover.
- **Fix:** Add it to the /coffee/ and /shop/ listings and to the pour-over and brewing-guide posts where relevant. Add Product schema too (see issue 11).

### 7. Two blog posts compete for the same query: pour over
- **Affects:** https://kopikita.test/blog/how-to-brew-pour-over/ and https://kopikita.test/blog/pour-over-coffee-guide/
- **Why it matters:** Titles are "How to Brew Pour Over Coffee at Home" and "Pour Over Coffee Guide for Beginners". Both give the same recipe (15g to 250g of water, 93C, 40g bloom, about 3 minutes) and both use the exact phrase "pour over coffee". They are likely to split rankings, with one URL swapping in and out. I can't confirm this without Search Console data (cannibalisation check).
- **Fix, one of:**
  - (a) Merge them into one stronger guide, 301 the weaker URL to it, and keep the longer one.
  - (b) Differentiate them: make one the step-by-step recipe and the other a gear and troubleshooting guide for beginners. Cross-link them with distinct anchors, and rewrite titles and H1s so they don't share the head term.
  - Either way, confirm with GSC (queries where both URLs get impressions) before choosing.

### 8. Missing H1 / duplicate H1s
- **/visit/** (https://kopikita.test/visit/) has no `<h1>`, only two `<h2>`s ("Opening hours", "Menu"). Add an H1 such as "Visit our roastery cafe in Ubud".
- **/coffee/brewing-guide/** has two `<h1>` elements ("Coffee brewing guide" and "Brew methods"). Change the second to an `<h2>`.
- **Why it matters:** The H1 is a main on-page signal for what a page is about, and a page with no H1 or a split one is weaker for its target query. /visit/ is the local-intent page (opening hours, directions).

### 9. /about/ has no meta description
- **Affects:** https://kopikita.test/about/
- **Why it matters:** Google writes its own snippet, which usually performs worse for a page that has to build trust. It is the only page missing one, which also makes it a quick win.
- **Fix:** Add a description of 120–155 characters, for example: "Kopi Kita started in 2019 in a garage in Ubud. Meet our roaster Wayan Sudarma and the farmer groups we buy from in Bali, Java and Flores."

### 10. Missing canonical on /contact/
- **Affects:** https://kopikita.test/contact/
- **Why it matters:** Every other page has a self-referencing canonical. Without one, tracking-parameter or alternate URLs can create duplicates.
- **Fix:** Add `<link rel="canonical" href="https://kopikita.test/contact/">`.

---

## MEDIUM-PRIORITY ISSUES (roadmap)

### 11. Structured data problems
These came from reading the JSON-LD on each page. I didn't run Google's Rich Results Test, so validate after fixing.
- **/coffee/bali-kintamani/** (Product): has no `name`. Google requires `name` for Product rich results, so the page is currently not eligible. Add `"name": "Bali Kintamani natural coffee, 250g"`. The price (145000) matches the page text.
- **/coffee/java-ijen/** (Product): valid on the basics (name, image, offers).
- **/coffee/flores-bajawa/**: has no Product schema, unlike the other two coffees. Add it. The page lists Rp 155,000 for 250g.
- **Both Product blocks:** `offers` has no `url`. Also consider `sku` and `aggregateRating`/`review` if you have real reviews. Don't add ratings you don't have.
- **Blog Articles:** no `image` and no `publisher`. Add a primary image and the Organization as publisher. The `headline` values differ slightly from the H1s ("The best coffee beans in Bali" vs "... (2024 guide)"); make them match.
- **/coffee/ FAQPage:** Google has restricted FAQ rich results to well-known government and health sites, so this will not produce a rich result for a coffee shop. It's harmless, but the two questions also aren't visible on the page. Markup should match visible content, so either add the Q&A to the page or remove the block.
- **Homepage Organization:** add `sameAs` (Instagram and so on) and `contactPoint`. Consider a `CafeOrCoffeeShop` / `LocalBusiness` block with opening hours (7am–5pm daily), phone and geo on /visit/ or /contact/. This is the biggest schema opportunity for local search in Ubud.
- **Logo:** `https://kopikita.test/assets/img/logo.png` returns 200 (checked). Confirm it is at least 112×112 px.

### 12. Stale year in a URL and title
- **Affects:** https://kopikita.test/blog/best-coffee-beans-2024/ (title "Best Coffee Beans in Bali (2024 Guide)", H1 "(2024 guide)")
- **Why it matters:** The content was updated on 2026-09-01 per its schema (`dateModified`), but the URL, title and H1 all say 2024. That looks outdated in search results and lowers click-through. The URL can't change without a redirect.
- **Fix:** Retitle it "Best Coffee Beans in Bali (2026 Guide)". Better: move to an evergreen URL such as /blog/best-coffee-beans-bali/, 301 the old URL, and update the internal links and sitemap.

### 13. Thin content: /blog/cold-brew-at-home/
- **Affects:** https://kopikita.test/blog/cold-brew-at-home/
- **Why it matters:** The body is a single paragraph (about 80 words), compared with 400+ words for the other posts. It's thinner than anything else under /blog/, and the brewing guide already covers the same recipe (100g to 1 litre, 16 hours).
- **Fix:** Expand it with grind size, steeping time and ratio variations, dilution, storage, and which beans to use. Or fold it into the brewing guide and 301 it. Treat the word count as a flag to review, not a rule.

### 14. Oversized image on /about/
- **Affects:** https://kopikita.test/assets/img/roastery-hero.jpg (1.8 MB, 2400×1600)
- **Why it matters:** A 1.8 MB image on a small page hurts LCP, especially on mobile. The container is about 46rem wide, so the display size is far smaller than the file.
- **Fix:** Resize to about 1200px wide, serve as WebP/AVIF, and add `srcset`. The image does have width/height and alt text, which is good.

### 15. Homepage hero image has no `alt` text
- **Affects:** https://kopikita.test/ (`/assets/img/hero-beans.jpg`)
- **Fix:** Add a descriptive alt, e.g. "Freshly roasted Indonesian coffee beans". This also helps accessibility and image search. If the image is the LCP element, don't lazy-load it.

### 16. robots.txt blocks the CSS directory
- **Affects:** https://kopikita.test/robots.txt (`Disallow: /assets/css/`)
- **Why it matters:** Google needs to fetch CSS to render pages and judge mobile-friendliness. Blocking it can lead to a wrong render. The site is small and the CSS is trivial, so impact is low, but there is no benefit to blocking it.
- **Fix:** Remove that line. `Disallow: /cart/` is fine (the path currently returns 404, which is harmless). The `Sitemap:` line is correct.

### 17. Sitemap hygiene
- No `<lastmod>` values. Add accurate ones, especially for blog posts that were updated.
- Fix the 404 entry (issue 1) and the noindex page (issue 3).
- After the fixes, resubmit it in Search Console.

### 18. Titles and meta descriptions
- **Overlong titles** that will likely truncate in the SERP:
  - /coffee/bali-kintamani/: "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita" is 87 characters. Suggest "Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita".
- **/about/** title ("About Kopi Kita: Our Roastery Story") is fine.
- **Duplicate title: /subscriptions/ and /coffee/** both use "Single-Origin Indonesian Coffee | Kopi Kita". The /subscriptions/ page is about subscriptions (H1 "Coffee subscriptions", description "Fresh single-origin coffee delivered every two or four weeks"), so the title was probably copied from /coffee/. Two pages with one title compete for the same query and confuse the SERP. Retitle /subscriptions/ as, for example, "Coffee Subscription in Bali: Fresh Beans Every 2–4 Weeks | Kopi Kita". Keep the /coffee/ title. This is a High-priority fix, because it affects a revenue page.
- Apart from that pair, titles and meta descriptions are unique across the pages I fetched (the only missing description is /about/, issue 9).
- Note that the /coffee/ title, "Single-Origin Indonesian Coffee | Kopi Kita", is a good match for the page. Don't change it.

### 19. Content and internal-link depth
- **Product-to-blog links are thin.** The blog posts link to products, but /shop/ and /coffee/ link out only to the brewing guide and two coffees. Cross-link the guides to the right products.
- **Home page links** to /coffee/, /blog/, /wholesale/, the brewing guide and two coffees. Add /visit/ and /subscriptions/ as in-content links.
- **/subscriptions/** is reachable only from the nav, so one nav link per page. Link to it from product pages ("subscribe and save").

---

## TOP 5 QUICK WINS
1. **Fix the /shop/ canonical** to self-reference. One-line change. Impact: High.
2. **Remove `noindex` from /wholesale/** (or take it out of the sitemap, whichever matches intent). One-line change. Impact: High.
3. **Change the nav link from /menu/ to /visit/** and flatten the redirects. A site-wide template fix. Impact: Medium–High.
4. **Fix the two 404s** (/coffee/sumatra-mandheling/ in the sitemap, /coffee/aceh-gayo/ linked from the blog). Impact: Medium.
5. **Add the missing /visit/ H1, /about/ meta description, /contact/ canonical and the Kintamani Product `name`.** A handful of one-line edits. Impact: Medium.

---

## WHAT'S WORKING (don't change)
- **Status codes:** Every page in the sitemap returns 200, except the one 404 above.
- **Canonicals:** Present and self-referencing on all pages apart from /shop/ and /contact/.
- **Titles and descriptions:** Keyword-led and mostly within length, and unique apart from the /subscriptions/ vs /coffee/ title clash (issue 18).
- **robots.txt:** Valid, doesn't block any content pages, and declares the sitemap.
- **Page structure:** Clean semantic HTML, correct `lang`, viewport tag, one H1 on most pages, descriptive alt text on product and About images, and width/height set on images (low CLS).
- **Weight and rendering:** Static pages with a 100-byte stylesheet and no JavaScript, so there are no rendering risks.
- **Schema:** Organization (home), Product (two coffees) and Article (three posts) are present and mostly well-formed.
- **Internal links:** Descriptive anchors, with the main money pages reachable in one click from the nav.
- **Content:** The product pages, brewing guide and pour-over articles are substantive. The first-hand detail (farm groups, altitude, harvest dates) is good for E-E-A-T.

---

## BOTTOM LINE
The biggest problem is that the site is telling Google conflicting things about its own commercial pages: /shop/ is canonicalised away to /coffee/, /wholesale/ is noindexed while sitemapped, and the nav sends everyone through a double redirect. Fixing those three tags and links, plus the two 404s, should get the money pages indexed correctly, and none of it needs a redesign.
