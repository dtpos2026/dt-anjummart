// Draws every frame of a plan with Chromium (several pages in parallel) and writes them as numbered JPG files.
// Usage: node render.mjs <plan.json> <frames_dir> [workers] [only_times_csv]
import { createRequire } from 'module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire(process.env.PLAYWRIGHT_FROM || '/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const plan = JSON.parse(fs.readFileSync(path.resolve(process.argv[2]), 'utf8'));
const out = path.resolve(process.argv[3]);
const workers = parseInt(process.argv[4] || '4', 10);
const only = process.argv[5] ? process.argv[5].split(',').map(Number) : null;
fs.mkdirSync(out, { recursive: true });
const fps = plan.fps || 30;
const total = Math.round(plan.duration * fps);
const frames = only ? only.map((t) => Math.round(t * fps)) : Array.from({ length: total }, (_, i) => i);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--disable-gpu-vsync'] });
async function worker(id) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(here, 'scene.html'));
  await p.evaluate((pl) => window.__init(pl), plan);
  for (let k = id; k < frames.length; k += workers) {
    const i = frames[k];
    await p.evaluate((t) => window.__seek(t), i / fps);
    await p.screenshot({ path: path.join(out, 'f_' + String(only ? i : i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 93 });
  }
  await p.close();
}
const t0 = Date.now();
await Promise.all(Array.from({ length: workers }, (_, i) => worker(i)));
await b.close();
console.log('frames', frames.length, 'in', ((Date.now() - t0) / 1000).toFixed(1) + 's');
