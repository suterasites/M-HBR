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
- Referred by Johnny Sokolov (James's ANSC reserves teammate). Decision maker is the father, not Johnny. Pitch is B2B.
- Hero copy stays generic, no first names, until Johnny confirms naming with his dad.

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
- Single `index.html` file, all styles inline
- Tailwind CSS via CDN
- Mobile-first responsive
- Use real assets from `Assets/` folder, not placeholders, where available

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
- Single page (index.html) for prospect mockup pitch.
- Sections: Nav, Hero, Trust Strip, Services, Signs You Need Reblocking, Process, Gallery, About, FAQ, Contact, Footer.
