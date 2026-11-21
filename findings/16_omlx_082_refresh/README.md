# Finding 16. Five models on oMLX 0.8.2, a version refresh

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: oMLX 0.8.2 came out on 21 Nov 2026 at 12:20 SGT. Its notes call it a hotfix for click positions on screenshots and say everything else is the same as 0.8.1. My rule is to run the newest stable release, so I reran my default oMLX lines on it. One fresh server start a setting, with the same settings and the same texts as before. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**I see no speed change on oMLX 0.8.2 on any of the five models. Text by text against the earlier start, the middle ratio sits between 0.95 and 1.05 in every test. Hy4-flash oQ4h wrote the same text as on 0.8.1 on 100 of 100 short replies, and Qwen3.8 Flash Next full wrote the same answers as on 0.8.0 on 250 of 250. One line moved a lot by my own rule and I do not read it as a change. Inkling 2 Mini's max is 83.5 tok/s on this start against 96.3 on the 0.8.1 start, with overlapping ranges. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 21 Nov 2026.**

| Model and build | Max on 0.8.2 | Max before | Median on 0.8.2 | Median before | Earlier release |
|---|---|---|---|---|---|
| GLM-5.3 Flash, oQ4e | 76.0 | 78.7 | 70.9 | 69.7 | 0.8.1 |
| Hy4-flash, oQ4h, thinking off | 76.8 | 75.6 | 52.1 | 53.7 | 0.8.1 |
| Inkling 2 Mini, oQ4e | 83.5 | 96.3 | 65.8 | 65.9 | 0.8.1 |
| Inkling 2 Small, oQ4e | 52.7 | 51.6 | 41.3 | 42.2 | 0.8.0 |
| Qwen3.8 Flash Next, full, default depth | 50.8 | 49.4 | 34.6 | 33.2 | 0.8.0 |
| Qwen3.8 Flash Next, full, fixed depth 4 | 54.3 | 54.2 | 33.3 | 33.6 | 0.8.0 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The "before" columns** are the starts in findings [9](../09_omlx_080_four_models), [12](../12_hy4_flash_omlx_081), [14](../14_inkling2_mini_omlx_081) and [15](../15_glm53_flash_two_builds). Their rows are in those folders.
- **Drafts on in every row.** These are the engine's draft settings at their default depth, and one fixed depth for Qwen3.8 Flash Next.
- **Three of the five wrote thinking text.** GLM-5.3 Flash and the two Inkling models think even when the request switches thinking off, as on the earlier releases. Their speeds count every token written.

## Chart

ELI5: The same test on the new release and on the release each line ran on before. One pair of bars a model.

![Bars of writing speed in tokens per second, greedy at temperature 0, new code, replies of up to 2,048 tokens, 1K prompt, drafts on at the default depth. On oMLX 0.8.2 against the earlier start. GLM-5.3 Flash oQ4e 76.0 against 78.7. Hy4-flash oQ4h 76.8 against 75.6. Inkling 2 Mini 78.7 against 96.3. Inkling 2 Small 52.7 against 51.6. Qwen3.8 Flash Next full 50.8 against 49.4.](chart_max.png)

- **The chart is the 1K prompt only.** Inkling 2 Mini's max in the table above is its 4K cell, 83.5.
- **Inkling 2 Mini's two bars overlap in range.** The five 0.8.2 runs went from 76.9 to 96.7 and the five 0.8.1 runs from 83.1 to 97.3. The section "Inkling 2 Mini, the line that moved" has the rest.

## Same-text pairs

ELI5: Each request's text is picked from its size and repeat number, so the new release got the very texts the old one got. A pair is one text on both releases. If a release were faster, most pairs would say so.

New over old. "Faster on" counts the pairs where 0.8.2 wrote faster. The middle ratio is the median of 0.8.2 over the earlier start.

| Model | Runs, new and old | Long code replies | Short code replies | Own sampler |
|---|---|---|---|---|
| GLM-5.3 Flash, oQ4e | `34ae658e42ba`, `421e19a82f36` | 6 of 10, 1.01 | 7 of 10, 1.03 | 3 of 5, 1.00 |
| Hy4-flash, oQ4h | `fab79618854c`, `61f1f5a70d04` | 8 of 10, 1.01 | 4 of 10, 0.96 | 2 of 5, 0.99 |
| Inkling 2 Mini, oQ4e | `ff41df9ec565`, `a3cf6857c4b5` | 3 of 10, 0.95 | 5 of 10, 1.00 | 2 of 5, 1.00 |
| Inkling 2 Small, oQ4e | `fd37c30fd993`, `818c28dbb625` | 4 of 10, 0.98 | 2 of 10, 0.96 | 2 of 5, 0.98 |
| Qwen3.8 Flash Next, default depth | `fbc94b62491c`, `6542a7f95175` | 8 of 10, 1.01 | 5 of 10, 0.99 | 4 of 5, 1.00 |
| Qwen3.8 Flash Next, fixed depth 4 | `8f063cd2f425`, `5f6db4faf823` | 4 of 10, 0.99 | 6 of 10, 1.02 | 2 of 5, 0.96 |

