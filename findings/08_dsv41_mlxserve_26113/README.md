# Finding 8. DeepSeek V4.1 Flash on mlx-serve 26.11.3, pushing the max

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: mlx-serve 26.11.3 came out on 20 Nov 2026. I ran DeepSeek V4.1 Flash on it the same day, with the new warm-up flag its help recommends for benchmarks. I asked three different things of it on two server starts, and I tried one pinned draft depth.

**mlx-serve 26.11.3 wrote 93.8 and 95.3 tok/s on DeepSeek V4.1 Flash 1017 on two server starts while writing new code, greedy at temperature 0, at its defaults with replies of up to 2,048 tokens at a 4K prompt. With the model's own sampler on mixed text at 4K it wrote 57.5 and 56.4 tok/s. Copying code out of the prompt it wrote 167.0 tok/s, and counting from 1 it wrote 121.5. The defaults are not bit-exact. The server log says the output head is requantized to 8-bit. With the head kept dense it wrote 91.6 tok/s on the same code test and 57.9 sampled, on one start. Mac Studio M5 Ultra 512 GB, the ddalcu Lossless pack, one user, median of 5 runs, 20 and 21 Nov 2026.**

Updated 21 Nov 2026 03:50 SGT. Added one start with the output head kept dense, and one start of Qwen3.8 27B full without the warm-up flag.

## Chart

ELI5: One setup and three questions. Grey is the model writing something new. The two blues are text the drafts can guess almost every time.

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on mlx-serve 26.11.3 at its defaults, greedy at temperature 0. At a 1K prompt, 91.9 writing new code, 167.0 copying the prompt and 121.4 counting from 1. At a 4K prompt, 93.8, 162.3 and 121.5.](chart_tasks.png)

## Max and median

ELI5: Max is the best case, greedy on code the model has to write new. Median is the model's own sampler on mixed text, which is closer to daily use. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s. The first start is run `ddee83910540`. The second start, run `4d0f49b9ac43`, added `--no-decode-attn-quant`, which the log shows had nothing to act on with this pack.

| Test | Prompt | First start | Second start |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 91.9 (84.1 to 98.6) | 91.4 (83.6 to 98.6) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 93.8 (86.1 to 99.8) | 95.3 (90.1 to 100.3) |
| Greedy, new code, 512-token replies | 1K | 86.4 (75.2 to 95.6) | 93.2 (72.4 to 94.4) |
| Greedy, new code, 512-token replies | 4K | 84.0 (76.0 to 97.9) | 88.4 (75.0 to 88.8) |
| Own sampler, mixed text, 512-token replies | 4K | 57.5 (50.9 to 65.6) | 56.4 (52.6 to 61.4) |

- **Max.** 93.8 and 95.3 tok/s on the two starts, greedy on new code with replies of up to 2,048 tokens at 4K.
- **Median.** 57.5 and 56.4 tok/s, temperature 1.0 and top-p 1.0 on mixed text at 4K.
- **The two starts agree.** Text by text the middle ratio of the second over the first is 0.98 to 1.01 on every test.
- **The defaults are not bit-exact.** The log of both starts reads "lm head requantized to 8-bit (MLX_SERVE_DSV41_HEAD8=0 keeps it dense)". The section "The output head kept dense" below has one start with that switch set.
- **`--no-decode-attn-quant` changed nothing I can measure on this pack.** The help says that flag's default serves decode from requantized copies of dense attention weights and marks it LOSSY. On this pack the log prints no line for it on either start, where on the BF16 Qwen model below it prints "engaged". So I treat the second start as a repeat of the first.
- **The pack is named Lossless** because it keeps the precision DeepSeek ships. That name describes the weights and not how the engine decodes them by default.
- **Two starts did not give all the same short answers.** 246 of 250 greedy answers of 64 tokens match between them. Drafts are on in both.
- **Longer replies wrote a little faster.** On the first start, 93.8 against 84.0 at 4K. That is 93.8 / 84.0 = 1.12 times.
- **7 of the 20 long replies ran to 2,048 tokens.** The model ended the other 13 itself, the shortest at 1,114 tokens.
- **No pauses.** The longest gap between two streamed pieces in any of the 45 replies of the first start was 0.10 s.

