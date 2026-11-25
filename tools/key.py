import json, sys
SETS = [
 ('arith', 'Arithmetic', 'qc:BCDAADC mc:DDBDEE ms3:BC ms3:A ms8:CH ne:12 ne:7 ne:2500'),
 ('alg', 'Algebra', 'qc:ABDACBA mc:EDBDBE ms5:BD ms5:AB ne:7.2 ne:17'),
 ('geo', 'Geometry', 'qc:CCADB mc:BDDBE ms8:BCEG ms4:ACD ne:112.5'),
 ('data', 'Data Analysis', 'qc:ADCABB mc:DCAEEB ms6:BCDEF ne:0.76 ne:5 mc:BDAC mc:BC ms3:BC mc:E mc:DCE'),
 ('ps1', 'Mixed Practice Set 1', 'qc:BDBAACDCD mc:AEBABADC ms6:CDE ms6:ACF ne:22 ne:0.003 mc:AED ms8:CDEFGH'),
 ('ps2', 'Mixed Practice Set 2', 'qc:BDAACDABA mc:EDDDCCBE ms8:ADG ms3:BC fr:5/2 ne:15.8 mc:ABE ms3:AC'),
 ('ps3', 'Mixed Practice Set 3', 'qc:BDCCAABDA mc:CEBEDAAD ms5:AD ms6:CE ne:4.1 fr:3/2 mc:CDE ne:67'),
]
GROUPS = {'data': [(16, 19), (20, 23), (24, 26)], 'ps1': [(22, 25)], 'ps2': [(22, 25)], 'ps3': [(22, 25)]}
sizes = json.load(open(sys.argv[1]))
out = []
for key, title, spec in SETS:
    qs = []
    for tok in spec.split():
        kind, val = tok.split(':')
        if kind in ('qc', 'mc'):
            for ch in val:
                qs.append({'t': kind, 'n': 4 if kind == 'qc' else 5, 'a': ch})
        elif kind.startswith('ms'):
            qs.append({'t': 'ms', 'n': int(kind[2:]), 'a': val})
        else:
            qs.append({'t': kind, 'a': val})
    items = []
    for i, q in enumerate(qs, 1):
        qid = f'{key}-{i:02d}'
        q['id'] = qid
        q['k'] = i
        q['qs'] = sizes[qid]['q']
        q['es'] = sizes[qid]['e']
        for a, b in GROUPS.get(key, []):
            if a <= i <= b:
                q['d'] = f'{key}-{a:02d}'
                q['g'] = [a, b]
                from PIL import Image
                q['ds'] = list(Image.open(f"{sys.argv[3]}/{key}-{a:02d}-d.png").size)
        items.append(q)
    out.append({'id': key, 'title': title, 'qs': items})
    print(key, len(items))
dsz = {k: v for k, v in sizes.items()}
json.dump(out, open(sys.argv[2], 'w'), separators=(',', ':'))
