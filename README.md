# M5 Ultra benchmarks

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: I'm a learner with one Mac Studio M5 Ultra 512 GB, and I time local AI models on it. This page has the best speed I have measured for each model, then every finding behind it. Each finding is a folder with the report, the charts and every raw row, so you can check my arithmetic.

## Executive summary

ELI5: The page in seven lines. Every figure here is recomputed from the raw rows each time the page is built.

Updated 23 Nov 2026 20:05 SGT. Decode speed in tok/s, one user, one Mac.

- **Fastest on new code.** Qwen3.8 27B, 4-bit wrote 323.4 tok/s on TensorFold 1.3.4. Next are Qwen3.8 Flash Next, 4-bit at 211.5 and Qwen3.8 Flash Next, 6-bit at 201.3.
- **Fastest in daily use.** Qwen3.8 27B, 4-bit wrote 149.6 tok/s on TensorFold 1.3.4. Next are Qwen3.8 Flash Next, 4-bit at 128.4 and Qwen3.8 Flash Next, IQ3_S at 126.0.
- **Two speeds per model.** Max is greedy at temperature 0 while the model writes new code. Median is the model's own sampler on mixed text, which is closer to daily use.
- **Prefill too.** The table also has how fast each model read a cold prompt, with the prompt size.
- **Coverage.** 28 models, 422 setups and 34 findings.
- **Newest finding.** Finding 34, 23 to 24 Nov 2026. [MiniMax H3 video on mlx-serve 26.11.3, round two, the 4-bit pack and HyperFlow H3 Flash, seconds per clip](findings/34_minimax_h3_video_mlxserve_round2).
- **Check it.** Every figure links to a folder with the rows it came from. If I have set an engine up wrong, [open an issue](https://github.com/LazyLocalLLM/m5-ultra-512-benchmarks/issues).

## Benchmark summary

ELI5: The fastest setup I found for each model, one line each. The same tables, with the notes on how to read them, are in [benchmark_summary](benchmark_summary).

- **Filter it.** Open [summary.csv](benchmark_summary/summary.csv). GitHub shows that file as a table with a search box, so you can type a model, an engine or a kind and see only those lines.
- **Unfold it.** Under "Every setup measured" below, click a model to see all of its setups.
- "not run yet" means I have not measured it. A line marked "older release" has been replaced by a newer run.
- **Find the model.** Each model name links to the weights I ran. The row with a draft head joined here links to the base weights, and [finding 9](findings/09_omlx_080_four_models) has the join steps.

### Best per model

The exact setup behind each figure is one click away, under "Every setup measured". "Reply text" says whether the timed replies were the model's answer or its reasoning. A reasoning speed is not an answer speed.

- **Prefill** is how fast the engine read a cold prompt, the prompt's tokens divided by the time to the first token. Each figure is the middle of every timed request on one engine release, at one prompt size and one kind of text. The cell names both. Reading speed changes with both, so compare two cells only where they match.
- **Prefill engine.** The cell shows the best line of the engine of the best max, on a current release. Another engine is shown, and named, only where it read more than 5% faster on the same text at the same size. Every engine's line at every size is in [prefill.csv](benchmark_summary/prefill.csv).

| Model | Max tok/s | Median tok/s | Prefill tok/s | Reply text | Engine | Finding |
|---|---|---|---|---|---|---|
| [DeepSeek V4.1 Flash 1017, Lossless](https://huggingface.co/ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless) | **95.3** | **57.9** | **3,187.2**, 4K mixed prompt | answer | mlx-serve 26.11.3 | [8](findings/08_dsv41_mlxserve_26113) |
| [GLM-5.3, 4-bit](https://huggingface.co/mlx-community/GLM-5.3-4bit) | **24.6** | **24.5** | **645.7**, 4K mixed prompt | reasoning | oMLX 0.8.0 with its kernels | [9](findings/09_omlx_080_four_models) |
| [GLM-5.3, 4-bit, draft head joined here](https://huggingface.co/mlx-community/GLM-5.3-4bit) | **23.4** | **25.0** | **646.9**, 4K mixed prompt | reasoning | oMLX 0.8.0 with its kernels | [9](findings/09_omlx_080_four_models) |
| [GLM-5.3 Flash, 6-bit](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ6e-mtp) | not run yet | **57.8** | **1,858.8**, 4K mixed prompt | reasoning | oMLX 0.7.3 with its kernels | [2](findings/02_ten_models_4k_to_1m) |
| [GLM-5.3 Flash, oQ4e](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) | **84.9** | **70.1** | **2,173.5**, 4K mixed prompt, on oMLX 0.8.3 with its kernels | answer for max, reasoning for median | TensorFold 1.3.4 for max, oMLX 0.8.3 with its kernels for median | [27](findings/27_tensorfold_134_refresh), [26](findings/26_omlx_083_refresh) |
| [Inkling 2 Small](https://huggingface.co/mlx-community/Inkling-2-Small-oQ4e) | **52.7** | **41.3** | **1,259.3**, 4K code prompt | mostly reasoning | oMLX 0.8.2 with its kernels | [16](findings/16_omlx_082_refresh) |
| [Qwen3.8 27B, 4-bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) | **323.4** | **149.6** | **1,863.4**, 4K mixed prompt | answer | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Qwen3.8 27B, full](https://huggingface.co/mlx-community/Qwen3.8-27B-bf16) | **6.9** | **7.1** | **1,885.2**, 4K code prompt | answer | mlx-serve 26.11.3 | [8](findings/08_dsv41_mlxserve_26113) |
| [Qwen3.8 Flash Next, 4-bit](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP) | **211.5** | **128.4** | **4,057.1**, 4K code prompt | answer | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Qwen3.8 Flash Next, 6-bit](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP) | **201.3** | **114.5** | **3,841.0**, 4K mixed prompt | answer | TensorFold 1.3.3 | [19](findings/19_tensorfold_133_refresh) |
| [Qwen3.8 Flash Next, full](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | **54.5** | **34.4** | **3,233.3**, 4K code prompt | answer | oMLX 0.8.3 with its kernels | [26](findings/26_omlx_083_refresh) |
| [DeepSeek V4.1 Flash 1017, oQ4e-mtp](https://huggingface.co/mlx-community/DeepSeek-V4.1-Flash-1017-oQ4e-mtp) | **86.2** | **57.9** | **3,758.0**, 32K code prompt | answer | oMLX 0.8.0 with its kernels | [5](findings/05_dsv41_omlx_080_max_push), [3](findings/03_dsv41_omlx_080) |
| [DeepSeek V4.1 Flash 1017, maker's files](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) | **105.7** | **69.9** | **1,485.4**, 32K code prompt | answer | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [GLM-5.3 Flash, 4-bit](https://huggingface.co/TensorFold/GLM-5.3-Flash-MLX-4bit-MTP) | **104.7** | **85.9** | **2,234.3**, 4K mixed prompt, on oMLX 0.8.1 with its kernels | answer | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh), [15](findings/15_glm53_flash_two_builds) |
| [Hy4-flash, 4-bit](https://huggingface.co/TensorFold/Hy4-flash-MLX-4bit-MTP) | **79.0** | **51.6** | **1,649.2**, 1K code prompt | reasoning | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Hy4-flash, 8-bit](https://huggingface.co/TensorFold/Hy4-flash-MLX-8bit-MTP) | **55.2** | **44.8** | **1,235.8**, 1K code prompt | reasoning | TensorFold 1.3.3 | [19](findings/19_tensorfold_133_refresh) |
| [Hy4-flash, oQ4h](https://huggingface.co/Jundot/Hy4-flash-oQ4h-mtp) | **76.2** | **54.0** | **2,302.3**, 4K mixed prompt | answer for max, reasoning for median | oMLX 0.8.3 with its kernels for max, oMLX 0.8.1 with its kernels for median | [26](findings/26_omlx_083_refresh), [12](findings/12_hy4_flash_omlx_081) |
| [Inkling 2 Mini, oQ4e](https://huggingface.co/mlx-community/Inkling-2-Mini-oQ4e-mtp) | **108.1** | **83.3** | **3,257.6**, 4K code prompt | reasoning | oMLX 0.8.3 with its kernels | [26](findings/26_omlx_083_refresh) |
| [Inkling 2 Mini, oQ3e](https://huggingface.co/mlx-community/Inkling-2-Mini-oQ3e-mtp) | **105.1** | **67.1** | **2,850.7**, 4K code prompt | reasoning | oMLX 0.8.1 with its kernels | [14](findings/14_inkling2_mini_omlx_081) |
| [Inkling 2 Mini, 8-bit](https://huggingface.co/ddalcu/Inkling-2-Mini-MLX-8bit) | **146.8** | **105.2** | **4,932.1**, 4K code prompt | reasoning | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83 | [20](findings/20_inkling2_mini_mlxserve_pre) |
| [Inkling 2 Mini, Bare Speed](https://huggingface.co/Youssofal/Inkling-2-Mini-MTPLX-Bare-Speed) | **153.0** | **124.7** | **4,692.6**, 4K mixed prompt | reasoning | MTPLX 2.13.2 | [29](findings/29_inkling2_mini_mtplx_2132) |
| [Inkling 2 Mini, Optimized Speed](https://huggingface.co/Youssofal/Inkling-2-Mini-MTPLX-Optimized-Speed) | **152.0** | **113.0** | **4,675.6**, 4K code prompt | reasoning | MTPLX 2.13.2 | [29](findings/29_inkling2_mini_mtplx_2132) |
| [Inkling 2 Mini, Optimized Quality](https://huggingface.co/Youssofal/Inkling-2-Mini-MTPLX-Optimized-Quality) | **133.8** | **105.6** | **4,675.6**, 4K code prompt | reasoning | MTPLX 2.13.2 | [29](findings/29_inkling2_mini_mtplx_2132) |
| [Inkling 2 Mini, 4-bit](https://huggingface.co/mlx-community/Inkling-2-Mini-4bit) | **39.8** | **39.4** | **3,361.2**, 4K code prompt | reasoning | Rapid-MLX 1.1.0 | [23](findings/23_inkling2_mini_rapidmlx_110) |
| [Qwen3.8 Flash Next, IQ3_S](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) | **196.4** | **126.0** | **2,884.2**, 4K code prompt | answer | Strata 0.2.20 | [28](findings/28_qwen38_flash_next_strata_0220) |
| [Inkling 2 Mini, SQ-20](https://huggingface.co/strata-engine/Inkling-2-Mini-Strata) | **106.1** | **59.3** | **3,386.8**, 4K mixed prompt | answer | Strata 0.2.20 | [30](findings/30_inkling2_mini_strata_0220) |
| [Inkling 2 Mini, UD-Q8_K_XL](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | **60.1** | **58.2** | **3,216.4**, 4K mixed prompt | answer | Strata 0.2.20 | [30](findings/30_inkling2_mini_strata_0220) |
| [Inkling 2 Mini, maker's release](https://huggingface.co/thinkingmachines/Inkling-2-Mini) | **82.3** | **61.7** | **2,129.4**, 4K code prompt | reasoning | Ollama 0.40.17 | [31](findings/31_inkling2_mini_ollama_04017) |

### Ceiling on easy text

ELI5: Two tests hand the model text it can guess almost perfectly, copying the prompt and counting from 1. The speed is far above real work, so I keep these apart from Max.

| Model | Copy task tok/s | Counting toy tok/s | Engine | Finding |
|---|---|---|---|---|
| [DeepSeek V4.1 Flash 1017, Lossless](https://huggingface.co/ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless) | **167.0** | **121.5** | mlx-serve 26.11.3 | [8](findings/08_dsv41_mlxserve_26113) |
| [GLM-5.3 Flash, oQ4e](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) | **157.1** | **94.9** | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Qwen3.8 27B, 4-bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) | **818.8** | **450.6** | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Qwen3.8 Flash Next, 4-bit](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP) | **360.3** | **377.8** | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Qwen3.8 Flash Next, 6-bit](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP) | **260.1** | **296.2** | TensorFold 1.3.3 | [19](findings/19_tensorfold_133_refresh) |
| [Qwen3.8 Flash Next, full](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | **128.4** | **51.5** | oMLX 0.8.3 with its kernels | [26](findings/26_omlx_083_refresh) |
| [DeepSeek V4.1 Flash 1017, oQ4e-mtp](https://huggingface.co/mlx-community/DeepSeek-V4.1-Flash-1017-oQ4e-mtp) | **118.3** | **114.0** | oMLX 0.8.0 with its kernels | [5](findings/05_dsv41_omlx_080_max_push) |
| [DeepSeek V4.1 Flash 1017, maker's files](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) | **185.1** | **138.3** | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [GLM-5.3 Flash, 4-bit](https://huggingface.co/TensorFold/GLM-5.3-Flash-MLX-4bit-MTP) | **174.8** | **114.7** | TensorFold 1.3.4 | [27](findings/27_tensorfold_134_refresh) |
| [Hy4-flash, oQ4h](https://huggingface.co/Jundot/Hy4-flash-oQ4h-mtp) | **95.9** | **94.0** | oMLX 0.8.3 with its kernels | [26](findings/26_omlx_083_refresh) |

### Every setup measured

ELI5: Everything behind the tables above, including the setups that were not the fastest. Click a model to open its lines. The range is the slowest and fastest single run.

<details>
<summary><b>DeepSeek V4.1 Flash 1017, Lossless</b>, 14 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | mlx-serve 26.11.3, warmup-full, defaults with --no-decode-attn-quant, second start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 4K code | 2,048 | 95.3 | 90.1 to 100.3 | 5 | 2026-11-20 | `4d0f49b9ac43` | [8](findings/08_dsv41_mlxserve_26113) |
| max | mlx-serve 26.11.3, warmup-full, defaults, first start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 4K code | 2,048 | 93.8 | 86.1 to 99.8 | 5 | 2026-11-20 | `ddee83910540` | [8](findings/08_dsv41_mlxserve_26113) |
| max | mlx-serve 26.11.3, warmup-full, defaults with --no-decode-attn-quant, second start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 1K code | 512 | 93.2 | 72.4 to 94.4 | 5 | 2026-11-20 | `4d0f49b9ac43` | [8](findings/08_dsv41_mlxserve_26113) |
| max | mlx-serve 26.11.3, warmup-full, lm head kept dense by the log (MLX_SERVE_DSV41_HEAD8=0), --no-decode-attn-quant, prompt lookup drafts on | greedy, temperature 0 | 4K code | 2,048 | 91.6 | 87.7 to 96.7 | 5 | 2026-11-21 | `18b1cdba2631` | [8](findings/08_dsv41_mlxserve_26113) |
| max | mlx-serve 26.11.3, warmup-full, defaults with --no-decode-attn-quant, second start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 1K code | 2,048 | 91.4 | 83.6 to 98.6 | 5 | 2026-11-20 | `4d0f49b9ac43` | [8](findings/08_dsv41_mlxserve_26113) |
| max | mlx-serve 26.11.3, warmup-full, lm head kept dense by the log (MLX_SERVE_DSV41_HEAD8=0), --no-decode-attn-quant, prompt lookup drafts on | greedy, temperature 0 | 1K code | 2,048 | 90.2 | 85.2 to 97.7 | 5 | 2026-11-21 | `18b1cdba2631` | [8](findings/08_dsv41_mlxserve_26113) |
| copy task | mlx-serve 26.11.3, warmup-full, defaults, first start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 1K code | 512 | 167.0 | 159.0 to 169.0 | 5 | 2026-11-20 | `ddee83910540` | [8](findings/08_dsv41_mlxserve_26113) |
| copy task | mlx-serve 26.11.3, warmup-full, defaults with --no-decode-attn-quant, second start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 1K code | 512 | 165.1 | 159.5 to 170.1 | 5 | 2026-11-20 | `4d0f49b9ac43` | [8](findings/08_dsv41_mlxserve_26113) |
| counting toy | mlx-serve 26.11.3, warmup-full, defaults, first start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 4K code | 512 | 121.5 | 121.3 to 121.9 | 5 | 2026-11-20 | `ddee83910540` | [8](findings/08_dsv41_mlxserve_26113) |
| counting toy | mlx-serve 26.11.3, warmup-full, defaults with --no-decode-attn-quant, second start, lm head 8-bit by the log, prompt lookup drafts on | greedy, temperature 0 | 1K code | 512 | 121.5 | 121.2 to 121.9 | 5 | 2026-11-20 | `4d0f49b9ac43` | [8](findings/08_dsv41_mlxserve_26113) |
| median | mlx-serve 26.11.2, defaults, prompt lookup drafts on, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 58.3 | 51.3 to 70.6 | 5 | 2026-11-17 | `a227c80d0e61` | [2](findings/02_ten_models_4k_to_1m) |
| median | mlx-serve 26.11.3, warmup-full, lm head kept dense by the log (MLX_SERVE_DSV41_HEAD8=0), --no-decode-attn-quant, prompt lookup drafts on | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 57.9 | 49.7 to 59.2 | 5 | 2026-11-21 | `18b1cdba2631` | [8](findings/08_dsv41_mlxserve_26113) |
| median | mlx-serve 26.11.3, warmup-full, defaults, first start, lm head 8-bit by the log, prompt lookup drafts on | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 57.5 | 50.9 to 65.6 | 5 | 2026-11-20 | `ddee83910540` | [8](findings/08_dsv41_mlxserve_26113) |
| median | mlx-serve 26.11.3, warmup-full, defaults with --no-decode-attn-quant, second start, lm head 8-bit by the log, prompt lookup drafts on | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 56.4 | 52.6 to 61.4 | 5 | 2026-11-20 | `4d0f49b9ac43` | [8](findings/08_dsv41_mlxserve_26113) |

</details>

<details>
<summary><b>GLM-5.3, 4-bit</b>, 3 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.0 with its kernels, MTP off, reply is reasoning text, 512-token replies | greedy, temperature 0 | 4K code | 512 | 24.6 | 24.5 to 24.7 | 5 | 2026-11-20 | `2641f174f97a` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.8.0 with its kernels, MTP off, reply is reasoning text | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 24.5 | 24.5 to 24.5 | 5 | 2026-11-20 | `2641f174f97a` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.7.3 with its kernels, MTP off, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 24.3 | 24.2 to 24.3 | 5 | 2026-11-17 | `626f0c1b4ad9` | [2](findings/02_ten_models_4k_to_1m) |

</details>

<details>
<summary><b>GLM-5.3, 4-bit, draft head joined here</b>, 2 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.0 with its kernels, MTP on, default depth, reply is reasoning text, 512-token replies | greedy, temperature 0 | 4K code | 512 | 23.4 | 22.2 to 24.4 | 5 | 2026-11-21 | `1cdf9099760b` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.8.0 with its kernels, MTP on, default depth, reply is reasoning text | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 25.0 | 23.0 to 29.0 | 5 | 2026-11-21 | `1cdf9099760b` | [9](findings/09_omlx_080_four_models) |

</details>

<details>
<summary><b>GLM-5.3 Flash, 6-bit</b>, 1 setup</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| median | oMLX 0.7.3 with its kernels, MTP on | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 57.8 | 55.6 to 69.0 | 5 | 2026-11-17 | `2b64d54e7e5c` | [2](findings/02_ten_models_4k_to_1m) |

</details>

<details>
<summary><b>GLM-5.3 Flash, oQ4e</b>, 40 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | greedy, temperature 0 | 4K code | 2,048 | 84.9 | 75.7 to 99.6 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 4K code | 2,048 | 84.8 | 80.4 to 85.9 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 4K code | 2,048 | 82.9 | 77.1 to 89.2 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 1K code | 2,048 | 81.2 | 76.6 to 83.6 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 1K code | 2,048 | 80.7 | 74.5 to 84.5 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| max | oMLX 0.8.0 with its kernels, MTP on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 80.2 | 68.4 to 87.6 | 5 | 2026-11-21 | `8f12a00bcc4f` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.1 with its kernels, MTP on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 78.7 | 73.7 to 86.2 | 5 | 2026-11-21 | `421e19a82f36` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | greedy, temperature 0 | 1K code | 2,048 | 78.3 | 77.3 to 85.3 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| max | oMLX 0.8.3 with its kernels, MTP on, default depth, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 77.4 | 71.2 to 82.5 | 5 | 2026-11-23 | `42c428b2af1f` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.2 with its kernels, MTP on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 76.0 | 72.9 to 78.8 | 5 | 2026-11-21 | `34ae658e42ba` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.0 with its kernels, MTP on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 74.7 | 68.9 to 81.3 | 5 | 2026-11-21 | `8f12a00bcc4f` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.2 with its kernels, MTP on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 73.9 | 69.3 to 81.1 | 5 | 2026-11-21 | `34ae658e42ba` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.3 with its kernels, MTP on, default depth, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 73.6 | 66.3 to 77.4 | 5 | 2026-11-23 | `42c428b2af1f` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.1 with its kernels, MTP on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 73.4 | 66.6 to 77.3 | 5 | 2026-11-21 | `421e19a82f36` | [15](findings/15_glm53_flash_two_builds) |
| max | oMLX 0.8.0 with its kernels, MTP on, fixed depth 4, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 71.7 | 66.4 to 80.9 | 5 | 2026-11-21 | `605e0068ff28` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.0 with its kernels, MTP on, fixed depth 4, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 68.9 | 62.1 to 74.9 | 5 | 2026-11-21 | `605e0068ff28` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.1 with its kernels, MTP off, reply is reasoning text | greedy, temperature 0 | 1K code | 512 | 51.7 | 51.0 to 51.8 | 5 | 2026-11-21 | `9ab8740acc17` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.2, no drafts, thinking off, a build made for another engine | greedy, temperature 0 | 1K code | 512 | 50.9 | 50.5 to 51.0 | 5 | 2026-11-21 | `06d0073eb3e8` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.2, no drafts, thinking off, a build made for another engine | greedy, temperature 0 | 4K code | 512 | 50.9 | 50.9 to 50.9 | 5 | 2026-11-21 | `06d0073eb3e8` | [15](findings/15_glm53_flash_two_builds) |
| max | oMLX 0.8.1 with its kernels, MTP off, reply is reasoning text | greedy, temperature 0 | 4K code | 512 | 49.3 | 49.3 to 49.4 | 5 | 2026-11-21 | `9ab8740acc17` | [15](findings/15_glm53_flash_two_builds) |
| copy task | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | greedy, temperature 0 | 1K code | 512 | 157.1 | 108.4 to 160.6 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 1K code | 512 | 156.8 | 94.3 to 160.8 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| copy task | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 1K code | 512 | 155.9 | 124.3 to 161.1 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | greedy, temperature 0 | 4K code | 512 | 153.3 | 118.1 to 158.2 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 4K code | 512 | 148.8 | 98.6 to 157.5 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 4K code | 512 | 146.5 | 105.9 to 157.6 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| counting toy | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 4K code | 512 | 96.7 | 86.8 to 97.9 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 4K code | 512 | 96.3 | 86.7 to 99.5 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| counting toy | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 1K code | 512 | 95.2 | 83.1 to 96.5 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| counting toy | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | greedy, temperature 0 | 4K code | 512 | 94.9 | 85.9 to 101.5 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | greedy, temperature 0 | 1K code | 512 | 94.4 | 87.7 to 95.9 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | greedy, temperature 0 | 1K code | 512 | 91.3 | 81.5 to 97.6 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| median | oMLX 0.8.2 with its kernels, MTP on, default depth, reply is reasoning text, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 70.9 | 64.9 to 73.7 | 5 | 2026-11-21 | `34ae658e42ba` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.3 with its kernels, MTP on, default depth, reply is reasoning text | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 70.1 | 69.6 to 73.4 | 5 | 2026-11-23 | `42c428b2af1f` | [26](findings/26_omlx_083_refresh) |
| median | oMLX 0.8.1 with its kernels, MTP on, default depth, reply is reasoning text, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 69.7 | 66.9 to 73.3 | 5 | 2026-11-21 | `421e19a82f36` | [15](findings/15_glm53_flash_two_builds) |
| median | oMLX 0.7.3 with its kernels, MTP on, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 68.8 | 61.0 to 76.1 | 5 | 2026-11-17 | `8453ec3a372d` | [2](findings/02_ten_models_4k_to_1m) |
| median | oMLX 0.8.0 with its kernels, MTP on, default depth, reply is reasoning text, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 67.8 | 63.2 to 72.2 | 5 | 2026-11-21 | `8f12a00bcc4f` | [9](findings/09_omlx_080_four_models) |
| median | TensorFold 1.3.2, MTP drafts, thinking off, a build made for another engine, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 67.5 | 64.3 to 70.0 | 5 | 2026-11-21 | `787aea383796` | [15](findings/15_glm53_flash_two_builds) |
| median | TensorFold 1.3.4, MTP drafts, thinking off, a build made for another engine | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 65.9 | 63.2 to 66.3 | 5 | 2026-11-23 | `785a47562751` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.3, MTP drafts, thinking off, a build made for another engine, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 64.9 | 64.2 to 69.7 | 5 | 2026-11-22 | `0d05d0d3d24c` | [19](findings/19_tensorfold_133_refresh) |

</details>

<details>
<summary><b>Inkling 2 Small</b>, 7 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.2 with its kernels, DSpark draft on, default depth, reply is mostly reasoning text | greedy, temperature 0 | 1K code | 2,048 | 52.7 | 48.8 to 53.5 | 5 | 2026-11-21 | `fd37c30fd993` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.0 with its kernels, DSpark draft on, default depth, reply is mostly reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 51.6 | 46.9 to 51.9 | 5 | 2026-11-21 | `818c28dbb625` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.0 with its kernels, DSpark draft on, default depth, reply is mostly reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 48.6 | 46.0 to 58.7 | 5 | 2026-11-21 | `818c28dbb625` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.2 with its kernels, DSpark draft on, default depth, reply is mostly reasoning text | greedy, temperature 0 | 4K code | 2,048 | 47.6 | 43.6 to 53.2 | 5 | 2026-11-21 | `fd37c30fd993` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.0 with its kernels, DSpark draft on, default depth, reply is mostly reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 42.2 | 39.7 to 46.0 | 5 | 2026-11-21 | `818c28dbb625` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.8.2 with its kernels, DSpark draft on, default depth, reply is mostly reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 41.3 | 39.0 to 42.4 | 5 | 2026-11-21 | `fd37c30fd993` | [16](findings/16_omlx_082_refresh) |
| median | oMLX main 624cff0e with its kernels, DSpark draft on, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 41.3 | 38.5 to 42.9 | 5 | 2026-11-17 | `5c4d781c0e3d` | [2](findings/02_ten_models_4k_to_1m) |

</details>

<details>
<summary><b>Qwen3.8 27B, 4-bit</b>, 30 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.0, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 1K code | 2,048 | 331.3 | 245.7 to 342.1 | 5 | 2026-11-20 | `f2d856e22771` | [7](findings/07_qwen38_tensorfold_130) |
| max | TensorFold 1.3.2, DFlash2 drafter (z-lab), defaults, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 328.9 | 301.3 to 349.7 | 5 | 2026-11-21 | `ab1caacd2961` | [11](findings/11_qwen38_tensorfold_132) |
| max | TensorFold 1.3.4, DFlash2 drafter (z-lab), defaults, standard-block start | greedy, temperature 0 | 1K code | 2,048 | 323.4 | 264.2 to 347.6 | 5 | 2026-11-23 | `52b0c20da4cb` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 1K code | 2,048 | 315.3 | 286.3 to 366.3 | 5 | 2026-11-22 | `6a8e3b10559e` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.3, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 1K code | 512 | 264.7 | 225.1 to 300.3 | 5 | 2026-11-22 | `6a8e3b10559e` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.0, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 4K code | 2,048 | 250.8 | 217.1 to 332.2 | 5 | 2026-11-20 | `f2d856e22771` | [7](findings/07_qwen38_tensorfold_130) |
| max | TensorFold 1.3.3, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 4K code | 2,048 | 247.7 | 203.6 to 302.4 | 5 | 2026-11-22 | `6a8e3b10559e` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.4, DFlash2 drafter (z-lab), defaults, standard-block start | greedy, temperature 0 | 4K code | 2,048 | 246.9 | 212.7 to 299.7 | 5 | 2026-11-23 | `52b0c20da4cb` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.2, DFlash2 drafter (z-lab), defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 243.6 | 225.6 to 274.1 | 5 | 2026-11-21 | `ab1caacd2961` | [11](findings/11_qwen38_tensorfold_132) |
| max | TensorFold 1.3.2, DFlash2 drafter (z-lab), defaults, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 241.6 | 223.4 to 298.6 | 5 | 2026-11-21 | `ab1caacd2961` | [11](findings/11_qwen38_tensorfold_132) |
| max | TensorFold 1.3.4, DFlash2 drafter (z-lab), defaults, same-night start | greedy, temperature 0 | 1K code | 512 | 230.1 | 209.2 to 271.7 | 5 | 2026-11-23 | `2813d10958a6` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.0, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 1K code | 512 | 227.0 | 222.2 to 278.6 | 5 | 2026-11-20 | `f2d856e22771` | [7](findings/07_qwen38_tensorfold_130) |
| max | mlx-lm 0.32.2, defaults, the baseline, 20 Nov run | greedy, temperature 0 | 1K code | 2,048 | 45.1 | 45.0 to 45.2 | 5 | 2026-11-20 | `0c5446c7acc1` | [7](findings/07_qwen38_tensorfold_130) |
| copy task | TensorFold 1.3.0, DFlash2 drafter (z-lab), defaults, long copy block, older release | greedy, temperature 0 | 4K code | 2,048 | 824.0 | 734.9 to 832.0 | 5 | 2026-11-20 | `44a8ff4a173a` | [7](findings/07_qwen38_tensorfold_130) |
| copy task | TensorFold 1.3.4, DFlash2 drafter (z-lab), defaults | greedy, temperature 0 | 4K code | 2,048 | 818.8 | 713.0 to 834.3 | 5 | 2026-11-23 | `9466f37f6182` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.2, DFlash2 drafter (z-lab), defaults, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 814.3 | 705.9 to 825.8 | 5 | 2026-11-21 | `ab1caacd2961` | [11](findings/11_qwen38_tensorfold_132) |
| copy task | TensorFold 1.3.3, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 4K code | 2,048 | 810.8 | 702.0 to 839.0 | 5 | 2026-11-22 | `6a8e3b10559e` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.0, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 1K code | 512 | 450.8 | 169.0 to 454.8 | 5 | 2026-11-20 | `f2d856e22771` | [7](findings/07_qwen38_tensorfold_130) |
| counting toy | TensorFold 1.3.4, DFlash2 drafter (z-lab), defaults | greedy, temperature 0 | 1K code | 512 | 450.6 | 328.3 to 466.4 | 5 | 2026-11-23 | `9466f37f6182` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.3, DFlash2 drafter (z-lab), defaults, older release | greedy, temperature 0 | 1K code | 512 | 449.7 | 146.9 to 453.7 | 5 | 2026-11-22 | `6a8e3b10559e` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.2, DFlash2 drafter (z-lab), defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 448.9 | 163.8 to 453.2 | 5 | 2026-11-21 | `ab1caacd2961` | [11](findings/11_qwen38_tensorfold_132) |
| median | TensorFold 1.3.3, DFlash2 drafter (z-lab), defaults, sixth start, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 164.1 | 133.1 to 184.0 | 5 | 2026-11-22 | `e2420150405f` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, DFlash2 drafter (z-lab), defaults, second start, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 161.3 | 142.5 to 178.4 | 5 | 2026-11-21 | `ab1caacd2961` | [11](findings/11_qwen38_tensorfold_132) |
| median | TensorFold 1.2.8, DFlash2 drafter (z-lab), older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 154.2 | 136.9 to 219.4 | 5 | 2026-11-17 | `a798cea8b67e` | [2](findings/02_ten_models_4k_to_1m) |
| median | TensorFold 1.3.4, DFlash2 drafter (z-lab), defaults, standard-block start | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 149.6 | 133.3 to 161.7 | 5 | 2026-11-23 | `52b0c20da4cb` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.0, DFlash2 drafter (z-lab), defaults, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 148.2 | 128.2 to 178.6 | 5 | 2026-11-20 | `f2d856e22771` | [7](findings/07_qwen38_tensorfold_130) |
| median | TensorFold 1.2.7, DFlash2 drafter (z-lab), older release | temperature 0.7, top-p 0.8, top-k 20 | 1K mixed | 512 | 145.7 | 138.4 to 182.9 | 5 | 2026-11-13 | `f6775745e273` | [1](findings/01_tensorfold_qwen38-27b_4bit) |
| median | TensorFold 1.2.7, no draft model, older release | temperature 0.7, top-p 0.8, top-k 20 | 1K mixed | 512 | 48.7 | 48.6 to 48.7 | 5 | 2026-11-13 | `eabffb505d52` | [1](findings/01_tensorfold_qwen38-27b_4bit) |
| median | mlx-lm 0.32.2, defaults, the baseline | temperature 0.7, top-p 0.8, top-k 20 | 1K mixed | 512 | 44.5 | 44.4 to 44.5 | 5 | 2026-11-13 | `3ad3a150c4d0` | [1](findings/01_tensorfold_qwen38-27b_4bit) |
| median | mlx-lm 0.32.2, defaults, the baseline, 20 Nov run | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 43.6 | 43.6 to 43.7 | 5 | 2026-11-20 | `0c5446c7acc1` | [7](findings/07_qwen38_tensorfold_130) |

</details>

<details>
<summary><b>Qwen3.8 27B, full</b>, 4 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | mlx-serve 26.11.3, warmup-full, defaults (lossy decode copies engaged, by the log), prompt lookup drafts on | greedy, temperature 0 | 4K code | 512 | 6.9 | 6.5 to 7.4 | 5 | 2026-11-20 | `8594b4fe926a` | [8](findings/08_dsv41_mlxserve_26113) |
| median | mlx-serve 26.11.2, defaults, prompt lookup drafts on, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 8.8 | 8.3 to 9.8 | 5 | 2026-11-17 | `a30a665ca3ee` | [2](findings/02_ten_models_4k_to_1m) |
| median | mlx-serve 26.11.3, defaults without --warmup-full (lossy decode copies engaged, by the log), prompt lookup drafts on | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 7.1 | 6.6 to 7.6 | 5 | 2026-11-21 | `5619fdacb103` | [8](findings/08_dsv41_mlxserve_26113) |
| median | mlx-serve 26.11.3, warmup-full, defaults (lossy decode copies engaged, by the log), prompt lookup drafts on | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 6.8 | 6.8 to 6.9 | 5 | 2026-11-20 | `8594b4fe926a` | [8](findings/08_dsv41_mlxserve_26113) |

</details>

<details>
<summary><b>Qwen3.8 Flash Next, 4-bit</b>, 27 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.4, MTP on, recipe line, defaults, same-night start | greedy, temperature 0 | 1K code | 2,048 | 211.5 | 199.0 to 266.0 | 5 | 2026-11-23 | `51182015de42` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 4K code | 2,048 | 209.5 | 174.4 to 229.6 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 2,048 | 206.8 | 192.0 to 263.1 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 206.8 | 191.7 to 257.5 | 5 | 2026-11-21 | `70284626631f` | [11](findings/11_qwen38_tensorfold_132) |
| max | TensorFold 1.3.4, MTP on, recipe line, defaults, same-night start | greedy, temperature 0 | 4K code | 2,048 | 205.1 | 176.4 to 232.5 | 5 | 2026-11-23 | `51182015de42` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 2,048 | 204.4 | 176.6 to 247.5 | 5 | 2026-11-20 | `7bf80be3a997` | [7](findings/07_qwen38_tensorfold_130) |
| max | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 4K code | 512 | 194.4 | 169.7 to 217.0 | 5 | 2026-11-20 | `7bf80be3a997` | [7](findings/07_qwen38_tensorfold_130) |
| max | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 4K code | 512 | 188.9 | 172.9 to 200.7 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.4, MTP on, recipe line, defaults, same-night start | greedy, temperature 0 | 4K code | 512 | 185.4 | 167.8 to 205.9 | 5 | 2026-11-23 | `51182015de42` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 4K code | 512 | 179.1 | 176.1 to 183.6 | 5 | 2026-11-21 | `70284626631f` | [11](findings/11_qwen38_tensorfold_132) |
| copy task | TensorFold 1.3.4, MTP on, recipe line, defaults, counting-check start | greedy, temperature 0 | 1K code | 512 | 360.3 | 270.0 to 380.1 | 5 | 2026-11-23 | `dd4ddf3cf8cd` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 351.6 | 262.9 to 371.7 | 5 | 2026-11-21 | `70284626631f` | [11](findings/11_qwen38_tensorfold_132) |
| copy task | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 322.3 | 263.3 to 355.7 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.4, MTP on, recipe line, defaults | greedy, temperature 0 | 4K code | 2,048 | 320.8 | 290.2 to 352.3 | 5 | 2026-11-23 | `8d40d469c26c` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 312.3 | 277.4 to 344.1 | 5 | 2026-11-21 | `70284626631f` | [11](findings/11_qwen38_tensorfold_132) |
| copy task | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 4K code | 2,048 | 312.1 | 280.8 to 344.7 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 298.1 | 247.3 to 330.5 | 5 | 2026-11-20 | `7bf80be3a997` | [7](findings/07_qwen38_tensorfold_130) |
| copy task | TensorFold 1.3.0, MTP on, recipe line, defaults, long copy block, older release | greedy, temperature 0 | 4K code | 2,048 | 292.2 | 261.8 to 320.0 | 5 | 2026-11-20 | `37a4c93bd874` | [7](findings/07_qwen38_tensorfold_130) |
| counting toy | TensorFold 1.3.4, MTP on, recipe line, defaults, counting-check start | greedy, temperature 0 | 1K code | 512 | 377.8 | 367.2 to 377.9 | 5 | 2026-11-23 | `dd4ddf3cf8cd` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 369.5 | 360.5 to 370.2 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 369.3 | 359.4 to 370.0 | 5 | 2026-11-21 | `70284626631f` | [11](findings/11_qwen38_tensorfold_132) |
| counting toy | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 344.7 | 336.2 to 344.9 | 5 | 2026-11-20 | `7bf80be3a997` | [7](findings/07_qwen38_tensorfold_130) |
| median | TensorFold 1.3.3, MTP on, recipe line, defaults, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 130.9 | 120.7 to 135.4 | 5 | 2026-11-22 | `58be1ddd40c3` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 129.7 | 123.5 to 134.1 | 5 | 2026-11-21 | `70284626631f` | [11](findings/11_qwen38_tensorfold_132) |
| median | TensorFold 1.2.8, MTP on, recipe line, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 129.2 | 123.9 to 139.2 | 5 | 2026-11-17 | `72fae37b87f0` | [2](findings/02_ten_models_4k_to_1m) |
| median | TensorFold 1.3.4, MTP on, recipe line, defaults, same-night start | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 128.4 | 122.7 to 134.1 | 5 | 2026-11-23 | `51182015de42` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 126.7 | 115.9 to 131.9 | 5 | 2026-11-20 | `7bf80be3a997` | [7](findings/07_qwen38_tensorfold_130) |

</details>

<details>
<summary><b>Qwen3.8 Flash Next, 6-bit</b>, 20 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.3, MTP on, recipe line, defaults | greedy, temperature 0 | 1K code | 2,048 | 201.3 | 182.7 to 208.6 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 200.1 | 188.9 to 219.8 | 5 | 2026-11-21 | `51735d12713b` | [11](findings/11_qwen38_tensorfold_132) |
| max | TensorFold 1.3.3, MTP on, recipe line, defaults | greedy, temperature 0 | 4K code | 2,048 | 197.3 | 176.7 to 217.8 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 195.1 | 186.9 to 201.4 | 5 | 2026-11-21 | `51735d12713b` | [11](findings/11_qwen38_tensorfold_132) |
| max | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 2,048 | 193.0 | 178.5 to 212.3 | 5 | 2026-11-21 | `2bc45b1272e8` | [7](findings/07_qwen38_tensorfold_130) |
| max | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 188.2 | 177.9 to 192.6 | 5 | 2026-11-21 | `2bc45b1272e8` | [7](findings/07_qwen38_tensorfold_130) |
| max | TensorFold 1.3.3, MTP on, recipe line, defaults | greedy, temperature 0 | 1K code | 512 | 181.5 | 158.7 to 192.5 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.3, MTP on, recipe line, defaults | greedy, temperature 0 | 1K code | 512 | 260.1 | 213.0 to 283.0 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 260.0 | 213.3 to 283.3 | 5 | 2026-11-21 | `51735d12713b` | [11](findings/11_qwen38_tensorfold_132) |
| copy task | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 254.4 | 208.5 to 276.9 | 5 | 2026-11-21 | `2bc45b1272e8` | [7](findings/07_qwen38_tensorfold_130) |
| copy task | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 253.6 | 233.1 to 276.6 | 5 | 2026-11-21 | `51735d12713b` | [11](findings/11_qwen38_tensorfold_132) |
| copy task | TensorFold 1.3.3, MTP on, recipe line, defaults | greedy, temperature 0 | 4K code | 2,048 | 252.5 | 233.0 to 275.1 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 4K code | 2,048 | 247.7 | 223.1 to 268.9 | 5 | 2026-11-21 | `2bc45b1272e8` | [7](findings/07_qwen38_tensorfold_130) |
| counting toy | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | greedy, temperature 0 | 1K code | 512 | 296.4 | 290.2 to 297.1 | 5 | 2026-11-21 | `51735d12713b` | [11](findings/11_qwen38_tensorfold_132) |
| counting toy | TensorFold 1.3.3, MTP on, recipe line, defaults | greedy, temperature 0 | 1K code | 512 | 296.2 | 290.2 to 297.4 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | greedy, temperature 0 | 1K code | 512 | 290.0 | 283.9 to 290.3 | 5 | 2026-11-21 | `2bc45b1272e8` | [7](findings/07_qwen38_tensorfold_130) |
| median | TensorFold 1.3.0, MTP on, recipe line, defaults, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 117.4 | 112.0 to 122.0 | 5 | 2026-11-21 | `2bc45b1272e8` | [7](findings/07_qwen38_tensorfold_130) |
| median | TensorFold 1.3.3, MTP on, recipe line, defaults | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 114.5 | 112.7 to 127.1 | 5 | 2026-11-22 | `e4b66d27e9cb` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, MTP on, recipe line, defaults, second start, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 114.1 | 110.6 to 121.5 | 5 | 2026-11-21 | `51735d12713b` | [11](findings/11_qwen38_tensorfold_132) |
| median | TensorFold 1.2.8, MTP on, recipe line, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 114.0 | 108.6 to 125.6 | 5 | 2026-11-17 | `ea26b8919e88` | [2](findings/02_ten_models_4k_to_1m) |

</details>

<details>
<summary><b>Qwen3.8 Flash Next, full</b>, 31 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.3 with its kernels, MTP on (built-in head), fixed depth 4 | greedy, temperature 0 | 1K code | 2,048 | 54.5 | 49.2 to 56.6 | 5 | 2026-11-23 | `780bb9bba309` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.2 with its kernels, MTP on (built-in head), fixed depth 4, older release | greedy, temperature 0 | 1K code | 2,048 | 54.3 | 50.2 to 55.4 | 5 | 2026-11-21 | `8f063cd2f425` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.0 with its kernels, MTP on (built-in head), fixed depth 4, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 54.2 | 47.0 to 60.7 | 5 | 2026-11-21 | `5f6db4faf823` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.2 with its kernels, MTP on (built-in head), fixed depth 4, older release | greedy, temperature 0 | 4K code | 2,048 | 53.6 | 49.2 to 59.2 | 5 | 2026-11-21 | `8f063cd2f425` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.0 with its kernels, MTP on (built-in head), fixed depth 4, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 53.6 | 47.6 to 55.3 | 5 | 2026-11-21 | `5f6db4faf823` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.3 with its kernels, MTP on (built-in head), fixed depth 4 | greedy, temperature 0 | 4K code | 2,048 | 51.1 | 49.1 to 54.2 | 5 | 2026-11-23 | `780bb9bba309` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 1K code | 2,048 | 50.8 | 46.2 to 52.5 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 49.4 | 46.9 to 52.6 | 5 | 2026-11-21 | `57b0f4425846` | [9](findings/09_omlx_080_four_models) |
| max | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | greedy, temperature 0 | 4K code | 2,048 | 49.1 | 44.1 to 53.5 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 4K code | 2,048 | 49.1 | 44.9 to 53.6 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | greedy, temperature 0 | 1K code | 2,048 | 49.0 | 45.5 to 51.3 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 48.5 | 45.3 to 51.4 | 5 | 2026-11-21 | `57b0f4425846` | [9](findings/09_omlx_080_four_models) |
| copy task | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 1K code | 512 | 128.7 | 119.0 to 132.0 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| copy task | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | greedy, temperature 0 | 1K code | 512 | 128.4 | 120.5 to 132.3 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| copy task | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 1K code | 512 | 120.1 | 115.1 to 132.3 | 5 | 2026-11-21 | `6542a7f95175` | [9](findings/09_omlx_080_four_models) |
| copy task | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 4K code | 512 | 119.5 | 105.2 to 126.7 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| copy task | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | greedy, temperature 0 | 4K code | 512 | 118.6 | 105.2 to 127.9 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| copy task | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 4K code | 512 | 116.9 | 98.2 to 125.2 | 5 | 2026-11-21 | `6542a7f95175` | [9](findings/09_omlx_080_four_models) |
| counting toy | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 4K code | 512 | 51.5 | 51.1 to 52.6 | 5 | 2026-11-21 | `6542a7f95175` | [9](findings/09_omlx_080_four_models) |
| counting toy | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | greedy, temperature 0 | 4K code | 512 | 51.5 | 50.7 to 52.4 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| counting toy | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 4K code | 512 | 51.4 | 50.1 to 52.2 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| counting toy | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 1K code | 512 | 50.2 | 48.9 to 51.4 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| counting toy | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | greedy, temperature 0 | 1K code | 512 | 49.9 | 48.9 to 50.6 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| counting toy | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, older release | greedy, temperature 0 | 1K code | 512 | 49.5 | 47.6 to 51.8 | 5 | 2026-11-21 | `6542a7f95175` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.7.3 with its kernels, MTP on (built-in head), older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 34.9 | 32.2 to 35.9 | 5 | 2026-11-17 | `c4bbe7d3230c` | [2](findings/02_ten_models_4k_to_1m) |
| median | oMLX 0.8.2 with its kernels, MTP on (built-in head), default depth, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 34.6 | 31.6 to 35.1 | 5 | 2026-11-21 | `fbc94b62491c` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.3 with its kernels, MTP on (built-in head), default depth | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 34.4 | 34.1 to 36.1 | 5 | 2026-11-23 | `e741a35f57d5` | [26](findings/26_omlx_083_refresh) |
| median | oMLX 0.8.0 with its kernels, MTP on (built-in head), fixed depth 4, second start, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 33.6 | 31.8 to 40.2 | 5 | 2026-11-21 | `5f6db4faf823` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.8.2 with its kernels, MTP on (built-in head), fixed depth 4, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 33.3 | 31.9 to 33.9 | 5 | 2026-11-21 | `8f063cd2f425` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.0 with its kernels, MTP on (built-in head), default depth, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 33.2 | 31.5 to 34.6 | 5 | 2026-11-21 | `6542a7f95175` | [9](findings/09_omlx_080_four_models) |
| median | oMLX 0.8.3 with its kernels, MTP on (built-in head), fixed depth 4 | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 32.4 | 30.2 to 35.0 | 5 | 2026-11-23 | `780bb9bba309` | [26](findings/26_omlx_083_refresh) |

</details>

<details>
<summary><b>DeepSeek V4.1 Flash 1017, oQ4e-mtp</b>, 14 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 4K code | 2,048 | 86.2 | 73.8 to 86.8 | 5 | 2026-11-20 | `c15a39cf630a` | [5](findings/05_dsv41_omlx_080_max_push) |
| max | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 1K code | 2,048 | 84.4 | 78.2 to 85.5 | 5 | 2026-11-20 | `c15a39cf630a` | [5](findings/05_dsv41_omlx_080_max_push) |
| max | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 1K code | 2,048 | 77.2 | 72.5 to 78.7 | 5 | 2026-11-20 | `7ece67645192` | [5](findings/05_dsv41_omlx_080_max_push) |
| max | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 1K code | 512 | 71.2 | 65.7 to 73.1 | 5 | 2026-11-20 | `800dd0f8839c` | [3](findings/03_dsv41_omlx_080) |
| max | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 1K code | 128 | 58.2 | 52.4 to 60.1 | 5 | 2026-11-20 | `800dd0f8839c` | [3](findings/03_dsv41_omlx_080) |
| copy task | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 4K code | 512 | 118.3 | 110.7 to 121.0 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](findings/05_dsv41_omlx_080_max_push) |
| copy task | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 1K code | 512 | 114.7 | 113.6 to 118.1 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](findings/05_dsv41_omlx_080_max_push) |
| copy task | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 4K code | 512 | 98.3 | 93.3 to 99.9 | 5 | 2026-11-20 | `526b05fc2a44` | [5](findings/05_dsv41_omlx_080_max_push) |
| counting toy | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 4K code | 512 | 114.0 | 113.7 to 114.3 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](findings/05_dsv41_omlx_080_max_push) |
| counting toy | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | greedy, temperature 0 | 1K code | 512 | 113.0 | 111.9 to 114.0 | 5 | 2026-11-20 | `b1703d1d52b6` | [5](findings/05_dsv41_omlx_080_max_push) |
| counting toy | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | greedy, temperature 0 | 4K code | 512 | 90.6 | 90.4 to 90.8 | 5 | 2026-11-20 | `526b05fc2a44` | [5](findings/05_dsv41_omlx_080_max_push) |
| median | oMLX 0.8.0 with its kernels, MTP drafts on, default depth, second start | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 57.9 | 53.3 to 59.8 | 5 | 2026-11-20 | `cfff183a181f` | [5](findings/05_dsv41_omlx_080_max_push) |
| median | oMLX 0.8.0 with its kernels, MTP drafts on, default depth | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 56.5 | 55.1 to 58.5 | 5 | 2026-11-20 | `800dd0f8839c` | [3](findings/03_dsv41_omlx_080) |
| median | oMLX 0.8.0 with its kernels, MTP drafts on, fixed depth 5 | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 50.5 | 48.1 to 57.3 | 5 | 2026-11-20 | `c15a39cf630a` | [5](findings/05_dsv41_omlx_080_max_push) |

</details>

<details>
<summary><b>DeepSeek V4.1 Flash 1017, maker's files</b>, 26 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 4K code | 2,048 | 108.0 | 93.6 to 110.4 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| max | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 4K code | 2,048 | 105.7 | 93.7 to 108.4 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 1K code | 512 | 101.0 | 81.9 to 102.9 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| max | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 1K code | 2,048 | 100.4 | 99.5 to 101.3 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| max | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 1K code | 2,048 | 100.2 | 95.0 to 105.4 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 1K code | 512 | 99.6 | 86.1 to 114.5 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 4K code | 2,048 | 75.2 | 67.7 to 79.4 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| max | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 1K code | 2,048 | 74.4 | 67.6 to 82.5 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| max | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 1K code | 512 | 71.0 | 59.2 to 78.5 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| max | TensorFold 1.3.0, drafts at defaults (DSpark and copies) | greedy, temperature 0 | 1K code | 128 | 62.6 | 56.7 to 66.0 | 5 | 2026-11-20 | `778e5c808b88` | [4](findings/04_dsv41_tensorfold_130) |
| copy task | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 1K code | 512 | 186.9 | 180.5 to 191.0 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| copy task | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 1K code | 512 | 185.1 | 177.2 to 190.8 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 4K code | 512 | 179.9 | 173.0 to 188.3 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| copy task | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 4K code | 512 | 179.7 | 174.2 to 188.0 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 1K code | 512 | 159.1 | 138.5 to 161.4 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| copy task | TensorFold 1.3.0, drafts at defaults (DSpark and copies), long copy block | greedy, temperature 0 | 4K code | 2,048 | 148.8 | 143.1 to 150.4 | 5 | 2026-11-20 | `dd80ad7aa9fa` | [6](findings/06_dsv41_tensorfold_130_max_push) |
| copy task | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 4K code | 512 | 145.9 | 124.1 to 149.2 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| counting toy | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 1K code | 512 | 138.3 | 136.0 to 141.4 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | greedy, temperature 0 | 4K code | 512 | 138.2 | 137.0 to 138.4 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 1K code | 512 | 138.1 | 135.3 to 139.3 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| counting toy | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | greedy, temperature 0 | 4K code | 512 | 137.7 | 136.7 to 138.0 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| counting toy | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 1K code | 512 | 110.0 | 100.2 to 110.7 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| counting toy | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | greedy, temperature 0 | 4K code | 512 | 109.5 | 100.4 to 112.3 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |
| median | TensorFold 1.3.3, drafts at defaults (DSpark and copies), second start, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 74.5 | 71.2 to 75.6 | 5 | 2026-11-22 | `d690d6b1059b` | [18](findings/18_dsv41_tensorfold_133) |
| median | TensorFold 1.3.4, drafts at defaults (DSpark and copies), second start | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 69.9 | 68.6 to 76.2 | 5 | 2026-11-23 | `33d0baeed473` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.0, drafts at defaults (DSpark and copies), older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 45.7 | 44.1 to 47.2 | 5 | 2026-11-22 | `5b618f8c8234` | [18](findings/18_dsv41_tensorfold_133) |

</details>

<details>
<summary><b>GLM-5.3 Flash, 4-bit</b>, 34 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.4, DFlash2 draft model (incoai), thinking off | greedy, temperature 0 | 1K code | 2,048 | 104.7 | 100.5 to 111.8 | 5 | 2026-11-23 | `2820399df996` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.4, DFlash2 draft model (incoai), thinking off | greedy, temperature 0 | 4K code | 2,048 | 104.2 | 101.8 to 112.3 | 5 | 2026-11-23 | `2820399df996` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, MTP drafts, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 102.8 | 97.3 to 107.2 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.4, MTP drafts, thinking off | greedy, temperature 0 | 1K code | 2,048 | 102.5 | 97.9 to 104.8 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, MTP drafts, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 102.1 | 97.7 to 105.0 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP drafts, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 102.0 | 95.2 to 108.5 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.3, DFlash2 draft model (incoai), thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 101.6 | 97.8 to 107.8 | 5 | 2026-11-22 | `1e3c46e52f5f` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, MTP drafts, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 101.4 | 99.6 to 104.4 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.3, DFlash2 draft model (incoai), thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 101.4 | 100.6 to 108.7 | 5 | 2026-11-22 | `1e3c46e52f5f` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.4, MTP drafts, thinking off | greedy, temperature 0 | 4K code | 2,048 | 99.5 | 94.7 to 105.7 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| max | oMLX 0.8.1 with its kernels, MTP on, default depth, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 85.1 | 79.6 to 87.0 | 5 | 2026-11-21 | `4f9da10c3691` | [15](findings/15_glm53_flash_two_builds) |
| max | oMLX 0.8.1 with its kernels, MTP on, default depth, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 82.3 | 79.4 to 99.7 | 5 | 2026-11-21 | `4f9da10c3691` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.2, no drafts, thinking off | greedy, temperature 0 | 1K code | 512 | 73.4 | 72.4 to 73.6 | 5 | 2026-11-21 | `3b571bd4b948` | [15](findings/15_glm53_flash_two_builds) |
| max | TensorFold 1.3.2, no drafts, thinking off | greedy, temperature 0 | 4K code | 512 | 73.1 | 73.0 to 73.2 | 5 | 2026-11-21 | `3b571bd4b948` | [15](findings/15_glm53_flash_two_builds) |
| max | oMLX 0.8.1 with its kernels, MTP off, reply is reasoning text | greedy, temperature 0 | 1K code | 512 | 72.5 | 71.3 to 72.7 | 5 | 2026-11-21 | `5727fcf18ffb` | [15](findings/15_glm53_flash_two_builds) |
| max | oMLX 0.8.1 with its kernels, MTP off, reply is reasoning text | greedy, temperature 0 | 4K code | 512 | 68.9 | 68.8 to 69.0 | 5 | 2026-11-21 | `5727fcf18ffb` | [15](findings/15_glm53_flash_two_builds) |
| copy task | TensorFold 1.3.2, MTP drafts, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 175.0 | 118.0 to 183.3 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| copy task | TensorFold 1.3.4, MTP drafts, thinking off | greedy, temperature 0 | 1K code | 512 | 174.8 | 122.0 to 180.6 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.2, MTP drafts, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 174.5 | 107.2 to 177.2 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| copy task | TensorFold 1.3.3, MTP drafts, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 174.5 | 146.8 to 176.4 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| copy task | TensorFold 1.3.4, MTP drafts, thinking off | greedy, temperature 0 | 4K code | 512 | 172.5 | 132.3 to 175.3 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| copy task | TensorFold 1.3.3, MTP drafts, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 153.5 | 106.5 to 180.1 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.4, MTP drafts, thinking off | greedy, temperature 0 | 4K code | 512 | 114.7 | 101.7 to 117.1 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.3, MTP drafts, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 113.6 | 102.5 to 121.9 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| counting toy | TensorFold 1.3.2, MTP drafts, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 111.1 | 105.5 to 116.1 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| counting toy | TensorFold 1.3.4, MTP drafts, thinking off | greedy, temperature 0 | 1K code | 512 | 106.8 | 96.9 to 110.2 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| counting toy | TensorFold 1.3.2, MTP drafts, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 105.6 | 98.0 to 107.6 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| counting toy | TensorFold 1.3.3, MTP drafts, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 102.3 | 99.4 to 111.0 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.4, DFlash2 draft model (incoai), thinking off | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 85.9 | 83.9 to 86.2 | 5 | 2026-11-23 | `2820399df996` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.3, DFlash2 draft model (incoai), thinking off, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 84.2 | 83.6 to 85.4 | 5 | 2026-11-22 | `1e3c46e52f5f` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, MTP drafts, thinking off, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 80.9 | 79.2 to 85.4 | 5 | 2026-11-21 | `33ba6147e087` | [15](findings/15_glm53_flash_two_builds) |
| median | TensorFold 1.3.3, MTP drafts, thinking off, older release | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 79.8 | 72.6 to 89.0 | 5 | 2026-11-22 | `3a880091476a` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.4, MTP drafts, thinking off | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 78.5 | 70.8 to 86.4 | 5 | 2026-11-23 | `5d827a9f83a1` | [27](findings/27_tensorfold_134_refresh) |
| median | oMLX 0.8.1 with its kernels, MTP on, default depth, reply is reasoning text | temperature 1.0, top-p 0.95 | 4K mixed | 512 | 76.8 | 68.9 to 78.3 | 5 | 2026-11-21 | `4f9da10c3691` | [15](findings/15_glm53_flash_two_builds) |

</details>

<details>
<summary><b>Hy4-flash, 4-bit</b>, 21 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.4, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 79.0 | 65.5 to 106.5 | 5 | 2026-11-23 | `0263bc06d9cf` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 73.3 | 63.2 to 77.0 | 5 | 2026-11-22 | `95019a9ea00a` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.3, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 72.8 | 67.3 to 82.7 | 5 | 2026-11-22 | `95019a9ea00a` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.4, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 72.1 | 62.4 to 78.8 | 5 | 2026-11-23 | `0263bc06d9cf` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.2, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 71.5 | 67.4 to 85.9 | 5 | 2026-11-21 | `b09695c3eab1` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 70.7 | 61.1 to 77.4 | 5 | 2026-11-21 | `b09695c3eab1` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, DFly2 drafts on, thinking on, reply is reasoning text, third start, older release | greedy, temperature 0 | 1K code | 2,048 | 64.6 | 56.4 to 78.8 | 5 | 2026-11-21 | `5498d94e70db` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.3, DFly2 drafts on, thinking on, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 63.8 | 56.8 to 64.6 | 5 | 2026-11-22 | `9e3d9e5dce53` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.4, DFly2 drafts on, thinking on, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 63.8 | 59.9 to 93.4 | 5 | 2026-11-23 | `3523a0e3371d` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.3, DFly2 drafts on, thinking on, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 61.8 | 57.3 to 73.0 | 5 | 2026-11-22 | `9e3d9e5dce53` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, DFly2 drafts on, thinking on, reply is reasoning text, third start, older release | greedy, temperature 0 | 4K code | 2,048 | 60.4 | 56.9 to 65.9 | 5 | 2026-11-21 | `5498d94e70db` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.4, DFly2 drafts on, thinking on, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 60.2 | 53.5 to 62.4 | 5 | 2026-11-23 | `3523a0e3371d` | [27](findings/27_tensorfold_134_refresh) |
| max | TensorFold 1.3.2, drafts off, thinking on, reply is reasoning text, 512-token replies | greedy, temperature 0 | 1K code | 512 | 43.0 | 41.1 to 43.0 | 5 | 2026-11-21 | `df5b641735e6` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, drafts off, thinking on, reply is reasoning text, 512-token replies | greedy, temperature 0 | 4K code | 512 | 42.2 | 42.1 to 42.4 | 5 | 2026-11-21 | `df5b641735e6` | [10](findings/10_hy4_flash_tensorfold_132) |
| median | TensorFold 1.3.3, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 54.5 | 51.6 to 107.8 | 5 | 2026-11-22 | `95019a9ea00a` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.4, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 51.6 | 46.3 to 57.8 | 5 | 2026-11-23 | `0263bc06d9cf` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.2, DFly2 drafts on, thinking on, reply is reasoning text, third start, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 51.3 | 44.0 to 70.4 | 5 | 2026-11-21 | `5498d94e70db` | [10](findings/10_hy4_flash_tensorfold_132) |
| median | TensorFold 1.3.2, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, second start, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 51.0 | 49.4 to 59.1 | 5 | 2026-11-21 | `b09695c3eab1` | [10](findings/10_hy4_flash_tensorfold_132) |
| median | TensorFold 1.3.4, DFly2 drafts on, thinking on, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 48.0 | 44.0 to 84.0 | 5 | 2026-11-23 | `3523a0e3371d` | [27](findings/27_tensorfold_134_refresh) |
| median | TensorFold 1.3.3, DFly2 drafts on, thinking on, reply is reasoning text, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 44.2 | 43.3 to 71.6 | 5 | 2026-11-22 | `9e3d9e5dce53` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, drafts off, thinking on, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 41.3 | 41.1 to 41.4 | 5 | 2026-11-21 | `df5b641735e6` | [10](findings/10_hy4_flash_tensorfold_132) |

</details>

<details>
<summary><b>Hy4-flash, 8-bit</b>, 15 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | TensorFold 1.3.3, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 55.2 | 51.6 to 60.6 | 5 | 2026-11-22 | `bfcced24637c` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.3, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 53.8 | 50.4 to 56.5 | 5 | 2026-11-22 | `bfcced24637c` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 53.4 | 51.7 to 57.7 | 5 | 2026-11-21 | `f3e0bbdd9f33` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 52.0 | 48.1 to 55.3 | 5 | 2026-11-21 | `f3e0bbdd9f33` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, DFly2 drafts on, thinking on, reply is reasoning text, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 47.6 | 44.1 to 50.5 | 5 | 2026-11-21 | `a9fe24e89f10` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, DFly2 drafts on, thinking on, reply is reasoning text, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 46.8 | 41.8 to 51.3 | 5 | 2026-11-21 | `a9fe24e89f10` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.3, DFly2 drafts on, thinking on, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 46.7 | 46.3 to 51.9 | 5 | 2026-11-22 | `998afef57c31` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.3, DFly2 drafts on, thinking on, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 46.2 | 43.4 to 47.7 | 5 | 2026-11-22 | `998afef57c31` | [19](findings/19_tensorfold_133_refresh) |
| max | TensorFold 1.3.2, drafts off, thinking on, reply is reasoning text, 512-token replies | greedy, temperature 0 | 1K code | 512 | 34.4 | 33.2 to 34.6 | 5 | 2026-11-21 | `b8e543b952e1` | [10](findings/10_hy4_flash_tensorfold_132) |
| max | TensorFold 1.3.2, drafts off, thinking on, reply is reasoning text, 512-token replies | greedy, temperature 0 | 4K code | 512 | 34.0 | 33.9 to 34.2 | 5 | 2026-11-21 | `b8e543b952e1` | [10](findings/10_hy4_flash_tensorfold_132) |
| median | TensorFold 1.3.3, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 44.8 | 39.2 to 49.4 | 5 | 2026-11-22 | `bfcced24637c` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, DFly2 drafts on, TF_HY4_DRAFT_BITS=8 (a switch from the source), thinking on, reply is reasoning text, second start, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 40.9 | 40.7 to 44.1 | 5 | 2026-11-21 | `f3e0bbdd9f33` | [10](findings/10_hy4_flash_tensorfold_132) |
| median | TensorFold 1.3.3, DFly2 drafts on, thinking on, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 38.2 | 35.3 to 48.6 | 5 | 2026-11-22 | `998afef57c31` | [19](findings/19_tensorfold_133_refresh) |
| median | TensorFold 1.3.2, DFly2 drafts on, thinking on, reply is reasoning text, second start, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 37.1 | 36.2 to 38.1 | 5 | 2026-11-21 | `a9fe24e89f10` | [10](findings/10_hy4_flash_tensorfold_132) |
| median | TensorFold 1.3.2, drafts off, thinking on, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 33.2 | 33.2 to 33.3 | 5 | 2026-11-21 | `b8e543b952e1` | [10](findings/10_hy4_flash_tensorfold_132) |

</details>

<details>
<summary><b>Hy4-flash, oQ4h</b>, 30 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 76.8 | 72.5 to 78.4 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | greedy, temperature 0 | 4K code | 2,048 | 76.2 | 67.5 to 78.5 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 75.6 | 72.7 to 76.8 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 75.1 | 68.0 to 79.3 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 73.5 | 67.0 to 78.6 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | greedy, temperature 0 | 1K code | 2,048 | 72.4 | 56.1 to 78.8 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, no thinking setting, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 54.4 | 50.0 to 57.8 | 5 | 2026-11-21 | `7b6ccfb9c907` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, no thinking setting, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 53.8 | 52.7 to 56.4 | 5 | 2026-11-21 | `7b6ccfb9c907` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP off, thinking off | greedy, temperature 0 | 4K code | 2,048 | 35.5 | 35.4 to 35.5 | 5 | 2026-11-21 | `7a70518485cc` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP off, no thinking setting, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 35.5 | 35.4 to 35.6 | 5 | 2026-11-21 | `0404d67792d9` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP off, no thinking setting, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 35.2 | 35.1 to 35.4 | 5 | 2026-11-21 | `0404d67792d9` | [12](findings/12_hy4_flash_omlx_081) |
| max | oMLX 0.8.1 with its kernels, Lightning MTP off, thinking off | greedy, temperature 0 | 1K code | 2,048 | 35.1 | 35.0 to 35.4 | 5 | 2026-11-21 | `7a70518485cc` | [12](findings/12_hy4_flash_omlx_081) |
| copy task | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 101.0 | 94.3 to 103.0 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| copy task | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 100.9 | 94.2 to 103.4 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| copy task | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | greedy, temperature 0 | 1K code | 512 | 95.9 | 93.7 to 98.1 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| copy task | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | greedy, temperature 0 | 4K code | 512 | 93.0 | 88.8 to 94.5 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| copy task | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 92.1 | 88.1 to 93.3 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| copy task | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 91.7 | 87.6 to 93.6 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| counting toy | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 97.4 | 92.0 to 98.2 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| counting toy | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 1K code | 512 | 97.4 | 92.1 to 98.9 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| counting toy | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | greedy, temperature 0 | 1K code | 512 | 94.0 | 92.6 to 94.0 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| counting toy | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | greedy, temperature 0 | 4K code | 512 | 92.6 | 91.9 to 92.7 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| counting toy | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 92.0 | 91.3 to 92.0 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| counting toy | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | greedy, temperature 0 | 4K code | 512 | 91.5 | 91.3 to 92.1 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, no thinking setting, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 54.0 | 50.4 to 57.9 | 5 | 2026-11-21 | `7b6ccfb9c907` | [12](findings/12_hy4_flash_omlx_081) |
| median | oMLX 0.8.1 with its kernels, Lightning MTP on, default depth, thinking off, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 53.7 | 50.8 to 57.5 | 5 | 2026-11-21 | `61f1f5a70d04` | [12](findings/12_hy4_flash_omlx_081) |
| median | oMLX 0.8.2 with its kernels, Lightning MTP on, default depth, thinking off, older release | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 52.1 | 48.2 to 55.8 | 5 | 2026-11-21 | `fab79618854c` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.3 with its kernels, Lightning MTP on, default depth, thinking off | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 49.8 | 48.4 to 55.2 | 5 | 2026-11-23 | `0d2a17ccad56` | [26](findings/26_omlx_083_refresh) |
| median | oMLX 0.8.1 with its kernels, Lightning MTP off, thinking off | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 35.5 | 35.5 to 35.6 | 5 | 2026-11-21 | `7a70518485cc` | [12](findings/12_hy4_flash_omlx_081) |
| median | oMLX 0.8.1 with its kernels, Lightning MTP off, no thinking setting, reply is reasoning text | temperature 0.9, top-p 1.0 | 4K mixed | 512 | 35.5 | 35.4 to 35.6 | 5 | 2026-11-21 | `0404d67792d9` | [12](findings/12_hy4_flash_omlx_081) |

</details>

<details>
<summary><b>Inkling 2 Mini, oQ4e</b>, 17 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.3 with its kernels, DSpark draft on, default depth, reply is reasoning text, default thinking effort | greedy, temperature 0 | 1K code | 2,048 | 108.1 | 93.7 to 117.8 | 5 | 2026-11-23 | `af8afe759506` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.3 with its kernels, DSpark draft on, default depth, thinking switched off (effort 0), reply mostly reasoning text | greedy, temperature 0 | 1K code | 2,048 | 104.2 | 97.3 to 115.0 | 5 | 2026-11-23 | `0f8455f8a46f` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.3 with its kernels, DSpark draft on, default depth, reply is reasoning text, default thinking effort | greedy, temperature 0 | 4K code | 2,048 | 102.0 | 91.6 to 117.3 | 5 | 2026-11-23 | `af8afe759506` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.1 with its kernels, DSpark draft on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 96.3 | 83.1 to 97.3 | 5 | 2026-11-21 | `a3cf6857c4b5` | [14](findings/14_inkling2_mini_omlx_081) |
| max | oMLX 0.8.3 with its kernels, DSpark draft on, default depth, thinking switched off (effort 0), reply mostly reasoning text | greedy, temperature 0 | 4K code | 2,048 | 92.8 | 89.0 to 110.1 | 5 | 2026-11-23 | `0f8455f8a46f` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.2 with its kernels, DSpark draft on, default depth, reply is reasoning text, third start, older release | greedy, temperature 0 | 1K code | 2,048 | 85.3 | 81.3 to 94.1 | 5 | 2026-11-22 | `a7944f4eab8a` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.1 with its kernels, DSpark draft on, default depth, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 80.1 | 79.5 to 98.3 | 5 | 2026-11-21 | `a3cf6857c4b5` | [14](findings/14_inkling2_mini_omlx_081) |
| max | oMLX 0.8.2 with its kernels, DSpark draft on, default depth, reply is reasoning text, third start, older release | greedy, temperature 0 | 4K code | 2,048 | 78.1 | 73.7 to 87.1 | 5 | 2026-11-22 | `a7944f4eab8a` | [16](findings/16_omlx_082_refresh) |
| max | oMLX 0.8.3 with its kernels, DSpark draft off, thinking switched off (effort 0), reply mostly reasoning text | greedy, temperature 0 | 1K code | 2,048 | 62.4 | 62.2 to 62.5 | 5 | 2026-11-23 | `1e9d52ecfc69` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.3 with its kernels, DSpark draft off, thinking switched off (effort 0), reply mostly reasoning text | greedy, temperature 0 | 4K code | 2,048 | 61.6 | 61.5 to 61.9 | 5 | 2026-11-23 | `1e9d52ecfc69` | [26](findings/26_omlx_083_refresh) |
| max | oMLX 0.8.1 with its kernels, DSpark draft off, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 54.5 | 54.3 to 54.5 | 5 | 2026-11-21 | `fe2a52ddebd0` | [14](findings/14_inkling2_mini_omlx_081) |
| max | oMLX 0.8.1 with its kernels, DSpark draft off, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 53.7 | 53.6 to 53.9 | 5 | 2026-11-21 | `fe2a52ddebd0` | [14](findings/14_inkling2_mini_omlx_081) |
| median | oMLX 0.8.3 with its kernels, DSpark draft on, default depth, reply is reasoning text, default thinking effort | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 83.3 | 78.6 to 87.6 | 5 | 2026-11-23 | `af8afe759506` | [26](findings/26_omlx_083_refresh) |
| median | oMLX 0.8.3 with its kernels, DSpark draft on, default depth, thinking switched off (effort 0), reply mostly reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 80.1 | 72.5 to 82.3 | 5 | 2026-11-23 | `d066e1456e61` | [26](findings/26_omlx_083_refresh) |
| median | oMLX 0.8.1 with its kernels, DSpark draft on, default depth, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 65.9 | 59.2 to 67.7 | 5 | 2026-11-21 | `a3cf6857c4b5` | [14](findings/14_inkling2_mini_omlx_081) |
| median | oMLX 0.8.2 with its kernels, DSpark draft on, default depth, reply is reasoning text, third start, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 60.3 | 50.8 to 72.2 | 5 | 2026-11-22 | `a7944f4eab8a` | [16](findings/16_omlx_082_refresh) |
| median | oMLX 0.8.1 with its kernels, DSpark draft off, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 54.4 | 54.3 to 54.6 | 5 | 2026-11-21 | `fe2a52ddebd0` | [14](findings/14_inkling2_mini_omlx_081) |

</details>

<details>
<summary><b>Inkling 2 Mini, oQ3e</b>, 3 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | oMLX 0.8.1 with its kernels, DSpark draft on, default depth, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 105.1 | 92.2 to 111.9 | 5 | 2026-11-21 | `472bfd081962` | [14](findings/14_inkling2_mini_omlx_081) |
| max | oMLX 0.8.1 with its kernels, DSpark draft on, default depth, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 100.6 | 87.6 to 105.7 | 5 | 2026-11-21 | `472bfd081962` | [14](findings/14_inkling2_mini_omlx_081) |
| median | oMLX 0.8.1 with its kernels, DSpark draft on, default depth, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 67.1 | 61.3 to 83.1 | 5 | 2026-11-21 | `472bfd081962` | [14](findings/14_inkling2_mini_omlx_081) |

</details>

<details>
<summary><b>Inkling 2 Mini, 8-bit</b>, 6 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83, drafts on as the engine picks them, reply is reasoning text, second start | greedy, temperature 0 | 1K code | 2,048 | 146.8 | 131.4 to 162.8 | 5 | 2026-11-22 | `3f129b289ed7` | [20](findings/20_inkling2_mini_mlxserve_pre) |
| max | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83, drafts on as the engine picks them, reply is reasoning text, second start | greedy, temperature 0 | 4K code | 2,048 | 138.7 | 112.5 to 140.2 | 5 | 2026-11-22 | `3f129b289ed7` | [20](findings/20_inkling2_mini_mlxserve_pre) |
| max | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83, drafts off (--no-mtp --no-drafter --no-pld), reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 107.4 | 106.9 to 107.4 | 5 | 2026-11-22 | `8dddc3d76174` | [20](findings/20_inkling2_mini_mlxserve_pre) |
| max | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83, drafts off (--no-mtp --no-drafter --no-pld), reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 105.6 | 105.4 to 106.0 | 5 | 2026-11-22 | `8dddc3d76174` | [20](findings/20_inkling2_mini_mlxserve_pre) |
| median | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83, drafts off (--no-mtp --no-drafter --no-pld), reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 105.2 | 104.8 to 106.0 | 5 | 2026-11-22 | `a76707324154` | [20](findings/20_inkling2_mini_mlxserve_pre) |
| median | mlx-serve 26.11.4-pre-release.1, main at 2fe9be83, drafts on as the engine picks them, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 104.5 | 102.9 to 107.3 | 5 | 2026-11-22 | `338b6385675f` | [20](findings/20_inkling2_mini_mlxserve_pre) |

</details>

<details>
<summary><b>Inkling 2 Mini, Bare Speed</b>, 15 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 159.7 | 136.3 to 163.1 | 5 | 2026-11-22 | `69e9ae98c9d1` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 153.6 | 129.1 to 202.8 | 5 | 2026-11-22 | `ea4c8fa3bbcf` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 153.0 | 143.1 to 172.7 | 5 | 2026-11-23 | `8ddc9a4f863a` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 152.6 | 128.8 to 162.8 | 5 | 2026-11-22 | `69e9ae98c9d1` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 149.0 | 139.6 to 158.0 | 5 | 2026-11-22 | `ea4c8fa3bbcf` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 140.4 | 137.7 to 149.7 | 5 | 2026-11-23 | `8ddc9a4f863a` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 90.1 | 89.8 to 90.4 | 5 | 2026-11-22 | `a96cb656f07d` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head off (--no-mtp), no thinking field, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 89.9 | 89.7 to 90.1 | 5 | 2026-11-23 | `f41fca789e86` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.2, draft head off (--no-mtp), no thinking field, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 88.5 | 88.2 to 89.2 | 5 | 2026-11-23 | `f41fca789e86` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 88.4 | 88.2 to 89.2 | 5 | 2026-11-22 | `a96cb656f07d` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 130.0 | 115.0 to 159.3 | 5 | 2026-11-22 | `0bb9739897e0` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 124.7 | 114.1 to 134.7 | 5 | 2026-11-23 | `8ddc9a4f863a` | [29](findings/29_inkling2_mini_mtplx_2132) |
| median | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 120.2 | 114.0 to 176.9 | 5 | 2026-11-22 | `15120ef4588c` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.2, draft head off (--no-mtp), no thinking field, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 78.9 | 78.3 to 79.7 | 5 | 2026-11-23 | `f41fca789e86` | [29](findings/29_inkling2_mini_mtplx_2132) |
| median | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 78.5 | 78.0 to 79.7 | 5 | 2026-11-22 | `a96cb656f07d` | [21](findings/21_inkling2_mini_mtplx_213) |

</details>

<details>
<summary><b>Inkling 2 Mini, Optimized Speed</b>, 12 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 159.0 | 146.7 to 173.2 | 5 | 2026-11-22 | `e8af192bf883` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 152.0 | 141.0 to 184.2 | 5 | 2026-11-23 | `db1ba3d496e1` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 148.0 | 132.8 to 149.7 | 5 | 2026-11-22 | `472c4ceb9644` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 147.2 | 118.1 to 158.0 | 5 | 2026-11-22 | `e8af192bf883` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 143.4 | 135.1 to 164.9 | 5 | 2026-11-22 | `472c4ceb9644` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 136.1 | 134.5 to 154.1 | 5 | 2026-11-23 | `db1ba3d496e1` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 82.4 | 82.1 to 82.6 | 5 | 2026-11-22 | `0f6c20468d28` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 81.5 | 81.3 to 82.4 | 5 | 2026-11-22 | `0f6c20468d28` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 115.1 | 103.2 to 129.9 | 5 | 2026-11-22 | `472c4ceb9644` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 113.0 | 109.1 to 122.6 | 5 | 2026-11-23 | `db1ba3d496e1` | [29](findings/29_inkling2_mini_mtplx_2132) |
| median | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 112.5 | 109.6 to 124.7 | 5 | 2026-11-22 | `e8af192bf883` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 69.4 | 69.4 to 69.8 | 5 | 2026-11-22 | `0f6c20468d28` | [21](findings/21_inkling2_mini_mtplx_213) |

</details>

<details>
<summary><b>Inkling 2 Mini, Optimized Quality</b>, 12 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 136.5 | 123.4 to 157.8 | 5 | 2026-11-22 | `f0dac5df559b` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 133.8 | 128.3 to 142.5 | 5 | 2026-11-23 | `7ea5b8ae2d9e` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 1K code | 2,048 | 131.7 | 124.9 to 168.8 | 5 | 2026-11-22 | `b06906a7e390` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 129.7 | 117.0 to 149.8 | 5 | 2026-11-22 | `b06906a7e390` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | greedy, temperature 0 | 4K code | 2,048 | 127.9 | 115.0 to 146.9 | 5 | 2026-11-22 | `f0dac5df559b` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 121.6 | 113.6 to 134.8 | 5 | 2026-11-23 | `7ea5b8ae2d9e` | [29](findings/29_inkling2_mini_mtplx_2132) |
| max | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text | greedy, temperature 0 | 1K code | 2,048 | 69.6 | 69.4 to 69.7 | 5 | 2026-11-22 | `a28a0a8eae9d` | [21](findings/21_inkling2_mini_mtplx_213) |
| max | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text | greedy, temperature 0 | 4K code | 2,048 | 68.9 | 68.8 to 69.2 | 5 | 2026-11-22 | `a28a0a8eae9d` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.1, draft head on, no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 106.7 | 81.6 to 118.0 | 5 | 2026-11-22 | `f0dac5df559b` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.2, draft head on, no thinking field, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 105.6 | 93.1 to 129.3 | 5 | 2026-11-23 | `7ea5b8ae2d9e` | [29](findings/29_inkling2_mini_mtplx_2132) |
| median | MTPLX 2.13.0, draft head on, no thinking field, reply is reasoning text, older release | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 104.1 | 97.5 to 109.8 | 5 | 2026-11-22 | `b06906a7e390` | [21](findings/21_inkling2_mini_mtplx_213) |
| median | MTPLX 2.13.1, draft head off (--no-mtp), no thinking field, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 62.7 | 62.7 to 62.8 | 5 | 2026-11-22 | `a28a0a8eae9d` | [21](findings/21_inkling2_mini_mtplx_213) |

</details>

<details>
<summary><b>Inkling 2 Mini, 4-bit</b>, 3 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | Rapid-MLX 1.1.0, the catalog's settings, no drafts, reply is reasoning text, second start | greedy, temperature 0 | 1K code | 2,048 | 39.8 | 39.5 to 40.0 | 5 | 2026-11-22 | `3c2cb9130c7b` | [23](findings/23_inkling2_mini_rapidmlx_110) |
| max | Rapid-MLX 1.1.0, the catalog's settings, no drafts, reply is reasoning text, second start | greedy, temperature 0 | 4K code | 2,048 | 39.5 | 39.4 to 39.5 | 5 | 2026-11-22 | `3c2cb9130c7b` | [23](findings/23_inkling2_mini_rapidmlx_110) |
| median | Rapid-MLX 1.1.0, the catalog's settings, no drafts, reply is reasoning text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 39.4 | 39.3 to 39.9 | 5 | 2026-11-22 | `3bef921b4076` | [23](findings/23_inkling2_mini_rapidmlx_110) |

</details>

<details>
<summary><b>Qwen3.8 Flash Next, IQ3_S</b>, 23 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | Strata 0.2.19, setup's config with --spec 5, MTP on, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 200.3 | 183.5 to 215.1 | 5 | 2026-11-23 | `ef38b6483d5b` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.20, setup's config with --spec 5, MTP on, thinking off | greedy, temperature 0 | 1K code | 2,048 | 196.4 | 192.5 to 211.1 | 5 | 2026-11-23 | `dc88686985f3` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.19, setup's config with --spec 4, MTP on, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 193.6 | 172.8 to 211.9 | 5 | 2026-11-23 | `ca9762656ee4` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.20, setup's config with --spec 4, MTP on, thinking off | greedy, temperature 0 | 1K code | 2,048 | 189.2 | 187.0 to 208.6 | 5 | 2026-11-23 | `88b41d226df3` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.19, setup's config with --spec 4, MTP on, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 188.5 | 186.3 to 196.1 | 5 | 2026-11-23 | `ca9762656ee4` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.20, setup's config with --spec 5, MTP on, thinking off | greedy, temperature 0 | 4K code | 2,048 | 186.3 | 162.5 to 195.6 | 5 | 2026-11-23 | `dc88686985f3` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.19, setup's config with --spec 5, MTP on, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 185.0 | 176.1 to 200.5 | 5 | 2026-11-23 | `ef38b6483d5b` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.20, setup's config with --spec 4, MTP on, thinking off | greedy, temperature 0 | 4K code | 2,048 | 183.6 | 164.5 to 190.6 | 5 | 2026-11-23 | `88b41d226df3` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.20, setup's config, MTP on, --spec 3 --spec-min-p 0.5, thinking off, reads its saved table | greedy, temperature 0 | 1K code | 2,048 | 181.6 | 178.9 to 188.9 | 5 | 2026-11-23 | `8b55935c332e` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.19, setup's config, MTP on, --spec 3 --spec-min-p 0.5, thinking off, second start, older release | greedy, temperature 0 | 1K code | 2,048 | 173.8 | 173.1 to 180.3 | 5 | 2026-11-23 | `7b15a99cb722` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.20, setup's config, MTP on, --spec 3 --spec-min-p 0.5, thinking off, reads its saved table | greedy, temperature 0 | 4K code | 2,048 | 173.3 | 169.4 to 194.1 | 5 | 2026-11-23 | `8b55935c332e` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.19, setup's config, MTP on, --spec 3 --spec-min-p 0.5, thinking off, second start, older release | greedy, temperature 0 | 4K code | 2,048 | 169.4 | 166.2 to 172.4 | 5 | 2026-11-23 | `7b15a99cb722` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.19, MTP off by setup's own rule, thinking off, older release | greedy, temperature 0 | 1K code | 2,048 | 100.6 | 99.6 to 101.1 | 5 | 2026-11-23 | `dff5db389042` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.19, MTP off by setup's own rule, thinking off, older release | greedy, temperature 0 | 4K code | 2,048 | 99.2 | 99.1 to 99.3 | 5 | 2026-11-23 | `dff5db389042` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | Strata 0.2.20, MTP off by setup's own rule, thinking off | greedy, temperature 0 | 1K code | 2,048 | 98.7 | 98.0 to 100.3 | 5 | 2026-11-23 | `651e54639f7c` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | Strata 0.2.20, MTP off by setup's own rule, thinking off | greedy, temperature 0 | 4K code | 2,048 | 97.7 | 97.4 to 98.2 | 5 | 2026-11-23 | `651e54639f7c` | [28](findings/28_qwen38_flash_next_strata_0220) |
| max | llama.cpp b12359, the same IQ3_S files, defaults, thinking off | greedy, temperature 0 | 1K code | 2,048 | 58.2 | 57.7 to 58.6 | 5 | 2026-11-23 | `37c6f64892e9` | [24](findings/24_qwen38_flash_next_strata_0219) |
| max | llama.cpp b12359, the same IQ3_S files, defaults, thinking off | greedy, temperature 0 | 4K code | 2,048 | 57.4 | 57.3 to 60.0 | 5 | 2026-11-23 | `37c6f64892e9` | [24](findings/24_qwen38_flash_next_strata_0219) |
| median | Strata 0.2.19, setup's config, MTP on, --spec 3 --spec-min-p 0.5, thinking off, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 136.5 | 127.6 to 139.1 | 5 | 2026-11-23 | `77bb7582fe47` | [24](findings/24_qwen38_flash_next_strata_0219) |
| median | Strata 0.2.20, setup's config, MTP on, --spec 3 --spec-min-p 0.5, thinking off, reads its saved table | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 126.0 | 123.4 to 143.3 | 5 | 2026-11-23 | `8b55935c332e` | [28](findings/28_qwen38_flash_next_strata_0220) |
| median | Strata 0.2.19, MTP off by setup's own rule, thinking off, older release | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 96.4 | 96.2 to 96.4 | 5 | 2026-11-23 | `dff5db389042` | [24](findings/24_qwen38_flash_next_strata_0219) |
| median | Strata 0.2.20, MTP off by setup's own rule, thinking off | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 95.1 | 94.1 to 95.7 | 5 | 2026-11-23 | `651e54639f7c` | [28](findings/28_qwen38_flash_next_strata_0220) |
| median | llama.cpp b12359, the same IQ3_S files, defaults, thinking off | temperature 0.7, top-p 0.8, top-k 20 | 4K mixed | 512 | 55.7 | 55.3 to 55.7 | 5 | 2026-11-23 | `37c6f64892e9` | [24](findings/24_qwen38_flash_next_strata_0219) |

</details>

<details>
<summary><b>Inkling 2 Mini, SQ-20</b>, 6 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | Strata 0.2.20, Strata's own pack, DSpark drafter on, setup's config, engine built from source, thinking off (effort none), reply is answer text | greedy, temperature 0 | 4K code | 2,048 | 106.1 | 83.4 to 127.2 | 5 | 2026-11-23 | `acb7355827b4` | [30](findings/30_inkling2_mini_strata_0220) |
| max | Strata 0.2.20, Strata's own pack, DSpark drafter on, setup's config, engine built from source, thinking off (effort none), reply is answer text | greedy, temperature 0 | 1K code | 2,048 | 105.8 | 66.0 to 112.7 | 5 | 2026-11-23 | `acb7355827b4` | [30](findings/30_inkling2_mini_strata_0220) |
| max | Strata 0.2.20, Strata's own pack, drafting off, engine built from source, thinking off (effort none), reply is answer text | greedy, temperature 0 | 1K code | 2,048 | 61.5 | 60.9 to 62.3 | 5 | 2026-11-23 | `43be61155ecd` | [30](findings/30_inkling2_mini_strata_0220) |
| max | Strata 0.2.20, Strata's own pack, drafting off, engine built from source, thinking off (effort none), reply is answer text | greedy, temperature 0 | 4K code | 2,048 | 59.1 | 58.7 to 60.3 | 5 | 2026-11-23 | `43be61155ecd` | [30](findings/30_inkling2_mini_strata_0220) |
| median | Strata 0.2.20, Strata's own pack, drafting off, engine built from source, thinking off (effort none), reply is answer text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 59.3 | 59.0 to 59.4 | 5 | 2026-11-23 | `43be61155ecd` | [30](findings/30_inkling2_mini_strata_0220) |
| median | Strata 0.2.20, Strata's own pack, DSpark drafter on, setup's config, engine built from source, thinking off (effort none), reply is answer text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 37.7 | 35.6 to 40.3 | 5 | 2026-11-23 | `acb7355827b4` | [30](findings/30_inkling2_mini_strata_0220) |

</details>

<details>
<summary><b>Inkling 2 Mini, UD-Q8_K_XL</b>, 3 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | Strata 0.2.20, Unsloth's GGUF, drafting off (this build refused the DSpark file), engine built from source, thinking off (effort none), reply is answer text | greedy, temperature 0 | 1K code | 2,048 | 60.1 | 59.3 to 60.5 | 5 | 2026-11-23 | `c7ce703a276f` | [30](findings/30_inkling2_mini_strata_0220) |
| max | Strata 0.2.20, Unsloth's GGUF, drafting off (this build refused the DSpark file), engine built from source, thinking off (effort none), reply is answer text | greedy, temperature 0 | 4K code | 2,048 | 58.4 | 57.4 to 58.7 | 5 | 2026-11-23 | `c7ce703a276f` | [30](findings/30_inkling2_mini_strata_0220) |
| median | Strata 0.2.20, Unsloth's GGUF, drafting off (this build refused the DSpark file), engine built from source, thinking off (effort none), reply is answer text | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 58.2 | 58.0 to 59.5 | 5 | 2026-11-23 | `c7ce703a276f` | [30](findings/30_inkling2_mini_strata_0220) |

</details>

<details>
<summary><b>Inkling 2 Mini, maker's release</b>, 3 setups</summary>

| Kind | Engine and setup | Sampler | Prompt | Reply tokens | Decode tok/s | Range | Runs | Date | Run | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| max | Ollama 0.40.17, MTP drafter on, as in Ollama's library model, Ollama's default thinking (no thinking field, effort 0.9), reply is reasoning text, sampler adds Ollama's default top-k 40 | greedy, temperature 0 | 4K code | 2,048 | 82.3 | 70.6 to 87.7 | 5 | 2026-11-23 | `b5f573f87f3c` | [31](findings/31_inkling2_mini_ollama_04017) |
| max | Ollama 0.40.17, MTP drafter on, as in Ollama's library model, Ollama's default thinking (no thinking field, effort 0.9), reply is reasoning text, sampler adds Ollama's default top-k 40 | greedy, temperature 0 | 1K code | 2,048 | 76.6 | 71.5 to 88.4 | 5 | 2026-11-23 | `b5f573f87f3c` | [31](findings/31_inkling2_mini_ollama_04017) |
| median | Ollama 0.40.17, MTP drafter on, as in Ollama's library model, Ollama's default thinking (no thinking field, effort 0.9), reply is reasoning text, sampler adds Ollama's default top-k 40 | temperature 1.0, top-p 1.0 | 4K mixed | 512 | 61.7 | 51.2 to 68.4 | 5 | 2026-11-23 | `b5f573f87f3c` | [31](findings/31_inkling2_mini_ollama_04017) |

</details>

## Findings

ELI5: Each finding is one question, one run of an hour or two, and one report. Newest first. Click a title for the full report and the raw rows.

### 34. [MiniMax H3 video on mlx-serve 26.11.3, round two, the 4-bit pack and HyperFlow H3 Flash, seconds per clip](findings/34_minimax_h3_video_mlxserve_round2)

Runs of 23 to 24 Nov 2026. mlx-serve 26.11.3 made a 5-second MiniMax H3 clip with sound at 832 by 480 in 35.0 s on its author's 4-bit pack and 35.1 s on the 8-bit pack, both with 4-step Turbo, and in 136.1 s and 135.1 s at 1344 by 768. The 4-bit pack is 27.0 GiB smaller and was no faster, with the int8 path on or off. HyperFlow H3 Flash, given a first and a last frame, took 43.5 s at 832 by 480 with its 6 steps.

<details>
<summary>Chart</summary>

![Bars of seconds per 5-second MiniMax H3 clip on mlx-serve 26.11.3, lower is faster, the 8-bit pack against the 4-bit pack. At 832 by 480 with the int8 path on, 35.1 and 35.0. At 1344 by 768 with it on, 135.1 and 136.1. At 832 by 480 with it off, 48.9 and 47.8.](findings/34_minimax_h3_video_mlxserve_round2/chart_seconds.png)

</details>

### 33. [MiniMax H3 video on mlx-serve 26.11.3 and Rapid-MLX 1.1.0, seconds per clip](findings/33_minimax_h3_video_mlxserve_rapidmlx)

Runs of 23 Nov 2026. mlx-serve 26.11.3, on its author's 8-bit pack with its 4-step Turbo, made a 5-second MiniMax H3 clip with sound in 34.9 s at 832 by 480 and 149.4 s at 1344 by 768, H3's native size. Rapid-MLX 1.1.0, on the maker's bf16 weights with its fixed 9-step Turbo LoRA, took 116.6 s and 446.2 s. mlx-serve's own 30-step default took 109.3 s, and 471.4 s on one clip. Different weights, adapters and step counts, so the gaps are not one engine's speed alone. A rerun of mlx-serve's 1344 by 768 clip on 24 Nov took 132.0 s and 138.2 s, in finding 34.

<details>
<summary>Chart</summary>

![Bars of seconds per clip for MiniMax H3 video, lower is faster. At 832 by 480 for 5 seconds, mlx-serve Turbo 4 steps 34.9, mlx-serve default 30 steps 109.3, Rapid-MLX Turbo LoRA 9 steps 116.6. At 1344 by 768 for 5 seconds, 149.4, 471.4 and 446.2. At 832 by 480 for 10 seconds, mlx-serve Turbo 100.7 and Rapid-MLX 293.5, with no mlx-serve default bar.](findings/33_minimax_h3_video_mlxserve_rapidmlx/chart_seconds.png)

</details>

### 32. [mlx-lm 0.32.2 on Qwen3.8-27B 4-bit, the inference-optimisation skill's levers](findings/32_mlxlm_skill_qwen38_27b)

Runs of 23 Nov 2026. mlx-lm 0.32.2, run as its docs show, decoded Qwen3.8-27B 4-bit at 43.9 tok/s for one user sending no seed, at most 70% of this Mac's ceiling, and 45.2 with a seed. None of the skill's levers that mlx-lm 0.32.2 offers on this model raised that. It has no drafting route here, and a larger prefill step showed no change this test could see. With no seed, 8 users together got 114.5 tok/s in all.

<details>
<summary>Chart</summary>

![Bars in tokens per second for mlx-lm 0.32.2 on Qwen3.8-27B 4-bit. Ceiling for one user, at least 63.1. One user decoding with no seed, 43.9. One user with a seed, 45.2. With a seed and prefill step 4096, 45.1. All tokens over wall time with no seed, two users 67.7, four users 99.4, eight users 114.5.](findings/32_mlxlm_skill_qwen38_27b/chart_skill.png)

</details>

### 31. [Inkling 2 Mini on Ollama 0.40.17, its drafter 2.3 times as fast, with the thinking hidden](findings/31_inkling2_mini_ollama_04017)

Runs of 23 Nov 2026. Ollama 0.40.17 decoded Inkling 2 Mini at 76.8 tok/s at its max with its MTP drafter, and 51.0 with the model's own sampler, by Ollama's own count, on the maker's release rebuilt to match Ollama's library model tensor for tensor. With no drafter it decoded 33.6 and 32.4, so the drafter made greedy decoding on code prompts 2.3 times as fast. With thinking off the model still thought at effort 0 and Ollama dropped that thinking from the reply, so 27 of 40 greedy replies to code prompts, capped at 2,048 tokens, came back with no text.

<details>
<summary>Chart</summary>

![Paired bars of decode speed in tokens per second, by Ollama's own count, for Inkling 2 Mini on Ollama 0.40.17, no drafter against the MTP drafter on. Code prompt at 1K, replies capped at 2,048 tokens, 33.6 and 76.8. The same at 4K, 33.2 and 75.8. Code prompt at 1K, capped at 512, 33.2 and 65.6. Mixed text at 4K with the model's own sampler, 32.4 and 51.0.](findings/31_inkling2_mini_ollama_04017/chart_draft.png)

</details>

### 30. [Inkling 2 Mini on Strata 0.2.20, its drafter faster on greedy code and slower on the sampler](findings/30_inkling2_mini_strata_0220)

Runs of 23 Nov 2026. Strata 0.2.20, its Inkling engine built from source, wrote 106.1 tok/s on Inkling 2 Mini at its max with Strata's own SQ-20 pack and its DSpark drafter, and 37.7 with the model's own sampler. With drafting off it wrote 61.5 and 59.3. So the drafter made greedy code 1.7 times as fast and the sampler 0.64 times as fast, and it changes 14 of 100 short greedy replies. This build refused the DSpark drafter file Strata's setup pins for Unsloth's GGUF, so the GGUF ran with drafting off only, at 60.1. Every reply is answer text.

<details>
<summary>Chart</summary>

![Paired bars of writing speed in tokens per second for Inkling 2 Mini on Strata 0.2.20 with Strata's SQ-20 pack, DSpark drafter off against on. Greedy code with replies of up to 2,048 tokens at 1K, 61.5 and 105.8. The same at 4K, 59.1 and 106.1. Greedy code with 512-token replies at 1K, 61.6 and 90.0. The model's own sampler at 4K, 59.3 and 37.7.](findings/30_inkling2_mini_strata_0220/chart_draft.png)

</details>

### 29. [Inkling 2 Mini on MTPLX 2.13.2, 2.8 times as fast with top-p 0.95](findings/29_inkling2_mini_mtplx_2132)

Runs of 23 Nov 2026. MTPLX 2.13.2 writes Inkling 2 Mini 2.8 times as fast as 2.13.1 when a request sets top-p 0.95, as its notes say. On the Bare Speed pack at a 4K prompt it wrote 122.0 tok/s against 42.9, faster on 20 of 20 same-text pairs. Top-p 0.95 cut 2.13.1 to 0.36 of its own top-p 1.0 speed and left 2.13.2 where it was. At the model's own sampler, top-p 1.0, and on greedy code, 2.13.2 shows no change I can call, and all 100 short greedy replies match on all three packs.

<details>
<summary>Chart</summary>

![Paired bars of writing speed in tokens per second for Inkling 2 Mini Bare Speed, MTPLX 2.13.1 against 2.13.2, the middle of 10 runs over two starts each. Long code at 1K, 153.9 and 152.1. Long code at 4K, 148.7 and 147.5. Short code at 1K, 137.4 and 142.7. The model's own sampler at 4K, 120.6 and 123.9.](findings/29_inkling2_mini_mtplx_2132/chart_bare.png)

</details>

### 28. [Strata 0.2.20 on Qwen3.8 Flash Next IQ3_S, level with 0.2.19, and its saved draft table](findings/28_qwen38_flash_next_strata_0220)

Runs of 23 Nov 2026. Strata 0.2.20 writes at the same speed as 0.2.19 on Qwen3.8 Flash Next IQ3_S. Back to back, with each release reading a draft table learned from the same requests, 0.2.20 wrote 181.7 and 181.6 tok/s at the max and 0.2.19 wrote 182.7, middle ratios 0.99 to 1.00 on every greedy test. Strata saves a table of draft costs and later starts read it. The table 0.2.19 saved at 02:28 SGT priced a 3-token check at 29.5 ms, about twice the later tables, and made later 0.2.19 starts 6 to 7% slower on long code. That cost was measured on a slow first request, and a quiet repeat measured 14.9 ms. 0.2.20 changes 2 of 50 short answers.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Qwen3.8 Flash Next IQ3_S, greedy, new code, replies of up to 2,048 tokens, 1K prompt, Strata 0.2.19 against 0.2.20. No table, 180.3 and 183.4. 0.2.19 reading its table from 09:42 SGT and 0.2.20 its table from 08:48 SGT, 182.7 and 181.6. 0.2.19 reading its table from 02:28 SGT and 0.2.20 its table from 08:48 SGT, 169.7 and 181.7.](findings/28_qwen38_flash_next_strata_0220/chart_max.png)

</details>

### 27. [TensorFold 1.3.4, Flash Next 4-bit 2% faster on five starts of six, seven settings level](findings/27_tensorfold_134_refresh)

Runs of 23 Nov 2026. TensorFold 1.3.4 is about 2% faster on Qwen3.8 Flash Next 4-bit and level on the seven other settings I reran. On the counting toy, five of six 1.3.4 starts wrote 377.8 to 379.3 tok/s at 1K, where four 1.3.3 starts wrote 369.4 to 369.8. Three 1.3.4 starts run beside one 1.3.3 start were faster on 30 of 30 counting pairs, middle ratio 1.02. The sixth 1.3.4 start ran partly at each release's speed and came out level. The replies are the same, and the Flash Next server holds 7.2 GiB less. DeepSeek V4.1 Flash, Qwen3.8 27B, GLM-5.3 Flash and Hy4-flash show no speed change I can call.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Qwen3.8 Flash Next 4-bit on the counting toy, greedy, 512-token replies, 1K prompt, four starts of TensorFold 1.3.3 against four of 1.3.4. First start of each release, 369.5 and 378.7. Same night 1, 369.4 and 369.9. Same night 2, 369.8 and 377.9. Check, 369.8 and 377.8.](findings/27_tensorfold_134_refresh/chart_count.png)

</details>

### 26. [oMLX 0.8.3, Inkling 2 Mini faster and three models level](findings/26_omlx_083_refresh)

Runs of 23 Nov 2026. oMLX 0.8.3 wrote 108.1 tok/s on Inkling 2 Mini oQ4e at its max and 83.3 with the model's own sampler, against 85.3 and 60.3 on the last 0.8.2 start. Text by text it was faster on 25 of 25 pairs against each of three 0.8.2 starts, with middle ratios from 1.17 to 1.38. With drafts on and off it now wrote the same short replies, 100 of 100. Hy4-flash gave its first token 1.47 times sooner. GLM-5.3 Flash, Hy4-flash and Qwen3.8 Flash Next wrote at the same speed as on 0.8.2. Switching thinking off did not stop Inkling 2 Mini thinking.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second, oMLX 0.8.2 against 0.8.3, drafts on, median of 5. Max is greedy new code, 2,048-token replies, 1K prompt. Inkling 2 Mini oQ4e max 85.3 against 108.1. Inkling 2 Mini median, own sampler, 4K prompt, 60.3 against 83.3. GLM-5.3 Flash max 76.0 against 77.4. Hy4-flash max 76.8 against 72.4. Qwen3.8 Flash Next max 50.8 against 49.0.](findings/26_omlx_083_refresh/chart_max.png)

</details>

### 25. [Qwen-Image 2.1 and its Turbo on mlx-serve 26.11.3, against Rapid-MLX 1.1.0](findings/25_qwen_image_mlxserve_26113)

Runs of 22 and 23 Nov 2026. With the same passes a step, mlx-serve 26.11.3 made each picture in about half Rapid-MLX 1.1.0's time. A 1024 by 1024 Qwen-Image 2.1 picture at 20 steps took 8.3 s against 17.2 s, and a Turbo picture 3.9 s against 8.7 s. Most of the gap is mlx-serve's lossy int8 path, on by default on this Mac. With it off, a step took 0.71 s against Rapid-MLX's 0.72 s. mlx-serve read its author's 8-bit packs and Rapid-MLX the makers' bf16 weights.

<details>
<summary>Chart</summary>

![Bars of seconds per picture, shorter is faster, the same passes a step on both engines, mlx-serve with its int8 path on. Turbo, 1024 square, 8 steps. Rapid-MLX 8.7, mlx-serve 3.9. Qwen-Image 2.1, 1024 square, 20 steps. Rapid-MLX 17.2, mlx-serve 8.3. The same at 40 steps, Rapid-MLX 34.1, mlx-serve 16.6. 2048 square, 20 steps, Rapid-MLX 105.4, mlx-serve 53.3. 1024 square, 20 steps, two passes a step, Rapid-MLX 33.4, mlx-serve 18.4.](findings/25_qwen_image_mlxserve_26113/chart_seconds.png)

</details>

### 24. [Qwen3.8 Flash Next IQ3_S on Strata 0.2.19, MTP on and off, against llama.cpp on the same files](findings/24_qwen38_flash_next_strata_0219)

Runs of 23 Nov 2026. Strata 0.2.19 wrote 200.3 tok/s on Qwen3.8 Flash Next IQ3_S at its max, with --spec 5. With its setup's own config, MTP on and a 3-token window, it wrote 173.8 on its latest start and 183.3 on the start before. With the model's own sampler it wrote 136.5. llama.cpp b12359 on the same files wrote 58.2 and 55.7, so Strata is 3.4 times llama.cpp at the max and 2.5 times at the median. Setup's config and MTP off wrote the same text on 100 of 100 replies.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Qwen3.8 Flash Next IQ3_S, greedy at temperature 0, new code, replies of up to 2,048 tokens. At a 1K and a 4K prompt. llama.cpp 58.2 and 57.4. Strata with MTP off 100.6 and 99.2. Strata with its setup's config, first start 183.3 and 179.7, second start 173.8 and 169.4. With --spec 4, 193.6 and 188.5. With --spec 5, 200.3 and 185.0.](findings/24_qwen38_flash_next_strata_0219/chart_max.png)

</details>

### 23. [Inkling 2 Mini on Rapid-MLX 1.1.0, max and median speed](findings/23_inkling2_mini_rapidmlx_110)

Runs of 22 Nov 2026. Rapid-MLX 1.1.0 wrote 39.8 tok/s on Inkling 2 Mini at its max, on its latest start, and 39.7 on the start before. With the model's own sampler it wrote 39.4. Every test sat between 39.4 and 40.0, greedy or sampled, 1K or 4K prompt, 512 or 2,048-token replies. The catalog runs this model with no drafts. Replies were reasoning text, 54 of 55 timed replies streaming no answer text.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Inkling 2 Mini on Rapid-MLX 1.1.0, greedy at temperature 0, new code, replies of up to 2,048 tokens. At a 1K prompt, first start 39.7, second start 39.8. At 4K, 39.5 and 39.5.](findings/23_inkling2_mini_rapidmlx_110/chart_max.png)

</details>

### 22. [Qwen-Image 2.1 and MiniMax H3 video on Rapid-MLX 1.1.0, time per picture and per clip](findings/22_image_video_rapidmlx_110)

Runs of 22 Nov 2026. Rapid-MLX 1.1.0 made a 1024 by 1024 Qwen-Image 2.1 picture in 17.1 s at 20 steps, the same on two starts and ten pictures. The Turbo model made one in 8.7 s at 8 steps. MiniMax H3, its weights not quantized, made a 5-second clip, 124 frames at 24 fps, in 116.5 s at 832 by 480 and 388.9 s at 1280 by 720.

<details>
<summary>Chart</summary>

![Bars of seconds per output on Rapid-MLX 1.1.0, lower is faster. Qwen-Image 2.1 Turbo 1024 square, 8 steps, 8.7. Qwen-Image 2.1 1024 square, 20 steps, 17.1. The same at 40 steps, 34.1. Qwen-Image 2.1 2048 square, 20 steps, 105.4. MiniMax H3 5-second clip at 768 by 448, 92.5. At 832 by 480, 116.5. At 1280 by 720, 388.9.](findings/22_image_video_rapidmlx_110/chart_seconds.png)

</details>

### 21. [Inkling 2 Mini on MTPLX 2.13.1, three packs, drafts on and off](findings/21_inkling2_mini_mtplx_213)

Runs of 22 Nov 2026. MTPLX 2.13.1 wrote 159.7 tok/s on Inkling 2 Mini Bare Speed at its max, on its latest start, and 161.1 on the start before. With the model's own sampler it wrote 130.0. With the draft head off the same pack wrote 90.1 and 78.5, so the drafts gave 1.77 times at the max and 1.66 times at the median. The drafts did not change a reply, 100 of 100 the same text with them on and off, on every pack. Optimized Speed wrote 148.0 and 115.1, and Optimized Quality 136.5 and 106.7. Replies were reasoning text.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Inkling 2 Mini on MTPLX 2.13.1, greedy at temperature 0, new code, replies of up to 2,048 tokens, 1K prompt. Bare Speed, drafts off 90.1, drafts on 159.7. Optimized Speed, 82.4 and 143.4. Optimized Quality, 69.6 and 136.5.](findings/21_inkling2_mini_mtplx_213/chart_max.png)

</details>

### 20. [Inkling 2 Mini on the mlx-serve 26.11.4 pre-release, max and median speed](findings/20_inkling2_mini_mlxserve_pre)

Runs of 22 Nov 2026. mlx-serve 26.11.4-pre-release.1 wrote 146.8 tok/s on Inkling 2 Mini at its max, on its latest start, and 160.5 on the start before. With the model's own sampler it wrote 104.5. With its drafts off the same pack wrote 107.4 at the max and 105.2 with the sampler. So text by text the drafts were faster on all 10 long code replies, with a middle ratio of 1.32, and level with the sampler. Every reply I read back was reasoning text, though the request switched thinking off.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Inkling 2 Mini on the mlx-serve 26.11.4 pre-release, greedy at temperature 0, new code, replies of up to 2,048 tokens. At a 1K prompt, drafts off 107.4, drafts on first start 160.5, drafts on second start 146.8. At 4K, 105.6, 131.3 and 138.7.](findings/20_inkling2_mini_mlxserve_pre/chart_max.png)

</details>

### 19. [Seven builds on TensorFold 1.3.3, a version refresh](findings/19_tensorfold_133_refresh)

Runs of 22 Nov 2026. I see no speed change on TensorFold 1.3.3 on any of these seven builds. Text by text against the latest 1.3.2 start, the middle ratio sits between 0.96 and 1.06 on every test but two, and the replies I checked are the same. One was Qwen3.8 27B with its own sampler, 136.2 tok/s on its first 1.3.3 start against 161.3 on 1.3.2. Run again on one night, the two releases wrote 147.0 and 147.3 over 20 requests each, so that was a low start and not the release. The other is Hy4-flash 8-bit with the draft-bits switch and its own sampler, 1.08, with 1.3.3 faster on only 3 of 5 texts. One thing is new. GLM-5.3 Flash can now draft with a DFlash2 model on a Mac, and it wrote 84.2 tok/s with its own sampler against 79.8 with the built-in MTP drafts, with the same replies.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second, greedy at temperature 0, new code, replies of up to 2,048 tokens, 1K prompt, on TensorFold 1.3.2 and 1.3.3. Qwen3.8 27B 4-bit 328.9 and 315.3. Qwen3.8 Flash Next 4-bit 206.8 and 206.8. GLM-5.3 Flash 4-bit 101.4 and 102.1. GLM-5.3 Flash oQ4e 80.7 and 81.2. Hy4-flash 4-bit 64.6 and 61.8. Qwen3.8 Flash Next 6-bit 200.1 and 201.3. Hy4-flash 8-bit at defaults 47.6 and 46.7.](findings/19_tensorfold_133_refresh/chart_max.png)

</details>

### 18. [DeepSeek V4.1 Flash on TensorFold 1.3.3, the release](findings/18_dsv41_tensorfold_133)

Runs of 22 Nov 2026. TensorFold 1.3.3 wrote 108.0 tok/s on DeepSeek V4.1 Flash at its max and 74.5 with the model's own sampler. TensorFold 1.3.0 wrote 75.2 and 45.7 on the same night, so 1.3.3 is 1.44 and 1.63 times as fast. It was faster on every same-text pair, 58 of 58 and 55 of 55, on two starts. The answers did not change. 250 of 250 short greedy answers match 1.3.0, and so do the replies to the engine author's own 16 prompts, greedy and sampled. The release matches the main-branch build of finding 17 in speed and in text.

<details>
<summary>Chart</summary>

![Paired bars of writing speed in tokens per second for DeepSeek V4.1 Flash, TensorFold 1.3.0 against TensorFold 1.3.3. Greedy code with replies of up to 2,048 tokens at a 4K prompt, 75.2 and 108.0. Greedy code with 512-token replies at 4K, 69.5 and 94.6. Greedy prose at 1K, 53.9 and 74.5. The model's own sampler on mixed text at 4K, 45.7 and 74.5.](findings/18_dsv41_tensorfold_133/chart_133.png)

</details>

### 17. [DeepSeek V4.1 Flash on TensorFold main at 1093b795, now in release 1.3.3](findings/17_dsv41_tensorfold_main_1093b795)

Runs of 22 Nov 2026. Now in a release. TensorFold 1.3.3 holds this change, and finding 18 is the run on the release. As written before the release. TensorFold main at 1093b795, not in a release yet, wrote 105.5 tok/s on DeepSeek V4.1 Flash at its max and 71.2 with the model's own sampler. TensorFold 1.3.0 wrote 74.5 and 44.6 on the same night, so main is 1.42 and 1.60 times as fast. It was faster on every same-text pair, 58 of 58 and 55 of 55, on two starts. The answers did not change. 250 of 250 short greedy answers match 1.3.0, and so do the replies to the author's own 16 prompts, greedy and sampled. On those 16 prompts I measured 102.3 tok/s, within 1% of the pull request's own table.

<details>
<summary>Chart</summary>

![Paired bars of writing speed in tokens per second for DeepSeek V4.1 Flash, TensorFold 1.3.0 against TensorFold main at 1093b795, which is in no release yet. Greedy code with replies of up to 2,048 tokens at a 4K prompt, 74.5 and 105.5. Greedy code with 512-token replies at 4K, 66.5 and 92.1. Greedy prose at 1K, 51.8 and 72.1. The model's own sampler on mixed text at 4K, 44.6 and 71.2.](findings/17_dsv41_tensorfold_main_1093b795/chart_main.png)

</details>

### 16. [Five models on oMLX 0.8.2, a version refresh](findings/16_omlx_082_refresh)

Runs of 21 and 22 Nov 2026. I see no speed change on oMLX 0.8.2 on any of the five models. Text by text against the earlier start, the middle ratio sits between 0.95 and 1.05 in every test. Hy4-flash oQ4h wrote the same text as on 0.8.1 on 100 of 100 short replies, and Qwen3.8 Flash Next full wrote the same answers as on 0.8.0 on 250 of 250. One line moved a lot by my own rule and I do not read it as a change. Inkling 2 Mini's max is 83.5, 88.5 and then 85.3 tok/s on three 0.8.2 starts against 96.3 on the 0.8.1 start, with overlapping ranges.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second, greedy at temperature 0, new code, replies of up to 2,048 tokens, 1K prompt, drafts on at the default depth. On oMLX 0.8.2 against the earlier start. GLM-5.3 Flash oQ4e 76.0 against 78.7. Hy4-flash oQ4h 76.8 against 75.6. Inkling 2 Mini, third start, 85.3 against 96.3. Inkling 2 Small 52.7 against 51.6. Qwen3.8 Flash Next full 50.8 against 49.4.](findings/16_omlx_082_refresh/chart_max.png)

</details>

### 15. [GLM-5.3 Flash, an all-4-bit build against a mixed 4-bit and 8-bit build](findings/15_glm53_flash_two_builds)

Runs of 21 Nov 2026. On TensorFold 1.3.2 with no drafts, TensorFold's all-4-bit build wrote 73.4 tok/s and the oQ4e build, which keeps 290 of its 419 tensors at 8 bits, wrote 50.9. oMLX 0.8.1 gave 72.5 and 51.7. With MTP drafts the all-4-bit build reached 102.0 tok/s at its max on TensorFold and oQ4e 82.9. The oQ4e build predicted fixed text slightly better, 0.4849 against 0.5079 nats a token, lower on 21 of 24 texts.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for two builds of GLM-5.3 Flash, greedy at temperature 0, new code, 512-token replies, 1K prompt. TensorFold with no drafts, 73.4 for the all-4-bit build and 50.9 for oQ4e. TensorFold with MTP drafts, 101.5 and 74.6. oMLX with no drafts, 72.5 and 51.7. oMLX with MTP drafts, 88.9 and 80.7.](findings/15_glm53_flash_two_builds/chart_builds.png)

</details>

### 14. [Inkling 2 Mini on oMLX 0.8.1, max and median speed](findings/14_inkling2_mini_omlx_081)

Runs of 21 Nov 2026. oMLX 0.8.1 wrote 96.3 tok/s on Inkling 2 Mini oQ4e at its max and 65.9 with the model's own sampler, on the day the model came out. With drafts off the same build wrote 54.5 and 54.4, so the drafts gave 1.8 times at the max. The smaller oQ3e build wrote 105.1 and 67.1. Every timed reply was reasoning text, though the request switched thinking off. The server held 16.6 GiB.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Inkling 2 Mini on oMLX 0.8.1, greedy at temperature 0, new code, replies of up to 2,048 tokens. oQ4e with drafts on 96.3 at a 1K prompt and 80.1 at 4K. oQ4e with drafts off 54.5 and 53.7. oQ3e with drafts on 100.6 and 105.1.](findings/14_inkling2_mini_omlx_081/chart_max.png)

</details>

### 13. [DeepSeek V4.1 Flash with 1 to 8 users on one Mac, mlx-serve 26.11.3](findings/13_dsv41_mlxserve_several_users)

Runs of 21 to 22 Nov 2026. One Mac wrote 55.5 to 57.4 tok/s for one user on DeepSeek V4.1 Flash at full precision on stock mlx-serve 26.11.3, and 115.0 to 116.2 tok/s in total with 8 users at once, about 15 each. Short open questions, 768-token replies, reasoning effort max, temperature 0, the test of a public two-Mac write-up. Every reply was reasoning text. With several users the drafts hardly landed. Added 22 Nov 2026. On a 3-bit pack, the one I take the write-up to have run on its one Studio, the same Mac wrote 61.1 to 69.8 tok/s for one user and 139.8 to 140.9 in total with 8 users, about 1.2 times the full-precision pack.

<details>
<summary>Chart</summary>

![Paired horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on mlx-serve 26.11.3 on one Mac. With 1 user, 55.5 in total and 56.4 each. With 2 users, 74.1 and 38.1. With 4 users, 97.0 and 25.0. With 8 users, 115.7 and 15.0.](findings/13_dsv41_mlxserve_several_users/chart_users.png)

</details>

### 12. [Tencent Hy4-flash on oMLX 0.8.1, with thinking off and on](findings/12_hy4_flash_omlx_081)

Runs of 21 Nov 2026. oMLX 0.8.1 wrote 75.6 tok/s on Hy4-flash oQ4h on new code with thinking switched off, and 53.7 with the model's own sampler. Those replies are answer text. With no thinking setting the model thinks, and oMLX wrote 54.4 and 54.0. Thinking off built the 46-token prompt the model's own chat template renders for it, and the replies I read back were clean. With drafts off the build wrote about 35 tok/s, so the drafts gave 2.1 to 2.2 times on answer text.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Hy4-flash oQ4h on oMLX 0.8.1, greedy at temperature 0, new code, replies of up to 2,048 tokens. With thinking off, 75.6 at a 1K prompt and 73.5 at 4K. With no thinking setting, 53.8 and 54.4.](findings/12_hy4_flash_omlx_081/chart_max.png)

</details>

### 11. [Three Qwen builds on TensorFold 1.3.2, a version refresh](findings/11_qwen38_tensorfold_132)

Runs of 21 Nov 2026. On TensorFold 1.3.2, on two server starts, Qwen3.8 27B 4-bit wrote 315.1 and 328.9 tok/s at its max and 157.4 and 161.3 with its own sampler. Qwen3.8 Flash Next 4-bit wrote 219.4 and 206.8, and the 6-bit build 199.8 and 200.1. On each build 250 of 250 short greedy answers match 1.3.0. On easy text Flash Next 4-bit wrote 7% faster than on 1.3.0 on both starts. The DeepSeek server did not compile at the 1.3.2 tag here, so that line stays on 1.3.0.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second on TensorFold 1.3.2, greedy at temperature 0, new code, replies of up to 2,048 tokens, the second of two server starts. Qwen3.8 27B 4-bit 328.9 at a 1K prompt and 241.6 at 4K. Qwen3.8 Flash Next 4-bit 206.8 and 194.6. Qwen3.8 Flash Next 6-bit 200.1 and 190.2.](findings/11_qwen38_tensorfold_132/chart_max.png)

</details>

### 10. [Tencent Hy4-flash on TensorFold 1.3.2, max and median speed](findings/10_hy4_flash_tensorfold_132)

Runs of 21 Nov 2026. At its defaults TensorFold 1.3.2 wrote 65.3 and then 64.6 tok/s on Hy4-flash 4-bit at its max, on a morning and an evening start, and 50.8 and 47.6 on the 8-bit build, with thinking on. One switch from the engine's source, TF_HY4_DRAFT_BITS=8, was faster on every code text on both builds on two starts each. Against the default start of the same evening it wrote 71.5 against 64.6 on the 4-bit build and 53.4 against 47.6 on the 8-bit build, with the same text on 100 of 100 short replies. With drafts off the builds wrote 42.2 and 34.0 on code. Nearly every timed reply was reasoning text. With thinking switched off through the API the replies went off course on both builds, so there is no thinking-off line.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second for Hy4-flash on TensorFold 1.3.2, greedy at temperature 0, new code, thinking on, replies of up to 2,048 tokens, at the defaults and with TF_HY4_DRAFT_BITS=8. The 4-bit build writes 64.6 and 71.5 at a 1K prompt, and 60.4 and 70.7 at 4K. The 8-bit build writes 47.6 and 53.4 at 1K, and 46.8 and 52.0 at 4K.](findings/10_hy4_flash_tensorfold_132/chart_max.png)

</details>

### 9. [Four more models on oMLX 0.8.0, max and median speed](findings/09_omlx_080_four_models)

Runs of 20 to 21 Nov 2026. On oMLX 0.8.0, GLM-5.3 Flash 4-bit wrote 80.2 tok/s at its max and 67.8 with its own sampler. Inkling 2 Small wrote 51.6 and 42.2. Qwen3.8 Flash Next at full precision wrote 53.6 with draft depth fixed at 4, 49.4 at the default, and 33.6 and 33.2 with its own sampler. GLM-5.3 4-bit wrote 24.6 and 24.5. Three of the four wrote reasoning text.

<details>
<summary>Chart</summary>

![Bars of writing speed in tokens per second on oMLX 0.8.0, greedy at temperature 0, new code, replies of up to 2,048 tokens. GLM-5.3 Flash 4-bit 80.2 at a 1K prompt and 74.7 at 4K. Inkling 2 Small 51.6 and 48.6. Qwen3.8 Flash Next full at the default depth 49.3 and 48.9.](findings/09_omlx_080_four_models/chart_max.png)

</details>

### 8. [DeepSeek V4.1 Flash on mlx-serve 26.11.3, pushing the max](findings/08_dsv41_mlxserve_26113)

Runs of 20 Nov 2026. mlx-serve 26.11.3 wrote 93.8 and 95.3 tok/s on the Lossless pack on two starts, on new code at its defaults with replies of up to 2,048 tokens at a 4K prompt. With the model's own sampler it wrote 57.5. With the output head kept dense, one start wrote 91.6 on the same code test and 57.9 sampled, and 179 of 250 short greedy answers matched the default start. Copying the prompt it wrote 167.0 and counting from 1 it wrote 121.5. The defaults are not bit-exact, by the server log. Qwen3.8 27B full wrote 6.8 tok/s sampled on one start.

<details>
<summary>Chart</summary>

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on mlx-serve 26.11.3 at its defaults, greedy at temperature 0. At a 1K prompt, 91.9 writing new code, 167.0 copying the prompt and 121.4 counting from 1. At a 4K prompt, 93.8, 162.3 and 121.5.](findings/08_dsv41_mlxserve_26113/chart_tasks.png)

</details>

### 7. [Qwen3.8 27B and Flash Next on TensorFold 1.3.0, pushing the max](findings/07_qwen38_tensorfold_130)

Runs of 20 Nov 2026. TensorFold 1.3.0 wrote 331.3 tok/s on Qwen3.8 27B 4-bit on new code with replies of up to 2,048 tokens at a 1K prompt, 7.3 times `mlx-lm` 0.32.2 on the same weights, and 148.2 with the model's own sampler at 4K, 3.4 times. Copying the prompt it wrote 824.0. Flash Next 4-bit wrote 204.4, 126.7 sampled and 292.2 copying. Flash Next 6-bit wrote 193.0 and 117.4 sampled.

<details>
<summary>Chart</summary>

![Horizontal bars of writing speed in tokens per second for Qwen3.8 27B 4-bit, greedy at temperature 0. At a 1K prompt, mlx-lm 0.32.2 writes 45.1 on new code, TensorFold 1.3.0 writes 331.3 on new code and 841.0 copying the prompt. At a 4K prompt, 44.2, 250.8 and 659.1.](findings/07_qwen38_tensorfold_130/chart_27b.png)

</details>

### 6. [DeepSeek V4.1 Flash on TensorFold 1.3.0, pushing the max](findings/06_dsv41_tensorfold_130_max_push)

Runs of 20 Nov 2026. At its defaults TensorFold 1.3.0 wrote 76.4 and 75.6 tok/s on two starts on new code with replies of up to 2,048 tokens at a 4K prompt. With 512-token replies at a 1K prompt it wrote 159.1 tok/s copying the prompt and 106.9 counting from 1. None of six draft settings separated from the defaults, with cell medians at 0.95 to 1.06 times.

<details>
<summary>Chart</summary>

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on TensorFold 1.3.0 with drafts at defaults, greedy at temperature 0. At a 1K prompt, 74.1 writing new code, 159.1 copying the prompt and 106.9 counting from 1. At a 4K prompt, 76.4, 146.3 and 105.3.](findings/06_dsv41_tensorfold_130_max_push/chart_tasks.png)

</details>

### 5. [DeepSeek V4.1 Flash on oMLX 0.8.0, pushing the max](findings/05_dsv41_omlx_080_max_push)

Runs of 20 Nov 2026. With draft depth fixed at 5 and replies of up to 2,048 tokens, oMLX 0.8.0 wrote 84.1 and 81.3 tok/s on new code at a 1K prompt on two starts, against 77.2 and 76.2 at the default depth. With 512-token replies at a 4K prompt the same setting wrote 118.3 tok/s copying the prompt and 114.0 counting from 1. With the model's own sampler fixed depth 5 was slower, 50.5 against 57.9 tok/s.

<details>
<summary>Chart</summary>

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on oMLX 0.8.0 with draft depth fixed at 5, greedy at temperature 0. At a 1K prompt, 84.1 writing new code, 114.7 copying the prompt and 113.0 counting from 1. At a 4K prompt, 82.7, 118.3 and 114.0.](findings/05_dsv41_omlx_080_max_push/chart_tasks.png)

</details>

### 4. [DeepSeek V4.1 Flash on TensorFold 1.3.0 against 1.2.10](findings/04_dsv41_tensorfold_130)

Runs of 20 Nov 2026. On two server starts each, in both orders, TensorFold 1.3.0 read prompts 3% to 11% faster than 1.2.10 and wrote at the same speed with drafts on, 70.5 against 69.5 tok/s greedy on code. 17 of 68 replies on 1.3.0 held one pause of 0.25 to 0.58 s, and none did on 1.2.10. With drafts off, on one start each, 1.3.0 wrote 40.5 tok/s against 44.7.

<details>
<summary>Chart</summary>

![Horizontal bars of prefill speed in tokens per second for DeepSeek V4.1 Flash on TensorFold at 1K, 4K and 32K prompts. Version 1.2.10 reads 662.0, 986.4 and 1,334.1. Version 1.3.0 reads 707.8, 1,042.4 and 1,379.8.](findings/04_dsv41_tensorfold_130/chart_prefill.png)

</details>

### 3. [DeepSeek V4.1 Flash on oMLX 0.8.0, max and median speed](findings/03_dsv41_omlx_080)

Runs of 20 Nov 2026. oMLX 0.8.0 wrote 71.2 tok/s on DeepSeek V4.1 Flash oQ4e-mtp, greedy on code at its default draft depth, and 56.5 with the model's own sampler on mixed text. Deeper draft settings gave 65.8 to 78.7, inside the noise between server starts.

<details>
<summary>Chart</summary>

![Horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on oMLX 0.8.0 at 1K, 4K and 32K prompts, greedy at temperature 0 on code. With 128-token replies, 58.2, 61.3 and 55.4. With 512-token replies, 71.2, 69.5 and 69.4.](findings/03_dsv41_omlx_080/chart_decode.png)

</details>

### 2. [Ten open-weight models, from 4K to 1M tokens](findings/02_ten_models_4k_to_1m)

Runs of 16 to 18 Nov 2026. Qwen3.8 Flash Next 4-bit wrote 124.1 tok/s at a 128K prompt and 93.2 at 1M. DeepSeek V4.1 Flash 1017 Lossless wrote 55.0 to 58.3 tok/s at every length from 4K to 1M.

<details>
<summary>Chart</summary>

![Ten small line charts of prefill speed in tokens per second at 4K, 32K, 128K, 512K and 1M prompts. Qwen3.8 Flash Next reads fastest at every size, 4,046.2 at 4K on the 4-bit build and 2,705.6 at 1M on the BF16 build. DeepSeek V4.1 Flash reads 2,851.8 at 4K and 1,642.7 at 1M. GLM-5.3 4-bit reads 645.7 at 4K. The two Qwen3.8 27B builds are shown up to 128K only.](findings/02_ten_models_4k_to_1m/chart_prefill.png)

</details>

### 1. [TensorFold with a draft model on Qwen3.8-27B 4-bit](findings/01_tensorfold_qwen38-27b_4bit)

Runs of 13 Nov 2026. TensorFold 1.2.7 with the DFlash2 draft wrote 145.7 tok/s at a 1K prompt. `mlx-lm` 0.32.2 wrote 44.5 on the same weights. That is 3.3 times.

<details>
<summary>Chart</summary>

![Bar chart of writing speed for Qwen3.8-27B 4-bit on a Mac Studio M5 Ultra 512 GB, one user. At a 1K prompt, mlx-lm 0.32.2 writes 44.5 tokens per second, TensorFold 1.2.7 with no draft model writes 48.7, and TensorFold 1.2.7 with the DFlash2 draft model writes 145.7. At a 32K prompt the three write 39.5, 43.4 and 118.7.](findings/01_tensorfold_qwen38-27b_4bit/card.png)

</details>

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

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
