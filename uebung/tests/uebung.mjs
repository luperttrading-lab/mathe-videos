// Browser-Test der Übungs-App: node tests/uebung.mjs [bildordner]
// Bildet die Pages-Adresse nach: /mathe-videos/… = dieses Repo, /wuerfel/… = Würfel-Repo (Sprachmodell),
// Pfad zum Würfel-Klon über WUERFEL=… (Standard /home/user/luperttrading-lab/wuerfel).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

let pw;
try { pw = await import('playwright'); } catch { pw = await import('/opt/node22/lib/node_modules/playwright/index.mjs'); }
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const wuerfel = process.env.WUERFEL || '/home/user/luperttrading-lab/wuerfel';
const bilder = process.argv[2];
const typen = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.png': 'image/png', '.gz': 'application/gzip',
  '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  const pfad = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/\/$/, '/index.html');
  let p = null;
  if (pfad.startsWith('/mathe-videos/')) p = path.join(repo, pfad.slice('/mathe-videos/'.length));
  else if (pfad.startsWith('/wuerfel/')) p = path.join(wuerfel, pfad.slice('/wuerfel/'.length));
  if (!p || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': typen[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const basis = `http://127.0.0.1:${server.address().port}/mathe-videos/uebung/`;

let fehler = 0;
const ok = (bed, text) => { console.log((bed ? '  ok   ' : '  FEHLER ') + text); if (!bed) fehler++; };
const browser = await pw.chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'] });   // Ersatz-Mikrofon (Piepton)
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: bilder ? 2 : 1, permissions: ['microphone'] });
const page = await ctx.newPage();
const konsole = [];
page.on('pageerror', e => konsole.push(e.message));
page.on('console', m => { if (m.type() === 'error') konsole.push(m.text()); });
const foto = async name => { if (bilder) { fs.mkdirSync(bilder, { recursive: true }); await page.screenshot({ path: path.join(bilder, name + '.png') }); } };

console.log('Zahlwörter (Sprechen)');
const faelle = { 'zweihundert achtundachtzig': 288, 'zweihundertachtundachtzig': 288, 'hundert einundzwanzig': 121,
  'einhundert einundzwanzig': 121, 'dreihundert einundsechzig': 361, 'zweihundert neun': 209, 'zweihundert zehn': 210,
  'dreihundert': 300, '[unk] zweihundert sechzehn': 216, 'zwei hundert vier und zwanzig': 224, 'hundert zwei und achtzig': 182,
  'fünfundzwanzig': 25, 'zwölf': 12, '[unk]': null, 'hallo': null, 'zweihundert fünfundzwanzig': 225 };
await page.goto(basis);
for (const [t, z] of Object.entries(faelle)) {
  const w = await page.evaluate(t => window.uebung.zahlwortZuZahl(t), t);
  ok(w === z, `„${t}“ → ${w}`);
}
const gram = await page.evaluate(() => JSON.parse(window.uebung.grammatik()));
ok(gram.includes('zweihundert achtundachtzig') && gram.includes('zweihundert dreiundzwanzig') && gram.includes('hundert einundzwanzig')
  && gram.includes('[unk]'), `Grammatik: ${gram.length} Phrasen für 100 … 399, auch Zahlen, die kein Ergebnis sind (223)`);

console.log('Runde mit Tippen');
await page.evaluate(() => localStorage.clear());
const folge = '16x18,12x18,13x17,14x16,15x15,11x19,17x13,19x19,11x11,15x14';
await page.goto(basis + '?folge=' + folge);
await foto('1_start');
await page.click('#los');
ok(await page.isVisible('#bereit') && !(await page.isVisible('#frage')), 'Start zeigt erst „Bereit?“ – noch keine Aufgabe, die Zeit läuft noch nicht');
ok(await page.evaluate(() => window.uebung.runde.phase === 'bereit' && window.uebung.runde.ergebnisse.length === 0), 'Phase „bereit“');
await foto('1b_bereit');
await page.waitForTimeout(700);                      // warten auf der Bereit-Karte darf nicht in die Zeit der ersten Aufgabe zählen
await page.click('#bereit-los');
ok(await page.isVisible('#frage'), '„Los“ zeigt die erste Aufgabe');
ok((await page.getAttribute('#mikro', 'class')).includes('aus') && (await page.textContent('#mikro')).includes('Mikrofon aus'),
  `Tippen: Anzeige „${(await page.textContent('#mikro')).trim()}“`);
