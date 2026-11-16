"""Shared print styling and the HTML -> PDF step (Chromium) for the Anjum Mart marketing documents."""
import html
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fonts'))
LOGO = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'editable', 'anjum-mart-logo-for-light-background.svg'))
LOGO_DARK = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'editable', 'anjum-mart-logo-for-dark-background.svg'))

CSS = f'''
@font-face{{font-family:Cormorant;font-weight:600;src:url(file://{FONTS}/cormorant-latin-600-normal.woff2)}}
@font-face{{font-family:Cormorant;font-weight:500;src:url(file://{FONTS}/cormorant-latin-500-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:400;src:url(file://{FONTS}/jost-latin-400-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:500;src:url(file://{FONTS}/jost-latin-500-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:600;src:url(file://{FONTS}/jost-latin-600-normal.woff2)}}
@page{{size:A4;margin:13mm 13mm 14mm}}
*{{box-sizing:border-box}}
body{{margin:0;font:400 10pt/1.45 Jost,sans-serif;color:#171717}}
h1{{font:600 30pt/1.05 Cormorant,serif;margin:0 0 4pt}}
h2{{font:600 17pt/1.15 Cormorant,serif;margin:16pt 0 6pt;padding-bottom:3pt;border-bottom:2px solid #d4af37;break-after:avoid}}
h3{{font:600 11pt/1.3 Jost,sans-serif;margin:11pt 0 3pt;color:#7a5c14;break-after:avoid}}
p{{margin:3pt 0}} ul,ol{{margin:3pt 0 3pt 15pt;padding:0}} li{{margin:1.5pt 0}}
.cover{{height:255mm;background:#0b0b0b;color:#fff;padding:26mm 18mm;position:relative;break-after:page;
 background:radial-gradient(ellipse 80% 55% at 50% 45%,#4d3910 0%,#1c150a 48%,#0a0a0a 85%)}}
.cover h1{{font-size:44pt;color:#fff}}
.cover .sub{{color:#e6c875;letter-spacing:3pt;text-transform:uppercase;font-size:10pt;margin-top:10pt}}
.cover img.logo{{height:34mm;margin-bottom:16mm}}
.cover .meta{{position:absolute;left:18mm;right:18mm;bottom:20mm;color:#d8d8d8;font-size:9.5pt;border-top:1px solid rgba(212,175,55,.6);padding-top:8pt}}
.box{{border:1px solid #e7e0d0;border-left:4px solid #d4af37;background:#faf7ef;padding:7pt 10pt;margin:7pt 0;break-inside:avoid}}
.warn{{border-left-color:#a51c30;background:#fbf1f2}}
table{{border-collapse:collapse;width:100%;margin:5pt 0;break-inside:auto}}
tr{{break-inside:avoid}}
td,th{{border:1px solid #ddd;padding:4pt 6pt;text-align:left;vertical-align:top;font-size:9pt}}
th{{background:#111;color:#fff;font-weight:500}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:8.6pt;background:#f1f1f1;padding:0 2pt}}
.pill{{display:inline-block;padding:1pt 7pt;border-radius:9pt;background:#111;color:#f1d98a;font-size:8pt;letter-spacing:.5pt;margin-right:3pt}}
.pill.ig{{background:#a51c30;color:#fff}} .pill.fb{{background:#1b4a8a;color:#fff}} .pill.tt{{background:#111;color:#fff}}
.day{{break-before:page}}
.day .top{{display:flex;gap:12pt;align-items:flex-start}}
.day .thumb{{width:46mm;flex:none}}
.day .thumb img{{width:46mm;border:1px solid #d4af37;display:block}}
.day .thumb .cap{{font-size:7.5pt;color:#666;margin-top:3pt}}
.day h2{{margin-top:0}}
.cap-box{{white-space:pre-wrap;font-size:8.2pt;line-height:1.35;background:#f7f7f4;border:1px solid #e4e0d4;padding:4pt 6pt;margin:2pt 0;break-inside:avoid}}
table.ov td,table.ov th{{padding:2.2pt 5pt;font-size:7.8pt}}
.day p{{font-size:8.6pt}}
.day .thumb img{{width:40mm}}
.day .thumb{{width:40mm}}
.lbl{{font-weight:600;font-size:7.8pt;letter-spacing:.6pt;text-transform:uppercase;color:#7a5c14;margin-top:5pt}}
.small{{font-size:8.5pt;color:#555}}
.cols{{display:flex;gap:10pt}} .cols>div{{flex:1}}
'''


def page(body, title):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'


def cover(title, subtitle, meta):
    return (f'<div class="cover"><img class="logo" src="file://{LOGO_DARK}"><h1>{html.escape(title)}</h1>'
            f'<div class="sub">{html.escape(subtitle)}</div><div class="meta">{meta}</div></div>')


def to_pdf(html_path, pdf_path):
    js = f'''
import {{ createRequire }} from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const {{ chromium }} = require('playwright');
const b = await chromium.launch({{ executablePath: '/opt/pw-browsers/chromium' }});
const p = await b.newPage();
await p.goto('file://{html_path}');
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(600);
await p.pdf({{ path: '{pdf_path}', format: 'A4', printBackground: true, preferCSSPageSize: true }});
await b.close();
'''
    tmp = html_path + '.mjs'
    open(tmp, 'w').write(js)
    subprocess.run(['node', tmp], check=True)
    os.remove(tmp)
    print('pdf', pdf_path)


def e(s):
    return html.escape(s)
