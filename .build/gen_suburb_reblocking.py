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

# (suburb, slug, council, housing-stock, ground-conditions, site-access)
#
# The ground sentence is the real differentiator. Reactive basalt clay in the inner
# west, a high water table on the bay side and a long wet winter up in the Ranges are
# genuinely different failure modes for a timber stump - not one paragraph with the
# suburb name swapped. Added 2026-09-02 after Google indexed 7 of 22 of these pages
# and rejected the rest: normalise the suburb name and only 8 lines differed across a
# 1,130-word page, which is a doorway-page footprint however good the copy is.
#
# Nothing here claims a job we cannot evidence. It describes the GROUND, which is a
# matter of public geology, and the on-site inspection is what speaks to the property.
#
# Site access is the second real differentiator and it is not decoration: whether a
# machine fits down the side decides if the dig is machine or hand work, which is a
# genuine price and duration difference. A Yarraville terrace and an Altona North
# post-war block are different jobs, and saying so is more useful than repeating the
# same paragraph with the suburb swapped.
SUBURBS = [
    ("Footscray", "footscray", "Maribyrnong", "Footscray is packed with Victorian and Edwardian weatherboard cottages and workers' terraces, many never reblocked since they went up.",
     "Footscray sits on the western basalt plain, and the reactive clay beneath it swells through winter then shrinks back over summer. Timber stumps ride that movement up and down until floors slope and the plaster starts cracking at the cornice.",
     "Footscray's older streets are tight, with narrow frontages and cars parked both sides. On a lot of these cottages there is no side access wide enough for a machine, so the dig is done by hand and the spoil carried out the front."),
    ("Yarraville", "yarraville", "Maribyrnong", "Yarraville is a tightly-held pocket of Victorian and Federation weatherboard cottages, most still sitting on their original timber stumps.",
     "The ground through Yarraville is the same reactive western-suburbs clay, moving with every wet and dry season. On a house still on its original stumps, that seasonal lift and drop is usually what has pulled the floors out of level.",
     "Most Yarraville cottages sit on narrow blocks with a metre or less down the side. That rules out machinery, so the excavation is hand-dug and the soil barrowed out, which we price in rather than discovering on the day."),
    ("Seddon", "seddon", "Maribyrnong", "Seddon's streets are lined with period Victorian and Edwardian cottages, the kind stumped in timber when they were first built and never since.",
     "Seddon's clay subsoil holds water through winter and pulls away from the stumps as it dries out. Decades of that cycle is enough to rot timber at the ground line and leave the footings carrying the house unevenly.",
     "Seddon's terraces and semi-detached cottages often share a boundary on one side, leaving a single narrow path to work through. We plan the sequence around that so the house is never left unsupported longer than it needs to be."),
    ("West Footscray", "west-footscray", "Maribyrnong", "West Footscray runs from period weatherboards to solid California bungalows, plenty of them still on ageing timber stumps.",
     "West Footscray sits on reactive clay that shifts noticeably between seasons. Older timber stumps have no way to resist it, so the movement shows up as doors that stick through winter and swing free by February.",
     "West Footscray blocks are generally wider than the terrace streets closer in, and many have a driveway down one side. Where a machine can get through, the dig is quicker and the job is cheaper."),
    ("Kingsville", "kingsville", "Maribyrnong", "Kingsville is a quiet pocket of Federation and interwar weatherboard homes, many on their original stumps.",
     "Under Kingsville's weatherboards is the same shrink-swell clay found across the inner west. It works timber stumps loose over time, and a loose stump stops carrying its share of the load long before anything looks wrong.",
     "Kingsville's Federation and interwar homes usually have a usable side path, though not always wide enough for machinery. We work out which it is at the inspection, because it changes the quote."),
    ("Maidstone", "maidstone", "Maribyrnong", "Maidstone mixes period weatherboards with post-war homes, and both eras were built on timber stumps that eventually give out.",
     "Maidstone's ground is reactive clay over basalt, expanding when wet and contracting hard through a dry summer. Timber stumps sitting directly in that soil move with it and rot from the base up.",
     "Maidstone's post-war blocks tend to be wider with proper driveways, which usually means machine access to the subfloor and a faster job than the terrace streets closer to the city."),
    ("Maribyrnong", "maribyrnong", "Maribyrnong", "Maribyrnong blends older weatherboard homes with newer builds, and the older stock was stumped in timber decades ago.",
     "Close to the river, Maribyrnong's soils hold moisture longer than the clay further inland, and damp ground is what finishes a timber stump. Uneven moisture across a block also means the house settles unevenly.",
     "Blocks around Maribyrnong vary from tight period cottages to newer builds with proper driveways. Access is the first thing we assess, because it decides whether the dig is done by machine or by hand."),
    ("Braybrook", "braybrook", "Maribyrnong", "Braybrook is full of post-war weatherboard homes, a generation now old enough for the original stumps to be failing.",
     "Braybrook sits on the western basalt plain with reactive clay beneath, so the ground lifts and drops with the seasons. Post-war stumps were never meant for sixty years of that, and it shows up in the floors.",
     "Braybrook's post-war homes generally sit on wider blocks with driveways, so machinery can usually reach the subfloor. That keeps the excavation quicker and the disruption shorter."),
    ("Williamstown", "williamstown", "Hobsons Bay", "Williamstown is one of Melbourne's oldest suburbs, full of heritage Victorian and colonial cottages that have been settling for well over a century.",
     "Williamstown is low-lying and close to the bay, with a high water table and pockets of filled ground through the older streets. Timber stumps standing in damp soil rot at the ground line, and on houses this age they have been doing it a long time.",
     "Williamstown's heritage streets are narrow and parking is tight, and many of the older cottages have no side access at all. Hand excavation and a carefully staged setup are usually the only way in."),
    ("Newport", "newport", "Hobsons Bay", "Newport is Federation and California-bungalow territory, street after street of weatherboard homes on ageing timber stumps.",
     "Newport's ground sits low and drains slowly, so the soil around a stump stays wet well into spring. Constant damp is the fastest way to lose a timber stump, and it takes the level of the floor with it.",
     "Newport's Federation homes and bungalows mostly have a side path, though width varies street to street. Where a machine fits the job moves faster, and where it does not we dig by hand."),
    ("Spotswood", "spotswood", "Hobsons Bay", "Spotswood's Victorian and Edwardian workers' cottages are classic reblocking candidates, most still on the stumps they were built on.",
     "Parts of Spotswood are built on made ground near the river flats, where fill settles unevenly over decades. Add a high water table and timber stumps have both movement and moisture working against them.",
     "Spotswood's workers' cottages sit close together on narrow blocks, often with no gap wide enough for machinery. The dig is done by hand and the spoil carted out, which we allow for in the quote."),
    ("Altona", "altona", "Hobsons Bay", "Altona is largely post-war weatherboard and beachside cottages, a generation of homes now old enough for their stumps to be going.",
     "Altona is flat, sandy and close to the water, with a water table that sits high through winter. Sand gives a timber stump very little lateral support, and the damp finishes the job from below.",
     "Altona's post-war blocks are generally generous, with driveways and proper side access. That usually means machinery can get to the subfloor, which shortens the job."),
    ("Altona North", "altona-north", "Hobsons Bay", "Altona North is post-war weatherboard country, homes built in the 50s and 60s that are reaching the age where stumps fail.",
     "The ground through Altona North is sandy over clay and holds water after heavy rain. Stumps put in during the post-war build have spent decades in soil that stays wet for months at a time.",
     "Altona North's 50s and 60s homes sit on wide blocks with driveways, so access is rarely the constraint here. The dig is usually machine work and the crew can move quickly."),
    ("South Kingsville", "south-kingsville", "Hobsons Bay", "South Kingsville is a small, tightly-held pocket of period weatherboard homes, most on their original timber stumps.",
     "South Kingsville sits between the clay of the inner west and the sandier ground closer to the bay. That mix means different parts of the same block can move at different rates, which is why the floors rarely drop evenly.",
     "South Kingsville's period cottages sit on tighter blocks than the newer streets around them, so side access is often too narrow for a machine and the excavation is done by hand."),
    ("Seaholme", "seaholme", "Hobsons Bay", "Seaholme's beachside cottages sit close to the water, where damp ground is hard on timber stumps.",
     "Seaholme is as close to the water as this service area gets, and the water table stays high year-round. Timber stumps in permanently damp sand do not last, which is why so many homes here are already on their second set.",
     "Seaholme's beachside homes mostly have workable side access, though sandy ground means the excavation needs shoring as it goes rather than being left open."),
    ("Laverton", "laverton", "Hobsons Bay", "Laverton's older weatherboard and post-war homes were stumped in timber and are now reaching the age where reblocking makes sense.",
     "Laverton's flat, low-lying ground drains slowly and holds water through winter. Timber stumps standing in that for decades rot at the ground line long before anything is visible from inside the house.",
     "Laverton's older and post-war homes generally sit on wider blocks with driveways, so machinery can usually reach the subfloor and the dig is quicker than the inner-west terraces."),
    # ---- Macedon Ranges (expansion zone, shipped 2026-08-14) ----
    ("Gisborne", "gisborne", "Macedon Ranges", "Gisborne runs from older weatherboard cottages around the town centre to newer estates, and the earlier timber-stumped homes are the ones now needing work.",
     "Gisborne sits higher and colder than the Melbourne suburbs, with a longer wet season and ground that stays damp well into spring. Timber stumps in soil that never fully dries out have a short working life.",
     "Gisborne blocks are larger than the metro suburbs and access is rarely the problem. Getting the crew and gear up from the inner west is the part we plan around, and we bring everything needed for the whole job in one trip."),
    ("Woodend", "woodend", "Macedon Ranges", "Woodend's weatherboard and timber-framed homes sit in a cold, wet pocket of the Ranges, and damp ground is hard on timber stumps.",
     "Woodend takes considerably more rain than the metro suburbs and holds it in the soil. Persistent damp around a stump is what rots it, and on older weatherboards up here it is usually well advanced before anyone notices.",
     "Woodend properties tend to sit on generous blocks with room to work, though wet ground through winter can make access harder for machinery than the block size suggests."),
    ("Kyneton", "kyneton", "Macedon Ranges", "Kyneton is a heritage town of Victorian-era cottages and weatherboard homes, plenty of them still on the stumps they were built on.",
     "Kyneton's older cottages sit on ground that stays wet through a long Ranges winter then dries hard in summer. That cycle works timber stumps loose and rots them at the same time.",
     "Kyneton's township cottages sit on older, narrower allotments than the surrounding farmland, so access varies sharply between the heritage streets and the newer edges of town."),
    ("Romsey", "romsey", "Macedon Ranges", "Romsey mixes older weatherboard farmhouses and township cottages with newer builds, and the older timber-stumped stock is well past its first reblock.",
     "Around Romsey the blocks are larger and the ground drains unevenly, so one corner of a house can sit in wet soil while another stays dry. Uneven moisture is what produces uneven settlement.",
     "Romsey's larger blocks and farmhouses give plenty of room to work, and we bring the machinery up rather than hiring locally, so the job runs to the same schedule as one in the inner west."),
    ("Riddells Creek", "riddells-creek", "Macedon Ranges", "Riddells Creek runs to larger rural blocks with older timber homes and farmhouses, the kind stumped in timber and left that way for decades.",
     "Riddells Creek runs to bigger rural blocks where drainage varies across a single property. A house can be close to level at one end and well down at the other, purely because of what the ground is doing underneath.",
     "Riddells Creek's rural blocks have space to work, but long driveways and soft ground after rain are worth checking before the machinery comes up. We assess that at the inspection."),
    ("Macedon", "macedon", "Macedon Ranges", "Macedon sits on the mountain's slopes under heavy tree cover, where sloping ground and constant damp work against timber stumps.",
     "Macedon sits on the mountain's slopes under heavy tree cover, where the ground holds damp almost year-round and sloping sites push water against one side of a house. Both are hard on timber stumps.",
     "Macedon's sloping, tree-covered blocks are the hardest access in our service area. Machinery cannot always get around the house, and the fall across a site changes how the levelling is set out."),
    ("Lancefield", "lancefield", "Macedon Ranges", "Lancefield is an old township of weatherboard cottages and farmhouses, a lot of them on their original timber stumps.",
     "Lancefield's township cottages and farmhouses sit on ground that stays wet through winter and dries hard in summer. Timber stumps caught between the two rot at the base and shift as the soil moves.",
     "Lancefield's township cottages and surrounding farmhouses generally have room to work, and the larger blocks mean the crew and gear can set up close to the house."),
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


# Parts of these suburbs sit inside a heritage overlay, which adds a planning step
# before the building permit. Kept to precincts that are well documented rather than
# assumed from the age of the housing - claiming an overlay that does not exist would
# be worse than saying nothing.
HERITAGE = {"Williamstown", "Yarraville", "Seddon", "Footscray", "Spotswood", "Kyneton"}

FULL_COUNCIL = {
    "Maribyrnong": "Maribyrnong City Council",
    "Hobsons Bay": "Hobsons Bay City Council",
    "Macedon Ranges": "Macedon Ranges Shire Council",
}


def permit_answer(sub, council):
    """Reblocking is structural, so it needs a building permit. In Victoria that is
    issued by a registered building surveyor, NOT over the counter at the council -
    getting that backwards is the single most common misunderstanding on these calls."""
    base = (f"Yes. Reblocking is structural work, so it needs a building permit before we "
            f"start. In Victoria that permit is issued by a registered building surveyor "
            f"rather than over the counter at {FULL_COUNCIL[council]}, and we arrange it as "
            f"part of the job - it is in the quoted price, not billed on top.")
    if sub in HERITAGE:
        base += (f" Parts of {sub} also sit inside a heritage overlay, which can add a "
                 f"planning step through {FULL_COUNCIL[council]} before the building permit "
                 f"is issued. We check that at the inspection so it does not surface "
                 f"halfway through the job.")
    return base


def hero_area_line(council):
    """Macedon Ranges is a shire, not a metro council area - do not say 'council area'."""
    return ("the surrounding Macedon Ranges" if council == "Macedon Ranges"
            else f"the surrounding {council} council area")


def transform(html, sub, slug, council, house, ground, access):
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
    permit_q_schema = (
        '{\n'
        '      "@type": "Question",\n'
        f'      "name": "Do I need a permit to reblock in {sub}?",\n'
        '      "acceptedAnswer": {\n'
        '        "@type": "Answer",\n'
        f'        "text": "{permit_answer(sub, council)}"\n'
        '      }\n'
        '    }')
    head = head.replace('"mainEntity": [\n    {',
                        '"mainEntity": [\n    ' + local_q_schema + ',\n    '
                        + permit_q_schema + ',\n    {', 1)

    # BODY -----------------------------------------------------------------
    body = body.replace("SERVICING ALL OF MELBOURNE", f"SERVICING {upper} &amp; SURROUNDS")
    body = body.replace("Reblocking & restumping,<br/>", f"Reblocking & restumping in {sub},<br/>")
    body = body.replace(
        "across Maribyrnong, Hobsons Bay and greater Melbourne.",
        f"in {sub} and {hero_area_line(council)}.")
    body = body.replace(
        "On a typical Melbourne weatherboard, those supports are",
        f"{house} On a typical one, those supports are")
    # Ground conditions - the suburb-specific reason stumps fail here, dropped in as its
    # own paragraph rather than bolted onto the shared one, so it reads as content and
    # not as a keyword line.
    ground_para = (
        '<p class="mt-5 text-[17px] text-brand-charcoal/75 leading-[1.85]">\n'
        f'        <strong class="text-brand-charcoal">The ground under {sub}.</strong> {ground} '
        'Every house is different, which is why the inspection happens on site and not over the phone.\n'
        '      </p>\n'
        '      <p class="mt-5 text-[17px] text-brand-charcoal/75 leading-[1.85]">\n'
        f'        <strong class="text-brand-charcoal">Getting to the job in {sub}.</strong> {access}\n'
        '      </p>\n'
        '      ')
    anchor = '<div class="mt-8 grid sm:grid-cols-2 gap-4">'
    assert anchor in body, "ground-paragraph anchor missing"
    body = body.replace(anchor, ground_para + anchor, 1)

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
    permit_details = (
        '<details class="py-6 group">\n'
        '        <summary class="flex items-start justify-between gap-6">\n'
        f'          <h3 class="display text-[19px] lg:text-[22px] tracking-tight">Do I need a permit to reblock in {sub}?</h3>\n'
        '          <div class="flex-shrink-0 mt-2"><div class="faq-indicator h-1 w-6 bg-brand-orange"></div></div>\n'
        '        </summary>\n'
        f'        <p class="mt-4 text-[15.5px] text-brand-charcoal/72 leading-[1.8] max-w-3xl">{permit_answer(sub, council)}</p>\n'
        '      </details>\n'
        '      ')
    body = body.replace('<details class="py-6 group">',
                        local_details + permit_details + '<details class="py-6 group">', 1)

    return head + body


def main():
    with open(SRC, encoding="utf-8") as fh:
        src = fh.read()
    for sub, slug, council, house, ground, access in SUBURBS:
        out = transform(src, sub, slug, council, house, ground, access)
        # guards
        assert f"reblocking-restumping-{slug}.html" in out, f"{slug}: self URL missing"
        assert out.count("reblocking-restumping.html") >= 3, f"{slug}: nav/footer links lost"
        assert "SUTERA_LEAD_EVENTS" in out and "G-M67WRZBS53" in out, f"{slug}: tracking dropped"
        assert f"Do you service {sub}?" in out, f"{slug}: local FAQ missing"
        assert f"Do I need a permit to reblock in {sub}?" in out, f"{slug}: permit FAQ missing"
        assert ground[:40] in out, f"{slug}: ground paragraph missing"
        assert access[:40] in out, f"{slug}: access paragraph missing"
        dst = os.path.join(ROOT, f"reblocking-restumping-{slug}.html")
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"  wrote reblocking-restumping-{slug}.html  ({len(out)} bytes)")
    print(f"Done. {len(SUBURBS)} suburb pages.")


if __name__ == "__main__":
    main()
