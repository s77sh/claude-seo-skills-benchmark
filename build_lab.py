"""Build the Kopi Kita lab site (20 planted SEO issues, see answer-key.md).

python3 build_lab.py OUT_DIR   -> writes OUT_DIR/site/ (HTML, robots, sitemap, assets)
"""
import json, os, random, sys
from PIL import Image

OUT = sys.argv[1]
SITE = os.path.join(OUT, "site")
BASE = "https://kopikita.test"

NAV = [("/", "Home"), ("/coffee/", "Coffee"), ("/shop/", "Shop"), ("/subscriptions/", "Subscriptions"),
       ("/wholesale/", "Wholesale"), ("/menu/", "Visit the cafe"), ("/blog/", "Blog"),
       ("/about/", "About"), ("/contact/", "Contact")]

def p(*paras):
    return "\n".join(f"<p>{x}</p>" for x in paras)

PAGES = {}

def page(path, title, body, desc=None, canonical="self", robots=None, schema=None):
    PAGES[path] = dict(title=title, body=body, desc=desc, canonical=canonical, robots=robots, schema=schema or [])

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Kopi Kita",
       "url": BASE + "/", "logo": BASE + "/assets/img/logo.png",
       "address": {"@type": "PostalAddress", "streetAddress": "Jl. Raya Sayan 12", "addressLocality": "Ubud",
                   "addressRegion": "Bali", "addressCountry": "ID"}}

# 14: hero image without alt
page("/", "Kopi Kita | Specialty Coffee Roasted in Ubud, Bali",
     """<h1>Specialty coffee, roasted in Ubud</h1>
<img src="/assets/img/hero-beans.jpg" width="1200" height="700">
""" + p("Kopi Kita roasts single-origin coffee from across Indonesia in small batches at our roastery in Ubud. We buy green coffee directly from farmer groups in Kintamani, Ijen and Flores, and we pay them before the harvest is sold.",
        "Every bag is roasted to order and shipped within two days anywhere in Bali, and within a week to the rest of Indonesia. If you live nearby, you can pick up at the roastery cafe and taste the coffee before you buy.",
        "New to specialty coffee? Start with our <a href=\"/coffee/brewing-guide/\">brewing guide</a>, or read the <a href=\"/blog/\">blog</a> for recipes. Cafes and hotels can order through our <a href=\"/wholesale/\">wholesale programme</a>.",
        "Our best seller is the <a href=\"/coffee/bali-kintamani/\">Bali Kintamani natural</a>: sweet, fruity and easy to brew. For something cleaner, try the <a href=\"/coffee/java-ijen/\">Java Ijen washed</a>."),
     desc="Single-origin Indonesian coffee, roasted to order in Ubud, Bali. Beans from Kintamani, Ijen and Flores, shipped across Indonesia.",
     schema=[ORG])

# 18: FAQPage schema with no visible FAQ
page("/coffee/", "Single-Origin Indonesian Coffee | Kopi Kita",
     """<h1>Our coffee</h1>
""" + p("We roast three to five single origins at a time, depending on the harvest. Each one comes from a farmer group we visit at least once a year.",
        "<a href=\"/coffee/bali-kintamani/\">Bali Kintamani natural</a>: strawberry, brown sugar, a heavy body. Our most popular coffee for filter and espresso.",
        "<a href=\"/coffee/java-ijen/\">Java Ijen washed</a>: clean, bright and floral, with a tea-like finish. Best as pour over.",
        "Not sure how to brew it? Our <a href=\"/coffee/brewing-guide/\">brewing guide</a> has ratios and grind sizes for every method.",
        "All coffee comes in 250g and 1kg bags, whole bean or ground to order. Bags are roasted within 48 hours of shipping."),
     desc="Shop single-origin coffee from Bali, Java and Flores, roasted to order in small batches in Ubud.",
     schema=[{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
         {"@type": "Question", "name": "How fresh is your coffee?", "acceptedAnswer": {"@type": "Answer", "text": "We roast within 48 hours of shipping."}},
         {"@type": "Question", "name": "Do you ship outside Bali?", "acceptedAnswer": {"@type": "Answer", "text": "Yes, everywhere in Indonesia."}}]}])

