# Finding 5. DeepSeek V4.1 Flash on oMLX 0.8.0, pushing the max

ELI5: Finding 3 measured this model on oMLX at its default settings. Here I tried a few switches to see how high the top speed goes. I also asked three different things of the same setup, because the top speed depends more on what you ask than on any switch.

**oMLX 0.8.0 wrote 84.1 tok/s on DeepSeek V4.1 Flash 1017 oQ4e-mtp while writing new code, greedy at temperature 0, with draft depth fixed at 5 and replies of up to 2,048 tokens at a 1K prompt. The other fixed-depth start gave 81.3. The default depth gave 77.2 and 76.2 on the same test. With 512-token replies at a 4K prompt, fixed depth 5 wrote 118.3 tok/s copying code out of the prompt and 114.0 counting up from 1. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 20 Nov 2026.**

## Chart

ELI5: One setup and three questions. Grey is the model writing something new. The two blues are text the drafts can guess almost every time.

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on oMLX 0.8.0 with draft depth fixed at 5, greedy at temperature 0. At a 1K prompt, 84.1 writing new code, 114.7 copying the prompt and 113.0 counting from 1. At a 4K prompt, 82.7, 118.3 and 114.0.](chart_tasks.png)

## Max speed, writing new code

ELI5: The model reads a block of code and writes a new module with tests. Nothing in the reply can be copied, so this is the top speed for real work. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Greedy at temperature 0, code, replies of up to 2,048 tokens, tok/s.

| Draft setting | Run | Started, SGT | 1K prompt | 4K prompt |
|---|---|---|---|---|
| Default depth | `526b05fc2a44` | 16:34 | 76.2 (74.0 to 80.2) | 76.8 (74.6 to 79.1) |
| Fixed depth 5 | `b4b4f8bb5ecb` | 17:50 | 81.3 (78.0 to 88.8) | 83.9 (79.8 to 89.1) |
| Default depth | `7ece67645192` | 17:56 | 77.2 (72.5 to 78.7) | 72.9 (70.3 to 80.7) |
| Fixed depth 5 | `7513746c2ce0` | 18:02 | 84.1 (78.5 to 84.8) | 82.7 (77.7 to 85.7) |

- **Fixed depth 5 won on both of its starts.** Its four cells run from 81.3 to 84.1. The default's four run from 72.9 to 77.2.
- **Text by text, fixed depth 5 was faster on 19 of 20.** Each fixed-depth start got the same code text as the default start at 17:56. The middle ratio was 1.10 for the first start and 1.09 for the second. One pair was level.
- **The summary line uses the last start of the setting**, run `7513746c2ce0`, at 84.1. The other start gave 81.3.
- **Half the replies ended before the cap.** 20 of the 40 replies ran to 2,048 tokens. The model ended the other 20 itself, the shortest at 1,064 tokens. Speed is tokens written over the time from the first token to the last.

Greedy at temperature 0, code, 512-token replies, tok/s.

| Draft setting | Run | 1K prompt | 4K prompt |
|---|---|---|---|
| Default depth | `526b05fc2a44` | 72.5 (61.6 to 75.4) | 70.7 (62.0 to 77.1) |
| Fixed depth 5 | `b1703d1d52b6` | 74.7 (69.4 to 81.5) | 74.9 (64.6 to 85.6) |
| Default depth, burst decode aggressive | `eaf2a9876d78` | 72.4 (63.9 to 75.8) | 72.0 (65.9 to 76.2) |
| Fixed depth 5, burst decode aggressive | `e1932d58fe7a` | 75.5 (58.3 to 79.6) | 77.6 (63.0 to 86.7) |
| Fixed depth 5, burst decode aggressive, activation fp16 | `d17997b4541d` | 44.2 (41.1 to 48.1) | 41.2 (37.1 to 48.1) |

- **At 512 tokens the gain from fixed depth 5 is small.** It was faster on 16 of 20 texts, with a middle ratio of 1.05. Finding 3 measured 7% between two starts of one setting, so this is inside the noise.
- **Longer replies wrote faster.** At the default depth, 76.2 at 2,048 tokens against 72.5 at 512, both at 1K in run `526b05fc2a44`. That is 76.2 / 72.5 = 1.05 times.
- **Burst decode aggressive showed no change.** 72.4 against 72.5 at the default depth. The server log has no line that names the burst mode, so I can't confirm the setting applied.
- **Activation fp16 wrote slower here.** With `activation_fp16_enabled` true the run wrote 44.2 and 41.2 tok/s. The first token took 1.37 s at 1K against 0.67 s. 15 of its 250 greedy test answers matched the default's. The switch is off by default, at line 451 of `omlx/model_settings.py` in 0.8.0. I did not look into the cause.

