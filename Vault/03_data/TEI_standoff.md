# Wissensdokument: Authority- und Prosopographie-Daten als Stand-off Records in TEI (P5; Module *namesdates* + *linking*)

Dieses Dokument dient als Arbeitsgrundlage, um ein bestehendes TEI-XML (Text) mit **Authority-/Prosopographie-Daten** als **Stand-off Records** anzureichern und anschließend **jede Textreferenz stabil auf diese Records zu verlinken**.


**Stand (10. Januar 2026):** Inhaltlich gegengeprüft gegen die TEI P5 Guidelines (Kapitel *Names, Dates, People, and Places* / ND sowie *Linking, Segmentation, and Alignment* für `<standOff>`).

---

## 1. Zielbild und Prinzipien

### Ziel
- **Entitäten** (Personen, Orte, Organisationen, Ereignisse, Objekte, Namensformen) werden **einmal** als Records beschrieben.
- Im Fließtext werden Nennungen/Referenzen **nur noch verlinkt**, statt Information zu duplizieren.
- Unsicherheit, Quellenlage und Verantwortlichkeit werden **explizit** dokumentiert.

### Prinzipien
- **Single Source of Truth**: zentrale Entität = ein Record mit stabiler ID.
- **Trennung von Beleg und Aussage**: Textstelle ist Beleg; Record enthält die interpretierte Aussage.
- **Evidenz/Unsicherheit**: jede nicht-triviale Aussage kann *cert/resp/source* tragen.
- **Zeitdimension**: Zustände/Eigenschaften und Relationen können datiert werden.

---

## 2. Grundarchitektur im TEI-Dokument

### Platzierung (gültige Optionen)
- Das primäre Textmaterial bleibt in `<text>…</text>`.
- Die Authority-/Prosopographie-Daten liegen in `<standOff>` als eigenständigem Ressourcenkontainer (Modul *linking*) auf Ebene von `<TEI>` (Geschwisterelement von `<text>`).
- Die TEI macht **keine feste Reihenfolge**: `<standOff>` kann **vor oder nach** `<text>` stehen; viele Projekte platzieren es direkt nach `<teiHeader>`, weil es dort gut auffindbar ist.
- Falls du `<standOff>` **verschachteln** willst (Stand-off innerhalb Stand-off), muss das innere `<standOff>` ein `@type` besitzen.

Minimalgerüst:

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>…</teiHeader>

  <standOff>
    <!-- Authority/Prosopographie-Records -->
  </standOff>

  <text>
    <body>…</body>
  </text>
