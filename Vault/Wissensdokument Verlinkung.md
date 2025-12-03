
````markdown
# TEI-Element `<linkGrp>` – Wissensdokument (P5 4.10.2, 2025)

## 1. Zweck und Rolle von `<linkGrp>`

**Definition:**  
`<linkGrp>` („link group“) dient zur Bündelung von Verknüpfungen – also einer **Menge von Assoziationen oder Hyperlinks** – in einem gemeinsamen Container. Es ist ein zentrales Element im Modul:

- **Modul:** `linking — Linking, Segmentation, and Alignment` :contentReference[oaicite:0]{index=0}  

Typische Einsatzszenarien:

- Alignment von Übersetzungen (z. B. Satzpaare in verschiedenen Sprachen)  
- Verknüpfung von Noten und Textstellen (Kommentarapparat)  
- Kodierung semantischer Relationen (Periphrasen, Referenzketten, Sprecherreferenzen etc.) :contentReference[oaicite:1]{index=1}  

`<linkGrp>` ist dabei vor allem:

- ein **administrativer Container** für Links (und ggf. Pointer),  
- eine Möglichkeit, **gemeinsame Eigenschaften** (z. B. `@type`) für alle enthaltenen `<link>`-Elemente festzulegen.

---

## 2. Einordnung in TEI

### 2.1 Modul und Klassen

- **Modul:** `linking` – „Linking, Segmentation, and Alignment“ :contentReference[oaicite:2]{index=2}  
- **Mitglied von:** `model.global.meta` – `<linkGrp>` kann als Metadatenstruktur an vielen Stellen im Dokument auftreten.

`<linkGrp>` trägt u. a. folgende Attributklassen:

- `att.global` (inkl. `@xml:id`, `@xml:lang`, `@n`, `@xml:base`, `@xml:space`)  
- `att.global.analytic` (`@ana`)  
- `att.global.change` (`@change`)  
- `att.global.facs` (`@facs`)  
- `att.global.linking` (`@corresp`, `@sameAs`, `@copyOf`, `@next`, `@prev`, `@exclude`, `@select`, `@synch`)  
- `att.global.rendition` (`@rend`, `@style`, `@rendition`)  
- `att.global.responsibility` (`@cert`, `@resp`)  
- `att.global.source` (`@source`)  
- `att.cmc` (`@generatedBy`) :contentReference[oaicite:3]{index=3}  

Spezifisch für Link-Gruppen:

- `att.pointing.group`
  - `@domains`: schränkt die zulässigen Zielbereiche (Elemente) ein, auf die sich die Links beziehen sollen.  
  - `@targFunc`: beschreibt die **Funktion** der einzelnen Ziel-IDs in `@target` der enthaltenen `<link>`-Elemente.  
- `att.pointing`
  - u. a. `@targetLang`, `@target`, `@evaluate` – allgemeine Pointer-Attribute.  
- `att.typed`
  - `@type`, `@subtype`: zur semantischen Typisierung der Link-Gruppe. :contentReference[oaicite:4]{index=4}  

### 2.2 Mögliche Kontexte („Contained by“)

`<linkGrp>` kann in sehr vielen Kontexten stehen, u. a.:

- textstrukturell: `<body>`, `<div>`, `<group>`, `<front>`, `<back>`  
- stand-off: `<standOff>`  
- segmentbasiert: `<seg>`, `<ab>`  
- in verschiedenen Beschreibungsteilen (z. B. `msdescription`, `namesdates`, `figures`, `verse` etc.) :contentReference[oaicite:5]{index=5}  

Wichtig in der Praxis:

- **Innerhalb von `<standOff>`**: für externe Alignments, z. B. zwischen mehreren TEI-Dokumenten.  
- **Innerhalb von `<body>` oder `<div>`**: wenn Alignments im selben Dokument mitlaufen sollen.

---

## 3. Inhalt und Struktur von `<linkGrp>`

### 3.1 Erlaubte Kindelemente

`<linkGrp>` darf enthalten: :contentReference[oaicite:6]{index=6}  

- beliebig viele optionale **Beschreibungen**:
  - Elemente aus `model.descLike`, z. B. `<desc>`  
- danach eine oder mehrere **Verknüpfungen**:
  - `<link>`  
  - `<ptr>`

Formal (vereinfacht):

