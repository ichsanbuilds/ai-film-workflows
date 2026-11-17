#!/usr/bin/env python3
"""v2 — "The Driver" in the @heist_logic style: layered stills that MOVE (cutouts, variants swapped on words,
object scenes, wipers, passing streetlight sweeps, a self-drawing map, into-the-phone transition, one AI clip).
Reframes stay only as light seasoning. Times are film seconds = VO seconds (../vo/words-v1.json)."""
import textwrap, os, json
os.makedirs('shots', exist_ok=True)
for f in os.listdir('shots'): os.remove('shots/' + f)
WORDS = json.load(open('vo/words-v1.json'))
END = 86.6
HEAD = '''<!doctype html>
<html><head><meta charset="utf-8"><link rel="stylesheet" href="../shared/kit.css">
<style>{css}</style></head>
<body>
<script type="module">
import {{ W, H, shot, put, glow, h, pop, rise, seg, eo, eio, back, drop, lerp, clamp, noise, rain, flash, boot }} from '../shared/kit.js';
const I = '../assets/img/', C = '../assets/cut/';
{js}
</script></body></html>
'''
CSS = '''
.flashw{position:absolute;inset:0;background:#fff;pointer-events:none;opacity:0}
.cop{position:absolute;inset:0;pointer-events:none;mix-blend-mode:screen;opacity:0}
.sweep{position:absolute;inset:-20% -60%;pointer-events:none;mix-blend-mode:screen;
  background:linear-gradient(100deg,transparent 42%,rgba(255,186,104,.30) 50%,transparent 58%)}
.wiper{position:absolute;width:16px;height:980px;border-radius:8px;background:linear-gradient(90deg,#050708,#1b2326,#050708);
  transform-origin:50% 100%;box-shadow:0 0 18px rgba(0,0,0,.6)}
.tag{position:absolute;transform:translate(-50%,-50%);font:700 26px SpaceMono,monospace;letter-spacing:2px;color:#fff;white-space:nowrap;
  background:rgba(10,14,16,.88);border:2px solid rgba(255,255,255,.22);border-radius:10px;padding:7px 14px}
.tag b{color:#ff4f8b}.tag.y b{color:#ffd34d}.tag.g b{color:#3ccf91}.tag.r b{color:#ff3b5c}
.line{position:absolute;height:3px;background:#fff;transform-origin:0 50%;box-shadow:0 0 6px rgba(0,0,0,.8)}
.notif{position:absolute;left:110px;right:110px;top:300px;background:rgba(245,247,248,.97);color:#111;border-radius:30px;padding:26px 30px;
  box-shadow:0 24px 60px rgba(0,0,0,.55);font:800 34px Montserrat;display:flex;gap:22px;align-items:center}
.notif .ic{width:74px;height:74px;border-radius:18px;background:#111;flex:none;display:flex;align-items:center;justify-content:center;color:#3ccf91;font:400 44px Anton}
.notif small{display:block;font:700 22px SpaceMono;color:#666;margin-bottom:6px;letter-spacing:1px}
.money{position:absolute;left:50%;transform:translate(-50%,-50%);font:400 200px/1 Anton;color:#3ccf91;text-shadow:0 10px 40px rgba(0,0,0,.75);white-space:nowrap}
.plus{position:absolute;font:400 70px Anton;color:#3ccf91;text-shadow:0 6px 20px rgba(0,0,0,.8);transform:translate(-50%,-50%)}
.paper{position:absolute;left:110px;right:110px;background:#f3efe4;color:#14181a;border-radius:18px;padding:34px 38px;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.paper h3{margin:0 0 18px;font:400 64px/1 Anton;letter-spacing:1px}
.paper .row{display:flex;justify-content:space-between;align-items:center;font:700 34px SpaceMono;padding:12px 0;border-top:2px dashed rgba(0,0,0,.18)}
.paper .row i{font-style:normal;color:#c9302c}
.vs{position:absolute;top:470px;width:440px;height:760px;border-radius:26px;background:rgba(10,14,16,.9);border:3px solid rgba(255,255,255,.18);overflow:hidden}
.vs .lab{position:absolute;left:0;right:0;bottom:26px;text-align:center;font:400 64px/1 Anton;letter-spacing:1px}
.bar{position:absolute;left:140px;right:140px;height:26px;border-radius:13px;background:rgba(255,255,255,.15);overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#ff3b5c,#ff9f1c)}
.btn{flex:1;text-align:center;font:400 104px/1 Anton;padding:34px 0;border-radius:26px;color:#111;box-shadow:0 14px 40px rgba(0,0,0,.55)}
'''
SHOTS = []
COMMON = '''
const FW = h('div', 'flashw', S.ui);
const COP = h('div', 'cop', S.ui);
function cop(t, amt) { const on = Math.floor(t * 3) % 2; COP.style.opacity = amt;
  COP.style.background = on ? 'radial-gradient(ellipse at 15% 20%, rgba(255,40,70,.85), transparent 60%)' : 'radial-gradient(ellipse at 85% 20%, rgba(40,110,255,.85), transparent 60%)'; }
function sweeper(parent, per = 1.5, op = 1) { const d = h('div', 'sweep', parent); return t => { const q = ((t / per) % 1); d.style.transform = `translateX(${lerp(-60, 60, q)}%)`; d.style.opacity = op * Math.sin(q * Math.PI); }; }
function wiper(parent, x, y, len = 980, per = 1.15, a0 = -72, a1 = 18) { const d = h('div', 'wiper', parent); d.style.left = (x - 8) + 'px'; d.style.top = (y - len) + 'px'; d.style.height = len + 'px';
  return t => { const q = Math.abs(Math.sin(t * Math.PI / per)); d.style.transform = `rotate(${lerp(a0, a1, eio(q))}deg)`; }; }
function variant(src, ts, te = 1e9) { const v = put(S.world, src, { x: 540, y: 960, w: 1080 }); return t => v.place({ op: t >= ts && t < te ? 1 : 0 }); }
function tag(html, x, y, cls = '') { const d = h('div', 'tag ' + cls, S.ui, html); d.style.left = x + 'px'; d.style.top = y + 'px'; return d; }
'''

