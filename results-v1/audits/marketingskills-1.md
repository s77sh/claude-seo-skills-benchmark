# SEO Audit: Kopi Kita (kopikita.test)

Audit date: 22 October 2026
Evidence: raw HTML for all 16 pages, `robots.txt`, `sitemap.xml`, a Screaming Frog-style crawl (`crawl.csv`, 26 URLs), a Search Console export (`gsc.csv`, 22 Jul to 21 Oct 2026, 27 query/page rows), and live header checks against http://localhost:8765/.

## Executive summary

Kopi Kita is a small, clean, 16-page site for a specialty roaster and cafe in Ubud. The basics are in place: every page has a title, a viewport tag, `lang="en"` and mostly sensible canonicals, and the pages have real, specific copy. The problems are mostly self-inflicted conflicts between signals: the sitemap, the canonical tags, the robots tags and the internal links disagree with each other.

Search Console shows the site lives on brand searches. Of the 832 clicks in the export, 574 (69%) come from "kopi kita" queries. Almost every non-brand query sits on page 2 or lower, or on page 1 with a weak click-through rate. That is where the growth is.

**Top priorities**

1. **Two pour over articles compete for the same queries.** They split about 8,830 impressions and 36 clicks across positions 14 to 21. Merge them (issue 1).
2. **The sitemap lists URLs that should not be there:** a 404 page, a `noindex` page and a page canonicalised elsewhere (issue 2).
3. **The main navigation links to `/menu/`, which redirects twice** before reaching `/visit/`. The `/visit/` page has no H1 and is the page Google associates with "coffee shop ubud" (2,240 impressions, position 13.5) (issues 3 and 9).
4. **`/wholesale/` is set to `noindex`** while being linked from the main nav and listed in the sitemap. It is probably an accident (issue 4).
5. **`/shop/` canonicalises to `/coffee/`** even though it has different content (issue 5).

**Quick wins (under an hour each):** change the nav link from `/menu/` to `/visit/`, fix the `/subscriptions/` title, remove the 404 and `noindex` URLs from the sitemap, fix the `/coffee/aceh-gayo/` link, add alt text to the home hero image, add a canonical to `/contact/`, and add a meta description to `/about/`.

## Scope and limits

- Schema was checked in the raw HTML and cross-checked against the crawl. All JSON-LD on this site is inline in the HTML, so the raw HTML is reliable for it. Nothing is injected by JavaScript on the pages supplied.
- The localhost server is a plain Python file server. I could not test HTTP to HTTPS redirects, `www` vs non-`www`, HSTS, caching headers, compression or TTFB. Those are listed under "Not verified".
- No Core Web Vitals data was supplied. Page weight and image findings below are from file sizes only.
- The GSC export covers 27 rows, so it is the top of the query list rather than every query. Pages with no rows (`/wholesale/`, `/coffee/flores-bajawa/`, `/subscriptions/` aside from one query) may have queries that are simply below the export cutoff. I do not claim they get no traffic.
- Impact ratings are judgement calls based on the evidence. I have not forecast traffic gains, because the export has no baseline to forecast from.

---

## Findings in priority order

Impact: **High** blocks or splits ranking on a page that matters. **Medium** costs clicks or clarity. **Low** is hygiene.

### 1. Two pour over articles cannibalise each other (High)

**URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`

**Evidence (GSC).** Google swaps between the two pages for the same queries, and neither gets above position 13.9:

| Query | how-to-brew-pour-over | pour-over-coffee-guide |
|---|---|---|
| pour over coffee | 2,410 impr, pos 16.2 | 1,980 impr, pos 18.7 |
| how to make pour over coffee | 1,350 impr, pos 14.1 | 1,120 impr, pos 17.3 |
| pour over coffee guide | 610 impr, pos 19.4 | 820 impr, pos 13.9 |
| pour over ratio | 540 impr, pos 21.0 (one page only) | none |

Together: about 8,830 impressions and 36 clicks (0.4% CTR). Both pages are indexed, both are in the sitemap, and both carry the same recipe (15g coffee, 250g water, 93C, 40g bloom, about three minutes). Their titles and H1s target the same topic.

**Why it matters.** Two near-identical pages split links, internal anchors and click data, so neither looks like the best answer. Google is also testing both for each query, which is why the rankings are unstable.

**Fix.**
1. Keep `/blog/how-to-brew-pour-over/`. It has the most impressions, the best positions on 3 of 4 shared queries, and is the more recent edit (modified 2026-08-02).
2. Move the beginner-only material from the other page into it: dripper choice (V60 vs Kalita), filter rinsing, kettle options and the "try 1:15 vs 1:17" next-steps section. Add a short "Beginner mistakes" section so the "guide for beginners" intent is covered.
3. 301 redirect `/blog/pour-over-coffee-guide/` to the kept page. Remove it from the sitemap and from the blog index.
4. Retitle the kept page for the head term, for example "How to Make Pour Over Coffee: Recipe, Ratio and Beginner Guide | Kopi Kita" (about 66 characters, so trim to fit; see the title guidance in issue 14).
5. Add a ratio line near the top ("15g coffee to 250g water, a 1:16.7 ratio") to serve "pour over ratio".
6. Link to it from `/coffee/brewing-guide/` (the pour over line there currently has no link on the words "Pour over") and from `/coffee/java-ijen/`.
7. After the merge, re-check GSC after 4 to 6 weeks.

### 2. Sitemap lists URLs that are 404, noindex or canonicalised elsewhere (High)

**URL:** `/sitemap.xml`

**Evidence (crawl, "In Sitemap = Yes").**
- `/coffee/sumatra-mandheling/` returns **404** and has 0 inlinks.
- `/wholesale/` is `noindex, follow`.
- `/shop/` is canonicalised to `/coffee/`.

Three of the 18 sitemap entries (17%) should not be there. The sitemap also has no `<lastmod>` values.

**Why it matters.** A sitemap should list only canonical, indexable 200 URLs. Contradictory entries make Search Console report errors and make the file less trustworthy as a signal.

**Fix.** Remove the Sumatra 404 (or publish the product page, if the coffee is real). Resolve issues 4 and 5, then list `/wholesale/` and `/shop/` only if they end up indexable and self-canonical. Generate `<lastmod>` from real edit dates. After the change, resubmit in Search Console and check the "Page indexing" report.

### 3. Main nav links to `/menu/`, a double redirect chain (High)

**URLs:** `/menu/` to `/cafe/` to `/visit/` (the link is on every page)

**Evidence.** The nav on all 16 pages has `<a href="/menu/">Visit the cafe</a>`. Live check: `/menu/` returns 301 to `/cafe/`, which returns 301 to `/visit/`. The crawl shows `/menu/` with 17 inlinks and `/visit/` with only 2 (one from `/about/`, one from the redirect).

**Why it matters.** `/visit/` is the page that wins "kopi kita ubud" (96 clicks, position 1.6), "coffee cupping ubud" and "coffee shop ubud". Yet almost none of the site's internal links point at it directly. Each click through the nav costs two extra redirects, and chains waste crawl budget and dilute link signals.

**Fix.** Change the nav link to `/visit/` on all pages. Make `/menu/` and `/cafe/` each redirect straight to `/visit/` (single hop). Update any external profiles (Google Business Profile, social) that point to the old URLs.

### 4. `/wholesale/` is `noindex` but linked, listed and apparently meant to earn business (High, confirm intent)

**URL:** `/wholesale/`

**Evidence.** `<meta name="robots" content="noindex, follow">`. The page is in the sitemap, in the main nav (16 inlinks) and the About page promotes the 30+ wholesale partners. It has a title, meta description and 94 words of real copy. GSC shows no rows for it, which is consistent with it being kept out of the index.

**Why it matters.** Cafes, villas and hotels in Bali searching "wholesale coffee bali" or "coffee supplier ubud" cannot find this page. If wholesale is a revenue line, this is a lost channel. If it is deliberately private, it should not be in the sitemap or main nav.

**Fix.** If wholesale is meant to be public (likely), remove the `noindex` tag, keep the self-canonical, and expand the page (see issue 16). If it is deliberately hidden, remove it from the sitemap and say so in the team's SEO notes so nobody "fixes" it later.

### 5. `/shop/` is canonicalised to `/coffee/` but has different content (High)

**URL:** `/shop/`

**Evidence.** `<link rel="canonical" href="https://kopikita.test/coffee/">`. The crawl marks `/shop/` as Non-Indexable (Canonicalised) yet it is in the sitemap and has 16 inlinks. The page content is different from `/coffee/`: it covers gear (V60s, filters, grinder, scale), drip bags and a free-shipping threshold. Its title and description ("Shop Coffee Beans and Brewing Gear") do not match the page it points to.

**Why it matters.** Google will usually follow the canonical, so the gear and drip-bag content is never indexed and nothing ranks for those products. The site also has two near-identical navigation items for what is, to a crawler, one page.

**Fix.** Pick one:
- **Recommended:** make `/shop/` a real, self-canonical hub (beans, drip bags, gear, with links to product pages) and keep `/coffee/` as the beans category. Add individual pages or at least sections for gear and drip bags.
- **Alternative:** if `/shop/` is only meant to be a shortcut, 301 it to `/coffee/`, remove it from nav and sitemap, and merge the gear and drip-bag copy into `/coffee/`.

### 6. Internal link to a 404 page (High)

**URL affected:** `/blog/how-to-brew-pour-over/` links to `/coffee/aceh-gayo/`

**Evidence.** The article says "try our Aceh Gayo". The crawl and live check both show `/coffee/aceh-gayo/` returns 404. It is the only inlink to that URL. The article is the site's most visible blog post.

**Why it matters.** A dead link on a page that gets thousands of impressions loses the visitor at the point where they are most likely to buy, and sends crawlers to an error.

**Fix.** Either remove the Aceh Gayo sentence, or link to a live heavier-bodied coffee (`/coffee/bali-kintamani/` has "heavy body" in its copy). Do the same check for Sumatra Mandheling (issue 2): if neither coffee exists any more, decide whether any old pages elsewhere still link to them.

### 7. `robots.txt` blocks the stylesheet (Medium)

**URL:** `/robots.txt` (`Disallow: /assets/css/`)

**Evidence.** The crawl reports `/assets/css/site.css` as "Blocked by robots.txt". Every page loads that stylesheet.

**Why it matters.** Google needs CSS to render pages and judge mobile-friendliness and layout. Blocking it means Googlebot sees an unstyled page. It is a common leftover from old advice and has no upside.

**Fix.** Delete the `Disallow: /assets/css/` line. Keep `Disallow: /cart/` if a cart exists. The `Sitemap:` line is correct. Use the URL Inspection tool on `/` afterwards to confirm the rendered screenshot shows the styled page.

### 8. `/subscriptions/` has the same title as `/coffee/` (Medium)

**URL:** `/subscriptions/`

**Evidence.** Title is "Single-Origin Indonesian Coffee | Kopi Kita", identical to `/coffee/` (a copy-paste error). The H1 and meta description are correct ("Coffee subscriptions"). GSC shows "coffee subscription bali" at position 5.9 with 310 impressions and 9 clicks, the best-placed non-brand commercial query.

**Why it matters.** The title is the strongest on-page signal and the headline in the snippet. This page is on page 1 and the title does not mention subscriptions, which also makes it compete with `/coffee/` for the "single origin" query.

**Fix.** Change to something like "Coffee Subscription in Bali: Fresh Beans Every 2 or 4 Weeks | Kopi Kita". Keep it under about 60 characters if you can: "Coffee Subscription Bali: Fresh Beans Delivered | Kopi Kita" (58).

### 9. `/visit/` has no H1 and is under-built for local searches (High)

**URL:** `/visit/`

**Evidence.** The page has two `<h2>` tags ("Opening hours", "Menu") and no `<h1>`. GSC: "coffee shop ubud" 2,240 impressions, position 13.5, CTR 0.7% (15 clicks); "coffee cupping ubud" position 4.1, 6.2% CTR; "kopi kita ubud" 96 clicks. The page has 87 words, no address on the page body (only in the footer), no map or directions, no photos, and no LocalBusiness structured data.

**Why it matters.** For a local business this is the most important non-brand page. "Coffee shop ubud" is the largest single non-brand impression pool in the export, and the page is on page 2 for it.

**Fix.**
1. Add an H1, for example "Visit our roastery cafe in Ubud".
2. Add the full address, an embedded map, how to find it ("ten minutes from central Ubud" is a good start, add a landmark), opening hours, parking, and a photo of the cafe.
3. Give the Saturday public cupping its own short section with the day and time (Saturday 10am). If you want to rank for "coffee cupping ubud", consider a dedicated page later.
4. Add `CafeOrCoffeeShop` (or `LocalBusiness`) JSON-LD with address, `openingHoursSpecification`, `telephone`, `geo` and `url`. Use the same name, address and phone as the footer and the Google Business Profile.
5. Make sure the Google Business Profile exists, is verified, and links to `/visit/`. This is the main route into the local map pack, and I have no evidence about it either way.
6. Fix the internal links (issue 3) so the page gets nav-level link equity.

### 10. FAQPage schema describes content that is not on the page (Medium)

**URL:** `/coffee/`

**Evidence.** The JSON-LD contains two questions ("How fresh is your coffee?", "Do you ship outside Bali?") with answers. The visible page has no FAQ. The freshness fact appears in a sentence, but the "Do you ship outside Bali? Yes, everywhere in Indonesia" answer does not appear anywhere on the page.

**Why it matters.** Google's guidelines require structured data to match visible content. Mismatched markup risks a manual action for structured data and earns nothing: FAQ rich results are now shown only for a small set of authoritative government and health sites.

**Fix.** Either delete the FAQPage block, or add a visible FAQ section to the page with those questions and answers (which is also useful to customers) and keep the markup in sync. The visible FAQ is the better choice; I would not rely on the markup for rich results.

### 11. `/coffee/flores-bajawa/` is an orphan (Medium)

**URL:** `/coffee/flores-bajawa/`

**Evidence.** Crawl shows 0 inlinks. It is in the sitemap, so Google can find it, but no page on the site links to it. `/coffee/` and `/shop/` list only Kintamani and Ijen. Also, it has no Product schema, unlike the other two coffees.

**Why it matters.** A page with no internal links gets no link equity and signals that the site does not value it. It is a product page for a coffee you sell.

**Fix.** Add it to the `/coffee/` listing and to `/shop/` and the home page, link it from a relevant blog post, and add Product JSON-LD matching the other two (see issue 13).

### 12. Brewing guide has two H1s (Low)

**URL:** `/coffee/brewing-guide/`

**Evidence.** `<h1>Coffee brewing guide</h1>` and later `<h1>Brew methods</h1>` (crawl H1-1 and H1-2). It ranks for "coffee brewing guide" (1,240 impressions, position 12.8) and "coffee grind size chart" (980 impressions, position 15.5).

**Fix.** Change the second to an `<h2>`. While there, give the grind-size chart its own `<h2>` ("Coffee grind size chart") and format it as a table or list, because the current version is one bold-led paragraph. That targets the second query directly. Add a link to `/blog/cold-brew-at-home/` from the cold brew line and to the pour over article.

### 13. Product schema gaps (Medium)

**URLs:** `/coffee/bali-kintamani/`, `/coffee/java-ijen/`, `/coffee/flores-bajawa/`

**Evidence.**
- Kintamani Product JSON-LD has no `name` property (Ijen has one).
- Flores Bajawa has no Product markup at all.
- Offers only cover the 250g bag, and the pages sell a 1kg bag as well (Kintamani: Rp 145,000 / Rp 520,000).
- No `sku`, `url`, or `priceValidUntil`, and no review or rating data.

**Why it matters.** `name` is required for Product rich results, so the Kintamani markup is probably ineligible as it stands. Product snippets with price and availability can lift click-through for commercial queries like "bali kintamani coffee" (1,450 impressions, 2.1% CTR) and "buy coffee beans bali".

**Fix.** Add `name` to Kintamani, add Product markup to Flores Bajawa, and add a second Offer for the 1kg bag (or use `AggregateOffer`). Only add `aggregateRating` or `review` if you have real customer reviews shown on the page. Validate with Google's Rich Results Test, which renders the page; the markup here is static so it should be picked up either way.

### 14. Title tag problems: over-long, and weak on commercial queries (Medium)

**Evidence (crawl and GSC).**
- `/coffee/bali-kintamani/`: 88 characters ("Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita"). Google will truncate or rewrite it. Suggested: "Bali Kintamani Natural Coffee Beans, 250g | Kopi Kita" (53).
- `/` : "Kopi Kita | Specialty Coffee Roasted in Ubud, Bali" (50) is acceptable, but the query "coffee roastery ubud" (1,320 impressions, position 6.8, 3.1% CTR) uses the word "roastery". Consider "Kopi Kita: Specialty Coffee Roastery in Ubud, Bali" (49).
- `/about/`: "About Kopi Kita: Our Roastery Story" (35) is fine, but "ubud coffee roaster" (640 impressions, position 8.9, 1.9% CTR) lands here. The About page is not the right target for that query: the homepage or `/visit/` should be. Do not fight this with the About title; instead use "Ubud coffee roaster" naturally on the homepage and link to it.
- Pages ranking 5 to 12 with CTR at or below 2.9% (`/coffee/java-ijen/`, `/coffee/bali-kintamani/`, `/coffee/`, `/subscriptions/`) would benefit from adding a concrete reason to click, such as price, "roasted to order" or free shipping in Bali.

**Fix.** Rewrite titles as above, aim for 50 to 60 characters, then compare CTR for the same queries in GSC 4 to 6 weeks later.

### 15. `/blog/best-coffee-beans-2024/` is dated (Medium)

**URL:** `/blog/best-coffee-beans-2024/`

**Evidence.** The year 2024 is in the URL, title, H1 and meta (the schema headline omits it). The schema says `datePublished` 2024-01-15 and `dateModified` 2026-09-01, so it has been updated, but a visitor in 2026 sees "2024 Guide". The article says "Our picks this year". It ranks for "best coffee beans bali" (position 7.8, 960 impressions, 2.3% CTR) and "bali coffee beans" (position 11.4, 1,890 impressions, 0.7% CTR). It has one inlink (the blog index).

**Why it matters.** A stale year is a click-through penalty and the URL cannot be updated without a redirect later.

**Fix.** Move the URL to an evergreen slug (`/blog/best-coffee-beans-bali/`), 301 the old one, and update the title to "Best Coffee Beans in Bali: How to Choose (Updated 2026)". Update the schema headline to match the H1. Link to it from `/coffee/` and from the Kintamani page, and consider a short comparison table of Bali coffees.

### 16. Thin content on pages with commercial or ranking potential (Medium)

**Evidence (word counts from the crawl).**
- `/blog/cold-brew-at-home/`: 67 words, ranks at position 38.2 and 44.6 for "cold brew coffee at home" and "how to make cold brew coffee" (870 and 640 impressions, 1 click). It has a single paragraph and one inlink (the blog index). Compare the 330 to 440 words on the other blog posts.
- `/wholesale/`: 94 words.
- `/coffee/flores-bajawa/`: 75 words (Kintamani 104, Ijen 98).
- `/blog/` (index): 43 words, links only, no descriptions.

**Fix.** Expand the cold brew article to answer the common follow-up questions (coarse grind and why, steeping time range, dilution, concentrate vs ready-to-drink, storage, troubleshooting weak or bitter cold brew, hot bloom vs cold). Add a recipe with a ratio table. Link it from the brewing guide. Wholesale: add what you supply (grades, minimums, delivery area, sample process, training) and a clear enquiry form or WhatsApp button. Blog index: add a one-line summary under each post and the publish date.

### 17. Home page hero image has no alt text and the About hero is 1.8 MB (Medium)

**URLs:** `/` and `/about/`

**Evidence.** `hero-beans.jpg` has no `alt` attribute (crawl: "(missing)"). `roastery-hero.jpg` is 1,818,123 bytes at 2400x1600 and is displayed as an `<img>` at a larger size than most phones need. Width and height attributes are present (good, they prevent layout shift). No images use `loading="lazy"`, WebP or AVIF, or `srcset`.

**Why it matters.** Alt text is an accessibility requirement and an image-search signal. A 1.8 MB image can push LCP past 2.5 seconds on mobile data, and the hero image on the home page is likely the LCP element (I have no measured LCP).

**Fix.** Add descriptive alt text to the home hero. Re-export the images at the largest displayed size, as WebP or AVIF, targeting under 200 KB for heroes. Add `srcset`/`sizes`. Use `loading="lazy"` for images below the fold, but not on the LCP image (use `fetchpriority="high"` there). Run PageSpeed Insights on `/`, `/about/` and a product page to confirm.

Note: the three product images are 6,404 to 6,405 bytes each and the two with the same size are suspiciously alike. Check that they are the real product photos and not placeholders.

### 18. Missing canonical and meta description on two pages (Low)

**Evidence.**
- `/contact/` has no canonical tag (crawl: blank). Every other page has a self-referencing canonical.
- `/about/` has no meta description (crawl: length 0).
- Other descriptions are short: `/blog/` (95 chars), `/blog/cold-brew-at-home/` (83), `/contact/` (77). Most are under the 120 to 160 range.

**Fix.** Add `<link rel="canonical" href="https://kopikita.test/contact/">`. Write an About description, for example "Kopi Kita started in a Ubud garage in 2019. Meet the roasters, the farmer groups we buy from and the cafe where you can taste the coffee." Lengthen the short descriptions to roughly 120 to 155 characters with a reason to click.

### 19. Local and brand structured data is thin (Medium)

**URLs:** `/`, `/contact/`, `/visit/`

**Evidence.** Only the home page has Organization markup (name, URL, logo, address). There is no LocalBusiness or CafeOrCoffeeShop markup, no `sameAs`, no phone, no opening hours. The name, address, phone and hours appear in the page text (`/contact/`, `/visit/`, footer), so the data exists.

**Fix.** Add `LocalBusiness`/`CafeOrCoffeeShop` JSON-LD to `/visit/` (see issue 9), add `telephone`, `email` and `sameAs` (social profiles, Google Business Profile) to the Organization block, and keep NAP identical everywhere. Add `BlogPosting`/`Article` author URLs (below).

### 20. Authorship and trust signals are light (Low)

**Evidence.** Blog articles name "Wayan Sudarma" in schema but show no visible byline, date or author link on the page. The About page has his background ("trained in Melbourne, twelve years roasting") but it is not linked from the articles. The blog has no category pages. Contact details are good and there is no privacy policy or terms page in the crawl.

**Fix.** Add a visible byline and last-updated date to each article, linked to a short author bio (can be a section on `/about/`). Add a privacy policy page if the site collects any customer data (forms, subscriptions, analytics). These are trust signals for a food business, not ranking tricks.

### 21. Internal linking is shallow across the blog and products (Medium)

**Evidence (crawl inlinks).** `/blog/cold-brew-at-home/`, `/blog/best-coffee-beans-2024/` and `/blog/pour-over-coffee-guide/` each have 1 inlink, `/blog/how-to-brew-pour-over/` has 2, `/coffee/flores-bajawa/` has 0, and `/visit/` has 2. The three-coffee product set is linked mostly from the home page and nav, and the blog posts hardly link to each other. The home page links to products and the blog only through a few sentences.

**Fix.** Add a "Related reading" block to each article, link each coffee to the matching brewing advice and vice versa, link the brewing guide to every method article, and feature the best-selling product and the best-performing article on the home page. All pages are within two clicks of home, so depth is fine; it is link equity distribution that needs work.

### 22. Content gaps worth filling (Low, longer term)

Based on GSC demand and the site's offer:
- A page or section for "coffee cupping ubud" (position 4.1, 6.2% CTR) with date, price (free) and booking details.
- Pages for the other products you sell: drip bags and brewing gear (see issue 5).
- Grind size chart and pour over ratio content (issue 1 and 12).
- Wholesale content aimed at cafes and villas (issue 16).
- Origin pages per farmer group (Subak Abian, Ijen, Bajawa), which also support E-E-A-T because they show first-hand sourcing.

---

## What is working

- Every page has a unique title except `/subscriptions/` (issue 8), a meta viewport and `lang="en"`.
- Canonicals are absolute, HTTPS and self-referencing on 14 of 16 pages (exceptions: `/shop/`, `/contact/`).
- URLs are short, lowercase, hyphenated and have a consistent trailing slash.
- No duplicate content across hosts or protocols visible in the crawl. No hreflang is needed: the site is English only, so international SEO checks do not apply.
- Brand performance is excellent (position 1.1 to 1.6 on brand queries).
- Copy is specific and genuinely useful (ratios, altitudes, prices, harvest dates). Product facts agree across pages (prices, "30+ wholesale partners", roasting days, opening hours).
- Image dimensions are declared (no layout shift from images). Most images have good alt text.
- The sitemap and robots.txt both exist and reference each other.

## Not verified (needs access I did not have)

- HTTP to HTTPS redirect, `www` handling, HSTS, SSL certificate (the local server is HTTP only and the `.test` domain is a placeholder).
- Core Web Vitals, TTFB, caching and compression headers.
- Google Business Profile status, reviews and local rankings.
- Whether `/wholesale/` `noindex` is deliberate (issue 4).
- Backlink profile and competitor comparison (no link data supplied).
- Search Console Page Indexing and Core Web Vitals reports, and any manual actions or security issues.

## Prioritised action plan

**Week 1: fix conflicts (critical)**
1. Sitemap cleanup: remove the 404 and any non-indexable URLs (issue 2).
2. Nav link `/menu/` to `/visit/`, and flatten the redirects (issue 3).
3. Decide on `/wholesale/` (issue 4) and `/shop/` (issue 5).
4. Fix the `/coffee/aceh-gayo/` link (issue 6).
5. Remove the CSS block from robots.txt (issue 7).
6. Fix the `/subscriptions/` title (issue 8).

**Weeks 2 to 3: the biggest ranking gains**
7. Merge and redirect the pour over articles (issue 1).
8. Rebuild `/visit/` with an H1, address, map, photos and LocalBusiness schema; verify the Google Business Profile (issues 9 and 19).
9. Rewrite titles for CTR (issue 14); update the 2024 article (issue 15).

**Weeks 3 to 6: quality and structure**
10. Schema fixes: Product, FAQ (issues 10, 13).
11. Orphan page, internal links and related-reading blocks (issues 11 and 21).
12. Image optimisation (issue 17), cold brew and wholesale content (issue 16).
13. Small hygiene fixes: H1, canonical, descriptions, authorship (issues 12, 18, 20).

**Ongoing**
14. Re-pull the GSC export at 4, 8 and 12 weeks and compare impressions, CTR and position for the pour over cluster, "coffee shop ubud", "bali coffee beans" and "coffee roastery ubud".
15. Content gaps and links (issue 22), plus local citations and mentions from Bali food and travel sites to build authority beyond the brand.
