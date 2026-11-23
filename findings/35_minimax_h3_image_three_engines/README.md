# Finding 35. MiniMax-H3-Image on mlx-serve 26.11.3, Rapid-MLX 1.1.0 and TensorFold 1.3.4, seconds per picture

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: MiniMax-H3-Image draws a picture from a sentence in 6 steps. Three engines on this Mac can run it. I timed each one drawing the same picture at three sizes, with the maker's settings, and checked every picture's size.

**At 2048 by 2048, the model's own canvas, TensorFold 1.3.4 drew a MiniMax-H3-Image picture in 12.9 s, Rapid-MLX 1.1.0 in 13.3 s with 4-bit weights made at load, and mlx-serve 26.11.3 in 13.4 s on its author's 4-bit pack. At 4096 by 4096, mlx-serve took 51.8 s and TensorFold 76.0 s. Rapid-MLX 1.1.0 refused that size. At 1024 and 2048 the three are within 0.5 s of each other, too close to rank. Mac Studio M5 Ultra 512 GB, 6 steps, seed 42, one picture at a time, middle of the timed pictures, 24 Nov 2026 SGT.**

| Engine and weights | 1024x1024 | 2048x2048 | 4096x4096 |
|---|---|---|---|
| TensorFold 1.3.4, the maker's bf16 weights | 13.4 | 12.9 | 76.0 |
| Rapid-MLX 1.1.0, the maker's weights, 4-bit at load | 13.2 | 13.3 | refused |
| Rapid-MLX 1.1.0, the maker's weights, 8-bit at load | 14.8 | 14.6 | refused |
| mlx-serve 26.11.3, the author's 4-bit pack | 13.1 | 13.4 | 51.8 |
| mlx-serve 26.11.3, the author's 8-bit pack | 14.8 | 14.9 | 55.5 |
| mlx-serve 26.11.3, 8-bit pack, int8 path off | not run | 14.4 | not run |

- **Seconds per picture,** from sending the request to the finished PNG, as the client saw it. The middle of the timed pictures, warm-ups left out.
- **Pictures.** Every picture came back as a PNG at the size asked, checked on each one. Within each cell every picture hashed the same.
- **Runs.** 5 timed pictures at 2048x2048, 3 at 1024x1024, 2 at 4096x4096, after a warm-up for each new size. 3 for the int8-off cell. Each cell's range is under "Every cell".
- **Below 2048 the model draws on a 2048x2048 canvas.** Its card says so, and mlx-serve's log shows a 2048x2048 canvas for every 1024x1024 request. That is why 1024x1024 costs about the same as 2048x2048.
- **No `mlx-lm` multiple.** `mlx-lm` makes no pictures, so this page has no baseline.

## Chart

ELI5: Seconds for one picture, each engine at its fastest setting here. A shorter bar is faster.

![Bars of seconds per MiniMax-H3-Image picture, lower is faster. At 1024 by 1024, mlx-serve 26.11.3 with its 4-bit pack 13.1, Rapid-MLX 1.1.0 with 4-bit at load 13.2, TensorFold 1.3.4 with bf16 13.4. At 2048 by 2048, 13.4, 13.3 and 12.9. At 4096 by 4096, mlx-serve 51.8, Rapid-MLX refused the size, TensorFold 76.0.](chart_seconds.png)

## Where the time goes

ELI5: mlx-serve's log and TensorFold's server time each part of every picture. Reading the sentence, loading the drawing model, the 6 steps, and turning the result into a picture.

By each engine's own clock, middle of the timed pictures, seconds.

| Engine and setting | Size | Picture, client | Read the prompt | Load the model | 6 steps | Per step | Decode |
|---|---|---|---|---|---|---|---|
| mlx-serve, 8-bit pack | 2048x2048 | 14.9 | 0.8 | 6.0 | 6.4 | 1.1 | 1.3 |
| mlx-serve, 4-bit pack | 2048x2048 | 13.4 | 0.5 | 4.8 | 6.4 | 1.1 | 1.3 |
| mlx-serve, 8-bit pack, int8 off | 2048x2048 | 14.4 | 0.8 | 0.7 | 11.1 | 1.9 | 1.4 |
| TensorFold, bf16, model kept loaded | 2048x2048 | 12.9 | 0.2 | none | 11.3 | 1.9 | 1.4 |
| mlx-serve, 4-bit pack | 4096x4096 | 51.8 | 0.5 | 4.9 | 40.3 | 6.7 | 4.7 |
| TensorFold, bf16, model kept loaded | 4096x4096 | 76.0 | 0.2 | none | 70.1 | 11.7 | 5.6 |