def P(start, end, pois, every=1.1, first=0.5):
    out, last, k = [], start + first - every, 0
    for w in WORDS:
        if start + first <= w['s'] < end - 0.3 and w['s'] - last >= every:
            sc, ox, oy = pois[k % len(pois)]; out.append([round(w['s'] - start, 3), sc, ox, oy]); last = w['s']; k += 1
    return json.dumps(out)

def page(name, start, end, js_setup, js_each, bg=None, blur=0, dim=0, frm=1.04, to=1.1, ox=50, oy=50, kick=.08, pois=None, every=1.1, rain_n=0, flash_in=True, drift=(0, 0)):
    dur = round(end - start, 3)
    pun = P(start, end, pois, every) if pois else '[]'
    bgs = f"I + '{bg}.jpg'" if bg else 'null'
    js = f'''
const T0 = {start}; const T = x => x - T0; const DUR = {dur};
const S = shot({{ bg: {bgs}, dur: DUR, from: {frm}, to: {to}, ox: {ox}, oy: {oy}, kick: {kick}, blur: {blur}, dim: {dim}, drift: [{drift[0]}, {drift[1]}], punches: {pun} }});
''' + COMMON + (f"const R = rain(S.ui, {{ n: {rain_n}, op: .14 }});\n" if rain_n else '') + textwrap.dedent(js_setup) + f'''
boot(DUR, t => {{ S.set(t); {'R(t);' if rain_n else ''} {'FW.style.opacity = flash(t, 0, .1) * .3;' if flash_in else ''}
{textwrap.dedent(js_each)}
}});
'''
    open(f'shots/{name}.html', 'w').write(HEAD.format(css=CSS, js=js))
    SHOTS.append((name, start, end))

# 1. 2:14 AM
page('s01-dash', 0.0, 1.78, '''
const B1 = variant(I + 'D1-blink.jpg', 0.95, 1.12);
const SW = sweeper(S.ui, 1.3, .9);
''', 'B1(t); SW(t);', bg='D1', frm=1.0, to=1.08, oy=40, flash_in=False, rain_n=50)
page('s02-hours', 1.78, 4.00, '''
const SW = sweeper(S.ui, 1.1, 1);
const st = h('div', 'stamp', S.ui, ''); st.style.top = '1250px'; st.style.fontSize = '160px';
const lb = tag('HOURS DRIVING', 540, 1370, 'y');
''', '''SW(t); const n = Math.round(lerp(0, 11, eo(seg(t, T(2.4), .9)))); st.innerHTML = t > T(2.4) ? `<em style="color:#ff9f1c">${n}</em>:00` : ''; st.style.opacity = 1;
pop(lb, t, T(2.83), .25);''', bg='D7', frm=1.05, to=1.12, oy=45, drift=(0, -20))
page('s03-ride', 4.00, 6.51, '''
const card = h('div', 'paper', S.ui); card.style.top = '330px';
card.innerHTML = '<h3>TONIGHT</h3><div class="row">RIDES <span id="r">23</span></div><div class="row">HOURS <span>11</span></div><div class="row">LEFT <i id="l">1 RIDE</i></div>';
const r = card.querySelector('#r'), l = card.querySelector('#l');
''', '''rise(card, t, 0.05, .35, 120); r.textContent = t > T(4.55) ? '24' : '23'; l.textContent = t > T(5.75) ? 'DONE?' : '1 RIDE';''',
     bg='D2', frm=1.08, to=1.16, ox=40, oy=60, rain_n=110, drift=(-40, 0))
