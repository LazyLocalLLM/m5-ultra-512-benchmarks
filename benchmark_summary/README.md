# Benchmark summary

ELI5: One page with the best speed I have measured for each model on one Mac Studio M5 Ultra 512 GB. Every line links to the finding folder that holds the report and the raw rows.

Updated 20 Nov 2026 18:20 SGT. All figures are decode speed in tok/s for one user.

## Two speeds per model

ELI5: People measure speed in different ways, so I show two. The max is the top speed with everything tuned for it. The median is closer to what you get in daily use.

- **Max.** Greedy decoding at temperature 0 on a real task, with the engine's drafting tuned for speed. The model writes a new code module from the code in the prompt. The prompt is code where code wrote faster, and the line says so.
- **Median.** The model's own recommended sampler, on a prompt of mixed prose and code.
- Each figure is the middle value of its timed runs. The run count, prompt length, reply length and date are on each line.
- Reply length is part of the setup and differs by line. Longer replies wrote faster where I measured both, so compare two Max lines only at the same reply length. The full table below has each model at every reply length I ran.
- "not run yet" means I have not measured it. It does not mean the engine cannot do it.

## Best per model

ELI5: The fastest setup I found for each model, one line each.

| Model | Max tok/s | Max setup | Median tok/s | Median setup | Finding |
|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | not run yet |  | **58.3** | mlx-serve 26.11.2, defaults, prompt lookup drafts on. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| GLM-5.3, 4-bit | not run yet |  | **24.3** | oMLX 0.7.3 with its kernels, MTP off. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| GLM-5.3 Flash, 6-bit | not run yet |  | **57.8** | oMLX 0.7.3 with its kernels, MTP on. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| GLM-5.3 Flash, 4-bit | not run yet |  | **68.8** | oMLX 0.7.3 with its kernels, MTP on. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| Inkling 2 Small | not run yet |  | **41.3** | oMLX main 624cff0e with its kernels, DSpark draft on. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 27B, 4-bit | not run yet |  | **154.2** | TensorFold 1.2.8, DFlash2 drafter (z-lab). 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 27B, full | not run yet |  | **8.8** | mlx-serve 26.11.2, defaults, prompt lookup drafts on. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 Flash Next, 4-bit | not run yet |  | **129.2** | TensorFold 1.2.8, MTP on, recipe line. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 Flash Next, 6-bit | not run yet |  | **114.0** | TensorFold 1.2.8, MTP on, recipe line. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 Flash Next, full | not run yet |  | **34.9** | oMLX 0.7.3 with its kernels, MTP on (built-in head). 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-17 | [2](../findings/02_ten_models_4k_to_1m) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | **84.1** | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5. 1K prompt, code, replies up to 2,048 tokens, 5 runs, 2026-11-20 | **56.5** | oMLX 0.8.0 with its kernels, MTP drafts on, default depth. 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-20 | [5](../findings/05_dsv41_omlx_080_max_push), [3](../findings/03_dsv41_omlx_080) |
| DeepSeek V4.1 Flash 1017, maker's files | **70.5** | TensorFold 1.3.0, drafts at defaults (DSpark and copies). 1K prompt, code, replies up to 512 tokens, 5 runs, 2026-11-20 | **44.5** | TensorFold 1.3.0, drafts at defaults (DSpark and copies). 4K prompt, mixed, replies up to 512 tokens, 5 runs, 2026-11-20 | [4](../findings/04_dsv41_tensorfold_130) |

## Ceiling on easy text

ELI5: Some tests hand the model text it can guess almost perfectly. The drafts land nearly every time, so the speed is far above real work. I measure two such tests and keep them apart from Max.

- **Copy task.** The model repeats the code in the prompt word for word. Compare this one with benchmark figures made on repeated or copied text.
- **Counting toy.** The model counts up from 1, one number a line.
- Both are greedy at temperature 0. Neither is a speed you get when the model writes something new.

| Model | Copy task tok/s | Copy task setup | Counting toy tok/s | Counting toy setup | Finding |
|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | **118.3** | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5. 4K prompt, code, replies up to 512 tokens, 5 runs, 2026-11-20 | **114.0** | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5. 4K prompt, code, replies up to 512 tokens, 5 runs, 2026-11-20 | [5](../findings/05_dsv41_omlx_080_max_push) |

## Every setup measured

ELI5: Everything behind the table above, including the setups that were not the fastest. The range is the slowest and fastest single run.

