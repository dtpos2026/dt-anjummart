// Renders banner / tile / product-media artwork from HTML scenes with Chromium.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const ART = path.resolve(process.argv[2]);
const only = process.argv[3] ? new RegExp(process.argv[3]) : null;
const FONTS = path.resolve('fonts');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

const fontCss = `
@font-face{font-family:'Cormorant';font-weight:400;src:url('file://${FONTS}/cormorant-latin-400-normal.woff2')}
@font-face{font-family:'Cormorant';font-weight:500;src:url('file://${FONTS}/cormorant-latin-500-normal.woff2')}
@font-face{font-family:'Cormorant';font-weight:600;src:url('file://${FONTS}/cormorant-latin-600-normal.woff2')}
@font-face{font-family:'Cormorant';font-weight:500;font-style:italic;src:url('file://${FONTS}/cormorant-latin-500-italic.woff2')}
@font-face{font-family:'Jost';font-weight:400;src:url('file://${FONTS}/jost-latin-400-normal.woff2')}
@font-face{font-family:'Jost';font-weight:500;src:url('file://${FONTS}/jost-latin-500-normal.woff2')}
@font-face{font-family:'Jost';font-weight:600;src:url('file://${FONTS}/jost-latin-600-normal.woff2')}
`;

// Seeded random for stable bokeh
function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

const NOISE = `<svg width="0" height="0" style="position:absolute"><defs>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.9 -0.35"/></filter>
<filter id="marble" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.0035 0.011" numOctaves="5" seed="11" result="n"/><feColorMatrix type="matrix" values="0 0 0 0 0.85  0 0 0 0 0.62  0 0 0 0 0.25  0 0 0 -9 4.4"/></filter>
</defs></svg>`;

function darkBackdrop(w, h, { glowX = 0.72, glowY = 0.55, glowR = 0.55, warm = 1, bokeh = 14, seed = 3, floor = true, tint = [190, 138, 44] } = {}) {
  const [tr, tg, tb] = tint;
  const r = rng(seed);
  let dots = '';
  for (let i = 0; i < bokeh; i++) {
    const size = 8 + r() * 46, x = r() * w, y = r() * h * 0.85, a = 0.05 + r() * 0.18;
    dots += `<i style="position:absolute;left:${x}px;top:${y}px;width:${size}px;height:${size}px;border-radius:50%;background:radial-gradient(circle,rgba(246,214,130,${a}),rgba(246,214,130,0) 70%);filter:blur(${1 + r() * 5}px)"></i>`;
  }
  return `<div class="bg" style="position:absolute;inset:0;overflow:hidden;background:
    radial-gradient(${w * glowR}px ${h * 0.75}px at ${glowX * 100}% ${glowY * 100}%, rgba(${tr},${tg},${tb},${0.55 * warm}), rgba(${tr},${tg},${tb},0) 62%),
    radial-gradient(${w * 0.3}px ${h * 0.5}px at 4% 105%, rgba(130,90,26,${0.4 * warm}), transparent 70%),
    radial-gradient(${w * 0.7}px ${h * 0.6}px at 45% -10%, rgba(255,235,190,.08), transparent 70%),
    linear-gradient(115deg,#0a0805 0%,#15100a 48%,#0a0805 100%)">
    <div style="position:absolute;inset:-20%;background:linear-gradient(104deg,transparent 36%,rgba(255,226,160,.07) 41%,transparent 47%),linear-gradient(104deg,transparent 52%,rgba(255,226,160,.045) 57%,transparent 61%),linear-gradient(104deg,transparent 68%,rgba(255,226,160,.06) 72%,transparent 77%);filter:blur(10px)"></div>
    ${dots}
    ${floor ? `<div style="position:absolute;left:0;right:0;bottom:0;height:${h * 0.2}px;background:linear-gradient(to bottom,rgba(255,214,130,.05),rgba(0,0,0,.55))"></div>` : ''}
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.45) 100%)"></div>
    <div style="position:absolute;inset:0;filter:url(#grain);opacity:.07;mix-blend-mode:overlay"></div>
  </div>`;
}

function item(it) {
  const src = `file://${ART}/cut-${String(it.cut).padStart(2, '0')}.png`;
  const rot = it.rot || 0;
  const shadow = it.noShadow ? '' : `filter:drop-shadow(0 ${Math.round(it.h * 0.04)}px ${Math.round(it.h * 0.05)}px rgba(0,0,0,.62)) drop-shadow(0 0 ${Math.round(it.h * 0.08)}px rgba(212,175,55,.14));`;
  const wEst = it.h * (it.ar || 0.5);
  const ground = it.noGround ? '' : `<i style="position:absolute;left:${it.x}px;top:${it.y + it.h / 2 + 6}px;width:${wEst * 1.5}px;height:${Math.max(26, it.h * 0.06)}px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.62),rgba(0,0,0,0) 70%);z-index:${(it.z || 1) - 0.5}"></i>`;
  return ground + `<img src="${src}" style="position:absolute;left:${it.x}px;top:${it.y}px;height:${it.h}px;transform:translate(-50%,-50%) rotate(${rot}deg);z-index:${it.z || 1};${shadow}">`;
}

function sceneHtml(s) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}html,body{margin:0;background:#000}#c{position:relative;width:${s.w}px;height:${s.h}px;overflow:hidden}${s.css || ''}</style></head><body>${NOISE}<div id="c">${darkBackdrop(s.w, s.h, s.bg || {})}${(s.items || []).map(item).join('')}${s.extra || ''}</div></body></html>`;
}

async function shoot(html, w, h, out, quality = 82) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  const tmp = path.join(ART, '_tmp.html');
  fs.writeFileSync(tmp, html);
  await p.goto('file://' + tmp, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(250);
  const el = await p.$('#c');
  await el.screenshot({ path: out, type: 'jpeg', quality });
  await ctx.close();
  const kb = Math.round(fs.statSync(out).size / 1024);
  console.log(path.basename(out), `${w}x${h}`, kb + 'KB');
}

const scenes = JSON.parse(fs.readFileSync(path.join(ART, 'scenes.json'), 'utf8'));
for (const [name, s] of Object.entries(scenes)) {
  if (only && !only.test(name)) continue;
  const html = s.html ? s.html.replace('__NOISE__', NOISE).replace('__FONTS__', fontCss) : sceneHtml(s);
  await shoot(html, s.w, s.h, path.join(ART, 'out', s.dir, name + '.jpg'), s.q || 82);
}
await b.close();