# 2. the pickup
page('s04-bank', 6.51, 8.42, '''
const N = h('div', 'notif', S.ui, '<div class="ic">R</div><div><small>NEW RIDE · 2 MIN</small>Pickup: the bank on 5th</div>');
const pin = tag('<b>●</b> PICKUP', 300, 560);
''', '''const p = eo(seg(t, 0.1, .3)); N.style.opacity = p; N.style.transform = `translateY(${(1 - p) * -160}px)`;
pop(pin, t, T(7.74), .25);''', bg='D3', frm=1.2, to=1.3, ox=35, oy=30, rain_n=90)
page('s05-men', 8.42, 10.00, '''
const tg = [[300, 700], [520, 640], [720, 700]].map(([x, y], i) => tag('<b>' + (i + 1) + '</b>', x, y));
const st = h('div', 'stamp', S.ui, '<em>3</em> MEN. <em>SUITS.</em>'); st.style.top = '1450px'; st.style.fontSize = '120px';
''', '''tg.forEach((e, i) => pop(e, t, T(8.42) + .12 * i, .22)); pop(st, t, T(9.21), .22);''', bg='D4', frm=1.08, to=1.18, oy=45, rain_n=60)
page('s06-bag', 10.00, 11.74, '''
const BG = put(S.ui, C + 'bag.png', { x: 540, y: 1050, w: 720 });
const lb = tag('<b>HEAVY</b> · BLACK BAG', 540, 1480);
const dust = [0, 1, 2, 3, 4, 5].map(() => { const d = h('div', 'abs', S.ui); d.style.cssText += 'width:30px;height:30px;border-radius:50%;background:rgba(220,230,230,.35)'; return d; });
''', '''const p = seg(t, 0.05, .55), land = 0.6; BG.place({ dy: lerp(-1300, 0, drop(p)), rot: lerp(-8, 0, p) });
const q = seg(t, land, .5); dust.forEach((d, i) => { const a = (i / 5 - .5) * 2.4; d.style.left = (540 + Math.sin(a) * 340 * eo(q)) + 'px'; d.style.top = (1330 - Math.cos(a) * 60 * eo(q)) + 'px'; d.style.opacity = q > 0 ? (1 - q) : 0; d.style.transform = `scale(${1 + q * 2})`; });
pop(lb, t, T(10.65), .25);''', bg='D4', blur=22, dim=.45, frm=1.1, to=1.12)
page('s07-laps', 11.74, 15.41, '''
const st = h('div', 'stamp', S.ui, 'NOT IN THE <em>TRUNK</em>'); st.style.top = '380px'; st.style.fontSize = '104px';
const x = h('div', 'stamp', S.ui, '<em style="color:#ff3b5c">✕</em>'); x.style.top = '380px'; x.style.fontSize = '240px';
const lap = tag('ON THEIR <b>LAPS</b>', 540, 1240);
const ln = h('div', 'line', S.ui); ln.style.left = '540px'; ln.style.top = '1265px';
const SW = sweeper(S.ui, 1.6, .8);
''', '''pop(st, t, T(12.16), .25); pop(x, t, T(12.71), .2); x.style.opacity = t > T(12.71) && t < T(13.4) ? 1 : 0; st.style.opacity = t < T(13.4) ? st.style.opacity : 0;
pop(lap, t, T(14.49), .25); const lp = eo(seg(t, T(14.6), .3)); ln.style.width = (170 * lp) + 'px'; ln.style.transform = 'rotate(70deg)'; SW(t);''',
     bg='D5', frm=1.05, to=1.12, oy=55, pois=[[1.1, 50, 65]], every=1.6)
