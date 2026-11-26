# Finding 42. TensorFold 1.3.5 against 1.3.4 on four builds, no change I can call

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold 1.3.5 came out on 25 Nov 2026. I ran it against the 1.3.4 program Homebrew kept, on the four TensorFold builds the summary page holds, both releases on one day. Same prompts, same settings. The speeds were the same within what two starts of one release differ by, and the answers matched.

**TensorFold 1.3.5 showed no speed change I can call against 1.3.4 on Qwen3.8 27B, Qwen3.8 Flash Next, GLM-5.3 Flash and Hy4-flash, all 4-bit. Each ran in the order 1.3.5, 1.3.4, 1.3.4, 1.3.5 on 26 Nov 2026, with a fresh server each start. Pair ratios sat between 0.93 and 1.04, inside the spread between two starts of one release. 1,000 of 1,000 short greedy answers match 1.3.4. Mac Studio M5 Ultra 512 GB, one user, 5 timed runs a cell.**

## Each build, both releases

ELI5: A pair is one prompt on one 1.3.5 start against the same prompt on one 1.3.4 start. Two starts a release give 20 pairs a test. The two spread columns show how far two starts of the same release differ, the yardstick for a change.

### Qwen3.8 27B 4-bit, DFlash2

| Test | 1.3.5 | 1.3.4 | Faster pairs | Middle ratio | Equal-length pairs, middle | Spread within 1.3.5 | Spread within 1.3.4 |
|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 143.7 | 151.1 | 7 of 20 | 0.95 | - | 1.12 | 1.04 |
| Sampler, new code, 4K, 512 | 214.7 | 199.1 | 16 of 20 | 1.04 | - | 0.98 | 0.97 |
| Greedy code, 1K, 512 | 238.7 | 238.1 | 8 of 20 | 0.98 | - | 1.05 | 1.00 |
| Greedy code, 4K, 512 | 234.3 | 221.9 | 9 of 20 | 1.00 | - | 0.97 | 0.99 |
| Greedy code, 1K, 2,048 | 326.9 | 327.8 | 8 of 20 | 1.00 | 12 pairs, 1.00 | 1.01 | 1.00 |
| Greedy code, 4K, 2,048 | 265.3 | 262.0 | 5 of 20 | 0.94 | 13 pairs, 0.97 | 1.02 | 1.03 |

### Qwen3.8 Flash Next 4-bit, MTP

| Test | 1.3.5 | 1.3.4 | Faster pairs | Middle ratio | Equal-length pairs, middle | Spread within 1.3.5 | Spread within 1.3.4 |
|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 132.6 | 133.5 | 9 of 20 | 0.98 | - | 1.01 | 1.00 |
| Sampler, new code, 4K, 512 | 170.6 | 185.6 | 8 of 20 | 0.93 | - | 0.86 | 1.12 |
| Greedy code, 1K, 512 | 183.0 | 189.3 | 8 of 20 | 0.98 | - | 0.98 | 1.02 |
| Greedy code, 4K, 512 | 193.4 | 196.8 | 10 of 20 | 1.00 | - | 0.98 | 1.05 |
| Greedy code, 1K, 2,048 | 215.6 | 218.1 | 10 of 20 | 1.00 | 14 pairs, 1.00 | 1.00 | 1.03 |
| Greedy code, 4K, 2,048 | 193.2 | 207.9 | 14 of 20 | 1.03 | 20 pairs, 1.03 | 0.98 | 1.03 |

### GLM-5.3 Flash 4-bit, DFlash2

| Test | 1.3.5 | 1.3.4 | Faster pairs | Middle ratio | Equal-length pairs, middle | Spread within 1.3.5 | Spread within 1.3.4 |
|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 81.6 | 82.0 | 10 of 20 | 1.00 | - | 1.04 | 0.97 |
| Sampler, new code, 4K, 512 | 91.8 | 93.3 | 7 of 20 | 0.99 | - | 1.03 | 1.02 |
| Greedy code, 1K, 512 | 100.4 | 99.7 | 13 of 20 | 1.02 | - | 1.01 | 0.97 |
| Greedy code, 4K, 512 | 98.4 | 97.7 | 12 of 20 | 1.02 | - | 0.99 | 1.03 |
| Greedy code, 1K, 2,048 | 102.7 | 99.9 | 13 of 20 | 1.02 | 8 pairs, 1.00 | 1.00 | 0.98 |
| Greedy code, 4K, 2,048 | 97.4 | 97.9 | 11 of 20 | 1.01 | 10 pairs, 0.97 | 0.96 | 0.98 |

### Hy4-flash 4-bit, DFly2

| Test | 1.3.5 | 1.3.4 | Faster pairs | Middle ratio | Equal-length pairs, middle | Spread within 1.3.5 | Spread within 1.3.4 |
|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 46.2 | 46.6 | 10 of 20 | 1.02 | - | 1.00 | 0.96 |
| Sampler, new code, 4K, 512 | 46.8 | 47.5 | 10 of 20 | 1.00 | - | 0.98 | 1.06 |
| Greedy code, 1K, 512 | 60.1 | 59.6 | 10 of 20 | 1.00 | - | 0.97 | 1.02 |
| Greedy code, 4K, 512 | 57.1 | 58.3 | 8 of 20 | 0.99 | - | 0.97 | 1.00 |
| Greedy code, 1K, 2,048 | 63.1 | 64.5 | 5 of 20 | 0.97 | 20 pairs, 0.97 | 0.96 | 1.03 |
| Greedy code, 4K, 2,048 | 60.1 | 61.7 | 10 of 20 | 1.01 | 20 pairs, 1.01 | 1.07 | 1.03 |

