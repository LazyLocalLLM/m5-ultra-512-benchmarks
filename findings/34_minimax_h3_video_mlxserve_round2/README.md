# Finding 34. MiniMax H3 video on mlx-serve 26.11.3, round two, the 4-bit pack and HyperFlow H3 Flash

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: mlx-serve's author packs MiniMax H3 at two sizes, 8-bit at 65.3 GiB and 4-bit at 38.3 GiB. A smaller pack is often faster on a Mac. This one was not. On an M5, mlx-serve does H3's heavy maths in 8-bit integers whichever pack it loads. With that switched off the two packs still took the same time. I also timed HyperFlow H3 Flash, a 6-step H3 built to start from a first and a last frame.

**mlx-serve 26.11.3 made a 5-second MiniMax H3 clip with sound at 832 by 480 in 35.0 s on its author's 4-bit pack and in 35.1 s on the 8-bit pack, both with 4-step Turbo. At 1344 by 768, H3's native size, they took 136.1 s and 135.1 s, the middle of 4 clips over two starts each. The 4-bit pack is 27.0 GiB smaller, gives a different clip, and was no faster. HyperFlow H3 Flash, given a first and a last frame, took 43.5 s at 832 by 480 with its 6 steps. Mac Studio M5 Ultra 512 GB, one request at a time, middle of the clips, 23 to 24 Nov 2026 SGT.**

| Setting on mlx-serve 26.11.3 | 832x480, 5 s | 1344x768, 5 s | 640x960, 5 s |
|---|---|---|---|
| 8-bit pack, Turbo, 4 steps | 35.1 | 135.1 | not run |
| 4-bit pack, Turbo, 4 steps | 35.0 | 136.1 | not run |
| 8-bit pack, Turbo, int8 path off | 48.9 | not run | not run |
| 4-bit pack, Turbo, int8 path off | 47.8 | not run | not run |
| HyperFlow H3 Flash, 6 steps, first and last frame | 43.5 | 180.4 | 78.0 |

- **Seconds per clip,** from sending the request to the finished clip, as the client saw it. The middle of the timed clips, warm-ups left out.
- **Clips.** 5 s is 124 frames at 24 fps. Every clip came back with the frames asked, at the size asked, at 24 fps, with 32 kHz stereo sound, checked on each clip. One Flash cell asked for 73 frames.
- **Runs.** 2 or 3 timed clips a cell, after one warm-up for each new size. The 1344x768 Turbo figures are the middle of 4 clips over two starts each. The 8-bit figure pools the first and last starts of an 8-bit, 4-bit, 8-bit run. The 4-bit figure pools its 23:49 start and that run's middle start. Each cell's range is in the table under "Every cell".
- **Per second of video.** The 4-bit pack at 832x480 took 35.0 / 5.17 = 6.8 s of work per second of clip. 124 frames / 24 fps = 5.17 s.
- **No `mlx-lm` multiple.** `mlx-lm` makes no video, so this page has no baseline.

## Chart

ELI5: Seconds for one clip. A shorter bar is faster.

![Bars of seconds per 5-second MiniMax H3 clip on mlx-serve 26.11.3, lower is faster, the 8-bit pack against the 4-bit pack. At 832 by 480 with the int8 path on, 35.1 and 35.0. At 1344 by 768 with it on, 135.1 and 136.1. At 832 by 480 with it off, 48.9 and 47.8.](chart_seconds.png)

HyperFlow H3 Flash is a different model, so it is in the tables, not on the chart.

## Why the 4-bit pack is no faster

ELI5: mlx-serve has a switch for its int8 path. I timed both packs with it on, then off, to see what the pack's bits change.

