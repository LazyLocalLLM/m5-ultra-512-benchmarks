# Finding 22. Qwen-Image 2.1 and MiniMax H3 video on Rapid-MLX 1.1.0, time per picture and per clip

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: My first pictures and video on this Mac. Rapid-MLX 1.1.0 serves image and video models through an OpenAI-style API, so I timed each request from send to finished file, with every setting fixed and one seed. Qwen-Image 2.1 makes pictures. MiniMax H3 makes video with sound. Both ran on the makers' weights, not quantized.

**Rapid-MLX 1.1.0 made a 1024 by 1024 Qwen-Image 2.1 picture in 17.1 s at 20 steps, the same on two starts and ten pictures. The Turbo model made one in 8.7 s at 8 steps. MiniMax H3, its weights not quantized, made a 5-second clip, 124 frames at 24 fps, in 116.5 s at 832 by 480 and 388.9 s at 1280 by 720. Mac Studio M5 Ultra 512 GB, one request at a time, middle of the runs, 22 Nov 2026.**

Corrected on 23 Nov 2026 at 05:19 SGT. The 20-step pictures sent guidance 3.5 with no negative prompt. Rapid-MLX runs Qwen-Image 2.1 through mflux 0.23.0, whose loop runs the second, unconditioned pass only when guidance is above 1 and a negative prompt is sent. So these pictures ran one pass a step, and the guidance had no effect. [Finding 25](../25_qwen_image_mlxserve_26113) measured it. A 1024 by 1024 picture sent guidance 1.0 had the same file hash as one sent 3.5, at the same 0.72 s a step. The 2048 pictures rest on the code, as I checked the hash at 1024 only. With a negative prompt of one space, guidance 3.5 took 1.53 s a step and 33.4 s a picture. The times on this page stand. Only the label of the work changed.

| Model | Size | Steps | Seconds | Runs | Range |
|---|---|---|---|---|---|
| Qwen-Image 2.1, bf16 | 1024 by 1024 | 20, guidance 3.5 sent, one pass a step | 17.1 | 10 on two starts | 17.1 to 17.4 |
| Qwen-Image 2.1, bf16 | 1024 by 1024 | 40, the engine's default | 34.1 | 10 on two starts | 31.8 to 35.3 |
| Qwen-Image 2.1, bf16 | 2048 by 2048 | 20, guidance 3.5 sent, one pass a step | 105.4 | 6 on two starts | 104.8 to 108.5 |
| Qwen-Image 2.1 Turbo, bf16 | 1024 by 1024 | 8, the engine's default | 8.7 | 5 | 8.7 to 8.7 |
| MiniMax H3, bf16, 5 s clip | 832 by 480 | 9, Turbo LoRA | 116.5 | 3 | 112.6 to 118.7 |
| MiniMax H3, bf16, 5 s clip | 768 by 448 | 9, Turbo LoRA | 92.5 | 3 | 92.5 to 94.5 |
| MiniMax H3, bf16, 5 s clip | 1280 by 720 | 9, Turbo LoRA | 388.9 | 2 | 387.9 to 389.9 |

- **Seconds** run from sending the request to the finished file, picture or clip, as the client saw it. The middle of the runs, warm-ups left out.
- **Two starts for Qwen-Image 2.1.** A fresh server at 18:29 and at 19:30 SGT. Each start gave 17.1 at 20 steps.
- **Per second of video.** 116.5 s for 5.17 s of clip is 22.5 s of work per second of video at 832 by 480. 124 frames / 24 fps = 5.17 s. At 1280 by 720 it is 388.9 / 5.17 = 75.2.
- **The 20-step setting is Rapid-MLX's own image speed test,** 1024 by 1024, 20 steps, guidance 3.5, seed 12648430. I sent no negative prompt, and its test case lists none.
- **H3's 9 steps are the engine's own and fixed.** Its source sets 9 and notes that 9 gives the Turbo LoRA's 8 denoising passes.

## Chart

ELI5: Seconds for one picture or one clip. A shorter bar is faster.

![Bars of seconds per output on Rapid-MLX 1.1.0, lower is faster. Qwen-Image 2.1 Turbo 1024 square, 8 steps, 8.7. Qwen-Image 2.1 1024 square, 20 steps, 17.1. The same at 40 steps, 34.1. Qwen-Image 2.1 2048 square, 20 steps, 105.4. MiniMax H3 5-second clip at 768 by 448, 92.5. At 832 by 480, 116.5. At 1280 by 720, 388.9.](chart_seconds.png)

