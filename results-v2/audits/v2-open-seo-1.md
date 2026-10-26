# Kopi Kita SEO audit

Site: http://localhost:8766/ (production domain https://kopikita.test/)
Audited: 2026-10-22, by fetching every URL in the sitemap, the nav links and the robots.txt with curl.

## Scope and limits

- The OpenSEO MCP tools (site crawler, rankings, search volumes, backlinks, Search Console) were not connected in this session. This audit is technical and on-page only.
- There are no ranking, search volume or traffic figures here. Where an item says "likely", that is inference from the HTML, not measured loss.
- 22 pages were read (21 sitemap URLs plus /coffee/limited-release/) along with robots.txt. The site is small enough that this is close to the full site.
- Glossary: **canonical** is the tag that tells Google which URL is the preferred version of a page. **301** is a permanent redirect, **302** a temporary one. **Soft 404** is a "not found" page that returns a 200 "OK" status. **hreflang** tags tell Google which language version to show which searcher.

## Summary

The content is good: specific, honest, with clear titles on most pages. The problems are almost all in the plumbing. Four patterns cost the most:

1. Product and category pages send Google conflicting signals (wrong canonicals, redirected internal links, duplicated descriptions).
2. Sitemap, robots.txt and internal links disagree with each other.
3. A sitewide nav link goes to a soft 404.
4. The two pages with the clearest commercial or local intent (the Bali beans guide and the cafe page) are thinly supported.

Everything in "Priority 1" can be fixed in an afternoon by a developer.

---

## Priority 1: fix first (hurts indexing or rankings now)

### 1. The /coffee/ category page canonicalises to /shop/

- **URL:** https://kopikita.test/coffee/
- **Found:** `<link rel="canonical" href="https://kopikita.test/shop/">`. The /coffee/ page is a different page (origin descriptions, brewing guide, gift box), but it tells Google to treat /shop/ as the real one.
- **Why it matters:** Google will likely drop /coffee/ from the index and fold it into /shop/. /coffee/ is the best target for queries like "single origin Indonesian coffee" and is the hub that links to every product. It is also listed in the sitemap, which contradicts the canonical.
- **Fix:** Set the canonical on /coffee/ to itself (`https://kopikita.test/coffee/`). Then give /shop/ and /coffee/ distinct jobs: /coffee/ for beans by origin, /shop/ for everything (beans, gear, drip bags). Their titles are now similar ("Single-Origin Indonesian Coffee" vs "Shop Coffee Beans and Brewing Gear") and should stay clearly different.

### 2. Java Ijen product page canonicalises to a URL that redirects back to it

- **URL:** https://kopikita.test/coffee/java-ijen/
- **Found:** Canonical is `https://kopikita.test/coffee/ijen/`. That URL returns a 301 to `/coffee/java-ijen/`. The page, the sitemap and all internal links use `/java-ijen/`.
- **Why it matters:** A canonical that points at a redirect which points back is a loop. Google may ignore the hint or pick the wrong URL, and one of the site's two main products is affected.
- **Fix:** Change the canonical to `https://kopikita.test/coffee/java-ijen/`. Check the template that generates canonicals, since this looks like a leftover from an old URL.

### 3. "Gifts" link in the sitewide nav is a soft 404

- **URL:** https://kopikita.test/gifts/ (linked from the nav on every page)
- **Found:** Returns HTTP 200 with the title "Page not found" and a not-found message. A real missing page (for example /nonexistent/) returns a proper 404, so only this URL is wrong.
- **Why it matters:** Google treats soft 404s as errors, wastes crawl budget on them, and a dead link in the top navigation on all ~22 pages hurts users and passes link value to nothing. It also hides that there is a real gift page at /coffee/gift-box/.
- **Fix:** Either point the nav link to https://kopikita.test/coffee/gift-box/ or build a real /gifts/ page (gift box, gift subscriptions, which already exist on /subscriptions/). If the page is removed, make it return a real 404 or 301 to the gift box.

### 4. Internal links go through a temporary (302) redirect

- **URLs:** https://kopikita.test/ (home page), /blog/cold-brew-at-home/, /blog/best-coffee-beans-bali/ all link to https://kopikita.test/coffee/kintamani/
- **Found:** That URL returns a 302 (temporary) redirect to /coffee/bali-kintamani/. Your best seller is reached through it from the home page and the two blog posts.
- **Why it matters:** A 302 tells Google the old URL may come back, so it can keep the redirecting URL in play and not fully pass link value. Redirected internal links also add a pointless hop.
- **Fix:** Update the three links to `/coffee/bali-kintamani/`. Change the redirect to a 301 if the old URL needs to keep working for outside links. The same applies to `/coffee/ijen/`, which is a 301 (good) but is only used by the bad canonical above.