- **The ratios run from 0.95 to 1.03.**
- **One row leans one way in all three tests.** Inkling 2 Small was 2% to 4% lower on 0.8.2 on code and with the sampler. Its copy and counting pairs lean the other way, as the next line shows.
- **Easy text was level too.** On Hy4-flash the copy and counting pairs were each faster on 4 of 10 with a middle ratio of 1.00. On Inkling 2 Small they were 6 of 10 with 1.05 and 6 of 10 with 1.01. On Qwen3.8 Flash Next they were 8 of 10 with 1.02 and 5 of 10 with 1.00.
- **One start a release.** Finding 3 measured 7% between two starts of one setting on this engine. No middle ratio here is outside that.

## Inkling 2 Mini, the line that moved

ELI5: The summary page shows the latest start by rule, not the best one. On this model the new start's top cell came in lower. The evidence does not say the release is slower.

Decode tok/s, oQ4e build, drafts on at the default depth. Run `ff41df9ec565` on 0.8.2 and `a3cf6857c4b5` on 0.8.1.

| Test | Prompt | oMLX 0.8.1 | oMLX 0.8.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 96.3 (83.1 to 97.3) | 78.7 (76.9 to 96.7) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 80.1 (79.5 to 98.3) | 83.5 (76.0 to 88.3) |
| Greedy, new code, 512-token replies | 1K | 79.9 (50.6 to 89.6) | 80.8 (68.9 to 88.8) |
| Greedy, new code, 512-token replies | 4K | 80.4 (69.7 to 87.2) | 74.3 (68.4 to 94.3) |
| Own sampler, mixed text, 512-token replies | 4K | 65.9 (59.2 to 67.7) | 65.8 (63.1 to 74.1) |

- **The max by my rule fell from 96.3 to 83.5.** The 1K cell fell and the 4K cell rose.
- **The ranges overlap in every cell.** The fastest 1K run on 0.8.2 was 96.7, next to 97.3 on 0.8.1.
- **The pairs are mixed.** Long replies were faster on 3 of 10 with a middle ratio of 0.95. Short replies were faster on 5 of 10 with 1.00. The sampler cell is 65.8 against 65.9.
- **Drafted speed on this model spreads widely.** Finding 14 showed one 0.8.1 cell running from 50.6 to 89.6.
- **The greedy text is not fixed on this model with drafts on.** Inside one start, the second pass of 50 short questions gave the first pass's text on 46 of 50 on 0.8.2 and on 47 of 50 on 0.8.1. A different text takes a different time.
- **So I call it start spread, and I have one start to show for it.** A second 0.8.2 start is queued on this Mac behind another job. The summary page shows 83.5 until then, and the 0.8.1 line stays in the full table marked as an older release.

## The other four models

ELI5: Each cell is the middle of 5 runs, with the slowest and fastest run in brackets. The earlier start is on the left.

### GLM-5.3 Flash, oQ4e

Decode tok/s, MTP on at the default depth. Run `421e19a82f36` on 0.8.1 and `34ae658e42ba` on 0.8.2.

| Test | Prompt | oMLX 0.8.1 | oMLX 0.8.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 78.7 (73.7 to 86.2) | 76.0 (72.9 to 78.8) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 73.4 (66.6 to 77.3) | 73.9 (69.3 to 81.1) |
| Greedy, new code, 512-token replies | 1K | 80.7 (73.4 to 82.3) | 79.4 (74.1 to 91.3) |
| Greedy, new code, 512-token replies | 4K | 73.2 (67.7 to 76.6) | 73.6 (71.4 to 86.9) |
| Own sampler, mixed text, 512-token replies | 4K | 69.7 (66.9 to 73.3) | 70.9 (64.9 to 73.7) |

- **Every timed reply was thinking text**, as on 0.8.1. [Finding 15](../15_glm53_flash_two_builds) explains why.

### Hy4-flash, oQ4h, thinking off

Decode tok/s, Lightning MTP on at the default depth. Run `61f1f5a70d04` on 0.8.1 and `fab79618854c` on 0.8.2.

