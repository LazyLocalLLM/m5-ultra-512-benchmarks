# Finding 33. MiniMax H3 video on mlx-serve 26.11.3 and Rapid-MLX 1.1.0, seconds per clip

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: MiniMax H3 makes a short video with sound from a sentence. Two engines on this Mac serve it. mlx-serve runs its author's 8-bit pack, and Rapid-MLX runs the maker's own full-precision weights. I timed each one making the same clips, at the sizes and lengths other people use when they time H3, and checked each clip's frames and size.

**mlx-serve 26.11.3, on its author's 8-bit pack with its 4-step Turbo, made a 5-second MiniMax H3 clip with sound in 34.9 s at 832 by 480, and in 149.4 s at 1344 by 768, H3's native size. Rapid-MLX 1.1.0, on the maker's bf16 weights with its fixed 9-step Turbo LoRA, took 116.6 s and 446.2 s. A 10-second clip at 832 by 480 took 100.7 s and 293.5 s. mlx-serve's own default, 30 steps with its step cache, took 109.3 s, and 471.4 s on one clip. The two engines ran different weights, different Turbo adapters and different step counts, so these gaps are not one engine's speed alone. Mac Studio M5 Ultra 512 GB, one request at a time, middle of the clips, 23 Nov 2026.**

| Engine and setting | 832x480, 5 s | 1344x768, 5 s | 832x480, 10 s |
|---|---|---|---|
| mlx-serve 26.11.3, Turbo, 4 steps | 34.9 | 149.4 | 100.7 |
| mlx-serve 26.11.3, default, 30 steps, step cache on | 109.3 | 471.4 | not run |
| Rapid-MLX 1.1.0, Turbo LoRA merged, 9 steps | 116.6 | 446.2 | 293.5 |

- **Seconds per clip,** from sending the request to the finished clip, as the client saw it. The middle of the timed clips, warm-ups left out.
- **Clips.** 5 s is 124 frames and 10 s is 243 frames, at 24 fps, asked for exactly from both engines. Every mlx-serve clip came back with that many frames, at that size, at 24 fps, with 32 kHz stereo sound, checked on each clip. Every Rapid-MLX job record shows those frames and that size, completed. I did not open its files for sound this time. Finding 22 did, and found stereo sound.
- **Runs.** 3 clips at 832x480 with Turbo on mlx-serve, 2 for most other cells, 1 for mlx-serve's default at 1344x768. Each cell's range is in the table below.
- **Per second of video.** mlx-serve's Turbo at 832x480 took 34.9 / 5.17 = 6.8 s of work per second of clip. Rapid-MLX took 116.6 / 5.17 = 22.6. 124 frames / 24 fps = 5.17 s.
- **No `mlx-lm` multiple.** `mlx-lm` makes no video, so this page has no baseline.

## Chart

ELI5: Seconds for one clip. A shorter bar is faster.

![Bars of seconds per clip for MiniMax H3 video, lower is faster. At 832 by 480 for 5 seconds, mlx-serve Turbo 4 steps 34.9, mlx-serve default 30 steps 109.3, Rapid-MLX Turbo LoRA 9 steps 116.6. At 1344 by 768 for 5 seconds, 149.4, 471.4 and 446.2. At 832 by 480 for 10 seconds, mlx-serve Turbo 100.7 and Rapid-MLX 293.5, with no mlx-serve default bar.](chart_seconds.png)

## How others time H3, and what I matched

ELI5: Before the run I read how others time H3 and matched their sizes and lengths where I could.