### 5. Sitemap includes a URL that robots.txt blocks, plus a page that canonicalises elsewhere

- **URLs:** https://kopikita.test/sitemap.xml, /coffee/samples/, /blog/page/2/
- **Found:**
  - `/coffee/samples/` is in the sitemap but `robots.txt` says `Disallow: /coffee/samples/`.
  - `/blog/page/2/` is in the sitemap but its canonical points at `/blog/`.
- **Why it matters:** A sitemap should list only pages you want indexed. Mixed signals make Search Console report errors and weaken trust in the file.
- **Fix:** Remove both from the sitemap. For the samples page, decide what you want: if it should rank for "wholesale coffee sample Bali", remove the robots block and link it (see item 12); if it should stay private, keep the robots block and remove it from the sitemap.

### 6. Sitemap dates are in the future

- **URL:** https://kopikita.test/sitemap.xml
- **Found:** Every `<lastmod>` is `2027-03-01`, which is after today's date (2026-10-22), and the same on every page.
- **Why it matters:** Google ignores `lastmod` values it can't trust. Identical dates on all pages teach it that the field is unreliable, so real updates won't be picked up faster.
- **Fix:** Generate `lastmod` from the real last-edit date of each page, or leave it out.

---

## Priority 2: fix this month (duplicate or weak signals)

### 7. Duplicate meta descriptions on product pages

- **URLs:**
  - https://kopikita.test/coffee/flores-bajawa/ uses the Java Ijen description ("Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon and black tea…"), which is wrong for a honey-process Flores coffee.
  - https://kopikita.test/coffee/bali-kintamani/ and /coffee/bali-kintamani-1kg/ have identical descriptions.
- **Why it matters:** Google will usually rewrite a misleading description, and a wrong one shown in results hurts click-through. Identical descriptions on near-duplicate pages add to the confusion.
- **Fix:** Write a unique description for each, for example for Flores: "Honey-process coffee from Bajawa, Flores. Dark chocolate, red apple and clove, roasted to order in Ubud."

### 8. The 250g and 1kg Kintamani pages are near duplicates

- **URLs:** https://kopikita.test/coffee/bali-kintamani/ and https://kopikita.test/coffee/bali-kintamani-1kg/
- **Found:** Same image, same description, near-identical copy, each with a self-referencing canonical. They only differ by bag size and price. Both are in the sitemap. The 1kg page is reachable only from one link on the 250g page.
- **Why it matters:** Two pages compete for the same query ("bali kintamani coffee beans"), and Google may show the less useful one.
- **Fix:** Preferably one product page with a size selector and two Offers in the Product schema, and a 301 from the 1kg URL. If you keep both, canonical the 1kg page to the main one. Note also that Flores and Ijen are sold in both sizes ("Rp 560,000 for 1kg" appears on the Flores page) without separate pages, so the single-page approach is consistent.

### 9. Indonesian page hreflang is wrong and incomplete

- **URLs:** https://kopikita.test/id/ and https://kopikita.test/
- **Found:**
  - /id/ declares `hreflang="in"`. The code for Indonesian is `id`; `in` is an obsolete code that Google does not support.
  - The English home page has no hreflang tags, so the pair isn't reciprocal. Google needs each page to point at the other.
  - /id/ is only reachable from one text link on the home page, and the nav and all other pages are English only.
  - There is no `x-default`.
- **Why it matters:** Without a valid, two-way pair Google may ignore the annotations and show Indonesian searchers the English page, or the other way round. Indonesian is a large market and the site ships across Indonesia.
- **Fix:** On both pages add:
  `<link rel="alternate" hreflang="en" href="https://kopikita.test/">`
  `<link rel="alternate" hreflang="id" href="https://kopikita.test/id/">`
  `<link rel="alternate" hreflang="x-default" href="https://kopikita.test/">`
  Also fix `<html lang="en">` on /id/ to `lang="id"` (it is wrong now), and consider translating the nav, which is still in English there.

### 10. Invalid structured data on the pour-over article

- **URL:** https://kopikita.test/blog/how-to-brew-pour-over/
- **Found:** The Article JSON-LD ends with a trailing comma (`"author": {...},}`). That is invalid JSON, so the whole block is discarded.
- **Why it matters:** No article rich result or author signal from that page. It is the site's main how-to page and one of the likeliest to earn search traffic.
- **Fix:** Remove the comma. Test in Google's Rich Results Test. While there, add `image` and `publisher` to the Article schema here and on /blog/best-coffee-beans-bali/, which also lacks them.

### 11. Missing structured data on some product pages and the cafe page

