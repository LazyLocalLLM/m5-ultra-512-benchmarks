# Finding 4. DeepSeek V4.1 Flash on TensorFold 1.3.0 against 1.2.10

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold 1.3.0 came out on 20 Nov 2026 with a faster prompt kernel for DeepSeek V4.1 on Macs. I ran the new version and the one before it on the same Mac, the same files and the same prompts, a few hours after the release. Then I looked at how fast each reads a prompt, how fast each writes, and whether the writing is smooth.

**TensorFold 1.3.0 read DeepSeek V4.1 Flash prompts 3% to 11% faster than 1.2.10 in all eleven cells, on two server starts of each version run in both orders. With drafts on it wrote at the same speed within the spread of the runs, 70.5 against 69.5 tok/s greedy on code at a 1K prompt. 17 of 68 replies on 1.3.0 held one pause of 0.25 to 0.58 s between two tokens. None of 68 did on 1.2.10. With drafts off, on one start of each version, 9 of 10 replies on 1.3.0 held one to four pauses and it wrote 40.5 tok/s against 44.7 on 1.2.10. Mac Studio M5 Ultra 512 GB, the maker's own files, one user, median of 5 runs, 20 Nov 2026.**

Updated 20 Nov 2026 19:27 SGT with the second pair of starts and the drafts-off runs. The first version of this page had one start of each version.

## Chart

ELI5: How many prompt tokens a second each version reads, at three prompt sizes, on the first pair of starts. Higher is better.

![Horizontal bars of prefill speed in tokens per second for DeepSeek V4.1 Flash on TensorFold at 1K, 4K and 32K prompts. Version 1.2.10 reads 662.0, 986.4 and 1,334.1. Version 1.3.0 reads 707.8, 1,042.4 and 1,379.8.](chart_prefill.png)

## Reading the prompt

ELI5: Prefill is prompt tokens over the wait for the first token. Both versions got the same prompts, so each row is a like for like pair.

| Block | Prompt | Prompt tokens | 1.2.10 tok/s | 1.3.0 tok/s | 1.3.0 over 1.2.10 | First token, 1.2.10 | First token, 1.3.0 |
|---|---|---|---|---|---|---|---|
| Code, 512-token replies | 1K | 856 | 662.0 | 707.8 | 1.07 | 1.3 s | 1.2 s |
| Code, 512-token replies | 4K | 4,098 | 986.4 | 1,042.4 | 1.06 | 4.2 s | 4.0 s |
| Code, 512-token replies | 32K | 31,666 | 1,334.1 | 1,379.8 | 1.03 | 25.2 s | 23.6 s |
| Code, 128-token replies | 1K | 856 | 647.5 | 714.1 | 1.10 | 1.3 s | 1.2 s |
| Code, 128-token replies | 4K | 4,097 | 1,024.3 | 1,079.7 | 1.05 | 4.1 s | 3.8 s |
| Code, 128-token replies | 32K | 31,662 | 1,259.9 | 1,363.5 | 1.08 | 25.4 s | 23.2 s |
| Code, 128-token replies, 3 runs | 126K target | 115,186 | 1,285.4 | 1,360.1 | 1.06 | 90.0 s | 84.7 s |

- **1.3.0 was faster in all seven cells** of the first pair, by 3% to 10%.
- **Prompt by prompt, 1.3.0 read 29 of the 30 prompts up to 32K faster.** The middle ratio of those 30 pairs is 1.07. The ratios run from 0.96 to 1.20.
- **At the longest prompt the two did not overlap.** The three 1.2.10 runs read 1,279.4 to 1,307.4 tok/s and the three 1.3.0 runs 1,352.0 to 1,372.9.
- **The release notes say the prompt attention kernel is about 1.5 times faster.** That is one kernel. These rows time the whole prompt, which has other parts, so the two figures measure different things.

### Second pair, reverse order

ELI5: The first pair ran 1.3.0 first. To rule out a run-order effect I ran both again with 1.2.10 first, on fresh server starts.

