# Finding 2. Ten open-weight models on one Mac Studio M5 Ultra 512 GB, from 4K to 1M tokens

ELI5: I ran ten popular open-weight model builds on one Mac, each at the best setup I found for it. For each I timed how fast it reads the prompt, how fast it writes the reply, how long you wait for the first word and how much memory it takes, at prompts from 4K to 1M tokens. Then I picked the fastest model that is smart enough and the smartest model that is fast enough.

**Qwen3.8 Flash Next 4-bit was the fastest of the models scoring 28 or more on the Artificial Analysis Intelligence Index. It wrote 124.1 tok/s at a 128K prompt and 93.2 at 1M. DeepSeek V4.1 Flash 1017 has the top index score of the ten and wrote 55.0 to 58.3 tok/s at every prompt length from 4K to 1M. Both scores are with thinking on, and I timed both models with thinking off. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs up to 128K and of 3 at 512K and 1M, 16 to 18 Nov 2026.**

## Charts

ELI5: Four pictures of the same results. How fast each model reads and writes as the prompt grows, how long you wait at 1M, and how much memory it takes.

![Ten small line charts of prefill speed in tokens per second at 4K, 32K, 128K, 512K and 1M prompts. Qwen3.8 Flash Next reads fastest at every size, 4,046.2 at 4K on the 4-bit build and 2,705.6 at 1M on the BF16 build. DeepSeek V4.1 Flash reads 2,851.8 at 4K and 1,642.7 at 1M. GLM-5.3 4-bit reads 645.7 at 4K. The two Qwen3.8 27B builds are shown up to 128K only.](chart_prefill.png)

![Ten small line charts, one per model, of decode speed in tokens per second at prompts of 4K, 32K, 128K, 512K and 1M tokens on a Mac Studio M5 Ultra 512 GB. DeepSeek V4.1 Flash holds 58.3 to 55.3. GLM-5.3 4-bit writes 24.3 to 21.0 and is out of memory from 512K. GLM-5.3 Flash 6-bit falls from 57.8 to 38.7 and the 4-bit from 68.8 to 45.2. Inkling 2 Small falls from 41.3 to 26.1 and is out of memory from 512K. Qwen3.8 27B 4-bit falls from 154.2 to 78.5 by 128K and the BF16 build holds 8.8 to 9.2, both shown up to 128K only. Qwen3.8 Flash Next falls from 129.2 to 93.2 at 4-bit, 114.0 to 85.4 at 6-bit and 34.9 to 25.6 at BF16.](chart_decode.png)

![Horizontal bars of seconds to the first token for a 1M-token prompt. DeepSeek V4.1 Flash 612.3 s, 10.2 minutes. GLM-5.3 Flash 6-bit 729.7 s and 4-bit 654.6 s. Qwen3.8 Flash Next 378.3 s at 4-bit, 410.4 s at 6-bit and 354.0 s at BF16. GLM-5.3 and Inkling 2 Small were out of memory at 512K, so 1M was not tried. The two Qwen3.8 27B builds are not shown at 1M.](chart_first_token_1m.png)

