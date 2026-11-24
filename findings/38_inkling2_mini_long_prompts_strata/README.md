# Finding 38. Inkling 2 Mini on Strata 0.2.20, prompts up to 255K tokens

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: [Finding 30](../30_inkling2_mini_strata_0220) timed Inkling 2 Mini on Strata 0.2.20 with prompts of 1K and 4K tokens. This page gives it long prompts, from about 19K tokens up to 255,376, with Strata's DSpark drafter on and off. They are the same prompts as [finding 37](../37_inkling2_mini_long_prompts_mtplx) up to that length. Two things are timed. How long Strata takes to read the prompt, and how fast it writes after that.

**Strata 0.2.20 read a 255,376-token prompt in 207.1 s, 1,234 tok/s, on Inkling 2 Mini with Strata's own SQ-20 pack. At 18,849 tokens it read in 6.0 s, 3,117 tok/s.** With the model's own sampler its DSpark drafter was slower than drafting off at every length, on 25 of 25 same-text pairs, as finding 30 found at 4K. On greedy code it was faster on 15 of 15 pairs where both replies ran full length, and on 19 of 25 over all replies. Middle of 5 runs each, 24 Nov 2026 SGT.

## Reading the prompt

ELI5: Before it writes a word, the model has to read the whole prompt. Here is how long that took on new code.

| Prompt tokens | First token, s | Read, tok/s |
|---|---|---|
| 18,849 | 6.0 | 3,117 |
| 43,260 | 15.9 | 2,722 |
| 83,817 | 37.9 | 2,211 |
| 169,677 | 107.4 | 1,580 |
| 255,376 | 207.1 | 1,234 |

- **Prompt tokens** are the middle of the engine's own count for the cell's runs. The harness asks for a target length at 3.5 characters a token, and Inkling's tokenizer makes more tokens than that, so I name each row by what was measured.
- **First token** is the seconds from sending the request to the first streamed piece of the reply. **Read** is prompt tokens over those seconds. Both are from the drafter on runs, greedy code. Mixed text read at much the same speeds, from 2,870 tok/s at 20,122 tokens to 1,253 at 242,129. Its table is below.
- **The drafter did not change the reading on code.** Pair by pair, the drafter on first token came 1.00 to 1.01 times as late as with drafting off, at every length. On mixed text it came 1.08 times as late at 20,122 tokens and 1.01 to 1.03 times above that. In the 32,768 control below, the mixed first token came 1.01 times as late.
- **Strata's own count agrees.** Its prompt speed, in each reply's timings, was within 0.5% of mine on every row.
- **Nothing was cached.** Every request opens with its own random session line, and every timed request reused 0 cached tokens, by Strata's own count.

## The model's own sampler, the median

ELI5: Temperature 1.0 and top-p 1.0 on a mix of prose and code. This is how the model samples by default, so it is the daily case.

| Prompt tokens | First token, s | Read, tok/s | Write, drafter on, tok/s | Write, drafting off, tok/s | Runs, on and off |
|---|---|---|---|---|---|
| 20,122 | 7.1 | 2,870 | 34.1 | 51.9 | 5 and 5 |
| 39,767 | 14.8 | 2,666 | 30.0 | 44.8 | 5 and 5 |
| 82,311 | 37.4 | 2,211 | 22.6 | 34.7 | 5 and 5 |
| 163,255 | 101.8 | 1,602 | 16.6 | 24.2 | 5 and 5 |
| 242,129 | 193.2 | 1,253 | 12.2 | 18.6 | 5 and 5 |

- **Write** is the reply's tokens after the first, over the seconds from the first streamed piece to the last, by my client's clock. Strata's own decode figure was within 4.0% of mine on every row, and the middle gap was 0.2%.
- **The drafter was slower on all 25 same-text pairs.** A pair is the same cell and repeat in both arms, so the same body of text. The middle ratio per cell ran from 0.66 to 0.68. Finding 30 found 0.64 at a 4K prompt.
- **What the drafter did, by Strata's own counts.** It proposed 4.9 to 5.2 drafts per written token and kept 4.7% to 6.0% of them, cell by cell. Finding 30 counted about 5 and about 5%.
- **The model stopped some replies early.** The cap was 512 tokens. With the drafter on, 23 of 25 replies reached it. With drafting off, 18 of 25 did, and the shorter replies wrote at about the speed of the full ones.

## Chart

ELI5: Writing speed after the prompt, the model's own sampler, drafting off and on. Each bar is the middle of 5 runs.

