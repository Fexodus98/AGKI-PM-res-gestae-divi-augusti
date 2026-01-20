import os
import glob
from lxml import etree

INPUT_DIR = os.path.join("Vault", "03_data", "chapters_tei")
OUTPUT_DIR = os.path.join("Vault", "03_data", "chapters_txt")
NS = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

LANG_ORDER = [
    ('la', None),
    ('grc', None),
    ('de', None)
]


def extract_text(xml_path: str) -> str:
    """Extract plain text for all language versions (la, grc, de)."""
    tree = etree.parse(xml_path)
    chapter = tree.find(".//tei:text/tei:body/tei:div[@type='chapter']", namespaces=NS)
    if chapter is None:
        return ""

    sections = []
    for lang_code, label in LANG_ORDER:
        div = chapter.find(f".//tei:div[@type='version'][@xml:lang='{lang_code}']", namespaces=NS)
        if div is None:
            continue

        paragraphs = []
        for p in div.findall(".//tei:p", namespaces=NS):
            parts = []
            if p.text:
                parts.append(p.text)
            for child in p:
                parts.append(etree.tostring(child, method="text", encoding=str))
                if child.tail:
                    parts.append(child.tail)
            raw = "".join(parts)
            text = " ".join(raw.split()).strip()
            if text:
                paragraphs.append(text)

        if paragraphs:
            section_text = "\n\n".join(paragraphs)
            sections.append(section_text)

    return "\n\n".join(sections)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.xml")))
    if not files:
        print("No XML chapters found.")
        return

    for xml_path in files:
        base = os.path.basename(xml_path)
        txt_name = os.path.splitext(base)[0] + ".txt"
        out_path = os.path.join(OUTPUT_DIR, txt_name)

        text_content = extract_text(xml_path)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
