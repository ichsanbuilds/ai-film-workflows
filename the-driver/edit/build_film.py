#!/usr/bin/env python3
"""Writes film.html for "The Driver" from shots.json + the sound list below."""
import json, subprocess
END = 86.6
shots = json.load(open('shots.json'))
vis = '\n'.join(f'  <iframe src="shots/{n}.html" at="{a}"></iframe>' for n, a, e in shots)
def dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'assets/' + f], capture_output=True, text=True).stdout)
def loop(src, a, b, vol, skip=0.0):
    L0 = dur(src) - skip - 0.05; out, t = [], a
    while t < b - 0.05:
        L = min(L0, b - t); out.append(f'  <audio src="assets/{src}#t={skip:.2f},{skip + L:.2f}" at="{t:.2f}" volume="{vol}"></audio>'); t += L
    return out
rainl = loop('fx/rain-in-car.mp3', 0, END, 0.35)
music = loop('fx/dark-held-tension-03cc9c.mp3', 0.6, END, 0.36, skip=1.0)
# sirens: far -> louder -> one block
sir = [f'  <audio src="assets/fx/siren-us.mp3#t=0,12.1" at="23.4" volume="0.12"></audio>',
       f'  <audio src="assets/fx/siren-us.mp3#t=0,12.1" at="46.0" volume="0.3"></audio>',
       f'  <audio src="assets/fx/siren-us.mp3#t=0,10.0" at="66.5" volume="0.22"></audio>',
       f'  <audio src="assets/fx/siren-arrival.mp3#t=0,{END - 77.9:.2f}" at="77.9" volume="0.45"></audio>']
POP, WH1, WH2, BOOM, HIT = 'sfx/sfx_009.mp3', 'sfx/sfx_006.mp3', 'sfx/sfx_007.mp3', 'sfx/sfx_004.mp3', 'sfx/sfx_005.mp3'
sfx = [('fx/car-door.mp3', 8.5, .5), ('fx/car-door.mp3', 9.1, .45), (WH1, 20.16, .45), (BOOM, 23.57, .5), (WH1, 27.38, .35),
       ('fx/cash-register-tally-5529ea.mp3', 31.06, .35), ('fx/watch-haptic-buzz-5bfa59.mp3', 50.52, .8), ('fx/watch-haptic-buzz-5bfa59.mp3', 51.2, .8),
       ('fx/liquid-metal-swish-18ebfa.mp3', 56.9, .5), ('fx/heartbeat-fast.mp3#t=0,5.4', 57.0, .55),
       (BOOM, 65.11, .6), ('fx/paper-stamp-thump-e00c70.mp3', 65.11, .7), (WH1, 72.24, .4), (WH1, 76.38, .4),
       ('fx/heartbeat-fast.mp3#t=0,6.3', 80.2, .6)]
sfx += [(HIT, round(33.72 + i * .55, 2), .35) for i in range(5)]                      # five bricks (clip rhythm)
sfx += [(BOOM, 10.6, .55), (WH2, 10.02, .4), (WH1, 17.67, .45), (WH2, 31.06, .35), (WH1, 49.95, .4), (WH2, 53.5, .45), (WH1, 62.29, .45), (WH1, 66.5, .35), (WH2, 77.97, .4)]
sfx += [(POP, t, .35) for t in (2.83, 4.27, 8.42, 12.71, 21.45, 31.06, 40.0, 42.11, 44.07, 51.49, 54.8, 66.69, 67.7, 70.51, 72.3, 74.05, 78.9, 80.2, 81.27, 82.88, 83.77, 84.4)]
sfx += [('fx/paper-stamp-thump-e00c70.mp3', t, .55) for t in (36.47, 23.6)]
def d(f):
    if '#t=' in f: a, b = map(float, f.split('#t=')[1].split(',')); return b - a
    return dur(f)
for f, a, v in sfx: assert a + d(f) <= END + 0.01, (f, a)
tracks = []
for f, a, v in sorted(sfx, key=lambda x: x[1]):
    for tr in tracks:
        lf, la, _ = tr[-1]
        if la + d(lf) <= a: tr.append((f, a, v)); break
    else: tracks.append([(f, a, v)])
sx = '\n'.join('<section>\n' + '\n'.join(f'  <audio src="assets/{f}" at="{a}" volume="{v}"></audio>' for f, a, v in tr) + '\n</section>' for tr in tracks)
sec = lambda xs: '<section>\n' + '\n'.join(xs) + '\n</section>'
html = f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920">
<style>@keyframes cpush {{ from {{ scale: 1 }} to {{ scale: 1.06 }} }}</style>
</head>
<body>
<section>
  <iframe src="captions.html#t=0,{END}"></iframe>
</section>
<section>
  <iframe src="hud.html#t=0,{END}"></iframe>
</section>
<section>
{vis}
</section>
<section>
  <video src="assets/klip/cash.mp4#t=0,3.93" at="33.16" style="object-fit: cover; animation: cpush 4s linear both"></video>
</section>
<section>
  <audio src="assets/vo.mp3"></audio>
</section>
{sec(music)}
{sec(rainl)}
{chr(10).join(sec([s]) for s in sir)}
{sx}
</body>
</html>
'''
open('film.html', 'w').write(html)
print(len(shots), 'shots,', len(tracks), 'sfx tracks')
