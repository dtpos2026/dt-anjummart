#!/usr/bin/env python3
"""Checks what Shopify silently rejects on theme import (it drops the file or empties the schema without an error):
- config/settings_schema.json: range settings with more than 101 steps, defaults off the step or out of range, select defaults
  that are not options, duplicate ids.
- templates/*.json and sections/*-group.json: unknown settings or block types, range values outside min/max or off the step,
  select values that are not options, checkboxes that are not booleans.
Run from the theme folder:  python3 docs/tools/validate_theme_json.py
"""
import glob, json, os, re, sys

problems = []

schema = json.load(open('config/settings_schema.json'))
seen = set()
for group in schema:
    for st in group.get('settings', []):
        i, t = st.get('id'), st.get('type')
        if i:
            if i in seen: problems.append(('settings_schema', 'duplicate id', i))
            seen.add(i)
        if t == 'range':
            if (st['max'] - st['min']) / st['step'] > 101: problems.append(('settings_schema', 'range has more than 101 steps', i))
            if (st['default'] - st['min']) % st['step'] or not st['min'] <= st['default'] <= st['max']: problems.append(('settings_schema', 'range default invalid', i))
        if t == 'select' and st.get('default') not in [o['value'] for o in st['options']]: problems.append(('settings_schema', 'select default not an option', i))


def section_schema(kind):
    path = f'sections/{kind}.liquid'
    if not os.path.exists(path): return None
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', open(path).read(), re.S)
    return json.loads(m.group(1)) if m else None


def check(where, values, defs):
    by_id = {d['id']: d for d in defs if 'id' in d}
    for key, value in values.items():
        d = by_id.get(key)
        if d is None: problems.append((where, 'unknown setting', key)); continue
        if d['type'] == 'range' and (not d['min'] <= value <= d['max'] or (value - d['min']) % d['step']): problems.append((where, 'range value invalid', key, value))
        if d['type'] == 'select' and value not in [o['value'] for o in d['options']]: problems.append((where, 'select value not an option', key, value))
        if d['type'] == 'checkbox' and not isinstance(value, bool): problems.append((where, 'checkbox is not a boolean', key))


for path in glob.glob('templates/*.json') + glob.glob('templates/customers/*.json') + glob.glob('sections/*-group.json'):
    data = json.load(open(path))
    for sid, sec in data.get('sections', {}).items():
        sc = section_schema(sec['type'])
        if sc is None: problems.append((path, 'section type has no schema', sec['type'])); continue
        check(f'{path}:{sid}', sec.get('settings', {}), sc.get('settings', []))
        blocks = {b['type']: b.get('settings', []) for b in sc.get('blocks', [])}
        for bid, block in sec.get('blocks', {}).items():
            if block['type'] not in blocks: problems.append((f'{path}:{sid}', 'unknown block type', block['type'])); continue
            check(f'{path}:{sid}:{bid}', block.get('settings', {}), blocks[block['type']])

for p in problems: print('PROBLEM', *p)
print('theme JSON check:', 'OK' if not problems else f'{len(problems)} problem(s)')
sys.exit(1 if problems else 0)