| Block | Prompt | Prompt tokens | 1.2.10 tok/s | 1.3.0 tok/s | 1.3.0 over 1.2.10 | First token, 1.2.10 | First token, 1.3.0 |
|---|---|---|---|---|---|---|---|
| Code, 512-token replies | 1K | 855 | 661.3 | 731.4 | 1.11 | 1.3 s | 1.2 s |
| Code, 512-token replies | 4K | 4,101 | 990.5 | 1,069.2 | 1.08 | 4.1 s | 3.8 s |
| Code, 512-token replies | 32K | 31,665 | 1,334.7 | 1,435.4 | 1.08 | 23.8 s | 22.8 s |
| Mixed, sampled, 512-token replies | 4K | 4,109 | 997.1 | 1,030.6 | 1.03 | 4.1 s | 4.0 s |

- **The gain repeated in the other order.** 1.3.0 was faster in all four cells, by 3% to 11%.
- **Prompt by prompt, 1.3.0 read 17 of these 20 faster.** The middle ratio is 1.07, the same as in the first pair. The ratios run from 0.97 to 1.18.

## Writing the reply

ELI5: Decode is tokens a second from the first reply token to the last. Each cell is the middle of 5 runs, with the slowest and fastest in brackets.

| Test | Prompt | 1.2.10 tok/s | 1.3.0 tok/s |
|---|---|---|---|
| Greedy, code, 512-token replies | 1K | 69.5 (59.7 to 72.9) | 70.5 (65.9 to 73.9) |
| Greedy, code, 512-token replies | 4K | 69.7 (63.7 to 83.5) | 68.1 (64.8 to 76.2) |
| Greedy, code, 512-token replies | 32K | 65.5 (53.6 to 66.9) | 60.7 (55.3 to 72.3) |
| Greedy, code, 128-token replies | 1K | 62.2 (53.4 to 64.9) | 62.6 (56.7 to 66.0) |
| Greedy, code, 128-token replies | 4K | 55.9 (46.6 to 60.1) | 55.7 (53.3 to 61.1) |
| Greedy, code, 128-token replies | 32K | 53.2 (48.0 to 62.6) | 52.6 (47.2 to 57.7) |
| Greedy, code, 128-token replies, 3 runs | 126K target | 47.7 (46.8 to 49.3) | 50.7 (48.5 to 55.7) |
| Greedy, prose, 512-token replies | 1K | 56.0 (52.6 to 59.0) | 54.3 (50.6 to 55.2) |
| Greedy, mixed, 512-token replies | 1K | 55.0 (55.0 to 59.1) | 54.8 (54.1 to 60.2) |
| Sampled, mixed, 512-token replies | 4K | 46.9 (44.3 to 52.8) | 44.5 (41.1 to 48.2) |

- **Max.** 70.5 tok/s on 1.3.0 and 69.7 on 1.2.10, greedy on code with 512-token replies. [Finding 6](../06_dsv41_tensorfold_130_max_push) pushes this on 1.3.0 with longer replies, a copy task, a counting toy and six draft settings.
- **Median.** 46.9 tok/s on 1.2.10 and 44.5 on 1.3.0, temperature 1.0 and top-p 1.0 on mixed text at a 4K prompt.
- **No cell separates the versions.** The ranges overlap in every row.
- **The second pair agrees.** Greedy on code with 512-token replies, 1.2.10 wrote 67.3, 72.1 and 63.3 tok/s at 1K, 4K and 32K, and 1.3.0 wrote 71.7, 68.8 and 67.9. Sampled on mixed text at 4K, 47.1 against 46.1. The ranges overlap in all four cells.
- **Same answers.** The two versions gave the same 250 greedy answers, 250 of 250 by hash.

## Pauses in the reply

ELI5: A reply should arrive as a steady stream. I looked for the longest wait between two tokens in each reply.

| Version | Drafts | Run | Timed replies | Replies with a gap over 0.2 s | Longest gap in any reply |
|---|---|---|---|---|---|
| 1.3.0 | Defaults | `778e5c808b88`, first pair | 48 | 11 | 0.58 s |
| 1.2.10 | Defaults | `de57ae5ff90f`, first pair | 48 | 0 | 0.13 s |
| 1.2.10 | Defaults | `2dbb544cad36`, second pair | 20 | 0 | 0.12 s |
| 1.3.0 | Defaults | `67e0a002783d`, second pair | 20 | 6 | 0.58 s |
| 1.3.0 | Off | `2436b815e3d3` | 10 | 9 | 0.50 s |
| 1.2.10 | Off | `933f466ec298` | 10 | 0 | 0.03 s |

