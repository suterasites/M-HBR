#!/usr/bin/env python3
"""
clean_url_links.py - point every internal reference at the URL the host actually
serves, instead of the one that 308-redirects to it.

WHY. As of 2026-09-15 Google had still not re-crawled the two reblocking suburb
pages it excluded as alternates of the hub (Williamstown, South Kingsville), four
days after 65b28c4 made all 23 suburb pages self-canonical. Of the 18 reblocking
pages inspected, 16 were "Discovered - currently not indexed" or unknown, the hub
among them. The canonicals and sitemap were already clean (8b71a14), but every
internal link, every og:url and every BreadcrumbList item still named the `.html`
form, and Cloudflare Pages 308s `.html` to the extension-less URL. So the only path
Google had into a suburb page was a redirect, from a hub it has never crawled, and
the clean URL the canonical nominates was linked from nowhere. Same defect and same
fix as TJM Detailing 2bbb832 (2026-09-03).

WHAT IT REWRITES, in the root *.html pages and nothing else:

    href="page.html"            -> href="/page"             (index.html -> "/")
    href="page.html#frag"       -> href="/page#frag"        (index.html#services -> "/#services")
    https://www.mhbreblocking.com/page.html  -> the clean URL (og:url, JSON-LD url/item)

Every `.html` reference in the root pages is internal and flat, with at most a
fragment (checked before writing this: 3,196 bare, 162 index.html#services, 115
stabilising-strengthening.html#verandahs, 165 absolute). The two Google Ads quote
pages in reblocking-quote/ and restumping-quote/ are deliberately out of scope:
they are noindex and carry a Formspree redirect this must not touch.

Idempotent - a second run finds nothing to do. Dry run by default, --apply writes.
"""

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.mhbreblocking.com"

# href="slug.html", href="/slug.html", href="slug.html#frag" -> href="/slug[#frag]"
HREF = re.compile(r'(href\s*=\s*")(?:\./)?/?([A-Za-z0-9._-]+)\.html((?:#[^"]*)?")')
# Absolute self-referencing URLs inside content="" and JSON-LD "url"/"item".
ABS = re.compile(r'(' + re.escape(DOMAIN) + r'/)([A-Za-z0-9._-]+)\.html\b')


def clean_href(m):
    slug = m.group(2)
    return m.group(1) + ("/" if slug == "index" else "/" + slug) + m.group(3)


def clean_abs(m):
    slug = m.group(2)
    return m.group(1) + ("" if slug == "index" else slug)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total = 0
    touched = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        txt = open(path, encoding="utf-8").read()
        new, n1 = HREF.subn(clean_href, txt)
        new, n2 = ABS.subn(clean_abs, new)
        n = n1 + n2
        if not n:
            continue
        touched += 1
        total += n
        print("  %-46s %4d  (%d href, %d absolute)"
              % (os.path.basename(path), n, n1, n2))
        if args.apply:
            open(path, "w", encoding="utf-8").write(new)

    print("\n%d reference(s) across %d file(s)%s"
          % (total, touched, "" if args.apply else "  [dry run - use --apply]"))

    if args.apply:
        # Nothing may name a .html URL afterwards. A leftover means a form this
        # script does not understand, and a silent partial sweep is worse than none.
        left = []
        for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
            txt = open(path, encoding="utf-8").read()
            for m in re.finditer(r'(?:href\s*=\s*"[^"]*|' + re.escape(DOMAIN)
                                 + r'/[^"\s]*)\.html\b', txt):
                left.append("%s: %s" % (os.path.basename(path), m.group(0)[:70]))
        if left:
            print("\nFAIL - %d reference(s) survived the sweep:" % len(left))
            for line in left[:20]:
                print("  " + line)
            return 1
        print("verified: no internal reference names a .html URL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
