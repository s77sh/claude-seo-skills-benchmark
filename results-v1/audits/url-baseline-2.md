# SEO Audit: Kopi Kita (kopikita.test)

Audited 22 Oct 2026 against the local copy at http://localhost:8765/. I fetched every URL in the sitemap, every URL in the nav, `robots.txt`, `sitemap.xml`, and the key assets. Paths below are relative to the site root.

**What I could not check:** real-world performance (the local Python dev server sends no compression or cache headers, so I have left those out), HTTPS/redirects between www and non-www, Search Console data, backlinks, and rankings.

## Summary

| Priority | # | Issue |
|---|---|---|
| Critical | 1 | `/shop/` canonical points to `/coffee/` (the shop page asks to be deindexed) |
| Critical | 2 | `/wholesale/` is `noindex` but is a core commercial page, listed in the sitemap and linked from the nav |
| Critical | 3 | Sitemap lists `/coffee/sumatra-mandheling/` which returns 404 |
| High | 4 | Broken internal link to `/coffee/aceh-gayo/` (404) |
| High | 5 | Nav link `/menu/` goes through a redirect chain (`/menu/` → `/cafe/` → `/visit/`) |
| High | 6 | Duplicate title on `/coffee/` and `/subscriptions/` |
| High | 7 | Two blog posts compete for the same pour over query |
| High | 8 | `robots.txt` blocks `/assets/css/` |
| Medium | 9 | `/visit/` has no `<h1>` |
| Medium | 10 | `/coffee/brewing-guide/` has two `<h1>` tags |
| Medium | 11 | Missing meta descriptions on `/about/` |
| Medium | 12 | Missing canonical on `/contact/` |
| Medium | 13 | Orphaned or weakly linked product pages (`/coffee/flores-bajawa/`) |
| Medium | 14 | Structured data errors and gaps (Product, Article, FAQPage, Organization) |
| Medium | 15 | Oversized image on `/about/` (1.8 MB) |
| Low | 16 | Homepage hero image has no `alt` |
| Low | 17 | Dated "2024" in URL and title of an evergreen post |
| Low | 18 | Thin content on `/blog/cold-brew-at-home/` |
| Low | 19 | No Open Graph / Twitter tags |
| Low | 20 | Sitemap has no `<lastmod>`; some pages are missing from it |
| Low | 21 | Default 404 page |
| Low | 22 | No breadcrumbs / weak internal linking from the homepage |

---

## Critical

### 1. `/shop/` canonicalises to `/coffee/`
- **URL:** `/shop/`
- **Found:** `<link rel="canonical" href="https://kopikita.test/coffee/">`, yet the page has its own title, description and unique content (gear, drip bags, shipping threshold).
- **Why it matters:** Google treats the canonical as a strong signal and will probably drop `/shop/` from the index in favour of `/coffee/`. You lose rankings for "buy coffee beans", "brewing gear" and "drip bags" queries. It's also in your sitemap, which sends a contradictory signal.
- **Fix:** Change the canonical to `https://kopikita.test/shop/`. If `/shop/` really is meant to be a duplicate of `/coffee/`, then remove it from the sitemap and 301 it instead. But the content is distinct, so a self-canonical is the right choice.

### 2. `/wholesale/` is set to `noindex`
- **URL:** `/wholesale/`
- **Found:** `<meta name="robots" content="noindex, follow">`, while the page has a unique title, description and a canonical, is listed in the sitemap, and sits in the main nav and homepage copy.
- **Why it matters:** The page targets B2B queries ("wholesale coffee Bali", "coffee supplier for cafes and hotels"), and noindex removes it from Google completely. It looks like a leftover from staging or an accident; the sitemap entry and canonical show you want it indexed.
- **Fix:** Remove the robots meta tag (or set `index, follow`). Re-submit the URL in Search Console. If you do want it hidden, remove it from the sitemap and nav instead; don't mix signals.