- **In the first pair, 11 replies on 1.3.0 each held one gap of 0.25 to 0.58 s.** All 11 were 512-token replies, out of 30. The gap came 3.4 to 6.7 s after the reply began.
- **The second pair shows the same.** 6 of 20 replies on 1.3.0 each held one gap of 0.26 to 0.58 s, 3.3 to 8.8 s after the reply began. None of 20 did on 1.2.10. So with drafts on it is 17 of 68 replies on 1.3.0 and 0 of 68 on 1.2.10.
- **No 128-token reply had one**, on either version. Those replies end within about 2.5 s.
- **With drafts on the cost is small.** The 11 gaps of the first pair add up to 4.5 s across the run. Each gap took 2.7% to 7.8% of the writing time of its own reply.
- **I did not look for the cause in this run.** Single gaps of 0.69 to 0.84 s were reported on two earlier commits of pull request #3351 in [ashhart/TensorFold#3547](https://github.com/ashhart/TensorFold/issues/3547) on 18 Nov 2026. The pull request changed after that and was merged on 20 Nov 2026 at a1cb6b85. The changelog names #3351 for the new prompt attention kernel. Whether today's shorter gaps are the same effect is not shown here.
- **The first two rows of the table ran a longer grid**, with 128-token replies and the 126K cell. The second pair ran 512-token replies only.
- **`gaps.csv` lists every reply** with its longest gap, its middle gap, each gap over 0.2 s and when it came. `rows.csv` holds the longest gap too, in the column `max_gap_s`.

## Drafts off

ELI5: Drafts are the engine's guesses at the next few tokens, and they are on by default. I switched them off with `--no-drafts` on both versions to see whether the pauses come from drafting. This is a check, not the setup to use.

Greedy at temperature 0, code, 512-token replies, drafts off, tok/s.

| Version | Run | 1K prompt | 4K prompt | Replies with a gap over 0.2 s |
|---|---|---|---|---|
| 1.2.10 | `933f466ec298` | 44.7 (44.6 to 44.8) | 44.5 (44.4 to 44.6) | 0 of 10 |
| 1.3.0 | `2436b815e3d3` | 40.5 (39.0 to 41.0) | 41.5 (40.6 to 44.3) | 9 of 10 |

- **The pauses do not need drafts.** With drafts off, 9 of 10 replies on 1.3.0 held one to four gaps of 0.21 to 0.50 s, 27 gaps in all. On 1.2.10 the longest gap in any reply was 0.03 s.
- **With drafts off 1.3.0 wrote slower.** 40.5 against 44.7 tok/s at 1K. That is 40.5 / 44.7 = 0.91 times. At 4K, 41.5 / 44.5 = 0.93 times.
- **The pauses account for most of that.** The 27 gaps add up to 9.6 s over 10 replies, about 1.0 s a reply. The middle reply took 12.55 s on 1.3.0 and 11.46 s on 1.2.10, which is 1.09 s apart.
- **One server start for each version here**, 1.3.0 first.
- **Drafts on is the setup to use.** It wrote 70.5 tok/s on the same test, and there the two versions are level.

## Reference points

ELI5: Apple's own server does not read these files, so there is no baseline bar. Two earlier findings ran the same model in other files on other engines.

- **`mlx-lm` is not a baseline for this model here.** Version 0.32.2 refused the MLX build of DeepSeek V4.1 on 13 Nov 2026, as finding 3 notes, and these are the maker's own FP8 files. So no multiple of `mlx-lm` can be given.
- **Finding 3, different weights and engine.** oMLX 0.8.0 on the oQ4e-mtp build wrote 71.2 tok/s greedy on code at 1K and 56.5 sampled on mixed text at 4K, on the same harness and the same day.
- **Finding 2, different weights and engine.** mlx-serve 26.11.2 on the Lossless pack wrote 58.3 tok/s sampled on mixed text at 4K on 17 Nov 2026.

## The setup

ELI5: One build of each version from its release tag, the same model files, the same command.

