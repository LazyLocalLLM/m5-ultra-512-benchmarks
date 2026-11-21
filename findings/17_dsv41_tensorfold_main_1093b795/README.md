# Finding 17. DeepSeek V4.1 Flash on TensorFold main at 1093b795, not in a release yet

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold's author posted that DeepSeek V4.1 Flash now writes much faster on an M5 Ultra 512 GB. The change behind that, pull request 3405, merged into the project's main branch on 22 Nov 2026 at 01:37 SGT. No release holds it yet. I built main at that commit and ran it against 1.3.0 on the same night and the same texts, two server starts each. When a release ships with it, I will rerun on the release and update this page.

**TensorFold main at 1093b795, not in a release yet, wrote 105.5 tok/s on DeepSeek V4.1 Flash at its max and 71.2 with the model's own sampler. TensorFold 1.3.0 wrote 74.5 and 44.6 on the same night, so main is 1.42 and 1.60 times as fast. It was faster on every same-text pair, 58 of 58 and 55 of 55, on two starts. The answers did not change. 250 of 250 short greedy answers match 1.3.0, and so do the replies to the author's own 16 prompts, greedy and sampled. On those 16 prompts I measured 102.3 tok/s, within 1% of the pull request's own table. Mac Studio M5 Ultra 512 GB, the maker's own weights, one user, median of 5 runs, 22 Nov 2026.**

| Test | TensorFold 1.3.0 | Main at 1093b795, not in a release yet | Main over 1.3.0 |
|---|---|---|---|
| Max, greedy on new code | 74.5 | 105.5 | 1.42 |
| Median, own sampler on mixed text | 44.6 | 71.2 | 1.60 |
| Greedy prose | 51.8 | 72.1 | 1.39 |
| Copy task | 160.2 | 186.5 | 1.16 |
| Counting toy | 106.4 | 138.2 | 1.30 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **Prose** is greedy, 512-token replies, 1K prompt. **Copy** and **counting** are greedy, 512-token replies, at the faster of 1K and 4K.
- **The figures are the second of two starts of each build**, by my rule of the latest start. The first starts are in the tables below.
- **The arithmetic.** 105.5 / 74.5 = 1.42. 71.2 / 44.6 = 1.60. 72.1 / 51.8 = 1.39. 186.5 / 160.2 = 1.16. 138.2 / 106.4 = 1.30.
- **The counting figures are at different prompt sizes**, 1K on main and 4K on 1.3.0, each build's faster one. At 1K alone it is 138.2 / 104.0 = 1.33.
- **No `mlx-lm` baseline.** `mlx-lm` is not a baseline for this model here, as [finding 4](../04_dsv41_tensorfold_130) notes. TensorFold 1.3.0 is the reference.

## What "not in a release yet" means

ELI5: A project's main branch is where finished changes land. A release is a tagged copy of main that people install. This code is on main and in no tagged copy.