```text
linkGrp = ( desc* , ( link | ptr )+ )
````

### 3.2 Inhaltliche Funktion

- `<link>` kodiert eine **Relation zwischen mindestens zwei Zielen** (`@target` mit ≥ 2 IDs). Die Position von `<link>` im Dokument ist semantisch normalerweise unerheblich; Bedeutung kommt über `@target` zustande. ([tei-c.org](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-link.html?utm_source=chatgpt.com "TEI element link (link)"))
    
- `<ptr>` ist ein allgemeiner Pointer und kann innerhalb von `<linkGrp>` ebenfalls genutzt werden, um z. B. externe Ressourcen oder andere Link-Sets zu referenzieren.
    

---

## 4. Attribute im Detail

### 4.1 Typisierung: `@type` und `@subtype`

Über `@type` (und optional `@subtype`) wird festgelegt, **welche Art von Links** in dieser Gruppe gesammelt werden, z. B.:

- `type="translation"` – Übersetzungs-Alignments
    
- `type="imitation"` – Imitationsbeziehungen zw. Text und Quelle ([tei-c.org](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html?utm_source=chatgpt.com "17 Linking, Segmentation, and Alignment - The TEI ..."))
    
- `type="periphrasis"` – periphrastische Ausdrücke für denselben Referenten ([tei-c.org](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-link.html?utm_source=chatgpt.com "TEI element link (link)"))
    

Wichtig:

- `<link>`-Elemente erben standardmäßig den `@type`-Wert von der umgebenden `<linkGrp>`.
    
- Abweichende Typen können auf einzelnen `<link>`-Elementen überschrieben werden (falls nötig).
    

### 4.2 `@domains`

- Spezifiziert die **identifizierten Elemente** (per `@xml:id`), innerhalb derer alle Ziele dieser Linkgruppe liegen sollen.
    
- Typischer Einsatz: Eingrenzung auf bestimmte Dokumentbereiche wie:
    
    ```xml
    <linkGrp type="translation" domains="#lat #deu #grc">
       ...
    </linkGrp>
    ```
    
    → Alle `@target`-IDs der enthaltenen `<link>`-Elemente liegen in diesen drei Bereichen (z. B. `<div xml:id="lat">`, `<div xml:id="deu">`, `<div xml:id="grc">`). ([tei-c.org](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html?utm_source=chatgpt.com "17 Linking, Segmentation, and Alignment - The TEI ..."))
    

### 4.3 `@targFunc`

- Beschreibt die **Funktion** jedes Zieles in `@target` der untergeordneten `<link>`-Elemente.
    
- Der Wert besteht aus einer **Liste von Funktionsbezeichnern**, deren Anzahl der Anzahl der Ziel-IDs in `@target` entspricht (Positionen korrespondieren).
    
- Beispiel:
    
    ```xml
    <linkGrp type="translation"
             targFunc="source translation translation">
      <link target="#la1 #de1 #gr1"/>
    </linkGrp>
    ```
    
    - `#la1` → Funktion „source“
        
    - `#de1`, `#gr1` → Funktion „translation“ ([tei-c.org](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html?utm_source=chatgpt.com "17 Linking, Segmentation, and Alignment - The TEI ..."))
        

---

## 5. Typische Anwendungsfälle mit Beispielen

### 5.1 Übersetzungs-Alignment (französisch–englisch)

Offizielles Beispiel (vereinfacht paraphrasiert) zeigt ein Satz-Alignment:

```xml
<linkGrp type="translation">
  <link target="#CCS1 #SW1"/>
  <link target="#CCS2 #SW2"/>
  <link target="#CCS  #SW"/>
</linkGrp>

<div type="volume" xml:id="CCS" xml:lang="fr">
  <p>
    <s xml:id="CCS1">Longtemps, je me suis couché de bonne heure.</s>
    <s xml:id="CCS2">Parfois, à peine ma bougie éteinte, ...</s>
  </p>
</div>

<div type="volume" xml:id="SW" xml:lang="en">
  <p>
    <s xml:id="SW1">For a long time I used to go to bed early.</s>
    <s xml:id="SW2">Sometimes, when I had put out my candle, ...</s>
  </p>
</div>
```

Interpretation:

- Die Linkgruppe `type="translation"` enthält drei `<link>`-Elemente:
    
    - zwei Satz-Alignments (`CCS1`↔`SW1`, `CCS2`↔`SW2`)
        
    - ein Alignment auf Volume-Ebene (`CCS`↔`SW`) ([tei-c.org](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-linkGrp.html?utm_source=chatgpt.com "TEI element linkGrp (link group)"))
        

