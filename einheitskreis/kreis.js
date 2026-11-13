// Einheitskreis: Rechnen und Zeichnen, getrennt von der Bedienung.
// Alles hängt nur am Winkel in Grad: zeichneKreis(ctx, rahmen, grad, opt) und zeichneKurven(…) malen ein Bild,
// ohne etwas über Regler oder Finger zu wissen. So lässt sich dasselbe Bild später Bild für Bild für ein Video
// erzeugen (z. B. per Playwright: Winkel setzen, Canvas abgreifen).
(function (global) {
  'use strict';

  const FARBEN = {
    papier: '#f6f1e7', ink: '#2b2d42', grau: '#8a8d98', gitter: 'rgba(120,100,70,.16)',
    sin: '#e63946',     // Sinus rot (senkrechte Strecke) – gemeinsame Farben mit dem Erklärvideo (13.11.)
    cos: '#3a86ff',     // Kosinus blau (waagrechte Strecke)
    tan: '#0f766e',     // Tangens grün (nur Zusatz)
    bogen: '#ff9f1c',   // Winkel θ und Bogen orange
    winkel: 'rgba(255,159,28,.18)',
  };

  // ---------- Exakte Werte ----------
  // Nur an Vielfachen von 30° und 45° gibt es die bekannten Werte. Alles andere: Dezimalzahl.
  const BETRAG = { 0: '0', 30: '½', 45: '√2/2', 60: '√3/2', 90: '1' };          // sin für 0 … 90°
  const TAN = { 0: '0', 30: '√3/3', 45: '1', 60: '√3' };                         // tan für 0 … 60°

  function normiere(grad) {
    let g = grad % 360; if (g < 0) g += 360;
    const r = Math.round(g);
    return Math.abs(g - r) < 1e-7 ? r : g;      // Rundungsrauschen (30.000000000004) weg
  }
  function besonders(grad) {
    const g = normiere(grad);
    return Number.isInteger(g) && (g % 30 === 0 || g % 45 === 0);
  }
  // Exakter sin-Wert eines besonderen Winkels als Text, sonst null
  function sinExakt(grad) {
    if (!besonders(grad)) return null;
    const g = normiere(grad);
    const ref = g <= 90 ? g : g <= 180 ? 180 - g : g <= 270 ? g - 180 : 360 - g;   // Bezugswinkel 0 … 90
    const b = BETRAG[ref];
    return (g > 180 && g < 360 && b !== '0') ? '−' + b : b;
  }
  function cosExakt(grad) { return besonders(grad) ? sinExakt(normiere(grad) + 90) : null; }
  function tanExakt(grad) {
    if (!besonders(grad)) return null;
    const g = normiere(grad);
    if (g % 180 === 90) return 'nicht definiert';
    const ref = g % 180 <= 90 ? g % 180 : 180 - g % 180;
    const b = TAN[ref];
    const negativ = (g % 180) > 90;               // 2. und 4. Quadrant
    return negativ && b !== '0' ? '−' + b : b;
  }
  // Bogenmaß als π-Bruch an besonderen Winkeln (auch 360° = 2π), sonst null
  function radExakt(grad) {
    const g = Math.abs(grad - 360) < 1e-7 ? 360 : normiere(grad);
    if (!Number.isInteger(g) || !(g % 30 === 0 || g % 45 === 0)) return null;
    if (g === 0) return '0';
    const ggt = (a, b) => b ? ggt(b, a % b) : a;
    const t = ggt(g, 180), z = g / t, n = 180 / t;
    return (z === 1 ? '' : z) + 'π' + (n === 1 ? '' : '/' + n);
  }
  const komma = (x, stellen = 3) => {
    let s = x.toFixed(stellen);
    if (/^-0\.0*$/.test(s)) s = s.slice(1);        // −0,000 vermeiden
    return s.replace('-', '−').replace('.', ',');
  };
  function werte(grad) {
    const r = grad * Math.PI / 180;
    let s = Math.sin(r), c = Math.cos(r);
    if (Math.abs(s) < 1e-12) s = 0; if (Math.abs(c) < 1e-12) c = 0;
    return {
      grad, rad: r, sin: s, cos: c, tan: c === 0 ? NaN : s / c,
      sinText: sinExakt(grad), cosText: cosExakt(grad), tanText: tanExakt(grad), radText: radExakt(grad),
      besonders: besonders(grad),
    };
  }

  // ---------- Zeichnen ----------
  function pfeil(ctx, x1, y1, x2, y2, k) {
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    const a = Math.atan2(y2 - y1, x2 - x1);
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - k * Math.cos(a - .45), y2 - k * Math.sin(a - .45));
    ctx.lineTo(x2 - k * Math.cos(a + .45), y2 - k * Math.sin(a + .45));
    ctx.closePath(); ctx.fill();
  }
  function punkt(ctx, x, y, r, farbe, rand = '#fff') {
    ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = farbe; ctx.fill();
    if (rand) { ctx.lineWidth = Math.max(1.5, r * .3); ctx.strokeStyle = rand; ctx.stroke(); }
  }
  // Wert für die Beschriftung: exakt (√3/2) oder drei Nachkommastellen wie unten
  function wertText(exakt, zahl) { return exakt || komma(zahl, 3); }
  // Name fett, Wert darunter etwas kleiner; (x, y) = Mitte des Blocks
  // Mit Papier-Rand (Halo): bleibt lesbar, auch wenn eine Linie (Kreis, Achse) darunter durchläuft
  function zweiZeilen(ctx, name, wert, x, y, fs) {
    ctx.save();
    ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
    ctx.strokeStyle = FARBEN.papier; ctx.lineWidth = Math.max(4, fs * .45);
    const zeile = (t, yy, f) => { ctx.font = f; ctx.strokeText(t, x, yy); ctx.fillText(t, x, yy); };
    zeile(name, y - fs * .55, schrift(fs, 800));
    zeile(wert, y + fs * .55, schrift(fs * .92, 700));
    ctx.restore();
  }
  function schrift(px, dick = 700) { return `${dick} ${px}px system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`; }

  // Geometrie des Kreises in einem Rahmen (auch für die Bedienung: Finger → Winkel)
  function kreisMasse(rahmen, opt = {}) {
    const { x, y, w, h } = rahmen;
    const rand = 0.15;                           // immer gleich groß, auch mit Tangens (Nutzer 13.11.); Platz für Beschriftung
    const r = Math.min(w, h) / 2 * (1 - rand * 2);
    return { mx: x + w / 2, my: y + h / 2, r };
  }

  // Zeichnet den Einheitskreis für den Winkel `grad`.
  // opt: { tan: bool, geist: 'sin' | 'cos' | null, punktGross: Zahl, beschriftung: bool, farben }
  function zeichneKreis(ctx, rahmen, grad, opt = {}) {
    const F = Object.assign({}, FARBEN, opt.farben || {});
    const { mx, my, r } = kreisMasse(rahmen, opt);
    const w = werte(grad);
    const px = mx + r * w.cos, py = my - r * w.sin;
    const u = r / 130;                          // Grundmaß für Linien und Schrift
    const fs = Math.max(11, Math.round(13 * u));

    ctx.save();
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';

    // Achsen
    ctx.strokeStyle = F.ink; ctx.fillStyle = F.ink; ctx.lineWidth = 1.4 * u;
    const ax = r * 1.18;
    pfeil(ctx, mx - ax, my, mx + ax, my, 8 * u);
    pfeil(ctx, mx, my + ax, mx, my - ax, 8 * u);
    ctx.font = schrift(fs, 600); ctx.fillStyle = F.grau;
    ctx.textAlign = 'left'; ctx.textBaseline = 'top';
    ctx.fillText('x', mx + ax - 2 * u, my + 6 * u);
    ctx.textAlign = 'right'; ctx.textBaseline = 'top';
    ctx.textAlign = w.cos < 0 ? 'right' : 'left'; ctx.fillText('y', mx + (w.cos < 0 ? -7 : 7) * u, my - ax - 2 * u);   // gegenüber der 1
    // Striche bei ±1
    ctx.strokeStyle = F.ink; ctx.lineWidth = 1.4 * u;
    for (const [sx, sy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      ctx.beginPath();
      if (sx) { ctx.moveTo(mx + sx * r, my - 4 * u); ctx.lineTo(mx + sx * r, my + 4 * u); }
      else { ctx.moveTo(mx - 4 * u, my - sy * r); ctx.lineTo(mx + 4 * u, my - sy * r); }
      ctx.stroke();
    }
    if (opt.beschriftung !== false) {
      ctx.fillStyle = F.grau; ctx.font = schrift(fs * .92, 600);
      // Zahlen dorthin, wo gerade nichts liegt
      ctx.textAlign = 'left'; ctx.textBaseline = 'top';
      ctx.fillText('1', mx + r + 4 * u, my + (w.sin < 0 ? -fs - 4 * u : 4 * u));
      ctx.textAlign = 'right';
      ctx.fillText('−1', mx - r - 4 * u, my + (w.sin < 0 ? -fs - 4 * u : 4 * u));
      // y-Achse: 1 knapp über, −1 knapp unter dem Kreis, auf der Seite ohne Punkt
      ctx.textAlign = w.cos < 0 ? 'left' : 'right';
      const xl = w.cos < 0 ? mx + 6 * u : mx - 6 * u;
      ctx.textBaseline = 'bottom'; ctx.fillText('1', xl, my - r - 3 * u);
      ctx.textBaseline = 'top'; ctx.fillText('−1', xl, my + r + 3 * u);
    }

    // Kleine Striche an den besonderen Winkeln (Vielfache von 30° und 45°): zeigen, wo Einrasten greift
    if (opt.marken) {
      ctx.strokeStyle = 'rgba(43,45,66,.35)'; ctx.lineWidth = 1.3 * u;
      for (let g = 0; g < 360; g += 15) {
        if (g % 30 && g % 45) continue;
        const a = g * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
        ctx.beginPath(); ctx.moveTo(mx + c * r, my - s * r); ctx.lineTo(mx + c * (r + 6 * u), my - s * (r + 6 * u)); ctx.stroke();
      }
    }
    // Kreis
    ctx.beginPath(); ctx.arc(mx, my, r, 0, 2 * Math.PI);
    ctx.strokeStyle = F.ink; ctx.lineWidth = 2.2 * u; ctx.stroke();

    // Winkelbogen
    const rb = r * 0.24;
    const bis = -w.rad;
    if (Math.abs(w.grad % 360) > 1e-9 || grad >= 360) {
      ctx.beginPath(); ctx.moveTo(mx, my);
      ctx.arc(mx, my, rb, 0, grad >= 360 ? -2 * Math.PI + 1e-6 : bis, true);
      ctx.closePath(); ctx.fillStyle = F.winkel; ctx.fill();
      ctx.beginPath(); ctx.arc(mx, my, rb, 0, grad >= 360 ? -2 * Math.PI + 1e-6 : bis, true);
      ctx.strokeStyle = F.bogen; ctx.lineWidth = 1.8 * u; ctx.stroke();
      // θ in die Mitte des Bogens
      const mitte = -w.rad / 2 - (grad >= 360 ? Math.PI : 0);
      const rt = rb + 11 * u;
      ctx.fillStyle = '#c96f00'; ctx.font = schrift(fs * 1.05, 800);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      if (Math.abs(w.grad) > 12 || grad >= 360) ctx.fillText('θ', mx + rt * Math.cos(mitte), my + rt * Math.sin(mitte));
    }

    // Tangens (Zusatz): Strecke auf der Tangente x = 1, Verlängerung des Radius bis dorthin
    if (opt.tan && w.cos !== 0) {
      const t = w.tan;
      const grenze = (rahmen.h / 2 - 6 * u) / r;            // so weit, wie der Rahmen reicht
      const tz = Math.max(-grenze, Math.min(grenze, t));
      ctx.setLineDash([5 * u, 5 * u]); ctx.strokeStyle = F.tan; ctx.lineWidth = 1.4 * u;
      ctx.beginPath(); ctx.moveTo(mx + r, my - grenze * r); ctx.lineTo(mx + r, my + grenze * r); ctx.stroke();
      // Verlängerung: vom Ursprung (bzw. vom Punkt) bis zur Tangente, geschnitten am Rahmen
      const s = Math.abs(t) > grenze ? Math.abs(grenze / t) : 1;
      ctx.beginPath(); ctx.moveTo(w.cos > 0 ? px : mx, w.cos > 0 ? py : my);
      ctx.lineTo(mx + r * s, my - r * t * s); ctx.stroke();
      ctx.setLineDash([]);
      ctx.strokeStyle = F.tan; ctx.lineWidth = 5 * u;
      ctx.beginPath(); ctx.moveTo(mx + r, my); ctx.lineTo(mx + r, my - r * tz); ctx.stroke();
      if (Math.abs(t) <= grenze) {
        punkt(ctx, mx + r, my - r * t, 4.5 * u, F.tan);
      }
      ctx.fillStyle = F.tan; ctx.textAlign = 'left';
      zweiZeilen(ctx, 'tan θ', wertText(w.tanText, w.tan), mx + r + 7 * u, my - r * tz / 2 + (Math.abs(tz) < .35 ? -22 * u : 0), fs);
    }

    // Geist: der zweite Punkt mit gleichem Sinus (bzw. Kosinus) – zeigt, warum ein Wert nicht reicht
    if (opt.geist) {
      const gg = opt.geist === 'sin' ? 180 - grad : -grad;
      const gw = werte(gg);
      const gx = mx + r * gw.cos, gy = my - r * gw.sin;
      if (Math.hypot(gx - px, gy - py) > 6 * u) {
        ctx.setLineDash([4 * u, 5 * u]); ctx.lineWidth = 1.5 * u;
        ctx.strokeStyle = opt.geist === 'sin' ? F.sin : F.cos;
        ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(gx, gy); ctx.stroke(); ctx.setLineDash([]);
        ctx.globalAlpha = .45; punkt(ctx, gx, gy, 8 * u, F.ink); ctx.globalAlpha = 1;
      }
    }

    // Radius
    ctx.strokeStyle = F.ink; ctx.lineWidth = 2 * u;
    ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(px, py); ctx.stroke();

    // Hilfslinie zur y-Achse (dort ist der Sinus abzulesen)
    ctx.setLineDash([3 * u, 4 * u]); ctx.strokeStyle = F.grau; ctx.lineWidth = 1.2 * u;
    ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(mx, py); ctx.stroke(); ctx.setLineDash([]);

    // cos: waagrecht auf der x-Achse, sin: senkrecht vom Fußpunkt zum Punkt
    ctx.lineCap = 'butt';
    ctx.strokeStyle = F.cos; ctx.lineWidth = 6 * u;
    ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(px, my); ctx.stroke();
    ctx.strokeStyle = F.sin;
    ctx.beginPath(); ctx.moveTo(px, my); ctx.lineTo(px, py); ctx.stroke();
    ctx.lineCap = 'round';
    punkt(ctx, mx, py, 3.6 * u, F.sin, null);
    punkt(ctx, px, my, 3.6 * u, F.cos, null);

    // Beschriftung der Strecken: auf der Außenseite, weg vom Radius
    if (opt.beschriftung !== false) {
      ctx.font = schrift(fs, 800);
      if (Math.abs(w.sin) > .16) {
        ctx.fillStyle = F.sin; ctx.textBaseline = 'middle';
        // Nutzerwahl 13.11.: von 0° bis unter 90° links der Strecke (innen), ab 90° rechts – nur ein Wechsel, kein Hin und Her
        const rechts = normiere(grad) >= 90;
        ctx.textAlign = rechts ? 'left' : 'right';
        zweiZeilen(ctx, 'sin', wertText(w.sinText, w.sin), px + (rechts ? 8 : -8) * u, my - r * w.sin / 2, fs);
      }
      if (Math.abs(w.cos) > .16) {
        ctx.fillStyle = F.cos; ctx.textAlign = 'center';
        const h2 = fs * 2.1;                                   // Höhe der zwei Zeilen
        zweiZeilen(ctx, 'cos', wertText(w.cosText, w.cos), mx + r * w.cos / 2, my + (w.sin >= 0 ? 7 * u + h2 / 2 : -7 * u - h2 / 2), fs);
      }
    }

    // Der Punkt P: groß, damit man ihn mit dem Finger trifft; Ring als Hinweis „zieh mich“
    const pr = (opt.punktGross || 11) * u;
    ctx.beginPath(); ctx.arc(px, py, pr * 1.75, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgba(43,45,66,.10)'; ctx.fill();
    punkt(ctx, px, py, pr, F.ink, '#fff');
    if (opt.beschriftung !== false) {
      ctx.fillStyle = F.ink; ctx.font = schrift(fs * 1.05, 800);
      const aussen = 1 + 28 * u / r;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText('P', mx + r * w.cos * aussen, my - r * w.sin * aussen);
    }
    ctx.restore();
  }

  // Abgewickelte Kurven: sin und cos über 0 … 2π, senkrechte Linie beim aktuellen Winkel
  // opt: { tan: bool, bis: Grad (nur bis hierher zeichnen, für Animationen), farben }
  function kurvenMasse(rahmen) {
    const { x, y, w, h } = rahmen;
    const links = x + 30, rechts = x + w - 10, oben = y + 10, unten = y + h - 20;
    return { links, rechts, oben, unten, mitte: (oben + unten) / 2, amp: (unten - oben) / 2 / 1.15 };
  }
  function zeichneKurven(ctx, rahmen, grad, opt = {}) {
    const F = Object.assign({}, FARBEN, opt.farben || {});
    const m = kurvenMasse(rahmen);
    const breite = m.rechts - m.links;
    const X = g => m.links + breite * g / 360;
    const Y = v => m.mitte - m.amp * v;
    const fs = 11;
    ctx.save();
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';

    // Gitter: Viertel 90°, y = ±1
    ctx.strokeStyle = F.gitter; ctx.lineWidth = 1;
    for (let g = 90; g <= 360; g += 90) { ctx.beginPath(); ctx.moveTo(X(g), m.oben); ctx.lineTo(X(g), m.unten); ctx.stroke(); }
    for (const v of [1, -1]) { ctx.beginPath(); ctx.moveTo(m.links, Y(v)); ctx.lineTo(m.rechts, Y(v)); ctx.stroke(); }
    // Achsen
    ctx.strokeStyle = F.ink; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(m.links, m.mitte); ctx.lineTo(m.rechts, m.mitte); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(m.links, m.oben); ctx.lineTo(m.links, m.unten); ctx.stroke();
    ctx.fillStyle = F.grau; ctx.font = schrift(fs, 600);
    ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    ctx.fillText('1', m.links - 5, Y(1)); ctx.fillText('0', m.links - 5, m.mitte); ctx.fillText('−1', m.links - 5, Y(-1));
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    [['π/2', 90], ['π', 180], ['3π/2', 270], ['2π', 360]].forEach(([t, g]) =>
      ctx.fillText(t, Math.min(X(g), m.rechts - 6), m.unten + 5));

    const bis = opt.bis == null ? 360 : opt.bis;
    const kurve = (f, farbe, lw) => {
      ctx.strokeStyle = farbe; ctx.lineWidth = lw; ctx.beginPath();
      let an = false;
      for (let px = 0; px <= breite; px += 1) {
        const g = 360 * px / breite;
        if (g > bis + 1e-9) break;
        const v = f(g * Math.PI / 180);
        if (!isFinite(v) || Math.abs(v) > 1.15) { an = false; continue; }
        if (!an) { ctx.moveTo(m.links + px, Y(v)); an = true; } else ctx.lineTo(m.links + px, Y(v));
      }
      ctx.stroke();
    };
    if (opt.tan) kurve(Math.tan, F.tan, 2);
    kurve(Math.cos, F.cos, 2.6);
    kurve(Math.sin, F.sin, 2.6);

    if (opt.marke !== false) {
      const w = werte(grad);
      const gx = X(Math.min(360, Math.max(0, grad)));
      ctx.setLineDash([3, 4]); ctx.strokeStyle = F.ink; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(gx, m.oben - 4); ctx.lineTo(gx, m.unten); ctx.stroke(); ctx.setLineDash([]);
      // Strecken wie im Kreis: Höhe = Wert
      ctx.lineCap = 'butt'; ctx.lineWidth = 4;
      ctx.strokeStyle = F.cos; ctx.beginPath(); ctx.moveTo(gx - 2.5, m.mitte); ctx.lineTo(gx - 2.5, Y(w.cos)); ctx.stroke();
      ctx.strokeStyle = F.sin; ctx.beginPath(); ctx.moveTo(gx + 2.5, m.mitte); ctx.lineTo(gx + 2.5, Y(w.sin)); ctx.stroke();
      punkt(ctx, gx, Y(w.cos), 5.5, F.cos);
      punkt(ctx, gx, Y(w.sin), 5.5, F.sin);
      if (opt.tan && isFinite(w.tan) && Math.abs(w.tan) <= 1.15) punkt(ctx, gx, Y(w.tan), 4.5, F.tan);
    }
    // Keine Legende im Bild: die Farben erklären die Regler direkt darunter (sin rot, cos blau)
    ctx.restore();
  }

  global.Einheitskreis = {
    FARBEN, werte, normiere, besonders, sinExakt, cosExakt, tanExakt, radExakt, komma,
    kreisMasse, zeichneKreis, kurvenMasse, zeichneKurven,
  };
})(typeof window !== 'undefined' ? window : globalThis);