ok((await page.textContent('#frage')).replace(/\s/g, '') === '16·18', 'Erste Aufgabe 16 · 18');
const loes = folge.split(',').map(p => p.split('x').map(Number)).map(([x, y]) => x * y);
const pausen = {};
for (let i = 0; i < loes.length; i++) {
  const falsch = i === 2;
  const ziffern = String(falsch ? 999 : loes[i]);
  if (i === 0) await foto('2_aufgabe');
  for (const z of ziffern) { await page.dispatchEvent(`#tasten button[aria-label="${z}"]`, 'pointerdown'); await page.waitForTimeout(120); }
  const t = Date.now();
  if (i === 0) { await page.waitForTimeout(100); await foto('3_richtig');
    ok(await page.$eval('#rueck .zeit', el => el.classList.contains('unter')), 'Schnelle Antwort: Zeit grün (unter dem Ziel)'); }
  if (falsch) {
    await page.waitForTimeout(150);
    const a = await page.innerHTML('#antwort');
    ok(a.includes('<s>999</s>') && a.includes('<b>221</b>'), 'Falsch: 999 durchgestrichen, 221 daneben – in der Antwort selbst');
    await foto('4_falsch');
  }
  await page.waitForFunction(n => window.uebung.runde.i === n && (window.uebung.runde.phase === 'frage' || window.uebung.runde.phase === 'ende'),
    i + 1, { timeout: 3000 });
  if (i < loes.length - 1) (pausen[falsch ? 'falsch' : 'richtig'] ||= []).push(Date.now() - t);
}
const mittel = l => l.reduce((a, b) => a + b, 0) / l.length;
ok(Math.abs(mittel(pausen.falsch) - mittel(pausen.richtig)) < 200,
  `Nach falsch geht es genauso schnell weiter wie nach richtig (${Math.round(mittel(pausen.falsch))} ms / ${Math.round(mittel(pausen.richtig))} ms), kein Lösungsweg in der Runde`);
await page.waitForSelector('#ende:not([hidden])', { timeout: 4000 });
ok((await page.textContent('#e-richtig')).trim() === '9 von 10 richtig', 'Ende: 9 von 10 richtig');
const e = await page.evaluate(() => window.uebung.runde.ergebnisse);
const schnitt = e.reduce((s, x) => s + x.dauer, 0) / e.length / 1000;
ok(/Ø \d+,\d s je Aufgabe/.test(await page.textContent('#e-zeit')), `Durchschnittszeit angezeigt (${(await page.textContent('#e-zeit')).trim()}, gemessen ${schnitt.toFixed(2)} s)`);
ok(e.length === 10 && e.every(x => x.dauer > 0 && x.dauer < 5000), 'Jede Aufgabe hat eine Zeit');
ok((await page.textContent('#e-ziel')).trim() === (schnitt <= 4 ? 'Unter vier Sekunden – Ziel geschafft!' : 'Ziel: unter vier Sekunden je Aufgabe.'),
  `Ziel „Alle Zahlen“ vier Sekunden: „${(await page.textContent('#e-ziel')).trim()}“`);
ok((await page.$$eval('#stufen .zielmarke', l => l.map(e => e.textContent))).join('|') === 'Ziel 4 s|Ziel 3 s|Ziel 4 s|Ziel 3 s', 'Ziel auf jeder Stufen-Kachel');
ok(JSON.stringify(await page.evaluate(() => UEBUNGEN[0].stufen.map(s => s.ziel))) === '[4,3,4,3]', 'Ziele je Stufe: Alle Zahlen 4 s, Einer ergeben 10 3 s, Quadrate 4 s, Mal 11 3 s');
{ // Spruch nach Lage: 9 von 10 richtig → Mut-Spruch, nicht Lob (Nutzer 05.11.)
  const sp = (await page.textContent('#e-spruch b')).trim();
  ok(await page.evaluate(t => SPRUECHE.includes(t) && !LOB_SPRUECHE.includes(t), sp), `Mit Fehler: Spruch zum Mutmachen („${sp}“)`);
}
ok(e[0].dauer < 600, `Die Wartezeit vor „Los“ zählt nicht: erste Aufgabe ${Math.round(e[0].dauer)} ms`);
ok((await page.$$('#liste li')).length === 10, 'Liste mit allen 10 Aufgaben');
const weg = await page.textContent('#liste li.nein .weg');
ok(weg.includes('13 + 7 = 20') && weg.includes('200') && weg.includes('= 21') && weg.includes('221'),
  `Im Ergebnis der Lösungsweg zum Fehler: „${weg.trim()}“`);
