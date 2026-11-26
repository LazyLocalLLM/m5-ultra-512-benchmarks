# Finding 43. TensorFold 1.3.5's Qwen3.8 Flash Next TFQ3 met its card and wrote 0.73 to 0.83 times the 4-bit build's speed

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold 1.3.5 brought TFQ3, a new way to pack Qwen3.8 Flash Next into smaller files. Its model card lists 82.9 tok/s plain and 154.5 with MTP drafts on an M5 Ultra. I checked both, and both held. Then I raced TFQ3 against TensorFold's own 4-bit MLX build of the same model, with the same prompts and the same server line, in alternating fresh starts. The 4-bit build wrote faster. TFQ3's files are a quarter smaller.

**On TensorFold 1.3.5, Qwen3.8 Flash Next TFQ3 met its model card's speeds and wrote 0.73 to 0.83 times as fast as TensorFold's 4-bit MLX build at the card's setup. The 4-bit build was faster in 119 of 120 same-prompt pairs. TFQ3's files are 79.0 GiB against 105.5 GiB. Four fresh starts in the order TFQ3, 4-bit, 4-bit, TFQ3 on 27 Nov 2026, and the same order on 26 Nov gave 0.74 to 0.84. Mac Studio M5 Ultra 512 GB, one user, 5 timed runs a cell.**

## TFQ3 against 4-bit at the card's setup

ELI5: A pair is one prompt on one TFQ3 start against the same prompt on one 4-bit start. Two starts each give 20 pairs a test. The two spread columns show how far two starts of one build differ, the yardstick for a real gap.

| Test | TFQ3 | 4-bit | Faster pairs, TFQ3 | Middle ratio | Range | Equal-length pairs, middle | Spread within TFQ3 | Spread within 4-bit |
|---|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 116.2 | 155.1 | 0 of 20 | 0.76 | 0.70 to 0.88 | - | 0.95 | 0.95 |
| Sampler, new code, 4K, 512 | 151.3 | 187.0 | 0 of 20 | 0.76 | 0.63 to 0.96 | - | 1.06 | 1.07 |
| Greedy code, 1K, 512 | 165.2 | 200.3 | 0 of 20 | 0.80 | 0.65 to 0.98 | - | 0.97 | 0.91 |
| Greedy code, 4K, 512 | 152.9 | 205.1 | 1 of 20 | 0.74 | 0.55 to 1.11 | - | 0.96 | 1.12 |
| Greedy code, 1K, 2,048 | 180.5 | 218.2 | 0 of 20 | 0.83 | 0.68 to 0.96 | 10 pairs, 0.84 | 1.00 | 1.06 |
| Greedy code, 4K, 2,048 | 166.4 | 212.3 | 0 of 20 | 0.73 | 0.57 to 0.99 | 17 pairs, 0.79 | 0.99 | 1.07 |

- **TFQ3 and 4-bit** are the middle of 10 timed runs, a build's two starts pooled, in tok/s by my client's clock.
- **Middle ratio** is the middle of the 20 pair ratios, TFQ3 over 4-bit. **Range** is the slowest and the fastest pair. **Spread within** is the middle ratio of a build's second start over its first, on the same prompts.
- **Same prompt, not same text.** The two builds are different weights. 0 of 250 short greedy answers matched between them, as expected. So a pair compares one prompt, never one reply. **Equal-length pairs** keep only pairs where both replies wrote the same number of tokens. That is the same length, not the same text.
- **The one faster pair** was greedy code at 4K and 512 tokens, ratio 1.11.
- **Times.** 27 Nov 2026, 00:48 to 01:04 SGT.

### The same race a night earlier

ELI5: I ran the same four starts on 26 Nov, without the 2,048-token cells. The ratios landed in the same place.

| Test | TFQ3 | 4-bit | Faster pairs, TFQ3 | Middle ratio | Range | Spread within TFQ3 | Spread within 4-bit |
|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 117.6 | 153.5 | 0 of 20 | 0.76 | 0.63 to 0.83 | 1.02 | 0.97 |
| Sampler, new code, 4K, 512 | 152.0 | 199.1 | 0 of 20 | 0.74 | 0.63 to 0.94 | 0.96 | 1.08 |
| Greedy code, 1K, 512 | 165.7 | 198.0 | 0 of 20 | 0.84 | 0.62 to 0.94 | 0.98 | 0.99 |
| Greedy code, 4K, 512 | 149.7 | 206.1 | 0 of 20 | 0.75 | 0.59 to 0.89 | 1.01 | 0.93 |

