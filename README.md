# AI Film Workflows

Short films made with AI agents, with the full workflow behind each one: the prompts, the costs, what failed, and the edit code.

Follow on X: [@ichsanbuilds](https://x.com/ichsanbuilds). Comment **ANIMATE** on any post to get the workflow.

## Films

| Film | Length | Tutorial | Prompts | Edit code |
|---|---|---|---|---|
| **The Driver**: a 2 AM rideshare, three men, $50,000 and a police badge. Drive or stop? | 86 s, 9:16 | [Read the tutorial](https://ichsanbuilds.github.io/ai-film-workflows/the-driver/) | [`the-driver/prompts`](the-driver/prompts) | [`the-driver/edit`](the-driver/edit) |

## Tools used

| Tool | What it did | Link |
|---|---|---|
| Claude Code | Wrote the script and prompts, drove the image tool, built the edit as code | [claude.com/claude-code](https://claude.com/claude-code) |
| Dreamina | Images (Seedream 4.7) and one video clip (Seedance 2.0 Mini) | [dreamina.capcut.com](https://dreamina.capcut.com) |
| ElevenLabs | Narration, one take with word timestamps | [elevenlabs.io](https://elevenlabs.io) |
| Mixkit | Free sound effects | [mixkit.co/free-sound-effects](https://mixkit.co/free-sound-effects/) |
| OpenFilm | Open-source editor where a film is web pages driven by time | [github.com/openfilm/openfilm](https://github.com/openfilm/openfilm) |

## How a film is made here

1. Write a second-person "what would you do" script for the ear.
2. Lock the look with two style images, then lock each recurring character with one reference image.
3. Generate the scenes with one shared prefix and suffix, check every image, redo the ones that break the story.
4. Make layers that can move: objects cut out from a magenta sheet, variants of the same frame, one AI clip for the key moment.
5. Record the voice in one take and build every animation on the spoken words.
6. Edit in layers, add sound, render at 1080 × 1920 and −14 LUFS.

## What is not in this repo

- Sound effects and music: Mixkit's licence does not allow sharing the files. Links to the sources are in each tutorial.
- The voice recording and the rendered video.
