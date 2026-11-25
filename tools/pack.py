import json, base64, glob, os, sys
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for st in ['arith', 'alg', 'geo', 'data', 'ps1', 'ps2', 'ps3']:
    d = {}
    for f in sorted(glob.glob(f'{src}/{st}-*.png')):
        d[os.path.basename(f)[:-4]] = 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    json.dump(d, open(f'{dst}/{st}.json', 'w'), separators=(',', ':'))
    print(st, len(d))
