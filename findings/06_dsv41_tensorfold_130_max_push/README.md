# Finding 6. DeepSeek V4.1 Flash on TensorFold 1.3.0, pushing the max

ELI5: Finding 4 compared TensorFold 1.3.0 with the version before it. Here I tried six draft settings on 1.3.0 to see how high the top speed goes, and asked three different things of the default setup. The answer is that the defaults are already the top, and that what you ask moves the number far more than any switch.

**TensorFold 1.3.0 wrote 76.4 tok/s on DeepSeek V4.1 Flash 1017 while writing new code, greedy at temperature 0, drafts at defaults, replies of up to 2,048 tokens at a 4K prompt, and 74.1 at a 1K prompt. With 512-token replies at a 1K prompt the same server wrote 159.1 tok/s copying code out of the prompt and 106.9 counting up from 1. None of six draft settings separated from the defaults. Their cell medians ran from 0.95 to 1.06 times the defaults, inside the 7% I measured between two starts of one setting. One server start per setting. Mac Studio M5 Ultra 512 GB, the maker's own files, one user, median of 5 runs, 20 Nov 2026.**

## Chart

ELI5: One setup and three questions. Grey is the model writing something new. The two blues are text the drafts can guess almost every time.

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on TensorFold 1.3.0 with drafts at defaults, greedy at temperature 0. At a 1K prompt, 74.1 writing new code, 159.1 copying the prompt and 106.9 counting from 1. At a 4K prompt, 76.4, 146.3 and 105.3.](chart_tasks.png)

## Max speed, writing new code

ELI5: The model reads a block of code and writes a new module with tests. Nothing in the reply can be copied, so this is the top speed for real work. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Greedy at temperature 0, code, drafts at defaults, run `605b3e0a7834`, tok/s.

| Reply length | 1K prompt | 4K prompt |
|---|---|---|
| Up to 2,048 tokens | 74.1 (69.2 to 75.0) | 76.4 (67.5 to 80.5) |
| 512 tokens | 71.0 (65.4 to 75.0) | 67.3 (63.8 to 74.0) |

- **Longer replies wrote faster.** 76.4 against 67.3 at 4K. That is 76.4 / 67.3 = 1.14 times. At 1K, 74.1 / 71.0 = 1.04 times.
- **The 512-token figure matches finding 4.** Two other starts of 1.3.0 at defaults wrote 70.5 and 71.7 at 1K, against 71.0 here.
- **6 of the 10 long replies ran to 2,048 tokens.** The model ended the other 4 itself, the shortest at 1,654 tokens. Speed is tokens written over the time from the first token to the last.
- **One server start.** The long-reply figures have not been repeated.

## Ceiling on easy text

ELI5: Two tests where the drafts guess almost every token. In one the model repeats the prompt's code word for word. In the other it counts 1, 2, 3. The speed is far above real work, so I keep these apart from the max.

Greedy at temperature 0, 512-token replies, drafts at defaults, run `605b3e0a7834`, tok/s. Every reply ran to 512 tokens.

| Test | 1K prompt | 4K prompt |
|---|---|---|
| Copy the prompt | 159.1 (149.3 to 163.1) | 146.3 (125.7 to 149.7) |
| Count from 1 | 106.9 (103.1 to 114.0) | 105.3 (102.2 to 111.2) |

- **Copying is where this engine is furthest ahead of its own real-task speed.** 159.1 against 71.0 on new code, both with 512-token replies at 1K. That is 159.1 / 71.0 = 2.24 times.
- **A likely reason.** The server starts with "drafts: DSpark + copies". My reading is that the copies part drafts from text already in the prompt, which would make a copy task its best case. I did not confirm that in the source.
- **I checked what the model wrote.** One extra copy request at 1K returned 63 lines. 62 are lines of the prompt's code word for word and the other is the session id from the prompt's first line. One extra counting request returned the numbers 1 to 256 in order. Both ran on a separate start of 1.3.0 at defaults and are not in `rows.csv`.

## Six settings, none clearly faster

ELI5: TensorFold reads a few draft switches from the environment. I started the server once with each of six settings of five switches and ran the same three tests. Each cell is the middle of 5 runs.

Greedy at temperature 0, 512-token replies, tok/s at a 1K and a 4K prompt.

| Setting | Run | New code | Copy | Counting |
|---|---|---|---|---|
| Defaults | `605b3e0a7834` | 71.0 and 67.3 | 159.1 and 146.3 | 106.9 and 105.3 |
| `TF_DSV41_TREE=2` | `f8a9dd23d94f` | 69.7 and 64.2 | 161.2 and 146.5 | 112.4 and 108.6 |
| `TF_DSV41_TREE=4` | `49f911e26a15` | 69.9 and 67.6 | 158.9 and 138.8 | 110.6 and 107.2 |
| `TF_DSV41_SPEC_DRAFT=1` | `1509855f5e17` | 73.8 and 68.3 | 160.7 and 145.8 | 102.2 and 105.0 |
| `TF_DSV41_CODE_ACCEPT=1` | `48ba8a61ba7d` | 74.3 and 67.0 | 160.6 and 145.8 | 106.5 and 112.1 |
| `TF_DSV41_LOOKUP_PLAN=1` | `a5b7d593f608` | 75.4 and 67.6 | 156.8 and 139.5 | 106.5 and 109.2 |
| `TF_DSV41_DRAFT_DEPTH=8` | `da960db5bb48` | 70.3 and 70.1 | 160.7 and 145.5 | 108.0 and 109.9 |