## Qwen-Image 2.1, step by step

ELI5: The engine logs how long each picture's denoise steps took, apart from reading the prompt and writing the file. Its totals match the client's within 0.1 s.

From Rapid-MLX's own log, both starts.

| Setting | Total per picture | Denoise | Per step |
|---|---|---|---|
| 1024 square, 20 steps | 17.1 s | 14.4 s | 0.72 s |
| 1024 square, 40 steps | 31.8 to 35.3 s | 29.1 to 32.5 s | 0.73 rising to 0.81 s |
| 2048 square, 20 steps | 104.7 to 108.4 s | 93.4 to 96.9 s | 4.67 to 4.84 s |
| Turbo, 1024 square, 8 steps | 8.7 s | 5.8 s | 0.73 s |

- **About 2.7 to 2.9 s of each 1024 picture is outside the steps**, reading the prompt and decoding the picture. 17.1 − 14.4 = 2.7 at 20 steps. 8.7 − 5.8 = 2.9 on Turbo.
- **The 40-step pictures slowed one by one, on both starts.** Each step took 0.73 s on the first picture and 0.81 s on the fifth. The 20-step pictures before them held 0.72 s. I did not find why.
- **Four times the pixels took 6.5 to 6.7 times as long per step.** 4.67 / 0.72 = 6.5 and 4.84 / 0.72 = 6.7, at 2048 square against 1024 square.
- **The same seed gave the same picture.** Every timed picture of a setting had the same file hash, on both starts.
- **The first picture of a start took longer.** 20.2 and 19.5 s at 20 steps, against 17.1 after. On Turbo 11.2 against 8.7.

## MiniMax H3, the clips

ELI5: H3 makes a clip with sound from a sentence. Rapid-MLX always merges a Turbo LoRA into it at load and runs 9 steps, which its source says gives the LoRA's 8 denoising passes. I asked for 5 seconds, which H3 makes as 124 frames.

- **Every clip came back complete.** Opened with ffmpeg, each is 5.17 s of H.264 video at 24 fps, 124 frames, with stereo AAC sound at 32 kHz.
- **The first clip took 122.6 s** against 112.6 to 118.7 for the next three at the same size. The server starts in seconds and loads the model on the first request. The files had just been read for a hash check, so they may have been in the file cache. I don't read 6 s as the load time.
- **The same seed and size gave the same clip.** The files differ by a few bytes of the container, but decoded they match. At 832 by 480 the frame hashes and the sound hash were equal across the warm-up and two timed clips, and at 768 by 448 across two clips.
- **More pixels cost more than their share.** 1280 by 720 has 2.31 times the pixels of 832 by 480 and took 3.34 times as long. 921,600 / 399,360 = 2.31. 388.9 / 116.5 = 3.34.
- **Licence.** MiniMax H3's licence covers use worldwide except the European Union, the United Kingdom, the Republic of Korea and the United States, and limits where outputs may be shown. The Mac is in Singapore. I publish timings only, no clip and no frame.

## Reference points

ELI5: My usual baseline is Apple's `mlx-lm`, which makes no pictures or video. So this page has no baseline.

- **Rapid-MLX's picture runtime is built on [mflux](https://github.com/mflux-community/mflux) 0.23.0**, which it installs. I did not run mflux on its own.
- **mlx-serve 26.11.3** on its author's 8-bit packs is in [finding 25](../25_qwen_image_mlxserve_26113), with Rapid-MLX run again beside it.

## The setup

ELI5: One engine, three models, and a fresh server start for each model.

- **Engine.** [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX) 1.1.0, released on PyPI 21 Nov 2026 20:01 SGT, installed with `uv tool install --python 3.12 'rapid-mlx==1.1.0'`. Telemetry off by its own kill switch.
- **Serve command.** Each model by Rapid-MLX's catalog name, with downloads switched off and the network closed.

```bash
rapid-mlx serve qwen-image-2.1-bf16 --host 127.0.0.1 --port 8220 --disable-model-downloads
rapid-mlx serve qwen-image-2.1-turbo --host 127.0.0.1 --port 8220 --disable-model-downloads
rapid-mlx serve minimax-h3 --host 127.0.0.1 --port 8220 --disable-model-downloads
```

