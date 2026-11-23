# Finding 29. Inkling 2 Mini on MTPLX 2.13.2, 2.8 times as fast with top-p 0.95

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Updated on 23 Nov 2026 at 12:08 SGT with a test at top-p 0.95, run from 11:51 SGT, and a new headline.

ELI5: MTPLX 2.13.2 came out on 23 Nov 2026 at 09:24 SGT. [Finding 21](../21_inkling2_mini_mtplx_213) measured 2.13.1 on Inkling 2 Mini's three packs. I reran its lines on 2.13.2 and ran both releases back to back on the Bare Speed pack, on the same texts. Its notes say a request that sets top-p or top-k now stays on the fast decoder. My sampler sends top-p 1.0, which never left it, so I also ran both releases at top-p 0.95.

**MTPLX 2.13.2 writes Inkling 2 Mini 2.8 times as fast as 2.13.1 when a request sets top-p 0.95, as its notes say. On the Bare Speed pack at a 4K prompt it wrote 122.0 tok/s against 42.9, over 10 runs a release, and it was faster on 20 of 20 same-text pairs. Top-p 0.95 cut 2.13.1 to 0.36 of its own speed at top-p 1.0, and left 2.13.2 where it was. At top-p 1.0, the model's own sampler, and on greedy code, 2.13.2 shows no change I can call: 123.9 against 120.6 with the sampler and 152.1 against 153.9 on long code at 1K. All 50 short greedy questions, asked twice, give the same replies on both releases on all three packs. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Pack and setting | Max on 2.13.2 | Max on 2.13.1 | Median on 2.13.2 | Median on 2.13.1 |
|---|---|---|---|---|
| Bare Speed, draft head on | 153.0 | 159.7 | 124.7 | 130.0 |
| Optimized Speed, draft head on | 152.0 | 148.0 | 113.0 | 115.1 |
| Optimized Quality, draft head on | 133.8 | 136.5 | 105.6 | 106.7 |
| Bare Speed, draft head off | 89.9 | 90.1 | 78.9 | 78.5 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The 2.13.2 figures are each setting's latest start.** The 2.13.1 columns are the summary's lines from finding 21, run on 22 Nov 2026.
- **Almost every reply here is reasoning text.** With no thinking field, Inkling 2 Mini thinks first, and most replies end inside the thinking, as in finding 21.
- **The Bare Speed gap is start to start.** Tonight's two 2.13.1 starts against its 22 Nov start read middle ratios of 0.92 to 1.07, about 1.00. Its max read 170.2 and 150.9 tonight and 159.7 then. Its sampler read 121.7 and 119.0 tonight and 130.0 then.
- **What this page can see.** Single starts spread by 0.93 to 1.06 text by text, so a change under about 5% would not show. The draft-off line is the tight one.
- **The summary page moves.** Bare Speed's median leaves second place in daily use, 130.0 to 124.7. Neither line is a release change.
- **Not rerun.** Optimized Speed and Optimized Quality with the draft head off keep their 2.13.1 lines.
- **No `mlx-lm` multiple.** `mlx-lm` 0.32.2 has no Inkling 2 model, as finding 21 notes. The draft head off is the baseline.

## Chart

ELI5: Both releases on the Bare Speed pack, two starts each, back to back. Each bar is the middle of the 10 runs of a release's two starts.