ok((await page.$$('.hoerfehler')).length === 0, 'Getippter Fehler: kein „Hörfehler“-Knopf');
ok((await page.textContent('#e-spruch')).length > 10, `Motivation: „${(await page.textContent('#e-spruch')).trim()}“`);
await foto('5_ende');
ok(!(await page.isVisible('#naechster')), 'Nächster Trick (Elfer) ohne Video: keine Karte „Nächster Trick“');
await page.evaluate(() => { UEBUNGEN.splice(1, 0, { ...UEBUNGEN[0], id: 'probe', kurz: 'probe', titel: 'Probe-Trick', video: 'https://youtu.be/probe' }); zeigeEnde(false); });
ok(await page.isVisible('#naechster') && (await page.getAttribute('#naechster', 'href')) === 'https://youtu.be/probe',
  `Mit zweitem Trick: „${(await page.textContent('#naechster')).trim()}“ führt zum Video`);
await page.evaluate(() => { UEBUNGEN.splice(1, 1); zeigeEnde(false); });
await page.click('#uebersicht');
ok(!(await page.$('#verlauf')), 'Startseite ohne Verlaufs-Grafik (Nutzer 06.11.)');
{ const adresse = await page.evaluate(() => UEBUNGEN[0].video), vt = (await page.textContent('#video')).trim();
  ok(adresse ? (await page.getAttribute('#video', 'href')) === adresse && vt === '▶ Video' : vt.includes('Video folgt'),
    adresse ? `Trick-Karte: „${vt}“ führt zu ${adresse}` : 'Vor dem Hochladen: „▶ Video folgt“ an der Trick-Karte'); }
const bestK = await page.textContent('#stufen button[aria-pressed="true"] .bestmarke').catch(() => '');
ok(/Best \d+,\d s/.test(bestK), `Bestwert auf der gewählten Kachel: „${bestK.trim()}“`);
await foto('6_verlauf');

console.log('Sprechen wählen: Laden sichtbar, „Solange tippen“');
await page.click('#eingabe button[data-e="sprechen"]');
await page.waitForTimeout(600);
const st = await page.textContent('#sprachstatus');
const losT = await page.textContent('#los');
ok(/Sprache lädt … \d+ s/.test(losT) && !(await page.isVisible('#sprachstatus')), `Laden steht im Start-Knopf, keine Zeile darüber: „${losT.trim()}“`);
ok((await page.getAttribute('#eingabe [data-e="sprechen"]', 'aria-pressed')) === 'true', 'Umschalter zeigt „Sprechen“ gewählt');
ok((await page.getAttribute('#schalter', 'aria-checked')) === 'true', 'Schieberegler steht rechts (sprechen)');
await page.click('#schalter');
ok((await page.getAttribute('#eingabe [data-e="tippen"]', 'aria-pressed')) === 'true' && (await page.getAttribute('#schalter', 'aria-checked')) === 'false',
  'Schieberegler antippen: zurück auf eintippen');
await page.click('#schalter');
ok((await page.getAttribute('#eingabe [data-e="sprechen"]', 'aria-pressed')) === 'true', 'Schieberegler antippen: wieder sprechen');
await foto('7_laedt');
await page.click('#los');
ok(await page.isVisible('#bereit') && await page.isDisabled('#bereit-los') && await page.isVisible('#ohne-sprechen'),
  `Beim Laden: „Los“ gesperrt, „${(await page.textContent('#bereit-text')).trim()}“, daneben „Ohne Sprechen los“`);
ok((await page.getAttribute('#mikro', 'class')).includes('laedt'), `Anzeige: „${(await page.textContent('#mikro')).trim()}“`);
await foto('8_vorbereitung');
await page.click('#ohne-sprechen');
ok(!(await page.isVisible('#bereit')) && (await page.textContent('#frage')).includes('16'), '„Ohne Sprechen los“ startet sofort');
for (const z of '288') await page.dispatchEvent(`#tasten button[aria-label="${z}"]`, 'pointerdown');
await page.waitForFunction(() => window.uebung.runde.ergebnisse.length === 1, null, { timeout: 2000 });
ok(true, 'Tippen geht, während die Sprache noch lädt');
await page.waitForFunction(() => window.uebung.sprache.modell, null, { timeout: 120000 });
ok(true, 'Sprache danach geladen');
await page.waitForFunction(() => document.querySelector('#mikro').classList.contains('an'), null, { timeout: 10000 });
ok((await page.textContent('#mikro')).includes('Mikrofon an'), `Danach mitten in der Runde: „${(await page.textContent('#mikro')).trim()}“`);
await foto('9_mikro_an');
await page.click('#mikro');
ok((await page.getAttribute('#mikro', 'class')).includes('aus') && !(await page.evaluate(() => !!window.uebung.sprache.strom)),
  'Antippen der Anzeige schaltet das Mikrofon wirklich aus');
