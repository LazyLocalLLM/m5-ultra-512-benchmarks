# Finding 26. oMLX 0.8.3, Inkling 2 Mini faster and three models level

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: oMLX 0.8.3 came out on 23 Nov 2026 at 02:23 SGT. Its notes call it an optimization release for Inkling 2 Mini and the Hy4 family. My rule is to run the newest stable release, so I reran the oMLX lines of [finding 16](../16_omlx_082_refresh) on it, with the same settings and the same texts. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**oMLX 0.8.3 wrote 108.1 tok/s on Inkling 2 Mini oQ4e at its max and 83.3 with the model's own sampler, against 85.3 and 60.3 on the last 0.8.2 start. Text by text it was faster on 25 of 25 pairs against each of three 0.8.2 starts, with middle ratios from 1.17 to 1.38. With drafts off it was 1.15 times 0.8.1 on 20 of 20 pairs. With drafts on and off it now wrote the same short replies, 100 of 100. Hy4-flash gave its first token 1.47 times sooner, and GLM-5.3 Flash, Hy4-flash and Qwen3.8 Flash Next wrote at the same speed as on 0.8.2. Switching thinking off did not stop Inkling 2 Mini thinking. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Model and build | Max on 0.8.3 | Max on 0.8.2 | Median on 0.8.3 | Median on 0.8.2 |
|---|---|---|---|---|
| Inkling 2 Mini, oQ4e, default thinking effort | 108.1 | 85.3 | 83.3 | 60.3 |
| Inkling 2 Mini, oQ4e, thinking switched off | 104.2 | | 80.1 | |
| Inkling 2 Mini, oQ4e, thinking switched off, drafts off | 62.4 | 54.5 on 0.8.1 | not run | 54.4 on 0.8.1 |
| GLM-5.3 Flash, oQ4e | 77.4 | 76.0 | 70.1 | 70.9 |
| Hy4-flash, oQ4h, thinking off | 76.2 | 76.8 | 49.8 | 52.1 |
| Qwen3.8 Flash Next, full, default depth | 49.1 | 50.8 | 34.4 | 34.6 |
| Qwen3.8 Flash Next, full, fixed depth 4 | 54.5 | 54.3 | 32.4 | 33.3 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The 0.8.2 columns** are finding 16's starts, the third for Inkling 2 Mini. The drafts-off line has no 0.8.2 start, so it shows 0.8.1's, from [finding 14](../14_inkling2_mini_omlx_081). Finding 16 found 0.8.1 and 0.8.2 level.
- **Drafts on in every row** but the one marked off, at the engine's default depth and one fixed depth for Qwen3.8 Flash Next.
- **The thinking-off max is the latest of two starts.** The first wrote 107.9.
- **Inkling 2 Small was not rerun.** Its build is parked on an external drive. Its line stays on 0.8.2.

## Chart

ELI5: The same test on 0.8.3 and on 0.8.2. One pair of bars a line.

![Bars of writing speed in tokens per second, oMLX 0.8.2 against 0.8.3, drafts on, median of 5. Max is greedy new code, 2,048-token replies, 1K prompt. Inkling 2 Mini oQ4e max 85.3 against 108.1. Inkling 2 Mini median, own sampler, 4K prompt, 60.3 against 83.3. GLM-5.3 Flash max 76.0 against 77.4. Hy4-flash max 76.8 against 72.4. Qwen3.8 Flash Next max 50.8 against 49.0.](chart_max.png)

- **The max bars are the 1K prompt only.** Hy4-flash's 1K cell on 0.8.3 had one slow run, 56.1. At 4K it wrote 76.2 against 75.1.
- **Inkling 2 Mini's 0.8.3 bars are the start with no thinking field.** The next section says why.

## Inkling 2 Mini

ELI5: The same weights and settings on the new release. Each request's text is picked from its size and repeat number, so 0.8.3 got the very texts 0.8.2 got. A pair is one text on both releases. If a release is faster, most pairs say so.

Decode tok/s, oQ4e build, DSpark drafts on at the default depth. Run `af8afe759506` on 0.8.3, with no thinking field. Run `a7944f4eab8a` on 0.8.2, finding 16's third start.

