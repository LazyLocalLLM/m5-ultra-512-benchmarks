# Finding 7. Qwen3.8 27B and Flash Next on TensorFold 1.3.0, pushing the max

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold 1.3.0 came out on 20 Nov 2026. I ran the two Qwen builds it serves on this Mac the same day, asked three different things of each, and tried a few draft switches. For the 27B model I also ran Apple's own `mlx-lm` on the same weights, so there is a baseline to hold it against.

**TensorFold 1.3.0 wrote 331.3 tok/s on Qwen3.8 27B 4-bit while writing new code, greedy at temperature 0, with its DFlash2 drafter and replies of up to 2,048 tokens at a 1K prompt. `mlx-lm` 0.32.2 wrote 45.1 on the same weights and the same test, so TensorFold is 7.3 times `mlx-lm`. With the model's own sampler on mixed text at 4K it wrote 148.2 against 43.6, which is 3.4 times. Copying code out of the prompt it wrote 824.0 tok/s with 2,048-token replies. Qwen3.8 Flash Next 4-bit wrote 204.4 on new code, 126.7 sampled and 292.2 on the same copy task. One server start per setting. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 20 Nov 2026.**

## Chart

ELI5: Qwen3.8 27B on the same weights. Grey is Apple's `mlx-lm` writing new code. Dark blue is TensorFold on the same task. Light blue is TensorFold copying the prompt, which is a ceiling and not real work.

![Horizontal bars of writing speed in tokens per second for Qwen3.8 27B 4-bit, greedy at temperature 0. At a 1K prompt, mlx-lm 0.32.2 writes 45.1 on new code, TensorFold 1.3.0 writes 331.3 on new code and 841.0 copying the prompt. At a 4K prompt, 44.2, 250.8 and 659.1.](chart_27b.png)

## Qwen3.8 27B 4-bit

ELI5: A 27B dense model with a small draft model, DFlash2, that guesses several tokens ahead. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s, defaults, run `f2d856e22771` on TensorFold and `0c5446c7acc1` on `mlx-lm`.

| Test | Prompt | `mlx-lm` 0.32.2 | TensorFold 1.3.0 | Times `mlx-lm` |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 45.1 (45.0 to 45.2) | 331.3 (245.7 to 342.1) | 7.3 |
| Greedy, new code, replies up to 2,048 tokens | 4K | 44.2 (44.1 to 44.4) | 250.8 (217.1 to 332.2) | 5.7 |
| Greedy, new code, 512-token replies | 1K | 45.2 (45.1 to 45.3) | 227.0 (222.2 to 278.6) | 5.0 |
| Greedy, new code, 512-token replies | 4K | 44.3 (44.0 to 44.8) | 206.2 (166.0 to 266.6) | 4.7 |
| Own sampler, mixed text, 512-token replies | 4K | 43.6 (43.6 to 43.7) | 148.2 (128.2 to 178.6) | 3.4 |

- **Max.** 331.3 tok/s, greedy on new code with replies of up to 2,048 tokens at 1K. 331.3 / 45.1 = 7.3 times `mlx-lm`.
- **Median.** 148.2 tok/s with the model's own sampler on mixed text at 4K. 148.2 / 43.6 = 3.4 times `mlx-lm`.
- **Longer replies wrote faster on TensorFold.** 331.3 against 227.0 at 1K, which is 331.3 / 227.0 = 1.46 times. `mlx-lm` wrote the same speed at both lengths.
- **The runs spread widely.** The 2,048-token cell at 1K goes from 245.7 to 342.1. Drafted speed depends on how well the drafter guesses each text. The four switch starts below wrote 320.9 to 327.8 in the same cell, so the 331.3 is not a lucky start.
- **7 of the 10 long replies ran to 2,048 tokens.** The model ended the other 3 itself, the shortest at 1,592 tokens.
- **Both engines got the same sampler**, temperature 0.7, top-p 0.8 and top-k 20. No presence penalty was applied on either.