await page.click('#abbruch');
ok((await page.getAttribute('#sprachstatus', 'class')).includes('bereit'), `Startseite danach: „${(await page.textContent('#sprachstatus')).trim()}“`);

console.log('Aufgaben-Erzeugung');
const z = await page.evaluate(() => {
  const u = UEBUNGEN[0], r = [];
  for (let k = 0; k < 200; k++) r.push(u.erzeuge('alle', 10).map(a => a.frage));
  const zehn = u.erzeuge('zehn', 10);
  return { r, zehn: zehn.map(a => [a.x, a.y]) };
});
ok(z.r.every(l => l.length === 10 && new Set(l.map(f => f.split(' · ').sort().join())).size === 10), '„Alle Zahlen“: 10 verschiedene Paare je Runde (200 Runden)');
ok(z.zehn.every(([x, y]) => (x - 10) + (y - 10) === 10), '„Einer ergeben 10“: nur 11·19, 12·18, 13·17, 14·16, 15·15');
const v = await page.evaluate(() => {
  const u = UEBUNGEN[0], paar = a => [Math.min(a.x, a.y), Math.max(a.x, a.y)].join('·');
  const z = { runden: 2000, nachbar: 0, quadrat2: 0, mehrAlsEinDoppel: 0, abstand: 99, gedreht: 0, aufgaben: 0, alleNachbar: 0, alleDoppel: 0 };
  for (let k = 0; k < z.runden; k++) {
    const l = u.erzeuge('zehn', 10);
    l.forEach((a, i) => { if (i && paar(a) === paar(l[i - 1])) z.nachbar++; z.aufgaben++; if (a.x > a.y) z.gedreht++; });
    if (l.filter(a => a.x === 15 && a.y === 15).length > 1) z.quadrat2++;
    const fr = l.map(a => a.frage), doppelt = fr.filter((f, i) => fr.indexOf(f) !== i);
    if (doppelt.length > 1) z.mehrAlsEinDoppel++;
    for (const d of doppelt) { const i = fr.indexOf(d), j = fr.lastIndexOf(d); z.abstand = Math.min(z.abstand, j - i); }
    const m = u.erzeuge('alle', 10);
    m.forEach((a, i) => { if (i && paar(a) === paar(m[i - 1])) z.alleNachbar++; });
    if (new Set(m.map(paar)).size !== 10) z.alleDoppel++;
  }
  return z;
});
ok(v.nachbar === 0, `„Einer ergeben 10“, ${v.runden} Runden: nie dasselbe Paar direkt hintereinander (auch nicht 12·18 → 18·12)`);
ok(v.quadrat2 === 0, '15 · 15 höchstens einmal je Runde');
ok(v.mehrAlsEinDoppel === 0 && v.abstand >= 4, `Höchstens eine Wiederholung je Runde (9 Aufgaben gibt es nur), frühestens 4 Aufgaben später (kleinster Abstand ${v.abstand})`);
ok(v.gedreht / v.aufgaben > 0.4 && v.gedreht / v.aufgaben < 0.6, `Beide Reihenfolgen: ${Math.round(100 * v.gedreht / v.aufgaben)} % mit der größeren Zahl vorne`);
ok(v.alleDoppel === 0 && v.alleNachbar === 0, '„Alle Zahlen“: nie ein Paar doppelt, auch nicht verdreht');
ok(z.r.flat().every(f => { const [x, y] = f.split(' · ').map(Number); return x >= 11 && x <= 19 && y >= 11 && y <= 19; }), 'Alle Faktoren zwischen 11 und 19');

console.log('Runde ohne Fehler: Lob-Spruch');
{
  await page.goto(basis + '?folge=16x18,12x18,13x17');
  await page.click('#los'); await page.waitForTimeout(300); await page.click('#bereit-los');
  for (const z of [288, 216, 221]) {
    for (const c of String(z)) { await page.dispatchEvent(`#tasten button[aria-label="${c}"]`, 'pointerdown'); await page.waitForTimeout(60); }
    await page.waitForTimeout(950);
  }
  await page.waitForSelector('#ende:not([hidden])', { timeout: 5000 });
  const sp = (await page.textContent('#e-spruch b')).trim();
  ok(await page.evaluate(t => LOB_SPRUECHE.includes(t), sp) && (await page.textContent('#e-spruch')).startsWith('Schnell und fehlerfrei'),
    `Alles richtig und schnell: Lob statt „keine Raketenwissenschaft“ („${sp}“)`);
}