- **With the int8 path on,** mlx-serve's default on an M5, the two packs took 35.1 s and 35.0 s at 832x480. mlx-serve's own log puts sampling at 24.5 s on both.
- **With it off** (`--no-w8a8`), the 8-bit pack took 48.9 s (47.9 to 49.6) and the 4-bit pack 47.8 s (47.8 to 48.9). The ranges overlap, so the bits did not change the speed here either.
- **What the int8 path gives.** 48.9 / 35.1 = 1.39 times on the 8-bit pack. 47.8 / 35.0 = 1.37 times on the 4-bit pack. Sampling alone went from 38.3 s to 24.5 s on the 8-bit pack, 38.3 / 24.5 = 1.56 times. [Finding 33](../33_minimax_h3_video_mlxserve_rapidmlx) measured 1.48 times on 23 Nov, with a wider spread off.
- **Its log says the same.** Every start with the int8 path on logged "[w8a8] engaged", and both starts with it off logged none.
- **At 832x480 the night held steady.** The 8-bit pack's 23:46 start took 35.1 s and its 00:30 start 34.9 s.
- **At 1344x768,** the two 8-bit starts took 132.0 s and 138.2 s, and the two 4-bit starts 135.5 s and 137.8 s. Each 4-bit start sits inside the 8-bit span, so the packs cannot be told apart at that size either. I ran them 8-bit, 4-bit, 8-bit, one after another, for this. Inside that run alone the 4-bit start took 137.8 s, between the 8-bit starts.
- **Clips slowed within each start at 1344x768.** By mlx-serve's log, sampling took 103 to 107 s on each warm-up and 106 to 114 s on the timed clips after it. I did not find the cause.
- **The clips differ.** Each pack gave one frame hash on every clip, at each size, and the two packs' hashes differ. So the int8 path does not erase the 4-bit pack's rounding. I did not judge which looks better.

## HyperFlow H3 Flash

ELI5: Flash is Video Rebirth's few-step version of H3, packed for mlx-serve by hancheng-ai. Its release notes say to give it a first and a last frame. I made two plain test pictures for those frames, as mlx-serve's own test does, and also tried it with text alone.

- **First and last frame, 6 steps,** its default. 43.5 s at 832x480, 180.4 s at 1344x768.
- **The size its card names,** 640x960. 38.2 s for 73 frames and 78.0 s for 124 frames.
- **Its other step counts.** 4 steps took 33.8 s and 8 steps 55.3 s, at 832x480 with both frames.
- **Text alone, 6 steps.** 41.2 s at 832x480. It worked, and its config lists text-to-video. The release notes do not mention it, so it is labelled as such.
- **What the frames cost.** mlx-serve's log puts encoding the two frames at 1.4 s at 832x480 (1.3 to 1.7 s, 8 clips), 1.6 s at 640x960 and 3.0 s at 1344x768. 43.5 − 41.2 = 2.3 s in all at 832x480. Sampling took 1.5 s longer with the frames, 31.6 s against 30.1 s.
- **Per step,** by mlx-serve's log at 832x480, Flash sampled in 31.6 / 6 = 5.3 s a step, and the 4-bit pack's Turbo in 24.5 / 4 = 6.1 s. I did not find why a Flash step costs less.
- **Its speed switches.** Its log shows the step cache and attention broadcast off on every clip ("step-cache 0.000, attn-broadcast k=0"), and "6 steps on its trained grid". The int8 path engaged here too.
- **The pack.** A tier C pack, by a named contributor whose pull request added Flash to mlx-serve 26.11.3. No pack from Video Rebirth or mlx-serve's author exists. It ships H3's 4-bit text encoder although it is named 8-bit.
- **Not the same model as H3 with Turbo.** Flash has its own distilled weights. Turbo is a LoRA on H3's own. So Flash's times and the packs' times are two models, not two settings.

## Where the time goes

ELI5: mlx-serve's log times each part of every clip, the denoising steps, then turning them into video frames and sound.

mlx-serve, by its own log, middle of the timed clips, seconds.

| Setting | Clip, client | Sampling | Video decode | Sound decode | Per step |
|---|---|---|---|---|---|
| 8-bit pack, Turbo, 832x480 | 35.1 | 24.5 | 9.7 | 0.4 | 6.1 |
| 4-bit pack, Turbo, 832x480 | 35.0 | 24.5 | 9.7 | 0.4 | 6.1 |
| 8-bit pack, Turbo, 1344x768, two starts | 135.1 | 109.3 | 24.4 | 0.4 | 27.3 |
| 4-bit pack, Turbo, 1344x768, two starts | 136.1 | 110.3 | 24.5 | 0.4 | 27.6 |
| 8-bit pack, int8 off, 832x480 | 48.9 | 38.3 | 9.7 | 0.4 | 9.6 |
| 4-bit pack, int8 off, 832x480 | 47.8 | 37.3 | 9.7 | 0.4 | 9.3 |
| Flash, 6 steps, frames, 832x480 | 43.5 | 31.6 | 9.7 | 0.4 | 5.3 |
| Flash, 6 steps, frames, 1344x768 | 180.4 | 152.4 | 23.8 | 0.4 | 25.4 |
| Flash, 6 steps, frames, 640x960, 124 frames | 78.0 | 62.9 | 12.6 | 0.4 | 10.5 |
| Flash, 6 steps, text alone, 832x480 | 41.2 | 30.1 | 10.2 | 0.4 | 5.0 |

