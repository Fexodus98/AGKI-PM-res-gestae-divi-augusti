# Wissensdokument – Digitale Edition *Res Gestae Divi Augusti*

Dieses Dokument fasst Ziel, Vorgehen, Werkzeuge, Datenflüsse, LLM-Einsatz und Web-Auslieferung so zusammen, dass daraus direkt eine Präsentation gebaut werden kann.

---

## 1) Zielbild & Nutzen
- **Editionsziel**: TEI-basierte, dreisprachige (Latein, Griechisch, Deutsch) Online-Edition des Monumentum Ancyranum mit Annotationen, Kommentaren und Download-Optionen.
- **Publikum**: Forschung (Alte Geschichte/Digital Humanities), Lehre, interessierte Öffentlichkeit.
- **Mehrwert**:
  - Vergleichende parallele Anzeige der Sprachversionen.
  - StandOff-Register für Personen/Orte/Organisationen.
  - Anmerkungen/Noten zur Kontextualisierung.
  - Such- und Filterfunktionen (Text, Register, Kapitel).
  - Offene Daten (TEI/XML, TXT, Kapitel-Exports).
- **LLM-Rolle**: Beschleunigung bei Strukturierung, Annotation, Kommentierung, Validierung; finale Entscheidungen bleiben menschlich.

---

## 2) Datenbasis & Input
- Ursprung: `.docx` mit dreisprachigem Text, kapitelweise, ohne kritischen Apparat/Kommentare.
- Aufbereitungsschritte (außerhalb Repo):
  - `.docx` → Markdown-Kapitel (la/grc/de getrennt, kapitelweise).
  - Manuelle/LLM-gestützte Korrekturen (Zeilenumbrüche, Sonderzeichen, Kapitelmarker).
- Im Repo zentrale Dateien:
  - `Vault/03_data/chapters/` (Markdown-Kapitel, Quelle für TEI-Konversion).
  - `Vault/03_data/entity_registry.json` (StandOff-IDs für Personen/Orte/Organisationen).
  - `Vault/03_data/Anmerkungen_res gestae.md` + `Res_Gestae_Divi_Augusti_mit_referenzen_korrigiert.md` (Noten/Kommentare).

---

## 3) Verarbeitungspipeline (Skripte & Befehle)
### 3.1 TEI-Erzeugung pro Kapitel
- Script: `scripts/convert_md_to_tei_basic.py`
- Aufgaben:
  - Liest Kapitel-Markdown aus `Vault/03_data/chapters`.
  - Markiert Augustus-Pronomina via Regex (pro Sprache).
  - Annotiert Personen/Orte/Organisationen via Registry (`entity_registry.json`).
  - Schreibt TEI-`div type="chapter"` nach `Vault/03_data/chapters_tei/*.xml`.
- Aufruf: `python scripts/convert_md_to_tei_basic.py`

### 3.2 Merge zur Haupt-TEI
- Script: `scripts/merge_tei.py`
- Aufgaben:
  - Sortiert Proömium nach vorne, lädt alle Kapitel-TEI.
  - Bindet Noten aus `Vault/03_data/Anmerkungen_res gestae.md` ein (`<back>/<note>`).
  - Ergänzt Timeline/Metadaten (optional via `timeline.json`).
  - Output: `Vault/03_data/Res_Gestae_Divi_Augusti.xml`.
- Aufruf: `python scripts/merge_tei.py`

### 3.3 Notenabgleich aus Markdown
- Script: `scripts/align_notes_from_md.py`
- Aufgaben:
  - Liest `Res_Gestae_Divi_Augusti_mit_referenzen_korrigiert.md` (deutsche Noten).
  - Kapitelerkennung, Parsen der Fußnotenmarker, Mapping auf TEI-Noten.
  - Schreibzugriff auf `Vault/03_data/Res_Gestae_Divi_Augusti.xml` (XPath mit lxml).
- Aufruf: `python scripts/align_notes_from_md.py`

### 3.4 Plaintext-Exporte
- Script: `scripts/export_chapter_txt.py`
- Aufgaben:
  - Extrahiert Klartext aus Kapitel-TEI (la/grc/de) → `Vault/03_data/chapters_txt/Res_Gestae_Divi_Augusti_XX.txt`.
- Aufruf: `python scripts/export_chapter_txt.py`
- Gesamt-TXT:  
  `Get-ChildItem Vault/03_data/chapters_txt/Res_Gestae_Divi_Augusti_*.txt | Sort-Object Name | Get-Content | Set-Content Vault/03_data/Res_Gestae_Divi_Augusti_full.txt`

### 3.5 LLM-/QA-Hilfen
- `run_inference.py`: Wrapper für Modellaufrufe (z. B. Glossar, Dublettencheck).
- `patch_augustus.py`: Korrektur-/Patchlogik für spezifische Stellen.
- `debug_models.py`: Testläufe/Diagnose.

### 3.6 Git-Workflow
- Status/Commit/Push: `git status`, `git add …`, `git commit -m "…"`, `git push origin main`.

---

## 4) Struktur der Web-Edition
### 4.1 Seiten
- `index.html`: Überblick/Forschungsblog-Intro.
- `projektplan.html`: Roadmap, Arbeitsschritte.
- `datenaufbereitung.html`: Beschreibung der Aufbereitungsschritte.
- `edition.html`: Hauptrenderer für TEI (Viewer).
- `register.html`: StandOff-Register-Ansicht (Person/Ort/Org).
- `textanalyse.html`: Argumentations-/Strukturanalyse.
- `gesamter-forschungsblog.html`: Langform-Blog.

