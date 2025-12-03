
# Data – Quellen, Modell & Kontextwissen

Siehe Projektplanung: [[WorkPackages]] · [[Roadmap]] · [[Projektplan]]  
Siehe Nutzeranforderungen: [[UserStories]]  
Siehe technische Umsetzung: [[Specs]]  
Siehe Detailbeschreibung der Datenaufbereitung: [[Datenaufbereitung]]  
Siehe TEI-Linking-Konzept: [[TEI-linkGrp]]

---

## 1. Datenquellen (Übersicht)

Die detaillierte Beschreibung der Datenbasis findet sich in [[Datenaufbereitung]]. Hier die komprimierte Übersicht:

- Primärquelle: eine `.docx`-Datei mit dem Text der *Res gestae divi Augusti* in:
  - lateinischer Originalsprache,
  - griechischer Übersetzung,
  - deutscher Übersetzung.
- Struktur:
  - kapitelweise organisiert,
  - pro Kapitel drei Sprachfassungen in derselben Reihenfolge,
  - keine editorischen Kommentare im `.docx` (nur im ursprünglichen PDF).

Ziel ist eine TEI-konforme XML-Struktur, die:

- die dreisprachige Textstruktur explizit abbildet,
- Kapitel, Abschnitte und ggf. Sätze klar identifizierbar macht,
- als Grundlage für Annotation, Kommentierung und Web-Ausgabe dient.

---

## 2. TEI-Datenmodell (Entitäten & Struktur)

### 2.1 Strukturelle Einheiten

**TextSegment**

- Repräsentiert eine Text-Einheit, z. B. Kapitel, Abschnitt, Absatz.
- Mögliche TEI-Implementierung:
  - `<div type="chapter">` für Kapitel,
  - `<div type="section">` oder `<p>` für Untereinheiten.
- Attribute (Beispiele):
  - `@xml:id` – eindeutige ID pro Segment,
  - `@type` – z. B. `chapter`, `section`, `paragraph`,
  - `@xml:lang` – Sprache (`"lat"`, `"grc"`, `"deu"`).

Ziel: Für jedes Kapitel/Segment sollen die drei Sprachversionen klar zugeordnet und ggf. verlinkt werden (z. B. via `<linkGrp>`, siehe [[TEI-linkGrp]]).

### 2.2 Referenzierte Entitäten

**Person (`Person`)**

- TEI-Element: `<persName>`
- Felder/Attribute:
  - `@xml:id` (eindeutige ID),
  - Inhalt: Name im Text,
  - optional: `@role` (z. B. „Kaiser“, „Senator“, „Verwandte“),
  - Verknüpfung zu externen Ressourcen möglich.

**Ort (`Place`)**

- TEI-Element: `<placeName>`
- Felder/Attribute:
  - `@xml:id`,
  - Name des Ortes,
  - optional: Referenzen/Koordinaten.

**Konzept / Sachbegriff (`Concept`)**

- TEI-Element: z. B. `<term>` oder bestimmte `<note>`-Strukturen.
- Felder:
  - `id`,
  - `label` (Begriff),
  - `description` (kurze Erklärung).

### 2.3 Beziehungen

- Ein `TextSegment` kann 0..n Referenzen auf `Person`, `Place` und `Concept` enthalten.
- Technisch:
  - eingebettete Elemente wie `<persName>`, `<placeName>`, `<term>` im laufenden Text,
  - zusätzliche Annotationen (z. B. `<note>`), die auf `@xml:id` eines Segments verweisen.

Für die Verknüpfung paralleler Sprachversionen und ggf. Kommentar-/Anmerkungsebenen wird TEI `<linkGrp>` eingesetzt (siehe [[TEI-linkGrp]]).

---

## 3. Ontologie (Semantic Markdown)

### 3.1 Kernbegriffe

**„Res gestae divi Augusti“**

- Selbstbiographische Inschrift des Augustus.
- Wird im Projekt als dreisprachiger Textkorpus (lat/grc/deu) bearbeitet.
- Zentraler Referenztext für Personen, Orte und politische Begriffe der frühen römischen Kaiserzeit.

