# Finding 30. Inkling 2 Mini on Strata 0.2.20, its drafter faster on greedy code and slower on the sampler

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Updated on 23 Nov 2026 at 13:49 SGT. llama.cpp's main-branch build b12642 could not load the same GGUF, so there is no same-file reference line. See the GGUF section.

ELI5: Strata 0.2.20 came out on 23 Nov 2026 at 07:20 SGT with a new engine for Inkling 2 Mini, `strata-inkling`. Strata's setup fetches a ready-made copy unless asked to build one. I had it build from Strata's source, with `--build` and ran it on the pack setup picks for this Mac, Strata's own SQ-20, with its built-in DSpark drafter on and off. I also tried Unsloth's 8-bit GGUF, which Strata supports too. Strata serves Inkling 2 Mini with thinking off only, so every reply here is answer text.

**Strata 0.2.20, its Inkling engine built from source, wrote 106.1 tok/s on Inkling 2 Mini at its max with Strata's own SQ-20 pack and its DSpark drafter, and 37.7 with the model's own sampler. With drafting off it wrote 61.5 and 59.3. So the drafter made greedy code 1.7 times as fast, faster on 19 of 20 same-text pairs, and made the sampler 0.64 times as fast, slower on 10 of 10. By Strata's own counts, with the sampler it proposed about 5 drafts a written token and kept about 5% of them. With the drafter on, 86 of 100 short greedy replies match drafting off. This build refused the DSpark drafter file Strata's setup pins for Unsloth's GGUF, so the GGUF ran with drafting off only, at 60.1. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Pack and setting | Max, tok/s | Median, tok/s |
|---|---|---|
| Strata's SQ-20, DSpark drafter on, setup's config | 106.1 | 37.7 |
| Strata's SQ-20, drafting off | 61.5 | 59.3 |
| Unsloth's UD-Q8_K_XL GGUF, drafting off | 60.1 | 58.2 |
| Unsloth's UD-Q8_K_XL GGUF, DSpark drafter on | did not start | did not start |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, temperature 1.0 and top-p 1.0, mixed text, 512-token replies, 4K prompt.
- **The arithmetic.** 106.1 / 61.5 = 1.73 at the max. 37.7 / 59.3 = 0.64 at the median.
- **The SQ-20 drafter line is its latest start.** The first start wrote 105.5 at 1K and 38.4 with the sampler.
- **The summary page shows SQ-20's best of each.** Its max, 106.1, is the drafter line, and its median, 59.3, is drafting off. Setup's own config, with the drafter, gives 37.7 with the sampler.
- **These are one build of the engine,** compiled here from the tag. Strata's ready-made `strata-inkling` may differ.
- **Every reply is answer text.** Strata serves Inkling 2 Mini with reasoning effort "none" only, by its source (`inkling_family.HAS_THINKING` is False). A check request streamed 449 characters, all in the answer field, and none as reasoning. Read back, the short replies answer directly, such as "This text is a set of instructions for a Rust programming exercise".
- **No `mlx-lm` multiple.** `mlx-lm` 0.32.2 has no Inkling 2 model. Drafting off is the baseline.

## Chart

ELI5: The same pack with Strata's drafter off and on. Greedy code gains, and the model's own sampler loses.

![Paired bars of writing speed in tokens per second for Inkling 2 Mini on Strata 0.2.20 with Strata's SQ-20 pack, DSpark drafter off against on. Greedy code with replies of up to 2,048 tokens at 1K, 61.5 and 105.8. The same at 4K, 59.1 and 106.1. Greedy code with 512-token replies at 1K, 61.6 and 90.0. The model's own sampler at 4K, 59.3 and 37.7.](chart_draft.png)

## The drafter on and off

ELI5: A drafter guesses several tokens and the model checks them in one step. On greedy text the guesses land often. With the sampler the model picks at random from its likely tokens. Here the drafter kept guessing several tokens a step and almost none landed, so the checks cost more than they saved.

Decode tok/s on Strata's SQ-20. Each cell is the middle of 5 runs.

| Test | Drafting off, `43be61155ecd` | Drafter on, `6d28d93cba3d` | Drafter on, `acb7355827b4` |
|---|---|---|---|
| Greedy code, 2,048, 1K | 61.5 | 105.5 | 105.8 |
| Greedy code, 2,048, 4K | 59.1 | 72.3 | 106.1 |
| Greedy code, 512, 1K | 61.6 | 93.8 | 90.0 |
| Greedy code, 512, 4K | 59.3 | 77.3 | 99.4 |
| Own sampler, 4K | 59.3 | 38.4 | 37.7 |
| Counting toy, 1K | not run | 170.6 | 166.6 |
| Copy task, 1K | not run | 144.4 | 147.8 |