| Test | Prompt | oMLX 0.8.1 | oMLX 0.8.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 75.6 (72.7 to 76.8) | 76.8 (72.5 to 78.4) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 73.5 (67.0 to 78.6) | 75.1 (68.0 to 79.3) |
| Greedy, new code, 512-token replies | 1K | 73.0 (64.5 to 76.9) | 70.3 (65.6 to 76.1) |
| Greedy, new code, 512-token replies | 4K | 68.2 (63.1 to 74.3) | 65.3 (58.5 to 71.0) |
| Own sampler, mixed text, 512-token replies | 4K | 53.7 (50.8 to 57.5) | 52.1 (48.2 to 55.8) |
| Copy the prompt, 512-token replies | 1K | 101.0 (94.3 to 103.0) | 100.9 (94.2 to 103.4) |
| Copy the prompt, 512-token replies | 4K | 92.1 (88.1 to 93.3) | 91.7 (87.6 to 93.6) |
| Count from 1, 512-token replies | 1K | 97.4 (92.1 to 98.9) | 97.4 (92.0 to 98.2) |
| Count from 1, 512-token replies | 4K | 92.0 (91.3 to 92.0) | 91.5 (91.3 to 92.1) |

- **Every timed reply was answer text**, with 0 reasoning tokens by the server's count.
- **3 of the 10 long replies ran to 2,048 tokens.** The model ended the other 7 itself, the shortest at 686 tokens.

### Inkling 2 Small, oQ4e

Decode tok/s, DSpark draft on at the default depth. Run `818c28dbb625` on 0.8.0 and `fd37c30fd993` on 0.8.2.

| Test | Prompt | oMLX 0.8.0 | oMLX 0.8.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 51.6 (46.9 to 51.9) | 52.7 (48.8 to 53.5) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 48.6 (46.0 to 58.7) | 47.6 (43.6 to 53.2) |
| Greedy, new code, 512-token replies | 1K | 49.2 (47.0 to 55.3) | 48.4 (46.6 to 49.5) |
| Greedy, new code, 512-token replies | 4K | 44.8 (44.5 to 47.2) | 44.1 (41.7 to 46.6) |
| Own sampler, mixed text, 512-token replies | 4K | 42.2 (39.7 to 46.0) | 41.3 (39.0 to 42.4) |
| Asked to copy the prompt, 512-token replies | 1K | 57.6 (36.7 to 63.5) | 56.8 (42.2 to 62.9) |
| Asked to copy the prompt, 512-token replies | 4K | 48.4 (46.6 to 60.8) | 51.3 (49.7 to 68.9) |
| Asked to count from 1, 512-token replies | 1K | 82.8 (78.2 to 83.5) | 83.0 (74.6 to 95.9) |
| Asked to count from 1, 512-token replies | 4K | 83.3 (82.7 to 85.4) | 82.7 (78.8 to 92.5) |

- **Mostly thinking text**, as on 0.8.0. Every short code reply and every sampled reply was 510 thinking tokens and 2 answer tokens. The long code replies held 1,451 to 2,046 thinking tokens of 2,048.
- **The copy and counting rows are not on the summary page.** Those replies were part thinking text, from 82 to 510 thinking tokens on the copy question and 62 to 510 on the counting one.

### Qwen3.8 Flash Next, full precision

Decode tok/s, MTP on with the built-in head. At the default depth, runs `6542a7f95175` and `57b0f4425846` on 0.8.0 and `fbc94b62491c` on 0.8.2.

| Test | Prompt | 0.8.0, first start | 0.8.0, second start | oMLX 0.8.2 |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 49.3 (44.1 to 51.9) | 49.4 (46.9 to 52.6) | 50.8 (46.2 to 52.5) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 48.9 (41.9 to 51.7) | 48.5 (45.3 to 51.4) | 49.1 (44.9 to 53.6) |
| Greedy, new code, 512-token replies | 1K | 44.0 (41.2 to 47.9) | 43.9 (40.5 to 47.5) | 45.2 (41.3 to 48.3) |
| Greedy, new code, 512-token replies | 4K | 46.9 (38.2 to 48.6) | 45.8 (43.1 to 46.7) | 44.9 (39.7 to 46.1) |
| Own sampler, mixed text, 512-token replies | 4K | 33.2 (31.5 to 34.6) | not run | 34.6 (31.6 to 35.1) |
| Copy the prompt, 512-token replies | 1K | 120.1 (115.1 to 132.3) | not run | 128.7 (119.0 to 132.0) |
| Copy the prompt, 512-token replies | 4K | 116.9 (98.2 to 125.2) | not run | 119.5 (105.2 to 126.7) |
| Count from 1, 512-token replies | 1K | 49.5 (47.6 to 51.8) | not run | 50.2 (48.9 to 51.4) |
| Count from 1, 512-token replies | 4K | 51.5 (51.1 to 52.6) | not run | 51.4 (50.1 to 52.2) |

