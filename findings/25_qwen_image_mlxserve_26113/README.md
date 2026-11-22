# Finding 25. Qwen-Image 2.1 and its Turbo on mlx-serve 26.11.3, against Rapid-MLX 1.1.0

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: mlx-serve also makes pictures, from its author's own 8-bit packs. I timed it on the pictures of [finding 22](../22_image_video_rapidmlx_110), with the same prompt, size, steps and seed, and ran Rapid-MLX again in the same session. Each step of a picture runs the model once, or twice when guidance is on. The two engines decide that differently, so each pair below does the same passes a step on both.

**With the same passes a step, mlx-serve 26.11.3 made each picture in about half Rapid-MLX 1.1.0's time. A 1024 by 1024 Qwen-Image 2.1 picture at 20 steps took 8.3 s against 17.2 s, and a Turbo picture 3.9 s against 8.7 s. With guidance on in both, two passes a step, it took 18.4 s against 33.4 s. Most of the gap is a lossy int8 path that mlx-serve turns on by itself on this Mac. With it off, the 20-step picture took 15.1 s, and a step took 0.71 s against Rapid-MLX's 0.72 s. mlx-serve read its author's 8-bit packs and Rapid-MLX the makers' bf16 weights. Mac Studio M5 Ultra 512 GB, one picture at a time, 22 and 23 Nov 2026.**

| Picture | Steps | Passes a step | mlx-serve, seconds | Rapid-MLX, seconds | Rapid-MLX over mlx-serve |
|---|---|---|---|---|---|
| Turbo, 1024 by 1024 | 8 | 1 | 3.9 (3.9 to 3.9) | 8.7 (8.7 to 8.7) | 2.2 |
| Qwen-Image 2.1, 1024 by 1024 | 20 | 1 | 8.3 (8.3 to 8.4) | 17.2 (17.2 to 17.2) | 2.1 |
| Qwen-Image 2.1, 1024 by 1024 | 40 | 1 | 16.6 (16.2 to 17.0) | 34.1, finding 22 | 2.1 |
| Qwen-Image 2.1, 2048 by 2048 | 20 | 1 | 53.3 (51.3 to 56.8) | 105.4, finding 22 | 2.0 |
| Qwen-Image 2.1, 1024 by 1024 | 20 | 2 | 18.4 (18.3 to 18.4) | 33.4 (33.2 to 34.2) | 1.8 |
| Qwen-Image 2.1, 1024 by 1024, int8 path off | 20 | 1 | 15.1 (15.0 to 15.2) | 17.2 (17.2 to 17.2) | 1.1 |
| Qwen-Image 2.1, 1024 by 1024, int8 path off, first start | 20 | 2 | 29.5 (28.6 to 31.6) | 33.4 (33.2 to 34.2) | 1.1 |
| Qwen-Image 2.1, 1024 by 1024, int8 path off, second start | 20 | 2 | 32.3 (30.9 to 32.5) | 33.4 (33.2 to 34.2) | 1.0 |

- **Each figure** is the middle of the timed pictures, with the fastest and slowest in brackets. 5 pictures a cell on mlx-serve, except 3 at 2048. 3 on Rapid-MLX in this session. A warm-up picture at each server start is not counted.
- **Rapid-MLX's 40-step and 2048 figures** are finding 22's, 22 Nov 2026, 10 and 6 pictures on two server starts.
- **The multiples** are worked from the figures in the table. 8.7 / 3.9 = 2.2. 17.2 / 8.3 = 2.1. 34.1 / 16.6 = 2.1. 105.4 / 53.3 = 2.0. 33.4 / 18.4 = 1.8. 17.2 / 15.1 = 1.1. 33.4 / 29.5 = 1.1. 33.4 / 32.3 = 1.0.
- **The time** runs from sending the request to receiving the whole picture.

## Chart

ELI5: Seconds per picture on each engine, paired by the work each step does. A shorter bar is faster.

![Bars of seconds per picture, shorter is faster, the same passes a step on both engines, mlx-serve with its int8 path on. Turbo, 1024 square, 8 steps. Rapid-MLX 8.7, mlx-serve 3.9. Qwen-Image 2.1, 1024 square, 20 steps. Rapid-MLX 17.2, mlx-serve 8.3. The same at 40 steps, Rapid-MLX 34.1, mlx-serve 16.6. 2048 square, 20 steps, Rapid-MLX 105.4, mlx-serve 53.3. 1024 square, 20 steps, two passes a step, Rapid-MLX 33.4, mlx-serve 18.4.](chart_seconds.png)

## Passes per step

ELI5: With guidance above 1, a step can run the model twice, once with the prompt and once without, and blend the two. That doubles the work. mlx-serve and Rapid-MLX switch the second pass on under different rules.

