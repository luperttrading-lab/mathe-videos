// Browser-Test der Einheitskreis-App: node tests/einheitskreis.mjs [bildordner]
// Bildet die Pages-Adresse nach (/mathe-videos/… = dieses Repo). Mit Bildordner: Bildschirmfotos (deviceScaleFactor 2).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

let pw;
try { pw = await import('playwright'); } catch { pw = await import('/opt/node22/lib/node_modules/playwright/index.mjs'); }
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const bilder = process.argv[2];
const typen = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.png': 'image/png', '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  const pfad = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/\/$/, '/index.html');
  const p = pfad.startsWith('/mathe-videos/') ? path.join(repo, pfad.slice('/mathe-videos/'.length)) : null;
  if (!p || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': typen[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const basis = `http://127.0.0.1:${server.address().port}/mathe-videos/einheitskreis/`;

let fehler = 0;
const ok = (bed, text) => { console.log((bed ? '  ok   ' : '  FEHLER ') + text); if (!bed) fehler++; };
const browser = await pw.chromium.launch();
const konsole = [];

async function neueSeite(w, h, hash = '') {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: bilder ? 2 : 1, hasTouch: true, isMobile: true });
  const page = await ctx.newPage();
  page.on('pageerror', e => konsole.push(e.message));
  page.on('console', m => { if (m.type() === 'error') konsole.push(m.text()); });
  await page.goto(basis + hash);
  await page.evaluate(() => localStorage.clear());
  await page.goto(basis + hash); await page.reload();
  return { ctx, page };
}
const foto = async (page, name) => { if (bilder) { fs.mkdirSync(bilder, { recursive: true }); await page.screenshot({ path: path.join(bilder, name + '.png') }); } };

console.log('Exakte Werte (Vergleich mit Math.sin/cos/tan)');
{
  const { ctx, page } = await neueSeite(390, 844);
  const r = await page.evaluate(() => {
    const EK = window.Einheitskreis;
    const zahl = t => {
      if (t === 'nicht definiert') return NaN;
      const neg = t.startsWith('−'); if (neg) t = t.slice(1);
      const v = { '0': 0, '1': 1, '½': .5, '√2/2': Math.SQRT2 / 2, '√3/2': Math.sqrt(3) / 2, '√3/3': Math.sqrt(3) / 3, '√3': Math.sqrt(3) }[t];
      return neg ? -v : v;
    };
    const aus = [];
    for (let g = 0; g <= 360; g += 15) {
      const w = EK.werte(g);
      if (!(g % 30 === 0 || g % 45 === 0)) { aus.push([g, w.sinText === null && w.cosText === null && w.radText === null, 'kein exakter Wert']); continue; }
      const s = zahl(w.sinText), c = zahl(w.cosText), t = zahl(w.tanText);
      const tanOk = g % 180 === 90 ? w.tanText === 'nicht definiert' : Math.abs(t - Math.tan(w.rad)) < 1e-9;
      const radOk = Math.abs(eval(w.radText.replace(/(\d)π/, '$1*π').replace('π', 'Math.PI')) - (g === 360 ? 2 * Math.PI : w.rad)) < 1e-12 || (g === 0 && w.radText === '0');
      aus.push([g, Math.abs(s - Math.sin(w.rad)) < 1e-9 && Math.abs(c - Math.cos(w.rad)) < 1e-9 && tanOk && radOk,
        `${w.sinText} | ${w.cosText} | ${w.tanText} | ${w.radText}`]);
    }
    return aus;
  });
  const falsch = r.filter(x => !x[1]);
  ok(falsch.length === 0, `alle 25 Winkel im 15°-Raster richtig ${falsch.length ? JSON.stringify(falsch) : ''}`);
  ok(r.find(x => x[0] === 150)[2] === '½ | −√3/2 | −√3/3 | 5π/6', '150°: ½ | −√3/2 | −√3/3 | 5π/6');
  ok(r.find(x => x[0] === 225)[2] === '−√2/2 | −√2/2 | 1 | 5π/4', '225°: −√2/2 | −√2/2 | 1 | 5π/4');
  ok(r.find(x => x[0] === 270)[2] === '−1 | 0 | nicht definiert | 3π/2', '270°: −1 | 0 | nicht definiert | 3π/2');
  ok(r.find(x => x[0] === 360)[2].endsWith('2π'), '360° = 2π');
  await ctx.close();
}