- **From its log lines,** "sampling done in", "video decoded in" and "audio decoded", one line a clip in `engine_log_clock.csv`.
- **The rest of the client's time** is reading the prompt, encoding Flash's frames, and sending the raw frames and sound to the client.

## Every cell

ELI5: Every setting, its range and the number of clips.

| Setting | Size | Frames | Steps | Seconds | Range | Clips |
|---|---|---|---|---|---|---|
| 8-bit pack, Turbo | 832x480 | 124 | 4 | 35.1 | 35.1 to 35.1 | 3 |
| 4-bit pack, Turbo | 832x480 | 124 | 4 | 35.0 | 35.0 to 35.0 | 3 |
| 4-bit pack, Turbo | 1344x768 | 124 | 4 | 135.5 | 135.1 to 135.9 | 2 |
| 4-bit pack, int8 off | 832x480 | 124 | 4 | 47.8 | 47.8 to 48.9 | 3 |
| 8-bit pack, int8 off | 832x480 | 124 | 4 | 48.9 | 47.9 to 49.6 | 3 |
| Flash, both frames | 832x480 | 124 | 6 | 43.5 | 43.5 to 43.7 | 3 |
| Flash, both frames | 1344x768 | 124 | 6 | 180.4 | 179.5 to 181.2 | 2 |
| Flash, both frames | 640x960 | 73 | 6 | 38.2 | 38.2 to 38.4 | 3 |
| Flash, both frames | 640x960 | 124 | 6 | 78.0 | 77.8 to 78.6 | 3 |
| Flash, both frames | 832x480 | 124 | 4 | 33.8 | 33.7 to 33.8 | 2 |
| Flash, both frames | 832x480 | 124 | 8 | 55.3 | 55.2 to 55.3 | 2 |
| Flash, text alone | 832x480 | 124 | 6 | 41.2 | 41.1 to 41.2 | 2 |
| 8-bit pack, Turbo, again | 832x480 | 124 | 4 | 34.9 | 34.9 to 34.9 | 3 |
| 8-bit pack, Turbo, A/B/A first | 1344x768 | 124 | 4 | 132.0 | 130.8 to 133.1 | 2 |
| 4-bit pack, Turbo, A/B/A middle | 1344x768 | 124 | 4 | 137.8 | 136.2 to 139.4 | 2 |
| 8-bit pack, Turbo, A/B/A last | 1344x768 | 124 | 4 | 138.2 | 137.1 to 139.3 | 2 |

- **mlx-serve gave the same clip every time.** Within each cell, the frames and the sound hashed the same on every clip, warm-up included.
- **The 8-bit pack matches finding 33 at 832x480.** 35.1 s and 34.9 s here, 34.9 s on 23 Nov.
- **Not at 1344x768.** Finding 33's 1344x768 Turbo clip is the same clip, with the same frame hash, `b4184819929e1cbf`. It took 149.4 s on 23 Nov, and 132.0 s and 138.2 s in the two starts here. 149.4 / 135.1 = 1.11. Its sampling took 122.0 s by mlx-serve's log, against 109.3 s here. I did not find the cause. Finding 33 now carries a note.

## The setup

ELI5: mlx-serve at its newest stable release, run as its docs show, one fresh server for each pack and switch.

- **mlx-serve** 26.11.3, the newest stable release, checked on 23 Nov 2026 at 18:20 SGT, installed with Homebrew, mlx 0.32.5. `mlx-serve --model <pack> --serve --host 127.0.0.1 --port <port>`, and the same with `--no-w8a8` for the int8-off starts. Requests to its video endpoint with the size, frames and seed 42, `"turbo": true` for Turbo, and a step count for Flash's 4 and 8.
- **Flash's frames.** Two plain pictures at each clip's size, a red pattern first and a blue pattern last, sent as `first_frame_image` and `last_frame_image`. Their short hashes are in the rows.
- **Prompt.** One sentence about a sailing boat at sunrise, the same as finding 33, seed 42.

