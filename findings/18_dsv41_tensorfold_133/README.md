# Finding 18. DeepSeek V4.1 Flash on TensorFold 1.3.3, the release

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: [Finding 17](../17_dsv41_tensorfold_main_1093b795) timed a change to TensorFold on the project's main branch, before any release held it. TensorFold 1.3.3 came out on 22 Nov 2026 at 04:58 SGT and holds that change. So I ran the same test again on the release, against 1.3.0 on the same night and the same texts, two server starts each. This is the page to use now.

**TensorFold 1.3.3 wrote 108.0 tok/s on DeepSeek V4.1 Flash at its max and 74.5 with the model's own sampler. TensorFold 1.3.0 wrote 75.2 and 45.7 on the same night, so 1.3.3 is 1.44 and 1.63 times as fast. It was faster on every same-text pair, 58 of 58 and 55 of 55, on two starts. The answers did not change. 250 of 250 short greedy answers match 1.3.0, and so do the replies to the engine author's own 16 prompts, greedy and sampled. The release matches the main-branch build of finding 17 in speed and in text. Mac Studio M5 Ultra 512 GB, the maker's own weights, one user, median of 5 runs, 22 Nov 2026.**

| Test | TensorFold 1.3.0 | TensorFold 1.3.3 | 1.3.3 over 1.3.0 |
|---|---|---|---|
| Max, greedy on new code | 75.2 | 108.0 | 1.44 |
| Median, own sampler on mixed text | 45.7 | 74.5 | 1.63 |
| Greedy prose | 53.9 | 74.5 | 1.38 |
| Copy task | 159.1 | 186.9 | 1.17 |
| Counting toy | 110.0 | 138.1 | 1.26 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **Prose** is greedy, 512-token replies, 1K prompt. **Copy** and **counting** are greedy, 512-token replies, at the faster of 1K and 4K, which was 1K for both builds.
- **The figures are the second of two starts of each build**, by my rule of the latest start. The first starts are in the tables below.
- **The arithmetic.** 108.0 / 75.2 = 1.44. 74.5 / 45.7 = 1.63. 74.5 / 53.9 = 1.38. 186.9 / 159.1 = 1.17. 138.1 / 110.0 = 1.26.
- **No `mlx-lm` baseline.** `mlx-lm` is not a baseline for this model here, as [finding 4](../04_dsv41_tensorfold_130) notes. TensorFold 1.3.0 is the reference.

## Chart

ELI5: Four tests on both releases. Grey is 1.3.0 and blue is 1.3.3.