### Ceiling on easy text

ELI5: Two tests where the drafts guess almost every token. In one the model repeats the prompt's code. In the other it counts 1, 2, 3. The speed is far above real work, so I keep these apart from the max.

Greedy at temperature 0, TensorFold 1.3.0 at defaults, tok/s.

| Test | Run | 1K prompt | 4K prompt |
|---|---|---|---|
| Copy the prompt, 512-token replies | `f2d856e22771` | 841.0 (755.4 to 881.3) | 659.1 (504.4 to 693.2) |
| Copy the prompt, 2,048-token replies | `44a8ff4a173a` | not run | 824.0 (734.9 to 832.0) |
| Count from 1, 512-token replies | `f2d856e22771` | 450.8 (169.0 to 454.8) | 427.6 (422.5 to 444.6) |

- **Copying is 2.5 times the max.** With 2,048-token replies, 824.0 / 331.3 = 2.49 times. The 824.0 is the figure I quote, for the reason in the next line.
- **Why I ran the long copy block.** A 512-token copy arrives in about 13 pieces of about 39 tokens. The clock starts at the first piece, so its tokens are not timed. If one average piece is taken off, 841.0 becomes about 778. With 2,048-token replies that share is under 2%, and the figure is 824.0.
- **The copy speed comes from copied rows.** With `TF_Q27_COPY_ROWS=0`, which the environment guide says disables copied rows, the copy task fell to 513.6 at 1K and 278.3 at 4K. New code and counting did not move.
- **One counting reply ended early.** At 1K one of the five stopped by itself at 156 tokens and wrote 169.0 tok/s. The other four ran to 512 tokens.
- **I checked what the model wrote.** One extra copy request returned 56 lines, and 55 are in the prompt word for word. One extra counting request returned 155 lines, each the next number. Neither is in `rows.csv`.

### Four switches, none faster

ELI5: I started the server once with each of four documented draft settings and ran the same tests. Each cell is the middle of 5 runs at a 1K and a 4K prompt.

| Setting | Run | New code, 512 | New code, up to 2,048 | Copy, 512 | Counting, 512 |
|---|---|---|---|---|---|
| Defaults | `f2d856e22771` | 227.0 and 206.2 | 331.3 and 250.8 | 841.0 and 659.1 | 450.8 and 427.6 |
| `TF_MTP_DRAFTS=8` | `d2c3ae991994` | 241.0 and 206.1 | 325.2 and 239.6 | 844.6 and 659.3 | 443.3 and 434.5 |
| `TF_MTP_DRAFTS=15` | `09602ed68067` | 243.4 and 242.8 | 322.4 and 256.7 | 842.4 and 638.0 | 451.6 and 425.3 |
| `TF_Q27_COPY_ROWS=0` | `9aa3726e1140` | 246.8 and 214.1 | 320.9 and 266.4 | 513.6 and 278.3 | 452.3 and 427.9 |
| `TF_Q27_COPY_ROWS=96` | `7964339f0ee4` | 234.0 and 222.1 | 327.8 and 221.2 | 844.8 and 662.2 | 443.6 and 434.9 |

- **No setting beat the defaults.** Text by text against the defaults start, the middle ratio of every setting on every test is between 0.98 and 1.06, except the copy task with copied rows off at 0.56.
- **One start each**, so differences of a few percent between rows mean nothing.
- **Each variable was in the server's process environment.** Only `TF_Q27_COPY_ROWS=0` shows an effect I can point to. For the others I can't confirm from the log that the setting applied.

### Against 1.2.8

ELI5: The 1.3.0 notes list a change to how Qwen3.8 27B runs its drafted rounds on M5 Macs, with the same tokens. I had the same five settings on 1.2.8 from an hour earlier, so I compared them.