- **The 4K long-code cell spread most.** The two drafter starts read 72.3 and 106.1 there, on the same texts.
- **Greedy code, text by text.** Against drafting off, the first drafter start was faster on 9 of 10 long code pairs, middle ratio 1.66, and the second on 10 of 10, 1.74. Short code read 1.41 and 1.47.
- **The sampler, text by text.** Slower on 5 of 5 pairs each time, middle ratios 0.65 and 0.64. Strata's own timing agrees. The middle of five requests is 26.2 and 26.5 ms a token with the drafter, and 16.8 without.
- **What the drafter did, by Strata's own counts.** With the sampler it proposed 5.0 and 5.1 drafts per written token and kept 5.5% and 5.1% of them. On long greedy code it proposed 1.1 a token and kept 58.3% and 58.7%. On short greedy code it kept 52.0% and 52.8%, and on counting and copying 79% to 85%.
- **The two drafter starts spread widely on greedy code.** At 4K with long replies they read 72.3 and 106.1. Text by text the second against the first reads 1.08 on long code and 1.10 on short, faster on 6 of 10 each.
- **No saved draft table that I could find.** Strata's Qwen engine keeps one (finding 28). For these starts I pointed `STRATA_DRAFT_COSTS_DIR` at a new folder, and it stayed empty. After the runs, only Strata's run logs had changed in its settings, data and pack folders, and both packs still matched their hashes.

## Did the text change

ELI5: The same 50 short greedy questions, asked twice on each start.

- **The drafter changes some replies.** With it on, 86 of 100 replies match drafting off, so 7 of the 50 questions end differently, on both passes.
- **Each setting agrees with itself.** The two drafter starts give the same 100 replies, and each start repeats itself on 50 of 50.
- **SQ-20 and the GGUF are different weights.** With drafting off they agree on 96 of 100.
- **This says nothing about answer quality.** I did not grade the answers.

## Unsloth's GGUF

ELI5: Strata reads Unsloth's GGUFs of Inkling 2 Mini as well as its own packs, with a separate DSpark drafter file. Its setup lists that file, with its size and SHA-256.

- **The drafter file was refused.** This build of `strata-inkling` loaded the GGUF in 1.85 s and stopped with "missing dspark tensor: dspark.markov_head.hidden_out.weight", exit code 2, on both tries. The file is `dspark-Inkling-2-Mini-Q8_0.gguf` from `unsloth/Inkling-2-Mini-GGUF` @ 45fd0876, and its size and SHA-256 match the table in Strata's setup at this tag.
- **Drafting off ran.** 60.1 tok/s at the max and 58.2 with the sampler.
- **llama.cpp could not read it either.** llama.cpp's stable v1.0.0 has no Inkling 2 model. Its main-branch build b12642, a pre-release of 23 Nov 2026 09:47 SGT at commit 5bacb7c8, stopped loading this GGUF with "check_tensor_dims: tensor 'blk.24.attn_q.weight' not found", on two tries from 13:46 SGT. Its download matched GitHub's SHA-256 digest. So there is no same-file reference line here.
- **SQ-20 decodes 2% faster.** With drafting off on both, SQ-20 against the GGUF was faster on 24 of 25 same-text pairs, middle ratio 1.02.

## Against other engines, with drafting off

ELI5: With drafting off an engine writes one token a step, whatever the text. That makes plain decoding the fairest line to set beside other engines, though the weights differ.

Max with drafting off, by finding. The pack sizes are on disk.

- **mlx-serve 26.11.4 pre-release, its 8-bit pack, 17.5 GiB.** 107.4 tok/s, [finding 20](../20_inkling2_mini_mlxserve_pre).
- **Rapid-MLX 1.1.0, 4-bit, 16.1 GiB.** 39.8, [finding 23](../23_inkling2_mini_rapidmlx_110).
- **oMLX 0.8.3, oQ4e, 15.7 GiB.** 62.4, [finding 26](../26_omlx_083_refresh).
- **MTPLX 2.13.2, Bare Speed pack, 14.9 GiB.** 89.9, [finding 29](../29_inkling2_mini_mtplx_2132).
- **Strata 0.2.20, SQ-20, 18.6 GiB.** 61.5, this page.
- **These are different weights and sizes, and not a ranking.** The other engines' replies were reasoning text. Text kind matters less with no drafts, but it still shows. MTPLX with drafts off read 89.9 greedy and 78.9 with the sampler. So I set no drafted line beside them.

## The setup

ELI5: Strata's own setup, run as its docs say, building the engine from source.

