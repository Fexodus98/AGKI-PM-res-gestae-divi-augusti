# TEI-Inferenz-Workflow (Kapitel → TEI-XML mit Stand-off)

Dieses Dokument beschreibt, wie aus den einzelnen Kapitel-Markdown-Dateien (`Vault/03_data/chapters/Res_Gestae_Divi_Augusti_*.md`) mithilfe eines LLM-Inference-API-Calls valide TEI-P5-XML-Dateien erzeugt werden, inklusive Stand-off-Annotationen. Ziel ist ein abschließendes, zusammengefügtes TEI-Dokument mit vollständigen Entitätsannotationen (Personen, Orte, Jahreszahlen, Events, Organisationen) in allen drei Sprachfassungen.

## Zielbild
- Pro Kapitel eine TEI-Datei mit:
  - TEI-Header (minimales `fileDesc`, `profileDesc/langUsage` für `la`, `grc`, `de`)
  - `<text>` mit `<div type="chapter">` und drei `<div type="version" xml:lang="…">` (Latin/Greek/German), jeweils Absatz-IDs (`xml:id="la|grc|de-sXX-pYY"`).
  - Inline-Basisannotationen durch den LLM (falls gewünscht): `<persName>`, `<placeName>`, `<orgName>`, `<date>`, `<event>`, `<name type="…">`.
  - `<standOff>` mit:
    - `listPerson`, `listPlace`, `listOrg`, `listEvent` (optional), `listDate` (optional) mit `note type="desc"`-Kurzbeschreibungen.
    - `linkGrp` für Entitätsreferenzen (`type="entity-mention"` mit `targFunc="entity text text text"`, Targets verweisen auf die drei Sprachsegmente).
    - `linkGrp` für Übersetzungs-Alignment (bestehend: `lg-translation`).
- Abschluss: Merge aller Kapitel-TEI in ein Gesamt-TEI (`Res_Gestae_Divi_Augusti.xml`) mit konsolidiertem Stand-off (Union aller `list*` + zusammengeführte `linkGrp`), IDs stabil und eindeutig.

## Eingaben
- Kapitel-Markdown aus `Vault/03_data/chapters/Res_Gestae_Divi_Augusti_*.md`.
- Wunschliste der zu annotierenden Entitätstypen (Start-Set):
  - Personen (`persName`, `listPerson`)
  - Orte (`placeName`, `listPlace`)
  - Organisationen (`orgName`, `listOrg`)
  - Ereignisse (`event`, `listEvent`; ggf. `name type="event"`)
  - Jahreszahlen/Datumsangaben (`date`/`time`, `listDate` optional)
  - Übersetzungs-Alignment (`linkGrp type="translation"`)

## LLM-Inference-Call (pro Kapitel)
Beispiel-Prompt-Skizze:
```
System: Du erzeugst TEI-P5-XML. Halte dich strikt an TEI-Syntax (Namespace http://www.tei-c.org/ns/1.0). Keine DOCTYPE.
User: Hier ist Markdown eines Kapitels (Latein/Griechisch/Deutsch, mit Headings). Erzeuge TEI:
- Struktur: <TEI><teiHeader>…</teiHeader><standOff>…</standOff><text><body><div type="chapter" n="NN">…</div></body></text></TEI>
- Drei Sprachabschnitte als <div type="version" xml:lang="la|grc|de"> mit <p xml:id="la|grc|de-sNN-pYY">…
- Annotiere Personen/Orte/Org/Ereignisse/Jahreszahlen im Fließtext: setze passende TEI-Elemente (<persName>, <placeName>, <orgName>, <event>, <date>).
- **WICHTIG**: Annotiere alle Referenzen auf die erste Person (Deutsch: 'ich', 'mich', 'mir', 'mein...'; Latein: 'ego', 'me', 'mihi', 'meus...'; Griechisch: 'ἐγώ', 'ἐμοῦ', 'ἐμοί'...) explizit als `<persName ref="#augustus">Wort</persName>`.
- Baue <standOff>:
  - <listPerson>/<person xml:id="…"><persName/><note type="desc">Kurze Beschreibung aus Kontext</note></person>
  - <listPlace>/<place …><placeName/><note type="desc">…</note></place>
  - <listOrg>/<org …>…
  - (optional) <listEvent>, <listDate>
  - <linkGrp xml:id="lg-translation" type="translation" targFunc="latin greek german">: ein <link> je Absatz-Dreier; **muss in jeder Kapitel-TEI vorhanden sein** und beim Merge übernommen/vereinigt werden, sodass Übersetzungen auch kapitelintern verlinkt sind.
  - <linkGrp xml:id="lg-entity-mentions" type="entity-mention" targFunc="entity text text text">: <link target="#ENT #la-sNN-pYY #grc-sNN-pYY #de-sNN-pYY"/> für jede erkannte Entität
Output: TEI als UTF-8-String, keine Erklärungen.
Kapitel-Markdown:
<<<CHAPTER_MARKDOWN>>>
```