- **URLs:** /coffee/flores-bajawa/ and /coffee/gift-box/ (no Product schema), /visit/ and the home page (no local business markup)
- **Found:** Kintamani and Ijen pages have Product schema with price and availability; Flores and the gift box do not. The home page has a generic `Organization` with an address but no phone, hours, geo coordinates or `sameAs` links. The /visit/ page, which has opening hours and a Saturday cupping, has no schema at all.
- **Why it matters:** Product markup can show price and stock in results. Local business markup helps with "coffee shop Ubud" and "roastery Ubud" searches and with Google Maps consistency.
- **Fix:** Add Product schema (with `offers`, and `aggregateRating` only if real reviews exist) to the missing pages. Use `CafeOrCoffeeShop` on /visit/ with address, `openingHoursSpecification` (7am to 5pm daily), phone and map coordinates. Make sure the Google Business Profile matches.

### 12. Wholesale pages are cut off from search and from each other

- **URLs:** https://kopikita.test/wholesale/ and https://kopikita.test/coffee/samples/
- **Found:**
  - Every nav link to /wholesale/ has `rel="nofollow"`. This is an internal link and the page is meant to rank ("wholesale coffee for cafes and hotels in Bali"), and the page is in the sitemap.
  - The wholesale page asks readers to "ask for a free sample box" but links to /contact/, not to the real sample page. The sample page, /coffee/samples/, has no inbound internal links at all (an orphan) and is blocked by robots.txt.
- **Why it matters:** Nofollow on internal links withholds link value from a revenue page. Wholesale is likely the highest-value customer type (30+ partners, weekly orders), and its funnel is broken at the sample step.
- **Fix:** Remove `rel="nofollow"` from the nav. Decide on the samples page (see item 5). If it should be public, unblock it, link to it from /wholesale/ and add it to the nav or footer. If it is not meant to be public, remove it from the sitemap and leave the robots rule. Add more detail to /wholesale/: minimum order, price tiers, delivery area list, a short enquiry form, and a couple of partner names or quotes.

### 13. A real page is reachable only through JavaScript

- **URL:** https://kopikita.test/coffee/limited-release/
- **Found:** The page exists (200, own canonical) but the only link to it is a `<button onclick="location.href=...">` on /coffee/. It is also missing from the sitemap.
- **Why it matters:** Crawlers don't reliably follow `onclick` handlers, so the page is likely undiscovered and cannot rank or get link value.
- **Fix:** Use a real `<a href="/coffee/limited-release/">` link and add the page to the sitemap. Because it is a limited run, plan what happens when it sells out (keep the page, mark it out of stock, link to the next release).

### 14. Flores Bajawa product is not linked from the category page

- **URLs:** https://kopikita.test/coffee/ and https://kopikita.test/coffee/flores-bajawa/
- **Found:** /coffee/ lists Kintamani and Ijen but not Flores. /shop/ also lists only two coffees. The Flores page is linked only from the pour-over article. It is in the sitemap.
- **Why it matters:** Pages that only one blog post links to get little link value and may be crawled rarely. It is also one of three origins the home page promotes.
- **Fix:** Add Flores to /coffee/ and /shop/, and to the home page copy.

### 15. Gift box and 1kg pages are thinly linked

- **URLs:** /coffee/gift-box/, /coffee/bali-kintamani-1kg/
- **Found:** Each has a single inbound link (from /coffee/ and from the 250g page respectively), and they appear in no nav, footer or blog link. There is no /gifts/ page (see item 3).
- **Fix:** Link the gift box from the nav (once fixed), the home page and relevant blog posts.

---

## Priority 3: content and opportunity

### 16. "Best coffee beans in Bali" guide could convert better and is not fully supported

- **URL:** https://kopikita.test/blog/best-coffee-beans-bali/
- **Found:**
  - A good, honest guide, and a sound target for a high-intent query. But its only brand link goes to the redirecting /coffee/kintamani/ (see item 4), and it does not link to the shop, to the Ijen or Flores coffees, or to the brewing guide.
  - It recommends "a washed Kintamani from any good local roaster" for lighter coffee, which sends buyers to a competitor and is not what you sell.
  - It has no images, no author byline on the page and no sources, even though the schema names Wayan Sudarma. The Article schema also has no image.
  - No FAQ or comparison table, and only about 350 words.
- **Why it matters:** This is the page most likely to bring in new customers from search, and it currently leaks them.
- **Fix:** Link to products with descriptive anchors, add photos of the beans and farms, show the author and roast date practices, and expand with a short comparison of the Kopi Kita origins (naturals, washed, honey). Without ranking data I cannot say where the page sits now; check Search Console before rewriting if it already ranks well, and protect what works.