- **mlx-serve loads the drawing model again for every picture.** Its log has "dit loaded" on each request, 6.0 s on the 8-bit pack and 4.8 s on the 4-bit pack with the int8 path on, and 0.7 s with it off. It also frees the text encoder after each prompt ("encoder released").
- **Its steps were quicker than TensorFold's.** 6.4 s for six at 2048x2048, against 11.3 s. TensorFold keeps its model loaded after the first picture ("reused" in its log), so it skips the load.
- **The int8 path, on images.** mlx-serve turns it on by itself on an M5. It cut the 6 steps from 11.1 s to 6.4 s. The load grew from 0.7 s to 6.0 s. So at 2048x2048 the picture took 14.9 s with it on and 14.4 s with it off. At 4096x4096 the steps are most of the time, and int8-off was not run there.
- **Rapid-MLX gives no breakdown** beyond its progress events, so it has the client's time only.
- **From the logs.** mlx-serve's lines are "prompt encoded", "dit loaded", "step k/6" and "decoded", one line a picture in `engine_log_clock.csv`. TensorFold's server prints prompt, transformer, steps, decoder and total seconds for each picture, in `gen_image_rows.csv`. Its total matched the client's clock within 0.01 s on every picture.

## Every cell

ELI5: Every setting, its range and the number of pictures.

| Engine and setting | Size | Seconds | Range | Pictures |
|---|---|---|---|---|
| TensorFold, bf16 | 2048x2048 | 12.9 | 12.8 to 13.1 | 5 |
| TensorFold, bf16 | 1024x1024 | 13.4 | 13.1 to 13.8 | 3 |
| TensorFold, bf16 | 4096x4096 | 76.0 | 75.9 to 76.1 | 2 |
| Rapid-MLX, 4-bit at load | 2048x2048 | 13.3 | 13.3 to 13.4 | 5 |
| Rapid-MLX, 4-bit at load | 1024x1024 | 13.2 | 13.2 to 13.5 | 3 |
| Rapid-MLX, 8-bit at load | 2048x2048 | 14.6 | 14.6 to 14.7 | 5 |
| Rapid-MLX, 8-bit at load | 1024x1024 | 14.8 | 14.5 to 14.9 | 3 |
| mlx-serve, 4-bit pack | 2048x2048 | 13.4 | 13.3 to 13.4 | 5 |
| mlx-serve, 4-bit pack | 1024x1024 | 13.1 | 13.0 to 13.2 | 3 |
| mlx-serve, 4-bit pack | 4096x4096 | 51.8 | 51.7 to 51.9 | 2 |
| mlx-serve, 8-bit pack | 2048x2048 | 14.9 | 14.9 to 15.0 | 5 |
| mlx-serve, 8-bit pack | 1024x1024 | 14.8 | 14.7 to 14.8 | 3 |
| mlx-serve, 8-bit pack | 4096x4096 | 55.5 | 55.4 to 55.7 | 2 |
| mlx-serve, 8-bit pack, int8 off | 2048x2048 | 14.4 | 14.3 to 14.5 | 3 |
| mlx-serve, 8-bit pack, again at the end | 2048x2048 | 15.1 | 15.0 to 15.2 | 3 |

- **Rapid-MLX 1.1.0 refused 4096x4096** on both its 4-bit and 8-bit names, with HTTP 400 and "width must be between 256 and 2048". The limit is fixed in its request check (`_IMAGE_MAX_DIM = 2048` in `rapid_mlx/api/models.py` at 1.1.0), not a setting. The card names 4096x4096, a 16 MP area, as its best size. TensorFold and mlx-serve drew it.
- **Too close to rank at 1024 and 2048.** The fastest setup of each engine fell within 0.5 s there, and the order changed between the two sizes. mlx-serve's repeated 8-bit cell moved 0.2 s in 23 minutes. TensorFold's pictures grew slower one by one within a cell, 12.8 to 13.1 s at 2048x2048 and 13.1 to 13.8 s at 1024x1024. At 4096x4096 the gap, 51.8 against 76.0 s, is far larger than any of that.
- **First pictures.** Rapid-MLX's first picture of a start took 21.8 s and 23.1 s, and TensorFold's 13.7 s while it loaded its model. These are the warm-ups, left out above.
- **The night held steady.** mlx-serve's 8-bit pack took 14.9 s first and 15.1 s at the end, 23 minutes later, the same picture by its hash.

## The setup

ELI5: Each engine at its newest release, run as its own docs show, with the maker's settings.