- **Times.** 26 Nov 2026, 17:55 to 18:09 SGT.
- **Both nights together.** TFQ3 was faster in 1 of 200 same-prompt pairs.

## Where the time goes

ELI5: With MTP, the model guesses a few tokens ahead and checks them in one step, called a round. TFQ3 keeps as many guessed tokens a round as the 4-bit build, or a few more. Each round takes longer.

| Test | TFQ3, tokens a round | 4-bit, tokens a round | TFQ3, ms a round | 4-bit, ms a round |
|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 2.5 | 2.4 | 21.2 | 15.8 |
| Sampler, new code, 4K, 512 | 3.7 | 3.5 | 24.9 | 17.9 |
| Greedy code, 1K and 4K, 512 | 4.1 | 3.6 | 25.6 | 17.7 |
| Greedy code, 1K and 4K, 2,048 | 4.7 | 3.9 | 27.6 | 18.4 |

- **Source.** The server's own done line for each reply, from the 27 Nov starts, a build's two starts pooled. Tokens a round is tokens written over draft rounds. ms a round is the server's decode time over draft rounds.
- **Mixed text, worked through.** Rounds took 1.34 times as long on TFQ3. That is 21.2 ms over 15.8 ms, so 21.2 / 15.8 = 1.34. Tokens a round stayed level, 2.5 against 2.4. By the server's clock TFQ3 wrote 117.6 tok/s and the 4-bit build 153.1, so 117.6 / 153.1 = 0.77. My client's pairs gave 0.76.

## Off the card's setup

ELI5: TensorFold's docs at v1.3.5 have no TFQ3 serve line. The project's M5 Ultra line for the 4-bit build is 1M context and two users. I ran TFQ3 there first. With the model's sampler, it fell much further behind.

| Test | TFQ3 | 4-bit | Faster pairs, TFQ3 | Middle ratio | Range | Equal-length pairs, middle | Spread within TFQ3 | Spread within 4-bit |
|---|---|---|---|---|---|---|---|---|
| Sampler, mixed, 4K, 512 | 82.5 | 132.6 | 0 of 20 | 0.62 | 0.58 to 0.67 | - | 0.99 | 1.01 |
| Sampler, new code, 4K, 512 | 90.4 | 170.6 | 0 of 20 | 0.54 | 0.43 to 0.65 | - | 1.00 | 0.86 |
| Greedy code, 1K, 512 | 164.1 | 183.0 | 0 of 20 | 0.88 | 0.65 to 0.99 | - | 0.98 | 0.98 |
| Greedy code, 4K, 512 | 148.2 | 193.4 | 2 of 20 | 0.75 | 0.65 to 1.10 | - | 0.96 | 0.98 |
| Greedy code, 1K, 2,048 | 174.1 | 215.6 | 0 of 20 | 0.78 | 0.68 to 0.94 | 6 pairs, 0.83 | 0.96 | 1.00 |
| Greedy code, 4K, 2,048 | 173.2 | 193.2 | 1 of 20 | 0.82 | 0.68 to 1.03 | 20 pairs, 0.82 | 1.04 | 0.98 |

- **Not interleaved, so weaker than the tables above.** The 4-bit rows are finding 42's two 1.3.5 starts, which began at 11:53 and 12:08 SGT on 26 Nov 2026. TFQ3 ran 17:19 to 17:33 SGT the same day.
- **Draft rounds with the sampler.** On this line TFQ3 kept 1.6 tokens a round on mixed text and 1.8 on new code. At the card's setup it kept 2.5 and 3.7. The 4-bit build kept 2.3 and 3.3 on this line. Greedy code kept 3.9 tokens a round at 512 tokens and 4.8 at 2,048 on this line, against 4.1 and 4.7 at the card's setup.
- **The summary page** holds this line as a second TFQ3 setup. The card's setup wrote faster on every test, so it sets TFQ3's numbers.

## The card's own claims

ELI5: The TFQ3 card lists four speeds on an M5 Ultra and says its MTP drafts change no answer. I checked the two speeds I can match, and the answers.

- **Drafts off.** TFQ3 wrote 85.0 tok/s on 1K code and 83.3 on 4K code with `--no-drafts` at the card's setup, 26 Nov 2026 17:49 SGT. The card says 82.9 tok/s for single-row decode. On the recipe line, drafts off wrote 72.5 to 74.4 tok/s.
- **MTP on.** Greedy code at 512 tokens wrote 149.0 to 168.0 tok/s, the 1K and 4K medians of TFQ3's four starts at the card's setup over both nights. The card says 154.5 tok/s with MTP depth 3. TensorFold's MTP head chains three drafts by default.
- **Same answers.** MTP answers matched drafts-off answers 250 of 250, by the harness's identity test on 26 Nov. The card says depth 3 matched depth 0 token for token.
- **Not compared.** The card's 3,855 tok/s prefill is on a 2,048-token prompt, and I read 1K and 4K prompts. Its 126 to 139 tok/s for live streaming with MTP and copy drafts names no prompt or sampler. Its perplexity table needs a quality test, and I ran none.

