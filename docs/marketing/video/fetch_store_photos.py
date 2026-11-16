"""Downloads the first (white background) photo of every watch and jewellery product from the public storefront
(https://anjummart.com/products.json) and saves it as <code>.jpg (M1.jpg ... W5.jpg, J1.jpg, J2.jpg).

Usage: python3 fetch_store_photos.py <out_dir> [store_url]
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'content'))
from catalog import HANDLES  # noqa: E402

out = os.path.abspath(sys.argv[1])
store = (sys.argv[2] if len(sys.argv) > 2 else 'https://anjummart.com').rstrip('/')
os.makedirs(out, exist_ok=True)
raw = subprocess.run(['curl', '-sS', '-m', '60', f'{store}/products.json?limit=250'], capture_output=True, text=True, check=True).stdout
by_handle = {p['handle']: p for p in json.loads(raw)['products']}
for code, handle in HANDLES.items():
    p = by_handle.get(handle)
    if not p or not p['images']:
        print('MISSING on the store:', code, handle)
        continue
    dst = os.path.join(out, code + '.jpg')
    subprocess.run(['curl', '-sS', '-m', '90', '-o', dst, p['images'][0]['src']], check=True)
    print(code, handle[:50], os.path.getsize(dst) // 1024, 'KB')
