import re
from pathlib import Path
from lxml import etree

MD_PATH = Path(r"C:\Users\Felix\Downloads\Res_Gestae_Divi_Augusti_mit_referenzen_korrigiert.md")
XML_PATH = Path("Vault/03_data/Res_Gestae_Divi_Augusti.xml")
NS = {"tei": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}


def parse_md_notes(md_text: str):
    """Return mapping chapter -> list of paragraphs, each with segments and following note ids."""
    chapters = {}
    current = None
    in_de = False
    buf = []
    ch_pat = re.compile(r"^##\s+(.+)$")
    note_pat = re.compile(r"\[\^(?P<num>\d+)\]")

    def flush_para():
        nonlocal buf
        if not buf:
            return
        para = "\n".join(buf).strip()
        if not para:
            buf = []
            return
        parts = note_pat.split(para)
        # parts alternates: text, num, text, num...
        assembled = []
        for i in range(0, len(parts), 2):
            text_part = parts[i]
            note_num = parts[i + 1] if i + 1 < len(parts) else None
            assembled.append((text_part, note_num))
        chapters.setdefault(current, []).append(assembled)
        buf = []

    for line in md_text.splitlines():
        m = ch_pat.match(line)
        if m:
            flush_para()
            current = m.group(1).strip()
            in_de = False
            continue
        if line.strip() == "### Deutsch":
            flush_para()
            in_de = True
            continue
        if line.startswith("###"):
            flush_para()
            in_de = False
            continue
        if not in_de:
            continue
        if line.strip() == "":
            flush_para()
            continue
        buf.append(line)

    flush_para()
    return chapters


def flatten_text_nodes(p_el):
    """Return list of (node, is_text, text) in document order for a paragraph."""
    acc = []

    def rec(node):
        if node.text:
            acc.append((node, True, node.text))
        for child in node:
            rec(child)
            if child.tail:
                acc.append((child, False, child.tail))

    rec(p_el)
    return acc


def insert_ptr_at_offset(p_el, offset, target):
    """Insert ptr into paragraph text at given character offset in flattened text."""
    flat = flatten_text_nodes(p_el)
    cursor = 0
    for node, is_text, txt in flat:
        if txt is None:
            continue
        next_cursor = cursor + len(txt)
        if offset <= next_cursor:
            rel = offset - cursor
            before = txt[:rel]
            after = txt[rel:]
            ptr = etree.Element("{http://www.tei-c.org/ns/1.0}ptr")
            ptr.set("target", target)
            ptr.set("type", "commentary-link")
            if is_text:
                node.text = before
                node.insert(0, ptr)
                ptr.tail = after
            else:
                node.tail = before
                parent = node.getparent()
                idx = list(parent).index(node)
                parent.insert(idx + 1, ptr)
                ptr.tail = after
            return True
        cursor = next_cursor
    # Fallback: append at end
    ptr = etree.Element("{http://www.tei-c.org/ns/1.0}ptr")
    ptr.set("target", target)
    ptr.set("type", "commentary-link")
    p_el.append(ptr)
    return False


def norm_pattern(text):
    # Escape and allow flexible whitespace
    escaped = re.escape(text.strip())
    return re.sub(r"\\\s+", r"\\s+", escaped)


def main():
    md_text = MD_PATH.read_text(encoding="utf-8")
    md_chapters = parse_md_notes(md_text)

    tree = etree.parse(str(XML_PATH))
    root = tree.getroot()

    for ch_label, paras in md_chapters.items():
        n_val = ch_label.strip().lower()
        if n_val.startswith("pro"):
            n_val = "proomium"
        elif re.fullmatch(r"\d+", n_val):
            n_val = n_val.zfill(2)
        ch_div = root.xpath(f".//tei:div[@type='chapter'][@n='{n_val}']", namespaces=NS)
        if not ch_div:
            print(f"Missing chapter {ch_label} -> {n_val}")
            continue
        ch_div = ch_div[0]
        p_list = ch_div.xpath(".//tei:div[@type='version' and @xml:lang='de']/tei:p", namespaces=NS)
        if len(p_list) != len(paras):
            print(f"Paragraph count mismatch in chapter {ch_label}: TEI {len(p_list)} vs MD {len(paras)}")
        for idx, parts in enumerate(paras):
            if idx >= len(p_list):
                continue
            p_el = p_list[idx]
            # Remove existing ptrs in this paragraph
            for ptr in list(p_el.xpath(".//tei:ptr", namespaces=NS)):
                ptr.getparent().remove(ptr)

            # Flatten paragraph text
            flat = flatten_text_nodes(p_el)
            raw_text = "".join([t for (_, _, t) in flat if t])

            search_start = 0
            for segment, note_num in parts:
                seg = segment.strip()
                if seg:
                    pattern = norm_pattern(seg)
                    m = re.search(pattern, raw_text[search_start:], flags=re.MULTILINE)
                    if m:
                        search_start += m.end()
                    else:
                        # fallback: skip to end of raw text
                        search_start = len(raw_text)
                if note_num:
                    insert_ptr_at_offset(p_el, search_start, f"#note-{note_num}")

    XML_PATH.write_bytes(etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True))
    print("Aligned pointers written.")


if __name__ == "__main__":
    main()