console.log('Elfer-Trick (Folge 2)');
{
  await page.evaluate(() => localStorage.clear());
  await page.goto(basis + '#elfer');
  ok((await page.textContent('#u-titel')).trim() === 'Elfer-Trick', 'Direktlink #elfer öffnet den Elfer-Trick');
  ok((await page.textContent('#held-aufgabe')).replace(/\s/g, '') === '53·11=?', `Startbild: „${(await page.textContent('#held-aufgabe')).trim()}“`);
  ok((await page.$$eval('#stufen .zielmarke', l => l.map(e => e.textContent))).join('|') === 'Ziel 3 s|Ziel 3 s|Ziel 4 s|Ziel 6 s',
    'Stufen: Zweistellig 3 s, Summe unter 10 3 s, Die Eins wandert 4 s, Dreistellig 6 s');
  const sch = (await page.textContent('#schritte')).replace(/\s+/g, ' ');
  ok(sch.includes('5 _ 3') && sch.includes('5 + 3 = 8') && sch.includes('nichts wandert') && sch.includes('583'), `So geht der Trick: „${sch.trim()}“`);
  await foto('e1_elfer_start');
  const g = await page.evaluate(() => {
    const u = UEBUNGEN.find(x => x.id === 'elfer'), r = {};
    for (const st of ['zwei', 'ohne', 'wandert', 'drei']) {
      const runden = Array.from({ length: 300 }, () => u.erzeuge(st, 10));
      r[st] = { doppelt: runden.filter(l => new Set(l.map(a => a.x)).size !== 10).length,
        laengen: [...new Set(runden.flat().map(a => String(a.loesung).length))],
        summen: runden.flat().map(a => { const d = String(a.x).split('').map(Number); return d.length === 2 ? d[0] + d[1] : -1; }),
        richtig: runden.flat().every(a => a.loesung === a.x * 11 && a.x % 10 !== 0) };
    }
    return r;
  });
  ok(Object.values(g).every(x => x.doppelt === 0 && x.richtig), 'Je Runde jede Zahl höchstens einmal, Lösung = Zahl · 11, keine Endziffer 0 (je 300 Runden)');
  ok(g.ohne.summen.every(s => s < 10) && g.wandert.summen.every(s => s >= 10), '„Summe unter 10“ nur ohne, „Die Eins wandert“ nur mit Wandern');
  ok(g.ohne.laengen.join() === '3' && g.zwei.laengen.sort().join() === '3,4' && g.wandert.laengen.sort().join() === '3,4'
    && g.drei.laengen.join() === '4', 'Ergebnisse: Summe unter 10 dreistellig, mit 91 … 99 auch vierstellig (1001 … 1089), dreistellig vierstellig');
  const neun = await page.evaluate(() => { const u = UEBUNGEN.find(x => x.id === 'elfer'), z = new Set();
    for (let k = 0; k < 300; k++) for (const a of u.erzeuge('wandert', 10)) if (a.x >= 91) z.add(a.x);
    return [...z].sort(); });
  ok(neun.join() === '91,92,93,94,95,96,97,98,99', `„Die Eins wandert“ übt auch 91 … 99 (wie im Video 97 · 11 = 1067): ${neun.join(', ')}`);
  const tausend = await page.evaluate(() => ['tausend siebenundsechzig', 'eintausend eins', 'tausend und neunundachtzig', 'tausend',
    'tausendacht'].map(t => window.uebung.zahlwortZuZahl(t)));
  ok(tausend.join() === '1067,1001,1089,1000,1008', `Zahlwörter ab tausend: ${tausend.join(', ')}`);
  const gr = await page.evaluate(() => { const u = UEBUNGEN.find(x => x.id === 'elfer'); return zahlPhrasen(u.antworten[0], u.antworten[1]); });
  ok(gr.includes('tausend siebenundsechzig') && gr.includes('eintausend eins') && gr.includes('neunhundert neunundsiebzig')
    && !gr.some(x => x.includes('undefined')), `Grammatik Elfer 100 … 1099: ${gr.length} Phrasen, mit „tausend …“`);
  const w = await page.evaluate(() => { const u = UEBUNGEN.find(x => x.id === 'elfer');
    return [87, 789].map(x => u.weg(u.aufgabe(x)).map(s => s.text.replace(/<[^>]+>/g, '')).join(' | ')); });
  ok(w[0].includes('8 + 7 = 15') && w[0].includes('8 + 1 = 9') && w[0].includes('957'), `Lösungsweg 87 · 11: „${w[0]}“`);
  ok(w[1].includes('15 + 1 = 16') && w[1].includes('7 + 1 = 8') && w[1].includes('8679'), `Lösungsweg 789 · 11 (zweimal wandern): „${w[1]}“`);
  // Runde tippen: nach drei Ziffern wird geprüft
  await page.goto(basis + '?folge=53x11,87x11,19x11#elfer');
  await page.click('#los'); await page.waitForTimeout(300); await page.click('#bereit-los');
  ok((await page.innerHTML('#frage')).includes('<span class="c1">5</span><span class="c2">3</span> · 11'), 'Aufgabe wie im Video: 5 orange, 3 violett');
  await foto('e2_elfer_aufgabe');
  for (const z of [583, 957, 209]) {
    for (const c of String(z)) { await page.dispatchEvent(`#tasten button[aria-label="${c}"]`, 'pointerdown'); await page.waitForTimeout(60); }
    await page.waitForTimeout(950);
  }
  await page.waitForSelector('#ende:not([hidden])', { timeout: 5000 });
  ok((await page.textContent('#e-richtig')).trim() === '3 von 3 richtig', 'Elfer-Runde getippt: 3 von 3 richtig');
  await page.click('#uebersicht');
  // Dreistellig: nur tippen, auch wenn „sprechen“ gewählt war (neu laden ohne ?folge=)
  await page.goto(basis + '#elfer');
  await page.evaluate(() => { window.uebung.stand.eingabe = 'sprechen'; });
  await page.click('#stufen button[data-s="drei"]');
  ok((await page.getAttribute('#eingabe', 'class')).includes('nur-tippen') && (await page.getAttribute('#schalter', 'aria-checked')) === 'false'
    && (await page.textContent('#los')).trim() === 'Start · 10 Aufgaben', 'Dreistellig: Regler steht auf eintippen, ausgegraut, keine Sprach-Ladeanzeige');
  await foto('e3_dreistellig');
  await page.click('#los');
  ok(!(await page.isDisabled('#bereit-los')) && (await page.getAttribute('#mikro', 'class')).includes('aus'), 'Dreistellig: Runde startet sofort mit Tippen, Mikrofon aus');
  await page.click('#bereit-los');
  const a = await page.evaluate(() => window.uebung.runde.aufgaben[0]);
  for (const c of String(a.loesung)) await page.dispatchEvent(`#tasten button[aria-label="${c}"]`, 'pointerdown');
  await page.waitForFunction(() => window.uebung.runde.ergebnisse.length === 1, null, { timeout: 2000 });
  ok(await page.evaluate(() => window.uebung.runde.ergebnisse[0].ok) && String(a.loesung).length === 4 && a.x >= 101,
    `Vierstelliges Ergebnis getippt (${a.frage} = ${a.loesung})`);
  await page.click('#abbruch');
  await page.click('#stufen button[data-s="zwei"]');
  ok((await page.getAttribute('#schalter', 'aria-checked')) === 'true', 'Zurück auf Zweistellig: die Wahl „sprechen“ ist noch da');
  // Trick wählen
  await page.click('#trickwahl');
  ok(await page.isVisible('#trickblatt') && (await page.$$('#trickliste button')).length === 2, 'Trickname antippen: Liste mit zwei Tricks');
  await foto('e4_trick_waehlen');
  await page.click('#trickliste button:first-child');
  ok(!(await page.isVisible('#trickblatt')) && (await page.textContent('#u-titel')).trim() === 'Zehner-Trick' && page.url().endsWith('#zehner'),
    'Zehner gewählt: Titel, Adresse #zehner');
  await page.reload();
  ok((await page.textContent('#u-titel')).trim() === 'Zehner-Trick', 'Nach dem Neuladen bleibt der gewählte Trick');
}

ok(konsole.length === 0, 'Keine Fehler in der Konsole' + (konsole.length ? ': ' + konsole.join(' | ') : ''));
await browser.close(); server.close();
console.log(fehler ? `${fehler} Fehler` : 'Alles grün');
process.exit(fehler ? 1 : 0);
