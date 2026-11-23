# Finding 28. Strata 0.2.20 on Qwen3.8 Flash Next IQ3_S, level with 0.2.19, and its saved draft table

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: Strata 0.2.20 came out on 23 Nov 2026 at 07:20 SGT. [Finding 24](../24_qwen38_flash_next_strata_0219) measured 0.2.19 at 02:22 SGT, so I reran its lines on 0.2.20 and ran both releases back to back from 08:42 SGT. On the way I found a second thing. Strata saves a table of what each draft size costs on this Mac, learned from a setting's first requests, and every later start reads it. Which table a start reads moved its speed more than the release did.

**Strata 0.2.20 writes at the same speed as 0.2.19 on Qwen3.8 Flash Next IQ3_S. With MTP on and each release reading a table learned from the same requests, 0.2.20 wrote 181.7 and 181.6 tok/s at the max and 0.2.19 wrote 182.7, with middle ratios of 0.99 to 1.00 on every greedy test. With no table, and with MTP off, the two were level too. The table made the gap. The one 0.2.19 saved at 02:28 SGT on finding 24's first start priced a 3-token check at 29.5 ms, twice the 14.8 and 15.6 ms of the tables learned from 08:42 SGT. It made later 0.2.19 starts 6 to 7% slower on long code, 169.7 and 172.4. That cost was measured on a slow first request. The same first request on a quiet Mac at 11:02 SGT measured 14.9 ms on both releases. It explains finding 24's 183.3 against 173.8. 0.2.20 changes 2 of 50 short answers. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Setting | Max on 0.2.20 | Max on 0.2.19 | Median on 0.2.20 | Median on 0.2.19 |
|---|---|---|---|---|
| Setup's config, MTP on, a table from the same requests | 181.6 | 182.7 | 126.0 | 131.9 |
| Setup's config, MTP on, no table yet | 183.4 | 180.3 | 134.1 | 131.8 |
| MTP off | 98.7 | 99.1 | 95.1 | 94.7 |
| `--spec 4` | 189.2 | 193.6 | not run | not run |
| `--spec 5` | 196.4 | 200.3 | not run | not run |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The first three rows ran back to back,** 23 Nov 2026 from 08:42 to 10:02 SGT. The `--spec` rows for 0.2.19 are finding 24's, from 02:36 and 02:39 SGT the same day, one start each.
- **0.2.19 read up to 3% higher from 02:22 to 02:39 SGT than from 08:42.** With no table, setup's config read 183.3 then and 180.3 at 09:37, slower on 9 of 10 long code pairs with a middle ratio of 0.97. The counting toy read 203.0 and 202.8. MTP off read 100.6 and 99.1. I give no cause. So the `--spec` rows can't compare closer than about 3%.
- **The summary page moves** from 200.3 to 196.4 at the max and from 136.5 to 126.0 at the median, and IQ3_S leaves second place in daily use. Neither is a release change. The max is one `--spec 5` start a release, at different times of day. The median is 0.2.20's latest start of setup's config, which read a saved table.
- **The medians move with the start.** Text by text, 0.2.20's latest start against 0.2.19's start with a table from the same requests was faster on 2 of 5 sampled texts, middle ratio 0.99.
- **No `mlx-lm` multiple.** `mlx-lm` reads MLX weights, and this pack is GGUF. llama.cpp read the same files in finding 24 and wrote 58.2 and 55.7.

## Chart

ELI5: The top speed on new code at a 1K prompt, both releases. Each pair is named by the table 0.2.19 read. 0.2.20 read none in the first pair and its own table from 08:48 SGT in the other two. Every bar ran on 23 Nov 2026 between 08:42 and 10:02 SGT.

![Bars of writing speed in tokens per second for Qwen3.8 Flash Next IQ3_S, greedy, new code, replies of up to 2,048 tokens, 1K prompt, Strata 0.2.19 against 0.2.20. No table, 180.3 and 183.4. 0.2.19 reading its table from 09:42 SGT and 0.2.20 its table from 08:48 SGT, 182.7 and 181.6. 0.2.19 reading its table from 02:28 SGT and 0.2.20 its table from 08:48 SGT, 169.7 and 181.7.](chart_max.png)

- **The third pair is what a user saw at 08:49.** Both releases at their defaults, each reading the table it saved earlier. It looks like a 7% win for 0.2.20. The second pair shows it is the table.

## Both releases back to back