# 4: same title as /coffee/
page("/subscriptions/", "Single-Origin Indonesian Coffee | Kopi Kita",
     """<h1>Coffee subscriptions</h1>
""" + p("Get a fresh bag of single-origin coffee every two or four weeks. You pick the roast, the grind and the bag size, and you can pause or cancel any time from your account.",
        "Each delivery comes with a card from the roaster: where the coffee grew, who farmed it and how we suggest brewing it. Subscribers get every new origin first, often a week before it goes on the shop.",
        "Subscriptions start at Rp 165,000 per delivery for 250g, with free shipping in Bali. Gift subscriptions run for three, six or twelve months.",
        "Questions about your subscription? <a href=\"/contact/\">Contact us</a> and we usually reply the same day."),
     desc="Fresh single-origin coffee delivered every two or four weeks. Pause or cancel any time. Free shipping in Bali.")

# 2: canonical points to /coffee/
page("/shop/", "Shop Coffee Beans and Brewing Gear | Kopi Kita",
     """<h1>Shop</h1>
""" + p("Everything we sell in one place: coffee beans, drip bags, and the brewing gear we use at the roastery.",
        "Coffee: <a href=\"/coffee/bali-kintamani/\">Bali Kintamani</a>, <a href=\"/coffee/java-ijen/\">Java Ijen</a>, and seasonal lots when we have them.",
        "Gear: V60 drippers, paper filters, a hand grinder with ceramic burrs, and a 0.1g scale. We only stock gear we have used for at least a year.",
        "Drip bags: ten single-serve bags per box, for travel or the office. Just add hot water.",
        "Orders over Rp 500,000 ship free across Indonesia."),
     desc="Buy coffee beans, drip bags and brewing gear from Kopi Kita, a specialty roaster in Ubud, Bali.",
     canonical="/coffee/")

# 5: long title; 17: Product schema without name
page("/coffee/bali-kintamani/", "Bali Kintamani Natural Coffee Beans, Medium Roast, 250g Whole Bean or Ground | Kopi Kita",
     """<h1>Bali Kintamani natural</h1>
<img src="/assets/img/kintamani.jpg" alt="Bag of Bali Kintamani natural coffee beans" width="600" height="600">
""" + p("Grown at 1,400 metres on the slopes of Mount Batur by the Subak Abian farmer group. The cherries are dried whole on raised beds for three weeks, which gives this coffee its fruit.",
        "Tasting notes: strawberry, brown sugar, cacao. Heavy body, low acidity. Works as espresso and as filter.",
        "Roast: medium. Process: natural. Varieties: Kopyol and S795. Harvest: June to August 2026.",
        "We suggest 15g of coffee to 250g of water for pour over, or 18g in, 36g out in 28 seconds for espresso. See the <a href=\"/coffee/brewing-guide/\">brewing guide</a> for more.",
        "Rp 145,000 for 250g. Rp 520,000 for 1kg."),
     desc="Natural-process coffee from Mount Batur, Bali. Notes of strawberry, brown sugar and cacao. Roasted to order in Ubud.",
     schema=[{"@context": "https://schema.org", "@type": "Product",
              "image": BASE + "/assets/img/kintamani.jpg", "description": "Natural-process coffee from Mount Batur, Bali.",
              "brand": {"@type": "Brand", "name": "Kopi Kita"},
              "offers": {"@type": "Offer", "price": "145000", "priceCurrency": "IDR", "availability": "https://schema.org/InStock"}}])

