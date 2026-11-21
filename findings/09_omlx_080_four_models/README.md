# Finding 9. Four more models on oMLX 0.8.0, max and median speed

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: My older lines for these four models came from oMLX 0.7.3 or from an unreleased commit. I reran them on oMLX 0.8.0, the latest stable release when these ran. oMLX 0.8.1 came out on 21 Nov 2026 at 09:17 SGT, after the last run here, and I have not run it yet. Each model gets two figures. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**On oMLX 0.8.0, GLM-5.3 Flash 4-bit wrote 80.2 tok/s at its max and 67.8 with its own sampler. Inkling 2 Small wrote 51.6 and 42.2. Qwen3.8 Flash Next at full precision wrote 53.6 on new code and 33.6 with its own sampler with the draft depth fixed at 4, against 49.4 and 33.2 at the default depth. GLM-5.3 4-bit wrote 24.6 and 24.5 with no drafts.**

Runs of 20 and 21 Nov 2026 SGT. One server start per setting unless a line says otherwise. Updated on 21 Nov 2026 at 09:45 SGT with a follow-up job. It added the reply read-backs, fixed depths 4 and 5 on GLM-5.3 Flash, and second starts and depths 5 and 6 on Qwen3.8 Flash Next.

| Model | Build | Max, tok/s | Median, tok/s |
|---|---|---|---|
| GLM-5.3 Flash | 4-bit, oQ4e-mtp | 80.2 | 67.8 |
| Inkling 2 Small | 4-bit, oQ4e | 51.6 | 42.2 |
| Qwen3.8 Flash Next | full, BF16 | 53.6 at fixed depth 4, 49.4 at the default depth | 33.6 at fixed depth 4, 33.2 at the default depth |
| GLM-5.3 | 4-bit | 24.6 | 24.5 |

- **Max** is the middle of 5 greedy runs on new code. Replies of up to 2,048 tokens at a 1K prompt for the first three models. 512-token replies at a 4K prompt for GLM-5.3, which ran no longer replies. Where a setting has two starts the figure is the later start. The later Flash Next start at fixed depth 4 wrote 54.2 at a 4K prompt, and that cell is the one the summary page shows.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **Three of the four wrote reasoning text.** GLM-5.3, GLM-5.3 Flash and Inkling 2 Small think even when the request switches thinking off. Their speeds count every token written, reasoning included.

## Chart

ELI5: The top speed on new code for the three models that ran long replies. One bar per model and prompt size.

![Bars of writing speed in tokens per second on oMLX 0.8.0, greedy at temperature 0, new code, replies of up to 2,048 tokens. GLM-5.3 Flash 4-bit 80.2 at a 1K prompt and 74.7 at 4K. Inkling 2 Small 51.6 and 48.6. Qwen3.8 Flash Next full at the default depth 49.3 and 48.9.](chart_max.png)

- **The Flash Next bars are its first default start**, run `6542a7f95175`. The second start wrote 49.4 and 48.5.

## Max speed, writing new code

ELI5: The model reads a block of code and is asked to write a new module with tests. Nothing in the reply can be copied from the prompt. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Greedy at temperature 0, code, replies of up to 2,048 tokens, tok/s.

| Model | Draft setting | Run | 1K prompt | 4K prompt |
|---|---|---|---|---|
| GLM-5.3 Flash 4-bit | Default depth | `8f12a00bcc4f` | 80.2 (68.4 to 87.6) | 74.7 (68.9 to 81.3) |
| GLM-5.3 Flash 4-bit | Fixed depth 4 | `605e0068ff28` | 71.7 (66.4 to 80.9) | 68.9 (62.1 to 74.9) |
| GLM-5.3 Flash 4-bit | Fixed depth 5 | `df87c103a0f9` | 64.4 (57.9 to 80.9) | 60.5 (52.2 to 65.3) |
| Inkling 2 Small | Default depth | `818c28dbb625` | 51.6 (46.9 to 51.9) | 48.6 (46.0 to 58.7) |
| Inkling 2 Small | Fixed depth 4 | `c624f11aa341` | 51.8 (48.1 to 54.6) | 50.4 (43.6 to 53.6) |
| Qwen3.8 Flash Next full | Default depth | `6542a7f95175` | 49.3 (44.1 to 51.9) | 48.9 (41.9 to 51.7) |
| Qwen3.8 Flash Next full | Fixed depth 4 | `601378891241` | 53.3 (48.7 to 56.2) | 52.7 (49.2 to 59.1) |
| Qwen3.8 Flash Next full | Default depth, second start | `57b0f4425846` | 49.4 (46.9 to 52.6) | 48.5 (45.3 to 51.4) |
| Qwen3.8 Flash Next full | Fixed depth 4, second start | `5f6db4faf823` | 53.6 (47.6 to 55.3) | 54.2 (47.0 to 60.7) |
| Qwen3.8 Flash Next full | Fixed depth 5 | `0350d62ae1e8` | 55.4 (49.8 to 56.7) | 54.1 (43.8 to 57.8) |
| Qwen3.8 Flash Next full | Fixed depth 6 | `1898791c30eb` | 55.1 (41.1 to 57.1) | 55.0 (45.9 to 62.1) |