| Test | Prompt | oMLX 0.8.2 | oMLX 0.8.3 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 85.3 (81.3 to 94.1) | 108.1 (93.7 to 117.8) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 78.1 (73.7 to 87.1) | 102.0 (91.6 to 117.3) |
| Greedy, new code, 512-token replies | 1K | 79.5 (66.6 to 87.4) | 100.5 (93.6 to 175.7) |
| Greedy, new code, 512-token replies | 4K | 82.3 (65.8 to 84.2) | 96.0 (86.3 to 99.1) |
| Own sampler, mixed text, 512-token replies | 4K | 60.3 (50.8 to 72.2) | 83.3 (78.6 to 87.6) |

Same-text pairs, 0.8.3 over each 0.8.2 start. "Faster on" counts the pairs where 0.8.3 wrote faster. The ratio is the median of 0.8.3 over 0.8.2.

| 0.8.2 start | Long code replies | Short code replies | Own sampler |
|---|---|---|---|
| `ff41df9ec565`, first | 10 of 10, 1.20 | 10 of 10, 1.26 | 5 of 5, 1.27 |
| `2d6bd492fd78`, second | 10 of 10, 1.17 | 10 of 10, 1.23 | 5 of 5, 1.22 |
| `a7944f4eab8a`, third | 10 of 10, 1.26 | 10 of 10, 1.22 | 5 of 5, 1.38 |
| `a3cf6857c4b5`, 0.8.1 | 10 of 10, 1.13 | 10 of 10, 1.23 | 5 of 5, 1.29 |

- **Faster on every pair against every earlier start.** Finding 16 put three 0.8.2 starts of this line at 83.5, 88.5 and 85.3 at the max. The 0.8.3 start beat each of them on all 25 pairs.
- **The notes say decode is 10 to 13% faster,** measured on an M5 Max. My middle ratios run from 1.13 to 1.38 on one 0.8.3 start.
- **Drafts off, a cleaner test of each token's cost.** 62.4 (62.2 to 62.5) at 1K on 0.8.3 against 54.5 (54.3 to 54.5) on 0.8.1, both on long code. Faster on 10 of 10 long and 10 of 10 short replies, with a middle ratio of 1.15 on both. The five runs of each cell sit within 0.7 of each other, so text has little say here. This 0.8.3 start had thinking switched off and the 0.8.1 start did not.
- **What the drafts give on 0.8.3.** 104.2 / 62.4 = 1.67 at the max on the latest thinking-off start, and 107.9 / 62.4 = 1.73 on the first. Finding 14 measured 1.77 on 0.8.1.
- **The prompt is read faster.** First token at 4K 1.66 s against 1.94 s, sooner on 15 of 15 pairs, middle ratio 1.16. At 1K 0.54 s against 0.72 s, 10 of 10, 1.35. oMLX's own prompt timing gives 3,440 to 3,543 tok/s at 4K against 2,860 to 3,119. The notes say about 20% at 4K.
- **Copying the prompt was faster too, on the thinking-off start.** 157.8 tok/s at 1K and 119.6 at 4K, against 67.1 and 69.0 on 0.8.1, faster on 10 of 10 pairs with a middle ratio of 1.78. The model copied the text inside its thinking, and the thinking setting differs between the two starts. The notes say copying from context is more than twice as fast.

## Thinking switched off

ELI5: The notes say Inkling 2 now stops thinking when a request switches thinking off. On this build it thought less on some replies, but it still thought first on every reply.