## Verarbeitungsschritte
1. **Kapitel iterieren (UTF-8 erzwingen)**: Für jedes `Res_Gestae_Divi_Augusti_*.md` den LLM-Call durchführen und TEI-Output **immer als UTF-8** speichern (z. B. `chapters_tei/Res_Gestae_Divi_Augusti_XX.xml`). Eingabe-Prompt weist explizit auf UTF-8-Ausgabe hin.
2. **IDs prüfen**: Sicherstellen, dass `xml:id` pro Entitätstyp stabil und eindeutig bleiben (z. B. Präfixe `pers-XX`, `place-XX`, `org-XX`, `event-XX`). Beim Merge deduplizieren.
3. **Stand-off mergen**:
   - `listPerson`/`listPlace`/`listOrg`/`listEvent` vereinigen (nach `xml:id`).
   - `linkGrp lg-entity-mentions` zusammenführen (alle Links sammeln, Duplikate entfernen).
   - `lg-translation` Links anhängen (Abschnittsnummern je Kapitel).
4. **Text mergen**:
   - Alle `<div type="chapter">` in ein gemeinsames `<group>` oder `<body>` unter `<text>` einfügen.
   - Sprachstrukturen konsistent halten (`xml:lang="la/grc/de"`).
5. **Validierung**:
   - Well-Formedness (XML-Parser; UTF-8).
   - TEI-P5-RelaxNG/Schéma prüfen (z. B. `jing` gegen `tei_all.rng` oder `xmllint --relaxng`).
   - LLM-as-a-Judge (optional, second-pass): Kapitel-TEI an LLM geben mit Checkliste (Namespace, erwartete Elemente/Attribute, `linkGrp`-Vollständigkeit, IDs eindeutig), Rückmeldung parsen und ggf. automatisiert nachbessern.
   - Fixe Validierung bevorzugen; LLM-Check nur ergänzend nutzen, nicht als alleinige Quelle.
6. **Finale Datei**: `Vault/03_data/Res_Gestae_Divi_Augusti_merged.xml` (oder Überschreiben der bestehenden `Res_Gestae_Divi_Augusti.xml`), mit vollständigem Stand-off.

## Hinweise zur ID-Strategie
- Personen: `pers-XXXX` (z. B. pers-augustus, pers-antonius)
- Orte: `place-XXXX` (z. B. place-rome, place-actium)
- Organisationen: `org-XXXX`
- Ereignisse: `event-XXXX`
- Jahreszahlen: `date-YYYY` (optional)

## Global Entity Registry (Konsistenz)
Um sicherzustellen, dass Entitäten über alle Kapitel hinweg dieselben IDs erhalten (z. B. immer `xml:id="augustus"` statt mal `augustus` und mal `imp_caesar`), nutzt das Skript eine **Registry** (`Vault/03_data/entity_registry.json`).
- **Input**: Vor jedem Call werden die bereits bekannten Entitäten (Name -> ID) in den Prompt injiziert.
- **Output**: Nach jedem erfolgreichen Generieren werden neue Entitäten aus dem Output-XML extrahiert und der Registry hinzugefügt.

## Output-Ablage
- Einzel-TEI pro Kapitel: `Vault/03_data/chapters_tei/Res_Gestae_Divi_Augusti_XX.xml`
- Zusammengeführtes TEI: `Vault/03_data/Res_Gestae_Divi_Augusti_merged.xml`

Damit ist der Ablauf reproduzierbar: Markdown → LLM-Inferenz pro Kapitel → TEI + Stand-off → Merge zu vollständigem TEI mit Annotationen in drei Sprachen.
