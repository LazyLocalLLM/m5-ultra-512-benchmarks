# Finding 37. Inkling 2 Mini on MTPLX 2.13.2, prompts near 1M tokens

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Updated on 24 Nov 2026 at 12:32 SGT with a link to finding 38, the same prompts on Strata.

ELI5: [Finding 29](../29_inkling2_mini_mtplx_2132) timed Inkling 2 Mini on MTPLX 2.13.2 with prompts of 1K and 4K tokens. This page asks what happens when the prompt is long. I gave it new code and mixed text from about 19K tokens up to 988,698, near the model's limit of 1,048,576, with its draft head on and off. Two things are timed. How long it takes to read the prompt, and how fast it writes after that.

**MTPLX 2.13.2 read a 988,698-token prompt in 860.8 s, about 14 minutes, then wrote 29.0 tok/s with Inkling 2 Mini's draft head on.** With the head off it read for 908.3 s and wrote 21.9. Greedy code, middle of 3 runs each, 24 Nov 2026 SGT. At 18,852 tokens the same arms wrote 122.3 and 85.3.

## Greedy code, the max

ELI5: Temperature 0 on new code. This is the fastest case, so it is the max.

| Prompt tokens | First token, s | Read, tok/s | Write, draft head on, tok/s | Write, draft head off, tok/s | Runs, on and off |
|---|---|---|---|---|---|
| 18,852 | 3.8 | 4,908 | 122.3 | 85.3 | 5 and 5 |
| 43,261 | 9.1 | 4,698 | 107.4 | 79.3 | 5 and 5 |
| 83,816 | 19.9 | 4,174 | 98.6 | 71.0 | 5 and 5 |
| 169,676 | 51.0 | 3,322 | 85.6 | 58.4 | 5 and 5 |
| 255,377 | 91.9 | 2,778 | 75.3 | 49.3 | 5 and 5 |
| 514,313 | 279.9 | 1,840 | 47.6 | 34.3 | 3 and 3 |
| 988,698 | 860.8 | 1,149 | 29.0 | 21.9 | 3 and 3 |

- **Prompt tokens** are the middle of the engine's own count for the cell's runs. The harness asks for a target length at 3.5 characters a token, and Inkling's tokenizer made 1.15 to 1.32 tokens per target token on this text, by cell middles, so I name each row by what was measured.
- **First token** is the seconds from sending the request to the first streamed piece of the reply. **Read** is prompt tokens over those seconds. Both are from the draft head on runs.
- **The draft head barely moved the reading up to 255,377 tokens.** Its first token came 0.99 to 1.05 times as late as with the head off, as the middle of each cell's pairs. At 514,313 and 988,698 tokens the head off runs read slower, and the head on first token came 0.96 and 0.95 times as late. The head off arm ran second in both jobs. I did not test why.
- **Write** is the reply's tokens after the first, over the seconds from the first streamed piece to the last, by my client's clock.
- **The draft head was faster on all 31 same-text code pairs.** A pair is the same cell and repeat in both arms, so the same body of text. The middle ratio per cell ran from 1.32 at 988,698 tokens to 1.53 at 255,377.
- **By MTPLX's own clock the gain is smaller.** Its decode figure gave the draft head a middle ratio per cell of 1.26 at 988,698 tokens to 1.45 at 255,377, and the head was still faster on all 31 code pairs. At 988,698 tokens its middles were 24.4 tok/s on and 19.5 off. The gap between the clocks is in How I measured.
- **One cell is spread wide.** At 255,377 tokens the draft head wrote from 61.8 to 137.9 tok/s. Two of its five replies kept 86% and 93% of the drafted tokens and wrote 117.6 and 137.9. The other three kept 44% to 56%. The middle, 75.3, sits with the three. Drafted speed depends on how well the head guesses each text.
- **The code prompts did not repeat text** up to 514,313 tokens. Each prompt is one stretch of a 2,168,885-character code file. The 988,698-token prompts are longer than the file, so they wrap to the start, and 21.2% of each repeats earlier text.

## Chart