![Bar chart of writing speed after the prompt for Inkling 2 Mini on Strata 0.2.20 with the model's own sampler on mixed text. At 20K, 40K, 82K, 163K and 242K tokens, drafting off wrote 51.9, 44.8, 34.7, 24.2 and 18.6 tok/s, and the DSpark drafter on wrote 34.1, 30.0, 22.6, 16.6 and 12.2 tok/s.](chart_write.png)

## Greedy code, the max

ELI5: Temperature 0 on new code. This is where a drafter guesses best. Here the length of each reply matters, so the drafter's gain is given two ways.

| Prompt tokens | Write, drafter on, tok/s | Write, drafting off, tok/s | Replies at the 512 cap, on and off | Full replies only, on and off, tok/s |
|---|---|---|---|---|
| 18,849 | 55.0 | 52.8 | 2 and 5 | 71.8 and 52.8 |
| 43,260 | 53.1 | 44.0 | 3 and 2 | 53.6 and 44.9 |
| 83,817 | 50.6 | 34.9 | 4 and 3 | 57.4 and 34.4 |
| 169,677 | 33.0 | 23.5 | 4 and 5 | 33.8 and 23.5 |
| 255,376 | 27.9 | 17.9 | 4 and 4 | 29.7 and 17.9 |

- **Every reply.** The drafter was faster on 19 of 25 same-text pairs. The middle ratio per cell ran from 1.06 at 18,849 tokens to 1.56 at 83,817 and 255,376.
- **Replies that ran to the cap in both arms.** The drafter was faster on 15 of 15 pairs. The middle ratio per cell ran from 1.36 at 18,849 tokens to 1.83 at 83,817. Some cells have only 2 such pairs.
- **Short replies wrote at about the drafting off speed.** With the drafter on, the 7 replies of 35 to 183 tokens wrote 0.94 to 1.04 times the drafting off middle of their cell. The middle at 18,849 tokens, 55.0, is one of them, a 111-token reply. With drafting off, short and full replies wrote at the same speed.
- **The drafter kept more as the prompt grew.** By Strata's own counts it kept 44% of its drafts at 18,849 tokens, 62% at 83,817 and 78% at 255,376. It proposed 0.9 drafts per written token at the shortest length and 0.6 at the longest. Counting only full replies, it kept 44% and 51% at 18,849 tokens and 57% to 87% at 255,376.
- **One cell is spread wide.** At 255,376 tokens the drafter wrote from 20.7 to 36.0 tok/s. The slowest reply proposed 0.33 drafts per written token and kept 57%. The fastest proposed 0.70 and kept 87%.
- **Every reply is answer text.** Strata serves Inkling 2 Mini with reasoning effort "none" only, as finding 30 notes. Every timed reply had 0 thinking tokens.

## A control at Strata's own context

ELI5: These runs widen Strata's context from setup's 32,768 to 262,144. To check that the wider setting did not change the speed, I ran setup's own entries, unchanged, on the shortest prompts.

| Setting, about 19K to 20K tokens | Context | Greedy code, tok/s | Own sampler, tok/s |
|---|---|---|---|
| Drafting off | 262,144 | 52.8 | 51.9 |
| Drafting off | 32,768 | 52.6 | 51.9 |
| Drafter on | 262,144 | 55.0, 2 of 5 at the cap | 34.1 |
| Drafter on | 32,768 | 68.7, 3 of 5 at the cap | 32.5 |

- **With drafting off the context setting made no difference.** So the drop from finding 30's 59.3 tok/s at a 4K prompt to 51.9 here comes with the longer prompt.
- **With the drafter on, greedy code moved with reply length again.** Counting only full replies, it wrote 71.8 at 262,144 and 74.5 at 32,768. With the sampler the drafter was slower on 5 of 5 pairs at 32,768 too, middle ratio 0.62.
- **The reading was the same.** Code read at 3,157 tok/s with drafting off at 32,768, against 3,163 at 262,144.

## The setup

ELI5: Strata's own setup and pack, as in finding 30, with the context widened to the largest size in setup's own list.

- **Engine.** [Strata](https://github.com/Niko1221/Strata) 0.2.20, published 23 Nov 2026 07:20 SGT, tag `v0.2.20` at commit a34979fc. `strata-inkling` 0.1.66 compiled on this Mac by Strata's `./setup.sh` with `--build`, the build of finding 30. It was still the newest release on GitHub on 24 Nov 2026 at 12:30 SGT.
- **Pack.** Strata's own Inkling 2 Mini SQ-20, the pack setup picks for this Mac.
- **Config.** Setup's own config for SQ-20, with `--max-context 262144` in place of setup's default 32768. 262,144 is the largest context in setup's list for Inkling 2 Mini (`strata_control/inkling_fit.py`). Nothing else changed. The engine line was `strata-inkling --serve --native <pack> --max-context 262144 --vision <vision file>`, with `--draft dspark` for the drafter and `--draft off` for drafting off.
- **KV cache.** Setup leaves `--kv` at its default, `auto`. The engine log does not name the format it chose. It reported a KV cache of 1,184.0 MiB at 32,768 and 8,352.0 MiB at 262,144. Both sizes fit 32 KiB a token plus 160 MiB. 32,768 tokens at 32 KiB is 1,024 MiB, plus 160 is 1,184. 262,144 tokens at 32 KiB is 8,192 MiB, plus 160 is 8,352.
- **Server.** Strata's own `serve/server.py --engine strata --config <config> --host 127.0.0.1 --offline`. No thinking field in the requests, as in finding 30.
- **No saved draft table.** I pointed `STRATA_DRAFT_COSTS_DIR` at a new folder for each job, and it stayed empty, as in finding 30.

| Run id | Setting | Prompt tokens | Started, SGT, 24 Nov 2026 |
|---|---|---|---|
| `499646e1e300` | Drafter on, context 262,144 | 18,849 to 255,376 | 09:43 |
| `5b0ad10030e7` | Drafting off, context 262,144 | 18,849 to 255,376 | 10:59 |
| `3fddb5e2a63e` | Drafter on, context 32,768 | about 19K to 20K | 12:21 |
| `6636f24fc61e` | Drafting off, context 32,768 | about 19K to 20K | 12:25 |

## How I measured

ELI5: The same Mac, harness and prompts as finding 37.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time, replies capped at 512 tokens.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** is temperature 1.0 and top-p 1.0, as in finding 30.
- **Repeats.** 5 timed runs per cell. Each test, greedy code or sampled mixed, began with one warm-up request on mixed text with a 16-token reply, on a prompt of about 19K tokens. A minute's pause came before the first test of each job.
- **Prompts.** The same seeds as finding 37, so each cell reads the same bodies of text. The code prompts did not repeat text. The mixed prompts repeat 0% to 4% of their characters at 20,122 tokens and 12% to 15% at 242,129, as finding 37 measured.
- **Not fully quiet.** The drafter on arm at 262,144 had work beside it. I ran the repository's unit tests twice, about two minutes each, and built finding 37's page. Those overlapped 4 greedy code rows, at 255,376 tokens repeat 0, 18,849 repeat 1, 43,260 repeat 1 and 169,677 repeat 2, and the first 11 s of reading at 255,376 repeat 2. They wrote 27.9, 78.1, 53.1, 30.8 and 31.5 tok/s, none of them the slowest in its cell. I also wrote and rendered files and loaded one web page in a browser beside this arm, light work. The drafting off arm and the control ran with nothing beside them.

## No `mlx-lm` multiple

- **`mlx-lm` 0.32.2 has no Inkling 2 model**, as findings 21 and 30 note. Drafting off is the baseline.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every middle.

- **`rows.csv`.** 128 raw rows from the bench database, 8 warm-ups included and marked.
- **`runs.csv`.** The 4 runs, with engine, version, start time and settings. A run's settings line names its first test. Each row's own sampler is in its `extra` column.
- **Targets and tokens.** `summarize.py` names each cell by the harness's target, 16384 to 196608. The tables here name them by measured tokens. Each row of `rows.csv` has both.

From the top of this repository.

```bash
python3 tools/summarize.py findings/38_inkling2_mini_long_prompts_strata
```

## What I did not verify

- **Reply text.** Each request opens with its own random session line, so the two arms never read exactly the same prompt, and the traces keep timings, not text. Finding 30 found that 86 of 100 short replies match with the drafter on and off. I did not check that here.
- **Answer quality at length.** I did not ask questions about the long text or grade any reply.
- **Contexts above 262,144.** Setup's file sets a ceiling of 1,048,576 (`MAX_CONTEXT` in `inkling_fit.py`), but its list stops at 262,144, so I stopped there.
- **Other KV formats, packs and Strata's ready-made engine.** Only `--kv auto`, the SQ-20 pack and this build were run.
- **Two users at once.**

## Credit

- **Engine and the SQ-20 pack.** [Strata](https://github.com/Niko1221/Strata) by Niko1221 on GitHub.
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