- **mlx-serve logs it on every picture.** "two forwards per step" at guidance 3.5 and "one forward per step" at guidance 1.0. Its source at the tag runs the second pass for any guidance other than 1.0, with a blank negative prompt it encodes itself.
- **Rapid-MLX runs pictures through mflux 0.23.0.** Its Qwen-Image 2.1 loop runs the second pass only when guidance is above 1 and a negative prompt is sent. I read this in `mflux/models/qwen21/variants/txt2img/qwen_image_21.py`, line 108.
- **I measured it.** On Rapid-MLX, a 20-step picture sent guidance 1.0 had the same file hash as one sent guidance 3.5 with no negative prompt, `8a44a53388a2c8b2`, at 0.72 s a step by its log. So guidance 3.5 alone changed nothing. With a negative prompt of one space, guidance 3.5 gave another picture and took 1.53 s a step, the middle of 1.50, 1.53 and 1.57.
- **Finding 22 sent guidance 3.5 with no negative prompt,** so its pictures ran one pass a step. That page now says so.
- **Rapid-MLX's 40-step and 2048 rows** sent no negative prompt either, so by the code they ran one pass a step. The 40-step pictures took 0.73 to 0.81 s a step, near the one-pass 0.72 s. The 2048 rows rest on the code alone. I checked the hash at 1024 by 1024 and 20 steps only.
- **Both Turbos ran one pass a step.** mlx-serve's log said so for its default. Rapid-MLX sends its Turbo guidance 1.0.

## A step and the rest

ELI5: A picture's time is its steps plus the work before and after them, reading the prompt and turning the result into a picture.

| Pass and size | mlx-serve, int8 on | mlx-serve, int8 off | Rapid-MLX |
|---|---|---|---|
| One pass, 1024 by 1024 | 0.369 s | 0.708 s | 0.72 s |
| Two passes, 1024 by 1024 | 0.871 s | 1.428 s and 1.571 s, two starts | 1.53 s |
| One pass, 2048 by 2048 | 2.517 s | not run | 4.67 to 4.84 s |

- **Seconds a step.** mlx-serve's from its own progress events, the middle of the timed pictures. Rapid-MLX's from its log.
- **A step costs about the same on both with the int8 path off.** 0.708 s against 0.72 s with one pass. With two, 1.428 s and 1.571 s on two starts against 1.53 s.
- **The rest takes less on mlx-serve.** 8.3 − 20 × 0.369 = 0.9 s outside the steps of the one-pass picture. Its log puts the prompt at 51 to 72 ms and the picture decode at 758 to 845 ms. On Rapid-MLX it is 17.2 − 14.4 = 2.8 s, by its log's total and denoise times.
- **So with the int8 path off, the one-pass gap is mostly outside the steps.** 17.2 − 15.1 = 2.1 s between the pictures, and 2.8 − 0.9 = 1.9 s between the work outside the steps.

## The int8 path

ELI5: On an M5 with 64 GB or more, mlx-serve switches on a path that does the model's big matrix sums in 8-bit integers on the GPU's neural accelerators. It is faster and not exact. `--no-w8a8` turns it off.

- **On by default here.** The log says "[w8a8] engaged: NAX int8 x int8, block-256 rotation".
- **It made the picture 1.6 to 1.8 times faster.** 15.1 / 8.3 = 1.8 with one pass. With two, 29.5 / 18.4 = 1.6 on the first int8-off start and 32.3 / 18.4 = 1.8 on the second.
- **The picture differs with it off.** Another hash, as you'd expect from a different sum. I did not compare the pictures by eye or by any score.
- **With it off, the picture repeated across server starts.** Two starts at guidance 3.5 gave the same hash, `270f3e4f35fc3d4a`.
- **With it off, the steps climbed within each start.** The first start went from 1.38 to 1.53 s a step over its five two-pass pictures. On the second, the two-pass pictures came after six one-pass pictures, and went from 1.50 to 1.58. The second ran with only light reads of my results database beside it, so my push during the first did not cause the climb. I didn't look into why.

## Pictures with no Rapid-MLX partner

ELI5: These ran two passes a step on mlx-serve. I have no Rapid-MLX picture with two passes at these settings, so they stand alone.

| Picture | Steps | mlx-serve, seconds |
|---|---|---|
| Qwen-Image 2.1, 1024 by 1024, guidance 3.5 | 40 | 38.3 (38.2 to 38.6) |
| Qwen-Image 2.1, 2048 by 2048, guidance 3.5 | 20 | 111.8 (111.7 to 112.1) |
| Turbo, 1024 by 1024, guidance 3.5 | 8 | 7.9 (7.9 to 7.9) |

- **3 pictures in each of the first two rows and 5 in the last.**

## The setup

ELI5: One engine at its newest release with its author's packs, a fresh server for each pack, and the same requests as finding 22.