</TEI>
```

### Sammlungen (Listen) im Stand-off
Im `<standOff>` werden typischerweise Listen/Records aus dem Modul *namesdates* geführt (z. B. Personen, Orte, Organisationen); `<listRelation>/<relation>` (ebenfalls *namesdates*) ist für Prosopographie besonders nützlich und kann separat im `<standOff>` oder innerhalb einzelner Listen (z. B. innerhalb von `<listPerson>`) geführt werden.

Im `<standOff>` werden pro Entitätstyp Listen geführt:

- `<listPerson>` → `<person>`
- `<listPlace>` → `<place>`
- `<listOrg>` → `<org>`
- `<listEvent>` → `<event>`
- `<listObject>` → `<object>` (falls genutzt)
- `<listNym>` → `<nym>` (für Namensformen, optional)
- `<listRelation>` → `<relation>` (Beziehungen, sehr empfohlen)

---

## 3. Identifikatoren und Verlinkung

### Stabile IDs
- Jede Entität erhält ein **eindeutiges** `xml:id`.
- Konvention (Beispiel):
  - Person: `p_0001`, Ort: `pl_0001`, Org: `o_0001`, Event: `e_0001`, Objekt: `ob_0001`, Nym: `n_0001`

### Referenz im Text
- Verlinkung bevorzugt über `@ref="#ID"` (Pointer auf `xml:id`).
- `@key` nur als zusätzliches, projektspezifisches Kürzel (nicht als Primärreferenz).

Beispiel im Text:

```xml
<persName ref="#p_0001">Johann N.</persName>
<placeName ref="#pl_0003">Wien</placeName>
<orgName ref="#o_0002">Akademie</orgName>
```

Alternative (wenn du Nennungen generisch halten willst):

```xml
<rs type="person" ref="#p_0001">Johann N.</rs>
```

### URI-Strategie (optional, aber empfehlenswert)
Wenn Authority-Dateien ausgelagert werden (separate TEI-Datei), kann `@ref` als URI geführt werden, z. B.:
- `ref="authority.xml#p_0001"` oder ein http(s)-URI.

---

## 4. Record-Muster je Entitätstyp

### 4.1 Person (`<person>`)
Ziel: kanonische Identität + Namensvarianten + biographische Aussagen.

Minimaltemplate:

```xml
<listPerson>
  <person xml:id="p_0001">
    <persName>
      <forename>Johann</forename>
      <surname>Novak</surname>
    </persName>

    <!-- optionale Identifier -->
    <idno type="GND">…</idno>
    <idno type="VIAF">…</idno>

    <!-- optionale Aussagen -->
    <birth when="1832-05-14"/>
    <death notBefore="1901" notAfter="1903"/>

    <occupation>Jurist</occupation>

    <!-- Dokumentation/Begründung -->
    <note resp="#ed_001" cert="medium">Identifikation beruht auf …</note>
  </person>
</listPerson>
```

Hinweise:
- Mehrere `<persName>` sind zulässig (z. B. Varianten, Sprachformen, Namenswechsel).
- Namenskomponenten (forename/surname/addName/roleName/genName/nameLink) sind hilfreich für Normalisierung und Auswertbarkeit.
- Eigenschaften können als **Traits** (stabil) oder **States** (zeitlich) modelliert werden, je nach Detailgrad. Wenn du konsequent „stabil vs. zeitgebunden“ trennen willst, nutze `<trait>` und `<state>`.

---

### 4.2 Ort (`<place>`)
Ziel: Name(n), Lokation(en), administrative Einordnung, ggf. historische Zustände.

Minimaltemplate:

```xml
<listPlace>
  <place xml:id="pl_0003">
    <placeName>Wien</placeName>

    <location>
      <geo>48.2082 16.3738</geo>
    </location>

    <note source="#bibl_001" cert="high">Koordinaten nach …</note>
  </place>
</listPlace>
```

Erweiterungen:
- Mehrere `<placeName>` für Varianten (historische Namen, Mehrsprachigkeit).
- Komplexe Geometrien (z. B. Polygone) sind möglich; für viele Projekte reichen `geo`-Punkte.
- Politisch-administrative Zugehörigkeiten können als datierte Zustände modelliert werden (z. B. „Teil von X zwischen …“), idealerweise zusätzlich als Relation (siehe Abschnitt 5).

---

### 4.3 Organisation (`<org>`)
Ziel: Organisationsidentität, Namensformen, Struktur, Zugehörigkeiten.

Minimaltemplate:

```xml
<listOrg>
  <org xml:id="o_0002">
    <orgName>Akademie der Wissenschaften</orgName>
    <idno type="ROR">…</idno>

    <note resp="#ed_001" cert="medium">Abgleich über …</note>
  </org>
</listOrg>
```

Erweiterungen:
- Verschachtelung/Struktur: Organisationen können Untereinheiten enthalten oder über Relationen verbunden werden.
- Datierte Zustände: Name/Status/Standortwechsel.

---

### 4.4 Ereignis (`<event>`)
Ziel: Ereignis als identifizierbarer Knoten mit Datum/Ort/Teilnehmern.

Minimaltemplate:

```xml
<listEvent>
  <event xml:id="e_0001" when="1914-06-28">
    <label>Attentat von Sarajevo</label>
    <desc>…</desc>
    <placeName ref="#pl_0100">Sarajevo</placeName>
  </event>