## Ceiling on easy text

ELI5: Two tests where the drafts guess almost every token. In one the model repeats the prompt's code word for word. In the other it counts 1, 2, 3. The speed is far above real work, so I keep these apart from the max.

Greedy at temperature 0, 512-token replies, tok/s. Every reply ran to 512 tokens.

| Draft setting | Run | Copy, 1K | Copy, 4K | Counting, 1K | Counting, 4K |
|---|---|---|---|---|---|
| Default depth | `526b05fc2a44` | 98.2 (97.6 to 99.2) | 98.3 (93.3 to 99.9) | 90.4 (89.8 to 90.5) | 90.6 (90.4 to 90.8) |
| Fixed depth 5 | `b1703d1d52b6` | 114.7 (113.6 to 118.1) | 118.3 (110.7 to 121.0) | 113.0 (111.9 to 114.0) | 114.0 (113.7 to 114.3) |
| Default depth, burst decode aggressive | `eaf2a9876d78` | 98.5 (97.8 to 99.5) | 98.4 (94.3 to 100.3) | 90.4 (89.8 to 90.6) | 90.8 (90.6 to 91.1) |
| Fixed depth 5, burst decode aggressive | `e1932d58fe7a` | 116.0 (114.9 to 118.3) | 117.3 (110.8 to 121.0) | 113.1 (111.9 to 114.1) | 114.0 (113.7 to 114.4) |
| Fixed depth 5, burst decode aggressive, activation fp16 | `d17997b4541d` | 74.5 (73.6 to 76.0) | 74.6 (68.9 to 77.1) | 64.9 (64.8 to 65.1) | 64.3 (64.0 to 64.4) |

- **Fixed depth 5 is the lever here.** The copy task rose from 98.3 to 118.3 at 4K. That is 118.3 / 98.3 = 1.20 times. Counting rose from 90.6 to 114.0, and 114.0 / 90.6 = 1.26 times.
- **Both fixed-depth starts agree.** Copy at 114.7 to 118.3, counting at 113.0 to 114.0.
- **Why it moves.** oMLX's log gives the tokens kept per draft cycle. On these two tests the default depth kept about 4.0 and fixed depth 5 kept about 6.0. On new code with 2,048-token replies the default kept 2.9 to 3.5 and fixed depth 5 kept 4.2 to 4.8. Those log lines are not in `rows.csv`.
- **The same setting, three speeds.** At a 4K prompt with fixed depth 5 and 512-token replies, run `b1703d1d52b6` wrote 74.9 on new code, 118.3 copying and 114.0 counting. 118.3 / 74.9 = 1.58 times. Against the best new-code figure at 4K, 82.7 with replies of up to 2,048 tokens, it is 118.3 / 82.7 = 1.43 times.
- **I checked what the model wrote.** One extra copy request returned 63 lines, and all 63 are in the prompt word for word. One extra counting request returned the numbers 1 to 256 in order. Both ran on the default-depth start at 17:56 and are not in `rows.csv`.

## Same answers

ELI5: A speed switch should not change what the model says. I asked each setup the same 250 short questions with no randomness and compared the answers.

| Setup | Run | Answers that match the default's |
|---|---|---|
| Fixed depth 5 | `b1703d1d52b6` | 250 of 250 |
| Default depth, burst decode aggressive | `eaf2a9876d78` | 250 of 250 |
| Fixed depth 5, burst decode aggressive | `e1932d58fe7a` | 250 of 250 |
| Fixed depth 5, burst decode aggressive, activation fp16 | `d17997b4541d` | 15 of 250 |

- **The default here also matches finding 3's default**, run `800dd0f8839c`, on 250 of 250.
- **The two long-reply starts at fixed depth 5 did not run this test.** Runs `b4b4f8bb5ecb` and `7513746c2ce0` have the setting of run `b1703d1d52b6`, which matched on 250 of 250.
- **The test uses 64-token replies.** It does not show that a 2,048-token reply is the same text at both depths.
- **The speed prompts are not the same text run to run.** Each one opens with a new session line, so two runs of one code text can give replies of different lengths.

## Reference points

ELI5: Apple's own server can't load this file, so there is no baseline bar. The nearest rows are from the two findings before this one.

- **`mlx-lm` 0.32.2 does not load this build**, as finding 3 notes. So no multiple of `mlx-lm` can be given.
- **Finding 3, same engine and weights at defaults.** 71.2 tok/s greedy on code with 512-token replies at 1K, and 56.5 tok/s with the model's own sampler on mixed text at 4K.
- **Finding 4, different weights and engine.** TensorFold 1.3.0 on the maker's files wrote 70.5 tok/s greedy on code with 512-token replies at 1K.

