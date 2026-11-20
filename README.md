# M5 Ultra benchmarks

ELI5: I'm a learner with one Mac Studio M5 Ultra 512 GB, and I time local AI models on it. Each finding below is a folder with the report, the charts and every raw row, so you can check my arithmetic.

I post these as [@LazyLocalLLM](https://x.com/LazyLocalLLM) on X.

## Benchmark summary

The best speed I have measured for each model, on one page, with a max and a median figure. See [benchmark_summary](benchmark_summary).

## Findings

Newest first.

| # | Runs | Finding | Headline |
|---|---|---|---|
| 9 | 20 to 21 Nov 2026 | [Four more models on oMLX 0.8.0, max and median speed](findings/09_omlx_080_four_models) | On oMLX 0.8.0, GLM-5.3 Flash 4-bit wrote 80.2 tok/s at its max and 67.8 with its own sampler. Inkling 2 Small wrote 51.6 and 42.2. Qwen3.8 Flash Next at full precision wrote 53.3 with draft depth fixed at 4, 49.3 at the default, and 33.2 with its own sampler. GLM-5.3 4-bit wrote 24.6 and 24.5. Three of the four wrote reasoning text. |
| 4 | 20 Nov 2026 | [DeepSeek V4.1 Flash on TensorFold 1.3.0 against 1.2.10](findings/04_dsv41_tensorfold_130) | On two server starts each, in both orders, TensorFold 1.3.0 read prompts 3% to 11% faster than 1.2.10 and wrote at the same speed with drafts on, 70.5 against 69.5 tok/s greedy on code. 17 of 68 replies on 1.3.0 held one pause of 0.25 to 0.58 s, and none did on 1.2.10. With drafts off, on one start each, 1.3.0 wrote 40.5 tok/s against 44.7. |
| 5 | 20 Nov 2026 | [DeepSeek V4.1 Flash on oMLX 0.8.0, pushing the max](findings/05_dsv41_omlx_080_max_push) | With draft depth fixed at 5 and replies of up to 2,048 tokens, oMLX 0.8.0 wrote 84.1 and 81.3 tok/s on new code at a 1K prompt on two starts, against 77.2 and 76.2 at the default depth. With 512-token replies at a 4K prompt the same setting wrote 118.3 tok/s copying the prompt and 114.0 counting from 1. With the model's own sampler fixed depth 5 was slower, 50.5 against 57.9 tok/s. |
| 6 | 20 Nov 2026 | [DeepSeek V4.1 Flash on TensorFold 1.3.0, pushing the max](findings/06_dsv41_tensorfold_130_max_push) | At its defaults TensorFold 1.3.0 wrote 76.4 and 75.6 tok/s on two starts on new code with replies of up to 2,048 tokens at a 4K prompt. With 512-token replies at a 1K prompt it wrote 159.1 tok/s copying the prompt and 106.9 counting from 1. None of six draft settings separated from the defaults, with cell medians at 0.95 to 1.06 times. |
| 7 | 20 Nov 2026 | [Qwen3.8 27B and Flash Next on TensorFold 1.3.0, pushing the max](findings/07_qwen38_tensorfold_130) | TensorFold 1.3.0 wrote 331.3 tok/s on Qwen3.8 27B 4-bit on new code with replies of up to 2,048 tokens at a 1K prompt, 7.3 times `mlx-lm` 0.32.2 on the same weights, and 148.2 with the model's own sampler at 4K, 3.4 times. Copying the prompt it wrote 824.0. Flash Next 4-bit wrote 204.4, 126.7 sampled and 292.2 copying. Flash Next 6-bit wrote 193.0 and 117.4 sampled. |
| 8 | 20 Nov 2026 | [DeepSeek V4.1 Flash on mlx-serve 26.11.3, pushing the max](findings/08_dsv41_mlxserve_26113) | mlx-serve 26.11.3 wrote 93.8 and 95.3 tok/s on the Lossless pack on two starts, on new code at its defaults with replies of up to 2,048 tokens at a 4K prompt. With the model's own sampler it wrote 57.5. Copying the prompt it wrote 167.0 and counting from 1 it wrote 121.5. The defaults are not bit-exact, by the server log. Qwen3.8 27B full wrote 6.8 tok/s sampled on one start. |
| 3 | 20 Nov 2026 | [DeepSeek V4.1 Flash on oMLX 0.8.0, max and median speed](findings/03_dsv41_omlx_080) | oMLX 0.8.0 wrote 71.2 tok/s on DeepSeek V4.1 Flash oQ4e-mtp, greedy on code at its default draft depth, and 56.5 with the model's own sampler on mixed text. Deeper draft settings gave 65.8 to 78.7, inside the noise between server starts. |
| 2 | 16 to 18 Nov 2026 | [Ten open-weight models, from 4K to 1M tokens](findings/02_ten_models_4k_to_1m) | Qwen3.8 Flash Next 4-bit wrote 124.1 tok/s at a 128K prompt and 93.2 at 1M. DeepSeek V4.1 Flash 1017 Lossless wrote 55.0 to 58.3 tok/s at every length from 4K to 1M. |
| 1 | 13 Nov 2026 | [TensorFold with a draft model on Qwen3.8-27B 4-bit](findings/01_tensorfold_qwen38-27b_4bit) | TensorFold 1.2.7 with the DFlash2 draft wrote 145.7 tok/s at a 1K prompt. `mlx-lm` 0.32.2 wrote 44.5 on the same weights. That is 3.3 times. |

## The machine

- Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2.
- One harness for every engine. Engines run with the network closed.

## How to read a finding

- **`README.md`** is the report. It names the engine and its version, the weights and their commit, the settings, the date and the number of runs behind every figure.
- **`rows.csv`** has one line per request, straight from my bench database. **`runs.csv`** has one line per run, with engine, version, settings and sampler.
- **Medians.** Each figure is the middle of its runs. A report gives the range where the runs varied.
- **Not a ranking of engines.** Each engine runs at the best setup I found for it, and a report says which one.

## Check it yourself

From the top of this repository, with Python 3.9 or newer and nothing else installed.

```bash
python3 tools/summarize.py findings/02_ten_models_4k_to_1m
```

It prints the median and range of each run and prompt size from that folder's `rows.csv` and `runs.csv`.

## Corrections

If I've set an engine up wrong, [open an issue](https://github.com/LazyLocalLLM/m5-ultra-512-benchmarks/issues). I'll rerun it and post the fix.

## Licence

Data, charts and text under CC BY 4.0. Code under MIT. See [LICENSE.md](LICENSE.md).