**„Digitale Edition“**

- TEI-basierte, strukturierte Darstellung des Textes.
- Enthält Annotationen (Personen, Orte, Konzepte) und ggf. Kommentare.
- Wird über eine Weboberfläche zugänglich gemacht, inkl. paralleler Darstellung der Sprachversionen.

**„Annotation“**

- Zusätzliche Information, die einem Textsegment oder Token zugeordnet wird.
- Beispiele:
  - Identifikation historischer Akteure,
  - Georeferenzierung von Orten,
  - Erklärung politischer Begriffe.
- Kann manuell oder KI-gestützt erstellt werden.

**„KI-Annotation“**

- Annotationen, die mithilfe eines LLM erzeugt oder vorbereitet werden.
- Aufgaben:
  - Vorschläge für Entitäten (Personen, Orte, Konzepte),
  - Vorschläge für Relationen,
  - Generierung kurzer Erläuterungen.
- Muss durch Fachpersonen geprüft und ggf. korrigiert werden.

---

## 4. Prozesse / Pipelines

### 4.1 Pipeline: `.docx` → TEI-XML

1. **Import der `.docx`-Quelle**
   - Extraktion der Textinhalte (lat/grc/deu).
   - Erkennung der Kapiteleinteilung.

2. **Segmentierung**
   - Erstellung von `TextSegment`-IDs pro Kapitel und ggf. Untereinheit.
   - Zuordnung der drei Sprachversionen zu denselben Segment-IDs.

3. **TEI-Grundstruktur**
   - Aufbau des TEI-Headers (Metadaten).
   - Abbildung der Kapitel/Abschnitte in `<div>`/`<p>` mit `@xml:lang`.

4. **Anreicherung mit TEI-Tags**
   - Markierung von Personen, Orten, zentralen Begriffen.
   - Vorbereitung für spätere KI-Annotation.

5. **Validierung**
   - Prüfung gegen TEI-Schema.
   - Konsistenzchecks (z. B. vollständige dreisprachige Segmentstruktur).

Ausführlicher: [[Datenaufbereitung]]

### 4.2 Pipeline: TEI → KI-Annotation

1. **Segmentauswahl**
   - Identifikation der zu annotierenden TEI-Segmente.

2. **Prompt-Erstellung**
   - Projektkontext (vgl. [[Forschungsblog-Text]] / [[Projektplan]]).
   - Information zur TEI-Struktur (Segment-IDs, Sprache).
   - klare Vorgabe des gewünschten Ausgabeformats.

3. **LLM-Aufruf**
   - Ausführen der Anfragen an ein LLM.
   - Sammeln der Vorschläge für Entitäten und Annotationen.

4. **Review / Postprocessing**
   - Prüfung der LLM-Ergebnisse durch Fachpersonen.
   - Anpassung an das interne Datenmodell.

5. **Integration**
   - Einbau der geprüften Annotationen in TEI und/oder ergänzende Strukturen (z. B. JSON).

---

## 5. Token-effiziente Darstellung für LLMs

- **Redundanzen vermeiden**
  - Begriffe und Strukturen sind hier definiert.
  - In Prompts nur kurz referenzieren, statt sie vollständig zu wiederholen.

- **IDs konsequent nutzen**
  - Textsegmente über `@xml:id` referenzieren.
  - Annotationen immer auf IDs beziehen.

- **Strukturierte Formate bevorzugen**
  - nummerierte Listen,
  - klar benannte Felder (z. B. `type`, `target`, `description`),
  - einfache Pseudo-JSON- oder Listenformate.

- **Minimaler Kontext**
  - nur relevante Textausschnitte mitsenden,
  - wiederverwendbare Prompt-Templates etablieren.

Dieses Dokument fungiert als „Hub“ für LLM-Kontext. Tiefere Details liegen in [[Datenaufbereitung]] und [[TEI-linkGrp]].