# decoy: healthy product page
page("/coffee/java-ijen/", "Java Ijen Washed Coffee Beans | Kopi Kita",
     """<h1>Java Ijen washed</h1>
<img src="/assets/img/ijen.jpg" alt="Bag of Java Ijen washed coffee beans" width="600" height="600">
""" + p("From the Ijen plateau in East Java, grown at 1,500 metres in volcanic soil. The cherries are pulped, fermented for 36 hours and washed, which gives a very clean cup.",
        "Tasting notes: jasmine, lemon, black tea. Light body, bright acidity. Our pick for pour over.",
        "Roast: light. Process: washed. Varieties: Typica and USDA. Harvest: May to July 2026.",
        "Brew it at 15g to 250g of water, a little finer than usual, with water just off the boil. Our <a href=\"/coffee/brewing-guide/\">brewing guide</a> has the full recipe.",
        "Rp 150,000 for 250g. Rp 540,000 for 1kg."),
     desc="Washed coffee from the Ijen plateau, East Java. Notes of jasmine, lemon and black tea. Roasted to order in Ubud.",
     schema=[{"@context": "https://schema.org", "@type": "Product", "name": "Java Ijen washed coffee, 250g",
              "image": BASE + "/assets/img/ijen.jpg", "description": "Washed coffee from the Ijen plateau, East Java.",
              "brand": {"@type": "Brand", "name": "Kopi Kita"},
              "offers": {"@type": "Offer", "price": "150000", "priceCurrency": "IDR", "availability": "https://schema.org/InStock"}}])

# 8: orphan (in sitemap, nothing links here)
page("/coffee/flores-bajawa/", "Flores Bajawa Honey Coffee Beans | Kopi Kita",
     """<h1>Flores Bajawa honey</h1>
<img src="/assets/img/bajawa.jpg" alt="Bag of Flores Bajawa honey-process coffee beans" width="600" height="600">
""" + p("A honey-process lot from Bajawa in central Flores, grown at 1,300 metres under shade trees. Some of the fruit is left on the bean while it dries, which adds sweetness without the funk of a natural.",
        "Tasting notes: dark chocolate, red apple, clove. Medium body, round acidity.",
        "Roast: medium. Process: honey. Varieties: Typica and Catimor. Harvest: July to September 2026.",
        "Rp 155,000 for 250g. Rp 560,000 for 1kg."),
     desc="Honey-process coffee from Bajawa, Flores. Notes of dark chocolate, red apple and clove. Roasted to order in Ubud.")

# 13: two H1s
page("/coffee/brewing-guide/", "Coffee Brewing Guide: Ratios and Grind Sizes | Kopi Kita",
     """<h1>Coffee brewing guide</h1>
""" + p("Good coffee at home comes down to three things: the ratio of coffee to water, the grind size, and the water temperature. Get those right and most of the work is done.",
        "Start with 1 gram of coffee to 16 grams of water and adjust from there. If the cup tastes sour, grind finer. If it tastes bitter or dry, grind coarser.") + """
<h1>Brew methods</h1>
""" + p("Pour over: 15g coffee, 250g water at 93C, medium-fine grind, about 3 minutes in total.",
        "French press: 30g coffee, 500g water, coarse grind, steep for 4 minutes, then press slowly.",
        "Espresso: 18g in, 36g out, 25 to 30 seconds. Adjust the grind, not the dose.",
        "Cold brew: 100g coffee to 1 litre of cold water, coarse grind, 16 hours in the fridge.",
        "Want a step-by-step walkthrough? Read <a href=\"/blog/how-to-brew-pour-over/\">how to brew pour over</a>."),
     desc="Coffee-to-water ratios, grind sizes and temperatures for pour over, French press, espresso and cold brew.")

# 3: noindex on a page that should rank
page("/wholesale/", "Wholesale Coffee for Cafes and Hotels in Bali | Kopi Kita",
     """<h1>Wholesale coffee for cafes and hotels</h1>
""" + p("We supply more than 30 cafes, villas and hotels across Bali with fresh-roasted coffee every week. Wholesale prices start at 5kg per week.",
        "Every wholesale partner gets free barista training at the roastery, help dialling in their espresso, and a grinder on loan for the first three months.",
        "We roast on Monday and Thursday and deliver in Ubud, Canggu, Seminyak and Sanur the next day.",
        "Ask for a free sample box: <a href=\"/contact/\">contact us</a> with the name of your venue and how much coffee you use per week."),
     desc="Fresh-roasted wholesale coffee for cafes, villas and hotels in Bali. Free barista training and next-day delivery.",
     robots="noindex, follow")

