document.addEventListener('DOMContentLoaded', () => {
    loadEdition();
    setupControls();
    setupSearch();
});

// Global state for lookups
const state = {
    persons: {},
    places: {},
    orgs: {},
    notes: {},
    originalHtml: new Map() // Store original HTML for search reset
};

// Keep last search results to reopen the modal without re-running the search
let lastResultsHtml = '';
let lastCount = 0;

async function loadEdition() {
    const container = document.getElementById('edition-container');
    
    try {
        const response = await fetch('Vault/03_data/Res_Gestae_Divi_Augusti.xml');
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        const text = await response.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(text, "text/xml");
        
        // Check for parsing errors
        const parserError = xmlDoc.getElementsByTagName("parsererror");
        if (parserError.length > 0) {
            throw new Error("XML Parsing Error");
        }

        // 1. Parse Stand-off Definitions
        parseStandOff(xmlDoc);
        
        // 2. Parse Commentary Notes
        parseNotes(xmlDoc);
        
        // 3. Render Chapters
        container.innerHTML = ''; // Clear loading
        
        // Namespace-safe selection
        // getElementsByTagName returns a live HTMLCollection, works across namespaces in many browsers for XML
        const bodies = xmlDoc.getElementsByTagName('body');
        if (bodies.length === 0) throw new Error("No body element found in XML");
        
        const allDivs = bodies[0].getElementsByTagName('div');
        const chapters = Array.from(allDivs).filter(div => div.getAttribute('type') === 'chapter');
        
        if (chapters.length === 0) {
            container.innerHTML = '<p>Keine Kapitel gefunden.</p>';
            return;
        }

        chapters.forEach(chapter => {
            const html = renderChapter(chapter);
            container.appendChild(html);
        });

        // Cache original HTML for search
        document.querySelectorAll('.text-segment').forEach((el, index) => {
            el.dataset.searchId = index;
            el.id = `seg-${index}`;
            state.originalHtml.set(index.toString(), el.innerHTML);
        });

    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="card" style="border-color: red;">Fehler beim Laden der Edition: ${err.message}</div>`;
    }
}

function parseStandOff(doc) {
    // Helper to extract definition
    const extract = (tagName, store) => {
        const elements = doc.getElementsByTagName(tagName);
        Array.from(elements).forEach(el => {
            const id = el.getAttribute('xml:id');
            if (!id) return;

            // Find name sub-element (namespace agnostic)
            let name = 'Unbekannt';
            const persName = el.getElementsByTagName('persName')[0];
            const placeName = el.getElementsByTagName('placeName')[0];
            const orgName = el.getElementsByTagName('orgName')[0];
            
            if (persName) name = persName.textContent;
            else if (placeName) name = placeName.textContent;
            else if (orgName) name = orgName.textContent;

            // Find note sub-element
            let desc = '';
            const notes = el.getElementsByTagName('note');
            for (let note of notes) {
                if (note.getAttribute('type') === 'desc') {
                    desc = note.textContent;
                    break;
                }
            }

            store[id] = { name, desc };
        });
    };

    extract('person', state.persons);
    extract('place', state.places);
    extract('org', state.orgs);
}

function parseNotes(doc) {
    // Look for note elements in the back matter
    const back = doc.getElementsByTagName('back')[0];
    if (!back) return;

    const notes = back.getElementsByTagName('note');
    Array.from(notes).forEach(note => {
        const id = note.getAttribute('xml:id');
        if (id) {
            state.notes[id] = note.textContent;
        }
    });
}

function renderChapter(chapterNode) {
    const chapterNum = chapterNode.getAttribute('n');
    const chapterTitle = chapterNum === 'proomium' ? 'Proömium' : `Kapitel ${chapterNum}`;
    
    const section = document.createElement('section');
    section.className = 'chapter-container';
    section.id = `chapter-${chapterNum}`;
    
    // Header
    const header = document.createElement('div');
    header.className = 'chapter-header';
    header.innerHTML = `<h3>${chapterTitle}</h3>`;
    section.appendChild(header);

    // Mobile Tabs (visible only on small screens via CSS)
    const tabs = document.createElement('div');
    tabs.className = 'mobile-tabs';
    tabs.innerHTML = `
        <button class="tab-btn active" data-lang="la">Latein</button>
        <button class="tab-btn" data-lang="grc">Griechisch</button>
        <button class="tab-btn" data-lang="de">Deutsch</button>
    `;
    section.appendChild(tabs);

    // Grid
    const grid = document.createElement('div');
    grid.className = 'parallel-grid';

    // Columns
    // Add 'active' class to Latin by default for mobile view
    const colLat = renderColumn(chapterNode, 'la', 'Latein', chapterNum);
    colLat.classList.add('active'); // Default active
    colLat.dataset.lang = 'la';
    
    const colGrc = renderColumn(chapterNode, 'grc', 'Griechisch', chapterNum);
    colGrc.dataset.lang = 'grc';
    
    const colDe = renderColumn(chapterNode, 'de', 'Deutsch', chapterNum);
    colDe.dataset.lang = 'de';

    grid.appendChild(colLat);
    grid.appendChild(colGrc);
    grid.appendChild(colDe);

    section.appendChild(grid);
    
    // Setup Tab Logic
    setupMobileTabs(section);
    
    return section;
}

function setupMobileTabs(section) {
    const tabs = section.querySelectorAll('.tab-btn');
    const cols = section.querySelectorAll('.lang-column');

    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            // 1. Update Buttons
            tabs.forEach(t => t.classList.remove('active'));
            btn.classList.add('active');
            
            // 2. Show correct column
            const targetLang = btn.dataset.lang;
            cols.forEach(col => {
                if (col.dataset.lang === targetLang) {
                    col.classList.add('active');
                } else {
                    col.classList.remove('active');
                }
            });
        });
    });
}

function renderColumn(chapterNode, lang, label, chapterNum = '') {
    const col = document.createElement('div');
    col.className = 'lang-column';
    col.innerHTML = `<h4>${label}</h4>`;
    
    const divs = chapterNode.getElementsByTagName('div');
    const div = Array.from(divs).find(d => d.getAttribute('xml:lang') === lang);
    let paraIndex = 0;

    if (div) {
        // Transform TEI XML content to HTML, handling child nodes recursively
        Array.from(div.childNodes).forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE && node.nodeName === 'p') { // nodeName is usually safe
                const p = document.createElement('p');
                p.className = 'text-segment';
                p.dataset.lang = lang;
                p.dataset.chapter = chapterNum;
                p.dataset.seq = String(paraIndex);
                p.appendChild(transformTeiToHtml(node, lang));
                p.addEventListener('mouseenter', () => highlightSegment(chapterNum, paraIndex, true));
                p.addEventListener('mouseleave', () => highlightSegment(chapterNum, paraIndex, false));
                col.appendChild(p);
                paraIndex += 1;
            }
        });
    }
    return col;
}

function transformTeiToHtml(teiNode, lang = '') {
    const fragment = document.createDocumentFragment();
    
    Array.from(teiNode.childNodes).forEach(child => {
        if (child.nodeType === Node.TEXT_NODE) {
            fragment.appendChild(document.createTextNode(child.textContent));
        } else if (child.nodeType === Node.ELEMENT_NODE) {
            const tag = child.tagName;
            
            if (tag === 'persName' || tag === 'placeName' || tag === 'orgName') {
                const span = document.createElement('span');
                const ref = child.getAttribute('ref')?.replace('#', '');
                
                let type = 'unknown';
                if (tag === 'persName') type = 'person';
                if (tag === 'placeName') type = 'place';
                if (tag === 'orgName') type = 'org';
                
                span.className = `entity ${type}`;
                span.textContent = child.textContent;
                span.dataset.ref = ref;
                
                // Interaction via delegation
                
                fragment.appendChild(span);
            }
            else if (tag === 'ptr') {
                // Render Note-Marker nur in deutscher Spalte
                if (lang === 'de') {
                    const sup = document.createElement('sup');
                    const target = child.getAttribute('target')?.replace('#', '');
                    sup.className = 'ptr-marker';
                    sup.textContent = '[Note]';
                    sup.dataset.target = target;
                    fragment.appendChild(sup);
                }
            }
            else if (tag === 'num') {
                 const span = document.createElement('span');
                 span.style.fontVariantNumeric = 'oldstyle-nums';
                 span.textContent = child.textContent;
                 fragment.appendChild(span);
            }
            else {
                fragment.appendChild(transformTeiToHtml(child, lang));
            }
        }
    });
    
    return fragment;
}

function highlightSegment(chapterNum, seq, active) {
    const targets = document.querySelectorAll(`.text-segment[data-chapter="${chapterNum}"][data-seq="${seq}"]`);
    targets.forEach(el => {
        if (active) {
            el.classList.add('segment-highlight');
        } else {
            el.classList.remove('segment-highlight');
        }
    });
}

function showEntityInfo(event, id, type) {
    // Simple tooltip or sidebar logic
    // For now, let's use the commentary sidebar for entity info too
    const panel = document.getElementById('commentary-panel');
    let data = {};
    if (type === 'person') data = state.persons[id];
    if (type === 'place') data = state.places[id];
    if (type === 'org') data = state.orgs[id];

    if (!data) return;

    panel.innerHTML = `
        <h3>${data.name}</h3>
        <p class="label">${type.toUpperCase()}</p>
        <div class="commentary-card">
            <p>${data.desc}</p>
        </div>
    `;
}

function showCommentary(noteId) {
    const panel = document.getElementById('commentary-panel');
    const content = state.notes[noteId] || "Keine Anmerkung gefunden.";
    
    panel.innerHTML = `
        <h3>Anmerkung</h3>
        <div class="commentary-card">
            <p>${content}</p>
        </div>
    `;
}

function setupControls() {
    const toggle = (id, selector) => {
        document.getElementById(id).addEventListener('change', (e) => {
            const els = document.querySelectorAll(selector);
            els.forEach(el => {
                el.style.backgroundColor = e.target.checked ? '' : 'transparent';
                el.style.borderBottom = e.target.checked ? '' : 'none';
                el.style.color = e.target.checked ? '' : 'inherit';
            });
        });
    };
    
    toggle('toggle-person', '.entity.person');
    toggle('toggle-place', '.entity.place');
    toggle('toggle-org', '.entity.org');

    const chapterFilter = document.getElementById('chapter-filter');
    if (chapterFilter) {
        chapterFilter.addEventListener('change', (e) => {
            filterChapters(e.target.value);
        });
    }
}

function filterChapters(value) {
    const chapters = document.querySelectorAll('.chapter-container');
    chapters.forEach(section => {
        const id = section.id.replace('chapter-', '');
        section.style.display = (value === 'all' || value === id) ? '' : 'none';
    });
}
function setupSearch() {
    const input = document.getElementById('edition-search');
    const sidebarInfo = document.getElementById('search-results');
    const modal = document.getElementById('search-modal');
    const modalBody = document.getElementById('search-modal-body');
    const modalClose = document.getElementById('search-modal-close');
    const modalOpen = document.getElementById('search-modal-open');
    const modalFab = document.getElementById('search-modal-fab');
    let debounceTimer;

    const openFromCache = () => {
        if (lastResultsHtml) {
            modalBody.innerHTML = lastResultsHtml;
            modal.style.display = 'flex';
            bindResultClicks(modalBody, modal);
        }
    };

    const hideModal = () => {
        modal.style.display = 'none';
        modalBody.innerHTML = '';
    };
    modalClose?.addEventListener('click', hideModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) hideModal();
    });

    [modalOpen, modalFab].forEach(btn => {
        if (btn) btn.addEventListener('click', openFromCache);
    });

    input.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            performSearch(e.target.value, sidebarInfo, modal, modalBody, modalOpen, modalFab);
        }, 300);
    });
}

function performSearch(query, sidebarInfo, modal, modalBody, modalOpen, modalFab) {
    const segments = document.querySelectorAll('.text-segment');
    const normalizedQuery = query.toLowerCase().trim();
    let count = 0;

    // Reset if empty
    if (!normalizedQuery) {
        segments.forEach(el => {
            const id = el.dataset.searchId;
            if (state.originalHtml.has(id)) {
                el.innerHTML = state.originalHtml.get(id);
            }
        });
        lastResultsHtml = '';
        lastCount = 0;
        if (sidebarInfo) sidebarInfo.textContent = '';
        if (modal) modal.style.display = 'none';
        if (modalBody) modalBody.innerHTML = '';
        if (modalOpen) modalOpen.style.display = 'none';
        if (modalFab) modalFab.style.display = 'none';
        return;
    }

    const hits = [];

    // Search
    segments.forEach(el => {
        // Restore first to ensure clean state
        const id = el.dataset.searchId;
        el.innerHTML = state.originalHtml.get(id); // Reset
        
        if (el.textContent.toLowerCase().includes(normalizedQuery)) {
            const hitsInSegment = highlightTextNode(el, normalizedQuery);
            if (hitsInSegment > 0) {
                count += hitsInSegment;
                const chapter = el.dataset.chapter || '?';
                const lang = el.dataset.lang || '';
                const snippet = buildSnippet(el.textContent, normalizedQuery, 50);
                hits.push({
                    anchor: el.id,
                    chapter,
                    lang,
                    snippet
                });
            }
        }
    });

    if (sidebarInfo) sidebarInfo.textContent = `${count} Treffer`;

    if (modalBody && modal) {
        if (hits.length === 0) {
            modalBody.innerHTML = '<p class="text-muted">Keine Treffer</p>';
            lastResultsHtml = modalBody.innerHTML;
            modal.style.display = 'flex';
            if (modalOpen) {
                modalOpen.style.display = 'block';
                modalOpen.textContent = 'Keine Treffer';
            }
            if (modalFab) {
                modalFab.style.display = 'flex';
                modalFab.textContent = 'Keine Treffer';
            }
            return;
        }

        const listItems = hits.map(h => {
            const langLabel = h.lang === 'la' ? 'Lat' : h.lang === 'grc' ? 'Gr' : h.lang === 'de' ? 'De' : h.lang;
            return `<div class="search-hit" data-anchor="${h.anchor}">
                        <span class="text-muted">${h.chapter} · ${langLabel}</span>
                        <span>${h.snippet}</span>
                    </div>`;
        }).join('');

        const html = `<div class="search-count">${count} Treffer</div>${listItems}`;
        modalBody.innerHTML = html;
        lastResultsHtml = html;
        lastCount = count;
        modal.style.display = 'flex';
        if (modalOpen) {
            modalOpen.style.display = 'block';
            modalOpen.textContent = `Treffer anzeigen (${count})`;
        }
        if (modalFab) {
            modalFab.style.display = 'flex';
            modalFab.textContent = `${count} Treffer`;
        }

        bindResultClicks(modalBody, modal);
    }
}

function bindResultClicks(container, modal) {
    container.querySelectorAll('.search-hit').forEach(item => {
        item.addEventListener('click', () => {
            const anchor = item.getAttribute('data-anchor');
            const target = document.getElementById(anchor);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                target.style.outline = '2px solid var(--accent)';
                target.style.backgroundColor = 'rgba(240, 179, 92, 0.15)';
                setTimeout(() => {
                    target.style.outline = '';
                    target.style.backgroundColor = '';
                }, 1800);
            }
            if (modal) modal.style.display = 'none';
        });
    });
}

// DOM Walker to highlight text without destroying elements
function highlightTextNode(element, query) {
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    const nodes = [];
    while(walker.nextNode()) nodes.push(walker.currentNode);

    let hitCount = 0;

    nodes.forEach(node => {
        const val = node.nodeValue;
        if (!val) return;
        const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
        if (regex.test(val)) {
            const span = document.createElement('span');
            span.innerHTML = val.replace(regex, '<mark>$1</mark>');
            hitCount += (val.toLowerCase().match(new RegExp(escapeRegExp(query), 'g')) || []).length;
            node.parentNode.replaceChild(span, node);
            // Note: this replaces the text node with a span containing the text and marks.
            // It preserves surrounding tags.
        }
    });
    return hitCount;
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
}

function buildSnippet(text, query, radius = 40) {
    const lower = text.toLowerCase();
    const idx = lower.indexOf(query);
    if (idx === -1) return text.slice(0, radius * 2) + (text.length > radius * 2 ? '…' : '');
    const start = Math.max(0, idx - radius);
    const end = Math.min(text.length, idx + query.length + radius);
    const prefix = start > 0 ? '…' : '';
    const suffix = end < text.length ? '…' : '';
    return `${prefix}${text.slice(start, end)}${suffix}`;
}

// Register rendering (restored)
window.renderRegister = function(type) {
    const container = document.getElementById('register-list');
    const source = type === 'person' ? state.persons : 
                   type === 'place' ? state.places : state.orgs;
    
    if (!source || Object.keys(source).length === 0) {
        container.innerHTML = '<p class="small text-muted">Keine Einträge gefunden.</p>';
        return;
    }

    const items = Object.entries(source).map(([id, data]) => {
        const count = document.querySelectorAll(`.entity.${type}[data-ref="${id}"]`).length;
        return { id, name: data.name, count };
    });

    items.sort((a, b) => a.name.localeCompare(b.name));

    container.innerHTML = '';
    items.forEach(item => {
        if (item.count === 0) return;
        const div = document.createElement('div');
        div.style.cursor = 'pointer';
        div.style.display = 'flex';
        div.style.justifyContent = 'space-between';
        div.style.padding = '4px 0';
        div.innerHTML = `
            <span>${item.name}</span>
            <span class="text-muted" style="font-size: 0.8em;">${item.count}</span>
        `;
        div.onclick = () => scrollToEntity(item.id);
        container.appendChild(div);
    });
};

function scrollToEntity(id) {
    const el = document.querySelector(`.entity[data-ref="${id}"]`);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.backgroundColor = 'rgba(240, 179, 92, 0.5)';
        setTimeout(() => el.style.backgroundColor = '', 2000);
    }
}

// Add global delegation for entities to fix the "lost events on search reset" issue
document.getElementById('edition-container').addEventListener('click', (e) => {
    if (e.target.classList.contains('entity')) {
        const type = e.target.classList.contains('person') ? 'person' :
                     e.target.classList.contains('place') ? 'place' :
                     e.target.classList.contains('org') ? 'org' : 'unknown';
        const ref = e.target.dataset.ref;
        showEntityInfo(e, ref, type);
    }
    if (e.target.classList.contains('ptr-marker')) {
         const target = e.target.dataset.target;
         showCommentary(target);
    }
});
