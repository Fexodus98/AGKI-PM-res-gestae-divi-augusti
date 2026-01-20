# Tasks & Improvements: Digital Edition (Res Gestae)

This document outlines the remaining tasks and proposed improvements to finalize the Digital Edition of the *Res Gestae Divi Augusti*.

## 1. Core Feature Implementation (Missing from Design)

### 1.1 Timeline Visualization
- [ ] **Backend (Python)**: Update `scripts/merge_tei.py` to extract `listEvent` and `listDate` elements into a separate `site/data/timeline.json` file.
    - *Structure*: `{ "id": "ev1", "date": "0014", "label": "Death of Augustus", "relatedChapters": [1, 35] }`.
- [ ] **Frontend (JS)**: Create a timeline component in `edition.html` (bottom drawer or separate view).
    - *Tech*: Horizontal scrollable container or a lightweight library (e.g., Vis.js) if complexity increases.
    - *Interaction*: Clicking an event highlights relevant text segments.

### 1.2 Comprehensive Registers (Indices)
- [ ] **UI Implementation**: Add a dedicated "Index" tab in the control sidebar or a modal overlay.
- [ ] **Functionality**:
    - List all Persons, Places, and Organizations alphabetically.
    - Search/Filter input for the index.
    - "Hit counts" per entity (e.g., "Augustus (50)").
    - **Reverse Linking**: Clicking an entity in the index lists all chapters/segments where it appears.

### 1.3 Full-Text Search
- [ ] **Search Engine**: Implement a client-side search in `viewer.js`.
    - Index the text content of the XML DOM on load.
    - Support searching across specific languages (Latin, Greek, German).
- [ ] **UI**: Add search bar to the "Controls" sidebar.
- [ ] **Result Display**: Highlight matches in the text and provide a list of "Jump to" links.

### 1.4 Interactive Map (Geospatial View)
- [ ] **Data Prep**: Enhance `listPlace` in the TEI data with coordinates (`<geo>` tags) or a separate GeoJSON file.
- [ ] **Visualization**: Embed a lightweight map (Leaflet.js) showing mentioned places.
- [ ] **Interaction**: Clicking a pin shows context from the text; clicking a place in text pans the map.

## 2. UI/UX Improvements

### 2.1 Navigation & Layout
- [ ] **Sticky Column Headers**: Ensure "Latin / Greek / German" headers stay visible while scrolling long chapters.
- [ ] **Mobile Responsiveness**:
    - Currently, the 3-column grid breaks on small screens.
    - *Solution*: Implement a "Tabbed View" for mobile (show one language at a time with a switcher).
- [ ] **Deep Linking**: Ensure URL params (e.g., `edition.html?chapter=4&focus=ev3`) can open specific chapters and highlight specific entities or segments on load.

### 2.2 Reader Experience
- [ ] **Synoptic Alignment**: Ensure paragraphs align perfectly across columns even if one language is significantly longer. (Consider JS-based height matching or CSS Grid subgrid).
- [ ] **Font Controls**: Add a slider to adjust font size and line height.
- [ ] **Dark/Light Mode**: Verify high-contrast support for entity highlights (current colors might have low contrast in dark mode).

## 3. Data & Architecture Enhancements

### 3.1 Data Validation
- [ ] **Schema Validation**: Create a TEI ODD/RNG schema to validate `Res_Gestae_Divi_Augusti.xml` during the build process to prevent broken markup.
- [ ] **Automated Testing**: Add a GitHub Action to run `merge_tei.py` and validate XML structure on every commit.

### 3.2 Export Options
- [ ] **Citation Tool**: Add a "Cite this" button next to chapters/segments (providing BibTeX/Chicago format).
- [ ] **Downloads**:
    - "Download Chapter as PDF" (using browser print styles).
    - "Download Raw TEI" (already exists, but enhance with specific selection downloads).

## 4. Content Enrichment
- [ ] **Glossary**: Add a glossary for technical Roman terms (e.g., *Imperator*, *Consul*, *Tribunicia Potestas*) linked via `<term>` tags in TEI.
- [ ] **Commentary Expansion**: Ensure the existing notes (from Markdown) are fully linked and formatted correctly in the sidebar (Markdown rendering inside the sidebar notes).

---
**Priority Order:**
1. Fix Mobile View / Responsive Layout
2. Implement Search
3. Implement Registers (Person/Place Index)
4. Timeline
5. Map