# 12: no H1
page("/visit/", "Visit Our Roastery Cafe in Ubud | Kopi Kita",
     """<h2>Opening hours</h2>
""" + p("Our roastery cafe is open every day from 7am to 5pm, on Jalan Raya Sayan, ten minutes from central Ubud.",
        "You can watch us roast on Monday and Thursday mornings. Every Saturday at 10am we run a free public cupping: taste five coffees side by side and learn what to look for.") + """
<h2>Menu</h2>
""" + p("Espresso, pour over, cold brew and our own drip bags to take home. Pastries from a bakery down the road.",
        "Parking for motorbikes in front, and for cars on the side road."),
     desc="Visit the Kopi Kita roastery cafe in Ubud: opening hours, menu, free Saturday cuppings and directions.")

page("/blog/", "Coffee Blog: Brewing Tips and Bean Guides | Kopi Kita",
     """<h1>The Kopi Kita blog</h1>
""" + p("Recipes, brewing tips and notes from the farms we buy from.",
        "<a href=\"/blog/how-to-brew-pour-over/\">How to brew pour over coffee at home</a>",
        "<a href=\"/blog/pour-over-coffee-guide/\">A pour over coffee guide for beginners</a>",
        "<a href=\"/blog/best-coffee-beans-2024/\">The best coffee beans in Bali</a>",
        "<a href=\"/blog/cold-brew-at-home/\">How to make cold brew at home</a>"),
     desc="Brewing tips, recipes and bean guides from Kopi Kita, a specialty coffee roaster in Ubud, Bali.")

# 7: broken link to /coffee/aceh-gayo/; 19: cannibalizes with the next post
page("/blog/how-to-brew-pour-over/", "How to Brew Pour Over Coffee at Home | Kopi Kita",
     """<h1>How to brew pour over coffee at home</h1>
""" + p("Pour over is the easiest way to taste what makes a single-origin coffee different. All you need is a dripper, a paper filter, a kettle and a scale.",
        "1. Heat water to about 93C. 2. Rinse the paper filter and throw that water away. 3. Add 15g of medium-fine coffee. 4. Pour 40g of water and wait 30 seconds for the bloom. 5. Pour the rest slowly, in circles, until you reach 250g. 6. Let it drain. The whole brew should take about three minutes.",
        "If it drains too fast and tastes sour, grind finer. If it takes longer than four minutes and tastes bitter, grind coarser.",
        "Which coffee should you use? A washed coffee like our <a href=\"/coffee/java-ijen/\">Java Ijen</a> shows off pour over best. If you like it heavier, try our <a href=\"/coffee/aceh-gayo/\">Aceh Gayo</a>.",
        "For ratios for other methods, see the <a href=\"/coffee/brewing-guide/\">brewing guide</a>."),
     desc="A step-by-step pour over recipe: 15g of coffee, 250g of water, about three minutes. Plus how to fix sour or bitter cups.",
     schema=[{"@context": "https://schema.org", "@type": "Article", "headline": "How to brew pour over coffee at home",
              "datePublished": "2025-03-10", "dateModified": "2026-08-02", "author": {"@type": "Person", "name": "Wayan Sudarma"}}])

page("/blog/pour-over-coffee-guide/", "Pour Over Coffee Guide for Beginners | Kopi Kita",
     """<h1>Pour over coffee: a guide for beginners</h1>
""" + p("If you've never made pour over coffee, this guide is for you. Pour over means pouring hot water by hand over ground coffee in a filter, and it gives a clean, bright cup.",
        "You need a dripper (a V60 is a good start), paper filters, a kettle, a scale and freshly ground coffee. A gooseneck kettle helps but isn't required.",
        "The basic recipe: 15g of coffee, 250g of water at 93C. Bloom with 40g of water for 30 seconds, then pour the rest in slow circles. It should finish in about three minutes.",
        "Common mistakes: pre-ground coffee that's too fine, water that's too cool, and pouring too fast. Fix one thing at a time.",
        "Ready to try it? Our <a href=\"/coffee/java-ijen/\">Java Ijen</a> is a great first pour over coffee."),
     desc="New to pour over? What gear you need, the basic recipe, and the three most common beginner mistakes.",
     schema=[{"@context": "https://schema.org", "@type": "Article", "headline": "Pour over coffee: a guide for beginners",
              "datePublished": "2026-02-18", "dateModified": "2026-02-18", "author": {"@type": "Person", "name": "Wayan Sudarma"}}])

