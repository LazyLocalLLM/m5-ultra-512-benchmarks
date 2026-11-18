# Finding 1. TensorFold with a draft model on Qwen3.8-27B 4-bit

ELI5: A small draft model guesses the next few words and the big model checks them. When the guesses are right the big model writes much faster. I measured how much faster on one Mac.

**Qwen3.8-27B 4-bit writes 145.7 tok/s on a Mac Studio M5 Ultra 512 GB with TensorFold 1.2.7 and the DFlash2 draft model. Apple's `mlx-lm` 0.32.2 writes 44.5 tok/s on the same weights. That is 3.3 times. One user, 1K prompt, median of 5 runs, 13 Nov 2026.**

![Bar chart of writing speed for Qwen3.8-27B 4-bit on a Mac Studio M5 Ultra 512 GB, one user. At a 1K prompt, mlx-lm 0.32.2 writes 44.5 tokens per second, TensorFold 1.2.7 with no draft model writes 48.7, and TensorFold 1.2.7 with the DFlash2 draft model writes 145.7. At a 32K prompt the three write 39.5, 43.4 and 118.7.](card.png)

- **The multiple.** 3.27 times. TensorFold with the draft over `mlx-lm`, both at a 1K prompt. 145.7 / 44.5 = 3.27.
- **Second set.** I ran everything again about three hours later. 143.9 / 43.5 = 3.31 times.

## Setup

ELI5: Same Mac, same weights, same prompts for every engine. Only the engine changes.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Weights.** `TensorFold/Qwen3.8-27B-MLX-4bit` from Hugging Face. All three setups read this one build.
- **Draft model.** `z-lab/Qwen3.8-27B-DFlash2`. This is the setup TensorFold's own recipe for Qwen3.8-27B names.
- **Engines.** TensorFold 1.2.7 and `mlx-lm` 0.32.2.
- **Date.** 13 Nov 2026, from 19:58 to 23:57 SGT.
- **Answers.** 512 tokens each, thinking off. The identity test uses 64-token answers.
- **Sampling.** Temperature 0.7, top-p 0.8, top-k 20. The identity test runs at temperature 0.
- **Penalties.** Requests to TensorFold carry `presence_penalty` 0 and `frequency_penalty` 0. Requests to `mlx-lm` carry neither field. The exact request settings for every run are in the `sampling` column of `runs.csv`.
- **Repeats.** One warm-up thrown away, then 5 timed runs. Every figure is the middle value of the 5.

Serve commands. `MODEL` is the folder of the weights and `DRAFT` is the folder of the draft model.

```bash
mlx_lm.server --model MODEL --host 127.0.0.1 --port 8101
```

```bash
tensorfold serve MODEL --name qwen38-27b-tf-mlx-4bit --host 127.0.0.1 --port 8108 --context 262144 --parallel 16
```

```bash
tensorfold serve MODEL --name qwen38-27b-tf-mlx-4bit --host 127.0.0.1 --port 8112 --context 262144 --parallel 16 --drafter DRAFT
```

What TensorFold 1.2.7 logged at start, first set.

- **Draft off.** "16 streams of 262144 tokens" and "drafts: copies only".
- **Draft on.** "16 streams of 262144 tokens, DFlash2 drafts for 8 streams".

## Results

ELI5: Two sets of runs, about three hours apart. A figure that comes back within a few percent is one I can defend. The draft's speed swings more than the others, and the table shows by how much.

All figures are tok/s, the median of 5 with the range in brackets.

| Measure | Engine | First set | Second set | Change |
|---|---|---|---|---|
| Writing, 1K prompt | `mlx-lm`, no draft | 44.5 (44.4 to 44.5) | 43.5 (43.2 to 43.5) | -2.2% |
| Writing, 1K prompt | TensorFold, draft off | 48.7 (48.6 to 48.7) | 48.2 (47.9 to 48.3) | -0.9% |
| Writing, 1K prompt | TensorFold + DFlash2 | 145.7 (138.4 to 182.9) | 143.9 (137.4 to 158.0) | -1.3% |
| Writing, 4K prompt | `mlx-lm`, no draft | 43.6 (43.4 to 43.6) | 42.6 (42.5 to 42.9) | -2.3% |
| Writing, 4K prompt | TensorFold, draft off | 48.0 (47.8 to 48.0) | 47.6 (47.4 to 47.6) | -0.9% |
| Writing, 4K prompt | TensorFold + DFlash2 | 146.4 (137.4 to 156.4) | 135.5 (121.0 to 178.1) | -7.4% |
| Writing, 32K prompt | `mlx-lm`, no draft | 39.5 (39.1 to 39.8) | 38.7 (38.2 to 39.1) | -2.2% |
| Writing, 32K prompt | TensorFold, draft off | 43.4 (43.0 to 43.7) | 43.2 (42.6 to 43.3) | -0.5% |
| Writing, 32K prompt | TensorFold + DFlash2 | 118.7 (112.3 to 132.8) | 110.0 (105.1 to 118.1) | -7.3% |
| Prose, 8K prompt | TensorFold, draft off | 46.7 (46.4 to 47.2) | 46.6 (46.4 to 47.1) | -0.1% |
| Prose, 8K prompt | TensorFold + DFlash2 | 125.7 (122.3 to 131.9) | 123.8 (121.6 to 135.2) | -1.5% |
| Code, 8K prompt | TensorFold, draft off | 46.5 (46.2 to 47.2) | 46.4 (45.7 to 47.2) | -0.2% |
| Code, 8K prompt | TensorFold + DFlash2 | 222.5 (161.6 to 257.2) | 223.7 (180.3 to 272.3) | +0.5% |
| 8 users, each user | TensorFold, draft off | 33.5 (32.4 to 34.4) | 34.0 (32.3 to 34.5) | +1.6% |
| 8 users, each user | TensorFold + DFlash2 | 42.0 (40.8 to 55.1) | 40.7 (38.0 to 42.3) | -3.0% |
| 8 users, total | TensorFold, draft off | 166.9 (163.5 to 171.1) | 171.7 (169.0 to 176.0) | +2.8% |
| 8 users, total | TensorFold + DFlash2 | 170.8 (148.9 to 179.2) | 186.8 (183.8 to 190.0) | +9.4% |