page('s08-guy', 15.41, 17.67, '''
const SW = sweeper(S.ui, 1.2, .9);
const lb = tag('BEHIND <b>YOU</b>', 300, 420);
''', 'SW(t); pop(lb, t, T(15.86), .25);', bg='D6', frm=1.05, to=1.14, ox=30, oy=30)
page('s09-justdrive', 17.67, 20.16, '''
const L = put(S.ui, C + 'leader.png', { x: 640, y: 1920, w: 820, ax: .5, ay: 1 });
const q1 = h('div', 'stamp', S.ui, '<em style="color:#ff9f1c">"JUST DRIVE."</em>'); q1.style.top = '420px'; q1.style.fontSize = '120px';
const q2 = h('div', 'stamp', S.ui, '<em style="color:#ff9f1c">"DON\\'T LOOK BACK."</em>'); q2.style.top = '420px'; q2.style.fontSize = '96px';
''', '''const p = eo(seg(t, 0, .45)); L.place({ dx: lerp(700, 0, p), sc: lerp(1, 1.08, seg(t, .5, 2)), rot: lerp(6, 0, p) });
pop(q1, t, T(17.67), .2); q1.style.opacity = t < T(18.91) ? q1.style.opacity : 0; pop(q2, t, T(18.91), .2); q2.style.opacity = t >= T(18.91) ? q2.style.opacity : 0;''',
     bg='D6', blur=22, dim=.5, frm=1.1, to=1.14)
page('s10-pull', 20.16, 21.41, '''
const streaks = Array.from({ length: 14 }, (_, i) => { const d = h('div', 'abs', S.ui); d.style.cssText += `height:4px;border-radius:2px;background:rgba(255,200,130,.55);top:${200 + i * 110}px;width:${180 + (i * 53) % 260}px`; return d; });
''', '''S.world.style.translate = `${noise(t * 30) * 6}px ${noise(t * 23) * 4}px`;
streaks.forEach((d, i) => { const q = ((t * 1.8 + i * .13) % 1); d.style.left = lerp(1200, -500, q) + 'px'; d.style.opacity = .8 * Math.sin(q * Math.PI); });''',
     bg='D7', frm=1.12, to=1.2, oy=55, kick=.2)
# 3. sirens
page('s11-blocks', 21.41, 23.57, '''
const card = h('div', 'paper', S.ui); card.style.top = '360px';
card.innerHTML = '<h3>2 BLOCKS</h3><div style="position:relative;height:120px"><div id="rt" style="position:absolute;left:0;top:56px;height:10px;border-radius:5px;background:#14181a"></div><div id="car" style="position:absolute;top:30px;font:400 56px Anton">▶</div></div>';
const rt = card.querySelector('#rt'), car = card.querySelector('#car');
''', '''rise(card, t, 0.05, .35, 120); const p = eio(seg(t, .2, 1.6)); rt.style.width = (p * 100) + '%'; car.style.left = `calc(${p * 100}% - 30px)`; cop(t, seg(t, 1.9, .3) * .35);''',
     bg='D2', frm=1.1, to=1.2, ox=45, oy=55, rain_n=110, drift=(-50, 0))
page('s12-sirens', 23.57, 27.38, '''
const N2 = variant(I + 'D8.jpg', T(25.34));
const dots = [0, 1].map(i => glow(S.world, { x: 560 + i * 60, y: 380, r: 30, color: i ? '60,120,255' : '255,50,80', op: 1 }));
const st = h('div', 'stamp', S.ui, '<em style="color:#ff3b5c">SIRENS.</em>'); st.style.top = '1450px'; st.style.fontSize = '190px';
const bar = h('div', 'bar', S.ui, '<i></i>'); bar.style.top = '1600px'; const bi = bar.querySelector('i');
const lb = tag('DISTANCE', 540, 1560, 'r');
''', '''N2(t); const on = Math.floor(t * 3) % 2; const gr = lerp(.4, 1.2, seg(t, 0, 3)); dots[0].set(t < T(25.34) ? (on ? 1 : .15) : 0, gr); dots[1].set(t < T(25.34) ? (on ? .15 : 1) : 0, gr);
pop(st, t, 0, .2); st.style.opacity = t < T(25.3) ? st.style.opacity : 0; pop(lb, t, T(24.55), .2); lb.style.opacity = t > T(24.55) ? 1 : 0;
bar.style.opacity = t > T(24.55) ? 1 : 0; bi.style.width = lerp(15, 35, seg(t, T(24.6), 2.5)) + '%'; cop(t, t > T(25.34) ? .25 + seg(t, T(25.9), 1.4) * .25 : 0);''',
     bg='D12-normal', frm=1.15, to=1.25, oy=28)
