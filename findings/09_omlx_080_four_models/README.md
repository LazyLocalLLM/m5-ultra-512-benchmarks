# Finding 9. Four more models on oMLX 0.8.0, max and median speed

ELI5: My older lines for these four models came from oMLX 0.7.3 or from an unreleased commit. I reran them on oMLX 0.8.0, the latest stable release. Each model gets two figures. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**On oMLX 0.8.0, GLM-5.3 Flash 4-bit wrote 80.2 tok/s at its max and 67.8 with its own sampler. Inkling 2 Small wrote 51.6 and 42.2. Qwen3.8 Flash Next at full precision wrote 49.3 and 33.2 at the default draft depth, and 53.3 on new code with the draft depth fixed at 4. GLM-5.3 4-bit wrote 24.6 and 24.5 with no drafts.**

Runs of 20 and 21 Nov 2026 SGT. One server start per setting unless a line says otherwise.

| Model | Build | Max, tok/s | Median, tok/s |
|---|---|---|---|
| GLM-5.3 Flash | 4-bit, oQ4e-mtp | 80.2 | 67.8 |
| Inkling 2 Small | 4-bit, oQ4e | 51.6 | 42.2 |
| Qwen3.8 Flash Next | full, BF16 | 49.3 at the default depth, 53.3 at fixed depth 4 | 33.2 |
| GLM-5.3 | 4-bit | 24.6 | 24.5 |

- **Max** is the middle of 5 greedy runs on new code. Replies of up to 2,048 tokens at a 1K prompt for the first three models. 512-token replies at a 4K prompt for GLM-5.3, which ran no longer replies.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **Three of the four wrote reasoning text.** GLM-5.3, GLM-5.3 Flash and Inkling 2 Small think even when the request switches thinking off. Their speeds count every token written, reasoning included.

## Chart

ELI5: The top speed on new code for the three models that ran long replies. One bar per model and prompt size.

![Bars of writing speed in tokens per second on oMLX 0.8.0, greedy at temperature 0, new code, replies of up to 2,048 tokens. GLM-5.3 Flash 4-bit 80.2 at a 1K prompt and 74.7 at 4K. Inkling 2 Small 51.6 and 48.6. Qwen3.8 Flash Next full at the default depth 49.3 and 48.9.](chart_max.png)

## Max speed, writing new code

ELI5: The model reads a block of code and is asked to write a new module with tests. Nothing in the reply can be copied from the prompt. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Greedy at temperature 0, code, replies of up to 2,048 tokens, tok/s.

| Model | Draft setting | Run | 1K prompt | 4K prompt |
|---|---|---|---|---|
| GLM-5.3 Flash 4-bit | Default depth | `8f12a00bcc4f` | 80.2 (68.4 to 87.6) | 74.7 (68.9 to 81.3) |
| Inkling 2 Small | Default depth | `818c28dbb625` | 51.6 (46.9 to 51.9) | 48.6 (46.0 to 58.7) |
| Inkling 2 Small | Fixed depth 4 | `c624f11aa341` | 51.8 (48.1 to 54.6) | 50.4 (43.6 to 53.6) |
| Qwen3.8 Flash Next full | Default depth | `6542a7f95175` | 49.3 (44.1 to 51.9) | 48.9 (41.9 to 51.7) |
| Qwen3.8 Flash Next full | Fixed depth 4 | `601378891241` | 53.3 (48.7 to 56.2) | 52.7 (49.2 to 59.1) |

Greedy at temperature 0, code, 512-token replies, tok/s.

| Model | Draft setting | Run | 1K prompt | 4K prompt |
|---|---|---|---|---|
| GLM-5.3 Flash 4-bit | Default depth | `8f12a00bcc4f` | 75.8 (70.4 to 78.5) | 69.8 (64.9 to 75.0) |
| Inkling 2 Small | Default depth | `818c28dbb625` | 49.2 (47.0 to 55.3) | 44.8 (44.5 to 47.2) |
| Inkling 2 Small | Fixed depth 4 | `c624f11aa341` | 47.4 (44.4 to 53.0) | 45.0 (43.0 to 49.6) |
| Qwen3.8 Flash Next full | Default depth | `6542a7f95175` | 44.0 (41.2 to 47.9) | 46.9 (38.2 to 48.6) |
| Qwen3.8 Flash Next full | Fixed depth 4 | `601378891241` | 47.2 (44.7 to 52.4) | 51.9 (43.0 to 54.5) |

