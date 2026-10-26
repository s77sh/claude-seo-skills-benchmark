# SEO Audit: Kopi Kita (kopikita.test)

Audit date: 22 October 2026. GSC window: 22 July to 21 October 2026.

**Evidence used:** raw HTML of all 17 pages in `evidence/site/`, `robots.txt`, `sitemap.xml`, `crawl.csv` (27 URLs), `gsc.csv` (27 query/page rows), and live header checks against http://localhost:8765/.

**Not available, so not assessed:** real Core Web Vitals data, backlinks, HTTPS and security headers on production (the local server is Python's SimpleHTTP), and Google Business Profile. Where a finding is an inference rather than something shown in the evidence, I say so.

**Caveat on GSC data:** the export is 27 rows. Totals below are for those rows only, not the whole property.

---

## Summary

Business type: local specialty coffee roaster plus cafe, with an online shop, subscriptions and wholesale (small local business with e-commerce).

**Estimated health score: 61/100.** This is a judgement score using the skill's category weights, not a tool-measured number.

| Category | Weight | Score | Main drag |
|---|---|---|---|
| Technical SEO | 22% | 55 | CSS blocked, 404 in sitemap, redirect chain, wrong canonical, noindex page in sitemap |
| Content quality | 23% | 62 | Two competing pour-over posts, thin cold-brew and Flores pages, stale "2024" guide |
| On-page SEO | 20% | 60 | Duplicate title, missing description, H1 problems, over-long title |
| Schema | 10% | 50 | Product missing `name`, FAQ markup for hidden content, no local business markup |
| Performance | 10% | 70 | 1.8 MB image (lab estimate only, no field data) |
| AI search readiness | 10% | 65 | Clear facts and recipes, but weak entity and author markup |
| Images | 5% | 65 | Missing alt, one oversized image |

**What the data says about demand.** In these rows, branded queries ("kopi kita ...") produce 574 of 832 clicks (69%) but only 7% of impressions. The 8,830 pour-over impressions, 34% of all impressions, produce 36 clicks. Non-branded growth is stuck at positions 7 to 45, and most of the causes below are fixable on-site.

**Top 5 issues**
1. Two pour-over articles split the same queries, so neither gets past position 14 (P1-1).
2. `/coffee/sumatra-mandheling/` is a 404 in the sitemap and `/coffee/aceh-gayo/` is a 404 linked from a blog post (P1-2).
3. `/assets/css/site.css` is blocked in robots.txt, so Google can't render pages as users see them (P1-3).
4. `/shop/` canonicalises to `/coffee/`, but it is a distinct page that sits in the main nav and the sitemap (P1-4).
5. `/wholesale/` is `noindex` but listed in the sitemap, with no sign that this is deliberate (P1-5).

**Top 5 quick wins**
1. Change the nav link `/menu/` to `/visit/`. One template edit removes a 2-hop redirect chain from every page.
2. Remove the 404 from the sitemap and fix the Aceh Gayo link.
3. Remove `Disallow: /assets/css/` from robots.txt.
4. Write a unique title for `/subscriptions/` and a description for `/about/`.
5. Add `name` to the Kintamani Product schema and alt text to the hero image.

---

## Priority 1: Critical / High (fix this week)

### P1-1. Keyword cannibalisation: two pour-over articles
- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Evidence (gsc.csv):** both pages rank for the same four queries and swap positions between them.

| Query | Impressions (page A + page B) | Positions |
|---|---|---|
| pour over coffee | 2,410 + 1,980 | 16.2 / 18.7 |
| how to make pour over coffee | 1,350 + 1,120 | 14.1 / 17.3 |
| pour over coffee guide | 610 + 820 | 19.4 / 13.9 |
| pour over ratio | 540 | 21.0 |

  Together these are 8,830 impressions and 36 clicks, a CTR of about 0.4%. Both pages are about 370 to 440 words and give the same recipe (15g, 250g, 93C, bloom 40g). Neither links to the other.
- **Why it matters:** Google can't pick one page to rank, so link signals and click data are split. Page 1 is realistic for the head term "pour over coffee" if the pages become one stronger page.
- **Fix:** merge them into one definitive guide at `/blog/how-to-brew-pour-over/`, which has the better position on most queries and the longer text. Fold in the unique parts of the beginner guide (gear, dripper choice, common mistakes). 301 `/blog/pour-over-coffee-guide/` to it, update the blog index, and then re-point internal links. The alternative is to keep both but split the intent: a beginner "what you need" page and a recipe page, cross-linked, with different titles and H1s. Merging is simpler and better here.

### P1-2. 404 pages in the sitemap and in internal links
- **URLs:** `/coffee/sumatra-mandheling/` (404, in sitemap.xml) and `/coffee/aceh-gayo/` (404, linked from `/blog/how-to-brew-pour-over/`).
- **Why it matters:** a 404 in the sitemap tells Google you want it indexed and wastes crawl budget. A dead link in the pour-over article, your most-impressed page, is a poor user experience and a dead end for link equity. Both look like products that were planned or discontinued.
- **Fix:** if the coffees exist, publish the pages (with Product schema and links from `/coffee/`). If not, remove the sitemap entry and change the blog sentence to link to a live coffee, such as Bali Kintamani for the "heavier" option. Generate the sitemap from live 200 pages only.

### P1-3. robots.txt blocks the stylesheet
- **URL:** `/robots.txt`, line `Disallow: /assets/css/`. The crawl shows `/assets/css/site.css` as "Blocked by robots.txt" with 17 inlinks.
- **Why it matters:** Google renders pages for mobile-first indexing and needs CSS to do so. Blocking it can lead to wrong layout and mobile-usability assessments, and the Search Console URL Inspection tool will report resources it couldn't load.
- **Fix:** delete the line. `Disallow: /cart/` points at a path that doesn't exist in the crawl. Keep it only if a cart is planned, and plan to `noindex` or disallow checkout paths when it exists. Keep the `Sitemap:` line.

### P1-4. `/shop/` is canonicalised to `/coffee/` but is a different page
- **URL:** `/shop/`. Its canonical is `https://kopikita.test/coffee/`. It is also in `sitemap.xml` and linked from the main nav on all 16 other pages.
- **Why it matters:** the shop page covers gear, drip bags and shipping thresholds that `/coffee/` doesn't. Google will usually honour the canonical, so `/shop/` is excluded from the index and can never rank for gear or "buy ... Bali" queries. Sitemaps should only list canonical URLs. The title is also different from `/coffee/`, which signals this wasn't meant as a duplicate.
- **Fix:** decide what `/shop/` is. If it's the store front, make it self-canonical and have it link to every product. If it's genuinely just an alias of `/coffee/`, 301 it to `/coffee/`, remove it from the sitemap and nav, and don't keep both. I'd choose the first: the content is distinct.

### P1-5. `/wholesale/` is `noindex` yet in the sitemap and main nav
- **URL:** `/wholesale/`. Meta robots is `noindex, follow`, and the page is listed in `sitemap.xml`.
- **Why it matters:** it is a conversion page with real selling points (30+ venues, barista training, next-day delivery) and queries like "wholesale coffee Bali" would be the target. As it stands it cannot rank. The conflicting signals (sitemap says index, page says no) are also a sign of a deploy mistake. The evidence can't show whether this is intentional, for example a staging leftover, so confirm with the team.
- **Fix:** if it's not intentional, remove the `noindex`. If it is, remove the URL from the sitemap.

### P1-6. Redirect chain from the main nav: `/menu/` → `/cafe/` → `/visit/`
- **URLs:** `/menu/` (17 inlinks, i.e. the whole nav), `/cafe/` (1 inlink), final destination `/visit/`. Confirmed live with curl: two 301s in a row.
- **Why it matters:** every internal click to the cafe page takes two hops. `/visit/` gets only 2 inlinks from real links, yet it is the page earning the second-most clicks (96 for "kopi kita ubud"). Redirects also dilute the signal a little and slow crawling.
- **Fix:** change the nav `href` from `/menu/` to `/visit/`. Keep one 301 each from `/menu/` and `/cafe/` straight to `/visit/` for outside links, with no chain. Link to `/visit/` from the footer and home page as well.

### P1-7. Duplicate title on `/subscriptions/` and `/coffee/`
- **URLs:** `/subscriptions/` and `/coffee/` both use "Single-Origin Indonesian Coffee | Kopi Kita".
- **Why it matters:** the subscriptions page presumably inherited the wrong title. It ranks for "coffee subscription bali" at position 5.9 (310 impressions, 2.9% CTR), and a title that doesn't mention subscriptions weakens relevance and CTR. It also makes the two pages look like duplicates in the SERPs.
- **Fix:** for example "Coffee Subscription in Bali: Fresh Beans Every 2 or 4 Weeks | Kopi Kita". Keep the `/coffee/` title as it is.

### P1-8. The "2024" guide is aging, and the year is in the URL, title and H1
- **URL:** `/blog/best-coffee-beans-2024/`
- **Evidence:** it ranks for "best coffee beans bali" (position 7.8, 960 impressions, 2.3% CTR) and "bali coffee beans" (position 11.4, 1,890 impressions, 0.7% CTR). Its schema says `dateModified` is 2026-09-01, but the visible title, H1 and URL say 2024, and the copy says "our picks this year".
- **Why it matters:** a title with a year two years in the past reads as outdated in the SERP and suppresses clicks. The schema's headline ("The best coffee beans in Bali") also doesn't match the H1.
- **Fix:** retitle to an evergreen "Best Coffee Beans in Bali: How to Choose + Our Picks" or use the current year. Moving the URL to `/blog/best-coffee-beans-bali/` with a 301 is the best fix. Updating the title and H1 without the URL change is the minimum. Show a visible "Updated" date that matches `dateModified`. The article also only names one pick of its own and "any good local roaster" for the other, so add two or three real picks with reasons.

---

## Priority 2: Medium (fix within a month)

### P2-1. Page-type mismatch for commercial queries
- **Evidence:** "bali coffee beans" (1,890 impressions) is served by a blog post at position 11.4, while "buy coffee beans bali" is served by `/coffee/` at position 10.2 and "single origin indonesian coffee" at 9.3.
- **Why it matters:** for buying queries Google prefers a category or product page. The category page, `/coffee/`, is thin (102 words) and lists only two of the three coffees.
- **Fix:** build `/coffee/` into a proper category page: one card for each coffee (origin, process, notes, price, image), a short buying guide, and a link to the blog guide. Link the blog guide to `/coffee/` with the anchor "Bali coffee beans".

### P2-2. `/coffee/flores-bajawa/` is an orphan with no links
- **URL:** `/coffee/flores-bajawa/`: 0 inlinks, 75 words, no Product schema, only in the sitemap. `/coffee/` and `/shop/` both skip it, though the home page meta description advertises Flores.
- **Why it matters:** with no internal links it gets no authority and visitors can't find the coffee. 
- **Fix:** list it on `/coffee/`, `/shop/` and the home page, and add Product schema (see P2-5). Expand the page with a producer story, how to brew it, and the 250g and 1kg prices as separate offers.

### P2-3. Thin content: cold brew article and home page
- **URL:** `/blog/cold-brew-at-home/` has 67 words (one paragraph). It ranks at positions 38 and 45 for "cold brew coffee at home" and "how to make cold brew coffee" (1,510 impressions, 1 click).
- **Why it matters:** it is far too short to compete, and `/coffee/brewing-guide/` already has a cold brew line. The home page (132 words) is also light, though it ranks fine for brand.
- **Fix:** turn the cold brew post into a full guide of at least 400 words (ratios for concentrate and ready-to-drink, grind, steeping time, filtering, storage, serving, troubleshooting), with a step list and a link to the brewing guide and a recommended coffee. Link it from the brewing guide and from the nav of the blog.

### P2-4. Heading problems
- `/visit/` has no H1 (it starts with an H2 "Opening hours"). This page earns 129 clicks across its queries, the second-largest share after the home page. Add `<h1>Visit our roastery cafe in Ubud</h1>`.
- `/coffee/brewing-guide/` has two H1s ("Coffee brewing guide" and "Brew methods"). Make the second an H2, and make the bold-text "Grind size chart / Water temperature / Troubleshooting" lines H2s so Google can use them as sections.
- Blog posts use bold run-in labels where subheads (H2) would give structure for featured snippets and AI answers.

### P2-5. Product schema errors
- **`/coffee/bali-kintamani/`:** the Product has no `name`, which is required. Rich results and Merchant listings will not validate.
- **All Product markup:** no `url`, `sku`, `priceValidUntil` or `itemCondition`, and there is only one offer, although both pages sell 250g and 1kg. `/coffee/java-ijen/` names "Java Ijen washed coffee, 250g", which doesn't match its on-page heading.
- **`/coffee/flores-bajawa/`:** no Product schema at all.
- **Fix:** add `name`, `sku`, `url`, and an offer for each size, and a `shippingDetails`/`hasMerchantReturnPolicy` block if you want shopping-surface eligibility. Validate in the Rich Results Test. Don't add `aggregateRating` unless there are real, visible reviews.

### P2-6. FAQPage markup doesn't match visible content
- **URL:** `/coffee/`. The JSON-LD has two questions ("How fresh...", "Do you ship outside Bali?") that are not shown as questions on the page. Only the freshness fact is in the body.
- **Why it matters:** structured data should describe content the user can see. In addition, Google restricted FAQ rich results to well-known government and health sites in 2023, so this markup earns nothing in the SERP for a shop.
- **Fix:** either remove it, or add a visible FAQ section (including shipping outside Bali, which the home page covers only partly) and leave the markup for other consumers. Removing is fine.

### P2-7. No local business entity or markup
- **Evidence:** the only entity markup is `Organization` on the home page. The cafe's hours, phone and address appear as text on `/visit/` and `/contact/` with no structured data, and `/visit/` doesn't show the street address in the body (only in the footer).
- **Why it matters:** local queries are a large share of demand: "coffee shop ubud" has 2,240 impressions at position 13.5 (0.7% CTR), "coffee roastery ubud" 1,320 at 6.8 (3.1%), "ubud coffee roaster" 640 at 8.9. Closing the gap to the top 3 is the biggest non-brand opportunity in the data.
- **Fix:** add `CafeOrCoffeeShop` (or `LocalBusiness`) JSON-LD on `/visit/` with `openingHoursSpecification` (7:00 to 17:00 daily), `telephone`, `geo`, `priceRange`, `image`, `hasMap` and `sameAs` to the social and Google profiles. Put the full address, an embedded map and directions in the body of `/visit/`. Claim and complete the Google Business Profile (categories "Coffee roaster" and "Cafe", photos, hours, Saturday cupping as an event) and keep the name, address and phone identical everywhere. Add `sameAs` to the Organization markup.

### P2-8. Title and description clean-up
| URL | Problem | Suggested fix |
|---|---|---|
| `/coffee/bali-kintamani/` | Title is 88 characters and will be truncated; target query is "bali kintamani coffee" (1,450 impressions, 2.1% CTR at position 8.2) | "Bali Kintamani Natural Coffee Beans, 250g \| Kopi Kita" (about 52 characters) |
| `/about/` | No meta description; title has no location, though it ranks for "ubud coffee roaster" | Add a description; title "About Kopi Kita: Ubud Coffee Roaster Since 2019" |
| `/contact/` | No canonical tag (the only page without one) | Add a self-canonical |
| `/contact/`, `/blog/`, `/blog/cold-brew-at-home/` | Descriptions are short (77, 95, 83 characters) | Expand to 120 to 155 characters with a call to action |
| `/visit/` | Description fine; page is competing with home for "coffee shop ubud" | Add "coffee shop in Ubud" to the title |

### P2-9. Sitemap quality
- **URL:** `/sitemap.xml` lists 18 URLs. Of these, one is a 404, one is `noindex` and one is canonicalised away (three of 18).
- **Missing:** `<lastmod>` on every entry.
- **Fix:** list only indexable 200 pages, and add accurate `lastmod` values (the blog posts' `dateModified` is a good source). Resubmit in Search Console once fixed.

### P2-10. Oversized image on `/about/`
- **URL:** `/assets/img/roastery-hero.jpg` is 1,818,123 bytes (1.8 MB), dimensions 2400x1600. Everything else on the site is under 14 KB.
- **Why it matters:** this is the About page's likely LCP element and the heaviest asset on the site by a factor of over 100. It slows the page on mobile.
- **Fix:** resize to the largest displayed width (about 1200 to 1600 px), export as WebP or AVIF with a JPEG fallback, aim for under 200 KB, add `srcset`/`sizes`, and use `fetchpriority="high"` for the LCP image. The width and height attributes are already set, which is good for layout shift.

### P2-11. Missing alt text on the home page hero
- **URL:** `/` with `/assets/img/hero-beans.jpg` (the crawl shows "(missing)"; the HTML has no `alt` at all).
- **Fix:** add descriptive alt text such as "Freshly roasted single-origin coffee beans from Bali" (use `alt=""` only if the image is purely decorative, which a hero usually is not).

---

## Priority 3: Low (backlog)

- **Internal linking is nav-heavy.** Every page gets 16 sitewide links, but the content pages get almost no editorial links. Blog posts have 1 inlink each (just the blog index); `/visit/` has 2. Add in-body links: from the brewing guide and pour-over post to the coffee pages, from the cold-brew and Kintamani posts to each other, and from the home page to `/visit/`.
- **Two pages for one local intent.** Home ranks for "coffee roastery ubud" and `/about/` for "ubud coffee roaster". Make the home page the target and give `/about/` a brand-story focus.
- **No Open Graph or Twitter Card tags** on any page. Add `og:title`, `og:description`, `og:image`, `og:type` and `twitter:card`, with a branded 1200x630 image for each page type.
- **No favicon or logo in the HTML.** The logo is only referenced in schema. Add a `<link rel="icon">` and show the logo in the header.
- **Article markup is thin.** Add `image`, `publisher` (Organization with logo), `author.url` and `mainEntityOfPage`. `/blog/pour-over-coffee-guide/` has `dateModified` equal to `datePublished` although the text has been revised. Show the author and date on the page and link the author name to the About page.
- **E-E-A-T.** The strongest trust material (head roaster Wayan Sudarma, 12 years' experience, Melbourne training, 30+ wholesale partners, farmer-group relationships) lives only on `/about/`. Add a short author box to every article and cite farmer groups and photos on each coffee page.
- **No breadcrumbs.** Add visible breadcrumbs and `BreadcrumbList` for the `/coffee/` and `/blog/` sections.
- **Product image check.** `ijen.jpg` and `bajawa.jpg` are both exactly 6,405 bytes and `kintamani.jpg` is 6,404, so they may be placeholders or near-identical images. Confirm they show the right bag for each coffee.
- **Language.** The site is English-only, with an Indonesian shipping market. The GSC sample has no Indonesian queries. Consider a small Indonesian-language section later, with `hreflang`, if local demand matters.
- **Low-impression pages.** "Brewing guide" queries ("coffee brewing guide" 1,240 impressions at position 12.8, "coffee grind size chart" 980 at 15.5) could be lifted with a real grind-size table and a method-by-method section. It is the sort of structured content AI answers quote.
- **AI search readiness.** Content is plain, factual and well-structured (quantified recipes, named origins), which is good for citation. No `llms.txt` is needed, and Google ignores it. The gains are the schema and entity work above, plus question-style H2s on guides.
- **Unverified items.** Confirm on production: HTTPS with HSTS, one canonical host (www vs non-www, http to https redirects), trailing-slash redirects, security headers, and a custom 404 page that returns a real 404 status. The local server can't answer these.

---

## What is working

- Every indexable page has a self-referencing, absolute canonical (except `/contact/`).
- Clean, readable, lowercase URLs with trailing slashes; no parameters.
- Titles are unique and well-sized on most pages, descriptions are present on all but one, and the home title includes the brand and location.
- Semantic HTML with `lang="en"`, a viewport tag, and `width`/`height` set on every image.
- Descriptive alt text on all product images and the About image.
- Good, specific, useful copy: real brew ratios, altitudes, varieties, harvest dates, and prices on the coffee pages.
- robots.txt includes the `Sitemap:` line, and the sitemap is at the standard location.
- Branded search is strong (position 1.1 to 1.6, 20 to 35% CTR).
- No JavaScript dependency: content is in the initial HTML.

---

## Suggested order of work

| Phase | When | Items |
|---|---|---|
| 1. Quick fixes | Days 1 to 3 | Nav link to `/visit/`; remove CSS block; fix sitemap (remove 404, noindex or canonicalised URLs) and Aceh Gayo link; unique `/subscriptions/` title; `/about/` description; `/contact/` canonical; hero alt text; `/visit/` H1; confirm wholesale `noindex` |
| 2. Consolidation | Week 1 to 2 | Merge the two pour-over posts with a 301; decide `/shop/` canonical; retitle and move the 2024 guide; Kintamani title; brewing-guide headings |
| 3. Content and schema | Weeks 2 to 4 | Expand `/coffee/`, Flores, cold brew; Product schema fixes; local business schema, GBP and `/visit/` content; compress the About image |
| 4. Monitor | Ongoing | Re-export GSC in 4 to 6 weeks and compare the pour-over, local and Kintamani queries. Use URL Inspection on `/shop/`, `/wholesale/` and the merged pour-over page. Track branded vs non-branded share. |

Note: no attempt was made to link any ranking movement to Google algorithm updates. The evidence doesn't contain before-and-after data that would support that.