# 4. the cash
page('s13-mirror', 27.38, 31.06, '''
const OPEN = variant(I + 'D9.jpg', T(29.86));
const lb = tag('THE <b>BAG</b>', 540, 1180);
''', '''OPEN(t); FW.style.opacity = flash(t, T(29.86), .18) * .6; pop(lb, t, T(28.87), .25); lb.style.opacity = t < T(29.86) ? lb.style.opacity : 0; cop(t, .15);''',
     bg='D9-closed', frm=1.25, to=1.4, ox=50, oy=33)
page('s14-cash', 31.06, 33.16, '''
const BO = put(S.ui, C + 'bag-open.png', { x: 540, y: 1000, w: 820 });
const st = h('div', 'stamp', S.ui, '<em style="color:#3ccf91">CASH.</em>'); st.style.top = '420px'; st.style.fontSize = '200px';
const lb = tag('<b>STACKS</b> OF IT', 540, 1440, 'g');
''', '''BO.place({ sc: lerp(.6, 1, back(seg(t, 0, .35))), rot: Math.sin(t * 3) * 1.5 }); pop(st, t, 0, .2); pop(lb, t, T(31.92), .25);''',
     bg='D9', blur=22, dim=.45, frm=1.1, to=1.14)
page('s15-bricks', 33.16, 37.09, '''
const m = h('div', 'money', S.ui, ''); m.style.top = '380px'; m.style.fontSize = '170px';
const pl = [0, 1, 2, 3, 4].map(() => h('div', 'plus', S.ui, '+$10,000'));
''', '''const k = Math.min(5, Math.max(0, Math.floor((t - T(33.72)) / .55) + 1));
m.innerHTML = '$' + (k * 10000).toLocaleString('en-US'); m.style.opacity = k ? 1 : 0;
pl.forEach((e, i) => { const t0 = T(33.72) + i * .55, q = seg(t, t0, .9); e.style.left = (420 + i * 60) + 'px'; e.style.top = lerp(1000, 760, eo(q)) + 'px'; e.style.opacity = q > 0 && q < 1 ? 1 - q : 0; });''',
     frm=1, to=1, kick=0, flash_in=False)
page('s16-yours', 37.09, 40.00, '''
const q1 = h('div', 'stamp', S.ui, '<em style="color:#ff9f1c">"KEEP DRIVING,<br>AND IT\\'S YOURS."</em>'); q1.style.top = '420px'; q1.style.fontSize = '96px';
const m = h('div', 'money', S.ui, '$50,000'); m.style.top = '1450px';
const SW = sweeper(S.ui, 1.3, .9);
''', '''pop(q1, t, T(37.56), .25); pop(m, t, 0, .3); SW(t);''', bg='D10', frm=1.05, to=1.15, ox=40, oy=60)
page('s17-bills', 40.00, 46.10, '''
const SH = variant(I + 'D11-shock.jpg', T(40.58));
const card = h('div', 'paper', S.ui); card.style.top = '1180px';
card.innerHTML = '<h3>$50,000 =</h3><div class="row" id="a">EVERY BILL YOU OWE <i>✓</i></div><div class="row" id="b">RENT <i>3 YEARS</i></div>';
const a = card.querySelector('#a'), b = card.querySelector('#b');
''', '''SH(t); FW.style.opacity = flash(t, T(40.58), .15) * .5; rise(card, t, T(42.11), .35, 100); card.style.opacity = t > T(42.11) ? card.style.opacity : 0;
a.style.opacity = t > T(42.49) ? 1 : 0; b.style.opacity = t > T(44.41) ? 1 : 0;''', bg='D11', frm=1.04, to=1.12, oy=38, pois=[[1.15, 50, 35]], every=2)
# 5. closing in
page('s18-redblue', 46.10, 49.95, '''
const RB = variant(I + 'D12.jpg', T(47.99));
const bar = h('div', 'bar', S.ui, '<i></i>'); bar.style.top = '1600px'; const bi = bar.querySelector('i');
const lb = tag('SIRENS <b>CLOSER</b>', 540, 1560, 'r');
''', '''RB(t); FW.style.opacity = flash(t, T(47.99), .15) * .5; cop(t, t > T(47.99) ? .55 : .15); bi.style.width = lerp(35, 70, seg(t, 0, 3.5)) + '%'; pop(lb, t, 0.1, .25);''',
     bg='D12-normal', frm=1.1, to=1.2, oy=30, kick=.12)
