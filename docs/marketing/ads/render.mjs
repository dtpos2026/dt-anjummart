// Renders the pages listed in <out>/jobs.json (written by make_ads_pack.py) to JPG files with Chromium.
// Usage: node render.mjs <out_dir> [only-regex]
import { createRequire } from 'module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(process.env.PLAYWRIGHT_FROM || process.cwd() + '/');
const { chromium } = require('playwright');
const out = path.resolve(process.argv[2]);
const only = process.argv[3] ? new RegExp(process.argv[3]) : null;
const jobs = JSON.parse(fs.readFileSync(path.join(out, 'jobs.json'), 'utf8')).filter((j) => !only || only.test(j.out));
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const j of jobs) {
  const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
  await p.goto('file://' + j.html);
  await p.waitForSelector('body[data-ready="1"]');
  await p.waitForTimeout(300);
  fs.mkdirSync(path.dirname(j.out), { recursive: true });
  await p.screenshot({ path: j.out, type: 'jpeg', quality: 92 });
  await p.close();
  console.log(path.basename(j.out));
}
await b.close();