- **Weights,** at the exact revisions Rapid-MLX 1.1.0 pins, every file verified against them.
  - [Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) @ 790c9263, 30.9 GiB. Qwen Research licence.
  - [Qwen/Qwen-Image-2.1-Turbo](https://huggingface.co/Qwen/Qwen-Image-2.1-Turbo) @ fc13ba19, 30.2 GiB.
  - [MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) @ b3c7290e, the 63 files Rapid-MLX's H3 runtime reads, 134.2 GiB. MiniMax H3 Community licence.
  - [lightx2v/Minimax-h3-Turbo](https://huggingface.co/lightx2v/Minimax-h3-Turbo) @ 30f485ed, the 8-step Turbo LoRA, 1.3 GiB, which Rapid-MLX merges into H3 at load. Its card names no licence.
- **The cache.** Rapid-MLX loads these from the Hugging Face cache, and for a pinned revision it accepts only real files there. So the bench's cache holds hard links to the verified files.
- **Pictures.** `POST /v1/images/generations`, one picture, `response_format` b64_json. The 20-step blocks sent steps 20 and guidance 3.5, with no negative prompt. The default blocks sent no steps or guidance, and the engine's progress reported 40 steps for Qwen-Image 2.1 and 8 for Turbo.
- **Video.** `POST /v1/videos` with size, 5 seconds and seed 42, then the job polled until complete and the clip downloaded.
- **Seeds.** 12648430 for pictures, 42 for video.
- **Picture prompt.** "A lighthouse on a rocky coast at dusk, waves breaking below, warm light in the windows, a few gulls in a clear sky, photographed with a 35 mm lens".
- **Video prompt.** "A small sailing boat crosses a calm bay at sunrise, gulls circle overhead, gentle waves lap against the hull, the camera slowly follows the boat".

| Run id | Model | Started, SGT, 22 Nov 2026 |
|---|---|---|
| `c4b43c95b3a1` | Qwen-Image 2.1 | 18:29 |
| `795db536a70c` | Qwen-Image 2.1 Turbo | 18:39 |
| `3977cc991112` | MiniMax H3 | 18:40 |
| `fa2a90450acf` | Qwen-Image 2.1, second start | 19:30 |

## How I measured

ELI5: A small client sends one request, waits for the file and writes down the time.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **One request at a time.** Each block began with one warm-up request where marked, then the timed ones.
- **Time** is wall-clock seconds from sending the request to holding the decoded picture or the downloaded clip.
- **Repeats.** 5 pictures a block at 1024, 3 at 2048. 3 clips at the two small sizes and 2 at 1280 by 720, since each takes over 6 minutes.

## Things to know before you compare

ELI5: A picture or clip time is only comparable with one made the same way.

- **Steps, size and precision decide most of the time.** Check all three before comparing.
- **These are the makers' weights, not quantized.** By the files' own headers, Qwen-Image 2.1 and its Turbo store their transformers in bf16. H3 stores its transformer in bf16 with a few 32-bit tensors, its text encoder in bf16 and its VAE in 32-bit. Quantized versions are smaller and may be faster.
- **The Turbo LoRA is always on for H3 in Rapid-MLX.** That is 9 steps, not the model's own schedule.
- **No memory figure.** The memory I read from the process list was too low for Qwen-Image's 30.9 GiB of weights, so I don't trust it and don't publish it.

## Check it yourself

ELI5: Every timed request is in this folder.

- **`gen_rows.csv`.** 43 requests, warm-ups marked, with settings, status, seconds, output size and a short hash of each output file. No picture or clip.

## What I did not verify

- **What the pictures and clips look like.** I did not grade them, and I publish none.
- **Why the 40-step pictures slowed.**
- **Load time** apart from the first request.
- **Memory**, by a method I trust.
- **Quantized versions, mflux on its own, and other engines.**
- **Longer clips and larger sizes.**

## Credit

- **Engine.** [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX) by [@rapidmlx](https://x.com/rapidmlx), with [mflux](https://github.com/mflux-community/mflux) under its picture runtime.
- **Models.** Qwen-Image 2.1 by Qwen. MiniMax H3 by MiniMax. The H3 Turbo LoRA by lightx2v.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