## Ceiling on easy text

ELI5: Two tests where the drafts guess almost every token. In one the model repeats the prompt's code word for word. In the other it counts 1, 2, 3. The speed is far above real work, so I keep these apart from the max.

Greedy at temperature 0, 512-token replies, tok/s. Every reply ran to 512 tokens.

| Setup | Run | Copy, 1K | Copy, 4K | Counting, 1K | Counting, 4K |
|---|---|---|---|---|---|
| First start | `ddee83910540` | 167.0 (159.0 to 169.0) | 162.3 (116.6 to 166.2) | 121.4 (121.1 to 121.9) | 121.5 (121.3 to 121.9) |
| Second start | `4d0f49b9ac43` | 165.1 (159.5 to 170.1) | 160.4 (116.1 to 166.2) | 121.5 (121.2 to 121.9) | 121.5 (121.3 to 122.0) |
| Depth pinned at 5 | `31a7274d722a` | 164.1 (159.1 to 167.8) | 160.0 (113.7 to 165.9) | 121.7 (120.3 to 122.1) | 121.5 (121.4 to 122.2) |

- **Copying is about 1.8 times the max.** 167.0 / 93.8 = 1.78 times on the first start.
- **Prompt lookup drafts are on by default** in mlx-serve, and a copy task is their best case.
- **I checked what the model wrote.** One extra copy request returned 63 lines, all 63 in the prompt word for word. One extra counting request returned the numbers 1 to 256 in order. Neither is in `rows.csv`.

## One pinned draft depth, not faster

ELI5: mlx-serve picks its draft depth by itself, and its log shows depth 6 on this model. I pinned it at 5 to see whether that is faster.

Greedy at temperature 0, new code, tok/s at a 1K and a 4K prompt.

| Setup | Run | 512-token replies | Replies up to 2,048 tokens |
|---|---|---|---|
| Defaults, first start | `ddee83910540` | 86.4 and 84.0 | 91.9 and 93.8 |
| `--mtp-min-depth 5 --mtp-max-depth 5` | `31a7274d722a` | 87.2 and 85.1 | 90.1 and 90.7 |

- **The default is as fast as the pin.** Text by text the middle ratios are 1.02 and 0.99.
- **The pin took effect.** The log reads "mtp=enabled (streaming, depth=5)" on that start and "depth=6" on the other two.
- **248 of 250 short greedy answers match the first start.**

## The output head kept dense

ELI5: By default this release squeezes the model's last layer, the output head, to 8-bit. Its log names a switch that keeps the head as the pack ships it. I ran one start with that switch to see what it costs and whether the answers change.

Tok/s, the middle of 5 runs. The dense-head start is run `18b1cdba2631`, 21 Nov 2026 03:17 SGT. The default is the first start, run `ddee83910540`.

| Test | Prompt | Default, 8-bit head | Head kept dense |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 91.9 (84.1 to 98.6) | 90.2 (85.2 to 97.7) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 93.8 (86.1 to 99.8) | 91.6 (87.7 to 96.7) |
| Greedy, new code, 512-token replies | 1K | 86.4 (75.2 to 95.6) | 80.4 (65.1 to 85.7) |
| Greedy, new code, 512-token replies | 4K | 84.0 (76.0 to 97.9) | 85.2 (68.4 to 90.8) |
| Own sampler, mixed text, 512-token replies | 4K | 57.5 (50.9 to 65.6) | 57.9 (49.7 to 59.2) |