### 5.2 Imitationsbeziehungen (Kommentarapparat)

Im Kapitel 17 der Guidelines gibt es ein Beispiel, wie Annotationen mit ihren Zielversen verbunden werden:

```xml
<linkGrp type="imitation">
  <link target="#n2.79 #L2.79"/>
  <link target="#n2.88 #L2.88"/>
  <link target="#n3.284 #L3.284"/>
</linkGrp>
```

- Jede `<link>`-Relation verbindet eine **Note** (`#n2.79`, `#n2.88`, …) mit einer **Verszeile** (`#L2.79`, `#L2.88`, …).
    
- `type="imitation"` signalisiert, dass es um Nachahmungsverhältnisse (z. B. gegenüber einer antiken Quelle) geht. ([tei-c.org](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html?utm_source=chatgpt.com "17 Linking, Segmentation, and Alignment - The TEI ..."))
    

### 5.3 Periphrasen (gleicher Referent, verschiedene Ausdrücke)

Beispiel aus der `<link>`-Dokumentation:

```xml
<linkGrp type="periphrasis">
  <link target="#R1 #R3 #R4"/>
  <link target="#R2 #R5"/>
</linkGrp>
```

- Erste Relation: mehrere Ausdrücke für dieselbe Person (z. B. „Prison inmate“, Name, „fighter“)
    
- Zweite Relation: mehrere Ausdrücke für denselben Ort (z. B. „Rahway State Prison“ und „penitentiary“) ([tei-c.org](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-link.html?utm_source=chatgpt.com "TEI element link (link)"))
    

---

## 6. Best Practices für Projekte

### 6.1 Wann `<linkGrp>` benutzen?

- Wenn mehrere `<link>`- oder `<ptr>`-Elemente logisch zusammengehören:
    
    - Übersetzungs-Alignments
        
    - Text–Kommentar-Beziehungen
        
    - Referenz- oder Anaphernketten
        
- Wenn ein **einheitlicher Typ (`@type`)** für alle Links gelten soll.
    
- Wenn Stand-off-Strukturen verwaltet werden (z. B. mehrere konkurrierende Alignments).
    

### 6.2 Konventionen im Projekt

Empfehlenswert ist eine klare Konvention zu:

1. **ID-Schemata** für Ziele (`@xml:id`), z. B. `la1a`, `de1a`, `gr1a`.
    
2. **Typisierung** der Linkgruppen (`@type`-Werte wie `translation`, `commentary`, `alignment-fine` usw.).
    
3. Verwendung von **`@domains`** zur Eingrenzung der Quellenbereiche (z. B. pro Sprache oder pro Dokumentbereich).
    
4. Verwendung von **`@targFunc`** zur expliziten Rollenmarkierung der Ziele (Quelle/Übersetzung, Kommentar/Textstelle, etc.).
    

All diese Konventionen sollten im `<encodingDesc>` des TEI-Headers dokumentiert werden (insbesondere in `<projectDesc>` bzw. `<tagsDecl>`), damit die Link-Struktur maschinell und intellektuell nachvollziehbar bleibt. ([tei-c.org](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/SA.html?utm_source=chatgpt.com "17 Linking, Segmentation, and Alignment - The TEI ..."))

---

## 7. Kurzüberblick für den schnellen Einstieg

- **Was ist `<linkGrp>`?**  
    Container für eine thematisch zusammengehörige Menge von `<link>`-/`<ptr>`-Elementen.
    
- **Wofür wird es benutzt?**  
    Alignment, Assoziationen, Kommentarverknüpfungen, semantische Relationen.
    
- **Zentrale Attribute:**
    
    - `@type` / `@subtype`: Art der Linkgruppe
        
    - `@domains`: Geltungsbereich der Ziele
        
    - `@targFunc`: Rollen der Ziel-IDs in `@target`
        
- **Inhalt:**  
    `desc*` gefolgt von `(link | ptr)+`
    
- **Ort im TEI-Dokument:**  
    flexibel – u. a. in `<body>`, `<div>`, `<seg>`, `<standOff>`, oder in Metainformationen.
    

Damit bietet `<linkGrp>` einen standardisierten und leistungsfähigen Rahmen, um beliebige Relationen zwischen Textelementen (innerhalb eines Dokuments oder zwischen mehreren Dokumenten) in TEI-P5 4.10.2 zu modellieren.

```
::contentReference[oaicite:16]{index=16}
```