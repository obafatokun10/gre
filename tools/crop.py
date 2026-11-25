import json, sys, os
from PIL import Image
import numpy as np

PAGEDIR, REG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
S = 2.5  # px per pt
os.makedirs(OUT, exist_ok=True)
cache = {}

def page(p):
    if p not in cache:
        cache[p] = np.array(Image.open(f'{PAGEDIR}/p-{p:03d}.png').convert('RGB'))
    return cache[p]

def strip(a, b):
    (p1, y1), (p2, y2) = a, b
    parts = []
    for p in range(p1, p2 + 1):
        im = page(p)
        top = int(y1 * S) if p == p1 else 0
        bot = int(y2 * S) if p == p2 else im.shape[0]
        top, bot = max(0, top), min(im.shape[0], bot)
        if bot > top:
            parts.append(im[top:bot])
    return np.concatenate(parts, axis=0) if parts else None

def clean(a):
    g = a.min(axis=2)
    ink = g < 200
    W = a.shape[1]
    # remove horizontal rule lines (thin full-width runs)
    def longest(r):
        best = cur = 0
        for v in r:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        return best
    rowfrac = ink.sum(axis=1) / W
    for yy in np.where(rowfrac > 0.6)[0]:
        if longest(ink[yy]) < 0.5 * W or 60 < yy < len(rowfrac) - 60:
            rowfrac[yy] = 0
    a = a.copy()
    y = 0
    while y < len(rowfrac):
        if rowfrac[y] > 0.6:
            y2 = y
            while y2 < len(rowfrac) and rowfrac[y2] > 0.6:
                y2 += 1
            if y2 - y <= 6:
                a[max(0,y-3):y2+3] = 255
                ink[max(0,y-3):y2+3] = False
            y = y2
        else:
            y += 1
    rows = ink.any(axis=1)
    keep = []
    blank = 0
    for i, r in enumerate(rows):
        if r:
            blank = 0
            keep.append(i)
        else:
            blank += 1
            if blank <= 28:
                keep.append(i)
    a = a[keep]
    rows = ink[keep].any(axis=1)
    ys = np.where(rows)[0]
    if len(ys) == 0:
        return None
    a = a[max(0, ys[0] - 10): ys[-1] + 12]
    cols = (a.min(axis=2) < 200).any(axis=0)
    xs = np.where(cols)[0]
    a = a[:, max(0, xs[0] - 12): xs[-1] + 14]
    return a

def save(a, path):
    im = Image.fromarray(a).quantize(colors=24, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    im.save(path, optimize=True)
    return Image.open(path).size

GROUPS = {('data',16),('data',20),('data',24),('ps1',22),('ps2',22),('ps3',22)}
regions = json.load(open(REG))
meta = {}
for key, items in regions.items():
    for it in items:
        q = it['q']
        qa = strip((it['qstart'][0], it['qstart'][1] + 1), (it['qend'][0], it['qend'][1] - 3))
        if (key, q) in GROUPS:
            nl = it['numline']
            if key == 'ps3':
                nl = (nl[0], nl[1] - 8)
            da = clean(strip((it['qstart'][0], it['qstart'][1] + 1), (nl[0], nl[1] - 2)))
            save(da, f'{OUT}/{key}-{q:02d}-d.png')
            qa = strip((nl[0], nl[1] - 2), (it['qend'][0], it['qend'][1] - 3))
        ea = strip((it['estart'][0], it['estart'][1] - 3), (it['eend'][0], it['eend'][1] + 3))
        qa, ea = clean(qa), clean(ea)
        qs = save(qa, f'{OUT}/{key}-{q:02d}-q.png')
        es = save(ea, f'{OUT}/{key}-{q:02d}-e.png')
        meta[f'{key}-{q:02d}'] = {'q': qs, 'e': es}
json.dump(meta, open(f'{OUT}/sizes.json', 'w'))
print(len(meta))