ELI5: Seven starts of setup's config, in the order they ran. Each says which saved table it read.

Decode tok/s, greedy unless named, 512-token replies unless named.

| Start | Release | Table it read | Code, 2,048, 1K | Code, 2,048, 4K | Code, 1K | Code, 4K | Own sampler, 4K | Counting, 1K | Copy, 1K |
|---|---|---|---|---|---|---|---|---|---|
| `a688a6002ffd`, 08:42 | 0.2.20 | none yet | 183.4 | 175.2 | 173.3 | 166.8 | 134.1 | 202.4 | 237.5 |
| `f76501d66746`, 08:49 | 0.2.19 | from 02:28 | 169.7 | 167.3 | 169.6 | 158.7 | 127.9 | 201.8 | 235.2 |
| `6a841ce2238b`, 08:55 | 0.2.19 | from 02:28 | 172.4 | 163.2 | 168.9 | 162.0 | 126.1 | 201.3 | 233.2 |
| `c47488b9bf26`, 09:01 | 0.2.20 | its own, from 08:48 | 181.7 | 173.4 | 169.4 | 164.2 | 129.7 | 202.5 | 238.1 |
| `b1ff7ad1f607`, 09:37 | 0.2.19 | none, a new folder | 180.3 | 173.7 | 174.7 | 160.7 | 131.8 | 202.8 | 238.3 |
| `7e217b40d9c3`, 09:43 | 0.2.19 | its own, from 09:42 | 182.7 | 175.2 | 173.3 | 164.1 | 131.9 | 202.8 | 237.0 |
| `8b55935c332e`, 09:56 | 0.2.20 | its own, from 08:48 | 181.6 | 173.3 | 171.7 | 166.7 | 126.0 | 202.6 | 237.9 |

- **Like for like, level.** Each 0.2.20 start that read a table against the 0.2.19 start of 09:43, which read one learned from the same requests, gives middle ratios of 0.99 to 1.00 on every greedy test. With the sampler they read 0.97 and 0.99.
- **With no table, level.** The 0.2.20 start of 08:42 against the 0.2.19 start of 09:37 gives 1.00 to 1.02.
- **The table from 02:28 was the slow one.** The 0.2.19 start of 09:43 against each start that read it was faster on 10 of 10 long code pairs, with middle ratios of 1.06 and 1.07.
- **The counting toy moved about 1%,** 201.3 to 202.8 on all seven. The 0.2.19 start of 09:43 was faster on 10 of 10 counting pairs against each start that read the 02:28 table, middle ratio 1.01.
- **First token came a little later on 0.2.20.** With MTP on, every 0.2.20 start gave its first token later than every 0.2.19 start from 08:42 on the 1K code prompts, 60 of 60 pairs. With 512-token replies that was 0.49 to 0.50 s against 0.44 s, middle ratio 1.13. On the counting toy, 0.43 against 0.40, 1.05. At 4K the middle ratio was 1.02 with code and 1.00 with mixed text.
- **Draft acceptance is level.** On the long code replies every start accepted 84.8 to 87.1% of its drafts, by Strata's own log.

## The saved draft table

ELI5: Before Strata checks a batch of guesses, it decides how many to make. A longer batch costs more time to check. Strata measures those costs on real requests and writes them to a small file, so the same request gives the same answer on every start.

- **What Strata's code says.** The table makes output repeatable. It is learned from real requests, and until it exists the engine uses live costs. Its file name follows the model and every engine argument, so each setting gets its own. The engine checks the card, the driver and its own version inside the file. By Strata's source at this tag, `terminal/serve/server.py` and `terminal/serve/server_parts/engines.py`.
- **It is on by default only on Metal.** The code comment says so because the authors measured the table at or above live costs there.
- **Where it lives.** `~/.config/strata/draft-costs`, outside the Strata folder. The environment variable `STRATA_DRAFT_COSTS_DIR` moves it, and `"draft_costs": false` in a config turns it off. Both are in the same code.
- **When it is written.** Strata measures each draft size's cost once, on real requests, and the table takes over when 100 requests have run. On these jobs that was the 99th request, inside the untimed answer check. So a setting's first start is timed on live costs and its later starts on the table. A start that ends sooner still saves a file marked fresh, as the `--spec` starts did after 22 requests.
- **How I tested it.** For the 0.2.19 starts of 09:37 and 09:43 I set `STRATA_DRAFT_COSTS_DIR` to a new empty folder in this project. The first had no table and learned one from the same blocks 0.2.20 had learned from. The second read it.