### 3. Sitemap contains a 404 URL
- **URL:** `/coffee/sumatra-mandheling/` (listed in `/sitemap.xml`)
- **Found:** Returns `404 File not found`. Nothing links to it from the site.
- **Why it matters:** Sitemap URLs that 404 waste crawl budget and get reported as errors in Search Console, and they reduce Google's trust in the sitemap as a whole.
- **Fix:** Either publish the Sumatra Mandheling product page (with title, description, Product schema, and links from `/coffee/` and `/shop/`) or remove the entry from the sitemap. Generate the sitemap from the pages that exist so this can't recur.

---

## High

### 4. Broken internal link to a missing product
- **URL affected:** `/blog/how-to-brew-pour-over/` links to `/coffee/aceh-gayo/`, which returns 404.
- **Why it matters:** Dead internal links waste link equity, frustrate users at the point where they are ready to buy, and signal low quality. The post is your best-linked piece of content, so it should send people to real products.
- **Fix:** Remove the link or point it at an existing heavy-bodied coffee such as `/coffee/bali-kintamani/`. Run a link checker across the site after each release.

### 5. Redirect chain in the main navigation
- **URL:** `/menu/` (nav label "Visit the cafe", on every page)
- **Found:** `/menu/` → 301 → `/cafe/` → 301 → `/visit/` (200). The sitemap and canonical use `/visit/`.
- **Why it matters:** Every page on the site links to a URL that takes two hops. Chains slow users down, dilute equity, and Google may stop following after several hops. The nav is sitewide, so this repeats on all 20 pages.
- **Fix:** Update the nav href to `/visit/` and make `/menu/` and `/cafe/` each 301 straight to `/visit/`. Also consider whether the label "Visit the cafe" should match the page's title, "Visit Our Roastery Cafe".

### 6. Duplicate title tag
- **URLs:** `/coffee/` and `/subscriptions/` both use `Single-Origin Indonesian Coffee | Kopi Kita`.
- **Why it matters:** The subscriptions page is a different intent (recurring delivery). With an identical title Google may rewrite the title or treat the pages as competing, and the subscription page gets no keyword relevance for "coffee subscription".
- **Fix:** Give `/subscriptions/` something like `Coffee Subscription in Indonesia: Fresh Beans Every 2–4 Weeks | Kopi Kita`. Keep the `/coffee/` title as is.

### 7. Keyword cannibalisation between two blog posts
- **URLs:** `/blog/how-to-brew-pour-over/` and `/blog/pour-over-coffee-guide/`
- **Found:** Both target "pour over coffee" (how to brew / guide for beginners), share the same recipe (15g / 250g / 93C / 40g bloom / 3 minutes), and both link to Java Ijen. Both are in the blog index and sitemap.
- **Why it matters:** Two near-identical pages compete for the same query, so neither ranks as well as one stronger page would. Google may alternate between them.
- **Fix:** Pick one as the primary. Options: (a) merge the beginner content into the longer `how-to-brew-pour-over` post and 301 the other to it; or (b) differentiate clearly (one is gear and beginner setup, the other is the technique and troubleshooting), rewrite the titles/H1s so they target different queries, and link them to each other with distinct anchor text. Option (a) is simpler.

### 8. `robots.txt` blocks CSS
- **URL:** `/robots.txt` has `Disallow: /assets/css/`
- **Why it matters:** Googlebot renders pages and needs CSS to see layout, mobile-friendliness and hidden content. Blocking it can cause rendering to be misjudged. There is no reason to hide stylesheets.
- **Fix:** Remove the `Disallow: /assets/css/` line. Also note `/cart/` is disallowed but does not exist (404); that's harmless, but keep it only if a cart is planned. The `Sitemap:` line is correct.

---

## Medium

### 9. `/visit/` has no `<h1>`
- **Found:** The page only has `<h2>Opening hours</h2>` and `<h2>Menu</h2>`.
- **Why it matters:** The H1 is the page's main topic signal and is important for accessibility. This is also a local-intent page that should rank for "coffee shop Ubud".
- **Fix:** Add `<h1>Visit our roastery cafe in Ubud</h1>` above the first section, and include address and hours in text near the top.