console.log('Ein Bildschirm, kein Scrollen (Hochformate)');
for (const [w, h, name] of [[375, 667, 'se'], [390, 844, 'iphone15'], [430, 932, 'promax'], [375, 548, 'se_safari'], [360, 740, 'android']]) {
  const { ctx, page } = await neueSeite(w, h);
  await page.waitForTimeout(700);
  await foto(page, `start_${name}`);
  const s = await page.evaluate(() => {
    const t = document.querySelector('.titel').getBoundingClientRect(), l = document.querySelector('#los').getBoundingClientRect();
    return { titelOben: t.top, losUnten: l.bottom, h: innerHeight, sw: document.documentElement.scrollWidth, w: innerWidth };
  });
  ok(s.losUnten <= s.h && s.sw <= s.w, `${w}×${h} Start: Los-Knopf sichtbar (unten ${Math.round(s.losUnten)} ≤ ${s.h})`);
  await page.click('#los');
  await page.evaluate(() => window.einheitskreis.setzeGrad(60));
  await page.waitForTimeout(100);
  await foto(page, `kreis_${name}`);
  const m = await page.evaluate(() => {
    const r = id => document.querySelector(id).getBoundingClientRect();
    return { regler: r('.regler').bottom, kreis: Math.min(r('#kreisfeld').width, r('#kreisfeld').height), kurven: r('#kurven').height,
      h: innerHeight, sh: document.scrollingElement.scrollHeight, sw: document.documentElement.scrollWidth, w: innerWidth };
  });
  ok(m.regler <= m.h && m.sh <= m.h && m.sw <= m.w, `${w}×${h} Kreis: alles sichtbar (Regler unten ${Math.round(m.regler)} ≤ ${m.h})`);
  ok(m.kreis >= 200, `${w}×${h} Kreisfläche ${Math.round(m.kreis)} px (≥ 200)`);
  await ctx.close();
}

