import re, json, sys, html
from xml.etree import ElementTree as ET

SRC = sys.argv[1]  # bbox.html
FIRST_PAGE = 58
raw = open(SRC, encoding='utf-8').read()
raw = raw.replace('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')
root = ET.fromstring(raw)
ns = {'x': 'http://www.w3.org/1999/xhtml'}
pages = root.findall('.//x:page', ns)
lines = []  # (page, ymin, ymax, xmin, text)
for i, pg in enumerate(pages):
    pno = FIRST_PAGE + i
    for ln in pg.findall('.//x:line', ns):
        words = [w.text or '' for w in ln.findall('x:word', ns)]
        t = ' '.join(words).strip()
        lines.append((pno, float(ln.get('yMin')), float(ln.get('yMax')), float(ln.get('xMin')), t))
lines.sort(key=lambda l: (l[0], l[1]))

# explanation sections: (key, first page, last page, n questions)
SECTIONS = [
    ('arith', 63, 77, 19), ('alg', 82, 95, 17), ('geo', 100, 112, 13),
    ('data', 121, 142, 26), ('ps1', 150, 168, 25), ('ps2', 176, 192, 25), ('ps3', 200, 220, 25),
]
NAMES = ['Translate from Words to an Arithmetic or Algebraic Representation','Translate from Words to a Figure or Diagram','Translate from an Algebraic to a Graphical Representation','Translate from a Figure to an Arithmetic or Algebraic Representation','Simplify an Arithmetic or Algebraic Representation','Add to a Geometric Figure','Find a Pattern','Search for a Mathematical Relationship','Estimate','Trial and Error','Divide into Cases','Adapt Solutions to Related Problems','Determine Whether a Conclusion Follows from the Information Given']
def is_frag(t):
    if re.match(r'^\d+\.', t):
        return False
    for f in re.split(r'Strategy\s*\d*:?|^\d+:', t):
        f = f.strip()
        if f and not any(f in n for n in NAMES):
            return False
    return True
out = {}
for key, p0, p1, n in SECTIONS:
    L = [l for l in lines if p0 <= l[0] <= p1]
    # start after the heading
    idx = next(i for i, l in enumerate(L) if l[4].startswith('Answers and Explanations'))
    cur = (L[idx][0], L[idx][2])
    i = idx + 1
    items = []
    for q in range(1, n + 1):
        # find Explanation heading
        j = i
        while j < len(L) and not re.fullmatch(r'Explanation', L[j][4]):
            if L[j][4].startswith(('This explanation uses','The explanation uses')):
                break
            j += 1
        if j >= len(L) or L[j][4].startswith(('This explanation uses','The explanation uses')):
            print('NO EXPLANATION HEADING', key, q, file=sys.stderr)
            break
        qtext = ' '.join(l[4] for l in L[i:j])
        numline = next(((l[0], l[1]) for l in L[i:j] if re.match(r'%d\.' % q, l[4])), None)
        expl_top = (L[j][0], L[j][1])
        k = j
        while not L[k][4].startswith(('This explanation uses','The explanation uses')):
            k += 1
        m = k + 1
        while m < len(L) and (re.match(r'Strategy \d+', L[m][4]) or is_frag(L[m][4])):
            m += 1
        end = (L[m - 1][0], L[m - 1][2])
        items.append({'q': q, 'qstart': cur, 'qend': expl_top, 'estart': expl_top, 'eend': end,
                      'qtext': qtext[:160], 'numline': numline})
        cur = end
        i = m
    out[key] = items
    for it in items:
        ok = re.search(r'(^|\s)%d\.' % it['q'], it['qtext'])
        print(key, it['q'], 'OK' if ok else '??', it['qstart'], it['qend'], it['eend'], '|', it['qtext'][:90])
json.dump(out, open(sys.argv[2], 'w'), indent=1)
