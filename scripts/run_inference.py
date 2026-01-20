import os
import glob
import time
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tqdm import tqdm
from lxml import etree

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not found.")
    # exit(1) 

# Client Setup
client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)

# Configuration
INPUT_DIR = os.path.join("Vault", "03_data", "chapters")
OUTPUT_DIR = os.path.join("Vault", "03_data", "chapters_tei")
REGISTRY_FILE = os.path.join("Vault", "03_data", "entity_registry.json")
MODEL_NAME = "gemini-3-flash-preview" # Stable model

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'person': {}, 'place': {}, 'org': {}}

def save_registry(registry):
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

def get_chapter_number(filename):
    try:
        base = os.path.splitext(filename)[0]
        parts = base.split('_')
        return parts[-1]
    except:
        return "00"

def construct_prompt(content, chapter_num, registry):
    persons_str = ", ".join([f"{name} -> {pid}" for name, pid in list(registry.get('person', {}).items())[:50]])
    places_str = ", ".join([f"{name} -> {pid}" for name, pid in list(registry.get('place', {}).items())[:50]])
    orgs_str = ", ".join([f"{name} -> {pid}" for name, pid in list(registry.get('org', {}).items())[:50]])

    return f"""
System: Du erzeugst TEI-P5-XML. Halte dich strikt an TEI-Syntax.
Wichtig:
- Namespace: xmlns="http://www.tei-c.org/ns/1.0"
- Keine Markdown-Code-Blocks im Output (kein ```xml). Nur raw XML.

# EXISTING ENTITIES REGISTRY
Please reuse these xml:ids if you encounter these entities (fuzzy match names):
- Persons: {persons_str}
- Places: {places_str}
- Orgs: {orgs_str}

User: Hier ist Markdown eines Kapitels (Latein/Griechisch/Deutsch, mit Headings). Erzeuge TEI:
- Struktur: <TEI><teiHeader>...</teiHeader><standOff>...</standOff><text><body><div type="chapter" n="{chapter_num}">...</div></body></text></TEI>
- Drei Sprachabschnitte als <div type="version" xml:lang="la|grc|de"> mit <p xml:id="la|grc|de-s{chapter_num}-pYY">...
- Annotiere Personen/Orte/Org/Ereignisse/Jahreszahlen im Fließtext: setze passende TEI-Elemente (<persName>, <placeName>, <orgName>, <event>, <date>).
- **WICHTIG**: Annotiere alle Referenzen auf die erste Person (Deutsch: 'ich', 'mich', 'mir', 'mein...'; Latein: 'ego', 'me', 'mihi', 'meus...'; Griechisch: 'ἐγώ', 'ἐμοῦ', 'ἐμοί'...) explizit als `<persName ref="#augustus">Wort</persName>`.
- Baue <standOff>:
  - Verwende deutsche Bezeichnungen für die Entitäten (z.B. `<orgName>Senat</orgName>` statt 'Senatus') und deutsche Beschreibungen in `<note type="desc">`.
  - <listPerson>/<person xml:id="..."><persName/><note type="desc">Kurze Beschreibung auf Deutsch</note></person>
  - <listPlace>/<place ...><placeName/><note type="desc">...</note></place>
  - <listOrg>/<org ...>...
  - <linkGrp xml:id="lg-translation" type="translation" targFunc="latin greek german">: ein <link> je Absatz-Dreier.
  - <linkGrp xml:id="lg-entity-mentions" type="entity-mention" targFunc="entity text text text">: <link target="#ENT #la-s{chapter_num}-pYY #grc-s{chapter_num}-pYY #de-s{chapter_num}-pYY"/> für jede erkannte Entität
Output: TEI als UTF-8-String.

Kapitel-Markdown:
{content}
"""

def update_registry_from_xml(xml_content):
    try:
        root = etree.fromstring(xml_content.encode('utf-8'))
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        registry = load_registry()
        modified = False

        def update_category(tag, category, name_tag):
            nonlocal modified
            for el in root.findall(f".//tei:standOff/tei:{tag}", namespaces=ns):
                pid = el.get("{http://www.w3.org/XML/1998/namespace}id")
                name_el = el.find(f"tei:{name_tag}", namespaces=ns)
                name = name_el.text if name_el is not None else None
                
                if pid and name:
                    if name not in registry[category]:
                        registry[category][name] = pid
                        modified = True
        
        update_category('listPerson/tei:person', 'person', 'persName')
        update_category('listPlace/tei:place', 'place', 'placeName')
        update_category('listOrg/tei:org', 'org', 'orgName')
        
        if modified:
            save_registry(registry)
    except Exception:
        pass

def validate_xml(xml_content, chapter_num):
    try:
        root = etree.fromstring(xml_content.encode('utf-8'))
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        chapter_div = root.find(f".//tei:text/tei:body/tei:div[@type='chapter']", namespaces=ns)
        if chapter_div is None:
            return False, "Missing <div type='chapter'> element"
        return True, "Valid"
    except etree.XMLSyntaxError as e:
        return False, f"XML Syntax Error: {e}"

def process_file(filepath):
    filename = os.path.basename(filepath)
    chapter_num = get_chapter_number(filename)
    output_filename = filename.replace(".md", ".xml")
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    if os.path.exists(output_path):
        print(f"Skipping {filename} (already exists)")
        return

    print(f"Processing {filename}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    registry = load_registry()
    prompt = construct_prompt(content, chapter_num, registry)
    
    if not client:
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )
            
            xml_content = response.text
            # Cleanup markdown code blocks if present
            if xml_content.startswith("```xml"):
                xml_content = xml_content[6:]
            if xml_content.startswith("```"):
                xml_content = xml_content[3:]
            if xml_content.endswith("```"):
                xml_content = xml_content[:-3]
            
            xml_content = xml_content.strip()
            
            is_valid, message = validate_xml(xml_content, chapter_num)
            
            if is_valid:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                update_registry_from_xml(xml_content)
                time.sleep(1)
                return 
            else:
                print(f"Validation failed: {message}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                
        except Exception as e:
            print(f"Error {filename}: {e}")
            if "429" in str(e):
                 time.sleep(5)
            elif attempt < max_retries - 1:
                time.sleep(2)

    print(f"Failed {filename}")

def main():
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.md")))
    if not files:
        print(f"No markdown files found in {INPUT_DIR}")
        return

    print(f"Found {len(files)} chapters.")
    for filepath in tqdm(files):
        process_file(filepath)

if __name__ == "__main__":
    main()
