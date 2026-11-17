# The Driver: edit code

The edit is an [OpenFilm](https://github.com/openfilm/openfilm) project: every shot is a small web page that draws any moment `t`, and `film.html` places the shots, the clip and the sounds on a timeline.

| File | What it does |
|---|---|
| `build_shots.py` | Writes one HTML page per shot into `shots/`: background plate, cut-out objects, variants swapped on spoken words, light sweeps, cards, the self-drawing map. |
| `build_film.py` | Writes `film.html`: the shot track, the AI clip track, the voice, music, rain, sirens and every sound effect with its time. |
| `captions.html` | Word-by-word captions; the gang's lines in orange. |
| `hud.html` | The small bar at the top: clock, siren distance, cash on the seat. |
| `shared/kit.js`, `shared/kit.css` | Helpers: camera push-in, cut-out placement, rain, glow, pop and rise animations. |
| `vo/words-v1.json` | Start and end time of every spoken word, from ElevenLabs' `with-timestamps` endpoint. Every animation is timed from it. |

## To run it

1. Put your own files in `assets/`: `img/` (scene images and variants as 1080 × 1920 JPG, plus `-b22` blurred copies), `cut/` (transparent PNG cut-outs), `klip/cash.mp4`, `vo.mp3`, `fx/` and `sfx/` (sounds, see the tutorial for sources).
2. `python3 build_shots.py && python3 build_film.py`
3. `npx -y openfilm@latest look` to check frames, then `npx -y openfilm@latest render --loudness=-14`.

Keep any flashing light under 3 flashes per second.
