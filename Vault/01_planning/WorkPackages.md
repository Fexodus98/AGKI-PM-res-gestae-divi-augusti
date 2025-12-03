
# Work Packages – Tasks & Aufwand

Siehe Projektübersicht: [[Project-Index]]  
Siehe narrativen Überblick: [[Projektplan]]

---

## WP1: Projekt-Setup & Infrastruktur

**Ziel:** Arbeitsumgebung, Repo-Struktur und Obsidian-Vault aufsetzen.

### Tasks

- Task: GitHub-Repo erstellen (inkl. Projektkürzel)
  - Beschreibung: Neues Repo anlegen, Branch-Konvention definieren.
  - Aufwand: Low

- Task: Obsidian-Vault im Repo anlegen
  - Beschreibung: Verzeichnis `/vault` erstellen, Grundstruktur gemäß [[Project-Index]] anlegen.
  - Aufwand: Low

- Task: GitHub Pages konfigurieren
  - Beschreibung: Pages-Branch/Folder festlegen, erste `index.html` deployen.
  - Aufwand: Medium

---

## WP2: Datenbasis & TEI-Modellierung

**Ziel:** Ausgangsdatei (.docx) in eine bereinigte, TEI-konforme XML-Struktur überführen.

### Tasks

- Task: Analyse der .docx-Quelle
  - Beschreibung: Struktur der *Res gestae* im Word-Dokument erfassen (Kapitel, Absätze, dreisprachige Struktur).
  - Aufwand: Medium

- Task: Textbereinigung
  - Beschreibung: Entfernen von Artefakten, Vereinheitlichung von Zeichen, Normalisierung von Sonderzeichen.
  - Aufwand: High

- Task: Entwurf TEI-Schema / Tagging-Konzept
  - Beschreibung: Festlegen, welche TEI-Elemente (z. B. `<div>`, `<p>`, `<persName>`, `<placeName>`, `<linkGrp>`) wie eingesetzt werden.
  - Aufwand: High

- Task: Umsetzung TEI-XML
  - Beschreibung: Konvertierung/Bearbeitung der Daten in eine TEI-konforme XML-Struktur mit dreisprachiger Segmentstruktur.
  - Aufwand: High

---

## WP3: KI-Annotation & Context Engineering

**Ziel:** KI-gestützte Annotation vorbereiten und in den Workflow integrieren.

### Tasks

- Task: Annotationsschema definieren
  - Beschreibung: Festlegen, welche Arten von Informationen annotiert werden (Personen, Orte, Sachbegriffe, historischer Kontext).
  - Aufwand: Medium

- Task: Prompt-Design für LLM
  - Beschreibung: Kompakte, token-effiziente Prompts auf Basis der Ontologie in [[Data]] definieren.
  - Aufwand: Medium

- Task: Experimente mit KI-Annotation
  - Beschreibung: Beispiele durch ein LLM schicken, Ergebnisse prüfen und Schema ggf. anpassen.
  - Aufwand: High

- Task: KI-gestützte Kommentierung
  - Beschreibung: Generierung erläuternder Kommentare, die später redigiert werden.
  - Aufwand: High

- Task: KI-gestützte Validierung
  - Beschreibung: Nutzung von LLMs zur Prüfung auf Konsistenz und Vollständigkeit der Annotationen.
  - Aufwand: Medium

---

## WP4: Web-Frontend & GitHub Pages

**Ziel:** Statische Website (Forschungsblog/Projektseite) als Frontend für die Edition.

### Tasks

- Task: Grundgerüst `index.html` erstellen
  - Beschreibung: Struktur der Seite (Header, Navigation, Content-Bereich) definieren.
  - Aufwand: Medium

- Task: CSS-Stylesheet aufsetzen (responsive)
  - Beschreibung: Mobile-first-Design, Layout für Textanzeige der Edition und Projektinformationen.
  - Aufwand: Medium

- Task: Integration der TEI-Inhalte
  - Beschreibung: Transformation von TEI nach HTML; Einbindung ausgewählter Textpassagen und Annotationen.
  - Aufwand: High

- Task: Deployment auf GitHub Pages testen
  - Beschreibung: Build/Deployment prüfen, grundlegende Browser-Tests durchführen.
  - Aufwand: Medium

---

## WP5: Dokumentation & Reflexion

**Ziel:** Methodische Dokumentation, README und Reflexion der KI-Komponente.

### Tasks

- Task: README im Repo erstellen/aktualisieren
  - Beschreibung: Projektbeschreibung, Setup-Anleitung, Struktur der Dateien.
  - Aufwand: Low

- Task: Methodische Dokumentation
  - Beschreibung: Beschreibung, wie traditionelle Methoden und KI im Projekt zusammenspielen.
  - Aufwand: Medium

- Task: Lessons Learned / Reflexion
  - Beschreibung: Kritische Einschätzung von Nutzen und Grenzen der KI-Annotation und der gewählten Workflows.
  - Aufwand: Medium
