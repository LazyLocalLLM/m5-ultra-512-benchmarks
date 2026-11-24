# Finding 40. The code column, 17 models writing new code with their own sampler

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: The summary showed two speeds a model. Max is greedy decoding on code, the top speed. Median is the model's own sampler on mixed text, closer to daily use. Neither is how a coding agent runs, with the model's own sampler while it writes code. This adds that speed as a third column, for every model on this Mac's disk.

**Qwen3.8 27B 4-bit on TensorFold 1.3.4 wrote 196.2 tok/s of new code with its own sampler, and Qwen3.8 Flash Next 4-bit 165.5. DeepSeek V4.1 Flash wrote 90.9 on TensorFold 1.3.4 with the maker's files and 69.2 on mlx-serve 26.11.3 with the Lossless pack. Inkling 2 Mini wrote 127.2 on MTPLX 2.13.3, as reasoning text. Mac Studio M5 Ultra 512 GB, one user, 4K code prompt, 512-token replies, middle of 5 runs, 25 Nov 2026.**

| Model | Engine and setup | Code decode tok/s | Range | Reply text | Run |
|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017, Lossless | mlx-serve 26.11.3, the median line's arm, lm head 8-bit | 69.2 | 59.1 to 89.5 | answer | `1d2e394c0183` |
| DeepSeek V4.1 Flash 1017, maker's files | TensorFold 1.3.4, drafts at defaults | 90.9 | 86.6 to 105.8 | answer | `35a1123068ce` |
| GLM-5.3 Flash, 4-bit | TensorFold 1.3.4, DFlash2 draft model | 87.6 | 84.7 to 98.7 | answer | `df9d5aad61a8` |
| GLM-5.3, 4-bit | oMLX 0.8.3, MTP off | 24.4 | 24.3 to 24.5 | reasoning | `81b568ace86d` |
| Hy4-flash, 4-bit | TensorFold 1.3.4, DFly2 drafts, thinking on | 47.6 | 44.4 to 52.7 | reasoning | `9e81bf39a949` |
| Inkling 2 Mini, 8-bit | mlx-serve 26.11.4 pre-release, drafts on | 105.2 | 103.9 to 123.0 | reasoning | `2e9be2070510` |
| Inkling 2 Mini, 8-bit | mlx-serve 26.11.4 pre-release, drafts off | 104.2 | 103.5 to 105.1 | reasoning | `efc4664b216c` |
| Inkling 2 Mini, Bare Speed | MTPLX 2.13.3, draft head on | 125.4 | 117.7 to 165.3 | reasoning | `d520fa89d5ec` |
| Inkling 2 Mini, Optimized Quality | MTPLX 2.13.3, draft head on | 118.9 | 107.2 to 156.5 | reasoning | `c03f2fecccd4` |
| Inkling 2 Mini, Optimized Speed | MTPLX 2.13.3, draft head on | 127.2 | 115.1 to 153.6 | reasoning | `661a9c7f093c` |
| Inkling 2 Mini, SQ-20 | Strata 0.2.20, DSpark drafter on | 45.1 | 39.8 to 59.4 | answer | `b62f035fb6e4` |
| Inkling 2 Mini, SQ-20 | Strata 0.2.20, drafting off | 58.6 | 58.2 to 59.1 | answer | `1191fa929251` |
| Inkling 2 Mini, UD-Q8_K_XL | Strata 0.2.20, drafting off | 57.2 | 56.7 to 57.8 | answer | `488075759a6c` |
| Inkling 2 Mini, maker's release | Ollama 0.40.17, its MTP drafter | 67.1 | 56.6 to 70.1 | reasoning | `46ea0f5249c9` |
| Inkling 2 Mini, oQ3e | oMLX 0.8.3, DSpark draft on | 90.0 | 89.5 to 105.3 | reasoning | `273cb2e18022` |
| Inkling 2 Mini, oQ4e | oMLX 0.8.3, DSpark draft on | 84.8 | 83.2 to 95.0 | reasoning | `7e7d1190cde0` |
| Qwen3.8 27B, 4-bit | TensorFold 1.3.4, DFlash2 drafter | 196.2 | 189.3 to 265.1 | answer | `dddd7122c281` |
| Qwen3.8 Flash Next, 4-bit | TensorFold 1.3.4, MTP on, recipe line | 165.5 | 148.2 to 204.4 | answer | `2ca592767578` |
| Qwen3.8 Flash Next, full | oMLX 0.8.3, MTP on | 45.2 | 42.2 to 49.5 | answer | `7b671868eda1` |

- **Each figure** is the middle of 5 timed runs after a warm-up, in tok/s by my client's clock. The range is the slowest and fastest run.
- **Models in alphabetical order.** The summary page shows each model's faster line where two arms ran.
- **Reasoning text** means the timed replies were the model's thinking, as on the model's median line. A reasoning speed is not an answer speed.

## How each line was set up

ELI5: Each model ran as its median line on the summary ran, with code in place of mixed text. So the code figure and the median differ only in the text.

- **Same engine entry, context, slots and thinking** as the model's best median line, on the engine's newest release here.
- **Release changes.** GLM-5.3 4-bit and Inkling 2 Mini oQ3e ran on oMLX 0.8.3, where their median lines ran 0.8.0 and 0.8.1. Inkling 2 Mini Optimized Speed and Optimized Quality ran on MTPLX 2.13.3, where their median lines ran 2.13.2. The engine column of the summary names each release.
- **Same sampler.** For every run, the sampler recorded on the code rows matched the model's median line, checked by script before anything was published.
- **Draft modes, from the server logs.** oMLX logged MTP lines for the Inkling and Flash Next runs and none for GLM-5.3 4-bit, which has no draft head. TensorFold's DeepSeek log reads "drafts: DSpark + copies". mlx-serve's DeepSeek log reads "lm head requantized to 8-bit".
- **Two arms where the median used drafting off.** mlx-serve and Strata default to drafts, so their drafts-on arms ran too. On Strata's SQ-20 pack, drafting off was faster, 58.6 against 45.1.

## Not covered yet

- **Ten builds parked on the external drive.** GLM-5.3 with the joined draft head, GLM-5.3 Flash oQ6e and oQ4e, Qwen3.8 27B full, Qwen3.8 Flash Next 6-bit, DeepSeek V4.1 Flash oQ4e-mtp, Inkling 2 Small, Hy4-flash oQ4h and 8-bit, and Qwen3.8 Flash Next IQ3_S on Strata. Their code cells stay blank until they are back on the Mac's disk.
- **Rapid-MLX.** 1.1.1 is out. Its code cell waits for the run on that release.

## How I measured

- **Writing speed** is tokens written less one, over the time from the first streamed piece to the last.
- **The prompt** is the code prompt of the Max lines at 4K tokens, the same prompts by seed, and the model writes a new module from it.
- **The sampler** is each model's own recommended one, from `models.json`, as on the median lines.
- **One user**, streamed, network closed, 25 Nov 2026 04:01 to 05:36 SGT.

## Check it yourself

- `rows.csv` holds every request of the 19 runs, warm-ups marked. `runs.csv` holds each run's engine, build and settings.
- From the top of the repository, `python3 tools/summarize.py findings/40_code_column` prints the median and range of each run.

If I have set an engine up wrong, [open an issue](https://github.com/LazyLocalLLM/m5-ultra-512-benchmarks/issues) and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