- **Engine.** [mlx-serve](https://github.com/ddalcu/mlx-serve) 26.11.3, the newest stable release, from its Homebrew formula. `mlx-serve --version` prints "mlx-serve 26.11.3 (fast)".
- **Serve command,** one start per pack, bound to this Mac.

```bash
mlx-serve --model <models>/<pack> --serve --host 127.0.0.1 --port 8107 --ctx-size 4096 --max-concurrent 1
```

- **The int8-off starts** added `--no-w8a8`.
- **Packs.** [ddalcu/Qwen-Image-2.1-MLX-Serve-8bit](https://huggingface.co/ddalcu/Qwen-Image-2.1-MLX-Serve-8bit) @ dc21b8d3, 17.1 GiB, and [ddalcu/Qwen-Image-2.1-Turbo-MLX-Serve-8bit](https://huggingface.co/ddalcu/Qwen-Image-2.1-Turbo-MLX-Serve-8bit) @ 214ca346, 16.5 GiB. Every file was verified against the pinned commit, and Hugging Face's scan flagged nothing. The cards say the transformer and text encoder are 8-bit at group 64, with the picture decoder kept dense. mlx-serve's log said "text encoder resident".
- **Requests to mlx-serve.** `POST /v1/images/generations` with the size, steps, `guidance_scale` and seed, streamed so the client could time each step from mlx-serve's progress events. No negative prompt. The prompt is finding 22's.
- **Requests to Rapid-MLX.** 1.1.0 served `qwen-image-2.1-bf16` and `qwen-image-2.1-turbo` as in finding 22, the makers' bf16 weights, with the same requests. The two-pass block added `negative_prompt` set to one space.
- **Seed.** 12648430 on every picture.
- **The models.** [Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) and its Turbo, by Qwen.

| Server start | Engine and pack | Started, SGT, 23 Nov 2026 |
|---|---|---|
| `8c84f2b01fd3` | mlx-serve, Qwen-Image 2.1 8-bit | 02:56 |
| `6e11d078d3a3` | mlx-serve with `--no-w8a8`, Qwen-Image 2.1 8-bit | 03:07 |
| `b1a817c7a6ac` | mlx-serve, Turbo 8-bit | 03:10 |
| `d0d897b66229` | Rapid-MLX, Qwen-Image 2.1 bf16, guidance 3.5 with no negative prompt | 03:12 |
| `25af7924ee28` | Rapid-MLX, Turbo bf16 | 03:14 |
| `3c457af7940c` | Rapid-MLX, Qwen-Image 2.1 bf16, guidance 1.0, then 3.5 with a negative prompt | 04:51 |
| `9c651f675456` | mlx-serve, Qwen-Image 2.1 8-bit, guidance 1.0 | 04:54 |
| `da9491f4623d` | mlx-serve with `--no-w8a8`, Qwen-Image 2.1 8-bit | 04:58 |

## Things to know before you compare

ELI5: Steps, passes a step, size and precision decide most of the time. Check all four before comparing.

- **Different weights.** mlx-serve read 8-bit packs and Rapid-MLX the makers' bf16. mlx-serve's own pack cards say quantizing these models saves memory more than time.
- **The int8 path is mlx-serve's default here, and lossy.** The int8-off rows are the lossless reference.
- **Guidance alone does not tell you the work.** On mlx-serve any guidance but 1.0 doubles the passes. On Rapid-MLX it takes guidance above 1 and a negative prompt.
- **Not fully quiet for the first two starts.** From about 02:56 to 03:09 SGT I built and pushed this repository's previous update on this Mac, light CPU and disk work, while `8c84f2b01fd3` and the start of `6e11d078d3a3` ran. The starts from 04:51 SGT ran with only light reads of my results database beside them.
- **Some blocks climbed.** mlx-serve's 2048 pictures went from 2.41 to 2.70 s a step over three pictures, and its 40-step default from 16.2 to 17.0 s over five. Finding 22 saw Rapid-MLX's 40-step pictures climb too.

## Check it yourself

ELI5: Every timed picture is a row in this folder, with its settings, time and a short hash of the picture.

- **`gen_rows.csv`.** 69 rows, 61 timed pictures and 8 warm-ups, with an engine column and the negative prompt sent. No picture is published.

## What I did not verify

- **Picture quality.** I compared hashes only, not the pictures.
- **MiniMax H3 video on mlx-serve.** It is not in this finding.
- **Rapid-MLX with two passes at 40 steps or at 2048,** and on quantized weights.
- **Memory.** The client's memory figure counts ordinary process memory, not the GPU's, so I give none.
- **Why some blocks slowed** over their pictures.

## Credit

- **Engine and packs.** [mlx-serve](https://github.com/ddalcu/mlx-serve) by [@ddalcu](https://x.com/ddalcu).
- **Other engine.** [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX) by [@rapidmlx](https://x.com/rapidmlx), with [mflux](https://github.com/mflux-community/mflux) under its picture runtime.
- **Models.** Qwen-Image 2.1 and its Turbo by [Qwen](https://x.com/Alibaba_Qwen).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