</listEvent>
```

Hinweise:
- Ereignisse eignen sich als **Anker** für biographische Aussagen („Person nahm teil“, „Person erhielt Amt“, etc.), oft zusammen mit Relationen.

---

### 4.5 Objekt (`<object>`) (optional)
Nur nutzen, wenn Objekte als erstklassige Entitäten relevant sind (z. B. Artefakte, Werke, Insignien).

```xml
<listObject>
  <object xml:id="ob_0001">
    <objectName>…</objectName>

    <!-- optionale Identifier (z. B. GND, Wikidata, Inventarnummer) -->
    <idno type="GND">…</idno>

    <note>…</note>
  </object>
</listObject>
```

---

### 4.6 Namensformen (`<listNym>/<nym>`) (optional, aber wertvoll bei Namensvarianten)
Wenn du **die Namensform selbst** als kontrolliertes Objekt führen willst (z. B. Variantenmanagement, Onomastik):

```xml
<listNym>
  <nym xml:id="n_0007">
    <form>Johann Novak</form>
    <note>Kanonische Form</note>
  </nym>
</listNym>
```

Verknüpfung aus dem Text bzw. aus Namelementen über `@nymRef`:

```xml
<persName ref="#p_0001" nymRef="#n_0007">Johann N.</persName>
```

---

## 5. Beziehungen und Netzwerke: `<listRelation>` / `<relation>`

### Warum Relationen zentral sind
Prosopographie lebt von Kanten: Verwandtschaft, Patronage, Mitgliedschaft, Arbeitsverhältnisse, Ortszugehörigkeiten, Ereignisteilnahmen.

### Muster
- `@active` und `@passive` für gerichtete Relationen
- `@mutual` für ungerichtete/reziproke Relationen
- `@name` (oder projektinterne Taxonomie) für Relationstyp
- **Mindestens eines** von `@name`, `@ref` oder `@key` muss gesetzt sein.
- Konsistenzregeln: `@passive` nur zusammen mit `@active`; `@mutual` nicht zusammen mit `@active/@passive`.
- Optional datierbar (z. B. `when`, `from/to`, `notBefore/notAfter`)

Beispiel: Mitgliedschaft/Anstellung (Person → Organisation)

```xml
<listRelation>
  <relation xml:id="r_0001"
            name="memberOf"
            active="#p_0001"
            passive="#o_0002"
            notBefore="1880"
            notAfter="1890"
            resp="#ed_001"
            cert="medium"/>
</listRelation>
```

Beispiel: „Ort ist Teil von Ort“ (hierarchisch, historisch variabel)

```xml
<relation xml:id="r_0102"
          name="partOf"
          active="#pl_0003"
          passive="#pl_0001"
          from="1850"
          to="1918"/>
```

Empfehlung:
- Lege eine **kontrollierte Liste von Relationstypen** fest (kleines Vokabular) und dokumentiere sie projektintern.

---

## 6. Datierung: Normalformen und Unsicherheit

### Kernregeln
- Punktdatum: `@when="YYYY-MM-DD"` (oder nur Jahr/Monat, wenn erlaubt/gewollt).
- Zeitraum: `@from` + `@to`.
- Unsicherheit: `@notBefore` + `@notAfter`.
- **Nicht mischen**: `@when` nicht zusammen mit `from/to` oder `notBefore/notAfter`.

Beispiele:

```xml
<birth when="1832-05-14"/>
<death notBefore="1901" notAfter="1903"/>
<relation name="inOffice" active="#p_0001" passive="#o_0002" from="1888-01-01" to="1892-12-31"/>
```

### Nicht-gregorianische Kalender (falls relevant)
- Kalenderbeschreibung im Header (Projektentscheid).
- Datumsangaben können zusätzlich mit kalenderbezogenen Attributen geführt werden; als Arbeitsregel: **immer auch eine gregorianische Entsprechung** dokumentieren, wenn möglich (für Suche/Sortierung).

---

## 7. Quellen, Verantwortlichkeit, Sicherheit

### Attribute (praktischer Kern)
- `@source` → Beleg/Quelle (z. B. auf `<bibl xml:id="…">`)
- `@resp` → Verantwortliche Person/Stelle (z. B. Editor*in, Team)
- `@cert` → Sicherheit (TEI-Standard: `high|medium|low|unknown`; projektspezifische Skalen sind möglich, sollten aber auf diese Werte abbildbar sein)

Beispiel:

```xml
<person xml:id="p_0001" source="#bibl_003" resp="#ed_001" cert="medium">
  …