Greedy at temperature 0, code, 512-token replies, tok/s.

| Model | Draft setting | Run | 1K prompt | 4K prompt |
|---|---|---|---|---|
| GLM-5.3 Flash 4-bit | Default depth | `8f12a00bcc4f` | 75.8 (70.4 to 78.5) | 69.8 (64.9 to 75.0) |
| GLM-5.3 Flash 4-bit | Fixed depth 4 | `605e0068ff28` | 70.8 (65.7 to 78.7) | 71.6 (63.3 to 81.4) |
| GLM-5.3 Flash 4-bit | Fixed depth 5 | `df87c103a0f9` | 64.3 (60.7 to 78.6) | 57.7 (51.8 to 67.3) |
| Inkling 2 Small | Default depth | `818c28dbb625` | 49.2 (47.0 to 55.3) | 44.8 (44.5 to 47.2) |
| Inkling 2 Small | Fixed depth 4 | `c624f11aa341` | 47.4 (44.4 to 53.0) | 45.0 (43.0 to 49.6) |
| Qwen3.8 Flash Next full | Default depth | `6542a7f95175` | 44.0 (41.2 to 47.9) | 46.9 (38.2 to 48.6) |
| Qwen3.8 Flash Next full | Fixed depth 4 | `601378891241` | 47.2 (44.7 to 52.4) | 51.9 (43.0 to 54.5) |
| Qwen3.8 Flash Next full | Default depth, second start | `57b0f4425846` | 43.9 (40.5 to 47.5) | 45.8 (43.1 to 46.7) |
| Qwen3.8 Flash Next full | Fixed depth 4, second start | `5f6db4faf823` | 46.9 (42.5 to 51.4) | 52.9 (43.2 to 53.3) |
| Qwen3.8 Flash Next full | Fixed depth 5 | `0350d62ae1e8` | 47.4 (42.2 to 54.8) | 52.3 (40.9 to 54.8) |

- **What the replies were.** Qwen3.8 Flash Next wrote answer text only. GLM-5.3 Flash wrote reasoning text only, 2,048 of 2,048 tokens. Inkling 2 Small wrote mostly reasoning, about 1,930 of 2,048 tokens on average. So for those two the max is a reasoning speed on a code task.
- **Longer replies wrote a little faster**, as in findings 5 to 8. GLM-5.3 Flash went from 75.8 to 80.2 at 1K. That is 80.2 / 75.8 = 1.06 times.
- **Some Flash Next replies ended before the cap.** 3 of 5 ran to 2,048 tokens in each default-depth cell of the first start. The shortest was 1,701 tokens. Across the six Flash Next starts the shortest long reply was 1,295 tokens.

## Draft depth

ELI5: These builds carry a small draft head that guesses a few tokens ahead, and the model checks the guesses. The depth is how many tokens it guesses at once. I tried fixed depths of 4, 5 and 6. A deeper draft helped one model, did nothing for another and slowed the third.