- **What 0.8.3 sends.** `enable_thinking: false` and `reasoning_effort: "off"` both become the template's effort "none". I read this in oMLX's `engine/vlm.py`. The model's own template turns "none" into a system line, "Thinking effort level: 0", and its default is 0.9. That line is my reading of the template.
- **What I measured.** With the switch sent, every prompt on the answer check was 2 tokens shorter on 0.8.3 than on 0.8.2, 100 of 100, 268 against 270 on the first question. That fits "0" against "0.9". The two switches gave the same reply, byte for byte, 786 characters of thinking text and no answer in 256 tokens.
- **It still thought.** Every one of the 75 timed replies on the thinking-off starts held at least 253 thinking tokens. On the answer check, 100 of 100 short replies were thinking text with no answer. In the timed rows on the thinking-off starts, no sampled reply and 3 of 20 short code replies reached an answer of over 10 tokens.
- **It thought less on some long replies.** At 1K, 3 of 5 and 4 of 5 long code replies reached an answer of over 10 tokens on the two thinking-off starts. On 0.8.2 it was 0 of 15 across three starts, and 1 of 5 on the 0.8.3 start with no thinking field.
- **Why the headline uses the start with no thinking field.** On 0.8.2 the switch never reached this template, so every earlier oMLX line on this model ran at the default effort. A start with no field gives 0.8.2's prompt. I checked it. The answer check's prompt token counts matched 0.8.2's on 100 of 100.
- **The effort level hardly moved the speed.** The start with no field was faster on 16 of 25 pairs against the first thinking-off start, with middle ratios from 1.03 to 1.05.

## Did the text change

ELI5: I ask 50 short greedy questions twice on each start and compare the whole reply, thinking text included, by hash.

| Check, 64-token replies | Result |
|---|---|
| 0.8.3, drafts on against drafts off, thinking switched off | 100 of 100 the same |
| 0.8.1, drafts on against drafts off, finding 14 | 43 of 100 the same |
| Second pass against first, inside each 0.8.3 start | 50 of 50 on all three starts |
| Second pass against first, inside each 0.8.2 start | 46, 48 and 49 of 50 |
| 0.8.3 with no thinking field against 0.8.1 with drafts off | 66 of 100 the same |
| 0.8.3 with no thinking field against each 0.8.2 start, drafts on | 37 to 38 of 100 the same |
| 0.8.1 with drafts off against the third 0.8.2 start | 42 of 100 the same |

- **The notes say greedy text with Lightning MTP now matches decoding without it.** On this check it did, 100 of 100. On 0.8.1 the drafts changed more than half the replies.
- **The release changed the text.** 0.8.3's replies are nearer to what 0.8.1 wrote with drafts off than to any earlier drafts-on start, but not the same. I report the counts and no cause.
- **Only short replies.** Each is 64 tokens at most, on a prompt of about 270 tokens. The timed prompts open with a random session line, so they can't be compared this way.
- **The check files are not in `rows.csv`.** Nor is Qwen3.8 Flash Next's 250-answer check.

## The other four lines

ELI5: Each cell is the middle of 5 runs, with the slowest and fastest in brackets. 0.8.2 is on the left.

| Model | Test | Prompt | oMLX 0.8.2 | oMLX 0.8.3 |
|---|---|---|---|---|
| GLM-5.3 Flash, oQ4e | Greedy, long code | 1K | 76.0 (72.9 to 78.8) | 77.4 (71.2 to 82.5) |
| | Greedy, long code | 4K | 73.9 (69.3 to 81.1) | 73.6 (66.3 to 77.4) |
| | Own sampler | 4K | 70.9 (64.9 to 73.7) | 70.1 (69.6 to 73.4) |
| Hy4-flash, oQ4h | Greedy, long code | 1K | 76.8 (72.5 to 78.4) | 72.4 (56.1 to 78.8) |
| | Greedy, long code | 4K | 75.1 (68.0 to 79.3) | 76.2 (67.5 to 78.5) |
| | Own sampler | 4K | 52.1 (48.2 to 55.8) | 49.8 (48.4 to 55.2) |
| | Copy the prompt | 1K | 100.9 (94.2 to 103.4) | 95.9 (93.7 to 98.1) |
| | Count from 1 | 1K | 97.4 (92.0 to 98.2) | 94.0 (92.6 to 94.0) |
| Qwen3.8 Flash Next, default depth | Greedy, long code | 1K | 50.8 (46.2 to 52.5) | 49.0 (45.5 to 51.3) |
| | Greedy, long code | 4K | 49.1 (44.9 to 53.6) | 49.1 (44.1 to 53.5) |
| | Own sampler | 4K | 34.6 (31.6 to 35.1) | 34.4 (34.1 to 36.1) |
| | Copy the prompt | 1K | 128.7 (119.0 to 132.0) | 128.4 (120.5 to 132.3) |
| Qwen3.8 Flash Next, fixed depth 4 | Greedy, long code | 1K | 54.3 (50.2 to 55.4) | 54.5 (49.2 to 56.6) |
| | Greedy, long code | 4K | 53.6 (49.2 to 59.2) | 51.1 (49.1 to 54.2) |
| | Own sampler | 4K | 33.3 (31.9 to 33.9) | 32.4 (30.2 to 35.0) |