- **No setting separates from the defaults.** The cell medians run from 0.95 to 1.06 times the defaults. The largest are 112.1 / 105.3 = 1.06 for `TF_DSV41_CODE_ACCEPT=1` on counting at 4K and 75.4 / 71.0 = 1.06 for `TF_DSV41_LOOKUP_PLAN=1` on new code at 1K. Text by text, the middle ratio of every setting on every test lies between 0.96 and 1.03. Finding 3 measured 7% between two starts of one setting on this Mac.
- **The largest move up is `TF_DSV41_SPEC_DRAFT=1` on new code**, faster on 9 of 10 texts with a middle ratio of 1.03. One start, so I do not count it as a gain.
- **Only `TF_DSV41_TREE` is documented.** It is in the changelog, which says trees stay off by default because they were flat on an M5 Ultra. The other four names are read by the 1.3.0 source and are in no guide I found. I do not know what the project intends them for, so treat those rows as a screen and nothing more.
- **Two settings are confirmed by the log.** `TF_DSV41_DRAFT_DEPTH=8` shows as "depth: cost, cap 8" against "cap 5", and `TF_DSV41_LOOKUP_PLAN=1` adds the line "lookup: Python's priced plan". For the two tree settings, `TF_DSV41_SPEC_DRAFT` and `TF_DSV41_CODE_ACCEPT`, the variable was in the server's process environment, but no log line shows the engine acted on it. So for those four rows I can't confirm the setting applied.
- **I did not run the answer test on these starts**, since no setting earned a place.

## Pauses

ELI5: Finding 4 found single pauses of about half a second in replies on 1.3.0. They show here too.

- **83 of the 220 timed replies held a gap over 0.2 s.** The longest was 0.60 s. On the defaults start it was 17 of 40.
- **`gaps.csv` lists every reply** with its longest gap and each gap over 0.2 s.
- **Finding 4 has the comparison with 1.2.10**, where no reply had such a gap.

## Reference points

ELI5: Apple's own server does not read these files, so there is no baseline bar. The nearest rows are the same model on another engine and in other files.

- **`mlx-lm` is not a baseline for this model here**, as finding 4 notes.
- **Finding 5, different weights and engine.** oMLX 0.8.0 on the oQ4e-mtp build wrote 84.1 tok/s on new code with replies of up to 2,048 tokens at 1K, with draft depth fixed at 5, and 77.2 at its default depth. It wrote 118.3 on the copy task and 114.0 counting, at 4K.
- **Finding 4, same engine and weights.** 44.5 and 46.1 tok/s on two starts with the model's own sampler on mixed text at 4K. That is the figure to plan around.

## The setup

ELI5: The engine and weights of finding 4. One environment variable changed between server starts.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) `tensorfold-dsv41` 1.3.0, commit d3d0bf11, built from the release tag with Zig 0.17.0 and `zig build dsv41-metal-serve -Dcpu=apple_m1`. The project calls this server experimental, switched on with `TF_EXPERIMENTAL=deepseek`.
- **Weights.** [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) @ 08c8657f, the maker's FP8 and MXFP4 files.
- **Serve command**, the same on every start.

```bash
tensorfold-dsv41 serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 131072 --parallel 1 --no-update-check
```

- **The one switch** was set in the environment of that start and nowhere else.
- **Thinking** off.

| Run id | Setting | Started, SGT, 20 Nov 2026 |
|---|---|---|
| `605b3e0a7834` | Defaults | 18:43 |
| `f8a9dd23d94f` | `TF_DSV41_TREE=2` | 18:52 |
| `49f911e26a15` | `TF_DSV41_TREE=4` | 18:57 |
| `1509855f5e17` | `TF_DSV41_SPEC_DRAFT=1` | 19:01 |
| `48ba8a61ba7d` | `TF_DSV41_CODE_ACCEPT=1` | 19:05 |
| `a5b7d593f608` | `TF_DSV41_LOOKUP_PLAN=1` | 19:09 |
| `da960db5bb48` | `TF_DSV41_DRAFT_DEPTH=8` | 19:13 |

## How I measured

ELI5: Same Mac, same harness and same three questions as finding 5.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects. The text of a request is picked from its size and repeat number, so every start got the same code texts. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. The prompts came to about 855 and 4,100 tokens.
- **Three questions**, each placed after the code text.
  - **New code.** "Write a new Python module, with unit tests, that reimplements the most important function above in a cleaner way. Write it in full." In `rows.csv` the content is `code`.
  - **Copy.** "Repeat the text above exactly as written, starting from its first line after the Session line. Change nothing and add no commentary." The content is `code_echo`.
  - **Counting.** "Ignore the text above. Count from 1 to 400, one number per line, nothing else." The content is `code_count`.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first reply token to the last.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 242 raw rows from the bench database. The 220 timed requests and the 22 warm-ups.
- **`runs.csv`.** The 7 runs behind them, with engine, version, start time, settings and sampling. The switch of each start is in its `settings` text.
- **`gaps.csv`.** One line for each of the 220 timed replies, made from the arrival time of every streamed piece.

From the top of this repository.

```bash
python3 tools/summarize.py findings/06_dsv41_tensorfold_130_max_push
```

## What I did not verify

- **A second start of any setting.** Every row here is one server start.
- **What the four undocumented switches are meant to do**, and whether the tree, spec draft and code accept settings took effect.
- **That the switches leave answers unchanged.** The answer test did not run on these starts.
- **A measured draft cost table** (`TF_DSV41_CALIB_FILE`). I ran the built-in table.
- **Prompts longer than 4K** on these tests. Finding 4 has 512-token replies up to 32K and 128-token replies at about 115K tokens.
- **Peak memory.** These runs did not log it.
- **Thinking on.**

## Credit

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Model.** DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.