# 20: stale year in title and URL
page("/blog/best-coffee-beans-2024/", "Best Coffee Beans in Bali (2024 Guide) | Kopi Kita",
     """<h1>The best coffee beans in Bali (2024 guide)</h1>
""" + p("Bali grows some of the best coffee in Indonesia, almost all of it in the Kintamani highlands around Mount Batur. Here is what to look for when you buy.",
        "Kintamani naturals are fruity and sweet. Kintamani washed coffees are cleaner, with citrus notes. Both are grown at 1,200 to 1,600 metres, often next to citrus trees.",
        "Buy whole beans and check the roast date: coffee is best between one and four weeks after roasting. Avoid bags with no roast date at all.",
        "Our picks this year: the <a href=\"/coffee/bali-kintamani/\">Kopi Kita Kintamani natural</a> for sweetness, and a washed Kintamani from any good local roaster for something lighter.",
        "Skip kopi luwak. Most of it comes from caged animals, and it doesn't taste better."),
     desc="How to choose coffee beans from Bali: naturals vs washed, roast dates, and our picks from the Kintamani highlands.",
     schema=[{"@context": "https://schema.org", "@type": "Article", "headline": "The best coffee beans in Bali",
              "datePublished": "2024-01-15", "dateModified": "2026-09-01", "author": {"@type": "Person", "name": "Wayan Sudarma"}}])

# 16: thin page (about 80 words)
page("/blog/cold-brew-at-home/", "How to Make Cold Brew Coffee at Home | Kopi Kita",
     """<h1>How to make cold brew coffee at home</h1>
""" + p("Cold brew is easy. Mix 100g of coarse ground coffee with 1 litre of cold water in a jar. Leave it in the fridge for 16 hours, then strain it through a paper filter. Serve it over ice, with milk if you like. It keeps for a week in the fridge. A fruity natural like our <a href=\"/coffee/bali-kintamani/\">Kintamani</a> works well."),
     desc="An easy cold brew recipe: 100g of coffee, 1 litre of water, 16 hours in the fridge.")

# 6: no meta description; 15: 2MB hero
page("/about/", "About Kopi Kita: Our Roastery Story",
     """<h1>About Kopi Kita</h1>
<img src="/assets/img/roastery-hero.jpg" alt="The Kopi Kita roaster at work in Ubud" width="2400" height="1600">
""" + p("Kopi Kita started in 2019 with a 1kg roaster in a garage in Ubud. Today we roast about 400kg a week for our cafe, our online shop and more than 30 wholesale partners.",
        "We buy from four farmer groups in Bali, Java and Flores. We visit each of them every year, we pay above the market price, and we pay before the harvest is sold so farmers don't have to borrow.",
        "Our head roaster, Wayan Sudarma, trained in Melbourne and has roasted for twelve years. Our team of nine is all from Bali.",
        "Come and see us at the <a href=\"/visit/\">roastery cafe</a>, or <a href=\"/contact/\">get in touch</a>."),
     desc=None)

# 1: no canonical
page("/contact/", "Contact Kopi Kita | Ubud, Bali",
     """<h1>Contact us</h1>
""" + p("Email hello@kopikita.test or WhatsApp +62 812 0000 0000. We reply within a day, usually much faster.",
        "Roastery cafe: Jl. Raya Sayan 12, Ubud, Bali. Open every day, 7am to 5pm.",
        "Wholesale enquiries: tell us the name of your venue, where it is, and how much coffee you use per week, and we'll send a free sample box."),
     desc="Email, WhatsApp and the address of the Kopi Kita roastery cafe in Ubud, Bali.",
     canonical=None)