- **LMSYS** timed H3 on 8 H200s at 1344x768, 124 frames for 5 s, and 10-second clips, as the median over three prompts of generation time, with server start, warm-up, polling and download left out. [Their post](https://www.lmsys.org/blog/2026-08-27-minimax-h3-h200).
- **[h3.c](https://github.com/antirez/h3.c)** names 1344x768 the largest canvas and takes frames on a 5 + 17n grid, which 124 and 243 both fit.
- **Matched.** The native 1344x768 size, 5-second and 10-second clips, frames asked exactly, warm-ups left out, the middle of the clips.
- **Not matched.**
  - **Steps.** LMSYS ran H3's 50. Rapid-MLX fixes 9 with its Turbo LoRA, and mlx-serve's are 4 with Turbo and 30 by default. No cell here runs 50.
  - **Prompts.** One prompt and one seed, not three prompts. With Turbo the work is fixed by the size and the steps. mlx-serve's default step cache skips steps by how the clip changes, so there one prompt is one sample.
  - **The finish line.** mlx-serve's clock stops when the raw frames and sound arrive. Rapid-MLX's stops when an encoded MP4 file is ready. The next section gives each engine's own clock.

## Where the time goes

ELI5: mlx-serve's log times each part of every clip, the denoising steps, then turning them into video frames and sound. Rapid-MLX records when each job started and finished.

mlx-serve, by its own log, middle of the timed clips, seconds.

| Setting | Clip, client | Sampling | Video decode | Sound decode | Per step |
|---|---|---|---|---|---|
| Turbo, 832x480, 5 s | 34.9 | 24.5 | 9.6 | 0.4 | 6.1 |
| Turbo, 1344x768, 5 s | 149.4 | 122.0 | 26.2 | 0.4 | 30.5 |
| Turbo, 832x480, 10 s | 100.7 | 77.0 | 22.2 | 0.8 | 19.3 |
| Default, 832x480, 5 s | 109.3 | 97.1 | 11.3 | 0.4 | 3.2 |
| Default, 1344x768, 5 s, one clip | 471.4 | 443.7 | 26.5 | 0.4 | 14.8 |

- **From its log lines,** "sampling done in", "video decoded in" and "audio decoded", one line a clip in `engine_log_clock.csv`. The step times it logs add up to its sampling time within about 0.1 s.
- **The rest of the client's time** is reading the prompt, about 0.15 s, and sending the raw frames and sound to the client, about 0.2 to 1 s.
- **The default's per-step figure is its sampling time over 30 steps,** cached steps included, which take almost no time.
- **Rapid-MLX's own job span** matched the client's clock within 2 s on every clip, 114.5 s, 446.0 s and 293.0 s in the middle. That span includes encoding the MP4. So waiting for the job and downloading the file cost little, and Rapid-MLX's times include building a finished file that mlx-serve's do not.
- **Some cells slowed clip by clip within a start.** mlx-serve's default at 832x480 sampled in 85.5 s on its warm-up, then 94.0 and 100.1. The 8-step Turbo cell sampled in 50.2, 52.3 and 54.7. The 4-step Turbo cell held at 24.4 to 24.5. I did not find the cause.

## The same number of denoising passes

ELI5: Rapid-MLX's 9 steps give its Turbo LoRA 8 denoising passes, by its own source. So I also ran mlx-serve's Turbo at 8 steps.

- **mlx-serve at 8 Turbo steps,** 832x480, 5 s, took 63.9 s (61.3 to 66.6), against Rapid-MLX's 116.6 s.
- **The weights still differ.** mlx-serve's pack quantizes the DiT and text encoder to 8 bits and keeps both decoders as released. Rapid-MLX runs the maker's bf16 weights. The pack's own README says the 8 bits buy room, not speed, since the work is compute bound. I did not test that.
- **The Turbo adapters differ.** mlx-serve's pack carries larryvrh's 4-step LoRA, and Rapid-MLX merges lightx2v's 8-pass LoRA. Both are adapters for H3, trained separately.

## Two switches in mlx-serve

ELI5: mlx-serve turns on two speed-ups by itself on this Mac. I turned each one off to see what it gives.

- **The int8 path.** On an M5, mlx-serve runs the DiT's matrix work in 8-bit integers by default (`--w8a8`, by its source). I timed it on, off, then on again, 3 clips each, at 832x480 with Turbo. With it off a clip took 52.3 s (48.9 to 55.3), and with it on 34.9 and 35.8 s. Clip by clip, off took 1.40, 1.48 and 1.53 times the mean of the two on starts, a middle of 1.48. Sampling alone took 1.64 times. An earlier off start read 50.5 s. It is lossy but steady. Every clip with it on had one frame hash, across three starts, and every clip with it off had another.
- **The fast recipe.** mlx-serve's default reuses the last step's result when the clip barely changed from the step before (a velocity cache at 0.05), and reuses cached attention outputs between refresh steps (attention broadcast, k=2). With it off, one default 30-step clip at 832x480 took 213.2 s, against the middle of two with it on, 109.3 s. 213.2 / 109.3 = 1.95, one clip against two. With it on the cache reused 14 of 30 steps. Turbo turns it off by itself (mlx-serve's `geometry.zig`).

## Two more settings

ELI5: Two settings others have published, one for this pack and one for this Mac model.

- **The pack author's own test,** 960x544, 39 frames. 4 Turbo steps took 13.0 s and 16 steps without Turbo took 23.1 s, the 16-step run with the fast recipe on, reusing 6 of 16 steps. 23.1 / 13.0 = 1.78, about the ratio the pack's README gives on another Mac.
- **960x544, 5 s, 6 Turbo steps,** a setting posted for an M5 Ultra. 75.8 s (75.7 to 75.8).

## Every cell

ELI5: Every setting, its range and the number of clips.

| Engine and setting | Size | Frames | Steps | Seconds | Range | Clips |
|---|---|---|---|---|---|---|
| mlx-serve, Turbo | 832x480 | 124 | 4 | 34.9 | 34.9 to 34.9 | 3 |
| mlx-serve, Turbo | 832x480 | 124 | 8 | 63.9 | 61.3 to 66.6 | 3 |
| mlx-serve, Turbo | 1344x768 | 124 | 4 | 149.4 | 149.4 to 149.4 | 2 |
| mlx-serve, Turbo | 832x480 | 243 | 4 | 100.7 | 100.3 to 101.1 | 2 |
| mlx-serve, Turbo | 960x544 | 39 | 4 | 13.0 | 13.0 to 13.1 | 2 |
| mlx-serve, Turbo | 960x544 | 124 | 6 | 75.8 | 75.7 to 75.8 | 2 |
| mlx-serve, fast recipe | 960x544 | 39 | 16 | 23.1 | 23.0 to 23.2 | 2 |
| mlx-serve, default | 832x480 | 124 | 30 | 109.3 | 106.3 to 112.2 | 2 |
| mlx-serve, default | 1344x768 | 124 | 30 | 471.4 | one clip | 1 |
| mlx-serve, fast recipe off | 832x480 | 124 | 30 | 213.2 | one clip | 1 |
| mlx-serve `--no-w8a8`, Turbo | 832x480 | 124 | 4 | 52.3 | 48.9 to 55.3 | 3 |
| The same, an earlier start | 832x480 | 124 | 4 | 50.5 | 47.4 to 54.6 | 3 |
| mlx-serve, Turbo, on starts beside it | 832x480 | 124 | 4 | 34.9 and 35.8 | 34.9 to 37.3 | 3 and 3 |
| Rapid-MLX, Turbo LoRA | 832x480 | 124 | 9 | 116.6 | 114.5 to 118.6 | 2 |
| Rapid-MLX, Turbo LoRA | 1344x768 | 124 | 9 | 446.2 | 446.1 to 446.2 | 2 |
| Rapid-MLX, Turbo LoRA | 832x480 | 243 | 9 | 293.5 | 293.5 to 293.5 | 2 |

- **Rapid-MLX's 832x480 clip matches its own run of 22 Nov,** 116.5 s, in [finding 22](../22_image_video_rapidmlx_110).
- **mlx-serve gave the same clip every time.** Within each cell, the frames and the sound hashed the same on every clip, warm-up included. Rapid-MLX's MP4 files differed in their bytes. I kept no clip to decode, so I cannot say whether its frames differ.

## The setup

ELI5: Both engines at their newest stable release, run as their docs show, one fresh server for each setting group.

- **mlx-serve** 26.11.3, the newest stable release, checked on 23 Nov 2026 at 18:20 SGT, installed with Homebrew, mlx 0.32.5. `mlx-serve --model <pack> --serve --host 127.0.0.1 --port <port>`, and the same with `--no-w8a8` for that one start. Requests to its video endpoint with the size, frames and seed, `"turbo": true` for Turbo, a step count where one is shown, and `"fast": false` for the one clip with the fast recipe off.
- **Weights for mlx-serve.** [ddalcu/MiniMax-H3-FL2VA-MLX-Serve-8bit](https://huggingface.co/ddalcu/MiniMax-H3-FL2VA-MLX-Serve-8bit) @ 64314cde, 65.3 GiB, the author's 8-bit conversion of H3's FL2VA checkpoint, every file checked against its SHA-256. Its config lists text-to-video-with-audio as one of its two tasks.
- **Rapid-MLX** 1.1.0, the newest release, `rapid-mlx serve minimax-h3`, downloads off. It merges its Turbo LoRA at load and fixes 9 steps.
- **Weights for Rapid-MLX.** [MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) @ b3c7290e, the 63 files its H3 runtime reads, 134.2 GiB, bf16, and [lightx2v/Minimax-h3-Turbo](https://huggingface.co/lightx2v/Minimax-h3-Turbo) @ 30f485ed, as in finding 22.
- **Prompt.** One sentence about a sailing boat at sunrise, the same for both engines, seed 42.

| Run id | Engine | Cells | Started, SGT, 23 Nov 2026 |
|---|---|---|---|
| `ae6b33d8a969` | mlx-serve 26.11.3 | Turbo cells and the 960x544 cells | 18:34 |
| `e4582a4edf7f` | mlx-serve 26.11.3, `--no-w8a8` | Turbo, 832x480 | 18:52 |
| `d298c3c6cf24` | Rapid-MLX 1.1.0 | All three sizes | 18:56 |
| `1464ef87f364` | mlx-serve 26.11.3 | Default, and the fast recipe off | 19:27 |
| `12db1cae53e2` | mlx-serve 26.11.3 | Int8 check, on | 19:51 |
| `05bf4b57cfe8` | mlx-serve 26.11.3, `--no-w8a8` | Int8 check, off | 19:54 |
| `ad2206686019` | mlx-serve 26.11.3 | Int8 check, on again | 19:58 |

## Licence

- **MiniMax H3's licence** covers use worldwide except the European Union, the United Kingdom, the Republic of Korea and the United States, and limits where outputs may be shown. The Mac is in Singapore. I publish timings only, no clip and no frame. My clients saved no clip from these runs. Rapid-MLX's server builds an MP4 for download, and I did not check where it keeps it.

## Check it yourself

ELI5: Every clip's timing is in two files, one from the clients and one from mlx-serve's log.

- **`gen_video_rows.csv`.** 45 rows, one a clip, warm-ups included and marked, with the client's seconds, Rapid-MLX's own job span, the frames and size returned, and short hashes of the frames and sound. Its `sampling_seconds` for mlx-serve is the client's estimate from step events, which reads low when the step cache skips steps. Its `peak_rss_gib` is the server's process size only.
- **`engine_log_clock.csv`.** 38 rows, one an mlx-serve clip in all six of its starts, with mlx-serve's own logged sampling, step sum, video decode and sound decode in ms, and the steps its cache reused. The tables above use these.

## What I did not verify

- **H3's 50-step reference schedule.** Neither engine ran it here.
- **Clip quality.** I did not watch or grade the clips.
- **Memory.** The process sizes in the CSV leave out GPU memory on this Mac, so I quote none.
- **More prompts.** One prompt and seed throughout.
- **Not in this run.** MiniMax-H3-Image, mlx-serve's 4-bit H3 pack, HyperFlow H3 Flash (it needs keyframes), h3.c and pi-H3.

## Credit

- **mlx-serve and its H3 pack.** [mlx-serve](https://github.com/ddalcu/mlx-serve) by [@ddalcu](https://x.com/ddalcu).
- **Rapid-MLX.** [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX), [@rapidmlx](https://x.com/rapidmlx).
- **Model.** MiniMax H3 by MiniMax. Turbo LoRAs by larryvrh and lightx2v.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