</person>
```

Empfehlung:
- Pflege ein kleines Register im Header oder Stand-off für Verantwortliche (`<respStmt>`-Logik) und Bibliographie (`<listBibl>`), damit `@resp` und `@source` stabil verweisen können.

---

## 8. Verlinkungsstrategie im Fließtext (Minimal, aber konsistent)

### Empfohlene Minimalmarkierung
- Personen: `<persName ref="#p_…">…</persName>`
- Orte: `<placeName ref="#pl_…">…</placeName>`
- Orgs: `<orgName ref="#o_…">…</orgName>`
- Ereignisse: `<eventName ref="#e_…">…</eventName>` (oder `<rs type="event" …>`)

Wenn du Nennungen zunächst nur generisch auszeichnen willst (z. B. aus NLP-Outputs), nutze `<rs type="…">` und migriere später zu `<persName>/<placeName>/…`.

---

## 9. Arbeitsworkflow für die Annotation (bewährt und skalierbar)

1. **Entity Harvesting**
   - Alle Nennungen im Text sammeln (Person/Ort/Org/Event/Object).
   - Dubletten/Varianten clustern.

2. **Authority Record Creation**
   - Für jedes Cluster einen Record anlegen (`xml:id` vergeben).
   - Namensvarianten als zusätzliche Name-Elemente hinzufügen.
   - Quellen/resp/cert konsequent setzen.

3. **Text Linking**
   - Jede Nennung mit `@ref` auf den Record verlinken.
   - Bei unsicheren Zuordnungen: `cert="low"` und Begründungsnote im Record (oder an der Textstelle).

4. **Relations Layer**
   - Beziehungen aus Text/Records ableiten und in `<listRelation>` modellieren.
   - Wenn möglich datieren.

5. **Validierung**
   - Prüfen: eindeutige IDs, keine toten `@ref`-Pointer, konsistente Relationstypen, keine widersprüchlichen Datierungen.

---

## 10. Startvorlage für ein vollständiges Stand-off-Gerüst

```xml
<standOff>

  <listPerson>
    <!-- <person xml:id="p_0001">…</person> -->
  </listPerson>

  <listPlace>
    <!-- <place xml:id="pl_0001">…</place> -->
  </listPlace>

  <listOrg>
    <!-- <org xml:id="o_0001">…</org> -->
  </listOrg>

  <listEvent>
    <!-- <event xml:id="e_0001">…</event> -->
  </listEvent>

  <listObject>
    <!-- optional -->
  </listObject>

  <listNym>
    <!-- optional -->
  </listNym>

  <listRelation>
    <!-- <relation xml:id="r_0001" name="…" active="…" passive="…"/> -->
  </listRelation>

</standOff>
```

---

## 11. Projektentscheidungen, die du jetzt festlegen solltest (damit alles nachher sauber bleibt)

- **ID-Konvention** (Präfixe, Nummerierung, Stabilität über Versionen)
- **Relationstyp-Vokabular** (z. B. `memberOf`, `employedBy`, `bornIn`, `diedIn`, `partOf`, `marriedTo`, `correspondedWith`, `participantIn`)
- **Cert-Skala** (z. B. `high|medium|low`)
- **Quellenmodell** (`@source` auf `<bibl>` vs. externe URIs)
- **Umgang mit Mehrdeutigkeit** (ein Record vs. mehrere Kandidaten; wie dokumentiert)