### What was in the slow table

ELI5: Each table holds one cost for each draft size, in milliseconds a check. Three tables for setup's config, side by side.

| Draft rows checked | 0.2.19, saved 02:28 | 0.2.19, saved 09:42 | 0.2.20, saved 08:48 |
|---|---|---|---|
| 1 | 12.1 | 12.2 | 11.8 |
| 2 | 13.2 | 13.7 | 13.2 |
| 3 | 29.5 | 15.6 | 14.8 |
| 4, scaled, not measured | 17.0 | 19.1 | 19.1 |
| 5 | 18.2 | 18.3 | 18.3 |

- **One measured cost is off.** The 02:28 table prices 3 rows at 29.5 ms, about twice the other two tables, and above its own 5 rows. Setup's window is 3. Its 4-row figure, which Strata scales from the others and does not measure, reads 17.0 against 19.1 in the other two.
- **That cost came from the first request.** The log of finding 24's first start shows the 3-row cost measured on its own, before any other size, during the first request after the server started. That request was a field check with no warm-up before it. It read its 43-token prompt in 614 ms and wrote 137 tokens at 138.0 tok/s. The same request right after read the prompt in 36 ms and wrote at 181.3.
- **The first starts from 08:42 measured it later.** Each began with a 16-token warm-up, and the 3-row cost was measured together with the 1- and 2-row costs, after 1 and 7 requests.
- **The table keeps the first measurement.** The 02:28 file still holds 29.5 for 3 rows after 100 requests.
- **A cold first request alone doesn't repeat it.** At 11:02 SGT I gave each release a new empty table folder and sent the same field check first, with no warm-up, on a quiet Mac. The 3-row cost was again measured on the first request, at 14.9 ms on both. That request read its prompt in 189 ms and wrote at 174.3 tok/s.
- **So the 02:22 first request was slow for another reason.** Finding 24 records that I built and pushed this repository beside that start. That fits, and it may be this bench's doing. It is not shown.
- **Finding 24's two starts.** The first, 183.3, ran on live costs and wrote the table. The second, 173.8, read it. That page now points here.

## MTP off and the wider windows

ELI5: With MTP off the model writes one token a step. Strata still saves a table, of the one-token cost only. Each of the three MTP-off starts was the first for its table folder, so all three ran on live costs.

- **MTP off is level.** Back to back, 0.2.20 at 09:07 against 0.2.19 at 09:49, middle ratios of 1.00 on long and short code and 1.01 with the sampler. 0.2.20 was faster on 1 of 10 long code pairs, 4 of 10 short ones and 3 of 5 sampled.
- **First token is level with MTP off,** 0.47 s at 1K on both releases, middle ratios 1.00 to 1.01. The later first token on 0.2.20 shows only with MTP on. Against finding 24's start of 02:29 it read 0.98. 0.2.19 against itself across those times reads 0.98 to 0.99, slower on 10 of 10 code pairs. So that 0.98 is the time of day.
- **`--spec 4` and `--spec 5`** ran one start each on 0.2.20, 189.2 and 196.4. Against finding 24's starts they read middle ratios of 0.98 and 1.00 on long code. Each was the first start of its setting on its release, so each ran on live costs.
- **`--spec 5` is still the fastest setting I've found**, as on 0.2.19.

## Did the text change

ELI5: The same 50 short questions, asked twice on each start, greedy.

- **0.2.20 changes 2 of the 50 questions,** on both passes, so 96 of 100 replies match 0.2.19. The two replies match for their first 120 characters and end differently later.
- **0.2.20 agrees with itself.** All four 0.2.20 starts, MTP off among them, give the same 100 replies.
- **0.2.19 agrees with itself.** All seven 0.2.19 starts across finding 24 and this page give the same 100, whichever table they read and with MTP off.
- **The table didn't change these replies.** Strata's code says the table is there so the same request gives the same answer on every start. Here the 64-token replies matched whichever table a start read. I did not check longer replies across table states.
- **This says nothing about answer quality.** I did not grade the answers.

## The setup

ELI5: Strata's own setup, run as its docs say, on the same files as finding 24.