page('s19-phone', 49.95, 53.50, '''
const PHN = put(S.ui, C + 'phone.png', { x: 540, y: 1000, w: 560 });
// screen of phone.png (476x652) measured at x .452-.904, y .153-.828; phone box: left 260, top 616.4, 560x767.2
const scr = h('canvas', 'abs', S.ui); scr.width = 253; scr.height = 518; const g = scr.getContext('2d');
scr.style.cssText += 'left:513px;top:734px;width:253px;height:518px;border-radius:6px;transform-origin:126px 266px';
const N = h('div', 'notif', S.ui, '<div class="ic">R</div><div><small>RIDE APP · NOW</small>Rider changed destination</div>');
function map(c, k) { c.fillStyle = '#16302f'; c.fillRect(0, 0, 253, 518); c.strokeStyle = 'rgba(160,210,205,.25)'; c.lineWidth = 5;
  for (let i = 0; i < 8; i++) { c.beginPath(); c.moveTo(0, i * 72 + 20); c.lineTo(253, i * 72 - 10); c.stroke(); c.beginPath(); c.moveTo(i * 38, 0); c.lineTo(i * 38 + 22, 518); c.stroke(); }
  c.strokeStyle = '#3ccf91'; c.lineWidth = 7; c.beginPath(); c.moveTo(126, 460); c.lineTo(126, 300); c.lineTo(60, 200); c.stroke();
  if (k) { c.strokeStyle = '#ff4f8b'; c.beginPath(); c.moveTo(126, 300); c.lineTo(200, 140); c.lineTo(200, 60); c.stroke(); c.fillStyle = '#ff3b5c'; c.beginPath(); c.arc(200, 60, 12, 0, 7); c.fill(); }
  c.fillStyle = '#3ccf91'; c.beginPath(); c.arc(126, 460, 10, 0, 7); c.fill(); }
''', '''const p = eo(seg(t, 0, .4)); const sh = t > T(50.52) && t < T(51.4) ? noise(t * 50) * 3 : 0; PHN.place({ dy: lerp(900, 0, p), rot: sh });
map(g, t > T(51.49)); scr.style.transform = `translateY(${lerp(900, 0, p)}px) rotate(${sh}deg)`;
const q = eo(seg(t, T(51.49), .3)); N.style.opacity = q; N.style.transform = `translateY(${(1 - q) * -160}px)`;''',
     bg='D13', blur=22, dim=.5, frm=1.1, to=1.12)
page('s20-river', 53.50, 56.96, '''
const cv = h('canvas', 'abs', S.ui); cv.width = 1080; cv.height = 1920; const c = cv.getContext('2d');
const pin = tag('<b>●</b> NEW STOP', 760, 470);
const lot = tag('EMPTY <b>LOT</b> · RIVER', 540, 1560, 'r');
const route = [[540, 1700], [540, 1350], [380, 1180], [380, 900], [620, 700], [760, 560]];
''', '''const z = lerp(1.25, 1, eo(seg(t, 0, .5))); cv.style.transform = `scale(${z})`;
c.fillStyle = '#16302f'; c.fillRect(0, 0, 1080, 1920);
c.strokeStyle = 'rgba(160,210,205,.22)'; c.lineWidth = 16; for (let i = 0; i < 14; i++) { c.beginPath(); c.moveTo(0, i * 150); c.lineTo(1080, i * 150 - 60); c.stroke(); c.beginPath(); c.moveTo(i * 90, 0); c.lineTo(i * 90 + 80, 1920); c.stroke(); }
c.fillStyle = '#1f4e7a'; c.beginPath(); c.moveTo(0, 380); c.bezierCurveTo(400, 300, 700, 520, 1080, 420); c.lineTo(1080, 560); c.bezierCurveTo(700, 660, 400, 440, 0, 520); c.fill();
const p = eio(seg(t, .2, 2.2)); const tot = route.length - 1, f = p * tot, k = Math.floor(f);
c.strokeStyle = '#ff4f8b'; c.lineWidth = 18; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath(); c.moveTo(...route[0]);
for (let i = 1; i <= k && i <= tot; i++) c.lineTo(...route[i]);
if (k < tot) { const a = route[k], b = route[k + 1], u = f - k; c.lineTo(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u); } c.stroke();
c.fillStyle = '#3ccf91'; c.beginPath(); c.arc(540, 1700, 22, 0, 7); c.fill();
if (p >= 1) { c.fillStyle = '#ff3b5c'; c.beginPath(); c.arc(760, 560, 30 + 6 * Math.sin(t * 8), 0, 7); c.fill(); }
pop(pin, t, T(53.88), .25); pop(lot, t, T(55.16), .25);''', frm=1, to=1, kick=0)
page('s21-seeit', 56.96, 58.47, '''
const B = h('div', 'blk', S.ui); B.style.background = 'radial-gradient(ellipse at 50% 15%, transparent 25%, rgba(0,0,0,.88) 70%)';
''', '''const beat = Math.max(0, Math.sin(t * Math.PI * 2.4)) ** 6; S.world.style.scale = 1 + beat * .05; cop(t, .12);''', bg='D16', frm=1.15, to=1.25, oy=15)
# 6. the badge
page('s22-leans', 58.47, 62.29, '''
const OP = variant(I + 'D14.jpg', T(61.82));
const SW = sweeper(S.ui, 1.4, .8);
''', '''OP(t); SW(t); FW.style.opacity = flash(t, T(61.82), .15) * .5;''', bg='D14-closed', frm=1.0, to=1.12, ox=52, oy=55, pois=[[1.2, 52, 62]], every=1.8)
page('s23-badge', 62.29, 66.50, '''
const BD = put(S.ui, C + 'badge.png', { x: 540, y: 950, w: 640 });
const shine = h('div', 'sweep', S.ui); shine.style.background = 'linear-gradient(100deg,transparent 45%,rgba(255,255,255,.55) 50%,transparent 55%)';
const st = h('div', 'stamp', S.ui, '<em style="color:#ffd34d">POLICE BADGE</em>'); st.style.top = '1500px'; st.style.fontSize = '130px';
const lb = tag('CLIPPED TO HIS <b>BELT</b>', 540, 360, 'y');
''', '''const p = seg(t, 0, .5); BD.place({ sc: lerp(.3, 1, back(p)) * (1 + .03 * Math.sin(t * 3)), rot: lerp(-25, 0, eo(p)) });
const s = seg(t, T(65.11), .5); shine.style.transform = `translateX(${lerp(-60, 60, s)}%)`; shine.style.opacity = s > 0 && s < 1 ? 1 : 0;
pop(lb, t, T(63.01), .25); pop(st, t, T(65.11), .2); st.style.opacity = t >= T(65.11) ? 1 : 0; FW.style.opacity = flash(t, T(65.11), .2) * .7;''',
     bg='D14', blur=22, dim=.55, frm=1.1, to=1.14)