# Longer bodies for the real posts and guides, so the thin page (16) stands out.
EXTRA = {
    "/blog/how-to-brew-pour-over/": p(
        "<strong>Why weigh everything?</strong> A tablespoon of coffee can weigh anywhere from 5 to 9 grams depending on the roast and the grind. A cheap scale takes the guessing out, and it means you can repeat a cup you liked tomorrow.",
        "<strong>Grind size.</strong> Aim for something like coarse sand. If you only have pre-ground coffee, buy the filter grind, not espresso. A hand grinder with ceramic or steel burrs is the single best upgrade for pour over, better than any kettle.",
        "<strong>Water.</strong> Bali tap water is hard and changes from village to village. Use filtered or bottled water with some minerals in it. Distilled water makes flat, sour coffee because there is nothing in it to pull the flavour out.",
        "<strong>The bloom.</strong> Fresh coffee holds carbon dioxide from roasting. When you first add water, it bubbles up. Waiting 30 seconds lets that gas escape so the rest of the water can reach the coffee evenly. If your coffee doesn't bloom at all, it's probably more than six weeks old.",
        "<strong>Pouring.</strong> Pour in slow circles from the centre outwards, and avoid pouring straight onto the paper. Keep the water level steady rather than filling the dripper to the top. Some people pour in three or four stages of about 50g each; try both and see which you like.",
        "<strong>Dialling in.</strong> Change one thing at a time. Most problems are fixed by grind size alone. Write down the dose, the grind setting and the time for every cup you like, and after a week you will have your own recipe.",
        "<strong>Cleaning.</strong> Rinse the dripper after every brew and wash it with soap once a week. Old coffee oils go rancid and make every cup taste stale, even with fresh beans."),
    "/blog/pour-over-coffee-guide/": p(
        "<strong>Which dripper?</strong> A V60 is fast and gives a bright cup, but it punishes uneven pouring. A flat-bottom dripper like a Kalita Wave is more forgiving for beginners. Both cost less than a bag of good coffee.",
        "<strong>Paper filters.</strong> Use the filters made for your dripper. Rinse them with hot water first, or your first few sips will taste of paper. Brown unbleached filters need a longer rinse than white ones.",
        "<strong>Kettle.</strong> A gooseneck kettle gives you control over where the water goes. If you don't have one, pour from a normal kettle into a small jug first, and pour from the jug slowly.",
        "<strong>Freshness.</strong> Coffee is at its best between one and four weeks after roasting. Buy small bags often rather than one big bag a month, and keep them sealed, away from heat and light. Don't keep coffee in the fridge: it picks up smells and moisture.",
        "<strong>Tasting.</strong> Let the cup cool for a few minutes before you judge it. Flavours like fruit and sweetness show up as the coffee cools, and defects like sourness or bitterness are easier to spot too.",
        "<strong>Next steps.</strong> Once your basic cup is consistent, try changing the ratio: 1 to 15 for a stronger cup, 1 to 17 for a lighter one. Then try the same recipe with two different coffees side by side. That is how you learn what you like."),
    "/blog/best-coffee-beans-2024/": p(
        "<strong>Natural or washed?</strong> In a natural, the whole cherry dries around the bean, so the coffee tastes fruity and sweet, sometimes like wine. In a washed coffee, the fruit is removed before drying, so the cup is cleaner and the acidity is easier to taste. Neither is better; it depends on what you like.",
        "<strong>Altitude.</strong> Higher farms usually grow denser beans with more acidity and more complex flavours. Most of the coffee in Kintamani is grown between 1,200 and 1,600 metres, which is high for Indonesia.",
        "<strong>Roast level.</strong> A light roast keeps more of the flavour of the farm. A dark roast tastes more of the roast itself: chocolate, smoke and bitterness. For pour over, choose light to medium. For espresso with milk, medium to medium-dark.",
        "<strong>Where to buy.</strong> Buy from a roaster that prints the roast date, the farm or farmer group, the process and the altitude on the bag. If a bag only says \"100% Arabica\", you don't know much about what's inside.",
        "<strong>Price.</strong> Good specialty coffee from Bali costs between Rp 120,000 and Rp 200,000 for 250g. Much cheaper than that and the coffee is usually old, or a blend of unknown origins."),
    "/coffee/brewing-guide/": p(
        "<strong>Grind size chart.</strong> Extra fine for Turkish coffee, fine for espresso, medium-fine for pour over and AeroPress, medium for batch brewers, coarse for French press and cold brew.",
        "<strong>Water temperature.</strong> 90 to 96C for most methods. Use the hotter end for light roasts and the cooler end for dark roasts. If you don't have a thermometer, let a boiled kettle rest for 30 seconds.",
        "<strong>Troubleshooting.</strong> Sour, thin or salty: grind finer, use hotter water or brew longer. Bitter, dry or harsh: grind coarser, use cooler water or brew shorter. Weak: use more coffee. Too strong: add a little hot water to the finished cup."),
}
for k, v in EXTRA.items():
    PAGES[k]["body"] = PAGES[k]["body"].replace("\n<p>For ratios", "\n" + v + "\n<p>For ratios") if "For ratios" in PAGES[k]["body"] else PAGES[k]["body"] + "\n" + v

