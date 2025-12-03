# Digitale Edition der *Res Gestae Divi Augusti* – Forschungsblog

Dieses Repository dokumentiert ein Projekt zur digitalen Edition der *Res Gestae Divi Augusti* (Monumentum Ancyranum).

## Projektkontext

- Das Projekt ist im Bereich der Alten Geschichte und der Digital Humanities angesiedelt und versteht sich als digitales Editionsprojekt.
- Es soll die Taten des Augustus in einer wissenschaftlich fundierten, annotierten und interaktiven Online-Edition zugänglich machen.
- Damit wird ein zentraler Text der römischen Antike digital erschlossen und für Forschung, Lehre und Öffentlichkeit nutzbar gemacht.

## Datenbasis

- Die Daten liegen als .docx-Datei vor.
- Sie enthalten den Text der *Res Gestae Divi Augusti* in:
  - lateinischer Originalsprache,
  - griechischer Übersetzung,
  - deutscher Übersetzung.
- Der Text wurde aus einem separaten PDF entnommen und ist kapitelweise gegliedert. Jedes Kapitel umfasst die drei Sprachfassungen in derselben Reihenfolge.
- Anmerkungen oder Kommentare sind in der .docx-Datei nicht enthalten (sie liegen im source-PDF).

## Ziel

- Umwandlung der Daten in ein TEI-konformes XML-Format, in dem Kapiteleinteilung und Sprachversionen strukturell ausgezeichnet sind.
- Erstellung einer öffentlichen, webbasierten digitalen Edition mit:
  - paralleler Darstellung von Originaltext, Übersetzungen und Annotationen,
  - Downloadmöglichkeiten der strukturierten Daten (XML, JSON) für Forschungszwecke,
  - optionalen Visualisierungen von Personen, Orten und Netzwerken,
  - interaktiven Such- und Filterfunktionen.

## Einsatz von LLMs

LLMs unterstützen das Projekt in mehreren Arbeitsschritten:

- Datenaufbereitung (Extraktion der Textstruktur aus .docx-Dateien, Vorschläge für TEI-Tagging),
- Annotation (Erkennung und semantische Verknüpfung historischer Personen, Orte und Ereignisse),
- Kommentierung (Generierung von erläuternden Texten und vereinfachten Erklärungen komplexer Passagen),
- Validierung (Prüfung auf Konsistenz und Vollständigkeit der Annotationen).

Alle Ergebnisse werden anschließend manuell überprüft, um wissenschaftliche Genauigkeit sicherzustellen.

## Zentrale Forschungsfrage

> Wie kann die Transformation der Res Gestae Divi Augusti in ein XML-basiertes, annotiertes Format mithilfe von Large Language Models (LLMs) neue Wege der Interpretation, Kontextualisierung und Vermittlung antiker Texte eröffnen?