- **Qwen3.8 Flash Next full gained at fixed depth 4, on two starts.** The first starts wrote 53.3 against 49.3 at 1K. The second starts wrote 53.6 against 49.4, which is 53.6 / 49.4 = 1.09 times. Text by text the second fixed start was faster than the second default start on 10 of 10 long replies, with a middle ratio of 1.11. With 512-token replies it was faster on 9 of 10, with a middle ratio of 1.07.
- **The starts repeat.** On long replies the second default start against the first has a middle ratio of 1.01. The second fixed start against the first has 1.01 too.
- **Its own sampler was level at fixed depth 4.** 33.6 (31.8 to 40.2) against 33.2 (31.5 to 34.6) at the default, faster on 4 of 5 texts with a middle ratio of 1.03. One start each.
- **Depths 5 and 6 were level with depth 4.** Depth 5 wrote 55.4 and 54.1 with long replies, and depth 6 wrote 55.1 and 55.0, against 53.6 and 54.2 at depth 4. Text by text against the second depth-4 start, depth 5 was faster on 6 of 10 with a middle ratio of 1.00, and depth 6 on 7 of 10 with 1.01. Each is one start on code only, with no answer check and no sampled run. So the summary page keeps depth 4.
- **The log agrees.** At the default the deepest draft on every request of the first start was 3 tokens, and at fixed depth 4 it was 4. The last request of the depth-5 start drafted to 5, and that of the depth-6 start to 6.
- **GLM-5.3 Flash lost speed at a fixed depth.** Depth 4 wrote 71.7 against 80.2 at 1K with long replies, which is 71.7 / 80.2 = 0.89 times. Depth 5 wrote 64.4, which is 64.4 / 80.2 = 0.80 times. Text by text on long replies, depth 4 was faster on 1 of 10 with a middle ratio of 0.92, and depth 5 on 0 of 10 with 0.82. With 512-token replies depth 4 was level, faster on 5 of 10 with a middle ratio of 1.00. One start each. Depth 4's gap on long replies is close to the 7% that finding 3 measured between two starts of one setting, and depth 5's is clear of it. So the default stays this model's max.
- **It did not run in the first job.** My harness checks the listening ports before each start, and that check timed out after 5 seconds. That is my tool and says nothing about oMLX. Both depths ran in the follow-up job on 21 Nov 2026.
- **Inkling 2 Small was level on code.** 51.8 against 51.6 at 1K, faster on 6 of 10 texts with a middle ratio of 1.01. Its default is already deeper. The log shows its draft loaded at depth 7, adaptive, and at depth 4, not adaptive, on the fixed start.
- **Same answers, checked for Qwen3.8 Flash Next only.** On 250 short greedy questions, fixed depth 4 gave the default's answer on 250 of 250, from its first starts.
- **Correction, 21 Nov 2026 11:08 SGT.** This page said the same check gave 250 of 250 for GLM-5.3 Flash and for Inkling 2 Small. That check compares answer text only. On those two models every one of the 250 replies was reasoning text with an empty answer, so it compared empty strings and proved nothing. I have no answer check for a fixed depth on either model.

## The model's own sampler

ELI5: The everyday figure. The sampler the model's maker recommends, mixed text, a 4K prompt and 512-token replies. The older column is the line this finding replaces on the summary page.

| Model | Sampler | Run | oMLX 0.8.0 | Older line | Older engine |
|---|---|---|---|---|---|
| GLM-5.3 Flash 4-bit | temperature 1.0, top-p 0.95 | `8f12a00bcc4f` | 67.8 (63.2 to 72.2) | 68.8 (61.0 to 76.1) | oMLX 0.7.3 |
| Inkling 2 Small | temperature 1.0, top-p 1.0 | `818c28dbb625` | 42.2 (39.7 to 46.0) | 41.3 (38.5 to 42.9) | oMLX main 624cff0e |
| Qwen3.8 Flash Next full | temperature 0.7, top-p 0.8, top-k 20 | `6542a7f95175` | 33.2 (31.5 to 34.6) | 34.9 (32.2 to 35.9) | oMLX 0.7.3 |
| GLM-5.3 4-bit | temperature 1.0, top-p 0.95 | `2641f174f97a` | 24.5 (24.5 to 24.5) | 24.3 (24.2 to 24.3) | oMLX 0.7.3 |

- **I see no version change here.** Each pair is one start against one start, and three of the four ranges overlap. The older lines are in [finding 2](../02_ten_models_4k_to_1m).
- **GLM-5.3 moved by 0.2 tok/s.** Its five runs sit within 0.1 of each other on both releases, so the ranges do not overlap, and the gap is under 1%.

## GLM-5.3 4-bit, with and without a draft head

ELI5: The 4-bit build on Hugging Face leaves out the model's draft layer. Another repository has that one layer on its own. I joined the two on this Mac to see if drafts make it faster. On this build and release they did not.