Same-text pairs, 0.8.3 over 0.8.2.

| Model | Runs, new and old | Long code | Short code | Own sampler |
|---|---|---|---|---|
| GLM-5.3 Flash, oQ4e | `42c428b2af1f`, `34ae658e42ba` | 5 of 10, 1.00 | 0 of 10, 0.96 | 3 of 5, 1.01 |
| Hy4-flash, oQ4h | `0d2a17ccad56`, `fab79618854c` | 3 of 10, 0.99 | 4 of 10, 0.99 | 2 of 5, 0.99 |
| Qwen3.8 Flash Next, default depth | `e741a35f57d5`, `fbc94b62491c` | 2 of 10, 0.99 | 4 of 10, 1.00 | 3 of 5, 1.03 |
| Qwen3.8 Flash Next, fixed depth 4 | `780bb9bba309`, `8f063cd2f425` | 5 of 10, 1.00 | 5 of 10, 0.99 | 2 of 5, 0.97 |

- **Level, with one lean.** GLM-5.3 Flash's short code replies were slower on all 10 pairs, by a middle ratio of 0.96. That is inside the 7% finding 3 measured between two starts of one setting on this engine, and this is one start a release.
- **Hy4-flash's copy and counting pairs** were faster on 4 of 10 and 5 of 10, both at 1.00. On Qwen3.8 Flash Next they were 5 of 10 and 5 of 10, both at 1.00.
- **Hy4-flash gave its first token 1.47 times sooner.** 1.81 s against 2.71 s at 4K, sooner on 25 of 25 pairs. 0.56 s against 0.83 s at 1K, 20 of 20, 1.48. oMLX's own prompt timing gives 2,215 to 2,317 tok/s at 4K against 1,490 to 1,546. The notes name faster prefill on M5 and a smaller write to the SSD cache. The cache was on, at its default, on both releases, with no cache hits.
- **GLM-5.3 Flash and Qwen3.8 Flash Next gave their first token at the same time** on both releases, middle ratios 0.99 to 1.01.
- **The same text.** Hy4-flash's 50 short questions asked twice gave the same replies as on 0.8.2, 100 of 100. GLM-5.3 Flash gave 98 of 100, as it repeats itself on 49 of 50 inside one start. Qwen3.8 Flash Next gave 0.8.2's 250 answers on 250 of 250, and depth 4 gave the default depth's on 250 of 250.
- **Thinking.** GLM-5.3 Flash wrote thinking text in every timed reply, as before. Hy4-flash and Qwen3.8 Flash Next wrote answer text with 0 thinking tokens.

## The setup

ELI5: One engine at its newest release and four sets of weights. Nothing but the release differs from finding 16, apart from one Inkling start with no thinking field.