![Paired bars of writing speed in tokens per second for Inkling 2 Mini Bare Speed, MTPLX 2.13.1 against 2.13.2, the middle of 10 runs over two starts each. Long code at 1K, 153.9 and 152.1. Long code at 4K, 148.7 and 147.5. Short code at 1K, 137.4 and 142.7. The model's own sampler at 4K, 120.6 and 123.9.](chart_bare.png)

## Top-p 0.95, the notes' change

ELI5: Top-p 0.95 means the sampler drops the least likely tokens, those outside the top 95% of the chances, before it picks one. At a temperature above 0, 2.13.1 left its fast decoder for any top-p below 1.0 or top-k above 0, by `mtplx/models/inkling/fast/round.py` at that tag, where it returns "filtered_sampler". 2.13.2 removed that condition. Here are both releases at top-p 0.95, two starts each, back to back.

![Paired bars of writing speed in tokens per second for Inkling 2 Mini Bare Speed, MTPLX 2.13.1 against 2.13.2, the model's sampler at temperature 1.0, the middle of 10 runs over two starts each. Top-p 1.0 at 4K, 120.6 and 123.9. Top-p 0.95 at 4K, 42.9 and 122.0. Top-p 0.95 at 1K, 45.6 and 129.7.](chart_topp.png)

Decode tok/s, temperature 1.0 and top-p 0.95, mixed text, 512-token replies. Each cell is the middle of 5 runs.

| Start | Release | 1K prompt | 4K prompt |
|---|---|---|---|
| `571b2f74994a`, 11:51 | 2.13.2 | 115.1 | 132.3 |
| `d7f638f9f0a9`, 11:53 | 2.13.1 | 45.4 | 42.8 |
| `cdb278964e7a`, 11:56 | 2.13.1 | 45.8 | 42.9 |
| `1980bb5c8d3f`, 11:59 | 2.13.2 | 137.7 | 119.2 |

- **2.8 times as fast at 4K.** Over the 10 runs of each release's two starts, 122.0 / 42.9 = 2.84. Text by text, each 2.13.2 start against each 2.13.1 start, faster on 20 of 20 pairs, middle ratio 2.83, from 2.53 to 3.71.
- **At 1K too.** 129.7 / 45.6 = 2.84 by the pooled cells. Text by text, faster on 20 of 20, middle ratio 2.68, from 2.35 to 3.41.
- **Top-p 0.95 is what slowed 2.13.1.** Against its own two starts at top-p 1.0, at 10:14 and 10:20 SGT, on the same 4K texts, it wrote 0.36 as fast, slower on 20 of 20 pairs. 42.9 against 120.6.
- **2.13.2 kept its speed.** Against its own top-p 1.0 starts, middle ratio 0.98, faster on 9 of 20 pairs. 122.0 against 123.9.
- **The requests carried the setting.** Every timed request sent temperature 1.0 and top-p 0.95, by the sampler recorded with each row, and reused 0 cached tokens.
- **MTPLX's own request log shows the path.** On 2.13.1 each top-p 0.95 request logged a decision on the host for a filtered sampler, and drew its drafts at temperature 0. On 2.13.2 the same requests logged their decisions on the device, with top-p 0.95 applied to the drafts. Both logged top-p 0.95 as the setting in effect. From `~/.mtplx/logs`, the last two requests of each release.
- **This is not the pack's own sampler.** The Bare Speed pack's `mtplx_runtime.json` sets temperature 1.0, top-p 1.0 and top-k 0. So a client that sends no sampler ran on 2.13.1's fast path, and the change shows only for clients that set top-p or top-k. The summary page keeps its top-p 1.0 lines, and these rows aren't on it.

## Both releases back to back

ELI5: Four starts on the Bare Speed pack in the order 2.13.2, 2.13.1, 2.13.1, 2.13.2, the same texts each time.

Decode tok/s, greedy unless named. Each cell is the middle of 5 runs.

| Start | Release | Code, 2,048, 1K | Code, 2,048, 4K | Code, 512, 1K | Code, 512, 4K | Own sampler, 4K | Counting, 1K | Copy, 1K |
|---|---|---|---|---|---|---|---|---|
| `3cf8e9e1ecff`, 10:07 | 2.13.2 | 149.2 | 150.4 | 142.7 | 131.2 | 123.0 | 160.6 | 182.5 |
| `26d9d4ea77a2`, 10:14 | 2.13.1 | 170.2 | 144.7 | 135.6 | 137.8 | 121.7 | 187.6 | 199.7 |
| `283eb0d4fdb4`, 10:20 | 2.13.1 | 150.9 | 150.9 | 139.3 | 133.6 | 119.0 | 167.5 | 141.3 |
| `8ddc9a4f863a`, 10:27 | 2.13.2 | 153.0 | 140.4 | 142.8 | 137.3 | 124.7 | 161.9 | 140.3 |

- **Text by text, each 2.13.2 start against each 2.13.1 start.**
  - Long code, middle ratios 0.93 to 1.01, faster on 2 to 5 of 10.
  - Short code, 0.99 to 1.05, faster on 4 to 6 of 10.
  - Own sampler, 1.01 to 1.06, faster on 3 of 5 each time.
- **Two starts of 2.13.1 against each other** read 0.94 to 0.99 on the same tests. So the gaps above are start to start.
- **The counting toy leans lower and can't be called.** Its replies are reasoning text, so it isn't the ceiling it is on other models. Every 2.13.2 counting cell reads below every 2.13.1 cell tonight. Pooled it reads 161.8 against 182.7, and text by text 0.89 and 0.90 against the first 2.13.1 start and 0.98 against the second. The notes' fixed draft depth of 3 would point that way. Two starts a release can't settle it.
- **The copy task can't be called either.** It swings by 0.91 between two starts of one release.
- **The notes change the draft depth.** 2.13.2 drafts 3 tokens a round by default on Inkling 2 Mini, where 2.13.1 chose a depth each round. The notes call 2.13.2 about level on their standard coding prompt, and so do these runs.

## The other packs

ELI5: One 2.13.2 start each, against finding 21's 2.13.1 start of 22 Nov.

- **Optimized Speed.** Text by text, long code 0.99, short code 1.00, the sampler 1.03.
- **Optimized Quality.** Long code 0.97, short code 1.03, the sampler 0.99.
- **Bare Speed with the draft head off.** 1.00 on all three tests. With no drafts this is the plain decode, and it held across the two days.

## Did the text change

- **No.** The same 50 short questions, asked twice, give the same 100 replies on 2.13.2 and 2.13.1, on each of the three packs and with the draft head off. Both 2.13.2 Bare Speed starts agree with each other, and so do the three 2.13.1 Bare Speed starts across both days.
- **The replies hash reasoning and answer together.** Every one ended inside the thinking at 64 tokens.

## The setup

ELI5: MTPLX from source at each tag, the same packs and serve line as finding 21.

- **Engine.** [MTPLX](https://github.com/youssofal/MTPLX) 2.13.2, published 23 Nov 2026 09:24 SGT, not a pre-release, tag `v2.13.2` at commit 3890be55. Installed by `uv sync --locked` from the tag into its own folder. Its `pyproject.toml` and `uv.lock` change only the version line from 2.13.1. `mtplx --version` prints 2.13.2.
- **It was still the newest release** when I published this, checked on 23 Nov 2026 at 12:08 SGT.
- **2.13.1** is finding 21's install, commit cf39588f, kept in its own folder.
- **Serve line.** `mtplx serve --model <pack> --host 127.0.0.1 --port <port> --context-window 131072 --no-stats-footer`, and `--no-mtp` for the draft head off. No thinking field in the requests.
- **Packs.** The three Inkling 2 Mini packs of finding 21, Bare Speed, Optimized Speed and Optimized Quality.
- **The top-p 0.95 runs** read the Bare Speed files in place under the same served name. The only change is top-p 0.95 in the sampler, the value in the notes.
- **Saved state.** MTPLX keeps a folder in the home directory, `~/.mtplx`. It holds kernel proofs, which got new files during these runs, and a session bank of saved conversations. Each timed prompt opens with a new session line, and every timed request reused 0 cached tokens. The answer check repeats its prompts by design.

| Run id | Release | Pack and setting | Started, SGT, 23 Nov 2026 |
|---|---|---|---|
| `3cf8e9e1ecff` | 2.13.2 | Bare Speed | 10:07 |
| `26d9d4ea77a2` | 2.13.1 | Bare Speed | 10:14 |
| `283eb0d4fdb4` | 2.13.1 | Bare Speed | 10:20 |
| `8ddc9a4f863a` | 2.13.2 | Bare Speed | 10:27 |
| `db1ba3d496e1` | 2.13.2 | Optimized Speed | 10:34 |
| `7ea5b8ae2d9e` | 2.13.2 | Optimized Quality | 10:40 |
| `f41fca789e86` | 2.13.2 | Bare Speed, draft head off | 10:46 |
| `571b2f74994a` | 2.13.2 | Bare Speed, top-p 0.95 | 11:51 |
| `d7f638f9f0a9` | 2.13.1 | Bare Speed, top-p 0.95 | 11:53 |
| `cdb278964e7a` | 2.13.1 | Bare Speed, top-p 0.95 | 11:56 |
| `1980bb5c8d3f` | 2.13.2 | Bare Speed, top-p 0.95 | 11:59 |

## How I measured

ELI5: Same Mac, same harness, same texts and same questions as finding 21.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** is temperature 1.0 and top-p 1.0, as in finding 21. **Top-p 0.95** is temperature 1.0 and top-p 0.95.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. Each prompt opens with a new session line so no prompt cache can hit.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request. A minute's pause followed the unit tests before the first timed start of each job.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.
- **Not fully quiet.** I wrote files beside the job, light work.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 332 raw rows from the bench database. 295 timed requests and 37 warm-ups.
- **`runs.csv`.** The 11 runs, with engine, version, start time, settings and sampling.
- **The 2.13.1 rows of 22 Nov** are in finding 21.
- **The answer checks are not in `rows.csv`.** They are hashes of untimed replies.

From the top of this repository.

```bash
python3 tools/summarize.py findings/29_inkling2_mini_mtplx_2132
```

## What I did not verify

- **Top-k.** I tested top-p 0.95 only. The notes' change covers top-k too.
- **Whether the sampled replies at top-p 0.95 match between releases.** The traces keep timings, not text.
- **Other packs at top-p 0.95.** I ran Bare Speed only.
- **Whether the counting toy is slower on 2.13.2.**
- **The draft-off lines** of Optimized Speed and Optimized Quality on 2.13.2.
- **Answer text.** With no thinking field the replies are reasoning. I did not time answers with thinking switched off.
- **Answer quality, long prompts, and two users at once.**

## Credit

- **Engine and packs.** [MTPLX](https://github.com/youssofal/MTPLX) by [@Youssofal_](https://x.com/Youssofal_).
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