- **1.3.5 and 1.3.4** are the middle of 10 timed runs, a release's two starts pooled, in tok/s by my client's clock.
- **Middle ratio** is the middle of the 20 pair ratios, 1.3.5 over 1.3.4. **Spread within** is the middle ratio of a release's second start over its first, the same prompts.
- **Equal-length pairs.** Long greedy replies changed length from start to start on both releases, so some 2,048-token pairs are not the same text. That column keeps only pairs where both replies wrote the same number of tokens. I added it after seeing the all-pairs figure.
- **Leaning slow, 3 to 7%.** Qwen3.8 27B on mixed text (0.95) and on 4K code at 2,048 tokens (0.94, or 0.97 on equal-length pairs). Flash Next on new code with its sampler (0.93). Hy4-flash on 1K code at 2,048 tokens (0.97). Each sits inside its own same-release spread. Flash Next's sampled code cell spread from 0.86 to 1.12 between starts of one release.
- **Leaning fast.** None by more than 4%. Qwen3.8 27B on new code with its sampler (1.04) and Flash Next on 4K code at 2,048 tokens (1.03).
- **Reply text.** Hy4-flash runs with thinking on and writes reasoning text. The others write answer text.

## Did the text change

ELI5: The harness's identity test, 250 short greedy replies on the first start of each release, compared text for text.

- **250 of 250 the same** on each of the four builds, 1,000 of 1,000 in all, by the harness's identity test against the 1.3.4 start of the same night.

## The summary page

ELI5: Only the setup I reran moves to 1.3.5. A setup I did not rerun keeps its 1.3.4 line.

- **Moved to 1.3.5,** from each build's latest start. Qwen3.8 27B with the DFlash2 drafter, run `2b0a3fd3c45a`. Flash Next with MTP at the recipe line, run `dd04a3121fd2`. GLM-5.3 Flash with the DFlash2 draft model, run `f3a0f5cee6a0`. Hy4-flash at defaults, run `163b98382a23`. Their code lines from finding 40 move too.
- **Left on 1.3.4, not rerun.** GLM-5.3 Flash with MTP drafts, Hy4-flash with `TF_HY4_DRAFT_BITS=8`, and the counting-toy lines.
- **What a reader sees.** Qwen3.8 27B max 325.7, median 156.9, code 204.4. Flash Next max 217.6, median 131.2, code 165.5. GLM-5.3 Flash median 83.2 and code 93.7 on 1.3.5, and max 102.5 from the 1.3.4 MTP-drafts line. Hy4-flash max 79.0 and median 51.6 stay on the 1.3.4 `TF_HY4_DRAFT_BITS=8` line, code 46.7 on 1.3.5.
- **A latest start can move a few percent on a level release.** GLM-5.3 Flash's DFlash2 max read 104.7 on its one 1.3.4 start of 23 Nov and 102.3 on tonight's latest 1.3.5 start, against 103.1 on the first. Its median read 85.9 then and 83.2 now. The pairs above show no change.

## The setup

ELI5: The same builds, serve lines and harness as finding 27, with 1.3.5 from TensorFold's Homebrew tap and 1.3.4 run from the copy Homebrew kept.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.5, published on GitHub 25 Nov 2026 15:49 SGT, not a pre-release, tag `v1.3.5` at commit `02b324ae`. Installed from the project's Homebrew tap. The tap's change, commit `8943393`, is the formula's url and sha256 alone, and the sha256 `5959b770` equals the digest GitHub lists for `tensorfold-1.3.5-macos-arm64.tar.gz`. `tensorfold-native --version` prints 1.3.5.
- **The 1.3.4 program** is the keg Homebrew kept in its Cellar, run by its full path. It prints 1.3.4. Nothing was installed for it.
- **Builds.** TensorFold/Qwen3.8-27B-MLX-4bit with the z-lab DFlash2 drafter, `--context 262144 --parallel 1`. TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP at the project's M5 Ultra recipe line, `--context 1048576 --parallel 2`. TensorFold/GLM-5.3-Flash-MLX-4bit-MTP with the incoai DFlash2 draft model, and TensorFold/Hy4-flash-MLX-4bit-MTP with its DFly2 drafts, both `--context 131072 --parallel 1`.
- **Thinking** off for the Qwen and GLM builds, on for Hy4-flash, as in finding 27.
- **Requests.** One user, streamed. Greedy, temperature 0, for code. Each model's own sampler for mixed text and for new code. 5 timed runs a cell after a warm-up.
- **Times.** 26 Nov 2026, 11:33 to 13:42 SGT.

## How I measured

- **Writing speed** is tokens written less one, over the time from the first streamed piece to the last, by my client's clock.
- **Same prompts.** Each run uses the seed target times 1,000 plus the run number, so run 3 at 4K reads the same prompt on both releases.

## Check it yourself

- `rows.csv` holds every request of the 16 runs, warm-ups marked. `runs.csv` holds each run's engine, build and settings.
- From the top of the repository, `python3 tools/summarize.py findings/42_tensorfold_135_refresh` prints the median and range of each run.

## What I did not verify

- DeepSeek V4.1 Flash on 1.3.5. Its server is built from source, and that build is not done yet.
- 1.3.5's new TFQ3 checkpoints and its new model families. They are not on this page.
- Whether any reply is a good answer. I read none of them for quality.

## Credit

TensorFold is by [@ashxhart](https://x.com/ashxhart). If I have set it up wrong, [open an issue](https://github.com/LazyLocalLLM/m5-ultra-512-benchmarks/issues) and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