ELI5: Writing speed after the prompt, greedy code, the draft head off and on. Each bar is the middle of 3 to 5 runs.

![Bar chart of writing speed after the prompt for Inkling 2 Mini on MTPLX 2.13.2, greedy code. At 19K, 43K, 84K, 170K, 255K, 514K and 989K tokens, the draft head off wrote 85.3, 79.3, 71.0, 58.4, 49.3, 34.3 and 21.9 tok/s, and the draft head on wrote 122.3, 107.4, 98.6, 85.6, 75.3, 47.6 and 29.0 tok/s.](chart_write.png)

## The model's own sampler, the median

ELI5: Temperature 1.0 and top-p 1.0 on a mix of prose and code. This is how the model samples by default, so it is the daily case.

| Prompt tokens | First token, s | Read, tok/s | Write, draft head on, tok/s | Write, draft head off, tok/s | Runs, on and off |
|---|---|---|---|---|---|
| 20,122 | 4.2 | 4,770 | 113.4 | 73.1 | 5 and 5 |
| 39,769 | 8.6 | 4,644 | 110.0 | 67.0 | 5 and 5 |
| 82,310 | 19.9 | 4,134 | 95.8 | 63.3 | 5 and 5 |
| 163,257 | 48.5 | 3,363 | 77.1 | 52.5 | 5 and 5 |
| 242,131 | 85.6 | 2,828 | 68.1 | 46.8 | 5 and 5 |
| 483,894 | 259.0 | 1,877 | 43.5 | not run | 3 and 0 |
| 967,802 | 843.1 | 1,148 | 26.3 | not run | 3 and 0 |

- **The draft head was faster on all 25 same-text pairs** up to 242,131 tokens. The middle ratio per cell ran from 1.46 to 1.63 by my clock and 1.39 to 1.59 by MTPLX's.
- **The draft head off was not run on mixed text at 483,894 and 967,802 tokens.** To fit the night, that arm ran code only at those two lengths.
- **Mixed text repeats more as it grows.** Each prompt is built from 2,000-character pieces of prose and 6,000-character pieces of code, each from a random place in its file, so long prompts draw some pieces twice. By rebuilding each prompt from its seed, the share of repeated characters was 0% to 4% at 20,122 tokens, 7% to 13% at 163,257, 12% to 15% at 242,131, 23% to 25% at 483,894 and 38% at 967,802.
- **Against the short prompts.** Finding 29's median at a 4K prompt, the same sampler, text mix and 512-token replies, was 124.7 tok/s with the draft head on. Here it was 113.4 at 20,122 tokens, 68.1 at 242,131 and 26.3 at 967,802.

## Reading the prompt

ELI5: Before it writes a word, the model has to read the whole prompt. Near 1M tokens, that is most of the wait.

- **Reading slowed as the prompt grew.** 4,908 tok/s at 18,852 tokens, 3,322 at 169,676, 2,778 at 255,377, 1,840 at 514,313 and 1,149 at 988,698, greedy code with the draft head on.
- **At 988,698 tokens, reading was 98% of the wait.** In each of the 3 draft head on runs, the first token came at 97.9% of the time to the end of the reply. The middle run read for 860.8 s of 879.6 s.
- **This page cannot say how much of the slowdown is the model and how much is MTPLX.** [Finding 38](../38_inkling2_mini_long_prompts_strata) runs the same prompts up to 255,376 tokens on Strata 0.2.20.
- **Nothing was cached.** Every request opens with its own random session line, and every timed request reused 0 cached tokens, by MTPLX's own count.

## The setup

ELI5: MTPLX in its default long-context mode, the Bare Speed pack of findings 21 and 29, one request at a time.

