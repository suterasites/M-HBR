#!/usr/bin/env python3
"""
Generate per-suburb Reblocking & Restumping pages by cloning the canonical
reblocking-restumping.html and localising it to a suburb. Deterministic +
idempotent: nav, footer, mobile menu, scripts, GA4 + SUTERA_LEAD_EVENTS and the
shared "Areas We Service" section are preserved byte-for-byte (never targeted).
Only the head SEO block, schema, hero, the "What It Means" lead, breadcrumb and
the FAQ are localised, plus one suburb-specific FAQ.

Run from the site root:  python3 .build/gen_suburb_reblocking.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "reblocking-restumping.html")

# (suburb, slug, council, housing-stock character sentence)
SUBURBS = [
    ("Footscray", "footscray", "Maribyrnong", "Footscray is packed with Victorian and Edwardian weatherboard cottages and workers' terraces, many never reblocked since they went up."),
    ("Yarraville", "yarraville", "Maribyrnong", "Yarraville is a tightly-held pocket of Victorian and Federation weatherboard cottages, most still sitting on their original timber stumps."),
    ("Seddon", "seddon", "Maribyrnong", "Seddon's streets are lined with period Victorian and Edwardian cottages, the kind stumped in timber when they were first built and never since."),
    ("West Footscray", "west-footscray", "Maribyrnong", "West Footscray runs from period weatherboards to solid California bungalows, plenty of them still on ageing timber stumps."),
    ("Kingsville", "kingsville", "Maribyrnong", "Kingsville is a quiet pocket of Federation and interwar weatherboard homes, many on their original stumps."),
    ("Maidstone", "maidstone", "Maribyrnong", "Maidstone mixes period weatherboards with post-war homes, and both eras were built on timber stumps that eventually give out."),
    ("Maribyrnong", "maribyrnong", "Maribyrnong", "Maribyrnong blends older weatherboard homes with newer builds, and the older stock was stumped in timber decades ago."),
    ("Braybrook", "braybrook", "Maribyrnong", "Braybrook is full of post-war weatherboard homes, a generation now old enough for the original stumps to be failing."),
    ("Williamstown", "williamstown", "Hobsons Bay", "Williamstown is one of Melbourne's oldest suburbs, full of heritage Victorian and colonial cottages that have been settling for well over a century."),
    ("Newport", "newport", "Hobsons Bay", "Newport is Federation and California-bungalow territory, street after street of weatherboard homes on ageing timber stumps."),
    ("Spotswood", "spotswood", "Hobsons Bay", "Spotswood's Victorian and Edwardian workers' cottages are classic reblocking candidates, most still on the stumps they were built on."),
    ("Altona", "altona", "Hobsons Bay", "Altona is largely post-war weatherboard and beachside cottages, a generation of homes now old enough for their stumps to be going."),
    ("Altona North", "altona-north", "Hobsons Bay", "Altona North is post-war weatherboard country, homes built in the 50s and 60s that are reaching the age where stumps fail."),
    ("South Kingsville", "south-kingsville", "Hobsons Bay", "South Kingsville is a small, tightly-held pocket of period weatherboard homes, most on their original timber stumps."),
    ("Seaholme", "seaholme", "Hobsons Bay", "Seaholme's beachside cottages sit close to the water, where damp ground is hard on timber stumps."),
    ("Laverton", "laverton", "Hobsons Bay", "Laverton's older weatherboard and post-war homes were stumped in timber and are now reaching the age where reblocking makes sense."),
    # ---- Macedon Ranges (expansion zone, shipped 2026-08-14) ----
    ("Gisborne", "gisborne", "Macedon Ranges", "Gisborne runs from older weatherboard cottages around the town centre to newer estates, and the earlier timber-stumped homes are the ones now needing work."),
    ("Woodend", "woodend", "Macedon Ranges", "Woodend's weatherboard and timber-framed homes sit in a cold, wet pocket of the Ranges, and damp ground is hard on timber stumps."),
    ("Kyneton", "kyneton", "Macedon Ranges", "Kyneton is a heritage town of Victorian-era cottages and weatherboard homes, plenty of them still on the stumps they were built on."),
    ("Romsey", "romsey", "Macedon Ranges", "Romsey mixes older weatherboard farmhouses and township cottages with newer builds, and the older timber-stumped stock is well past its first reblock."),
    ("Riddells Creek", "riddells-creek", "Macedon Ranges", "Riddells Creek runs to larger rural blocks with older timber homes and farmhouses, the kind stumped in timber and left that way for decades."),
    ("Macedon", "macedon", "Macedon Ranges", "Macedon sits on the mountain's slopes under heavy tree cover, where sloping ground and constant damp work against timber stumps."),
    ("Lancefield", "lancefield", "Macedon Ranges", "Lancefield is an old township of weatherboard cottages and farmhouses, a lot of them on their original timber stumps."),
]


def local_faq_answer(sub, council):
    if council == "Macedon Ranges":
        # Expansion zone, not the home patch - claim the service area, not a volume
        # we cannot evidence ("most weeks" is true of the inner-west, not up here).
        return (f"Yes. We cover the Macedon Ranges and {sub} is well inside our service area. "
                f"Maribyrnong &amp; Hobsons Bay Reblocking is family-owned with 35 years behind it, "
                f"and we bring the crew, the gear and the permits up with us. Free on-site "
                f"inspection, fixed written quote, and the same 15-year guarantee as every job.")
    return (f"Yes. {sub} is squarely in our patch. Maribyrnong &amp; Hobsons Bay Reblocking is "
            f"family-owned and based in Melbourne's inner-west, and we reblock and restump homes "
            f"across {sub} most weeks. Free on-site inspection, fixed written quote, and the same "
            f"15-year guarantee as every job.")


def hero_area_line(council):
    """Macedon Ranges is a shire, not a metro council area - do not say 'council area'."""
    return ("the surrounding Macedon Ranges" if council == "Macedon Ranges"
            else f"the surrounding {council} council area")


def transform(html, sub, slug, council, house):
    upper = sub.upper()
    # ---- split head / body so the URL rewrite never touches nav/footer links ----
    b = html.index("<body")
    head, body = html[:b], html[b:]

    # HEAD -----------------------------------------------------------------
    head = head.replace(
        "<title>Reblocking & Restumping Melbourne | MHB Reblocking</title>",
        f"<title>Reblocking & Restumping {sub} | MHB Reblocking</title>")
    head = head.replace(
        "Reblocking &amp; Restumping Melbourne | MHB Reblocking",
        f"Reblocking &amp; Restumping {sub} | MHB Reblocking")  # og:title + twitter:title
    head = head.replace(
        "Whole-of-house reblocking and restumping across Melbourne. Concrete stumps only, computer-levelled, all permits supplied, 15-year written guarantee.",
        f"Whole-of-house reblocking and restumping in {sub}. Concrete stumps only, computer-levelled, all permits supplied, 15-year written guarantee.")  # meta/og/twitter desc
    head = head.replace("reblocking-restumping.html", f"reblocking-restumping-{slug}.html")  # canonical/og:url/schema (head only)
    head = head.replace('content="Melbourne, Victoria"', f'content="{sub}, Victoria"')  # geo.placename
    head = head.replace('"name": "Reblocking & Restumping"', f'"name": "Reblocking & Restumping {sub}"')  # Service + Breadcrumb schema
    head = head.replace(
        "weatherboard and timber-frame homes across Melbourne. Computer-levelled",
        f"weatherboard and timber-frame homes in {sub}. Computer-levelled")  # Service schema description
    head = head.replace('"name": "Melbourne"', f'"name": "{sub}"')  # Service areaServed city

    # local FAQ into the FAQPage schema (as the first mainEntity item)
    local_q_schema = (
        '{\n'
        '      "@type": "Question",\n'
        f'      "name": "Do you service {sub}?",\n'
        '      "acceptedAnswer": {\n'
        '        "@type": "Answer",\n'
        f'        "text": "{local_faq_answer(sub, council).replace("&amp;", "&")}"\n'
        '      }\n'
        '    }')
    head = head.replace('"mainEntity": [\n    {', '"mainEntity": [\n    ' + local_q_schema + ',\n    {', 1)

    # BODY -----------------------------------------------------------------
    body = body.replace("SERVICING ALL OF MELBOURNE", f"SERVICING {upper} &amp; SURROUNDS")
    body = body.replace("Reblocking & restumping,<br/>", f"Reblocking & restumping in {sub},<br/>")
    body = body.replace(
        "across Maribyrnong, Hobsons Bay and greater Melbourne.",
        f"in {sub} and {hero_area_line(council)}.")
    body = body.replace(
        "On a typical Melbourne weatherboard, those supports are",
        f"{house} On a typical one, those supports are")
    body = body.replace(
        'text-brand-charcoal/85">Reblocking & Restumping</span>',
        f'text-brand-charcoal/85">Reblocking & Restumping {sub}</span>')  # breadcrumb visible

    # local FAQ into the visible list (first item)
    local_details = (
        '<details class="py-6 group">\n'
        '        <summary class="flex items-start justify-between gap-6">\n'
        f'          <h3 class="display text-[19px] lg:text-[22px] tracking-tight">Do you service {sub}?</h3>\n'
        '          <div class="flex-shrink-0 mt-2"><div class="faq-indicator h-1 w-6 bg-brand-orange"></div></div>\n'
        '        </summary>\n'
        f'        <p class="mt-4 text-[15.5px] text-brand-charcoal/72 leading-[1.8] max-w-3xl">{local_faq_answer(sub, council)}</p>\n'
        '      </details>\n'
        '      ')
    body = body.replace('<details class="py-6 group">', local_details + '<details class="py-6 group">', 1)

    return head + body


def main():
    with open(SRC, encoding="utf-8") as fh:
        src = fh.read()
    for sub, slug, council, house in SUBURBS:
        out = transform(src, sub, slug, council, house)
        # guards
        assert f"reblocking-restumping-{slug}.html" in out, f"{slug}: self URL missing"
        assert out.count("reblocking-restumping.html") >= 3, f"{slug}: nav/footer links lost"
        assert "SUTERA_LEAD_EVENTS" in out and "G-M67WRZBS53" in out, f"{slug}: tracking dropped"
        assert f"Do you service {sub}?" in out, f"{slug}: local FAQ missing"
        dst = os.path.join(ROOT, f"reblocking-restumping-{slug}.html")
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"  wrote reblocking-restumping-{slug}.html  ({len(out)} bytes)")
    print(f"Done. {len(SUBURBS)} suburb pages.")


if __name__ == "__main__":
    main()
