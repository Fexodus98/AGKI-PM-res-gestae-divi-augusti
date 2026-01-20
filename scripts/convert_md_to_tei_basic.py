import os
import glob
import re
import json
from xml.sax.saxutils import escape

# Configuration
INPUT_DIR = os.path.join("Vault", "03_data", "chapters")
OUTPUT_DIR = os.path.join("Vault", "03_data", "chapters_tei")
REGISTRY_FILE = os.path.join("Vault", "03_data", "entity_registry.json")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Augustus Pronouns for annotation
AUGUSTUS_KEYWORDS = {
    'la': [r'\b[Ee]go\b', r'\b[Mm]e\b', r'\b[Mm]ihi\b', r'\b[Mm]ei\b', r'\b[Mm]eus\b', r'\b[Mm]eum\b', r'\b[Mm]eam\b', r'\b[Mm]eo\b'],
    'grc': [r'\b ἐγώ\b', r'\b ἐμοῦ\b', r'\b ἐμοί\b', r'\b ἐμέ\b', r'\b μου\b', r'\b μοι\b', r'\b με\b'], 
    'de': [r'\b[Ii]ch\b', r'\b[Mm]ich\b', r'\b[Mm]ir\b', r'\b[Mm]ein\b', r'\b[Mm]eine\b', r'\b[Mm]einen\b', r'\b[Mm]einem\b']
}

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'person': {}, 'place': {}, 'org': {}}

def annotate_text(text, lang, registry):
    if not text:
        return ""
    
    # 1. Escape XML
    # We do NOT escape yet because we want to insert tags. 
    # But if we insert tags, we must escape the rest.
    # Strategy: Tokenize, escape plain text, wrap tags.
    # Simpler: Escape whole text first, then replacing matching words with tags works 
    # ONLY if the words don't contain < > & (which names usually don't).
    
    text = escape(text)
    
    # 2. Annotate Augustus Pronouns
    for pattern in AUGUSTUS_KEYWORDS.get(lang, []):
        # Using a replacement function to preserve case/content
        def rep_aug(match):
            return f'<persName ref="#augustus">{match.group(0)}</persName>'
        
        # Avoid replacing inside existing tags (though there are none yet)
        text = re.sub(pattern, rep_aug, text)

    # 3. Annotate Registry Entities (Naive implementation)
    # We only look for exact name matches.
    # Sort keys by length desc to match "Senatus Romanus" before "Senatus"
    
    all_entities = []
    for cat, items in registry.items():
        tag_map = {'person': 'persName', 'place': 'placeName', 'org': 'orgName'}
        tag = tag_map.get(cat, 'rs')
        for name, eid in items.items():
            if not name.strip(): continue
            all_entities.append((name, eid, tag))
            
    # Sort by name length descending
    all_entities.sort(key=lambda x: len(x[0]), reverse=True)
    
    for name, eid, tag in all_entities:
        # Simple word boundary check for Western languages
        # Escaped name because text is escaped
        safe_name = escape(name)
        pattern = r'(?<!>)\b' + re.escape(safe_name) + r'\b(?!<)'
        
        def rep_ent(match):
            return f'<{tag} ref="#{eid}">{match.group(0)}</{tag}>'
            
        text = re.sub(pattern, rep_ent, text, flags=re.IGNORECASE)

    return text

def parse_markdown(content):
    # Normalize newlines
    content = content.replace('\r\n', '\n')
    
    # Split by headers
    # Expected: 
    # # Res Gestae ...
    # ### Latein
    # ...
    # ### Griechisch
    # ...
    # ### Deutsch
    # ...
    
    sections = {'la': '', 'grc': '', 'de': ''}
    
    current_section = None
    
    lines = content.split('\n')
    for line in lines:
        if "### Latein" in line:
            current_section = 'la'
            continue
        elif "### Griechisch" in line:
            current_section = 'grc'
            continue
        elif "### Deutsch" in line:
            current_section = 'de'
            continue
        elif line.strip().startswith("#"):
            # Main title or other header
            continue
            
        if current_section:
            sections[current_section] += line + "\n"
            
    return {k: v.strip() for k, v in sections.items()}

def get_chapter_number(filename):
    try:
        base = os.path.splitext(filename)[0]
        parts = base.split('_')
        num = parts[-1]
        if num.isdigit():
            return num
        if "proomium" in filename.lower():
            return "proomium"
        return "00"
    except:
        return "00"

def generate_xml(filename, registry):
    chapter_num = get_chapter_number(filename)
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = parse_markdown(content)
    
    # Annotate
    txt_la = annotate_text(parts['la'], 'la', registry)
    txt_grc = annotate_text(parts['grc'], 'grc', registry)
    txt_de = annotate_text(parts['de'], 'de', registry)
    
    # Construct TEI
    # We create a single paragraph per language for now, unless double newlines suggest more.
    # Splitting by double newline for paragraphs.
    
    def make_paragraphs(text, lang_code, chap_num):
        paras = text.split('\n\n')
        xml_paras = []
        for i, p_text in enumerate(paras):
            if not p_text.strip(): continue
            pid = f"{lang_code}-s{chap_num}-p{i+1:02d}"
            xml_paras.append(f'<p xml:id="{pid}">{p_text.strip()}</p>')
        return "\n".join(xml_paras)

    body_la = make_paragraphs(txt_la, 'la', chapter_num)
    body_grc = make_paragraphs(txt_grc, 'grc', chapter_num)
    body_de = make_paragraphs(txt_de, 'de', chapter_num)
    
    # Links (One big link for the chapter if we don't align perfectly yet)
    # Ideally link p01 with p01.
    
    # Count paras to generate links safely (min length)
    count_la = body_la.count('<p ')
    count_grc = body_grc.count('<p ')
    count_de = body_de.count('<p ')
    min_paras = min(count_la, count_grc, count_de)
    
    links = []
    if min_paras > 0:
        for i in range(1, min_paras + 1):
            target = f"#la-s{chapter_num}-p{i:02d} #grc-s{chapter_num}-p{i:02d} #de-s{chapter_num}-p{i:02d}"
            links.append(f'<link target="{target}"/>')
    
    links_str = "\n".join(links)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Res Gestae Divi Augusti - Caput {chapter_num}</title>
      </titleStmt>
      <publicationStmt>
        <p>Generated by Script</p>
      </publicationStmt>
      <sourceDesc>
        <p>Converted from Markdown</p>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <standOff>
    <linkGrp xml:id="lg-translation" type="translation" targFunc="latin greek german">
      {links_str}
    </linkGrp>
    <listPerson/>
    <listPlace/>
    <listOrg/>
  </standOff>
  <text>
    <body>
      <div type="chapter" n="{chapter_num}">
        <div type="version" xml:lang="la">
          {body_la}
        </div>
        <div type="version" xml:lang="grc">
          {body_grc}
        </div>
        <div type="version" xml:lang="de">
          {body_de}
        </div>
      </div>
    </body>
  </text>
</TEI>"""

    out_file = os.path.join(OUTPUT_DIR, filename.replace('.md', '.xml'))
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f"Generated {out_file}")

def main():
    registry = load_registry()
    files = glob.glob(os.path.join(INPUT_DIR, "*.md"))
    print(f"Found {len(files)} markdown files.")
    
    for f in files:
        fname = os.path.basename(f)
        # Check if already exists? No, overwrite to ensure consistency given "all missing" comment
        generate_xml(fname, registry)

if __name__ == "__main__":
    main()