With `mtp_fixed_depth` at 4, run `5f6db4faf823` on 0.8.0 and `8f063cd2f425` on 0.8.2.

| Test | Prompt | oMLX 0.8.0 | oMLX 0.8.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 53.6 (47.6 to 55.3) | 54.3 (50.2 to 55.4) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 54.2 (47.0 to 60.7) | 53.6 (49.2 to 59.2) |
| Greedy, new code, 512-token replies | 1K | 46.9 (42.5 to 51.4) | 50.0 (47.4 to 50.2) |
| Greedy, new code, 512-token replies | 4K | 52.9 (43.2 to 53.3) | 51.6 (40.6 to 54.4) |
| Own sampler, mixed text, 512-token replies | 4K | 33.6 (31.8 to 40.2) | 33.3 (31.9 to 33.9) |

- **Every timed reply was answer text**, with 0 reasoning tokens.
- **Fixed depth 4 still helps on code and not with the sampler.** On 0.8.2 it was faster than the default depth on 9 of 10 long code replies with a middle ratio of 1.09, and on 10 of 10 short ones with 1.12. With the model's own sampler it was faster on 1 of 5 with 0.96. Finding 9 measured 53.6 against 49.4 on code and 33.6 against 33.2 with the sampler on 0.8.0.
- **This is the model the hotfix names.** The fix is for image input. I sent text only, so I did not test it.
- **Long replies.** 5 of 10 ran to 2,048 tokens at the default depth and 4 of 10 at depth 4. The shortest were 1,571 and 1,248.

## Did the text change

ELI5: A new release is only a fair swap if it writes the same words. I ask short greedy questions on both releases and compare the replies by hash.

| Model | Check | Same on 0.8.2 and the earlier start | Second pass against first, inside each start |
|---|---|---|---|
| Hy4-flash, oQ4h | 50 questions asked twice, thinking and answer text together | 100 of 100 | 50 of 50 on both releases |
| GLM-5.3 Flash, oQ4e | the same check | 98 of 100 | 49 of 50 on both releases |
| Inkling 2 Mini, oQ4e | the same check | 95 of 100 | 46 of 50 on 0.8.2, 47 of 50 on 0.8.1 |
| Inkling 2 Small, oQ4e | the same check | no 0.8.0 file to compare | 49 of 50 on 0.8.2 |
| Qwen3.8 Flash Next, default depth | 250 questions, answer text | 250 of 250 | not asked twice |

- **Hy4-flash and Qwen3.8 Flash Next wrote the same text on both releases.**
- **GLM-5.3 Flash and Inkling 2 Mini do not repeat themselves inside one start**, as the last column shows. So 98 of 100 and 95 of 100 across releases is what one release does against itself, and I read no version change into it.
- **Qwen3.8 Flash Next at depth 4 gave the default depth's answers** on 250 of 250, on 0.8.2. The 0.8.0 depth-4 start had no answer check.
- **Each reply is 64 tokens at most**, on a prompt of about 256 tokens. The check files are not in `rows.csv`.

## oMLX lines I did not rerun

ELI5: A refresh covers the default lines. These settings are still on the release they first ran on, and the summary page says which.

- **DeepSeek V4.1 Flash, oQ4e-mtp.** oMLX 0.8.0, findings [3](../03_dsv41_omlx_080) and [5](../05_dsv41_omlx_080_max_push). The build is parked on an external drive and is next in line.
- **GLM-5.3, 4-bit.** oMLX 0.8.0, finding 9.
- **GLM-5.3 Flash.** The fixed depth 4 line on 0.8.0, the drafts-off lines on 0.8.1, and TensorFold's 4-bit build on 0.8.1.
- **Hy4-flash, oQ4h.** The drafts-off lines and the lines with no thinking setting, on 0.8.1.
- **Inkling 2 Mini.** The drafts-off line and the oQ3e build, on 0.8.1.

## The setup

ELI5: One engine at its newest release and five sets of weights. Nothing but the release differs from the earlier starts.