| Test | Same-text pairs | 1.3.0 faster | Middle ratio, 1.3.0 over 1.2.8 |
|---|---|---|---|
| New code, 512-token replies | 50 | 24 | 1.00 |
| New code, replies up to 2,048 tokens | 50 | 26 | 1.00 |
| Copy, 512-token replies | 50 | 16 | 1.00 |
| Counting, 512-token replies | 50 | 22 | 1.00 |

- **The two versions wrote at the same speed here.** 200 same-text pairs across five settings, middle ratio 1.00 on every test.
- **Same answers.** The two defaults starts gave the same 250 greedy answers, 250 of 250 by hash.
- **The sampled test is level too.** 143.3 tok/s on 1.2.8 in run `83b6db5a6d68` and 148.2 on 1.3.0, on the same evening with overlapping ranges. Finding 2 measured 154.2 on 1.2.8 on 17 Nov 2026, from another day's start. So the lower figure today is start to start spread and not the new version.
- **One order only.** All five 1.2.8 starts ran from 19:32 SGT, before the upgrade. All five 1.3.0 starts ran from 20:05 SGT.
- **The 1.2.8 run was stopped in its fifth arm**, when I moved to 1.3.0. Its speed rows are complete and are in `rows.csv`. Its fifth arm has no answer-test rows.

## Qwen3.8 Flash Next 4-bit

ELI5: A larger mixture-of-experts model with its own draft head. TensorFold's recipe has a serve line for the M5 Ultra, and I used it.

Decode tok/s, TensorFold 1.3.0 at defaults, run `7bf80be3a997`.

| Test | 1K prompt | 4K prompt |
|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 204.4 (176.6 to 247.5) | 195.2 (162.2 to 207.2) |
| Greedy, new code, 512-token replies | 174.1 (151.6 to 229.8) | 194.4 (169.7 to 217.0) |
| Own sampler, mixed text, 512-token replies | not run | 126.7 (115.9 to 131.9) |
| Copy the prompt, 512-token replies | 298.1 (247.3 to 330.5) | 296.8 (222.3 to 383.2) |
| Copy the prompt, 2,048-token replies, run `37a4c93bd874` | not run | 292.2 (261.8 to 320.0) |
| Count from 1, 512-token replies | 344.7 (336.2 to 344.9) | 335.0 (329.4 to 335.7) |

- **Max.** 204.4 tok/s, greedy on new code with replies of up to 2,048 tokens at 1K.
- **Median.** 126.7 tok/s with the model's own sampler on mixed text at 4K.
- **No `mlx-lm` baseline for this model.** `mlx-lm` 0.32.2 did not load the build. Its log reads "ValueError: Model type qwen4_exp not supported." So no multiple of `mlx-lm` can be given.
- **Counting beat copying here**, 344.7 against 298.1. On the 27B model it was the other way round.
- **8 of the 10 long replies ran to 2,048 tokens.** The other 2 ended at 1,740 and 1,843.
- **Replies checked.** One extra copy request returned 56 lines, all 56 in the prompt word for word. One extra counting request returned 155 lines in order.

Three draft settings, one start each, tok/s at 1K and 4K.

| Setting | Run | New code, 512 | New code, up to 2,048 | Copy, 512 | Counting, 512 |
|---|---|---|---|---|---|
| Defaults | `7bf80be3a997` | 174.1 and 194.4 | 204.4 and 195.2 | 298.1 and 296.8 | 344.7 and 335.0 |
| `TF_FLASHNEXT_DRAFTS_GREEDY=12` | `e89d1354bd1b` | 174.0 and 177.7 | 195.8 and 195.4 | 299.6 and 305.6 | 345.6 and 336.4 |
| `TF_FLASHNEXT_DRAFTS_GREEDY=15` | `c097b7bf5f73` | 170.1 and 174.5 | 193.3 and 193.5 | 327.8 and 301.0 | 345.3 and 336.0 |
| `TF_FLASHNEXT_DRAFTS_GREEDY=15`, `TF_FLASHNEXT_GREEDY_WIDE=8` | `4b503ee09910` | 177.9 and 175.7 | 195.0 and 206.3 | 326.8 and 304.6 | 344.2 and 334.9 |

