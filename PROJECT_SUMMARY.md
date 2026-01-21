# Projektüberblick: Digitale Edition *Res Gestae Divi Augusti*

## Ausgangslage & Ziel
- Dreisprachiger Text (Latein, Griechisch, Deutsch) lag als `.docx` vor, kapitelweise gegliedert, ohne Apparat/Kommentare.
- Ziel: TEI-konforme, dreisprachige digitale Edition mit Web-Frontend, Download-Optionen und Basis-Suche/Filter.
- LLMs wurden zur Vorstrukturierung, Annotation, Kommentierung und Validierung eingesetzt; alle Ergebnisse wurden redaktionell geprüft.

## Pipeline & Werkzeuge
- **Vorbereitung**: `.docx` → Markdown/Kapitel (außerhalb des Repos).
- **TEI-Erzeugung**: `scripts/convert_md_to_tei_basic.py`
  - Liest Kapitel-Markdown aus `Vault/03_data/chapters`.
  - Annotiert Augustus-Pronomina (Regex, pro Sprache).
  - Markiert Personen/Orte/Organisationen anhand von `Vault/03_data/entity_registry.json`.
  - Schreibt TEI-Kapitel nach `Vault/03_data/chapters_tei/*.xml`.
- **Merge zur Haupt-TEI**: `scripts/merge_tei.py`
  - Sortiert Proömium nach vorne, kombiniert Kapitel-TEI.
  - Bindet Anmerkungen aus `Vault/03_data/Anmerkungen_res gestae.md` ein.
  - Output: `Vault/03_data/Res_Gestae_Divi_Augusti.xml`.
- **Anmerkungsabgleich**: `scripts/align_notes_from_md.py`
  - Liest `Res_Gestae_Divi_Augusti_mit_referenzen_korrigiert.md` (deutsche Noten).
  - Ordnet Noten per Kapitelerkennung/XPath zu TEI-Noten und schreibt zurück.
- **Plaintext-Exporte**: `scripts/export_chapter_txt.py`
  - Extrahiert Klartext je Kapitel/Sprache → `Vault/03_data/chapters_txt/Res_Gestae_Divi_Augusti_XX.txt`.
  - Gesamt-TXT: `Get-ChildItem Vault/03_data/chapters_txt/Res_Gestae_Divi_Augusti_*.txt | Sort-Object Name | Get-Content | Set-Content Vault/03_data/Res_Gestae_Divi_Augusti_full.txt`.
- Weitere Skripte: `run_inference.py`, `patch_augustus.py`, `debug_models.py` für LLM-Inferenz, Korrekturen, Tests.
- Git-Workflow: `git status`, `git add …`, `git commit …`, `git push origin main`.

## Web-Edition
- **Seiten**: `index.html`, `projektplan.html`, `datenaufbereitung.html`, `edition.html`, `register.html`, `textanalyse.html`, `gesamter-forschungsblog.html`.
- **Styles**: `styles.css` (monochrom, kontrastreich; Hero-/Card-/Panel-Layouts, Responsive Breakpoints, Register-Pills, Tabs).
- **Viewer**: `scripts/viewer.js`
  - `fetch` lädt `Vault/03_data/Res_Gestae_Divi_Augusti.xml`.
  - Parst StandOff-Register & `<note>`-Kommentare.
  - Rendert Kapitel in drei Spalten (la/grc/de) mit mobile Tabs.
  - Suche/Highlight + Modal, Registerfilter (Person/Ort/Org), Kapitel-Filter.
  - Links für Kapitel-Downloads (XML/TXT) und Gesamt-Downloads (TEI, Gesamt-TXT).
- **Downloads**: TEI-Hauptdatei, Gesamt-TXT, Kapitel-XML/TXT (automatisch verlinkt).

## Rolle der LLMs
- **Strukturierung**: Erkennung von Kapitel-/Abschnittsgrenzen, Vorschläge für TEI-Tagging.
- **Annotation**: Generierung/Normalisierung von Personen-, Orts-, Organisationsnamen für `entity_registry.json`; Markierung von Augustus-Pronomina.
- **Kommentierung**: Entwürfe für Noten/Interpretationen (in Markdown gesammelt, via Skripte in TEI überführt).
- **Validierung**: Querchecks auf Konsistenz zwischen Sprachfassungen, Dubletten, offensichtliche Fehlzuweisungen; immer mit manueller Endkontrolle.

## Ergebnis
- Vollständige TEI-Hauptdatei `Vault/03_data/Res_Gestae_Divi_Augusti.xml` mit StandOff-Register und Noten.
+- Kapitel-TEI-Exporte und Klartext je Kapitel (`Vault/03_data/chapters_tei`, `Vault/03_data/chapters_txt`), plus Gesamttext (`Vault/03_data/Res_Gestae_Divi_Augusti_full.txt`).
- Web-Edition mit paralleler Anzeige, Suche/Filter, Register-Navigation und Download-Optionen auf Basis der statischen Seiten und `viewer.js`.