- **Engine.** [Strata](https://github.com/Niko1221/Strata) 0.2.20, published 23 Nov 2026 07:20 SGT, tag `v0.2.20` at commit a34979fc. `strata-inkling` 0.1.66 compiled on this Mac by Strata's `./setup.sh` with `--build`, which builds it with Metal from the checkout instead of fetching the ready-made engine. Its build record says `"source": "local"`. SHA-256 starts `33332f7368526483`.
- **It was still the newest release** when I published this, checked on 23 Nov 2026 at 13:38 SGT.
- **Setup command for SQ-20.**

```bash
./setup.sh --family inkling-2-mini --model SQ-20 --gguf-dir <folder>/Inkling-2-Mini-SQ-20.strata --data-dir <data> --build --host 127.0.0.1 --port <port> --no-browser --no-start --yes
```

- **What setup chose.** SQ-20, which it recommends for any Mac with 32 GiB or more, with its built-in DSpark drafter, the Vision shard and a 32K context. The engine flags are `--native <pack> --max-context 32768 --vision <shard>`, and the server adds the drafter.
- **Drafting off** is setup's config with `"drafting": "off"`, so the server passes `--draft off`.
- **Weights.** [strata-engine/Inkling-2-Mini-Strata](https://huggingface.co/strata-engine/Inkling-2-Mini-Strata) @ 04996a1e, SQ-20 and the Vision shard, the engine author's own repository. [unsloth/Inkling-2-Mini-GGUF](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) @ 45fd0876, UD-Q8_K_XL with its DSpark drafter and picture reader. Every weight file was checked against its SHA-256, and each also matches Strata's own table. The small text files were checked against their git fingerprints.
- **Serve command.** Strata's Python server with setup's config, bound to this Mac, with `--offline`.
- **Sampler.** Temperature 1.0 and top-p 1.0, the model's own. No thinking field in the requests.

| Run id | Pack and setting | Started, SGT, 23 Nov 2026 |
|---|---|---|
| `c7ce703a276f` | Unsloth GGUF, drafting off | 12:50 |
| `6d28d93cba3d` | SQ-20, drafter on | 13:01 |
| `acb7355827b4` | SQ-20, drafter on | 13:09 |
| `43be61155ecd` | SQ-20, drafting off | 13:18 |

## Things the setup did

ELI5: Three things happened on the way that a Strata user on a Mac may meet too.

- **Given a folder, setup read the GGUF as a `.strata` file.** With `--gguf-dir` set to the folder, setup wrote a config with no drafter file and no picture reader. Naming the GGUF file itself gave the right config. By `inkling_local_source` in Strata's setup at this tag.
- **Setup overwrote its engine copy in place, seen once here.** Run a third time, setup copied the built `strata-inkling` over the old copy. macOS then refused to start it, "code signature validation failed", though the build output ran. A fresh copy of the same file, moved into place, ran. Nothing in the system's security settings was changed.
- **Setup removed the earlier model's config.** Strata's Qwen config from that morning, in the same checkout, was gone after the Inkling setup. This bench's Qwen runs read their own copies.

## How I measured

ELI5: Same Mac, same harness, same texts and same questions as the other Inkling 2 Mini pages.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. Each prompt opens with a new session line so no prompt cache can hit.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request. The field check came after the first timed block, and a minute's pause followed the unit tests.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.

## Things to know before you compare

- **Answer text, not reasoning.** The other Inkling 2 Mini pages time reasoning text.
- **Short answers ended early.** Answers to the 512-token code prompts averaged 397 to 491 tokens, and long code 1,151 to 1,349, since the model stopped on its own.
- **Max is not what a chat feels like.** Here the gap is wide, since the drafter helps greedy text and hurts the sampler.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 178 raw rows from the bench database. 160 timed requests and 18 warm-ups.
- **`runs.csv`.** The 4 runs, with engine, version, start time, settings and sampling.
- **The answer checks are not in `rows.csv`.** They are hashes of untimed replies.

From the top of this repository.

```bash
python3 tools/summarize.py findings/30_inkling2_mini_strata_0220
```

## What I did not verify

- **Why the drafter proposes about five drafts a token with the sampler.** Strata's counts show it, not why.
- **The other SQ packs and GGUF sizes.** I ran SQ-20 and UD-Q8_K_XL only.
- **The GGUF with its drafter.** It did not start.
- **Strata's ready-made `strata-inkling`.** I built it from source.
- **Answer quality, long prompts, pictures and two users at once.**

## Credit

- **Engine and the SQ-20 pack.** [Strata](https://github.com/Niko1221/Strata) by Niko1221 on GitHub.
- **GGUF and drafter.** [Unsloth](https://huggingface.co/unsloth).
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