- **No setting beat the defaults.** Text by text, the middle ratios are between 0.95 and 1.05. The default greedy draft count is 8.
- **I can't confirm from the log that these settings applied.** Each variable was in the server's process environment.

## Qwen3.8 Flash Next 6-bit

ELI5: The same model with 6-bit weights, which keep more precision than the 4-bit build and cost some speed. Added 21 Nov 2026 01:07 SGT.

Decode tok/s, TensorFold 1.3.0 at defaults, run `2bc45b1272e8`, started 21 Nov 2026 00:59 SGT.

| Test | 1K prompt | 4K prompt |
|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 193.0 (178.5 to 212.3) | 191.4 (171.1 to 207.8) |
| Greedy, new code, 512-token replies | 188.2 (177.9 to 192.6) | 184.9 (151.6 to 195.6) |
| Own sampler, mixed text, 512-token replies | not run | 117.4 (112.0 to 122.0) |
| Copy the prompt, 512-token replies | 254.4 (208.5 to 276.9) | 251.1 (195.8 to 323.1) |
| Copy the prompt, 2,048-token replies | not run | 247.7 (223.1 to 268.9) |
| Count from 1, 512-token replies | 290.0 (283.9 to 290.3) | 283.0 (282.1 to 284.7) |

- **Max.** 193.0 tok/s, greedy on new code with replies of up to 2,048 tokens at 1K. The 4-bit build wrote 204.4 on the same test.
- **Median.** 117.4 tok/s with the model's own sampler on mixed text at 4K. The 4-bit build wrote 126.7.
- **So 6-bit costs about 6% to 7% here.** 193.0 / 204.4 = 0.94 times and 117.4 / 126.7 = 0.93 times, one start of each build.
- **7 of the 10 long replies ran to 2,048 tokens.**
- **Replies checked.** One extra copy request returned 56 lines, all 56 in the prompt word for word. One extra counting request returned 155 lines in order.
- **Weights.** [TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP), served with the same recipe line as the 4-bit build.

## The setup

