import os
import glob
import re
import json
from lxml import etree

# Configuration
INPUT_DIR = os.path.join("Vault", "03_data", "chapters_tei")
NOTES_FILE = os.path.join("Vault", "03_data", "Anmerkungen_res gestae.md")
OUTPUT_FILE = os.path.join("Vault", "03_data", "Res_Gestae_Divi_Augusti.xml")
TIMELINE_FILE = os.path.join("Vault", "03_data", "timeline.json")

def parse_markdown_notes(filepath):
    notes = {} 
    if not os.path.exists(filepath):
        print(f"Warning: Notes file not found at {filepath}")
        return notes

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'^##\s+(\d+)\s*$', content, flags=re.MULTILINE)
    for i in range(1, len(sections), 2):
        note_id = sections[i].strip()
        note_content = sections[i+1].strip()
        notes[note_id] = note_content
    return notes

def main():
    print(f"Merging TEI files from {INPUT_DIR}...")
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.xml")))
    
    # Custom sorting: Ensure proomium is first
    proomium_file = next((f for f in files if "proomium" in f), None)
    if proomium_file:
        files.remove(proomium_file)
        files.insert(0, proomium_file)
        print("Moved Proömium to the beginning.")
    
    if not files:
        print("No XML files found!")
        return

    # Data structures
    all_persons = {}
    all_places = {}
    all_orgs = {}
    all_events = {}
    all_dates = {}
    translation_links = []
    entity_links = []
    chapters = []
    timeline_data = []

    ns = {'tei': 'http://www.tei-c.org/ns/1.0', 'xml': 'http://www.w3.org/XML/1998/namespace'}
    
    print(f"Parsing notes from {NOTES_FILE}...")
    notes_data = parse_markdown_notes(NOTES_FILE)
    print(f"Found {len(notes_data)} notes.")

    for filepath in files:
        print(f"Reading {os.path.basename(filepath)}...")
        try:
            tree = etree.parse(filepath)
            root = tree.getroot()
            
            chapter_div = root.find(".//tei:text/tei:body/tei:div[@type='chapter']", namespaces=ns)
            current_chapter_n = "unknown"
            if chapter_div is not None:
                current_chapter_n = chapter_div.get("n")
                chapters.append(chapter_div)
            else:
                print(f"Warning: No chapter div found in {filepath}")
                continue

            # Harvest Entities
            for tag, store in [
                ("listPerson/tei:person", all_persons),
                ("listPlace/tei:place", all_places),
                ("listOrg/tei:org", all_orgs),
                ("listEvent/tei:event", all_events),
                ("listDate/tei:date", all_dates)
            ]:
                for el in root.findall(f".//tei:standOff/tei:{tag}", namespaces=ns):
                    pid = el.get("{http://www.w3.org/XML/1998/namespace}id")
                    if pid and pid not in store:
                        store[pid] = el

            # Harvest Timeline
            for date_el in root.findall(".//tei:standOff/tei:listDate/tei:date", namespaces=ns):
                date_id = date_el.get("{http://www.w3.org/XML/1998/namespace}id")
                when = date_el.get("when")
                label = date_el.text.strip() if date_el.text else "Datierung"
                if when:
                    timeline_data.append({"id": date_id, "date": when, "label": label, "chapter": current_chapter_n})

            # Harvest Links
            for link in root.findall(".//tei:standOff/tei:linkGrp[@type='translation']/tei:link", namespaces=ns):
                translation_links.append(link)
            for link in root.findall(".//tei:standOff/tei:linkGrp[@type='entity-mention']/tei:link", namespaces=ns):
                entity_links.append(link)

        except Exception as e:
            print(f"Error parsing {filepath}: {e}")

    # Build Master TEI
    tei_root = etree.Element("{http://www.tei-c.org/ns/1.0}TEI", nsmap={None: ns['tei']})
    header = etree.SubElement(tei_root, "{http://www.tei-c.org/ns/1.0}teiHeader")
    fileDesc = etree.SubElement(header, "{http://www.tei-c.org/ns/1.0}fileDesc")
    titleStmt = etree.SubElement(fileDesc, "{http://www.tei-c.org/ns/1.0}titleStmt")
    title = etree.SubElement(titleStmt, "{http://www.tei-c.org/ns/1.0}title")
    title.text = "Res Gestae Divi Augusti – Die Taten des göttlichen Augustus"
    
    pubStmt = etree.SubElement(fileDesc, "{http://www.tei-c.org/ns/1.0}publicationStmt")
    etree.SubElement(pubStmt, "{http://www.tei-c.org/ns/1.0}p").text = "Digital Edition generated via LLM inference pipeline."
    
    sourceDesc = etree.SubElement(fileDesc, "{http://www.tei-c.org/ns/1.0}sourceDesc")
    etree.SubElement(sourceDesc, "{http://www.tei-c.org/ns/1.0}p").text = "Based on markdown chapters and annotations."
    
    standoff = etree.SubElement(tei_root, "{http://www.tei-c.org/ns/1.0}standOff")
    
    for tag, store in [("listPerson", all_persons), ("listPlace", all_places), ("listOrg", all_orgs), ("listEvent", all_events), ("listDate", all_dates)]:
        if store:
            l = etree.SubElement(standoff, f"{{http://www.tei-c.org/ns/1.0}}{tag}")
            l.extend(store.values())

    if translation_links:
        lg = etree.SubElement(standoff, "{http://www.tei-c.org/ns/1.0}linkGrp")
        lg.set("{http://www.w3.org/XML/1998/namespace}id", "lg-translation")
        lg.set("type", "translation")
        lg.set("targFunc", "latin greek german")
        lg.extend(translation_links)

    if entity_links:
        lg = etree.SubElement(standoff, "{http://www.tei-c.org/ns/1.0}linkGrp")
        lg.set("{http://www.w3.org/XML/1998/namespace}id", "lg-entity-mentions")
        lg.set("type", "entity-mention")
        lg.set("targFunc", "entity text text text")
        lg.extend(entity_links)

    text = etree.SubElement(tei_root, "{http://www.tei-c.org/ns/1.0}text")
    body = etree.SubElement(text, "{http://www.tei-c.org/ns/1.0}body")
    
    # Process Chapters & Inject Notes
    for chap in chapters:
        de_div = chap.find(".//tei:div[@xml:lang='de']", namespaces=ns)
        if de_div is not None:
            # Inject Notes Logic
            for p in de_div.findall(".//tei:p", namespaces=ns):
                if p.text:
                    # Regex for ".2" or ". 2" or just "2" at end of sentence.
                    # matches: dot/comma, space(opt), number, boundary
                    pattern = re.compile(r'([\.,])\s*(\d{1,2})(?=\s|<|$)')
                    
                    if pattern.search(p.text):
                        parts = []
                        last_end = 0
                        matched = False
                        
                        for m in pattern.finditer(p.text):
                            nid = m.group(2)
                            if nid in notes_data:
                                matched = True
                                # Text before
                                parts.append(('text', p.text[last_end:m.start()] + m.group(1)))
                                # Ptr
                                ptr = etree.Element("{http://www.tei-c.org/ns/1.0}ptr")
                                ptr.set("target", f"#note-{nid}")
                                ptr.set("type", "commentary-link")
                                parts.append(('elem', ptr))
                                last_end = m.end()
                        
                        if matched:
                            if last_end < len(p.text):
                                parts.append(('text', p.text[last_end:]))
                            
                            # Apply changes
                            p.text = parts[0][1] # First text part
                            
                            insertion_idx = 0
                            last_el = None
                            
                            for i in range(1, len(parts)):
                                kind, content = parts[i]
                                if kind == 'elem':
                                    p.insert(insertion_idx, content)
                                    last_el = content
                                    insertion_idx += 1
                                elif kind == 'text':
                                    if last_el is not None:
                                        last_el.tail = content
                                    else:
                                        # Should not happen given logic (starts with text)
                                        pass
        body.append(chap)

    # Back Matter
    if notes_data:
        back = etree.SubElement(text, "{http://www.tei-c.org/ns/1.0}back")
        div_notes = etree.SubElement(back, "{http://www.tei-c.org/ns/1.0}div")
        div_notes.set("type", "commentary")
        head = etree.SubElement(div_notes, "{http://www.tei-c.org/ns/1.0}head")
        head.text = "Anmerkungen"
        list_notes = etree.SubElement(div_notes, "{http://www.tei-c.org/ns/1.0}list")
        list_notes.set("type", "commentary")
        
        for nid, content in notes_data.items():
            item = etree.SubElement(list_notes, "{http://www.tei-c.org/ns/1.0}item")
            note = etree.SubElement(item, "{http://www.tei-c.org/ns/1.0}note")
            note.set("{http://www.w3.org/XML/1998/namespace}id", f"note-{nid}")
            note.set("type", "commentary")
            note.text = content

    tree = etree.ElementTree(tei_root)
    tree.write(OUTPUT_FILE, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"Successfully wrote merged TEI to {OUTPUT_FILE}")
    
    with open(TIMELINE_FILE, 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully wrote timeline data to {TIMELINE_FILE}")

if __name__ == "__main__":
    main()