"""Launch gates: flip held offers on pages that cannot read _config.yml.

Usage (from the repo root):  python3 _scripts/launch_gates.py
Reads the switches in _config.yml (pi_cover, aml_supervised, vat_registered) and, for each entry in
_scripts/launch_gates_registry.json, swaps the page text between its "held" and "open" wording.
Safe to run twice. Pages built with Liquid read the switches directly and need nothing.
"""
import json, re, sys
cfg = open('_config.yml', encoding='utf-8').read()
def flag(name):
    m = re.search(r'^%s:\s*(true|false)' % name, cfg, re.M)
    return bool(m and m.group(1) == 'true')
changed = 0
desk = open('cbam-desk.md', encoding='utf-8').read()
GATES = {'advice': lambda: flag('aml_supervised') and flag('pi_cover'),
         'pi': lambda: flag('pi_cover'), 'vat': lambda: flag('vat_registered')}
for e in json.load(open('_scripts/launch_gates_registry.json', encoding='utf-8')):
    want, other = (e['open'], e['held']) if GATES[e['gate']]() else (e['held'], e['open'])
    s = open(e['file'], encoding='utf-8').read()
    if want is e['open']:
        for price in set(re.findall(r'£[0-9,]+', want)):
            if price not in desk:
                print('PRICE CHECK:', e['file'], 'shows', price, 'which is not on cbam-desk.md: update the registry first')
    if want in s: continue
    if other not in s:
        print('NOT FOUND, fix by hand:', e['file']); continue
    open(e['file'], 'w', encoding='utf-8').write(s.replace(other, want)); changed += 1
    print('updated', e['file'])
print(changed, 'file(s) changed')