| Pack | Hugging Face | Revision | Size |
|---|---|---|---|
| 8-bit H3, the mlx-serve author's | [ddalcu/MiniMax-H3-FL2VA-MLX-Serve-8bit](https://huggingface.co/ddalcu/MiniMax-H3-FL2VA-MLX-Serve-8bit) | 64314cde | 65.3 GiB |
| 4-bit H3, the mlx-serve author's | [ddalcu/MiniMax-H3-FL2VA-MLX-Serve-4bit](https://huggingface.co/ddalcu/MiniMax-H3-FL2VA-MLX-Serve-4bit) | 9c927357 | 38.3 GiB |
| HyperFlow H3 Flash, tier C | [hancheng-ai/HyperFlow-H3-Flash-FL2VA-MLX-Serve-8bit](https://huggingface.co/hancheng-ai/HyperFlow-H3-Flash-FL2VA-MLX-Serve-8bit) | f34a0ec4 | 33.9 GiB |

Every file was checked against its SHA-256 before the runs.

| Run id | Server | Cells | Started, SGT |
|---|---|---|---|
| `f1487e052c4a` | 8-bit pack | Turbo, 832x480 | 23 Nov, 23:46 |
| `bb4fb0d0fa4e` | 4-bit pack | Turbo, 832x480 and 1344x768 | 23 Nov, 23:49 |
| `75c429a18ea3` | 4-bit pack, `--no-w8a8` | Turbo, 832x480 | 23 Nov, 23:58 |
| `d05c9e99b36e` | 8-bit pack, `--no-w8a8` | Turbo, 832x480 | 24 Nov, 00:02 |
| `b05c76b7ffa0` | Flash | Every Flash cell | 24 Nov, 00:06 |
| `f964ed8ee075` | 8-bit pack | Turbo, 832x480, again | 24 Nov, 00:30 |
| `d3233f0978b4` | 8-bit pack | Turbo, 1344x768, A/B/A first | 24 Nov, 02:00 |
| `e8b0c3b86c58` | 4-bit pack | Turbo, 1344x768, A/B/A middle | 24 Nov, 02:07 |
| `7acee3371ee8` | 8-bit pack | Turbo, 1344x768, A/B/A last | 24 Nov, 02:14 |

## Licence

- **MiniMax H3's licence** covers use worldwide except the European Union, the United Kingdom, the Republic of Korea and the United States, and limits where outputs may be shown. Flash's card names the same licence. The Mac is in Singapore. I publish timings only, no clip and no frame. My client hashed each clip and kept none.

## Check it yourself

ELI5: Every clip's timing is in two files, one from the client and one from mlx-serve's log.

- **`gen_video_rows.csv`.** 53 rows, one a clip, warm-ups included and marked, with the client's seconds, the frames and size returned, the keyframes sent, and short hashes of the frames and sound. Its `peak_rss_gib` is the server's process size only, which leaves out GPU memory on this Mac.
- **`engine_log_clock.csv`.** 53 rows, one a clip, with mlx-serve's own logged sampling, step sum, video decode and sound decode in ms. The tables above use these.

## What I did not verify

- **Clip quality.** I did not watch or grade the clips, so this page does not say which pack or model looks better.
- **Memory.** The process sizes in the CSV leave out GPU memory on this Mac, so I quote none.
- **More prompts.** One prompt and seed throughout.
- **Flash with real pictures.** Its frames here are plain test patterns.
- **pi-H3.** I found no way to run it on a Mac, so it is not here.
- **Next.** h3.c and MiniMax-H3-Image get their own pages.

## Credit

- **mlx-serve and its H3 packs.** [mlx-serve](https://github.com/ddalcu/mlx-serve) by [@ddalcu](https://x.com/ddalcu).
- **HyperFlow H3 Flash.** The model by [Video Rebirth](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash), packed for mlx-serve by hancheng-ai.
- **Model.** MiniMax H3 by MiniMax. The Turbo LoRA by larryvrh.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