![Paired horizontal bars of peak wired memory in GiB at a 128K prompt and a 1M prompt, against the Mac's 512 GiB. DeepSeek V4.1 Flash 305.5 and 328.4. GLM-5.3 4-bit 423.1 at 128K. GLM-5.3 Flash 6-bit 259.0 and 281.6, 4-bit 186.1 and 211.4. Inkling 2 Small 428.4 at 128K. Qwen3.8 27B 4-bit 215.7 and BF16 89.8 at 128K, not shown at 1M. Qwen3.8 Flash Next 4-bit 173.6 and 170.3, 6-bit 215.7 and 212.8, BF16 355.3 and 398.5.](chart_memory.png)

## All results

ELI5: Every model at every prompt size, in one table. Each line is the middle of its runs, 5 runs up to 128K and 3 at 512K and 1M.

- One user, 512-token replies. Each prompt size ran as its own block.
- "Engine and setup" is on each model's first line. Every server opened a 1,048,576-token window at 512K and 1M. A note on the 512K line marks a model whose setup changed.
- Peak memory is the highest block peak across the runs. Prompt tokens differ by model because each tokenizer cuts the same text differently.

<!-- table:start -->
| Model | Engine and setup | Prompt | Prompt tokens | Prefill tok/s | Decode tok/s | First token s | Peak memory GiB | Runs |
|---|---|---|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | mlx-serve 26.11.2, defaults, prompt lookup drafts on | 4K | 3,934 to 4,390 | 2,851.8 | 58.3 | 1.5 | 299.7 | 5 |
|  |  | 32K | 29,689 to 33,911 | 3,828.3 | 57.0 | 8.5 | 301.8 | 5 |
|  |  | 128K | 120,330 to 126,048 | 3,141.0 | 56.3 | 39.1 | 305.5 | 5 |
|  |  | 512K | 512,577 to 516,045 | 2,463.8 | 55.0 | 209.2 | 315.0 | 3 |
|  |  | 1M | 1,005,817 to 1,012,809 | 1,642.7 | 55.3 | 612.3 | 328.4 | 3 |
| GLM-5.3, 4-bit | oMLX 0.7.3 with its kernels, MTP off | 4K | 3,738 to 4,327 | 645.7 | 24.3 | 6.0 | 402.1 | 5 |
|  |  | 32K | 28,275 to 32,422 | 465.4 | 23.7 | 63.7 | 407.4 | 5 |
|  |  | 128K | 118,894 to 124,624 | 402.0 | 21.0 | 304.3 | 423.1 | 5 |
|  |  | 512K | out of memory | | | | | |
|  |  | 1M | not tried, 512K was out of memory | | | | | |
| GLM-5.3 Flash, 6-bit | oMLX 0.7.3 with its kernels, MTP on | 4K | 3,739 to 4,328 | 1,858.8 | 57.8 | 2.1 | 255.5 | 5 |
|  |  | 32K | 28,274 to 32,422 | 1,925.6 | 55.1 | 16.3 | 257.8 | 5 |
|  |  | 128K | 118,896 to 124,622 | 1,535.3 | 52.9 | 79.6 | 259.0 | 5 |
|  |  | 512K | 489,298 to 494,205 | 1,638.9 | 48.1 | 301.6 | 272.2 | 3 |
|  |  | 1M | 964,348 to 973,607 | 1,325.8 | 38.7 | 729.7 | 281.6 | 3 |
| GLM-5.3 Flash, 4-bit | oMLX 0.7.3 with its kernels, MTP on | 4K | 3,740 to 4,328 | 2,172.9 | 68.8 | 1.8 | 183.6 | 5 |
|  |  | 32K | 28,274 to 32,422 | 2,249.1 | 70.0 | 14.0 | 184.4 | 5 |
|  |  | 128K | 118,894 to 124,624 | 2,136.3 | 65.6 | 57.5 | 186.1 | 5 |
|  |  | 512K | 489,298 to 494,207 | 1,794.1 | 54.6 | 275.5 | 197.7 | 3 |
|  |  | 1M | 964,343 to 973,605 | 1,478.0 | 45.2 | 654.6 | 211.4 | 3 |
| Inkling 2 Small | oMLX main 624cff0e with its kernels, DSpark draft on | 4K | 4,941 to 5,630 | 1,176.4 | 41.3 | 4.3 | 331.8 | 5 |
|  |  | 32K | 38,090 to 42,838 | 1,115.1 | 39.1 | 36.3 | 360.2 | 5 |
|  |  | 128K | 159,291 to 163,988 | 648.3 | 26.1 | 253.0 | 428.4 | 5 |
|  |  | 512K | out of memory | | | | | |
|  |  | 1M | not tried, 512K was out of memory | | | | | |
| Qwen3.8 27B, 4-bit | TensorFold 1.2.8, DFlash2 drafter (z-lab) | 4K | 4,138 to 4,900 | 1,863.1 | 154.2 | 2.3 | 70.8 | 5 |
|  |  | 32K | 30,925 to 36,234 | 1,679.9 | 112.2 | 19.9 | 102.1 | 5 |
|  |  | 128K | 131,394 to 138,444 | 990.5 | 78.5 | 136.8 | 215.7 | 5 |
|  |  | 512K | not shown, no documented setup past 262,144 tokens | | | | | |
|  |  | 1M | not shown, no documented setup past 262,144 tokens | | | | | |
| Qwen3.8 27B, full | mlx-serve 26.11.2, defaults, prompt lookup drafts on | 4K | 4,139 to 4,901 | 1,866.9 | 8.8 | 2.3 | 64.4 | 5 |
|  |  | 32K | 30,927 to 36,232 | 1,617.7 | 8.8 | 20.7 | 80.2 | 5 |
|  |  | 128K | 131,395 to 138,444 | 1,127.5 | 9.2 | 120.5 | 89.8 | 5 |
|  |  | 512K | not shown, no documented setup past 262,144 tokens | | | | | |
|  |  | 1M | not shown, no documented setup past 262,144 tokens | | | | | |
| Qwen3.8 Flash Next, 4-bit | TensorFold 1.2.8, MTP on, recipe line | 4K | 4,137 to 4,903 | 4,046.2 | 129.2 | 1.1 | 167.9 | 5 |
|  |  | 32K | 30,928 to 36,233 | 4,482.6 | 122.3 | 7.5 | 175.6 | 5 |
|  |  | 128K | 131,395 to 138,446 | 4,226.2 | 124.1 | 32.1 | 173.6 | 5 |
|  |  | 512K | 542,186 to 547,357 | 3,441.1 | 109.6 | 159.1 | 170.8 | 3 |
|  |  | 1M | 956,904 to 967,811 | 2,529.3 | 93.2 | 378.3 | 170.3 | 3 |
| Qwen3.8 Flash Next, 6-bit | TensorFold 1.2.8, MTP on, recipe line | 4K | 4,141 to 4,902 | 3,821.0 | 114.0 | 1.1 | 211.1 | 5 |
|  |  | 32K | 30,928 to 36,234 | 4,217.6 | 116.0 | 8.0 | 213.7 | 5 |
|  |  | 128K | 131,393 to 138,448 | 3,786.5 | 107.7 | 36.5 | 215.7 | 5 |
|  |  | 512K | 542,184 to 547,359 | 3,046.0 | 102.1 | 179.7 | 212.7 | 3 |
|  |  | 1M | 956,906 to 967,811 | 2,331.7 | 85.4 | 410.4 | 212.8 | 3 |
| Qwen3.8 Flash Next, full | oMLX 0.7.3 with its kernels, MTP on (built-in head) | 4K | 4,140 to 4,901 | 3,076.8 | 34.9 | 1.4 | 345.8 | 5 |
|  |  | 32K | 30,927 to 36,234 | 3,576.4 | 34.9 | 9.7 | 350.2 | 5 |
|  |  | 128K | 131,397 to 138,445 | 3,711.0 | 29.9 | 36.6 | 355.3 | 5 |
|  | same oMLX, window raised to 1,048,576, YaRN x4 | 512K | 542,188 to 547,358 | 3,223.9 | 27.7 | 169.5 | 378.0 | 3 |
|  |  | 1M | 956,902 to 967,811 | 2,705.6 | 25.6 | 354.0 | 398.5 | 3 |
<!-- table:end -->

## The short answer

ELI5: "Fast" is what this Mac measured. "Smart" is a public leaderboard score, because I didn't test answer quality myself. I drew "smart enough" at 28 on the index and "fast enough" at 50 tok/s.

| Question | Pick | Index, scored with thinking on | Thinking when timed | Decode tok/s, 4K / 128K / 1M | Prefill tok/s, 4K / 128K / 1M | First token s, 4K / 128K / 1M | Peak memory GiB, 4K / 128K / 1M |
|---|---|---|---|---|---|---|---|
| Fastest at 28 or more | Qwen3.8 Flash Next, 4-bit | 29 | off | 129.2 / 124.1 / 93.2 | 4,046.2 / 4,226.2 / 2,529.3 | 1.1 / 32.1 / 378.3 | 167.9 / 173.6 / 170.3 |
| Next fastest | Qwen3.8 Flash Next, 6-bit | 29 | off | 114.0 / 107.7 / 85.4 | 3,821.0 / 3,786.5 / 2,331.7 | 1.1 / 36.5 / 410.4 | 211.1 / 215.7 / 212.8 |
| Smartest at 50 tok/s or more | DeepSeek V4.1 Flash 1017, Lossless | 33 | off | 58.3 / 56.3 / 55.3 | 2,851.8 / 3,141.0 / 1,642.7 | 1.5 / 39.1 / 612.3 | 299.7 / 305.5 / 328.4 |
| Next smartest | GLM-5.3 Flash, 6-bit | 28 | on, every reply | 57.8 / 52.9 / 38.7 | 1,858.8 / 1,535.3 / 1,325.8 | 2.1 / 79.6 / 729.7 | 255.5 / 259.0 / 281.6 |

- **The 28 line.** The ten score 33, 32, 31, 29, 28 and 20 on the index. The gap from 28 to 20 is the biggest, so I drew the line there. Only the two Qwen3.8 27B builds fall under it.
- **GLM-5.3 (32) and Inkling 2 Small (31) score above DeepSeek's runner-up.** They wrote 21.0 to 24.3 and 26.1 to 41.3 tok/s, under the 50 line.
- **GLM-5.3 Flash 6-bit stays above 50 tok/s up to 128K.** It wrote 48.1 at 512K and 38.7 at 1M. The 4-bit build wrote 54.6 at 512K and 45.2 at 1M.
- **Qwen3.8 27B 4-bit is the fastest writer at 4K,** 154.2 tok/s, but it scores 20 and Flash Next 4-bit passes it from 32K up (122.3 against 112.2 at 32K, 124.1 against 78.5 at 128K).
- **Thinking.** The index scores every one of these models with thinking on. I timed DeepSeek and the Qwen models with thinking off. With thinking off the index gives DeepSeek V4.1 Flash 19 and Qwen3.8 27B 10, and lists no thinking-off score for Flash Next. The GLM and Inkling models think on every reply, so their score and their speed come from the same mode.
- **Quantization.** The index scores each model as its makers or providers serve it, not the 4-bit and 6-bit files here. DeepSeek's Lossless weights are the precision DeepSeek ships.

## The setups

ELI5: Every model got one engine, one set of weights and one sampler for all of its prompt sizes up to 128K. The engine is the one that ran it best here. The two Qwen3.8 27B builds stop at 128K, because their engines here serve them to 262,144 tokens.

| Model | Weights @ commit | Precision | Engine | Setup | Sampling |
|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | [ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless](https://huggingface.co/ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless) @ 85002f89 | FP4 experts, FP8 rest, as DeepSeek ships | mlx-serve 26.11.2 | defaults, prompt lookup drafts on | temperature 1.0, top-p 1.0 |
| GLM-5.3, 4-bit | [mlx-community/GLM-5.3-4bit](https://huggingface.co/mlx-community/GLM-5.3-4bit) @ 81ad9b73 | 4-bit | oMLX 0.7.3 with its kernels | MTP off | temperature 1.0, top-p 0.95 |
| GLM-5.3 Flash, 6-bit | [Jundot/GLM-5.3-Flash-oQ6e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ6e-mtp) @ 51a9c6ce | oQ6e | oMLX 0.7.3 with its kernels | MTP on | temperature 1.0, top-p 0.95 |
| GLM-5.3 Flash, 4-bit | [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) @ 9e5c75a9 | oQ4e | oMLX 0.7.3 with its kernels | MTP on | temperature 1.0, top-p 0.95 |
| Inkling 2 Small | [mlx-community/Inkling-2-Small-oQ4e](https://huggingface.co/mlx-community/Inkling-2-Small-oQ4e) @ 973d9f96 | oQ4e | oMLX main 624cff0e with its kernels | DSpark draft on | temperature 1.0, top-p 1.0 |
| Qwen3.8 27B, 4-bit | [TensorFold/Qwen3.8-27B-MLX-4bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) @ 22d8d538 | 4-bit | TensorFold 1.2.8 | DFlash2 drafter ([z-lab/Qwen3.8-27B-DFlash2](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2)) | temperature 0.7, top-p 0.8, top-k 20 |
| Qwen3.8 27B, full | [mlx-community/Qwen3.8-27B-bf16](https://huggingface.co/mlx-community/Qwen3.8-27B-bf16) @ 379e7084 | BF16 | mlx-serve 26.11.2 | defaults, prompt lookup drafts on | temperature 0.7, top-p 0.8, top-k 20, presence-penalty 1.5 |
| Qwen3.8 Flash Next, 4-bit | [TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP) @ 2b170fa6 | 4-bit | TensorFold 1.2.8 | MTP on, recipe line | temperature 0.7, top-p 0.8, top-k 20 |
| Qwen3.8 Flash Next, 6-bit | [TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP) @ 45032a19 | 6-bit | TensorFold 1.2.8 | MTP on, recipe line | temperature 0.7, top-p 0.8, top-k 20 |
| Qwen3.8 Flash Next, full | [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) @ 812d96e1 | BF16 | oMLX 0.7.3 with its kernels | MTP on (built-in head) | temperature 0.7, top-p 0.8, top-k 20 |

- **Sampling** is each maker's recommended setting, sent with every request. Thinking was off for DeepSeek and Qwen, through each engine's `enable_thinking: false` request switch. The GLM and Inkling templates ignore that switch and think on every reply.
- **"With its kernels"** means oMLX built from its source with `OMLX_WITH_CUSTOM_KERNEL=1`, the switch its README documents for source installs.
- **oMLX main 624cff0e** is an unreleased commit of 13 Nov 2026. It holds the Inkling 2 Small support, which no tagged release had on 16 Nov. Its version string still reads 0.8.0rc1.
- **Engines had no network.** Each ran under `sandbox-exec` with only this Mac reachable.

Serve commands. These are the harness's templates from `engines.json`, filled with the window and slots each job passed. `MODEL` is the weights folder, `MODELS` the folder of all weights, `DRAFT` the DFlash2 folder, `NAME` any model name and `PORT` any free port.

mlx-serve 26.11.2, DeepSeek with `CTX` 131072 up to 128K and 1048576 for 512K and 1M, Qwen3.8 27B full with 262144.

```bash
mlx-serve --model MODEL --serve --host 127.0.0.1 --port PORT --ctx-size CTX --max-concurrent 1
```

oMLX 0.7.3 with its kernels, and oMLX main 624cff0e for Inkling. Per-model switches (MTP, DSpark, `max_context_window`) live in oMLX's own `model_settings.json`, as listed in the setups table.

```bash
omlx serve --model-dir MODELS --host 127.0.0.1 --port PORT --max-concurrent-requests 1 --headless --no-hf-cache
```

TensorFold 1.2.8, Qwen3.8 27B 4-bit with the DFlash2 drafter.

```bash
tensorfold serve MODEL --name NAME --host 127.0.0.1 --port PORT --context 262144 --parallel 1 --drafter DRAFT
```

TensorFold 1.2.8, Qwen3.8 Flash Next 4-bit and 6-bit. This is the M5 Ultra line in TensorFold's own Flash Next recipe. The server's `--temperature 0` is a default, and every request carries its own sampler.

```bash
tensorfold serve MODEL --name NAME --host 127.0.0.1 --port PORT --context 1048576 --parallel 2 --vision --prompt-cache-gib 8 --temperature 0 --no-update-check
```

## How I measured

ELI5: Same text, same harness and same Mac for every model. Only the engine and the weights change.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Text.** Open-source docs and code mixed in blocks of about 2,000 characters of prose and 6,000 of code. Each run gets new text, and each prompt starts with a new session line so no prompt cache can hit. In `rows.csv` every timed request at 512K and 1M shows 0 cached tokens, and none up to 128K shows more than 3.
- **Sizes.** "4K", "32K" and "128K" are 14,336, 114,688 and 458,752 characters, at 3.5 characters per target token. Each tokenizer cuts that into a different count, so the table shows the real prompt tokens. DeepSeek's 128K target is 126,000 so its reply fits its 131,072-token window. The 1M text is cut a little shorter for each tokenizer so prompt and reply fit in 1,048,576 tokens.
- **Replies.** 512 tokens, one user at a time. Every timed reply ran to the 512-token cap.
- **Repeats.** 4K to 128K, 5 timed runs per size, each size its own block. Each server start had one warm-up request before its first block, at 1K for the runs of 16 Nov and at 4K for those of 17 Nov. 512K and 1M, 3 runs. Run 1 came on its own server start after a 4K warm-up. Runs 2 and 3 came back to back on a second start, also after a 4K warm-up.
- **Prefill** is prompt tokens over the time to the first token. **Decode** is tokens per second from the first reply token to the last. **First token** is seconds from sending the request.
- **Memory** is the whole Mac's wired memory, sampled every 5 seconds, peak within each block. It includes macOS (about 8 GiB idle) and any cache the engine keeps. A watchdog would stop any run past 460 GiB wired. It never fired in these runs.
- **Dates.** 4K to 128K on 16 and 17 Nov 2026. 512K and 1M from 17 Nov 2026 to 02:18 SGT 18 Nov 2026.
- **Mixed dates.** Some 4K blocks ran on 17 Nov beside 32K and 128K blocks from 16 Nov. They sit together only where engine, version, weights, sampler and settings line all match, and the table builder stops if they don't.

## How much the runs varied

ELI5: A median hides how much the runs moved. Spread is the gap between the highest and lowest run, divided by the median.

- **Prefill, 4K to 128K.** The middle cell varied 3.9%. The widest was GLM-5.3 Flash 4-bit at 4K, 26.8%, from one slow run (1,607.2 against 2,168.6 to 2,188.8).
- **Decode, 4K to 128K.** The middle cell varied 12.0%, because drafts make decode swing. The widest was Qwen3.8 27B 4-bit at 4K, 136.9 to 219.4 tok/s around a median of 154.2. (219.4 − 136.9) ÷ 154.2 = 53.5%.
- **512K and 1M.** The middle of the 12 cells varied 4.9% in prefill and 6.0% in decode. The widest prefill was GLM-5.3 Flash 6-bit at 512K, (1,741.8 − 1,474.2) ÷ 1,638.9 = 16.3%. The widest decode was the same model at 1M, (44.2 − 37.8) ÷ 38.7 = 16.5%.
- **The last long run read slowest in 10 of 12 cells,** even where its text was shorter. On Flash Next 6-bit at 512K it had 545,050 tokens against 547,359 and still read at 2,886.0 tok/s against 3,046.0. I haven't found why.

## Things to know before you compare rows

ELI5: These are ten different models doing ten different jobs. A row is a reference point, not a race.

- **Thinking speed.** GLM-5.3, GLM-5.3 Flash and Inkling 2 Small think on every reply, so their decode figure is thinking speed. Qwen and DeepSeek ran with thinking off.
- **Drafts.** Most rows decode with a draft, MTP, DFlash2, DSpark or prompt lookup. Drafts win more on predictable text and with greedy sampling. On greedy prose Flash Next 6-bit wrote about 125 tok/s, and on code 150 to 185, in an earlier run on the same engine.
- **Qwen3.8 27B 4-bit at 128K.** Memory held near 115 GiB for four of the five runs, then reached 215.7 GiB on the last. TensorFold's prompt cache defaults to half the free room on a Mac.
- **Qwen3.8 27B full.** `mlx-lm` 0.32.2, mlx-serve 26.11.2 and oMLX 0.7.3 wrote 8.5, 8.7 and 8.4 tok/s at 4K, 3 runs each. The engine pick there is a near tie. Dense BF16 weights read 54.7 GB per token.
- **Qwen3.8 Flash Next full.** On oMLX its built-in MTP head doubled decode at 4K, 33.0 tok/s on against 16.0 off.
- **Qwen3.8 27B at 512K and 1M is not shown.** TensorFold serves the 27B up to 262,144 tokens, and I didn't try mlx-serve past that. I have no documented setup for it past 262,144 tokens to stand behind.
- **GLM-5.3 and Inkling 2 Small at 512K.** oMLX's prefill memory guard refused the prompt before reading it. It estimated about 434.2 GB at peak for GLM-5.3 and 436.6 GB for Inkling, against a limit of about 432 GB. That limit follows the Mac's GPU memory setting, which stayed the same for every row. So I didn't try 1M on either.
- **YaRN.** Qwen's configs give these models a native window of 262,144 tokens. Both engines stretch it with YaRN x4 for the whole load once the window is set past that. So TensorFold's Flash Next rows ran with YaRN at every size, because its recipe line opens 1,048,576. The Flash Next full row up to 128K ran at 262,144 without it. Qwen's model card says Flash Next extends to 1,000,000 tokens with YaRN.
- **oMLX 0.8.0rc1.** Its release notes say prefill is 43 to 48% faster on M5 Ultra. The oMLX rows here use 0.7.3, except Inkling on main 624cff0e. I haven't tested 0.8.0rc1 on the others.
- **Not tested here.** Answer quality, and more than one user at a time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`table.csv`.** 194 lines. One per timed request behind the tables, plus four out-of-memory cells and four not-shown cells. Column `table` is `short` for 4K to 128K and `long` for 512K and 1M. Each line carries model, weights, commit, engine, setup, prompt tokens, prefill, decode, first token, peak memory, run id, row id and sampler.
- **`rows.csv`.** 198 raw rows from the bench database. The 186 timed rows, the 10 warm-ups that ran at 4K inside the 4K blocks, and the two refused 512K requests. Warm-ups at other sizes are not in it.
- **`runs.csv`.** The 28 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/02_ten_models_4k_to_1m
```

It prints one line per run and prompt size with the median and range of decode and first token.

Run ids, 4K to 128K.

| Model | 4K | 32K and 128K |
|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | `a227c80d0e61` | `e95e5016b53d` |
| GLM-5.3, 4-bit | `626f0c1b4ad9` | `265e9e285991` |
| GLM-5.3 Flash, 6-bit | `2b64d54e7e5c` | `964c1f183722` |
| GLM-5.3 Flash, 4-bit | `8453ec3a372d` | `8453ec3a372d` |
| Inkling 2 Small | `5c4d781c0e3d` | `56377d0e6662` |
| Qwen3.8 27B, 4-bit | `a798cea8b67e` | `a798cea8b67e` |
| Qwen3.8 27B, full | `a30a665ca3ee` | `a30a665ca3ee` |
| Qwen3.8 Flash Next, 4-bit | `72fae37b87f0` | `72fae37b87f0` |
| Qwen3.8 Flash Next, 6-bit | `ea26b8919e88` | `ea26b8919e88` |
| Qwen3.8 Flash Next, full | `c4bbe7d3230c` | `c4bbe7d3230c` |

Run ids, 512K and 1M. Run 1, then runs 2 and 3.

| Model | Run 1 | Runs 2 and 3 |
|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | `5c553da26d08` | `457c24009db2` |
| GLM-5.3, 4-bit | `f8c2b1de245c`, refused | not run |
| GLM-5.3 Flash, 6-bit | `f845e7f1ff23` | `18a2c4ba29f9` |
| GLM-5.3 Flash, 4-bit | `348625c0d228` | `4954126b4c84` |
| Inkling 2 Small | `80f0bda26328`, refused | not run |
| Qwen3.8 27B, 4-bit | not shown | not shown |
| Qwen3.8 27B, full | not shown | not shown |
| Qwen3.8 Flash Next, 4-bit | `4b8c48246a51` | `de80c99ea350` |
| Qwen3.8 Flash Next, 6-bit | `86931c954655` | `11ca2b8aeea1` |
| Qwen3.8 Flash Next, full | `e9b5dd72aee1` | `705239342a6f` |

## The index scores

Artificial Analysis Intelligence Index, from [artificialanalysis.ai](https://artificialanalysis.ai/leaderboards/models) and each model's page there, read 18 Nov 2026 from 17:17 to 17:40 SGT.

| Model | Score | Mode |
|---|---|---|
| DeepSeek V4.1 Flash 1017 | 33 | Max. High 29, non-reasoning 19 |
| GLM-5.3 | 32 | Max. Low 23 |
| Inkling 2 Small | 31 | One entry, a reasoning model |
| Qwen3.8 Flash Next | 29 | One entry, a reasoning model |
| GLM-5.3 Flash | 28 | One entry, a reasoning model |
| Qwen3.8 27B | 20 | Xhigh. Medium 17, low 16, non-reasoning 10 |

## What I did not verify

- **Answer quality on these files.** The index scores the models as served by their makers or providers. I didn't score the 4-bit and 6-bit builds.
- **Decode with thinking on for DeepSeek and Qwen.** Their index scores are with thinking on, and I timed them with it off.
- **Why the last long run read slowest** in 10 of 12 cells.
- **Other engines on the single-engine models.** Flash Next 4-bit, GLM-5.3 Flash 4-bit, Inkling 2 Small and Flash Next full each ran on one engine here. Another engine may do better.
- **The Qwen3.8 27B past 262,144 tokens** at a documented setup.

## Credit

- **Engines.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart). [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim). [mlx-serve](https://github.com/ddalcu/mlx-serve) by ddalcu.
- **Models.** DeepSeek V4.1 Flash by DeepSeek. GLM-5.3 and GLM-5.3 Flash by Z.ai. Inkling 2 Small by [@thinkymachines](https://x.com/thinkymachines). Qwen3.8 by [@Alibaba_Qwen](https://x.com/Alibaba_Qwen).
- **Builds.** The Lossless pack by ddalcu. The oQ quants by Jundot and mlx-community. The MLX builds by TensorFold and mlx-community. The DFlash2 drafter by z-lab.
- **Scores.** Artificial Analysis.

If a setting here is wrong, open an issue and I will rerun it.
