// Layer kit for "Jam Sebelas Malam". Every picture depends only on t.
export const W = 1080, H = 1920;
export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const seg = (t, a, d = 0.35) => clamp((t - a) / d);
export const lerp = (a, b, p) => a + (b - a) * p;
export const eo = x => 1 - Math.pow(1 - x, 3);
export const eio = x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
export const back = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
// bounce in: falls and settles (for things dropped onto something)
export const drop = x => { if (x >= 1) return 1; const n = 7.5625, d = 2.75; if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75; if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; };
// smooth deterministic noise in [-1,1]
export const noise = (t, s = 1) => Math.sin(t * 1.7 * s + 1.3) * .5 + Math.sin(t * 3.1 * s + 4.2) * .3 + Math.sin(t * 7.3 * s + .7) * .2;
// plate px (1536x2752 cover into 1080x1920)
export const PX = (x, y) => [x * 0.703125, y * 0.703125 - 7.5];

export function h(tag, cls, parent, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  (parent || document.body).appendChild(e);
  return e;
}
export function pop(el, t, t0, d = 0.32, base = 'translate(-50%,-50%)') {
  const p = seg(t, t0, d);
  el.style.opacity = p > 0 ? Math.min(1, p * 2.5) : 0;
  el.style.transform = `${base} scale(${p > 0 ? lerp(0.55, 1, back(p)) : 0.55})`;
}
export function rise(el, t, t0, d = 0.4, dist = 40) {
  const p = eo(seg(t, t0, d));
  el.style.opacity = p; el.style.transform = `translateY(${(1 - p) * dist}px)`;
}

// A cut-out layer. (x,y) is where its anchor (ax,ay of its own box) sits; w is its width in px.
export function put(parent, src, { x = 540, y = 960, w = 600, ax = 0.5, ay = 0.5, flip = false, z } = {}) {
  const el = h('img', 'cut', parent); el.src = src; el.style.width = w + 'px';
  if (z != null) el.style.zIndex = z;
  el.style.left = x + 'px'; el.style.top = y + 'px';
  el.style.transformOrigin = `${ax * 100}% ${ay * 100}%`;
  el.place = ({ dx = 0, dy = 0, rot = 0, sc = 1, op = 1 } = {}) => {
    el.style.opacity = op;
    el.style.transform = `translate(${-ax * 100}%, ${-ay * 100}%) translate(${dx}px, ${dy}px) rotate(${rot}deg) scale(${flip ? -sc : sc}, ${sc})`;
  };
  el.place();
  return el;
}

// soft light cone: starts at (x,y), points at angle (deg, 0 = right), len px long, opens to `spread` px
export function beam(parent, { x, y, angle = 0, len = 700, spread = 360, color = '255,236,196', op = 0.55, blur = 22 }) {
  // drawn once into an image (soft cone + blur), so no CSS filter runs per frame
  const pad = blur * 2, cw = len + pad * 2, ch = spread + pad * 2;
  const src = document.createElement('canvas'); src.width = cw; src.height = ch; const c = src.getContext('2d');
  const g = c.createRadialGradient(pad, ch / 2, 0, pad, ch / 2, len);
  g.addColorStop(0, `rgba(${color},${op})`); g.addColorStop(0.45, `rgba(${color},${op * 0.45})`); g.addColorStop(1, `rgba(${color},0)`);
  c.fillStyle = g; c.beginPath(); c.moveTo(pad, ch / 2 - spread * 0.04); c.lineTo(pad + len, pad); c.lineTo(pad + len, ch - pad); c.lineTo(pad, ch / 2 + spread * 0.04); c.closePath(); c.fill();
  const out = document.createElement('canvas'); out.width = cw; out.height = ch; const o = out.getContext('2d');
  o.filter = `blur(${blur}px)`; o.drawImage(src, 0, 0);
  const el = h('img', 'beam', parent); el.src = out.toDataURL();
  el.style.cssText += `left:${x - pad}px;top:${y - ch / 2}px;width:${cw}px;height:${ch}px;transform-origin:${pad}px 50%;`;
  el.at = (lx, ly) => { el.style.left = (lx - pad) + 'px'; el.style.top = (ly - ch / 2) + 'px'; };
  el.set = (o2 = 1, ang = angle) => { el.style.opacity = o2; el.style.transform = `rotate(${ang}deg)`; };
  el.set();
  return el;
}
// soft round glow
export function glow(parent, { x, y, r = 120, color = '255,214,150', op = 0.8 }) {
  const el = h('div', 'glow', parent);
  el.style.cssText += `left:${x - r}px;top:${y - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;` +
    `background:radial-gradient(circle, rgba(${color},${op}) 0%, rgba(${color},${op * 0.35}) 35%, rgba(${color},0) 70%);`;
  el.set = (o = 1, s = 1) => { el.style.opacity = o; el.style.transform = `scale(${s})`; };
  el.set();
  return el;
}

