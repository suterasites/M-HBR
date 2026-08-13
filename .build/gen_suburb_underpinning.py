#!/usr/bin/env python3
"""
Generate per-suburb Underpinning pages by cloning the canonical underpinning.html
and localising it to a suburb. Deterministic + idempotent: nav, footer, mobile
menu, scripts, GA4 + SUTERA_LEAD_EVENTS and the shared "Areas We Service" section
are preserved byte-for-byte (never targeted). Only the head SEO block, schema,
hero, the "What It Means" lead, breadcrumb and the FAQ are localised, plus one
suburb-specific ground/housing-stock sentence and one suburb FAQ.

Sibling of gen_suburb_reblocking.py, same contract.

Run from the site root:  python3 .build/gen_suburb_underpinning.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "underpinning.html")

# (suburb, slug, region, ground/housing-stock character sentence)
# region drives the hero sub-line and which local-FAQ answer is used.
SUBURBS = [
    # ---- Maribyrnong council ----
    ("Footscray", "footscray", "Maribyrnong",
     "Footscray sits on reactive basalt clay, and its Victorian brick terraces, shop-top dwellings and later brick-veneer extensions are the stock that shows subsidence cracking first."),
    ("Yarraville", "yarraville", "Maribyrnong",
     "Yarraville's double-fronted brick homes and rear brick extensions sit on the same reactive clay that shrinks hard through a dry summer and swells again over winter."),
    ("Seddon", "seddon", "Maribyrnong",
     "Seddon's brick and part-brick period homes were built on shallow original footings, and the mature street trees through the area pull moisture straight out of the clay around them."),
    ("West Footscray", "west-footscray", "Maribyrnong",
     "West Footscray runs heavy to solid brick and brick-veneer homes from the interwar and post-war years, most on strip footings that were never designed for clay this reactive."),
    ("Kingsville", "kingsville", "Maribyrnong",
     "Kingsville's brick-veneer and full-brick homes sit on reactive clay, and the ones carrying a later rear extension often start moving at the join between old and new footings."),
    ("Maidstone", "maidstone", "Maribyrnong",
     "Maidstone mixes post-war brick homes with newer slab-on-ground builds and townhouses, and both crack the same way when the clay under one corner dries out."),
    ("Maribyrnong", "maribyrnong", "Maribyrnong",
     "Maribyrnong blends older brick homes with newer slab-on-ground builds close to the river flats, where ground conditions can change over a short distance."),
    ("Braybrook", "braybrook", "Maribyrnong",
     "Braybrook is post-war brick and brick-veneer country on reactive basalt clay, an era of shallow footings now old enough to be moving."),
    # ---- Hobsons Bay council ----
    ("Williamstown", "williamstown", "Hobsons Bay",
     "Williamstown is one of Melbourne's oldest suburbs, full of bluestone and solid-brick homes sitting on original footings that have been settling for well over a century."),
    ("Newport", "newport", "Hobsons Bay",
     "Newport's Federation and interwar brick homes sit on reactive clay, and the older ones carry shallow footings with big trees close to the walls."),
    ("Spotswood", "spotswood", "Hobsons Bay",
     "Spotswood's brick cottages and industrial-era housing sit on made and variable ground in parts, which is exactly where localised footing movement shows up."),
    ("Altona", "altona", "Hobsons Bay",
     "Altona is low-lying and close to the bay, with sandy topsoil over clay and a high water table, so ground moisture is the main driver of footing movement here."),
    ("Altona North", "altona-north", "Hobsons Bay",
     "Altona North is post-war brick-veneer country on reactive clay, homes built in the 50s and 60s whose original strip footings are now at the age where movement starts."),
    ("South Kingsville", "south-kingsville", "Hobsons Bay",
     "South Kingsville is a small, tightly-held pocket of period and post-war homes, many of them part-brick, on the same reactive clay that runs right through the inner-west."),
    ("Seaholme", "seaholme", "Hobsons Bay",
     "Seaholme sits on the coastal flats, where sandy ground over clay and a high water table are hard on shallow footings."),
    ("Laverton", "laverton", "Hobsons Bay",
     "Laverton's post-war brick homes and newer slab-on-ground estates sit out on the basalt plain, where clay movement through a dry summer is the usual cause of cracking."),
    # ---- Macedon Ranges ----
    ("Gisborne", "gisborne", "Macedon Ranges",
     "Gisborne mixes older brick and weatherboard homes with newer slab-on-ground estates, on ground that swings between heavy basalt clay and lighter granitic soils across the town."),
    ("Woodend", "woodend", "Macedon Ranges",
     "Woodend's period brick homes and newer builds sit among established gardens and big trees, and those root systems draw moisture out of the ground right beside the footings."),
    ("Kyneton", "kyneton", "Macedon Ranges",
     "Kyneton carries a large stock of heritage bluestone and solid-brick buildings on original shallow footings, the kind that show stair-step cracking as soon as the ground moves."),
    ("Romsey", "romsey", "Macedon Ranges",
     "Romsey's older brick homes and newer slab-on-ground builds sit on volcanic plains soils that shrink and swell hard between the seasons."),
    ("Riddells Creek", "riddells-creek", "Macedon Ranges",
     "Riddells Creek runs to larger blocks with established trees, and localised drying around one section of footing is a common cause of cracking on the older brick homes."),
    ("Macedon", "macedon", "Macedon Ranges",
     "Macedon sits on the mountain's slopes under heavy tree cover, where sloping ground and constant moisture change are both hard on original footings."),
    ("Lancefield", "lancefield", "Macedon Ranges",
     "Lancefield's older brick and bluestone buildings sit on reactive plains soils, on shallow original footings that move as the ground dries out."),
]


def local_faq_answer(sub, region):
    if region == "Macedon Ranges":
        return (f"Yes. We work right across the Macedon Ranges and {sub} is well inside our service "
                f"area. Maribyrnong &amp; Hobsons Bay Reblocking is family-owned with 35 years behind "
                f"it, and we bring the engineer, the permit and the crew with us. Free on-site "
                f"inspection, fixed written quote, and the same 15-year guarantee as every job.")
    return (f"Yes. {sub} is right in our home patch. Maribyrnong &amp; Hobsons Bay Reblocking is "
            f"family-owned and based in Melbourne's inner-west, and underpinning is one of our core "
            f"trades. Free on-site inspection, engineer-designed piers, fixed written quote, and the "
            f"same 15-year guarantee as every job.")


def hero_area_line(region):
    return ("the surrounding Macedon Ranges" if region == "Macedon Ranges"
            else f"the surrounding {region} council area")


def transform(html, sub, slug, region, ground):
    upper = sub.upper()
    # ---- split head / body so the URL rewrite never touches nav/footer links ----
    b = html.index("<body")
    head, body = html[:b], html[b:]

    # HEAD -----------------------------------------------------------------
    head = head.replace(
        "<title>Underpinning Melbourne | MHB Reblocking & Restumping</title>",
        f"<title>Underpinning {sub} | MHB Reblocking</title>")
    head = head.replace(
        "Underpinning Melbourne | MHB Reblocking &amp; Restumping",
        f"Underpinning {sub} | MHB Reblocking")  # og:title + twitter:title
    head = head.replace(
        "Engineered underpinning for brick, slab and double-storey Melbourne homes. Permitted, signed off, 15-year written guarantee on every job.",
        f"Engineered underpinning for brick, slab and double-storey homes in {sub}. Permitted, signed off, 15-year written guarantee on every job.")  # meta/og/twitter desc
    head = head.replace("underpinning.html", f"underpinning-{slug}.html")  # canonical/og:url/schema (head only)
    head = head.replace('content="Melbourne, Victoria"', f'content="{sub}, Victoria"')  # geo.placename
    head = head.replace('"name": "Underpinning"', f'"name": "Underpinning {sub}"')  # Service + Breadcrumb schema
    head = head.replace(
        "Engineered underpinning for brick, slab and double-storey Melbourne homes. Mass concrete piers",
        f"Engineered underpinning for brick, slab and double-storey homes in {sub}. Mass concrete piers")  # Service schema description
    head = head.replace('"name": "Melbourne"', f'"name": "{sub}"')  # Service areaServed city

    # local FAQ into the FAQPage schema (as the first mainEntity item)
    local_q_schema = (
        '{\n'
        '      "@type": "Question",\n'
        f'      "name": "Do you underpin homes in {sub}?",\n'
        '      "acceptedAnswer": {\n'
        '        "@type": "Answer",\n'
        f'        "text": "{local_faq_answer(sub, region).replace("&amp;", "&")}"\n'
        '      }\n'
        '    }')
    head = head.replace('"mainEntity": [\n    {', '"mainEntity": [\n    ' + local_q_schema + ',\n    {', 1)

    # BODY -----------------------------------------------------------------
    body = body.replace("SERVICING ALL OF MELBOURNE", f"SERVICING {upper} &amp; SURROUNDS")
    body = body.replace(
        "          Underpinning that<br/>\n          <span class=\"text-brand-orange\">stops the house moving.</span>",
        f"          Underpinning in {sub}<br/>\n          <span class=\"text-brand-orange\">that stops the house moving.</span>")
    body = body.replace(
        "Engineered underpinning for brick, slab and double-storey homes that have started\n          to subside.",
        f"Engineered underpinning for brick, slab and double-storey homes in {sub} and\n          {hero_area_line(region)} that have started to subside.")
    body = body.replace(
        "        Underpinning fixes that from below.",
        f"        {ground} Underpinning fixes that from below.")
    body = body.replace(
        'text-brand-charcoal/85">Underpinning</span>',
        f'text-brand-charcoal/85">Underpinning {sub}</span>')  # breadcrumb visible

    # local FAQ into the visible list (first item)
    local_details = (
        '<details class="py-6 group">\n'
        '        <summary class="flex items-start justify-between gap-6">\n'
        f'          <h3 class="display text-[19px] lg:text-[22px] tracking-tight">Do you underpin homes in {sub}?</h3>\n'
        '          <div class="flex-shrink-0 mt-2"><div class="faq-indicator h-1 w-6 bg-brand-orange"></div></div>\n'
        '        </summary>\n'
        f'        <p class="mt-4 text-[15.5px] text-brand-charcoal/72 leading-[1.8] max-w-3xl">{local_faq_answer(sub, region)}</p>\n'
        '      </details>\n'
        '      ')
    body = body.replace('<details class="py-6 group">', local_details + '<details class="py-6 group">', 1)

    return head + body


def main():
    with open(SRC, encoding="utf-8") as fh:
        src = fh.read()
    for sub, slug, region, ground in SUBURBS:
        out = transform(src, sub, slug, region, ground)
        # guards
        assert f"underpinning-{slug}.html" in out, f"{slug}: self URL missing"
        assert out.count('href="underpinning.html"') >= 3, f"{slug}: nav/footer links lost"
        assert "SUTERA_LEAD_EVENTS" in out and "G-M67WRZBS53" in out, f"{slug}: tracking dropped"
        assert f"Do you underpin homes in {sub}?" in out, f"{slug}: local FAQ missing"
        assert f"Underpinning in {sub}<br/>" in out, f"{slug}: hero H1 not localised"
        assert ground in out, f"{slug}: local ground sentence missing"
        assert "AREAS WE SERVICE" in out, f"{slug}: areas section lost"
        assert "Underpinning Melbourne" not in out, f"{slug}: stale Melbourne title left behind"
        dst = os.path.join(ROOT, f"underpinning-{slug}.html")
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"  wrote underpinning-{slug}.html  ({len(out)} bytes)")
    print(f"Done. {len(SUBURBS)} suburb pages.")


if __name__ == "__main__":
    main()