page('s24-dirty', 66.50, 68.92, '''
const BD = put(S.ui, C + 'badge.png', { x: 290, y: 980, w: 430 });
const CA = put(S.ui, C + 'bag-open.png', { x: 800, y: 1000, w: 500 });
const dv = h('div', 'abs', S.ui); dv.style.cssText += 'left:538px;top:300px;width:4px;height:1350px;background:linear-gradient(#ff3b5c,#2a6dff)';
const a = h('div', 'stamp', S.ui, 'DIRTY <em style="color:#ffd34d">COP?</em>'); a.style.top = '420px'; a.style.left = '290px'; a.style.fontSize = '96px';
const b = h('div', 'stamp', S.ui, 'OR A <em style="color:#3ccf91">SETUP?</em>'); b.style.top = '1530px'; b.style.left = '800px'; b.style.fontSize = '96px';
''', '''const p = eo(seg(t, 0, .35)); BD.place({ dx: lerp(-500, 0, p) }); CA.place({ dx: lerp(500, 0, p) });
pop(a, t, T(66.69), .2); a.style.opacity = t >= T(66.69) ? a.style.opacity : 0; pop(b, t, T(67.7), .2); b.style.opacity = t >= T(67.7) ? b.style.opacity : 0; cop(t, .2);''',
     bg='D15', blur=22, dim=.6, frm=1.1, to=1.12)
page('s25-scares', 68.92, 76.38, '''
const st = h('div', 'stamp', S.ui, 'WHO SCARES<br>YOU <em>MORE?</em>'); st.style.top = '300px'; st.style.fontSize = '100px';
const L = h('div', 'vs', S.ui); L.style.left = '80px'; const R2 = h('div', 'vs', S.ui); R2.style.left = '560px';
const cc = put(L, C + 'copcar.png', { x: 220, y: 330, w: 420 }); const ld = put(R2, C + 'leader.png', { x: 220, y: 760, w: 470, ax: .5, ay: 1 });
h('div', 'lab', L, '<span style="color:#ff3b5c">BEHIND</span>'); h('div', 'lab', R2, '<span style="color:#ffd34d">INSIDE</span>');
''', '''pop(st, t, T(70.51), .25); st.style.opacity = t >= T(70.51) ? st.style.opacity : 0;
const pl = eo(seg(t, T(72.24), .35)), pr = eo(seg(t, T(74.01), .35));
L.style.opacity = pl; L.style.transform = `translateY(${(1 - pl) * 120}px) scale(${t > T(72.24) && t < T(74.01) ? 1.04 : t >= T(74.01) ? .94 : 1})`;
R2.style.opacity = pr; R2.style.transform = `translateY(${(1 - pr) * 120}px) scale(${t >= T(74.01) ? 1.06 : 1})`;
cc.place({ sc: 1 + .04 * Math.sin(t * 6) }); cop(t, t > T(72.24) && t < T(74.01) ? .4 : .15);''',
     bg='D16', blur=22, dim=.55, frm=1.1, to=1.15)