- **This second build is not a download.** It is [mlx-community/GLM-5.3-4bit](https://huggingface.co/mlx-community/GLM-5.3-4bit) with the draft head of [inferencerlabs/GLM-5.3-MTP-MLX](https://huggingface.co/inferencerlabs/GLM-5.3-MTP-MLX) joined on this Mac. The steps are under "The setup" and the script is in this folder.

Tok/s, the middle of 5 runs.

| Test | No drafts, `2641f174f97a` | Draft head joined here, `1cdf9099760b` |
|---|---|---|
| Greedy, code, 512-token replies, 4K | 24.6 (24.5 to 24.7) | 23.4 (22.2 to 24.4) |
| Greedy, code, 512-token replies, 16K | 24.4 (24.3 to 24.4) | 22.4 (22.2 to 23.1) |
| Greedy, code, 128-token replies, 4K | 24.5 (24.5 to 24.6) | 24.9 (21.9 to 27.4) |
| Greedy, code, 128-token replies, 16K | 24.4 (24.2 to 24.4) | 21.8 (19.2 to 22.9) |
| Greedy, code, 128-token replies, 110K | 21.8 (21.6 to 22.0) | one run, 19.5 |
| Own sampler, mixed, 512-token replies, 4K | 24.5 (24.5 to 24.5) | 25.0 (23.0 to 29.0) |

- **The joined head was not faster on greedy code.** 23.4 against 24.6 at 4K, which is 23.4 / 24.6 = 0.95 times. On sampled text it wrote 25.0 against 24.5, inside its own range of 23.0 to 29.0.
- **The drafts were kept less than twice a cycle.** oMLX's log gives the tokens kept per draft cycle. The middle value over this start's requests was 1.83, and no request drafted deeper than 3.
- **No answer check. Correction, 21 Nov 2026 11:08 SGT.** This page said 250 of 250 short greedy answers match between the two builds. Every one of those replies was reasoning text with an empty answer, and the check compares answer text only. So it compared empty strings and proved nothing.
- **Reading 110K tokens took over 4 minutes.** The first token came after 257 s (245 to 288) on the no-drafts start. The prompts came to about 105,750 tokens.
- **The 110K cell of the joined build has 1 run, not 5.** I stopped the job when free disk reached my floor of 300 GiB. oMLX's prompt cache folder had grown to 120 GiB over the two starts, at the settings I used. I had set no limit on it.
- **Every reply was reasoning text.** The model's chat template ignores the thinking switch.
- **No long-reply, copy or counting blocks ran on GLM-5.3.**

## The easy-text questions

ELI5: Findings 5 to 8 also ask the model to copy the prompt and to count from 1, because drafts guess that text almost every time. On two of these models the reply was mostly reasoning, so those rows are not copy or counting speeds.

Greedy at temperature 0, 512-token replies, default depth, tok/s, with the average reasoning and answer tokens per reply at the 1K prompt.

| Model | Run | Asked to copy, 1K | Asked to copy, 4K | Reply to copy | Asked to count, 1K | Asked to count, 4K | Reply to count |
|---|---|---|---|---|---|---|---|
| GLM-5.3 Flash 4-bit | `8f12a00bcc4f` | 127.3 (77.3 to 136.0) | 102.4 (76.2 to 116.1) | 513 reasoning, 0 answer | 97.6 (93.9 to 100.5) | 97.9 (94.3 to 99.4) | 90 reasoning, 421 answer |
| Inkling 2 Small | `818c28dbb625` | 57.6 (36.7 to 63.5) | 48.4 (46.6 to 60.8) | 510 reasoning, 2 answer | 82.8 (78.2 to 83.5) | 83.3 (82.7 to 85.4) | 510 reasoning, 2 answer |
| Qwen3.8 Flash Next full | `6542a7f95175` | 120.1 (115.1 to 132.3) | 116.9 (98.2 to 125.2) | 0 reasoning, 512 answer | 49.5 (47.6 to 51.8) | 51.5 (51.1 to 52.6) | 0 reasoning, 512 answer |

- **I read one copy reply and one counting reply back per model**, on a fresh default start of each on 21 Nov 2026. Greedy, the 1K prompt, 512 tokens, each request naming its model. The first job's read-backs had gone to the wrong model, because oMLX lists every build in the models folder and my script asked for the first one listed.
  - **Qwen3.8 Flash Next.** The copy reply was 56 lines, and all 56 are in the prompt word for word. The counting reply was 155 lines, each the next number. No reasoning text in either.
  - **GLM-5.3 Flash.** The copy reply was reasoning text only, with no answer inside 512 tokens. 48 of its 58 reasoning lines are in the prompt word for word. The counting reply reasoned briefly, then wrote 233 lines, each the next number.
  - **Inkling 2 Small.** Both replies were reasoning text only, with no answer inside 512 tokens. 44 of the 46 reasoning lines of the copy reply are in the prompt word for word.
- **So only the Flash Next rows are on the summary page as copy and counting speeds.** The other two models' rows stay in `rows.csv` under the contents `code_echo` and `code_count`.
- **Fixed depth 4 on these questions.** Qwen3.8 Flash Next counted at 58.0 and 60.7 against 49.5 and 51.5, faster on 10 of 10 texts with a middle ratio of 1.17. Its copy speed was level at 119.5 and 122.5. Inkling 2 Small was slower on the counting question at 69.8 and 71.7 against 82.8 and 83.3, slower on 10 of 10. GLM-5.3 Flash wrote 105.9 and 97.9 when asked to copy, against 127.3 and 102.4, and 96.5 and 93.2 when asked to count, against 97.6 and 97.9. Each has a middle ratio of 0.97.

## Reference points

ELI5: Apple's own server is my usual baseline. It can't load three of these four model types, so there is no baseline bar here.

- **`mlx-lm` 0.32.2 did not load GLM-5.3 4-bit** when I tried it on 15 Nov 2026. That try has no rows in this repository.
- **`mlx-lm` 0.32.2 does not load the `qwen4_exp` model type** of Qwen3.8 Flash Next. [Finding 7](../07_qwen38_tensorfold_130) has the error line, on the 4-bit build.
- **I did not try `mlx-lm` on GLM-5.3 Flash or Inkling 2 Small for this finding.**
- **Qwen3.8 Flash Next on other weights.** TensorFold 1.3.2 wrote 219.4 tok/s at its max on the 4-bit build and 199.8 on the 6-bit build, in [finding 11](../11_qwen38_tensorfold_132). Those are quantized weights on a different engine. This finding is the full BF16 release.

## The setup

ELI5: One engine at one release. A fresh server start for every setting.

- **Engine.** [oMLX](https://github.com/jundot/omlx) 0.8.0, the release of 18 Nov 2026, installed from the tagged source with its custom kernels built (`OMLX_WITH_CUSTOM_KERNEL=1`).
- **Serve command.**

```bash
omlx serve --model-dir <models> --host 127.0.0.1 --port 8180 --max-concurrent-requests 1 --headless --no-hf-cache --base-path <home>
```

- **Weights.**
  - [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) @ 9e5c75a9.
  - [mlx-community/Inkling-2-Small-oQ4e](https://huggingface.co/mlx-community/Inkling-2-Small-oQ4e) @ 973d9f96.
  - [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) @ 812d96e1, the maker's BF16 files.
  - [mlx-community/GLM-5.3-4bit](https://huggingface.co/mlx-community/GLM-5.3-4bit) @ 81ad9b73.
  - [inferencerlabs/GLM-5.3-MTP-MLX](https://huggingface.co/inferencerlabs/GLM-5.3-MTP-MLX) @ f1187efe, the draft head only.
- **Model settings**, in oMLX's own `model_settings.json`. `mtp_enabled` true, `a8_prefill_enabled` false, `activation_fp16_enabled` false. On the GLM-5.3 start without drafts `mtp_enabled` was false.
- **Fixed depth.** `mtp_fixed_depth` set to 4, 5 or 6 in the model's entry. Unset is the default.
- **Burst decode.** `server.burst_decode_mode` at `balanced`, the default.
- **Thinking** switched off in every request. Three of the models wrote reasoning text anyway.
- **Joining the GLM-5.3 draft head.** `make_glm53_mtp_build.py` in this folder, standard-library Python.
  - It hard-links the weight files of the 4-bit build into a new folder.
  - It writes the head's tensors into one new file under the names oMLX reads, `mtp.0.*`. The tensor bytes are unchanged and checked by SHA-256.
  - It joins the head's `gate_proj` and `up_proj` tensors into `gate_up_proj`, as oMLX's loader does for the trunk.
  - It sets `num_nextn_predict_layers` to 1 in `config.json`.

```bash
python3 make_glm53_mtp_build.py <GLM-5.3-4bit folder> <GLM-5.3-MTP-MLX folder> <new folder>
```

| Run id | Model | Setting | Started, SGT |
|---|---|---|---|
| `2641f174f97a` | GLM-5.3 4-bit | No drafts | 20 Nov, 23:30 |
| `1cdf9099760b` | GLM-5.3 4-bit with the draft head joined here | Drafts on, default depth | 21 Nov, 00:23 |
| `8f12a00bcc4f` | GLM-5.3 Flash 4-bit | Drafts on, default depth | 21 Nov, 01:16 |
| `818c28dbb625` | Inkling 2 Small | Drafts on, default depth | 21 Nov, 01:33 |
| `c624f11aa341` | Inkling 2 Small | Drafts on, fixed depth 4 | 21 Nov, 01:58 |
| `6542a7f95175` | Qwen3.8 Flash Next full | Drafts on, default depth | 21 Nov, 02:21 |
| `601378891241` | Qwen3.8 Flash Next full | Drafts on, fixed depth 4 | 21 Nov, 02:46 |
| `605e0068ff28` | GLM-5.3 Flash 4-bit | Drafts on, fixed depth 4 | 21 Nov, 08:00 |
| `df87c103a0f9` | GLM-5.3 Flash 4-bit | Drafts on, fixed depth 5 | 21 Nov, 08:15 |
| `57b0f4425846` | Qwen3.8 Flash Next full | Drafts on, default depth, second start | 21 Nov, 08:24 |
| `5f6db4faf823` | Qwen3.8 Flash Next full | Drafts on, fixed depth 4, second start | 21 Nov, 08:34 |
| `0350d62ae1e8` | Qwen3.8 Flash Next full | Drafts on, fixed depth 5 | 21 Nov, 08:45 |
| `1898791c30eb` | Qwen3.8 Flash Next full | Drafts on, fixed depth 6 | 21 Nov, 08:54 |

## How I measured

ELI5: Same Mac, same harness and same text rules as findings 3 to 8.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test, as in finding 2. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes** are targets at 3.5 characters per token. A "1K" prompt came to about 840 tokens on GLM-5.3 Flash, 960 on Qwen3.8 Flash Next and 1,150 on Inkling 2 Small. A "4K" prompt came to about 3,920, 4,450 and 5,330.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first reply token to the last, reasoning tokens included.
- **The questions** are the three of [finding 5](../05_dsv41_omlx_080_max_push), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Reasoning text is not answer text.** Three of these models spent the reply thinking. A benchmark that counts only answer tokens will show other numbers.
- **Max is not what a chat feels like.** The median column is the everyday figure.
- **One start per setting, two for the Flash Next default and depth 4.** Finding 3 measured 7% between two starts of one setting on this engine.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 451 raw rows from the bench database. 406 timed requests and 45 warm-ups.
- **`runs.csv`.** The 13 runs behind them, with engine, version, start time, settings and sampling.
- **`make_glm53_mtp_build.py`.** The script that joined the GLM-5.3 draft head.

From the top of this repository.

```bash
python3 tools/summarize.py findings/09_omlx_080_four_models
```

## What I did not verify

- **More than one copy and one counting reply per model.** I read back one of each.
- **A second start** of any setting but the Flash Next default and depth 4.
- **The model's own sampler at a fixed depth** on GLM-5.3 Flash and Inkling 2 Small.
- **The answer check and the own sampler at depths 5 and 6** on Flash Next.
- **Whether a fixed depth or the joined draft head changes the reasoning text** on GLM-5.3 Flash, Inkling 2 Small or GLM-5.3. The answer check saw only empty answers there.
- **Long replies, copy and counting on GLM-5.3 4-bit**, and the 110K block on the joined build.
- **Whether oMLX has a setting that caps the prompt cache folder.** I did not look.
- **Answer quality** of any build here.
- **Peak memory.** These runs did not log it.
- **Thinking on**, as a setting.
- **GLM-5.3 Flash 6-bit on oMLX 0.8.0.** Its line on the summary page is still from 0.7.3.

## Credit

- **Engine.** [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim).
- **Weights.** The oQ4e builds by Jundot and [mlx-community](https://huggingface.co/mlx-community). GLM-5.3 4-bit by mlx-community. The GLM-5.3 draft head by [inferencerlabs](https://huggingface.co/inferencerlabs).
- **Models.** GLM-5.3 and GLM-5.3 Flash by Z.ai. Inkling 2 Small by Thinking Machines. Qwen3.8 Flash Next by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