- **The switch took.** The log of this start reads "lm head dense, as shipped". The default starts read "lm head requantized to 8-bit".
- **The speed cost is small.** Text by text the middle ratio of dense over default is 0.98 on the long replies, 0.93 on the 512-token replies and 0.98 on the sampled test. That is one start against one start.
- **The short answers differ more.** 179 of 250 greedy answers of 64 tokens match the first default start, and 181 of 250 match the second. The two default starts match each other on 246 of 250.
- **This is not a bit-exact run.** I also set `MLX_SERVE_DSV41_EXACT=1`, a switch named in the binary and not in the docs. The log says that check "is proven only where every verify row takes the fused decode kernels (a NAX GPU)" and that it was "left off". So drafts were on and the exact check was off.
- **Which answers are right I can't say.** I have no plain-decode reference for this pack on this engine. I only show that the head setting changes about 28% of these short answers. 250 − 179 = 71, and 71 / 250 = 28%.
- **The start also passed `--warmup-full` and `--no-decode-attn-quant`.** The log prints no line for the second flag on this pack.

## Against 26.11.2

ELI5: Finding 2 ran the same pack on the release before. Only the sampled test is on both.

- **The median is level.** 57.5 tok/s on 26.11.3 against 58.3 on 26.11.2 on 17 Nov 2026, same test and same texts. The five same-text ratios run from 0.90 to 1.04.
- **Two things differ besides the version.** Today's starts had `--warmup-full`, and the runs are three days apart.

## Qwen3.8 27B full, BF16

ELI5: The same engine on the unquantized 27B model. It is slow on any engine here, so I ran only the short blocks.

Decode tok/s, defaults with `--warmup-full`, run `8594b4fe926a`.

| Test | Prompt | tok/s |
|---|---|---|
| Own sampler, mixed text, 512-token replies | 4K | 6.8 (6.8 to 6.9) |
| Greedy, new code, 512-token replies | 1K | 6.6 (6.5 to 10.1) |
| Greedy, new code, 512-token replies | 4K | 6.9 (6.5 to 7.4) |

- **Finding 2 measured 8.8 tok/s on the sampled test** on 17 Nov 2026 with mlx-serve 26.11.2. Today it is 6.8.
- **Without the warm-up flag it wrote 7.1 tok/s** (6.6 to 7.6) on the sampled test, run `5619fdacb103` on 21 Nov 2026 03:29 SGT at plain defaults. So the flag does not explain the gap to 8.8.
- **I would not read that as a version change yet.** It is one start on each version, three days apart, and today's start had `--warmup-full`. The 4-bit build showed a gap of the same kind today that turned out to be spread between starts.
- **The default decode here is lossy.** The log reads "[decode-attn-quant] engaged" and describes int8 side copies of the dense attention projections, used for decode only, with `--no-decode-attn-quant` to restore the dense weights. I did not run with that flag off on this model.
- **For speed on this model use the 4-bit build.** Finding 7 measured 148.2 tok/s on the same sampled test with TensorFold 1.3.0.

## Reference points

ELI5: Apple's own server does not load this model, so there is no baseline bar. The nearest rows are the same model in other files on other engines.

- **`mlx-lm` is not a baseline for DeepSeek V4.1 here.** Version 0.32.2 refused the MLX build on 13 Nov 2026, as finding 3 notes.
- **Finding 5, different weights and engine.** oMLX 0.8.0 on the oQ4e-mtp build wrote 86.2 tok/s on the same max test with draft depth fixed at 5, and 57.9 on the sampled test at its default depth.
- **Finding 6, different weights and engine.** TensorFold 1.3.0 on the maker's files wrote 75.6 and 76.4 tok/s on the same max test on two starts.

## The setup

ELI5: One engine at its newest release, started fresh six times.