- **Engine.** [oMLX](https://github.com/jundot/omlx) 0.8.3, released 23 Nov 2026 02:23 SGT, installed from the tagged source with its custom kernels built (`OMLX_WITH_CUSTOM_KERNEL=1`). The source tarball's SHA-256 equals the one in the project's Homebrew formula. `omlx --version` prints 0.8.3, and all five kernel families report available.
- **The same mlx and mlx-lm** as my 0.8.2 install, mlx 0.32.4 and mlx-lm at commit 0d4d3d04.
- **Serve command.**

```bash
omlx serve --model-dir <models> --host 127.0.0.1 --port 8228 --max-concurrent-requests 1 --headless --no-hf-cache --base-path <home>
```

- **Weights**, the builds of finding 16, each verified against its pinned commit.
  - [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) @ 9e5c75a9.
  - [Jundot/Hy4-flash-oQ4h-mtp](https://huggingface.co/Jundot/Hy4-flash-oQ4h-mtp) @ 6255edf3.
  - [mlx-community/Inkling-2-Mini-oQ4e-mtp](https://huggingface.co/mlx-community/Inkling-2-Mini-oQ4e-mtp) @ 3eea0427.
  - [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) @ 812d96e1, the maker's BF16 files.
- **Model settings**, in oMLX's own `model_settings.json`. `mtp_enabled` true, or false on the drafts-off start, `a8_prefill_enabled` false, `activation_fp16_enabled` false, and `mtp_fixed_depth` unset or 4.
- **Burst decode.** `server.burst_decode_mode` at `balanced`, the default.
- **Thinking.** Every request switched thinking off with `enable_thinking: false`, as in finding 16, except Inkling start `af8afe759506`, which sent no thinking field.
- **Samplers.** Each model's own, sent with each request. Temperature 1.0 and top-p 0.95 for GLM-5.3 Flash. Temperature 0.9 and top-p 1.0 for Hy4-flash. Temperature 1.0 and top-p 1.0 for Inkling 2 Mini. Temperature 0.7, top-p 0.8 and top-k 20 for Qwen3.8 Flash Next.

| Run id | Model | Setting | Started, SGT, 23 Nov 2026 |
|---|---|---|---|
| `d066e1456e61` | Inkling 2 Mini, oQ4e | Drafts on, thinking switched off | 03:20 |
| `0f8455f8a46f` | Inkling 2 Mini, oQ4e | The same, second start, long code only | 03:30 |
| `1e9d52ecfc69` | Inkling 2 Mini, oQ4e | Drafts off, thinking switched off | 03:34 |
| `42c428b2af1f` | GLM-5.3 Flash, oQ4e | Drafts on | 03:44 |
| `0d2a17ccad56` | Hy4-flash, oQ4h | Drafts on | 03:54 |
| `e741a35f57d5` | Qwen3.8 Flash Next, full | Drafts on, default depth | 04:06 |
| `780bb9bba309` | Qwen3.8 Flash Next, full | Drafts on, fixed depth 4 | 04:30 |
| `af8afe759506` | Inkling 2 Mini, oQ4e | Drafts on, no thinking field | 05:04 |

## How I measured

ELI5: Same Mac, same harness and same texts as finding 16. Only the release changed.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last, thinking tokens included.
- **First token** is the client's time from sending the request to the first streamed piece. The prompt rate is oMLX's own input token count over its own prompt time.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **One start a release for most lines.** A gap of a few percent between two starts is not a version change. Inkling 2 Mini's gain is far above that and showed on every pair.
- **One order only.** Every 0.8.3 start ran after the 0.8.2 start it is compared with.
- **Thinking text is not answer text.** Inkling 2 Mini and GLM-5.3 Flash wrote thinking text.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 267 raw rows from the bench database. 240 timed requests and 27 warm-ups.
- **`runs.csv`.** The 8 runs behind them, with engine, version, start time, settings and sampling.
- **The 0.8.2 rows** are in finding 16, and the 0.8.1 rows in finding 14.

From the top of this repository.

```bash
python3 tools/summarize.py findings/26_omlx_083_refresh
```

## What I did not verify

- **A second start** of any line but Inkling 2 Mini with thinking switched off.
- **Inkling 2 Small**, parked, and DeepSeek V4.1 Flash, whose oMLX line is still on 0.8.0. The notes name a change for DeepSeek V4.1's drafts.
- **The notes' other claims.** Long-context memory, the SSD cache hit after a restart, Hy4-flash's N-gram offload, web search and the Prefill Accelerator.
- **Drafts off with the sampler** on 0.8.3.
- **What the timed replies say.** I read back the openings of the answer check only.
- **Answer quality, long prompts, two users at once, and server memory.**

## Credit

- **Engine.** [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim).
- **Weights.** The oQ builds by Jundot and [mlx-community](https://huggingface.co/mlx-community). The BF16 files by Qwen.
- **Models.** GLM-5.3 Flash by Z.ai. Hy4-flash by Tencent. Inkling 2 Mini by Thinking Machines. Qwen3.8 Flash Next by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