- **Engine.** [Strata](https://github.com/Niko1221/Strata) 0.2.20, published 23 Nov 2026 07:20 SGT, not a pre-release, tag `v0.2.20` at commit a34979fc. Built from source on this Mac by its own `./setup.sh` at 08:36 SGT. The engine program prints `strata 0.1.66-metal`.
- **It was still the newest release** when I published this, checked on 23 Nov 2026 at 11:04 SGT.
- **0.2.19** is finding 24's build, tag `v0.2.19` at commit c6f6427d, engine 0.1.65.
- **Setup's script is byte for byte 0.2.19's.** I ran it with finding 24's flags and a new data folder.
- **Setup reused 0.2.19's model files.** The two tools that make them, `terminal/tools/iq_pack.py` and `terminal/tools/mtp_fetch.py`, are byte for byte the same in both releases.
- **How it found them.** It read `~/.config/strata/settings.json`, which the 0.2.19 setup wrote, and used the pack and MTP draft layer already in 0.2.19's data folder. Their file times stayed at 02:04 to 02:05 SGT. So both releases read the very same files, which suits a comparison.
- **The engine flags setup wrote are the same as 0.2.19's.** `--expert-cache 64 --prefill auto --spec 3 --spec-min-p 0.5 --mtp <draft layer> --max-context 65536 --mmap-experts --vision`.
- **Serve command** as finding 24, Strata's Python server with `--offline`, bound to this Mac.
- **Weights.** [ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) @ ed59f920, the IQ3_S files, as finding 24.
- **Sampler.** The maker's thinking-off sampler, temperature 0.7, top-p 0.8, top-k 20 and presence penalty 1.5.
- **Thinking** switched off in every request.

| Run id | Release | Setting | Started, SGT, 23 Nov 2026 |
|---|---|---|---|
| `a688a6002ffd` | 0.2.20 | setup's config | 08:42 |
| `f76501d66746` | 0.2.19 | setup's config | 08:49 |
| `6a841ce2238b` | 0.2.19 | setup's config | 08:55 |
| `c47488b9bf26` | 0.2.20 | setup's config | 09:01 |
| `651e54639f7c` | 0.2.20 | MTP off | 09:07 |
| `88b41d226df3` | 0.2.20 | `--spec 4` | 09:14 |
| `dc88686985f3` | 0.2.20 | `--spec 5` | 09:17 |
| `b1ff7ad1f607` | 0.2.19 | setup's config, table in a new folder | 09:37 |
| `7e217b40d9c3` | 0.2.19 | setup's config, table in that folder | 09:43 |
| `4212761f35de` | 0.2.19 | MTP off, table in that folder | 09:49 |
| `8b55935c332e` | 0.2.20 | setup's config | 09:56 |

## How I measured

ELI5: Same Mac, same harness, same texts and same questions as finding 24.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line, so no prompt cache can hit.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.
- **Not fully quiet.** During the 08:42 start I exported rows from the bench database for another page. Through the runs I wrote files beside the jobs. All light work. Nothing else ran on the GPU.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Say which table a start read.** On this model the table moved long code by 6 to 7%, more than the release.
- **Different times of day.** 0.2.19 read up to 3% higher at 02:22 SGT than from 08:42. Compare the starts from 08:42 with each other.
- **One start each** for MTP off and the wider windows on each release.
- **Max is not what a chat feels like.** The median is the everyday figure.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 450 raw rows from the bench database. 405 timed requests and 45 warm-ups.
- **`runs.csv`.** The 11 runs, with engine, version, start time, settings and sampling.
- **Finding 24's rows** are in its own folder.
- **The answer checks are not in `rows.csv`.** They are hashes of untimed replies.

From the top of this repository.

```bash
python3 tools/summarize.py findings/28_qwen38_flash_next_strata_0220
```

## What I did not verify

- **What slowed the first request of finding 24's first start.** A quiet repeat measured 14.9 ms.
- **Whether a table can be slower than live costs on 0.2.20.** The 08:48 0.2.20 table was level with live costs, 1.01.
- **`"draft_costs": false`.** I moved the table with the environment variable and did not switch it off.
- **Hy4-flash and Inkling 2 Mini on Strata.** 0.2.20 ships engines for both. I ran neither.
- **Answer quality, long prompts, and two users at once.**

## Credit

- **Engine.** [Strata](https://github.com/Niko1221/Strata) by Niko1221 on GitHub.
- **Weights.** The GSQ-RCO GGUF build by [ISTA-DASLab](https://huggingface.co/ISTA-DASLab).
- **Model.** Qwen3.8 Flash Next by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