- **Engine.** [MTPLX](https://github.com/youssofal/MTPLX) 2.13.2, published 23 Nov 2026 09:24 SGT, not a pre-release, tag `v2.13.2` at commit 3890be55. It was still the newest release on GitHub and PyPI on 24 Nov 2026 at 06:35 SGT.
- **Mode.** Sustained, by MTPLX's own start lines, which call it the profile. Its README's table of modes makes Sustained the default for this model, calls it a "Long-context MTP path with chunked prefill and request-sized KV", and gives it for "16K-200K prompts". The rows above 200K tokens run past that range. The same README gives the Bare Speed pack a context of 1,048,576 tokens on a Mac with 96 GB to 512 GB, and names no mode for prompts above 200K. I changed no prefill or cache setting. Sustained Max, which pins the fans, and the other modes were not run.
- **Pack.** Inkling 2 Mini Bare Speed, `Youssofal/Inkling-2-Mini-MTPLX-Bare-Speed`, the pack of findings 21 and 29.
- **Serve line.** `mtplx serve --model <pack> --host 127.0.0.1 --port <port> --context-window 262144 --no-stats-footer` up to 255,377 tokens, and `--context-window 1048576` for the two longest lengths. `--no-mtp` for the draft head off. No thinking field in the requests, as in finding 29.
- **Replies were reasoning text.** With no thinking field, Inkling 2 Mini thinks first. Every timed reply ran to its 512-token cap, and the harness counted 508 to 510 of those tokens as thinking.
- **Saved state.** MTPLX keeps a session bank of saved conversations in `~/.mtplx`. It held 53 GiB at 06:41 SGT and 64 GiB at 09:38 SGT, during the 1M job, by `du`. No timed request read from it.

| Run id | Setting | Prompt tokens | Started, SGT, 24 Nov 2026 |
|---|---|---|---|
| `ab2566f12c50` | Draft head on | 18,852 to 255,377, code and mixed | 05:15 |
| `dd498489c8a1` | Draft head off | 18,852 to 255,377, code and mixed | 05:49 |
| `a1cdd8e853df` | Draft head on | 483,894 to 988,698, code and mixed | 06:27 |
| `3d10d9bb0602` | Draft head off | 514,313 and 988,698, code only | 08:31 |

## How I measured

ELI5: The same Mac and harness as every page here, with longer prompts.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time, 512-token replies.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** is temperature 1.0 and top-p 1.0, as in finding 29.
- **Repeats.** 5 timed runs per cell up to 255,377 tokens, 3 at the two longest lengths. Each test, greedy code or sampled mixed, began with one warm-up request on mixed text with a 16-token reply, 7 in all. Its prompt was about 19K tokens in the shorter job and about 487K in the 1M job. A minute's pause came before the first test of each job.
- **Clock.** My client's. MTPLX's own decode figure, in each reply's timings, ran below mine, by 1% to 7% at about 19K tokens. At 988,698 tokens it ran 15% to 18% below with the draft head on and 11% to 12% below with it off. Both are in `rows.csv`.
- **Not fully quiet.** I wrote files beside the runs, light work.

## No `mlx-lm` multiple

- **`mlx-lm` 0.32.2 has no Inkling 2 model**, as finding 21 notes, and it was still the newest release on 24 Nov 2026. The draft head off is the baseline.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every middle.

- **`rows.csv`.** 125 raw rows from the bench database, 7 warm-ups included and marked.
- **`runs.csv`.** The 4 runs, with engine, version, start time and settings. A run's settings line names its first test. Each row's own sampler is in its `extra` column.
- **Targets and tokens.** `summarize.py` names each cell by the harness's target, 16384 to 786432. The tables here name them by measured tokens. Each row of `rows.csv` has both.

From the top of this repository.

```bash
python3 tools/summarize.py findings/37_inkling2_mini_long_prompts_mtplx
```

## What I did not verify

- **Reply text.** Each request opens with its own random session line, so the two arms never read exactly the same prompt, and the traces keep timings, not text. Finding 21's short questions gave the same replies with the head on and off. I did not check that here.
- **Answer quality at length.** I did not ask questions about the long text or grade any reply.
- **Mixed text with the draft head off** at 483,894 and 967,802 tokens.
- **Other modes and settings.** Sustained Max, `--prefill-chunk-tokens`, `--paged-kv-quantization` and the other packs were not run.
- **Two users at once.**

## Credit

- **Engine and pack.** [MTPLX](https://github.com/youssofal/MTPLX) by [@Youssofal_](https://x.com/Youssofal_).
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