- **Engine.** [mlx-serve](https://github.com/ddalcu/mlx-serve) 26.11.3, released 20 Nov 2026 12:14 SGT, installed from the project's Homebrew formula. The formula's SHA-256 equals the digest GitHub lists for `mlx-serve-bin-macos-arm64.tar.gz`. `mlx-serve --version` prints 26.11.3.
- **Weights.** [ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless](https://huggingface.co/ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless) @ 85002f89, and [mlx-community/Qwen3.8-27B-bf16](https://huggingface.co/mlx-community/Qwen3.8-27B-bf16) @ 379e7084.
- **Serve command.**

```bash
mlx-serve --model <model folder> --serve --host 127.0.0.1 --port <port> --ctx-size 131072 --max-concurrent 1 --warmup-full
```

- **`--warmup-full`** is new in 26.11.3. Its help says it compiles a model's Metal kernels before the server reports ready and calls it strongly recommended when benchmarking.
- **The second start** adds `--no-decode-attn-quant`. **Depth pinned at 5** adds `--mtp-min-depth 5 --mtp-max-depth 5`.
- **The full warm-up ran once.** The log of the first start reads "Warm requests complete (20 of 20, 16898 ms)". The help says it runs only the first time a build loads a model.
- **The dense-head start** is the second start's command with `MLX_SERVE_DSV41_HEAD8=0` and `MLX_SERVE_DSV41_EXACT=1` set in the server's environment.
- **Qwen3.8 27B** used `--ctx-size 262144`. Its second start left out `--warmup-full`.
- **Everything else at defaults**, which includes prompt lookup drafts on.
- **Thinking** off.

| Run id | Model | Setup | Started, SGT |
|---|---|---|---|
| `ddee83910540` | DeepSeek V4.1 Flash | Defaults, first start | 20 Nov, 22:17 |
| `4d0f49b9ac43` | DeepSeek V4.1 Flash | Defaults with `--no-decode-attn-quant`, second start | 20 Nov, 22:31 |
| `31a7274d722a` | DeepSeek V4.1 Flash | Depth pinned at 5 | 20 Nov, 22:45 |
| `8594b4fe926a` | Qwen3.8 27B full | Defaults | 20 Nov, 22:57 |
| `18b1cdba2631` | DeepSeek V4.1 Flash | Output head kept dense, `--no-decode-attn-quant` | 21 Nov, 03:17 |
| `5619fdacb103` | Qwen3.8 27B full | Defaults without `--warmup-full` | 21 Nov, 03:29 |

## How I measured

ELI5: Same Mac, same harness and same three questions as findings 5, 6 and 7.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** means temperature 1.0 and top-p 1.0 for DeepSeek, and temperature 0.7, top-p 0.8, top-k 20 and presence penalty 1.5 for Qwen3.8 27B, as in finding 2.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. The text of a request is picked from its size and repeat number, so every start got the same texts. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. The code prompts came to about 858 and 4,098 tokens on DeepSeek.
- **Three questions**, each placed after the code text.
  - **New code.** "Write a new Python module, with unit tests, that reimplements the most important function above in a cleaner way. Write it in full." In `rows.csv` the content is `code`.
  - **Copy.** "Repeat the text above exactly as written, starting from its first line after the Session line. Change nothing and add no commentary." The content is `code_echo`.
  - **Counting.** "Ignore the text above. Count from 1 to 400, one number per line, nothing else." The content is `code_count`.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 195 raw rows from the bench database. The 175 timed requests and the 20 warm-ups.
- **`runs.csv`.** The 6 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/08_dsv41_mlxserve_26113
```

## What I did not verify

- **A bit-exact run.** The head was kept dense on one start. The exact draft check (`MLX_SERVE_DSV41_EXACT`) was left off by the server, by its log.
- **A second start with the head kept dense**, and its copy and counting speeds.
- **A plain-decode reference** for the 250 short answers on this engine.
- **Whether `--no-decode-attn-quant` does anything on this pack.** The log is silent on it.
- **A second start of the pinned depth or of Qwen3.8 27B full.**
- **mlx-serve without `--warmup-full`** on 26.11.3 on the DeepSeek pack.
- **Whether Qwen3.8 27B full is slower on 26.11.3**, or why.
- **Prompts longer than 4K** on these tests. Finding 2 ran this pack to 1M tokens on 26.11.2.
- **Answer quality.** I timed the replies and did not score them.
- **Peak memory.** These runs did not log it.
- **Thinking on.**

## Credit

- **Engine and pack.** [mlx-serve](https://github.com/ddalcu/mlx-serve) and the Lossless pack by ddalcu.
- **Model.** DeepSeek V4.1 Flash by DeepSeek. Qwen3.8 27B by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