## The setup

ELI5: The engine and weights of finding 3. One or two settings changed between server starts.

- **Engine.** [oMLX](https://github.com/jundot/omlx) 0.8.0, the release of 18 Nov 2026, installed from the tagged source with its custom kernels built (`OMLX_WITH_CUSTOM_KERNEL=1`).
- **Weights.** [mlx-community/DeepSeek-V4.1-Flash-1017-oQ4e-mtp](https://huggingface.co/mlx-community/DeepSeek-V4.1-Flash-1017-oQ4e-mtp) @ 8080db68.
- **Serve command.**

```bash
omlx serve --model-dir <models> --host 127.0.0.1 --port 8180 --max-concurrent-requests 1 --headless --no-hf-cache --base-path <home>
```

- **Model settings on every start**, in oMLX's own `model_settings.json`. `mtp_enabled` true, `deepseek_v41_ced_prefill_enabled` true, `a8_prefill_enabled` false, `deepseek_v41_engram_ssd_offload` false.
- **Fixed depth 5.** `mtp_fixed_depth` set to 5 in the model's entry of `model_settings.json`. Unset is the default, which drafts 1 to 3 deep on this build. oMLX caps the depth at the build's `dspark_block_size`, which is 5.
- **Burst decode.** `server.burst_decode_mode` in `settings.json`. The default is `balanced`, at line 170 of `omlx/settings.py` in 0.8.0. It was `aggressive` on the three starts that say so.
- **Activation fp16.** `activation_fp16_enabled` true in the model's entry, on one start. The default is false.
- **Every change** was made with the server stopped, followed by a fresh start.
- **Thinking** off.

| Run id | Setting | Started, SGT, 20 Nov 2026 |
|---|---|---|
| `526b05fc2a44` | Default depth | 16:34 |
| `b1703d1d52b6` | Fixed depth 5 | 16:51 |
| `eaf2a9876d78` | Default depth, burst decode aggressive | 17:02 |
| `e1932d58fe7a` | Fixed depth 5, burst decode aggressive | 17:14 |
| `d17997b4541d` | Fixed depth 5, burst decode aggressive, activation fp16 | 17:26 |
| `b4b4f8bb5ecb` | Fixed depth 5 | 17:50 |
| `7ece67645192` | Default depth | 17:56 |
| `7513746c2ce0` | Fixed depth 5 | 18:02 |

## How I measured

ELI5: Same Mac, same harness and same text rules as findings 3 and 4. Two new questions were added for the easy-text tests.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects. The text of a request is picked from its size and repeat number, so every start got the same code texts. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. The prompts came to about 856 and 4,100 tokens.
- **Three questions**, each placed after the code text.
  - **New code.** "Write a new Python module, with unit tests, that reimplements the most important function above in a cleaner way. Write it in full." In `rows.csv` the content is `code`.
  - **Copy.** "Repeat the text above exactly as written, starting from its first line after the Session line. Change nothing and add no commentary." The content is `code_echo`.
  - **Counting.** "Ignore the text above. Count from 1 to 400, one number per line, nothing else." The content is `code_count`.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first reply token to the last.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Ask what the test asked.** A benchmark that feeds the model repeated or copyable text is measuring the ceiling, not the max. On this setup the two differ by 1.43 to 1.58 times.
- **Max is not what a chat feels like.** The model's own sampler on mixed text gave 56.5 tok/s at the default depth in finding 3. I have not run that test at fixed depth 5.
- **One build.** oQ4e-mtp is a 4-bit quant with the model's draft head kept. I did not score its answers against the maker's files.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 209 raw rows from the bench database. The 190 timed requests and the 19 warm-ups.
- **`runs.csv`.** The 8 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/05_dsv41_omlx_080_max_push
```

It prints one line per run, text kind, prompt size, reply length and sampler, with the median and range.

## What I did not verify

- **Whether burst decode aggressive applied.** The log does not name the mode.
- **Why activation fp16 wrote slower and changed answers.**
- **The model's own sampler at fixed depth 5.** So the median speed for this setting is not known.
- **Prompts longer than 4K** at fixed depth 5 with long replies. Finding 3 ran fixed depth 5 at 32K with 512-token replies and measured 69.1.
- **That a 2,048-token greedy reply is the same text at both depths.** The answer test uses 64-token replies.
- **Answer quality** of the oQ4e-mtp build.
- **Peak memory.** These runs did not log it.
- **Thinking on.**
- **oMLX's built-in benchmark on this Mac.** Not run.

## Credit

- **Engine.** [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim).
- **Weights.** The oQ4e-mtp build by [mlx-community](https://huggingface.co/mlx-community).
- **Model.** DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.
