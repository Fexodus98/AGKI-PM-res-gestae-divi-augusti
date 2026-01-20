# Digital Edition Subsite (static)

Concept for a dedicated edition page that renders the TEI and exposes the trilingual text with lightweight, static assets (HTML/CSS/JS). Intended target: `site/edition/index.html` with shared styles from `styles.css`.

## Goals
- Surface the TEI as a readable, trilingual edition with synced chapters.
- Keep everything static (no backend); rely on client-side transformation or prebuilt HTML.
- Provide direct TEI download and clear links back to the repo/data.
- Expose annotation affordances (hover/click) and dedicated registers for persons, places, events.
- Offer a timeline view to contextualize events mentioned in the text.

## Data inputs
- Master TEI: `Vault/03_data/Res_Gestae_Divi_Augusti.xml`.
- Per-chapter TEI slices (already in `Vault/03_data/chapters_tei/*.xml`) can be pre-rendered or fetched on demand.
- Optional derived JSON for registers (persons/places/events) and timeline events; generated from TEI during the build.

## Page structure (single-page static)
- Hero: title, short blurb, CTA buttons (e.g., “Open TEI”, “Download TEI”, link to GitHub).
- Utility bar: language layout toggle (3-column vs. single-column tabs), search box, annotation toggle (show/hide highlights), font-size control.
- Left sidebar (sticky): table of contents for chapters; click/keyboard to jump to chapter anchors.
- Main content: synced chapter blocks with the three languages; inline annotations with hover tooltips; click to pin details in a right-side drawer.
- Right drawer (collapsible): annotation details (entity metadata), “related places/persons/events” links, “open in register” link.
- Footer: links to data, licensing, method notes (TEI schema, annotation policy).

## Text display patterns
- Two view modes:
  - Parallel view: three columns (lat/grc/deu) with matched segments by `@xml:id` or `<linkGrp>`; synced scrolling per chapter.
  - Focus view: tabbed or single-column with quick language switch, keeping the current segment in sync.
- Chapter framing: each chapter rendered as a block with anchor IDs; include a sticky “back to top / next chapter” micro-navigation.
- Per-segment controls: copy permalink, open annotation detail, toggle line wrapping.

## Annotations (hover + detail)
- Mark annotated spans with type-aware styling and `data-entity-type` (`person`, `place`, `event`, `concept`).
- Hover: show tooltip with label + short description; ensure keyboard focus also triggers the tooltip.
- Click: open/pin detail in the right drawer (full note, external refs, related segments, counts across languages).
- Toggle to hide/show highlights for focused reading.

## Registers (person/place/event)
- Dedicated section or sub-tabs (Personen, Orte, Ereignisse) fed by derived JSON from TEI.
- Features: search box, type filters (role/category), sort (A–Z, frequency), and quick letter index.
- Rows link back to occurrences in the text; hovering an item can preview snippets (per language).
- Add counts per language to surface coverage (e.g., “Augustus — 14 hits (lat), 12 (grc), 15 (deu)”).

## Timeline view
- Horizontal, scrollable timeline that plots dated events extracted from the TEI annotations.
- Each event card: title, date (or range/approximation), short summary, link to the segment(s) mentioning it.
- Consider dual modes: “compact dots” and “card stack” for accessibility; keyboard navigable.
- Data source: derived JSON with `{ id, label, when, relatedSegments, entityRefs }`; kept static in `site/data/timeline.json`.

## TEI download and data access
- Prominent download button: `Download TEI (XML)` pointing to the canonical TEI file.
- Secondary buttons: `Download chapter TEI (zip)`, `View on GitHub`, `API-less access: copy raw URL`.
- Note about license and version/date of the TEI snapshot shown on the page.

## Interaction microcopy & affordances
- Clear labels: “Show annotations”, “Hide annotations”, “Open register”, “Jump to chapter X”.
- Tooltips include entity type icons/colors; legend in the sidebar to explain color coding.
- Empty states: “No annotations in this segment”, “No hits for this filter”.

## Implementation notes (static-friendly)
- Prebuild path: XSLT or a small script to convert TEI → HTML snippets per chapter + JSON for registers/timeline.
- Client path: load prebuilt HTML into the page, or fetch TEI and transform client-side with a minimal XSLT/JS transformer.
- Keep assets lean: vanilla JS for interactivity; CSS grid/flex for the 3-column layout; prefers progressive enhancement.
- IDs: preserve `@xml:id` from TEI for anchors and cross-links; align parallel segments via shared IDs or link groups.
- Accessibility: ensure focus styles on annotations, ARIA labels on buttons/toggles, tab-order through sidebar and content.

## Possible extensions
- Map for places (static GeoJSON + lightweight map lib); link map pins to segments.
- Download buttons for “clean HTML” and “CSV of register entries”.
- “Compare languages” diff view for a selected segment (inline or modal).
- Print-friendly view that exports the current chapter with chosen language(s).
- Simple analytics (client-side) to count which chapters/entities are most viewed, stored locally (no tracking).