# 7. the choice
page('s28-green', 76.38, 77.97, '''
const GR = variant(I + 'D17.jpg', T(77.24));
''', '''GR(t); FW.style.opacity = flash(t, T(77.24), .15) * .4;''', bg='D17-red', frm=1.15, to=1.25, oy=30, rain_n=110)
page('s29-oneblock', 77.97, 80.19, '''
const CC = put(S.world, C + 'copcar.png', { x: 600, y: 760, w: 300 });
const bar = h('div', 'bar', S.ui, '<i></i>'); bar.style.top = '1600px'; const bi = bar.querySelector('i');
const lb = tag('SIRENS · <b>1 BLOCK</b>', 540, 1560, 'r');
''', '''const p = eio(seg(t, 0, 2.2)); CC.place({ sc: lerp(.6, 1.6, p), dy: lerp(-40, 220, p), dx: lerp(0, -60, p) }); cop(t, .35 + .35 * p);
bi.style.width = lerp(80, 97, p) + '%'; pop(lb, t, T(78.9), .25);''', bg='D19', frm=1.05, to=1.15, rain_n=110)
page('s30-pedal', 80.19, 82.16, '''
const D = put(S.ui, C + 'drv-shock.png', { x: 860, y: 1920, w: 420, ax: .5, ay: 1 });
const a = h('div', 'stamp', S.ui, '<em style="color:#3ccf91">DRIVE</em>'); a.style.top = '480px'; a.style.fontSize = '170px';
const b = h('div', 'stamp', S.ui, '<em style="color:#ff3b5c">STOP?</em>'); b.style.top = '480px'; b.style.fontSize = '170px';
''', '''D.place({ dy: lerp(500, 0, eo(seg(t, 0, .4))) }); const beat = Math.max(0, Math.sin(t * Math.PI * 2.6)) ** 6; S.world.style.scale = 1 + beat * .04;
a.style.opacity = t < T(81.03) ? 1 : 0; pop(a, t, 0, .2); b.style.opacity = t >= T(81.27) ? 1 : 0; pop(b, t, T(81.27), .2); cop(t, .3);''',
     bg='D18', frm=1.1, to=1.18, ox=55, oy=58)
page('s31-choice', 82.16, END, '''
const dim = h('div', 'blk', S.ui); dim.style.background = 'rgba(0,0,0,.5)';
const q = h('div', 'stamp', S.ui, 'WHAT WOULD<br><em>YOU</em> DO?'); q.style.top = '560px'; q.style.fontSize = '150px';
const row = h('div', 'abs', S.ui); row.style.cssText += 'left:90px;right:90px;top:930px;display:flex;gap:40px';
const bt = [['DRIVE', '#3ccf91'], ['STOP', '#ff3b5c']].map(([s, c]) => { const b = h('div', 'btn', row, s); b.style.background = c; return b; });
const cm = h('div', 'chip', S.ui, 'COMMENT <b>DRIVE</b> OR <b>STOP</b> 👇'); cm.style.left = '540px'; cm.style.top = '1210px';
''', '''cop(t, .3); pop(q, t, 0, .3);
bt.forEach((e, i) => { const at = i ? T(83.77) : T(82.88); const p = seg(t, at, .3); e.style.opacity = p > 0 ? 1 : 0; e.style.transform = `scale(${p > 0 ? back(p) : .5})`; });
pop(cm, t, T(84.4), .3); cm.style.opacity = t >= T(84.4) ? 1 : 0;''', bg='D19', frm=1.1, to=1.2, rain_n=90)

for (a, _, e), (b, s, _) in zip(SHOTS, SHOTS[1:]): assert abs(e - s) < 1e-6, (a, b)
json.dump(SHOTS, open('shots.json', 'w'), indent=1)
print(len(SHOTS), 'shots, ends at', SHOTS[-1][2])