- **mlx-serve** 26.11.3, the newest stable release on 24 Nov 2026 03:00 SGT (a 26.11.4 pre-release exists), installed with Homebrew. `mlx-serve --model <pack> --serve --host 127.0.0.1 --port <port>`, and the same with `--no-w8a8` for the int8-off start. Requests to its image endpoint with the size and seed 42, steps and guidance left out, since its card fixes 6 steps and refuses a guidance_scale field.
- **Rapid-MLX** 1.1.0, the newest release on 24 Nov 2026 03:15 SGT, `rapid-mlx serve minimax-h3-image`, and `minimax-h3-image-8bit` for its 8-bit name, downloads off. Both read the maker's diffusers files and quantize them at load. Requests with steps 6, guidance 1 and seed 42, as its own timing notes give.
- **TensorFold** 1.3.4's `tf-h3-image-server`, the newest release on 24 Nov 2026 03:00 SGT, built from the v1.3.4 tag as its MiniMax-H3-Image recipe shows, network denied by `sandbox-exec`. It reads the maker's native files and H3's text encoder, keeps the model loaded, and takes one request a line. Seed 42, its fixed 6 steps.
- **Prompt.** One sentence about a lighthouse at dusk, the same for all three engines.

| Weights | Hugging Face | Revision | Size |
|---|---|---|---|
| The maker's, for Rapid-MLX and TensorFold | [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | 5f904730 | 63.9 GiB each set |
| H3's text encoder, which both read | [MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) | b3c7290e | part of the 134.2 GiB set of finding 33 |
| mlx-serve author's 8-bit pack | [ddalcu/MiniMax-H3-Image-MLX-Serve-8bit](https://huggingface.co/ddalcu/MiniMax-H3-Image-MLX-Serve-8bit) | 47ae6e53 | 61.3 GiB |
| mlx-serve author's 4-bit pack | [ddalcu/MiniMax-H3-Image-MLX-Serve-4bit](https://huggingface.co/ddalcu/MiniMax-H3-Image-MLX-Serve-4bit) | 92d4839a | 34.3 GiB |

Every file was checked against its SHA-256, and each file's own Hugging Face scan read safe before the download.

| Run id | Engine and weights | Started, SGT, 24 Nov 2026 |
|---|---|---|
| `0f06fa6c299a` | mlx-serve, 8-bit pack | 02:31 |
| `2798fe5dfea5` | mlx-serve, 4-bit pack | 02:36 |
| `a95fcc14f6ac` | mlx-serve `--no-w8a8`, 8-bit pack | 02:41 |
| `f81046e17067` | Rapid-MLX, `minimax-h3-image` | 02:43 |
| `fa302b37ff17` | Rapid-MLX, `minimax-h3-image-8bit` | 02:45 |
| `tf11240248` | TensorFold `tf-h3-image-server` | 02:48 |
| `c67ff5fc9694` | mlx-serve, 8-bit pack, again | 02:54 |

## Licence

- **MiniMax-H3-Image has its own licence,** with the same excluded territories as H3 (the European Union, the United Kingdom, the Republic of Korea and the United States) and limits on where outputs may be shown. The Mac is in Singapore. I publish timings only, no picture. My clients hashed each picture and kept none, and a check after the run found no picture files written.

## Check it yourself

ELI5: Every picture's timing is in two files, one from the clients and one from mlx-serve's log.

- **`gen_image_rows.csv`.** 64 rows, one a request, warm-ups included and marked, with the client's seconds, each engine's own clock where it gives one, the PNG's size and a short hash. The two refused Rapid-MLX requests are in it. Its `peak_rss_gib` is the server's process size only, which leaves out GPU memory on this Mac.
- **`engine_log_clock.csv`.** 32 rows, one an mlx-serve picture, with its logged canvas, prompt, model load, steps and decode in ms.

## What I did not verify

- **Picture quality.** I did not look at or grade the pictures, so this page does not say which engine or pack draws better. The engines ran different weights.
- **Memory.** The process sizes in the CSV leave out GPU memory on this Mac, so I quote none.
- **More prompts.** One prompt and seed throughout.
- **Image editing.** The model can also edit a picture from a reference. Only text to picture ran here.

## Credit

- **mlx-serve and its packs.** [mlx-serve](https://github.com/ddalcu/mlx-serve) by [@ddalcu](https://x.com/ddalcu).
- **Rapid-MLX.** [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX), [@rapidmlx](https://x.com/rapidmlx).
- **TensorFold.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Model.** MiniMax-H3-Image by MiniMax.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