The card shows the first set.

## What the table says

- **The headline held.** 3.27 times in the first set and 3.31 in the second.
- **At a 32K prompt the multiple is about 3.** First set 118.7 / 39.5 = 3.01 times. Second set 110.0 / 38.7 = 2.84 times.
- **Code gains more than prose.** At 8K prompts the draft wrote code at 222.5 tok/s and prose at 125.7. With the draft off both wrote about 47.
- **The gain is a one-user number.** With 8 users at once, each user wrote 42.0 tok/s with the draft and 33.5 without. 42.0 / 33.5 = 1.25 times. The second set gives 40.7 / 34.0 = 1.20 times.
- **The 8-user totals swing.** The total counts the wait while eight prompts are read. The draft added 3.9 tok/s in the first set, 170.8 - 166.9, and 15.1 in the second, 186.8 - 171.7.
- **The answers match.** At temperature 0, 50 of 50 prompts gave the same answers with the draft on and off, in both sets.
- **No failed rows.** Every request in all 18 runs succeeded.

## First token

Seconds from sending the request to the first token, one user, first set, median of 5.

| Prompt | `mlx-lm`, no draft | TensorFold, draft off | TensorFold + DFlash2 |
|---|---|---|---|
| 1K | 0.61 | 0.60 | 0.57 |
| 4K | 2.37 | 2.52 | 2.38 |
| 32K | 19.83 | 22.07 | 19.97 |

## Check it yourself

From the top of this repository.

```bash
python3 tools/summarize.py findings/01_tensorfold_qwen38-27b_4bit
```

It prints one line per run, test, kind of text, prompt size and user count, then the identity counts. Run ids, first set then second set.

| Test | `mlx-lm` | TensorFold, draft off | TensorFold + DFlash2 |
|---|---|---|---|
| Speed | `3ad3a150c4d0`, `b84e7f743dd8` | `eabffb505d52`, `7a70d741eadd` | `f6775745e273`, `f153458d5e44` |
| Kinds of text | not run | `be444f0d9b7d`, `e48fa9016692` | `62b5bbbbc2b9`, `50eb84cfaaf0` |
| Several users | not run | `12e147f8731e`, `0fdcfa951511` | `b00cab7f6c32`, `7792789e7960` |
| Identity | not run | `f8f1ec1036d9`, `6330c73d7055` | `17b97bf6f3cf`, `3501535d1370` |

- **`rows.csv`.** 1,346 rows, one per request, for all 18 runs.
- **`runs.csv`.** 18 runs with engine, version, start time, settings and sampling.

The tests for several users send no seed. The `no_seed` column in `runs.csv` marks them.

## What I did not verify

- **Why `mlx-lm` came back 2.2% lower in the second set.** No heat warning was recorded. I did not find a cause.
- **Whether `mlx-lm` 0.32.2 can use DFlash2 through its own draft option.** I did not try it. The grey bar is `mlx-lm` with no draft model.
- **The `mlx-lm` side of the text, many-user and identity tests.** I ran those on TensorFold only, draft on against draft off.
- **A wider range than five runs shows.** A third draft run with `--parallel 1 --context 32768` wrote 168.5 tok/s at a 1K prompt. Its rows are not in this folder.

## Credit

- TensorFold is by [@ashxhart](https://x.com/ashxhart). https://github.com/ashhart/TensorFold
- `mlx-lm` is Apple's. https://github.com/ml-explore/mlx-lm
- [@pratikg](https://x.com/pratikg) showed about the same 3 times on an M5 Pro on 4 Nov 2026. This is the 512 GB data point.

If a setting here is wrong, open an issue and I will rerun it.
