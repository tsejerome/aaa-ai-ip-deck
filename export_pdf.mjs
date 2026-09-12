// Export index.html to a 16:9 PDF, one page per slide. Each slide is rasterised
// with Playwright (identical to the browser; no PDF font/clip quirks), and every
// http(s) link on the slide becomes a clickable PDF link annotation.
//   node export_pdf.mjs <dir containing node_modules/playwright>
//   e.g. node export_pdf.mjs ../../jupitrr/landing
import { createRequire } from 'module';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const pwDir = path.resolve(process.argv[2] || here);
const { chromium } = createRequire(path.join(pwDir, 'package.json'))('playwright');
const W = 1600, H = 900, SCALE = 2, JPEG_Q = 88;

const A = 'file://' + here + '/assets/';
let html = fs.readFileSync(path.join(here, 'index.html'), 'utf8')
  .replaceAll('src="assets/', 'src="' + A).replaceAll('poster="assets/', 'poster="' + A);
// Videos → linked still images
html = html.replace(/<video controls[^>]*poster="([^"]+)"[^>]*><\/video>/,
  (_, p) => `<a href="https://www.instagram.com/kallawaymarketing/"><img src="${p}" alt="@kallawaymarketing reel" style="width:100%;height:100%;object-fit:cover;display:block"></a>`);
html = html.replace(/<video autoplay[^>]*src="([^"]+stitch-loop\.mp4)"[^>]*><\/video>/,
  (_, p) => `<a href="https://www.jupitrr.com/"><img src="${p.replace('.mp4', '.gif')}" alt="Jupitrr Cut jump-cut" style="width:100%;height:100%;object-fit:cover;display:block"></a>`);
html = html.replace('</title>', `</title><style>
.hud,.brandmark,.hint,.lightbox{display:none!important}
.r{opacity:1!important;transform:none!important;transition:none!important}
*{animation:none!important}</style>`);
const tmp = path.join(here, '.print.tmp.html'); fs.writeFileSync(tmp, html);

const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
await pg.goto('file://' + tmp, { waitUntil: 'load' });
await pg.evaluate(async () => { await document.fonts.ready;
  await Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; }))); });
const n = await pg.evaluate(() => document.querySelectorAll('.slide').length);
const pages = [];
for (let i = 0; i < n; i++) {
  await pg.evaluate(i => document.querySelectorAll('.slide')[i].scrollIntoView({ behavior: 'instant' }), i);
  await pg.waitForTimeout(i === 0 ? 1500 : 900);
  const links = await pg.evaluate(i => {
    const s = document.querySelectorAll('.slide')[i], sr = s.getBoundingClientRect();
    return [...s.querySelectorAll('a[href^="http"]')].map(a => { const r = a.getBoundingClientRect();
      return { href: a.href, x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height }; })
      .filter(l => l.w > 4 && l.h > 4);
  }, i);
  const img = await pg.screenshot({ type: 'jpeg', quality: JPEG_Q, clip: { x: 0, y: 0, width: W, height: H } });
  pages.push({ img, links });
}
await b.close(); fs.unlinkSync(tmp);

// ---- minimal PDF writer (JPEG pages + URI link annotations) ----
const PW = W * 0.75, PH = H * 0.75; // px → pt
const objs = []; const add = o => (objs.push(o), objs.length);
const esc = s => s.replace(/[\\()]/g, m => '\\' + m);
const catalog = add(null), pagesObj = add(null); const kids = [];
for (const p of pages) {
  const im = add(Buffer.concat([Buffer.from(`<< /Type /XObject /Subtype /Image /Width ${W * SCALE} /Height ${H * SCALE} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${p.img.length} >>\nstream\n`), p.img, Buffer.from('\nendstream')]));
  const cs = `q ${PW} 0 0 ${PH} 0 0 cm /Im0 Do Q`;
  const c = add(`<< /Length ${cs.length} >>\nstream\n${cs}\nendstream`);
  const annots = p.links.map(l => add(`<< /Type /Annot /Subtype /Link /Border [0 0 0] /Rect [${(l.x * .75).toFixed(2)} ${(PH - (l.y + l.h) * .75).toFixed(2)} ${((l.x + l.w) * .75).toFixed(2)} ${(PH - l.y * .75).toFixed(2)}] /A << /S /URI /URI (${esc(l.href)}) >> >>`));
  kids.push(add(`<< /Type /Page /Parent ${pagesObj} 0 R /MediaBox [0 0 ${PW} ${PH}] /Resources << /XObject << /Im0 ${im} 0 R >> >> /Contents ${c} 0 R${annots.length ? ' /Annots [' + annots.map(a => a + ' 0 R').join(' ') + ']' : ''} >>`));
}
objs[catalog - 1] = `<< /Type /Catalog /Pages ${pagesObj} 0 R >>`;
objs[pagesObj - 1] = `<< /Type /Pages /Kids [${kids.map(k => k + ' 0 R').join(' ')}] /Count ${kids.length} >>`;
const parts = [Buffer.from('%PDF-1.4\n%\xe2\xe3\xcf\xd3\n', 'binary')]; const offs = []; let pos = parts[0].length;
objs.forEach((o, i) => { offs.push(pos); const b = Buffer.concat([Buffer.from(`${i + 1} 0 obj\n`), Buffer.isBuffer(o) ? o : Buffer.from(o), Buffer.from('\nendobj\n')]); parts.push(b); pos += b.length; });
const xref = `xref\n0 ${objs.length + 1}\n0000000000 65535 f \n` + offs.map(o => String(o).padStart(10, '0') + ' 00000 n \n').join('') + `trailer\n<< /Size ${objs.length + 1} /Root ${catalog} 0 R >>\nstartxref\n${pos}\n%%EOF\n`;
parts.push(Buffer.from(xref));
const out = path.join(here, 'deck.pdf'); fs.writeFileSync(out, Buffer.concat(parts));
console.log('wrote', out, n, 'pages,', pages.reduce((a, p) => a + p.links.length, 0), 'links,', (fs.statSync(out).size / 1048576).toFixed(1), 'MB');
