# CLAUDE.md - Maribyrnong & Hobsons Bay Reblocking

## Business Context

**Business Name:** Maribyrnong & Hobsons Bay Reblocking
**Phone:** 0466 961 177 (primary), 0418 802 192 (secondary)
**Email:** vsokolov@tpg.com.au
**Existing Website:** https://www.mhbreblocking.com/
**Location:** Inner-west Melbourne (Maribyrnong + Hobsons Bay councils). Services Victoria-wide.
**Experience:** 35+ years (trading since the early 1990s)

### About
- Family-owned and operated since the early 1990s
- Specialises in reblocking, restumping, underpinning, levelling, lifting and stabilising
- Concrete stump material, computer levelling, all permits supplied
- 15-year guarantee on all work
- Registered Building Practitioner (BPC), Member of MBA, public liability insurance
- 107 reviews
- Pensioner and senior discounts

### Services
- Reblocking and Restumping
- Weatherboard stump to concrete stump conversion
- Underpinning
- Levelling, Lifting, Raising and Re-packing
- Stabilising and Strengthening
- Foundation Repairs (verandahs, slabs, columns, footings, posts, bracing stumps)

### Problems Solved
- Door jamming, window jamming
- Uneven floors
- Wall cracks
- Uneven driveways and roads

### Referral / Decision Maker
- Referred by Johnny Sokolov (James's ANSC reserves teammate). Decision maker is Simon (Johnny's brother), not Johnny. Pitch is B2B.
- Hero copy stays generic, no first names, until Johnny confirms naming with his brother.

---

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.

## Reference Images
- Existing site (mhbreblocking.com) is dated and bare. Do not match it. Build from scratch with high craft.
- Screenshot output, compare, fix mismatches, re-screenshot. At least 2 comparison rounds.

## Local Server
- **Always serve on localhost** - never screenshot a `file:///` URL.
- Start the dev server: `node serve.mjs` (serves at `http://localhost:3000`)
- `serve.mjs` lives in the project root. Start in background before screenshotting.

## Screenshot Workflow
- **Always screenshot from localhost:** `node screenshot.mjs http://localhost:3000`
- Saved to `./temporary screenshots/screenshot-N.png`
- Optional label: `node screenshot.mjs http://localhost:3000 label`

## Output Defaults
- Multi-page static site, all styles inline per page
- Tailwind CSS via CDN
- Mobile-first responsive
- Use real assets from `Assets/` folder, not placeholders, where available
- Shared shell (nav, footer, mobile menu, scripts) is duplicated across each HTML file. Keep markup in sync when editing.

## Brand Assets
- Logo: `Assets/logo.jpg` (orange/red M-mark on white, condensed sans wordmark)
- Photography: 5 real job photos in `Assets/` (concrete stumps, jacked houses, under-house framing)

### Brand Colors (derived from logo)
- Brand Orange: `#E66A2C`
- Brand Rust:   `#8B2A1A`
- Charcoal:     `#1A1614`
- Cream:        `#F5EFE6`
- Sand:         `#E8DDC9`

### Type Pairing
- Display: industrial condensed sans (Archivo Narrow / Anton family) for headings
- Body: clean sans (Inter)

## Anti-Generic Guardrails
- No default Tailwind palette. Use brand tokens above.
- Layered shadows tinted with rust/charcoal at low opacity, never flat shadow-md.
- Tight tracking on display headings, generous line-height on body.
- Animate `transform` and `opacity` only.
- Image treatments: gradient overlay + mix-blend tone for cohesion.
- Layered surfaces: base, elevated, floating - not all flat.

## Hard Rules
- No em dashes anywhere. Use hyphens, commas, or periods.
- No `transition-all`.
- Do not invent first names for the owner. Hero stays generic until naming is confirmed.
- Do not invent specific testimonial names without flagging them as placeholders in commit notes.

## Site Scope
Multi-page client build (commenced 2026-05-04 on green light from Simon Sokolov).

Pages:
- `index.html` - Homepage. Sections: Nav, Hero, Services grid, Featured band, Gallery, About, Reviews (Elfsight), Contact CTA, Footer.
- `reblocking-restumping.html` - Core service page. Hero, what-it-is, signs you need it, 5-step process, featured band, gallery, FAQ, related, final CTA, footer.
- `underpinning.html` - Brick/slab/double-storey footing repair. Same shape as reblocking page, content tuned to subsidence and engineering.
- `levelling-lifting.html` - Computer-levelled lifting and raising. Content tuned to floor levelling and house raising.
- `stump-conversion.html` - Timber-to-concrete stump conversion. Content tuned to weatherboard conversion, pre-sale/pre-reno triggers.
- `stabilising-strengthening.html` - Bracing, footings, verandahs, slabs, columns. Includes `#verandahs` anchor used by mega-nav.
- `about.html` - Dedicated about page. Hero, story narrative, what-we-stand-for, credentials, service area band, final CTA.
- `gallery.html` - Dedicated gallery page. Hero, sticky filter bar (All / Reblocking / Conversion / Levelling / Underpinning / Stabilising), masonry grid, final CTA. Uses `data-cat` filtering JS.
- `contact.html` - Dedicated contact page. Hero, Formspree form (with service select), direct lines, service area, hours, trust strip.