![Paired bars of writing speed in tokens per second for DeepSeek V4.1 Flash, TensorFold 1.3.0 against TensorFold 1.3.3. Greedy code with replies of up to 2,048 tokens at a 4K prompt, 75.2 and 108.0. Greedy code with 512-token replies at 4K, 69.5 and 94.6. Greedy prose at 1K, 53.9 and 74.5. The model's own sampler on mixed text at 4K, 45.7 and 74.5.](chart_133.png)

## Every test on all four starts

ELI5: I started 1.3.0, then 1.3.3, then 1.3.3 again, then 1.3.0 again. If the Mac had drifted through the run, the two outer starts would differ from each other. They do not. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s, greedy unless the row says sampler.

| Test | Prompt | 1.3.0, start a | 1.3.3, start a | 1.3.3, start b | 1.3.0, start b |
|---|---|---|---|---|---|
| New code, replies up to 2,048 | 1K | 74.3 (67.8 to 76.9) | 106.4 (101.7 to 107.5) | 100.4 (99.5 to 101.3) | 74.4 (67.6 to 82.5) |
| New code, replies up to 2,048 | 4K | 75.7 (68.0 to 80.8) | 105.0 (92.1 to 108.6) | 108.0 (93.6 to 110.4) | 75.2 (67.7 to 79.4) |
| New code, 512-token replies | 1K | 70.6 (59.7 to 75.6) | 99.7 (89.7 to 107.0) | 101.0 (81.9 to 102.9) | 71.0 (59.2 to 78.5) |
| New code, 512-token replies | 4K | 71.5 (67.1 to 75.7) | 91.6 (89.1 to 99.0) | 94.6 (84.3 to 110.5) | 69.5 (64.3 to 80.9) |
| New code, 512-token replies | 32K | 64.1 (61.3 to 68.8) | 89.0 (76.8 to 105.6) | 88.7 (81.1 to 101.8) | 63.2 (58.1 to 71.4) |
| Prose, 512-token replies | 1K | 53.8 (46.3 to 56.3) | 75.0 (73.1 to 79.1) | 74.5 (73.2 to 78.2) | 53.9 (50.7 to 57.7) |
| Own sampler, mixed text, 512-token replies | 4K | 46.3 (41.2 to 52.8) | 72.8 (69.6 to 74.8) | 74.5 (71.2 to 75.6) | 45.7 (44.1 to 47.2) |
| Copy the prompt, 512-token replies | 1K | 160.8 (146.5 to 162.7) | 188.6 (181.0 to 190.2) | 186.9 (180.5 to 191.0) | 159.1 (138.5 to 161.4) |
| Copy the prompt, 512-token replies | 4K | 145.9 (130.1 to 149.1) | 179.9 (173.3 to 188.5) | 179.9 (173.0 to 188.3) | 145.9 (124.1 to 149.2) |
| Count from 1, 512-token replies | 1K | 106.2 (101.7 to 109.1) | 138.4 (130.2 to 138.8) | 138.1 (135.3 to 139.3) | 110.0 (100.2 to 110.7) |
| Count from 1, 512-token replies | 4K | 104.1 (102.9 to 112.1) | 136.9 (136.8 to 137.9) | 137.7 (136.7 to 138.0) | 109.5 (100.4 to 112.3) |

- **1.3.3 was faster on every same-text pair.** 58 of 58 on start a, which has the three 126K requests, and 55 of 55 on start b. By test the middle ratio runs from 1.22 on the copy task to 1.59 with the sampler.
- **The gain differs by test.** The sampler rose 1.51 to 1.59 times, prose 1.38 to 1.39 times and the copy task 1.22 times, over the two starts.
- **The two 1.3.3 starts agree.** Text by text, start b over start a has a middle ratio of 0.99 to 1.02 by test.
- **The two 1.3.0 starts agree.** Middle ratios of 0.98 to 1.00 by test.
- **A cold 126K prompt, start a only, 3 requests a build.** The 128-token replies decoded at 68.7 on 1.3.3 and 49.1 on 1.3.0.
- **Every timed reply was answer text**, with 0 reasoning tokens.
- **Long replies.** 5 of 10 ran to 2,048 tokens on 1.3.3's start a and 4 of 10 on start b. On 1.3.0 it was 6 of 10 on each start.

## The release against the main-branch build

ELI5: Finding 17 ran this change two hours earlier, on main at commit 1093b795. The release should behave the same. It does.

| Check | 1.3.3 against main at 1093b795 |
|---|---|
| Same-text pairs, start a against start a | middle ratio 0.97 to 1.04 by test |
| Same-text pairs, start b against start b | middle ratio 0.98 to 1.03 by test |
| 250 short greedy answers | 250 of 250 equal |
| The 16 prompts, greedy and sampled | 16 of 16 equal each, on both starts |

- **Max.** 108.0 on 1.3.3 against 105.5 on main. **Median.** 74.5 against 71.2. Both gaps are inside what two starts of one build show.
- **The summary page now carries the 1.3.3 lines** in place of the lines labelled "main at 1093b795, not in a release yet". Finding 17 stays as it was written, with a note at its top.
- **The main-branch rows are in finding 17's folder**, not here.

## The author's own prompts

ELI5: The change's own pull request quotes its figures on 16 short prompts that ship in TensorFold's repository. I ran those too, sent the way the project's own tool sends them.

Decode tok/s, 512 tokens a prompt, the mean over prompts.

| | 1.3.0, start a | 1.3.3, start a | 1.3.3, start b | 1.3.0, start b |
|---|---|---|---|---|
| 16 prompts, greedy | 74.9 | 102.4 | 102.4 | 74.7 |
| 16 prompts, sampled | 60.8 | 87.5 | 87.6 | 60.7 |
| Five prose prompts, greedy | 56.5 | 78.2 | 78.2 | 56.3 |
| Five prose prompts, sampled | 48.8 | 70.8 | 70.9 | 48.7 |

- **These four rows match the pull request's own table within 1%.** The author's figures, measured on his M5 Ultra, are in [the pull request](https://github.com/ashhart/TensorFold/pull/3405). I do not repeat them here.
- **The five prose prompts are my pick.** `sleep-tips`, `fishing-village`, `dinner-idea`, `heist-story` and `blue-sky`. The file does not mark which five the table means.
- **Greedy** is temperature 0. **Sampled** is temperature 1.0 with seed 1234. Thinking off for the 13 chat prompts. The other 3 are raw completions.
- **Slowest and fastest prompt on 1.3.3, greedy.** `fishing-village` at 63.7 and `js-debounce-raw` at 156.3.
- **I ran none of TensorFold's tool code.** My script `author_prompts.py` in this folder reads the prompt file as data and sends the same request fields.

## Did the text change

ELI5: A faster release is only a fair swap if it writes the same words.

| Check | 1.3.3 against 1.3.0 |
|---|---|
| 250 short greedy answers, 64 tokens each | 250 of 250 equal |
| The 16 prompts, greedy, 512 tokens | 16 of 16 equal, on both starts |
| The 16 prompts, sampled with seed 1234, 512 tokens | 16 of 16 equal, on both starts |

- **The 250 answers are real text.** 49 distinct answers, none empty and none with thinking.
- **The 16 replies are 16 distinct texts**, none empty, in both modes.
- **Each release also repeats itself.** Start b gave start a's text on 16 of 16 prompts, greedy and sampled, on 1.3.3 and on 1.3.0.
- **Not compared.** The long replies of my own code prompts. They carry a new session line on every start, so their texts differ from start to start on one build too.

## Reading a cold prompt

ELI5: Before it writes, the engine has to read the prompt. I measure that as prompt tokens over the time to the first token, on a prompt the server has not seen.

The middle, with the range for the 32K row.

| Prompt | 1.3.0, start a | 1.3.3, start a | 1.3.3, start b | 1.3.0, start b |
|---|---|---|---|---|
| 1K, 20 requests | 733 | 746 | 737 | 724 |
| 4K, 20 requests | 1,038 | 1,111 | 1,104 | 1,055 |
| 32K, 5 requests | 1,368 (1,348 to 1,435) | 1,509 (1,469 to 1,528) | 1,509 (1,468 to 1,529) | 1,434 (1,413 to 1,467) |
| 126K, 3 requests | 1,441 | 1,458 | not run | not run |

- **1.3.3 read a 32K prompt 5% to 10% faster on these starts.** 1,509 / 1,368 = 1.10 and 1,509 / 1,434 = 1.05.
- **The author's post about this change also names a prefill figure, well above anything in this table.** The post does not say how that figure is measured or on which prompts, so I can't set mine beside it.

## The setup

ELI5: Two releases of one engine, each built from its tag, the same weights and the same serve line.

- **Release.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.3, released 22 Nov 2026 04:58 SGT, tag commit `1e4a32cb`, built from the tag on 22 Nov 2026 at 05:11 SGT in 76 s. `--version` prints `tensorfold-native 1.3.3`. The binary's SHA-256 starts `2740ab106326c3ea`.
- **It was still the newest release** when I published this, checked on 22 Nov 2026 at 06:58 SGT.
- **Base.** Tag v1.3.0, commit `d3d0bf11`, the build of findings 4 and 6. I have published no run of 1.3.1 or 1.3.2 on this model. The 1.3.2 tag did not compile on this Mac, as [finding 11](../11_qwen38_tensorfold_132) shows. 1.3.3 compiles.
- **Why a source build.** The Homebrew 1.3.3 program does not list this model among the families it serves, by `tensorfold-native capabilities --json`. The DeepSeek server for Macs is its own build target in the source. The project marks it experimental, and it is switched on with `TF_EXPERIMENTAL=deepseek`.
- **Build and serve commands**, the same for both.

```bash
git clone --depth 1 --branch v1.3.3 https://github.com/ashhart/TensorFold
zig build dsv41-metal-serve -Dcpu=apple_m1
TF_EXPERIMENTAL=deepseek tensorfold-dsv41 serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 131072 --parallel 1 --no-update-check
```

- **Zig** 0.17.0, the version in the repository's `.zig-version`.
- **Weights.** [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017), the maker's own files.
- **Drafts** at each build's defaults. The banner reads "drafts: DSpark + copies" on both. No draft switch was set.
- **Sampler.** Temperature 1.0 and top-p 1.0, from the server's banner.
- **Thinking** off.
- **What the logs say.** "284.2 GiB kept wired between requests" on all four starts. "dsv41 drafter: 8.0 GiB kept resident in its own set" on the two 1.3.3 starts only.

| Run id | Build | Started, SGT, 22 Nov 2026 |
|---|---|---|
| `b2224ceaefc6` | TensorFold 1.3.0, start a | 05:19 |
| `6fe81d2e8d5c` | TensorFold 1.3.3, start a | 05:51 |
| `d690d6b1059b` | TensorFold 1.3.3, start b | 06:16 |
| `5b618f8c8234` | TensorFold 1.3.0, start b | 06:32 |

## How I measured

ELI5: Same Mac, same harness, same texts and same blocks as finding 17.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects, prose, or a mix of the two for the sampled test. The text of a request is picked from its size and repeat number, so both builds got the same texts. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K", "4K" and "32K" are targets at 3.5 characters per token.
- **Same-text pairs.** A pair is one text at one prompt size on both builds. The middle ratio is the median of the newer build over the older across the pairs.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.
- **The copy and counting questions** are those of [finding 5](../05_dsv41_omlx_080_max_push), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **The base is 1.3.0, three releases back.** The gain here is everything that landed for this model since then, not one change alone.
- **Drafted speed depends on the text.** The same build wrote 63.7 on one prompt and 156.3 on another.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.
- **This server is experimental by the project's own word**, and it is a source build, not the Homebrew program.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 256 raw rows from the bench database. 226 timed requests, 26 warm-ups and 4 refused requests.
- **The 4 refused requests** are two 126K prompts on each build that my harness sized past the 131,072-token window. They are in the file with no speed.
- **`runs.csv`.** The 4 runs behind them, with engine, version, commit, start time, settings and sampling.
- **`author_prompts.csv`.** 192 lines, one per request on the author's prompts, with the speed and a hash of the reply text.
- **`author_prompts.py`.** The script that sent them.

From the top of this repository.

```bash
python3 tools/summarize.py findings/18_dsv41_tensorfold_133
```

## What I did not verify

- **Which change gave how much.** The base is 1.3.0, and I ran no release in between.
- **The prefill figure of the author's post.** I do not know how it is measured.
- **Drafted replies against replies with drafts off**, on 1.3.3.
- **Pauses inside a reply**, the subject of TensorFold issue 3547.
- **Two or more users at once, vision and tools.**
- **Answer quality.** Same text as 1.3.0 is all I checked.
- **Peak memory.** I read the log lines above and nothing else.

## Credit

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Model and weights.** DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