def render(path, d):
    head = [f"<title>{d['title']}</title>", '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">']
    if d["desc"]:
        head.append(f'<meta name="description" content="{d["desc"]}">')
    if d["robots"]:
        head.append(f'<meta name="robots" content="{d["robots"]}">')
    if d["canonical"]:
        c = path if d["canonical"] == "self" else d["canonical"]
        head.append(f'<link rel="canonical" href="{BASE}{c}">')
    head.append('<link rel="stylesheet" href="/assets/css/site.css">')
    for s in d["schema"]:
        head.append(f'<script type="application/ld+json">{json.dumps(s)}</script>')
    nav = " ".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    foot = '<footer><p>Kopi Kita, Jl. Raya Sayan 12, Ubud, Bali. <a href="/contact/">Contact</a></p></footer>'
    return ('<!doctype html>\n<html lang="en">\n<head>\n' + "\n".join(head) + "\n</head>\n<body>\n"
            f"<header><nav>{nav}</nav></header>\n<main>\n{d['body']}\n</main>\n{foot}\n</body>\n</html>\n")

for path, d in PAGES.items():
    folder = os.path.join(SITE, path.strip("/"))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w") as f:
        f.write(render(path, d))

# 10: robots blocks CSS
with open(os.path.join(SITE, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nDisallow: /assets/css/\nDisallow: /cart/\n\nSitemap: {BASE}/sitemap.xml\n")

# 11: sitemap lists a 404 (sumatra-mandheling); 8: lists the orphan
sm = [u for u in PAGES] + ["/coffee/sumatra-mandheling/"]
with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in sm:
        f.write(f"  <url><loc>{BASE}{u}</loc></url>\n")
    f.write("</urlset>\n")

os.makedirs(os.path.join(SITE, "assets/css"), exist_ok=True)
with open(os.path.join(SITE, "assets/css/site.css"), "w") as f:
    f.write("body{font-family:system-ui,sans-serif;max-width:46rem;margin:0 auto;padding:1rem;color:#222}"
            "nav a{margin-right:.8rem}img{max-width:100%;height:auto}\n")

img = os.path.join(SITE, "assets/img")
os.makedirs(img, exist_ok=True)
random.seed(7)
def small(name, color):
    Image.new("RGB", (600, 600), color).save(os.path.join(img, name), quality=80)
small("kintamani.jpg", (120, 70, 40)); small("ijen.jpg", (90, 60, 30)); small("bajawa.jpg", (70, 45, 25))
small("logo.png", (40, 30, 20))
Image.new("RGB", (1200, 700), (110, 75, 45)).save(os.path.join(img, "hero-beans.jpg"), quality=80)
# 15: about 2MB: noise compresses badly
big = Image.frombytes("RGB", (2400, 1600), os.urandom(2400 * 1600 * 3))
for q in (60, 50, 40, 30):
    big.save(os.path.join(img, "roastery-hero.jpg"), quality=q)
    if os.path.getsize(os.path.join(img, "roastery-hero.jpg")) < 2_400_000:
        break
print(len(PAGES), "pages;", "roastery-hero.jpg", os.path.getsize(os.path.join(img, "roastery-hero.jpg")), "bytes")