- **Engine.** [oMLX](https://github.com/jundot/omlx) 0.8.2, released 21 Nov 2026 12:20 SGT, installed from the tagged source with its custom kernels built (`OMLX_WITH_CUSTOM_KERNEL=1`). The source tarball's SHA-256 equals the one in the project's Homebrew formula. `omlx --version` prints 0.8.2, and all five kernel families report available.
- **The installed packages differ from my 0.8.1 install in one line**, the oMLX version itself, by `pip freeze`.
- **Still the newest.** GitHub listed 0.8.2 as the latest release when I checked on 21 Nov 2026 at 20:17 SGT.
- **Serve command.**

```bash
omlx serve --model-dir <models> --host 127.0.0.1 --port 8198 --max-concurrent-requests 1 --headless --no-hf-cache --base-path <home>
```

- **Weights**, the builds of the earlier findings, each verified against its pinned commit.
  - [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) @ 9e5c75a9.
  - [Jundot/Hy4-flash-oQ4h-mtp](https://huggingface.co/Jundot/Hy4-flash-oQ4h-mtp) @ 6255edf3.
  - [mlx-community/Inkling-2-Mini-oQ4e-mtp](https://huggingface.co/mlx-community/Inkling-2-Mini-oQ4e-mtp) @ 3eea0427.
  - [mlx-community/Inkling-2-Small-oQ4e](https://huggingface.co/mlx-community/Inkling-2-Small-oQ4e) @ 973d9f96.
  - [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) @ 812d96e1, the maker's BF16 files.
- **Model settings**, in oMLX's own `model_settings.json`. `mtp_enabled` true, `a8_prefill_enabled` false, `activation_fp16_enabled` false, and `mtp_fixed_depth` unset or 4.
- **Burst decode.** `server.burst_decode_mode` at `balanced`, the default.
- **Thinking.** Every request switched thinking off. Hy4-flash and Qwen3.8 Flash Next then wrote answer text. The other three wrote thinking text.
- **Samplers.** Each model's own. Temperature 1.0 and top-p 0.95 for GLM-5.3 Flash. Temperature 0.9 and top-p 1.0 for Hy4-flash. Temperature 1.0 and top-p 1.0 for the two Inkling models. Temperature 0.7, top-p 0.8 and top-k 20 for Qwen3.8 Flash Next. Each is the same as on the earlier start.

| Run id | Model | Draft setting | Started, SGT, 21 Nov 2026 |
|---|---|---|---|
| `34ae658e42ba` | GLM-5.3 Flash, oQ4e | Default depth | 17:13 |
| `fab79618854c` | Hy4-flash, oQ4h | Default depth | 17:23 |
| `ff41df9ec565` | Inkling 2 Mini, oQ4e | Default depth | 17:35 |
| `fd37c30fd993` | Inkling 2 Small, oQ4e | Default depth | 17:44 |
| `fbc94b62491c` | Qwen3.8 Flash Next, full | Default depth | 18:03 |
| `8f063cd2f425` | Qwen3.8 Flash Next, full | Fixed depth 4 | 18:27 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as the earlier findings. Only the release changed.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last, thinking tokens included.
- **The three questions** are those of [finding 5](../05_dsv41_omlx_080_max_push), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **One start a release.** A gap of a few percent between two starts is not a version change.
- **One order only.** Every 0.8.2 start ran after the start it is compared with, between 17:13 and 18:47 SGT on 21 Nov 2026. The earlier starts ran between 01:33 and 16:43 SGT that day.
- **Thinking text is not answer text.** Three of these five models wrote thinking text.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 234 raw rows from the bench database. 210 timed requests and 24 warm-ups.
- **`runs.csv`.** The 6 runs behind them, with engine, version, start time, settings and sampling.
- **The earlier rows** are in findings 9, 12, 14 and 15.

From the top of this repository.

```bash
python3 tools/summarize.py findings/16_omlx_082_refresh
```

## What I did not verify

- **A second start on 0.8.2** of any setting. One is queued for Inkling 2 Mini.
- **The hotfix itself.** It is for image input and I sent text only.
- **The lines listed under "oMLX lines I did not rerun".**
- **What the timed replies say.** I read back none of them on 0.8.2.
- **Answer quality, long prompts, and two users at once.**
- **Server memory.** I did not compare it between the releases.

## Credit

- **Engine.** [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim).
- **Weights.** The oQ builds by Jundot and [mlx-community](https://huggingface.co/mlx-community). The BF16 files by Qwen.
- **Models.** GLM-5.3 Flash by Z.ai. Hy4-flash by Tencent. Inkling 2 Mini and Inkling 2 Small by Thinking Machines. Qwen3.8 Flash Next by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
