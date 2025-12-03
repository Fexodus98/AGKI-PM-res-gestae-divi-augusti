# README

Dieses Repository dokumentiert ein Projekt zur digitalen Edition der *Res Gestae Divi Augusti* (Monumentum Ancyranum).
Es verbindet methodische Ansätze der Alten Geschichte mit Verfahren der Digital Humanities und dem Einsatz von Large Language Models (LLMs).

---

## Projektkontext

- Das Projekt ist im Bereich der Alten Geschichte und der Digital Humanities angesiedelt und versteht sich als digitales Editionsprojekt.
- Es soll die Taten des Augustus in einer wissenschaftlich fundierten, annotierten und interaktiven Online-Edition zugänglich machen.
- Damit wird ein zentraler Text der römischen Antike digital erschlossen und für Forschung, Lehre und Öffentlichkeit nutzbar gemacht.

---

## Datenbasis

- Die Daten liegen als `.docx`-Datei vor.
- Sie enthalten den Text der *Res Gestae Divi Augusti* in:
  - lateinischer Originalsprache,
  - griechischer Übersetzung,
  - deutscher Übersetzung.
- Die Textteile sind kapitelweise organisiert. Anmerkungen, kritischer Apparat und editorische Kommentare des Ausgangswerks sind in der `.docx`-Datei nicht enthalten, sondern nur im ursprünglichen PDF.

Ziel der Datenaufbereitung ist die Umwandlung dieser `.docx`-Daten in eine TEI-konforme XML-Struktur, die:

- die dreisprachige Textstruktur explizit abbildet,
- die Grundlage für Annotation und Kommentierung darstellt,
- als Basis für eine digitale Edition und eine Weboberfläche genutzt werden kann.

---

## Ziel des Projekts

Das Projekt verfolgt mehrere Ziele:

- Erstellung einer TEI-basierten, dreisprachigen digitalen Edition der *Res Gestae Divi Augusti*.
- Aufbau einer webbasierten Edition (GitHub Pages) mit:
  - paralleler Darstellung der Sprachversionen,
  - Möglichkeit zum Download (z. B. TEI/HTML),
  - ggf. Visualisierung ausgewählter Aspekte (Orte, Personen, Themen),
  - grundlegenden Such- und Filterfunktionen.
- Systematische Integration von LLMs in:
  - Datenaufbereitung,
  - Annotation,
  - Kommentierung,
  - Validierung.

---

## Einsatz von LLMs

LLMs unterstützen das Projekt in mehreren Arbeitsschritten:

- **Datenaufbereitung**
  - Extraktion und Vorstrukturierung von Kapiteln und Abschnitten aus der `.docx`-Datei.
  - Vorschläge für TEI-Tagging (z. B. Personen, Orte, strukturelle Einheiten).
- **Annotation**
  - Erkennung und semantische Verknüpfung historischer Personen, Orte und zentraler Begriffe.
  - Strukturierte Ausgabe von Annotationen, die in TEI oder ergänzenden Formaten (z. B. JSON) abgelegt werden können.
- **Kommentierung**
  - Generierung erläuternder Texte und vereinfachter Erklärungen komplexer Passagen.
  - Unterstützung bei der Erstellung von didaktischen Kommentaren für Lehrkontexte.
- **Validierung**
  - Prüfung auf Konsistenz und Vollständigkeit der Annotationen.
  - Gegenprüfung verschiedener Sprachversionen (lat/grc/deu) auf offensichtliche Inkonsistenzen.

Alle durch LLMs generierten Ergebnisse werden manuell überprüft, um wissenschaftliche Genauigkeit sicherzustellen.

---

## Zentrale Forschungsfrage

> Wie kann die Transformation der *Res Gestae Divi Augusti* in eine TEI-basierte, KI-unterstützte digitale Edition neue Zugänge zur Analyse, Annotation, Kontextualisierung und Vermittlung antiker Texte eröffnen?

---

## Repository-Struktur

Zielstruktur dieses Repositories:

```text
/
|- README.md              # Dieses Dokument
|- vault/                 # Obsidian-Vault (Projektorganisation & Fachnotizen)
|  |- 00_Meta/
|  |  |- Project-Index.md
|  |  |- Forschungsblog-Text.md
|  |- 01_Planning/
|  |  |- WorkPackages.md
|  |  |- Roadmap.md
|  |  |- Projektplan.md
|  |- 02_Design/
|  |  |- UserStories.md
|  |  |- Specs.md
|  |- 03_Data/
|     |- Data.md
|     |- Datenaufbereitung.md
|     |- TEI-linkGrp.md
|- site/                  # Statische Website für GitHub Pages
|  |- index.html
|  |- css/
|  |  |- styles.css
|- data/                  # (optional) TEI-XML, Zwischenstände, Skripte
   ...
```