### 4.2 Styling (styles.css)
- Monochromes, kontrastreiches Design; Cards/Panels/Labels; responsive Breakpoints; mobile Tabs.
- Entity-Farbcodierung (Person/Ort/Org) ohne Rahmen; mark-Highlight; Typografie Work Sans/Cormorant.

### 4.3 Viewer/Interaktion (scripts/viewer.js)
- `fetch` lädt `Vault/03_data/Res_Gestae_Divi_Augusti.xml`.
- Parsed StandOff-Register (person/place/org) und `<note>`-Kommentare.
- Rendert Kapitel in drei Spalten (la/grc/de); mobile Tabs; sticky Kapitel-Header.
- Suche + Highlight + Modal; speichert Original-HTML je Segment für Reset.
- Registerfilter (Person/Ort/Org); Kapitel-Filter (`filterChapters`) zum Ausblenden einzelner Kapitel.
- Download-Links (Kapitel XML/TXT) werden dynamisch gesetzt; Gesamt-Downloads statisch verlinkt (TEI, Gesamt-TXT).
- Event-Delegation für Entities/Notes; Scroll-to-Entity und Sidebar-Info.

### 4.4 Downloads
- Gesamt: `Vault/03_data/Res_Gestae_Divi_Augusti.xml` (TEI), `Vault/03_data/Res_Gestae_Divi_Augusti_full.txt`.
- Kapitel: `Vault/03_data/chapters_tei/Res_Gestae_Divi_Augusti_XX.xml`, `Vault/03_data/chapters_txt/Res_Gestae_Divi_Augusti_XX.txt`.

---

## 5) Rolle der LLMs im Detail
- **Strukturierung**: Erkennung von Kapitel-/Abschnittsgrenzen und Vorschläge für TEI-Tagging (persName/placeName/orgName, div-Struktur).
- **Annotation**: Vorschläge/Normalisierung für `entity_registry.json`; Identifikation von Augustus-Pronomina; Entwürfe für StandOff-Beschreibungen (`desc`).
- **Kommentierung**: Entwürfe für Noten/Interpretationen (in Markdown gesammelt, via `align_notes_from_md.py` in TEI übertragen).
- **Validierung**: Querchecks auf Konsistenz (la/grc/de), Dubletten im Register, offensichtliche Fehlzuweisungen; menschliche Endkontrolle obligatorisch.
- **Grenzen**: LLMs liefern Entwürfe/Heuristiken; philologische und editorische Freigabe bleibt manuell.

---

## 6) Technische Eckpunkte (für Slides)
- **Formate**: TEI/XML mit StandOff-Register; Plaintext-Exports; statische HTML/CSS/JS.
- **Parsing/Manipulation**: Python + lxml, Regex; DOMParser im Browser.
- **Deployment**: Statische Dateien (geeignet für GitHub Pages/ähnliche Hosts).
- **Interaktion**: Native JS (kein Framework); Responsive Layout; Suche/Highlight; Filter.
- **Datenhaltung**: Keine DB, alles statisch; TEI als Single Source of Truth.

---

## 7) Storyline für Präsentation (Vorschlag)
1. **Problem & Ziel**: Warum *Res Gestae* digital? → Zugänglichkeit, Vergleichbarkeit, Annotation.
2. **Datenbasis**: `.docx` → Markdown → TEI; dreisprachig, kapitelweise.
3. **Pipeline**: Konversion (convert_md…), Merge (merge_tei), Noten-Abgleich (align_notes…), Exporte (export_chapter_txt).
4. **LLM-Einsatz**: Strukturierung, Annotation, Kommentierung, Validierung; immer mit manueller Kontrolle.
5. **Web-Edition**: Dreispalten-Viewer, Suche/Filter, Register, Downloads, Responsive UI.
6. **Outputs**: TEI-Hauptdatei, Kapitel-TEI, TXT (Kapitel+Gesamt), statische Site.
7. **Lerneffekte**: LLMs beschleunigen, ersetzen aber keine philologische Prüfung; klare Trennung von Entwurf (LLM) und Freigabe (Mensch).
8. **Ausblick**: Erweiterte Visualisierungen (Netzwerke, Karten), stärkere Validierungsregeln, Togglebare Kommentarseiten.

---

## 8) Quick-Reference (Dateien & Pfade)
- TEI-Gesamt: `Vault/03_data/Res_Gestae_Divi_Augusti.xml`
- Kapitel-TEI: `Vault/03_data/chapters_tei/Res_Gestae_Divi_Augusti_XX.xml`
- Kapitel-TXT: `Vault/03_data/chapters_txt/Res_Gestae_Divi_Augusti_XX.txt`
- Gesamt-TXT: `Vault/03_data/Res_Gestae_Divi_Augusti_full.txt`
- Scripts: `scripts/convert_md_to_tei_basic.py`, `merge_tei.py`, `align_notes_from_md.py`, `export_chapter_txt.py`, `viewer.js` (+ Hilfsskripte)
- Web: `edition.html`, `register.html`, `textanalyse.html` (+ weitere Seiten), `styles.css`, `scripts/viewer.js`

---

## 9) Hinweise für Live-Demo
- **Edition-Page**: Kapitel-Filter nutzen, Suche auslösen, Register-Filter zeigen, Entity-Klick -> Sidebar.
- **Downloads**: TEI & Gesamt-TXT anklicken; Kapitel-Downloads testen.
- **Responsiveness**: Mobile Tabs für Sprachen demonstrieren.
- **LLM-Hinweis**: Entwürfe aus LLM, aber kuratierte finale Fassung betonen.