ELI5: One engine at its newest release, two sets of weights, and the serve lines the project documents.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.0, released 20 Nov 2026 07:04 SGT, installed from the project's Homebrew tap. The formula's SHA-256 equals the digest GitHub lists for `tensorfold-1.3.0-macos-arm64.tar.gz`. `tensorfold-native --version` prints 1.3.0.
- **Baseline.** [`mlx-lm`](https://github.com/ml-explore/mlx-lm) 0.32.2 at its defaults, the newest release on 20 Nov 2026.
- **Weights, 27B.** [TensorFold/Qwen3.8-27B-MLX-4bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) with the drafter [z-lab/Qwen3.8-27B-DFlash2](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2). `mlx-lm` read the same model folder, with no drafter.
- **Weights, Flash Next.** [TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP).
- **Serve command, 27B.**

```bash
tensorfold serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 262144 --parallel 1 --drafter <DFlash2 folder>
```

- **Serve command, Flash Next**, the M5 Ultra line of `docs/recipes/qwen3.8-flash-next.md`. The recipe is unchanged for this Mac between 1.2.8 and 1.3.0.

```bash
tensorfold serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 1048576 --parallel 2 --vision --prompt-cache-gib 8 --temperature 0 --no-update-check
```

- **Switches.** Each one was set in the environment of one server start. All are in TensorFold's `docs/environment.md`.
- **Thinking** off.

| Run id | Model | Engine and setting | Started, SGT, 20 Nov 2026 |
|---|---|---|---|
| `f2d856e22771` | 27B | TensorFold 1.3.0, defaults | 20:05 |
| `d2c3ae991994` | 27B | TensorFold 1.3.0, `TF_MTP_DRAFTS=8` | 20:11 |
| `09602ed68067` | 27B | TensorFold 1.3.0, `TF_MTP_DRAFTS=15` | 20:16 |
| `9aa3726e1140` | 27B | TensorFold 1.3.0, `TF_Q27_COPY_ROWS=0` | 20:22 |
| `7964339f0ee4` | 27B | TensorFold 1.3.0, `TF_Q27_COPY_ROWS=96` | 20:27 |
| `44a8ff4a173a` | 27B | TensorFold 1.3.0, defaults, long copy block | 21:08 |
| `0c5446c7acc1` | 27B | `mlx-lm` 0.32.2, defaults | 21:10 |
| `7bf80be3a997` | Flash Next | TensorFold 1.3.0, defaults | 20:32 |
| `e89d1354bd1b` | Flash Next | TensorFold 1.3.0, `TF_FLASHNEXT_DRAFTS_GREEDY=12` | 20:39 |
| `c097b7bf5f73` | Flash Next | TensorFold 1.3.0, `TF_FLASHNEXT_DRAFTS_GREEDY=15` | 20:45 |
| `4b503ee09910` | Flash Next | TensorFold 1.3.0, greedy drafts 15 and wide 8 | 20:51 |
| `37a4c93bd874` | Flash Next | TensorFold 1.3.0, defaults, long copy block | 21:09 |
| `2bc45b1272e8` | Flash Next 6-bit | TensorFold 1.3.0, defaults | 00:59 on 21 Nov |
| `83b6db5a6d68` | 27B | TensorFold 1.2.8, defaults | 19:32 |
| `220f4546bd8e` | 27B | TensorFold 1.2.8, `TF_MTP_DRAFTS=8` | 19:38 |
| `9fb18e8990a7` | 27B | TensorFold 1.2.8, `TF_MTP_DRAFTS=15` | 19:43 |
| `ac7fdadfc232` | 27B | TensorFold 1.2.8, `TF_Q27_COPY_ROWS=0` | 19:48 |
| `a10e3c3d96dd` | 27B | TensorFold 1.2.8, `TF_Q27_COPY_ROWS=96` | 19:54 |

## How I measured

ELI5: Same Mac, same harness and same three questions as findings 5 and 6.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** means temperature 0.7, top-p 0.8 and top-k 20.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. The text of a request is picked from its size and repeat number, so every start got the same texts. Each prompt opens with a new session line so no prompt cache can hit. Timed requests show at most 3 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. The code prompts came to about 960 and 4,450 tokens on these models.
- **Three questions**, each placed after the code text.
  - **New code.** "Write a new Python module, with unit tests, that reimplements the most important function above in a cleaner way. Write it in full." In `rows.csv` the content is `code`.
  - **Copy.** "Repeat the text above exactly as written, starting from its first line after the Session line. Change nothing and add no commentary." The content is `code_echo`.
  - **Counting.** "Ignore the text above. Count from 1 to 400, one number per line, nothing else." The content is `code_count`.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last. Tokens in the first piece are not timed. That matters only where pieces are large, which here is the copy task.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 730 raw rows from the bench database. The 660 timed requests and the 70 warm-ups.
- **`runs.csv`.** The 18 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/07_qwen38_tensorfold_130
```

## What I did not verify

- **A second start of any setting.** Every row is one server start, apart from the two long copy blocks.
- **The reverse order for 1.3.0 against 1.2.8.**
- **Whether the draft-count settings took effect.**
- **Answer quality** of either build.
- **The full BF16 build of Flash Next** on 1.3.0.
- **Prompts longer than 4K** on these tests.
- **Two users at once.** Flash Next was served with two slots, as the recipe says, and tested with one user.
- **Peak memory.** These runs did not log it.
- **Thinking on.**

## Credit

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Drafter.** DFlash2 for Qwen3.8 27B by z-lab.
- **Baseline.** [`mlx-lm`](https://github.com/ml-explore/mlx-lm) by Apple's MLX team.
- **Models.** Qwen3.8 27B and Qwen3.8 Flash Next by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
