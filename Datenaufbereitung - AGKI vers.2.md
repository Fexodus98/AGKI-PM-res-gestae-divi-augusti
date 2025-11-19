# Datenaufbereitung für die digitale Edition der *Res Gestae Divi Augusti*

## 1. Ausgangslage

Die Daten liegen als .docx-Datei vor und enthalten den Text der *Res Gestae Divi Augusti* in:

- lateinischer Originalsprache,
- griechischer Übersetzung und
- deutscher Übersetzung.

Der Text wurde aus einem separaten PDF entnommen und ist kapitelweise gegliedert. Jedes Kapitel umfasst die drei Sprachfassungen in derselben Reihenfolge. Anmerkungen oder Kommentare sind in der .docx-Datei nicht enthalten, sondern nur im ursprünglichen source-PDF.

Ziel der Datenaufbereitung ist die Umwandlung dieser .docx-Daten in ein TEI-konformes XML-Format, in dem Kapiteleinteilung und Sprachversionen strukturell ausgezeichnet werden. Auf diese Weise entsteht eine maschinenlesbare, semantisch klar definierte Datenbasis als Grundlage für die digitale Edition.

## 2. Herausforderungen der Datenaufbereitung

Die Datenaufbereitung ist durch mehrere Herausforderungen gekennzeichnet:

- Die kapitelweise gegliederte Struktur des aus einem PDF entnommenen Textes muss beim Übergang in TEI/XML zuverlässig erkannt und abgebildet werden.
- In jedem Kapitel folgen lateinischer Text, griechische Übersetzung und deutsche Übersetzung in fester Reihenfolge; diese Beziehungen müssen in der XML-Struktur eindeutig modelliert werden.
- Da im .docx-Dokument keine Anmerkungen enthalten sind, müssen sämtliche späteren Annotationen und Kommentare auf der strukturierten Textbasis aufbauen.
- Es soll eine Datenbasis entstehen, die für weitere Schritte wie Annotation, Kommentierung, Validierung, Visualisierung und Suche geeignet ist.

## 3. Rolle der TEI-Auszeichnung

Die TEI-konforme Auszeichnung dient dazu,

- Kapitelgrenzen formal zu markieren,
- die drei Sprachversionen strukturell zu unterscheiden und
- die Textdaten so zu organisieren, dass sie maschinell lesbar und semantisch klar definiert sind.

Die TEI-Struktur bildet die technische Grundlage für die spätere digitale Edition, in der Originaltext, Übersetzungen und Annotationen parallel dargestellt werden.

## 4. Unterstützung durch LLMs

LLMs unterstützen die Datenaufbereitung in mehreren Punkten:

- Sie helfen bei der automatischen Extraktion der Textstruktur aus der .docx-Datei, insbesondere bei der Identifikation der Kapiteleinteilung.
- Sie machen Vorschläge für TEI-Tagging, mit denen Kapitel, Sprachversionen und weitere strukturelle Einheiten ausgezeichnet werden können.

Alle von LLMs vorgeschlagenen Strukturen und Tags werden im Anschluss manuell überprüft, um wissenschaftliche Genauigkeit sicherzustellen. Damit verbindet die Datenaufbereitung automatisierte Unterstützung mit fachlich kontrollierter Entscheidungsfindung.

## 5. Ergebnis der Datenaufbereitung

Das Ergebnis der Datenaufbereitung ist eine TEI-konforme XML-Datei, in der

- die Kapiteleinteilung,
- die dreisprachige Struktur (Latein, Griechisch, Deutsch) und
- weitere strukturelle Einheiten

klar ausgezeichnet sind. Diese XML-Datei bildet die Grundlage für:

- die weitere Annotation von Personen, Orten und Ereignissen,
- die Kommentierung durch LLMs mit anschließender manueller Kontrolle,
- die Validierung der Annotationen,
- die Umsetzung der webbasierten digitalen Edition mit paralleler Darstellung und Downloadmöglichkeiten der strukturierten Daten.