- **The commit.** `1093b795247cbcab0a4df2a87cfcfeafa062521c`, the commit that merged [pull request 3405](https://github.com/ashhart/TensorFold/pull/3405) on 22 Nov 2026 at 01:37 SGT.
- **The latest release was v1.3.2** when I published this, checked on 22 Nov 2026 at 04:46 SGT. It does not hold this change.
- **The binary still prints `tensorfold-native 1.3.2`.** So `--version` does not tell this build from the release. The commit does.
- **I only publish code that is merged to main.** I tested the pull request's older head a few hours earlier and kept those numbers private.
- **This page will be updated** on the first release that holds the change.

## Chart

ELI5: Four tests on both builds. Grey is 1.3.0 and blue is main.

![Paired bars of writing speed in tokens per second for DeepSeek V4.1 Flash, TensorFold 1.3.0 against TensorFold main at 1093b795, which is in no release yet. Greedy code with replies of up to 2,048 tokens at a 4K prompt, 74.5 and 105.5. Greedy code with 512-token replies at 4K, 66.5 and 92.1. Greedy prose at 1K, 51.8 and 72.1. The model's own sampler on mixed text at 4K, 44.6 and 71.2.](chart_main.png)

## Every test on all four starts

ELI5: I started 1.3.0, then main, then main again, then 1.3.0 again. If the Mac had drifted through the night, the two outer starts would differ from each other. They do not. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s, greedy unless the row says sampler.

| Test | Prompt | 1.3.0, start a | Main, start a | Main, start b | 1.3.0, start b |
|---|---|---|---|---|---|
| New code, replies up to 2,048 | 1K | 74.4 (66.7 to 76.6) | 101.3 (100.2 to 103.4) | 102.2 (99.9 to 104.0) | 73.1 (68.9 to 75.4) |
| New code, replies up to 2,048 | 4K | 73.0 (68.5 to 79.2) | 104.8 (97.6 to 109.1) | 105.5 (95.0 to 105.7) | 74.5 (67.6 to 77.4) |
| New code, 512-token replies | 1K | 72.9 (65.1 to 74.9) | 106.3 (82.4 to 107.3) | 103.2 (85.1 to 105.9) | 70.1 (63.8 to 74.6) |
| New code, 512-token replies | 4K | 69.0 (65.4 to 75.5) | 96.2 (90.3 to 100.5) | 92.1 (84.9 to 110.1) | 66.5 (56.6 to 78.7) |
| New code, 512-token replies | 32K | 64.7 (51.1 to 67.3) | 90.8 (79.2 to 99.2) | 86.3 (69.3 to 96.0) | 55.9 (50.2 to 63.7) |
| Prose, 512-token replies | 1K | 51.6 (50.6 to 54.6) | 76.6 (73.8 to 79.3) | 72.1 (69.2 to 78.1) | 51.8 (45.1 to 55.1) |
| Own sampler, mixed text, 512-token replies | 4K | 47.2 (42.6 to 49.2) | 74.3 (67.0 to 76.2) | 71.2 (65.8 to 75.4) | 44.6 (43.7 to 49.1) |
| Copy the prompt, 512-token replies | 1K | 160.2 (149.1 to 161.5) | 188.8 (179.2 to 192.2) | 186.5 (179.1 to 191.7) | 160.2 (151.6 to 161.5) |
| Copy the prompt, 512-token replies | 4K | 145.8 (132.8 to 150.5) | 179.9 (170.5 to 187.9) | 180.1 (173.3 to 187.6) | 146.8 (137.0 to 149.6) |
| Count from 1, 512-token replies | 1K | 102.0 (100.3 to 107.6) | 138.0 (131.0 to 138.4) | 138.2 (130.8 to 138.8) | 104.0 (100.7 to 111.0) |
| Count from 1, 512-token replies | 4K | 110.5 (100.3 to 111.5) | 136.9 (136.0 to 137.3) | 137.1 (136.9 to 137.7) | 106.4 (100.8 to 110.5) |

- **Main was faster on every same-text pair.** 58 of 58 on start a, which has the three 126K requests, and 55 of 55 on start b. By test the middle ratio runs from 1.19 on the 126K prompt to 1.57 with the sampler.
- **The gain differs by test.** The sampler rose 1.54 to 1.57 times, prose 1.43 to 1.48 times and the copy task 1.22 times, over the two starts.
- **The two main starts agree.** Text by text, start b over start a has a middle ratio of 0.98 to 1.00 on every test but prose, which reads 0.93 on 5 pairs.
- **The two 1.3.0 starts agree.** Middle ratios of 0.95 to 1.01 by test.
- **A cold 126K prompt, start a only, 3 requests a build.** The 128-token replies decoded at 63.6 on main and 52.0 on 1.3.0.
- **Every timed reply was answer text**, with 0 reasoning tokens.
- **Long replies.** 8 of 10 ran to 2,048 tokens on main's start a and 4 of 10 on start b. On 1.3.0 it was 5 of 10 and 6 of 10.

## The author's own prompts

ELI5: A speed claim is tied to the prompts it was measured on. The pull request quotes its figures on 16 short prompts that ship in TensorFold's repository. So I ran those too, sent the way the project's own tool sends them.

Decode tok/s, 512 tokens a prompt, the mean over prompts.

| | 1.3.0, start a | Main, start a | Main, start b | 1.3.0, start b |
|---|---|---|---|---|
| 16 prompts, greedy | 74.8 | 102.3 | 102.3 | 75.0 |
| 16 prompts, sampled | 60.8 | 87.4 | 87.4 | 60.7 |
| Five prose prompts, greedy | 56.0 | 78.1 | 78.1 | 56.3 |
| Five prose prompts, sampled | 48.7 | 70.7 | 70.8 | 48.7 |

- **These four rows match the pull request's own table within 1%.** The author's figures, measured on his M5 Ultra, are in [the pull request](https://github.com/ashhart/TensorFold/pull/3405). I do not repeat them here.
- **Its long-coding-prompt row I did not run.** I did not find that prompt in the repository.
- **The five prose prompts are my pick.** `sleep-tips`, `fishing-village`, `dinner-idea`, `heist-story` and `blue-sky`. The file does not mark which five the table means.
- **Greedy** is temperature 0. **Sampled** is temperature 1.0 with seed 1234, as the project's pull request 3288 states. Thinking off for the 13 chat prompts. The other 3 are raw completions.
- **Slowest and fastest prompt on main, greedy.** `fishing-village` at 63.5 and `js-debounce-raw` at 156.3.
- **I ran none of TensorFold's tool code.** My script `author_prompts.py` in this folder reads the prompt file as data and sends the same request fields.

## Did the text change

ELI5: A faster build is only a fair swap if it writes the same words.

| Check | Main against 1.3.0 |
|---|---|
| 250 short greedy answers, 64 tokens each | 250 of 250 equal |
| The 16 prompts, greedy, 512 tokens | 16 of 16 equal, on both starts |
| The 16 prompts, sampled with seed 1234, 512 tokens | 16 of 16 equal, on both starts |

- **The 250 answers are real text.** 49 distinct answers, none empty and none with thinking.
- **Each build also repeats itself.** Start b gave start a's text on 16 of 16 prompts, greedy and sampled, on main and on 1.3.0.
- **Not compared.** The long replies of my own code prompts. They carry a new session line on every start, so their texts differ from start to start on one build too.

## Reading a cold prompt

ELI5: Before it writes, the engine has to read the prompt. This change is about writing, so I expected reading to stay put. It moved a little.

Prompt tokens divided by the time to the first token, nothing cached, the middle with the range.

| Prompt | 1.3.0, start a | Main, start a | Main, start b | 1.3.0, start b |
|---|---|---|---|---|
| 1K, 20 requests | 719 | 740 | 737 | 717 |
| 4K, 20 requests | 1,053 | 1,100 | 1,108 | 1,049 |
| 32K, 5 requests | 1,385 (1,112 to 1,439) | 1,509 (1,475 to 1,528) | 1,508 (1,479 to 1,528) | 1,372 (1,234 to 1,451) |
| 126K, 3 requests | 1,432 | 1,455 | not run | not run |

- **Main read a 32K prompt 9% to 10% faster on these starts.** 1,509 / 1,385 = 1.09 and 1,508 / 1,372 = 1.10. The 1.3.0 runs spread from 1,112 to 1,451, so I read it as a small gain at most.
- **How this is measured.** Prompt tokens over the time to the first token, on a prompt the server has not seen. The server's own log agrees. It gives 3.74 s to the first token for a 4,192-token prompt, which is 1,120 tok/s.
- **The author's post also names a prefill figure, well above anything in this table.** The post does not say how that figure is measured or on which prompts, so I can't set mine beside it.

## The setup

ELI5: Two builds of one engine from source, the same weights, the same serve line.

- **Main.** [TensorFold](https://github.com/ashhart/TensorFold) at commit `1093b795`, fetched by commit and built on 22 Nov 2026 at 01:39 SGT. The build took 82 s. The binary's SHA-256 starts `01360cc35bad218f`.
- **Base.** Tag v1.3.0, commit `d3d0bf11`, the build of findings 4 and 6. It is the newest tag whose DeepSeek server I have built and run. The v1.3.2 tag did not compile on this Mac, as [finding 11](../11_qwen38_tensorfold_132) shows. Main compiles.
- **Build and serve commands**, the same for both.

```bash
zig build dsv41-metal-serve -Dcpu=apple_m1
TF_EXPERIMENTAL=deepseek tensorfold-dsv41 serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 131072 --parallel 1 --no-update-check
```

- **Zig** 0.17.0, the version in the repository's `.zig-version`.
- **Weights.** [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017), the maker's own files.
- **Drafts** at each build's defaults. The banner reads "drafts: DSpark + copies" on both. No draft switch was set.
- **Sampler.** Temperature 1.0 and top-p 1.0, from the server's banner.
- **Thinking** off.
- **What the logs say.** "284.2 GiB kept wired between requests" on all four starts. "dsv41 drafter: 8.0 GiB kept resident in its own set" on the two main starts only.

| Run id | Build | Started, SGT, 22 Nov 2026 |
|---|---|---|
| `292c0952255a` | TensorFold 1.3.0, start a | 03:05 |
| `3b5a26f59c1c` | Main at 1093b795, start a | 03:37 |
| `58aa0c134b88` | Main at 1093b795, start b | 04:03 |
| `2e72378f2ddd` | TensorFold 1.3.0, start b | 04:19 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as findings 4 to 6.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects, prose, or a mix of the two for the sampled test. The text of a request is picked from its size and repeat number, so both builds got the same texts. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K", "4K" and "32K" are targets at 3.5 characters per token.
- **Same-text pairs.** A pair is one text at one prompt size on both builds. The middle ratio is the median of main over 1.3.0 across the pairs.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.
- **The copy and counting questions** are those of [finding 5](../05_dsv41_omlx_080_max_push), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **This is not a release.** Main can change before the next release ships.
- **The base is 1.3.0, two releases back.** The gain here is everything that landed for this model since then, not pull request 3405 alone. By its own table that pull request is a small part of it.
- **Drafted speed depends on the text.** The same build wrote 63.5 on one prompt and 156.3 on another.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 256 raw rows from the bench database. 226 timed requests, 26 warm-ups and 4 refused requests.
- **The 4 refused requests** are two 126K prompts on each build that my harness sized past the 131,072-token window. The server refused them with a clear message. They are in the file with no speed.
- **`runs.csv`.** The 4 runs behind them, with engine, version, commit, start time, settings and sampling.
- **`author_prompts.csv`.** 192 lines, one per request on the author's prompts, with the speed and a hash of the reply text.
- **`author_prompts.py`.** The script that sent them.

From the top of this repository.

```bash
python3 tools/summarize.py findings/17_dsv41_tensorfold_main_1093b795
```

## What I did not verify

- **A release.** None holds this change yet.
- **Which change gave how much.** The base is 1.3.0, and I ran no build in between.
- **The prefill figure of the author's post.** I do not know how it is measured.
- **The long coding prompt of the pull request's table.**
- **Drafted replies against replies with drafts off**, on main.
- **Pauses inside a reply**, the subject of TensorFold issue 3547.
- **Two or more users at once, vision and tools.**
- **Answer quality.** Same text as 1.3.0 is all I checked.
- **Peak memory.** I read the log lines above and nothing else.

## Credit

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart). The change is pull request 3405.
- **Model and weights.** DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