### 10. Two `<h1>` tags on the brewing guide
- **URL:** `/coffee/brewing-guide/` has `<h1>Coffee brewing guide</h1>` and later `<h1>Brew methods</h1>`.
- **Fix:** Change the second to `<h2>`. Also consider H2s/H3s for the grind chart, temperature and troubleshooting blocks, which are currently bold paragraphs, so the page can win featured snippets and jump links.

### 11. Missing meta description
- **URL:** `/about/`
- **Why it matters:** Google will auto-generate a snippet from page text, usually less compelling and not controlled by you.
- **Fix:** Add a ~150 character description, e.g. "Kopi Kita started in 2019 in an Ubud garage. Meet our roasters and the farmer groups in Bali, Java and Flores we pay before harvest."

### 12. Missing canonical tag
- **URL:** `/contact/` is the only page without `rel="canonical"`.
- **Fix:** Add `<link rel="canonical" href="https://kopikita.test/contact/">`. Consider adding it to your page template so no page can miss it.

### 13. Weak internal linking to product pages
- **URL:** `/coffee/flores-bajawa/` (and `/coffee/sumatra-mandheling/`, which is also a 404)
- **Found:** `/coffee/` and `/shop/` only link Bali Kintamani and Java Ijen. Flores Bajawa is linked from nowhere except the sitemap, so it's effectively an orphan. The homepage only promotes two coffees as well.
- **Why it matters:** Orphan pages get little crawl priority and no internal equity, so a product on sale won't rank.
- **Fix:** List all current coffees on `/coffee/` and `/shop/`, and link Flores Bajawa from the homepage and relevant blog posts (e.g. the "best beans" post, which mentions only Kintamani).

### 14. Structured data errors and gaps
| URL | Issue | Fix |
|---|---|---|
| `/coffee/bali-kintamani/` | `Product` schema has **no `name`** (required). Also missing `sku`/`gtin` etc., which are optional but useful. | Add `"name": "Bali Kintamani natural coffee, 250g"`. |
| `/coffee/java-ijen/` | Has `name`, but no `review`/`aggregateRating`, which is needed for star rich results. | Add real reviews only if you have them. Don't fabricate. Add `priceValidUntil` and `url` to the offer. |
| `/coffee/flores-bajawa/` | No Product schema at all, despite having price and image. | Add it, matching the other two. |
| `/coffee/` | `FAQPage` schema, but the questions and answers are **not visible on the page** (the page just has prose). Google requires FAQ markup to match visible content, and since 2023 FAQ rich results are shown only for a few authoritative government/health sites, so there is little upside. | Either show the FAQ on the page, or remove the markup. Removing is fine. |
| `/blog/*` (3 posts) | `Article` schema has no `image`, no `publisher`, and the author is a bare `Person` with no `url`. | Add `image`, `publisher` (Organization with logo), and an author URL (an author bio page, ideally on `/about/`). |
| `/blog/best-coffee-beans-2024/` | Schema headline ("The best coffee beans in Bali") doesn't match the H1 ("... (2024 guide)"). | Make them match. |
| `/` | `Organization` has no `sameAs` (social profiles), `telephone`, or `email`. The business is also a physical cafe. | Use `CafeOrCoffeeShop` (a LocalBusiness subtype) on `/visit/` and/or `/` with `openingHoursSpecification` (7am–5pm daily), `geo`, `telephone`, `priceRange`, and `image`. Check that `logo.png` is at least 112×112 px. |

Validate everything afterwards with Google's Rich Results Test.

### 15. Oversized image
- **URL:** `/about/`, `/assets/img/roastery-hero.jpg`
- **Found:** 1,818,123 bytes, declared at 2400×1600. Compare with `hero-beans.jpg` at 13.8 KB.
- **Why it matters:** A 1.8 MB hero slows LCP, especially on mobile in Indonesia where connections vary, and speed is a ranking factor.
- **Fix:** Resize to the largest displayed width (about 1200–1600 px), convert to WebP/AVIF, aim for under 200 KB, and use `srcset`. Add `fetchpriority="high"` for above-the-fold images, and `loading="lazy"` for ones below it.