- **What the replies were.** Qwen3.8 Flash Next wrote answer text only. GLM-5.3 Flash wrote reasoning text only, 2,048 of 2,048 tokens. Inkling 2 Small wrote mostly reasoning, about 1,930 of 2,048 tokens on average. So for those two the max is a reasoning speed on a code task.
- **Longer replies wrote a little faster**, as in findings 5 to 8. GLM-5.3 Flash went from 75.8 to 80.2 at 1K. That is 80.2 / 75.8 = 1.06 times.
- **Some Flash Next replies ended before the cap.** 3 of 5 ran to 2,048 tokens in each default-depth cell. The shortest was 1,701 tokens.

## Draft depth

ELI5: These builds carry a small draft head that guesses a few tokens ahead, and the model checks the guesses. The depth is how many tokens it guesses at once. I tried one fixed depth of 4 on two of the models.

- **Qwen3.8 Flash Next full gained at fixed depth 4.** 53.3 against 49.3 at 1K, which is 53.3 / 49.3 = 1.08 times. Text by text it was faster on 10 of 10 long replies, with a middle ratio of 1.10. With 512-token replies it was faster on 9 of 10.
- **The log agrees.** At the default the deepest draft on every request was 3 tokens. At the fixed setting it was 4 on every request.
- **One start each.** The ranges in the tables overlap. I did not run the model's own sampler at fixed depth 4, so I can't say what it does to the median. On DeepSeek V4.1 Flash in finding 5 a fixed depth raised the max and lowered the median.
- **Inkling 2 Small was level on code.** 51.8 against 51.6 at 1K, faster on 6 of 10 texts with a middle ratio of 1.01. Its default is already deeper. The log shows its draft loaded at depth 7, adaptive, and at depth 4, not adaptive, on the fixed start.
- **GLM-5.3 Flash at fixed depth 4 did not run.** My harness checks the listening ports before each start, and that check timed out after 5 seconds. The server was never started. That is my tool and says nothing about oMLX.
- **Same answers.** On 250 short greedy questions, fixed depth 4 gave the default's answer on 250 of 250 for Inkling 2 Small and on 250 of 250 for Qwen3.8 Flash Next.

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
- **Same answers.** 250 of 250 short greedy answers match between the two builds.
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

- **I have not read these replies back.** My read-back requests in this job went to the wrong model. oMLX lists every build in the models folder, and my script asked for the first one listed. So I can't yet say that any of these replies is a true copy or a true count.
- **None of these rows is on the summary page as a copy or counting speed.** The rows are in `rows.csv` under the contents `code_echo` and `code_count`.
- **Fixed depth 4 on these questions.** Qwen3.8 Flash Next counted at 58.0 and 60.7 against 49.5 and 51.5, faster on 10 of 10 texts with a middle ratio of 1.17. Its copy speed was level at 119.5 and 122.5. Inkling 2 Small was slower on the counting question at 69.8 and 71.7 against 82.8 and 83.3, slower on 10 of 10.

## Reference points

ELI5: Apple's own server is my usual baseline. It can't load three of these four model types, so there is no baseline bar here.

- **`mlx-lm` 0.32.2 did not load GLM-5.3 4-bit** when I tried it on 15 Nov 2026. That try has no rows in this repository.
- **`mlx-lm` 0.32.2 does not load the `qwen4_exp` model type** of Qwen3.8 Flash Next. [Finding 7](../07_qwen38_tensorfold_130) has the error line, on the 4-bit build.
- **I did not try `mlx-lm` on GLM-5.3 Flash or Inkling 2 Small for this finding.**
- **Qwen3.8 Flash Next on other weights.** TensorFold 1.3.0 wrote 204.4 tok/s at its max on the 4-bit build and 193.0 on the 6-bit build, in finding 7. Those are quantized weights on a different engine. This finding is the full BF16 release.

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
- **Fixed depth 4.** `mtp_fixed_depth` set to 4 in the model's entry. Unset is the default.
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
- **One start per setting.** Finding 3 measured 7% between two starts of one setting on this engine.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 302 raw rows from the bench database. The timed requests and the warm-ups.
- **`runs.csv`.** The 7 runs behind them, with engine, version, start time, settings and sampling.
- **`make_glm53_mtp_build.py`.** The script that joined the GLM-5.3 draft head.

From the top of this repository.

```bash
python3 tools/summarize.py findings/09_omlx_080_four_models
```

## What I did not verify

- **What the copy and counting replies say.** The read-backs went to the wrong model and are being rerun.
- **GLM-5.3 Flash at any fixed depth.** That start did not run.
- **A second start** of any setting here.
- **The model's own sampler at fixed depth 4.**
- **Depths other than 4.**
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