Shared shell duplicated across each page (head, nav, mobile menu, breadcrumb, footer, scripts). When updating shared markup, propagate to ALL pages.

Nav links go to real pages, not anchors. About and Gallery now have dedicated pages (about.html, gallery.html) - no anchor jumps to homepage sections from anywhere. The homepage still has its embedded About and Gallery sections (kept as content for that page) but they no longer carry IDs targeted by the nav.

## Gallery filter JS
Gallery items use `data-cat` attributes (`reblocking`, `conversion`, `levelling`, `underpinning`, `stabilising`). Filter buttons use `data-filter`. To add a new category: add a button with the new `data-filter` value and tag the relevant `<figure>` with the matching `data-cat`. Empty-state element id `gallery-empty` shows when the active filter has zero matches.

## Lazy-loaded gallery images
Gallery images carry `loading="lazy"`. Full-page screenshot tools may show blanks below the fold; that is expected behaviour and does not indicate a broken asset. Real visitors see them load on scroll.

## SEO methodology applied (2026-05-04)
The full `SEO_brief/on-page-seo.md` checklist was applied to this site:

- **Per-page meta:** unique title (49-58 chars) + meta description (130-148 chars) with primary keyword per page; canonical URLs site-wide.
- **Open Graph + Twitter Card:** present on every page (wrapped in `<!-- OG_TWITTER_START -->` ... `<!-- OG_TWITTER_END -->` markers for idempotent re-runs).
- **JSON-LD schema** (wrapped in `<!-- JSONLD_START -->` ... `<!-- JSONLD_END -->`):
  - `HomeAndConstructionBusiness` on homepage, about, contact (single source of truth in `_seo_inject.py` `BUSINESS_CORE`).
  - `Service` on each of the 5 service pages.
  - `BreadcrumbList` on every non-home page.
  - `FAQPage` extracted automatically from `<details>` blocks on the 5 service pages.
- **Headings:** single H1 per page, all containing the primary service keyword.
- **Images:** width/height attributes added to every `Assets/*` image based on real intrinsic dimensions (probed via Pillow). Below-fold gallery images carry `loading="lazy"`.
- **Semantic HTML5:** every page wraps body content in `<main id="main" tabindex="-1">` between `</header>` and `<footer>`. Skip-to-content link injected after `<body>` (uses Tailwind `sr-only` + `focus:not-sr-only`).
- **Sitemap + robots:** `sitemap.xml` and `robots.txt` at site root. Sitemap lists all 9 pages with priority weights (homepage 1.0, services 0.9, contact 0.8, about/gallery 0.7).
- **OG image:** placeholder `https://www.mhbreblocking.com/og-image.jpg` referenced. Generate a 1200x630 brand image and drop at `og-image.jpg` before deploy.

### Re-running the SEO injection
The injection scripts (`_seo_inject.py`, `_seo_images.py`, `_seo_main.py`) were used as one-shot tools and removed. If you need to re-run, recreate them or write fresh, and re-extract. Idempotency markers (`<!-- OG_TWITTER_START -->`, `<!-- JSONLD_START -->`, `id="main"`) let you re-run without duplicating blocks.

### What still needs doing (pre-deploy)
- Generate the actual `og-image.jpg` (1200x630).
- Replace `REPLACE_WITH_FORMSPREE_ID` in `contact.html` with the real Formspree form ID.
- Confirm DNS access for mhbreblocking.com cutover.

## Formspree
- Both forms (currently only contact.html, homepage is now CTA-only) post to `https://formspree.io/f/REPLACE_WITH_FORMSPREE_ID`.
- Replace `REPLACE_WITH_FORMSPREE_ID` with the real Formspree form ID once Simon confirms the inbox to receive submissions.
- Form has built-in honeypot (`_gotcha` field).
- JS handler in contact.html intercepts submit, posts via fetch with JSON Accept header, shows inline success/error status. While the placeholder ID is in the action attribute the JS lets the form post normally (no submission goes anywhere).