console.log('Ziehen per Touch, Regler, Halbseite');
{
  const { ctx, page } = await neueSeite(390, 844, '#kreis');
  const cdp = await ctx.newCDPSession(page);
  const geo = await page.evaluate(() => {
    const r = document.querySelector('#kreis').getBoundingClientRect();
    const m = window.Einheitskreis.kreisMasse({ x: 0, y: 0, w: r.width, h: r.height }, {});
    return { x: r.left + m.mx, y: r.top + m.my, r: m.r };
  });
  const beruehre = (type, p) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: p ? [{ x: p[0], y: p[1] }] : [] });
  const bei = g => [geo.x + geo.r * Math.cos(g * Math.PI / 180), geo.y - geo.r * Math.sin(g * Math.PI / 180)];
  await beruehre('touchStart', bei(60));
  for (let g = 60; g <= 200; g += 7) await beruehre('touchMove', bei(g));
  await beruehre('touchMove', bei(203.4));
  await beruehre('touchEnd');
  let st = await page.evaluate(() => window.einheitskreis.stand.grad);
  ok(Math.abs(st - 203.4) < 0.3, `Touch-Zug von 60° nach 203,4°: ${st.toFixed(2)}°`);
  let txt = await page.textContent('#w-win');
  ok(txt === '203,4°', `Anzeige ohne Einrasten-Bereich: ${txt}`);
  // Einrasten: 223° → 225°
  await beruehre('touchStart', bei(223)); await beruehre('touchEnd');
  ok(Math.abs(await page.evaluate(() => window.einheitskreis.stand.grad) - 223) < .01, '223° bleibt 223° (Raster nur ±1,5°)');
  await beruehre('touchStart', bei(224)); await beruehre('touchEnd');
  st = await page.evaluate(() => window.einheitskreis.stand.grad);
  ok(st === 225, `Einrasten 224° → 225° (${st})`);
  ok(await page.textContent('#w-sin') === '−√2/2' && await page.textContent('#w-rad') === '5π/4', `225°: sin −√2/2, 5π/4`);
  await foto(page, 'kreis_225');

  // Sinus-Regler: Hälfte bleibt (links), Kosinus folgt mit √(1 − sin²)
  const regler = async (id, v) => page.evaluate(([id, v]) => {
    const e = document.querySelector(id); e.value = v; e.dispatchEvent(new Event('input', { bubbles: true }));
    return { ...window.Einheitskreis.werte(window.einheitskreis.stand.grad) };
  }, [id, v]);
  let w = await regler('#r-sin', 0.3);
  ok(w.cos < 0 && Math.abs(w.sin - 0.3) < 1e-9 && Math.abs(w.sin ** 2 + w.cos ** 2 - 1) < 1e-12, `sin = 0,3 von 225° aus: bleibt links (cos ${w.cos.toFixed(4)}), θ = ${w.grad.toFixed(2)}°`);
  await foto(page, 'regler_sin');
  w = await regler('#r-sin', 0.51);
  ok(w.grad === 150 && await page.textContent('#w-sin') === '½', `sin 0,51 (149,3°) rastet ein: 150°, ½ (${w.grad})`);
  w = await regler('#r-sin', 0.985);
  ok(w.grad > 90 && w.grad < 100, `sin 0,985 springt nicht mehr auf 90° (${w.grad.toFixed(1)}°)`);
  w = await regler('#r-sin', 1);
  ok(w.grad === 90, `sin = 1 → 90° (${w.grad})`);
  w = await regler('#r-sin', 0.2);
  ok(w.cos < 0, `nach sin = 1 zurück: weiter links (cos ${w.cos.toFixed(3)})`);
  w = await regler('#r-cos', 0.6);
  ok(w.sin > 0 && Math.abs(w.cos - 0.6) < 1e-9 && Math.abs(w.sin - 0.8) < 1e-9, `cos = 0,6 wechselt nach rechts, oben bleibt: sin ${w.sin.toFixed(3)}`);
  w = await regler('#r-cos', -0.5);
  ok(w.grad === 120, `cos −0,5 (oben) → 120° (${w.grad})`);
  w = await regler('#r-win', 359.9);
  ok(w.grad === 360 || w.grad === 0, `Winkel-Regler 359,9 rastet auf 360/0 (${w.grad})`);
  ok(await page.textContent('#w-rad') === '2π' || await page.textContent('#w-rad') === '0', `Bogenmaß dort: ${await page.textContent('#w-rad')}`);
  // Kreis gleich groß mit und ohne Tangens
  const gr = async () => page.evaluate(() => { const r = document.querySelector('#kreis').getBoundingClientRect();
    return window.Einheitskreis.kreisMasse({ x: 0, y: 0, w: r.width, h: r.height }, { tan: window.einheitskreis.stand.tan }).r; });
  const r1 = await gr(); await page.click('#tan'); const r2 = await gr(); await page.click('#tan');
  ok(r1 === r2, `Kreis mit und ohne tan gleich groß (${r1.toFixed(1)} / ${r2.toFixed(1)})`);
  // Ohne Einrasten: keine exakten Werte bei krummen Winkeln
  await page.click('#einrasten');
  w = await regler('#r-win', 29.9);
  ok(w.grad === 29.9 && await page.textContent('#w-sin') === '0,498', `ohne Einrasten 29,9°: sin 0,498 (${await page.textContent('#w-sin')})`);
  // Tangens
  await page.click('#einrasten');
  await page.click('#tan');
  await regler('#r-win', 60);
  ok(await page.isHidden('#tanwert'), 'tan 60°: Wert an der Tangente, keine Ecke');
  await foto(page, 'tan_60');
  await regler('#r-win', 90);
  ok((await page.textContent('#tanwert')).includes('nicht definiert'), 'tan 90°: nicht definiert');
  await page.click('#tan');
  // Version antippen: Auskunft „ist aktuell“, Layout springt nicht
  const vor = await page.evaluate(() => document.querySelector('#kurven').getBoundingClientRect().top);
  await page.click('#version'); await page.waitForTimeout(700);
  const nach = await page.evaluate(() => ({ t: document.querySelector('#update-text').textContent, k: document.querySelector('#kurven').getBoundingClientRect().top }));
  ok(/ist aktuell/.test(nach.t) && nach.k === vor, `Version antippen: „${nach.t}“, nichts verschoben`);
  // Stand bleibt nach Neuladen
  await regler('#r-win', 135); await page.waitForTimeout(500);
  await page.reload(); await page.waitForTimeout(300);
  ok(await page.evaluate(() => window.einheitskreis.stand.grad) === 135, 'Winkel bleibt nach Neuladen (135°)');
  await ctx.close();
}

ok(konsole.length === 0, 'keine Fehler in der Konsole ' + (konsole.length ? JSON.stringify(konsole) : ''));
await browser.close(); server.close();
console.log(fehler ? `${fehler} FEHLER` : 'Alles grün');
process.exit(fehler ? 1 : 0);
