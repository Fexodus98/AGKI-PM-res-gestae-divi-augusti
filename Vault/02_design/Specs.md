
# Specs – technische & nicht-funktionale Anforderungen

Siehe Anforderungen aus Nutzersicht: [[UserStories]]  
Siehe Datenmodell & Ontologie: [[Data]] · [[Datenaufbereitung]]

---

## Systemübersicht

- **Datenebene**
  - Quelle: `.docx`-Datei der *Res gestae divi Augusti* (dreisprachig, kapitelweise).
  - Zieldaten: TEI-konforme XML-Dateien.
  - Abgeleitete Daten: transformierte HTML-Fragmente für die Webanzeige, ggf. JSON für Annotationen.

- **Verarbeitungsebene**
  - Schritte:
    1. Import & Bereinigung der `.docx`-Daten.
    2. TEI-Tagging (halbmanuell oder skriptgestützt).
    3. KI-Annotation auf Basis definierter Prompts.
    4. Transformation TEI → HTML (z. B. XSLT oder Skript).

- **Präsentationsebene**
  - Statische Website (HTML/CSS, optional leichtes JavaScript).
  - Deployment via GitHub Pages.

---

## Tech-Stack

- Versionsverwaltung: Git / GitHub
- Hosting: GitHub Pages (statische Website)
- Frontend:
  - HTML5, CSS3 (responsive, mobile-first)
  - Optional: leichtes JavaScript für Interaktion (z. B. Navigation, TOC, Ein-/Ausblenden von Annotationen)
- Datenformate:
  - Eingang: `.docx`
  - Kern: `TEI-XML`
  - Ausgabe: `HTML`, optional `JSON` (für Annotationen)
- Tools (Beispiele):
  - XML-Editor (z. B. Oxygen, VS Code mit XML-Plugins)
  - Skriptsprache (z. B. Python) für Konvertierungen
  - Zugriff auf ein LLM (API oder Chat-Interface) zur Annotation und Kommentierung

---

## Funktionale Anforderungen (Auszug)

Die Website soll:

- eine Projektübersicht mit Forschungsblog-Charakter bieten (Ziele, Kontext, Vorgehen).
- ausgewählte Teile der *Res gestae* TEI-basiert anzeigen.
- Annotationen (z. B. Personen/Orte/Sachbegriffe) sichtbar machen, z. B. über:
  - Tooltips,
  - eine Sidebar,
  - oder einen Kommentar-/Annotationenbereich.
- Links auf das zugrunde liegende TEI und das GitHub-Repo bereitstellen.
- grundlegende Informationen zur KI-Annotation (Methodik, Prompts) zugänglich machen.

---

## Nicht-funktionale Anforderungen

- **Usability**
  - Klare, gut lesbare Typografie.
  - Intuitive Navigation (Startseite, Edition, Dokumentation, ggf. Blog).

- **Performance**
  - Schnelles Laden durch statische Seiten.
  - Verzicht auf schwere Frameworks, soweit möglich.

- **Wartbarkeit**
  - Saubere Repo-Struktur (z. B. Trennung von `vault/`, `site/`, `data/`).
  - Dokumentierte Build-/Deployment-Schritte im `README.md`.

- **Reproduzierbarkeit**
  - Dokumentation der TEI-Richtlinien und KI-Prompts in [[Data]] und [[Datenaufbereitung]].
  - Möglichkeit, zentrale Schritte (z. B. Transformationen) zu wiederholen.

- **Transparenz**
  - Kennzeichnung, welche Annotationen durch KI erzeugt wurden.
  - Kurze, verständliche Erklärung der Rolle von KI im Projekt.