| Model | Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | median | mlx-serve 26.11.2, defaults, prompt lookup drafts on | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 58.3 | 51.3 to 70.6 | 5 | 2026-11-17 | `a227c80d0e61` | [2](../findings/02_ten_models_4k_to_1m) |
| GLM-5.3, 4-bit | median | oMLX 0.7.3 with its kernels, MTP off | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 24.3 | 24.2 to 24.3 | 5 | 2026-11-17 | `626f0c1b4ad9` | [2](../findings/02_ten_models_4k_to_1m) |
| GLM-5.3 Flash, 6-bit | median | oMLX 0.7.3 with its kernels, MTP on | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 57.8 | 55.6 to 69.0 | 5 | 2026-11-17 | `2b64d54e7e5c` | [2](../findings/02_ten_models_4k_to_1m) |
| GLM-5.3 Flash, 4-bit | median | oMLX 0.7.3 with its kernels, MTP on | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 68.8 | 61.0 to 76.1 | 5 | 2026-11-17 | `8453ec3a372d` | [2](../findings/02_ten_models_4k_to_1m) |
| Inkling 2 Small | median | oMLX main 624cff0e with its kernels, DSpark draft on | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 41.3 | 38.5 to 42.9 | 5 | 2026-11-17 | `5c4d781c0e3d` | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 27B, 4-bit | median | TensorFold 1.2.8, DFlash2 drafter (z-lab) | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 154.2 | 136.9 to 219.4 | 5 | 2026-11-17 | `a798cea8b67e` | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 27B, 4-bit | median | TensorFold 1.2.7, DFlash2 drafter (z-lab) | temperature 0.7, top-p 0.8, top-k 20 | 1K mixed | 512 | 145.7 | 138.4 to 182.9 | 5 | 2026-11-13 | `f6775745e273` | [1](../findings/01_tensorfold_qwen38-27b_4bit) |
| Qwen3.8 27B, 4-bit | median | TensorFold 1.2.7, no draft model | temperature 0.7, top-p 0.8, top-k 20 | 1K mixed | 512 | 48.7 | 48.6 to 48.7 | 5 | 2026-11-13 | `eabffb505d52` | [1](../findings/01_tensorfold_qwen38-27b_4bit) |
| Qwen3.8 27B, 4-bit | median | mlx-lm 0.32.2, defaults, the baseline | temperature 0.7, top-p 0.8, top-k 20 | 1K mixed | 512 | 44.5 | 44.4 to 44.5 | 5 | 2026-11-13 | `3ad3a150c4d0` | [1](../findings/01_tensorfold_qwen38-27b_4bit) |
| Qwen3.8 27B, full | median | mlx-serve 26.11.2, defaults, prompt lookup drafts on | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 8.8 | 8.3 to 9.8 | 5 | 2026-11-17 | `a30a665ca3ee` | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 Flash Next, 4-bit | median | TensorFold 1.2.8, MTP on, recipe line | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 129.2 | 123.9 to 139.2 | 5 | 2026-11-17 | `72fae37b87f0` | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 Flash Next, 6-bit | median | TensorFold 1.2.8, MTP on, recipe line | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 114.0 | 108.6 to 125.6 | 5 | 2026-11-17 | `ea26b8919e88` | [2](../findings/02_ten_models_4k_to_1m) |
| Qwen3.8 Flash Next, full | median | oMLX 0.7.3 with its kernels, MTP on (built-in head) | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 34.9 | 32.2 to 35.9 | 5 | 2026-11-17 | `c4bbe7d3230c` | [2](../findings/02_ten_models_4k_to_1m) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | max | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 1K code | 2,048 | 84.1 | 78.5 to 84.8 | 5 | 2026-11-20 | `7513746c2ce0` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | max | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 4K code | 2,048 | 82.7 | 77.7 to 85.7 | 5 | 2026-11-20 | `7513746c2ce0` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | max | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 1K code | 2,048 | 77.2 | 72.5 to 78.7 | 5 | 2026-11-20 | `7ece67645192` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | max | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 1K code | 512 | 71.2 | 65.7 to 73.1 | 5 | 2026-11-20 | `800dd0f8839c` | [3](../findings/03_dsv41_omlx_080) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | max | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 1K code | 128 | 58.2 | 52.4 to 60.1 | 5 | 2026-11-20 | `800dd0f8839c` | [3](../findings/03_dsv41_omlx_080) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | copy task | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 4K code | 512 | 118.3 | 110.7 to 121.0 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | copy task | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 1K code | 512 | 114.7 | 113.6 to 118.1 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | copy task | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 4K code | 512 | 98.3 | 93.3 to 99.9 | 5 | 2026-11-20 | `526b05fc2a44` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | counting toy | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 4K code | 512 | 114.0 | 113.7 to 114.3 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | counting toy | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 1K code | 512 | 113.0 | 111.9 to 114.0 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | counting toy | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 4K code | 512 | 90.6 | 90.4 to 90.8 | 5 | 2026-11-20 | `526b05fc2a44` | [5](../findings/05_dsv41_omlx_080_max_push) |
| DeepSeek V4.1 Flash 1017, oQ4e-mtp | median | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 56.5 | 55.1 to 58.5 | 5 | 2026-11-20 | `800dd0f8839c` | [3](../findings/03_dsv41_omlx_080) |
| DeepSeek V4.1 Flash 1017, maker's files | max | TensorFold 1.3.0, drafts at defaults (DSpark and copies) | greedy, temperature 0 | 1K code | 512 | 70.5 | 65.9 to 73.9 | 5 | 2026-11-20 | `778e5c808b88` | [4](../findings/04_dsv41_tensorfold_130) |
| DeepSeek V4.1 Flash 1017, maker's files | max | TensorFold 1.3.0, drafts at defaults (DSpark and copies) | greedy, temperature 0 | 1K code | 128 | 62.6 | 56.7 to 66.0 | 5 | 2026-11-20 | `778e5c808b88` | [4](../findings/04_dsv41_tensorfold_130) |
| DeepSeek V4.1 Flash 1017, maker's files | median | TensorFold 1.3.0, drafts at defaults (DSpark and copies) | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 44.5 | 41.1 to 48.2 | 5 | 2026-11-20 | `778e5c808b88` | [4](../findings/04_dsv41_tensorfold_130) |

## Check it yourself

ELI5: Each figure here is recomputed from the raw rows in its finding folder. You can do the same.

- `summary.csv` in this folder holds every line above with its run id.
- From the top of the repository, `python3 tools/summarize.py findings/FOLDER` prints the median and range of each run in that folder.
- The weights behind each model name are in the `weights` column of `summary.csv`.
- If I have set an engine up wrong, [open an issue](https://github.com/LazyLocalLLM/m5-ultra-512-benchmarks/issues). I will rerun it and post the fix.