- **Added 22 Nov 2026 04:45 SGT.** TensorFold's main branch at commit 1093b795, which is in no release yet, was run against 1.3.0 on 22 Nov 2026. That is [finding 17](../17_dsv41_tensorfold_main_1093b795). Later that morning TensorFold 1.3.3, the release that holds the change, was run against 1.3.0 in [finding 18](../18_dsv41_tensorfold_133). The summary page shows that run's 1.3.0 start for the default lines, by my rule of the latest start. The figures on this page are unchanged.
- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) `tensorfold-dsv41`, built from source at each release tag with Zig 0.17.0 and `zig build dsv41-metal-serve -Dcpu=apple_m1`. Version 1.3.0 is commit d3d0bf11, released 20 Nov 2026 07:04 SGT. Version 1.2.10 is commit 2a674b55. The project calls this server experimental, switched on with `TF_EXPERIMENTAL=deepseek`.
- **Weights.** [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) @ 08c8657f, the maker's FP8 and MXFP4 files, with the Engram rows packed for TensorFold 1.2.8. Both versions checked those rows against the release and accepted them.
- **Serve command**, the same for both.

```bash
tensorfold-dsv41 serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 131072 --parallel 1 --no-update-check
```

- **Drafts** at the engine's defaults. Those logs read "drafts: DSpark + copies" and "depth: cost, cap 5". The two drafts-off starts add `--no-drafts` to the command, and their logs read "drafts: off".
- **Thinking** off.

| Run id | Version | Started, SGT |
|---|---|---|
| `778e5c808b88` | 1.3.0 | 20 Nov 2026 15:29 |
| `de57ae5ff90f` | 1.2.10 | 20 Nov 2026 16:00 |
| `2dbb544cad36` | 1.2.10, second pair | 20 Nov 2026 18:31 |
| `67e0a002783d` | 1.3.0, second pair | 20 Nov 2026 18:37 |
| `2436b815e3d3` | 1.3.0, drafts off | 20 Nov 2026 19:18 |
| `933f466ec298` | 1.2.10, drafts off | 20 Nov 2026 19:20 |

## How I measured

ELI5: Same Mac, same harness and same text rules as the earlier findings.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Sampled** means temperature 1.0 and top-p 1.0.
- **Text.** Code, prose, or a mix, from open-source docs and code. The text of a request is picked from its size and repeat number, so both versions got the same prompts. Each prompt starts with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **The 126K cell has 3 runs.** Two of its five prompts came to 131,444 and 142,222 tokens, past the 131,072-token window. Both versions refused them with a clear message. The harness sized the code text too long. The four refused requests are in `rows.csv`.
- **Order.** In the first pair 1.3.0 ran first, 15:29 to 15:51 SGT, and 1.2.10 second, 16:00 to 16:23 SGT. In the second pair 1.2.10 ran first, from 18:31 SGT, and 1.3.0 second, from 18:37 SGT. Every run is its own server start.
- **Other work on the Mac.** From about 16:04 to 16:11 SGT a light job was reading source files on this Mac, during the 1.2.10 run. The 1.2.10 prompts read before it began show the same gap to 1.3.0 as those read during it, a middle ratio of 1.07 in both groups.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 178 raw rows from the bench database. The 156 timed replies, the 4 refused requests and the 18 warm-ups.
- **`runs.csv`.** The 6 runs behind them, with engine, version, start time, settings and sampling.
- **`gaps.csv`.** One line for each of the 156 timed replies, made from the arrival time of every streamed piece. The `drafts` column says whether drafts were at defaults or off.

From the top of this repository.

```bash
python3 tools/summarize.py findings/04_dsv41_tensorfold_130
```

## What I did not verify

- **The 1.5 times figure for the kernel itself.** I timed whole prompts, not one kernel.
- **The cause of the pauses.** They appear with drafts on and off on 1.3.0 and on neither with 1.2.10. I did not trace them further.
- **A second start with drafts off.** That check ran once for each version.
- **The long grid on a second start.** The 128-token and 126K cells ran in the first pair only.
- **A measured draft cost table.** TensorFold can price drafts from a table measured on the serving Mac (`TF_DSV41_CALIB_FILE`). Its notes put the gain at 0.7% greedy and 2.4% sampled on an M5 Ultra. I ran the built-in table.
- **Peak memory.** This run did not log it.
- **Thinking on.**

## Credit

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Model.** DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