### 17. Only two thin blog posts besides the guide, no topical depth

- **URLs:** /blog/, /blog/how-to-brew-pour-over/, /blog/cold-brew-at-home/, /coffee/brewing-guide/
- **Found:** The brewing guide and blog recipes cover broad queries that big sites dominate. The blog index paginates to a second page that holds only one older post (cold brew).
- **Fix:** Rather than more generic recipes, use what only you know: Kintamani processing, farmer group profiles, the Saturday cupping, "how to brew Kopi Kita Kintamani natural". Link every post to the matching product. Fold page 2 into page 1 until there are enough posts to paginate.

### 18. The Indonesian site is one thin page

- **URL:** https://kopikita.test/id/
- **Found:** A short translated home page; no Indonesian product, shop or blog pages. Shipping across Indonesia is a core promise.
- **Fix:** If Indonesian searchers matter, translate the coffee, subscription and wholesale pages first. Otherwise do the hreflang fix (item 9) and leave it.

### 19. Subscriptions and visit pages are short

- **URLs:** https://kopikita.test/subscriptions/, https://kopikita.test/visit/
- **Found:** Subscriptions has no price table, FAQ or call to action beyond "contact us"; the only conversion path is the contact page. /visit/ has hours and menu but no phone number, map, address on the page, photos or reviews.
- **Fix:** Add a clear order or sign-up link, a short FAQ (shipping times, pausing) and, on /visit/, an embedded map, address, photos and a link to the Google Business Profile.

---

## Priority 4: technical hygiene

### 20. Hero image on the home page is lazy-loaded

- **URL:** https://kopikita.test/ (`<img src="/assets/img/hero-beans.jpg" … loading="lazy">`)
- **Why it matters:** This is the largest above-the-fold image, so it likely slows Largest Contentful Paint (the Core Web Vitals metric for load speed).
- **Fix:** Remove `loading="lazy"` from it, add `fetchpriority="high"`, and keep lazy loading only for images further down.

### 21. About page gallery images only load with JavaScript

- **URL:** https://kopikita.test/about/
- **Found:** The three farm photos use `data-src` and an IntersectionObserver script, with no `src` in the HTML.
- **Fix:** Use `<img src=… loading="lazy">`. Google may not see these images otherwise, and they have good alt text that is worth indexing.

### 22. Image on the contact page uses http://

- **URL:** https://kopikita.test/contact/ (`http://kopikita.test/assets/img/storefront.jpg`)
- **Fix:** Use a relative or https URL to avoid mixed-content warnings once the site is on https.

### 23. Missing favicon

- **URL:** https://kopikita.test/favicon.ico returns 404.
- **Fix:** Add a favicon and a `<link rel="icon">`. Google shows it in mobile results.

### 24. robots.txt blocks /cart/ which does not exist

- **URL:** https://kopikita.test/robots.txt
- **Found:** `Disallow: /cart/` and `Disallow: /blog/tag/` target URLs that return 404 here. That is harmless but worth checking against the real production site. Blocked pages can still be indexed if linked, so use `noindex` for anything that must stay out of search.
- **Fix:** Keep as is if these exist in production; otherwise tidy.

### 25. Missing breadcrumbs, and default 404 page style

- **Found:** No breadcrumb markup on product or blog pages. The server's own 404 page is a bare "Error response" page without site navigation.
- **Fix:** Add `BreadcrumbList` schema (Home > Coffee > Product). Serve the branded "Page not found" content (currently used at /gifts/) with a real 404 status for unknown URLs.

---

## What is already working

- Every page has a unique, descriptive title under about 60 characters and a single h1.
- Meta descriptions exist on every page (apart from the duplicates above).
- Clean, readable URLs, a sitemap and a robots.txt that points to it.
- Product images have descriptive alt text and width and height set, which avoids layout shift.
- Real, specific content: prices, altitudes, processes, roast schedule, named farmer groups and a named author. This supports Google's experience and trust signals.
- Product schema with price and availability on the two main coffees.
- Unknown URLs return a true 404.

## Suggested order of work

1. Items 1, 2, 3, 4 (canonicals, nav link, redirected links): under two hours.
2. Items 5, 6, 12, 13 (sitemap, robots, nofollow, JS link): about an hour.
3. Items 7 to 11 (descriptions, duplicates, hreflang, schema): half a day.
4. Items 14 to 19 (linking and content): ongoing.
5. Items 20 to 25: when convenient.

Once the fixes are live, submit the sitemap in Google Search Console and check the Pages report for "Duplicate, Google chose different canonical" and "Soft 404" to confirm they clear. Connect Search Console and a rank tracker so the content priorities (16 to 19) can be ordered by real impressions instead of by judgement.