---

## Low

### 16. Homepage hero image missing `alt`
- **URL:** `/` (`/assets/img/hero-beans.jpg`). All other images on the site have alt text.
- **Fix:** Add a descriptive alt such as "Freshly roasted single-origin coffee beans from Indonesia".

### 17. "2024" baked into an evergreen URL and title
- **URL:** `/blog/best-coffee-beans-2024/`, title "Best Coffee Beans in Bali (2024 Guide)"
- **Why it matters:** It's 2026; the "2024" signals that it is stale and lowers click-through, though `dateModified` says 2026-09-01. The post also says "our picks this year" without a year.
- **Fix:** Retitle to "(2026 Guide)" or remove the year. Move to a year-free URL (e.g. `/blog/best-coffee-beans-bali/`) with a 301 from the old one and an updated canonical and sitemap entry. Update the blog index text, which already says "The best coffee beans in Bali".

### 18. Thin content
- **URL:** `/blog/cold-brew-at-home/` is a single paragraph (~70 words) and has no schema or author, while sibling posts are 400–600 words. `/brewing-guide/` already covers the same recipe.
- **Fix:** Expand (steeping vs. immersion, ratios for concentrate, storage, troubleshooting, FAQ), or fold it into the brewing guide and 301 it. Add Article schema and a byline.

### 19. No social sharing metadata
- **Found:** No `og:title`, `og:description`, `og:image`, `og:url`, or `twitter:card` on any page.
- **Fix:** Add them in the page template. Use product photos for product pages, and a 1200×630 image for the default.

### 20. Sitemap improvements
- No `<lastmod>` values anywhere. Add accurate ones (the blog schema dates give you the data); Google uses them when they are trustworthy.
- `/shop/` is listed but its canonical points elsewhere (see #1).
- `/wholesale/` is listed but noindex (see #2).
- Check after fixes that every sitemap URL returns 200, is indexable and self-canonical.

### 21. Default 404 page
- **URL:** any missing URL, e.g. `/nonexistent-xyz`. The server returns a correct 404 status, but the body is the bare Python error page without navigation or branding.
- **Fix:** Add a branded 404 page with the nav, a search box or links to `/coffee/`, `/shop/` and `/blog/`. Keep the 404 status code.

### 22. Internal linking and navigation
- No breadcrumbs on product or blog pages. Add visible breadcrumbs with `BreadcrumbList` schema.
- The blog index has no dates or descriptions, only bare links; add the date and a one-line summary per post.
- Nav label "Visit the cafe" vs. URL `/visit/` vs. old `/menu/` vs. `/cafe/` is inconsistent; settle on one name.
- Pages link to one another mostly through the global nav and thin related links. Add contextual links from the homepage to Flores Bajawa and the subscription page, and from blog posts to `/subscriptions/` and `/shop/`.

---

## What's working

- Every page except `/contact/` has a unique title under ~65 characters (apart from #6) and, except `/about/`, a description of a good length.
- `lang="en"` and the viewport meta tag are set; canonicals use absolute HTTPS URLs on the production domain.
- `robots.txt` references the sitemap; 404s return a proper 404 status.
- Images other than the home hero have alt text and explicit width/height (prevents layout shift).
- Content is real and specific (prices, tasting notes, brew ratios), with sensible H1s on all but `/visit/`.

## Suggested order of work
1. Fix #1, #2, #3 (one-line changes with the biggest indexing impact), then #4, #5, #8.
2. Fix the titles/headings/meta items (#6, #9–#12).
3. Resolve the pour over cannibalisation (#7) and internal linking (#13, #22).
4. Clean up structured data (#14), images (#15, #16), and the lower-priority items.