// A shot: plate + world (moves with the camera) + fog + vignette + ui (fixed)
export function shot({ bg, dur, from = 1.06, to = 1.14, ox = 50, oy = 50, blur = 0, dim = 0, kick = 0.14, drift = [0, 0], fog = 0.3, tint = null, punches = [] }) {
  const world = h('div', 'world');
  // blurred plates are pre-rendered files (<name>-b<px>.jpg): a CSS blur every frame is too slow for the renderer
  if (bg) { const p = h('img', 'plate', world); p.src = blur ? bg.replace('.jpg', `-b${blur}.jpg`) : bg; }
  if (tint) { const d = h('div', 'blk', world); d.style.background = tint; }
  const cv = h('canvas', 'fxc'); cv.width = W / 2; cv.height = H / 2; const ctx = cv.getContext('2d');
  h('div', 'vig');
  const ui = h('div', 'screen');
  if (blur) { const d = h('div', 'blk', world); d.style.background = `rgba(0,0,0,${dim})`; }
  const blobs = Array.from({ length: 7 }, (_, i) => ({ x: (i * 173) % 540, y: 420 + (i * 97) % 520, r: 160 + (i * 53) % 140, v: 6 + (i * 7) % 10 }));
  return {
    world, ui,
    set(t) {
      const p = clamp(t / dur), k = kick ? 1 - eo(clamp(t / kick)) : 0;
      const sc = lerp(from, to, eio(p * 0.85 + 0.15 * p)) * (1 + 0.1 * k);
      let s2 = sc, o = [ox, oy];
      const pu = punches.filter(q => t >= q[0]).pop();
      if (pu) { const kk = 1 - eo(clamp((t - pu[0]) / 0.14)); s2 = sc * pu[1] * (1 + 0.07 * kk); o = [pu[2], pu[3]]; }
      world.style.transformOrigin = `${o[0]}% ${o[1]}%`;
      world.style.transform = `translate(${drift[0] * p}px, ${drift[1] * p}px) scale(${s2})`;
      ctx.clearRect(0, 0, W / 2, H / 2);
      if (fog > 0) for (const b of blobs) {
        const x = ((b.x + b.v * t * 4) % 760) - 110;
        const g = ctx.createRadialGradient(x, b.y, 0, x, b.y, b.r);
        g.addColorStop(0, `rgba(170,200,200,${0.09 * fog})`); g.addColorStop(1, 'rgba(170,200,200,0)');
        ctx.fillStyle = g; ctx.fillRect(x - b.r, b.y - b.r, 2 * b.r, 2 * b.r);
      }
    },
  };
}

export const CHECK = '<svg viewBox="0 0 40 40"><path d="M7 21 L16 30 L34 9" fill="none" stroke="#e5484d" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

export function boot(duration, frame) {
  const fonts = ['400 40px Anton', '800 40px Montserrat', '700 40px SpaceMono'].map(f => document.fonts.load(f));
  const imgs = [...document.images].map(i => i.decode().catch(() => {}));
  window.film = { duration, frame, ready: Promise.all([...fonts, ...imgs]) };
}

// rain streaks, deterministic in t (drawn on its own canvas)
export function rain(parent, { n = 140, speed = 2600, len = 46, op = 0.22, angle = 0.12, w = 2 } = {}) {
  const cv = h('canvas', 'fxc', parent); cv.width = W; cv.height = H; const c = cv.getContext('2d');
  const drops = Array.from({ length: n }, (_, i) => ({ x: (i * 397.13) % (W + 300) - 150, y: (i * 911.7) % H, v: 0.7 + ((i * 37) % 10) / 16, l: 0.6 + ((i * 13) % 10) / 12 }));
  return t => {
    c.clearRect(0, 0, W, H); c.lineWidth = w; c.lineCap = 'round';
    for (const d of drops) {
      const y = (d.y + t * speed * d.v) % (H + 200) - 100, x = d.x + y * angle, L = len * d.l;
      c.strokeStyle = `rgba(205,225,230,${op * (0.5 + d.l / 2)})`;
      c.beginPath(); c.moveTo(x, y); c.lineTo(x + L * angle, y + L); c.stroke();
    }
  };
}
// hazard blink, 1.4 Hz like a real flasher: returns 0/1 with soft edges
export const blink = (t, t0 = 0) => t < t0 ? 0 : (((t - t0) * 1.4) % 1 < 0.5 ? 1 : 0.08);
export function stepNum(parent, n, label, y = 380) {
  const e = h('div', 'step', parent, `<b>${n}</b><span>${label}</span>`); e.style.top = y + 'px'; return e;
}

// perspective map of a w x h box onto 4 points [TL, TR, BR, BL] (CSS matrix3d; set transform-origin 0 0)
export function homog(w, hh, P) {
  const src = [[0, 0], [w, 0], [w, hh], [0, hh]], A = [], B = [];
  src.forEach(([u, v], i) => { const [x, y] = P[i];
    A.push([u, v, 1, 0, 0, 0, -u * x, -v * x]); B.push(x);
    A.push([0, 0, 0, u, v, 1, -u * y, -v * y]); B.push(y); });
  for (let c = 0; c < 8; c++) { let p = c; for (let r = c + 1; r < 8; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
    [A[c], A[p]] = [A[p], A[c]]; [B[c], B[p]] = [B[p], B[c]];
    for (let r = 0; r < 8; r++) if (r !== c) { const f = A[r][c] / A[c][c]; for (let k = c; k < 8; k++) A[r][k] -= f * A[c][k]; B[r] -= f * B[c]; } }
  const [a, bb, c, d, e, f, g, k] = B.map((v, i) => v / A[i][i]);
  return `matrix3d(${a},${d},0,${g},${bb},${e},0,${k},0,0,1,0,${c},${f},0,1)`;
}
// white flash for hard cuts (0..1 over d seconds)
export const flash = (t, t0, d = 0.18) => t >= t0 && t < t0 + d ? 1 - (t - t0) / d : 0;
