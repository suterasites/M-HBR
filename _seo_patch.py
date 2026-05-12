"""
MHB Reblocking - 2026-05-12 SEO patch.

Adds the gaps surfaced in the verification audit on top of the 2026-05-04 base injection:
- og:image:alt on every page (was missing from all 9)
- geo.region / geo.placename / geo.position / ICBM on every page
- sitemap.xml lastmod bumped (or added) to today

Idempotent. Wraps additions in OG_GEO_PATCH markers.
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent
TODAY = date(2026, 5, 12).isoformat()

PAGES = [
    "index.html",
    "about.html",
    "contact.html",
    "gallery.html",
    "reblocking-restumping.html",
    "underpinning.html",
    "levelling-lifting.html",
    "stump-conversion.html",
    "stabilising-strengthening.html",
]

# H1 / page-specific OG image alt fallbacks
OG_IMAGE_ALT = "Maribyrnong & Hobsons Bay Reblocking - family-owned Melbourne reblocking and restumping"

PATCH_START = "<!-- OG_GEO_PATCH_START -->"
PATCH_END = "<!-- OG_GEO_PATCH_END -->"


def strip_block(html, start, end):
    pat = re.escape(start) + r".*?" + re.escape(end) + r"\n?"
    return re.sub(pat, "", html, flags=re.DOTALL)


def patch_page(path: Path):
    html = path.read_text(encoding="utf-8")
    html = strip_block(html, PATCH_START, PATCH_END)

    block = f"""{PATCH_START}
  <meta property="og:image:alt" content="{OG_IMAGE_ALT}">
  <meta name="twitter:image:alt" content="{OG_IMAGE_ALT}">
  <meta name="geo.region" content="AU-VIC">
  <meta name="geo.placename" content="Melbourne, Victoria">
  <meta name="geo.position" content="-37.7969;144.8907">
  <meta name="ICBM" content="-37.7969, 144.8907">
  {PATCH_END}
"""
    # Insert after the OG_TWITTER_END marker if present, else before </head>
    if "<!-- OG_TWITTER_END -->" in html:
        html = html.replace(
            "<!-- OG_TWITTER_END -->",
            "<!-- OG_TWITTER_END -->\n  " + block.strip() + "\n",
            1,
        )
    else:
        html = html.replace("</head>", "  " + block + "</head>", 1)

    path.write_text(html, encoding="utf-8")
    print(f"OK  {path.name}")


def patch_sitemap():
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    # Add or update <lastmod>YYYY-MM-DD</lastmod> after each <loc>
    def inject(match):
        loc = match.group(0)
        return loc + f"\n    <lastmod>{TODAY}</lastmod>"
    text = re.sub(r"<lastmod>[^<]*</lastmod>\n?\s*", "", text)
    text = re.sub(r"<loc>[^<]+</loc>", inject, text)
    sm.write_text(text, encoding="utf-8")
    print(f"OK  sitemap.xml lastmod={TODAY}")


def main():
    for f in PAGES:
        p = ROOT / f
        if not p.exists():
            print(f"SKIP {f} (missing)")
            continue
        patch_page(p)
    patch_sitemap()


if __name__ == "__main__":
    main()