## The summary page

ELI5: The summary keeps each model's fastest setup. TFQ3 gets its own row. The 4-bit build gains the one-user setup, which beat its recipe line on all three summary cells.

- **New row, Qwen3.8 Flash Next TFQ3.** Max 180.7, median 115.3 and code 150.2 tok/s, from the card's setup, run `01a33e97e798`. Its recipe-line setup, run `e76b38f9a661`, is listed under it.
- **Qwen3.8 Flash Next 4-bit moves to one user at 262K context,** run `2b3d0041ab7c`. Max 223.4 against 217.6, median 150.9 against 131.2, and code 191.1 against 165.5, all tok/s. The second figure of each pair is finding 42's recipe-line start of 26 Nov, which ran about 13 hours earlier, so this gap is not interleaved.
- **Picked by rule.** Each setup's line is its latest start, not its fastest.
- **Left as they were.** The 4-bit build's copy and counting lines, not rerun here.

## The setup

ELI5: The same engine and harness as finding 42. TFQ3 and the 4-bit build each ran on a fresh server, one after the other, with the serve line the TFQ3 card describes.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.5, tag `v1.3.5` at commit `02b324ae`, from the project's Homebrew tap, as in finding 42. `tensorfold-native --version` prints 1.3.5.
- **Builds.** [TensorFold/Qwen3.8-Flash-Next-TFQ3](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-TFQ3) at commit `eeb675d7`, 79.0 GiB of files. [TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP) at commit `2b170fa6`, 105.5 GiB. Sizes are the sum of each repository's file sizes.
- **The card's setup.** `tensorfold serve <folder> --context 262144 --parallel 1 --vision --prompt-cache-gib 8 --temperature 0 --no-update-check`. The server reports 262,112 tokens of context, the card's number, and "MTP + copies" drafts. Drafts off adds `--no-drafts`.
- **The recipe line.** The same with `--context 1048576 --parallel 2`, the M5 Ultra line of `docs/recipes/qwen3.8-flash-next.md` at v1.3.5. It is written for the 4-bit build.
- **Thinking** off.
- **Requests.** One user, streamed. Greedy, temperature 0, for code. The model's own sampler, temperature 0.7, top-p 0.8 and top-k 20, for mixed text and for new code. 5 timed runs a cell after a warm-up.
- **Server memory.** The resident memory `ps` reported after load was 55.6 GiB for TFQ3 and 122.4 GiB for the 4-bit build. TFQ3's figure is below its file size, so it is not the whole footprint. I did not measure total memory use.
- **First load.** TFQ3's first load on this Mac wrote a 7.5 GiB pack cache under `~/.cache/tensorfold`. Later loads reused it.
- **Times.** 26 Nov 2026, 17:19 to 18:09 SGT, and 27 Nov 2026, 00:48 to 01:04 SGT.

## How I measured

- **Writing speed** is tokens written less one, over the time from the first streamed piece to the last, by my client's clock.
- **Same prompts.** Each run uses the seed target times 1,000 plus the run number, so run 3 at 4K reads the same prompt on both builds.

## Check it yourself

- `rows.csv` holds every speed request of the 14 runs, warm-ups marked. That is 12 runs from this finding and finding 42's two 1.3.5 starts of the 4-bit build on the recipe line. `runs.csv` holds each run's engine, build and settings.
- From the top of the repository, `python3 tools/summarize.py findings/43_tensorfold_135_tfq3` prints the median and range of each run.

## What I did not verify

- TFQ3's quality. The card reports lower perplexity than MLX 4-bit, and I ran no quality test. I read no reply for quality.
- Why a TFQ3 round takes longer. The server's done lines give the time, not the cause.
- Whether TensorFold means a different serve line for TFQ3. Its docs at v1.3.5 have none, so I used the card's.
- TFQ3 at any context or user count besides these two lines.
- Total memory use.

## Credit

TensorFold is by [@ashxhart](https://x.com/ashxhart). Both checkpoints come from TensorFold's Hugging Face page. If I have set it up wrong, [open an issue](https://github.com/LazyLocalLLM/m5-ultra-512-benchmarks/issues) and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
