# Finding 24. Qwen3.8 Flash Next IQ3_S on Strata 0.2.19, MTP on and off, against llama.cpp on the same files

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: Strata is an engine built to run Qwen3.8 Flash Next, a 125B model with 6B active weights, on ordinary hardware. On a Mac it has its own Metal engine. Its setup picks the pack and settings for each Mac. On this one it picked the IQ3_S pack, 3.5 bits a weight, with its MTP draft layer on. I ran that, then MTP off, then wider draft windows to push the max. llama.cpp read the very same two files as a reference. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**Strata 0.2.19 wrote 200.3 tok/s on Qwen3.8 Flash Next IQ3_S at its max, with `--spec 5`. With its setup's own config, MTP on and a 3-token window, it wrote 173.8 on its latest start and 183.3 on the start before. With the model's own sampler it wrote 136.5. llama.cpp b12359 on the same files wrote 58.2 and 55.7, so Strata is 3.4 times llama.cpp at the max and 2.5 times at the median. With MTP off Strata wrote 100.6, 1.7 times llama.cpp, which also wrote one token a step. Setup's config and MTP off wrote the same text on 100 of 100 replies. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Setting | Max, tok/s | Median, tok/s |
|---|---|---|
| Strata, setup's config with `--spec 5` | 200.3 | not run |
| Strata, setup's config with `--spec 4` | 193.6 | not run |
| Strata, setup's config, latest start | 173.8 | not run on this start |
| Strata, setup's config, first start | 183.3 | 136.5 |
| Strata, MTP off | 100.6 | 96.4 |
| llama.cpp b12359, the same files | 58.2 | 55.7 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The summary page shows 200.3 and 136.5.** It takes the highest max among the settings tried, and `--spec 5` ran one start.
- **The multiples.** Max 200.3 / 58.2 = 3.4. Median 136.5 / 55.7 = 2.5. MTP off 100.6 / 58.2 = 1.7. Setup's config on its latest start 173.8 / 58.2 = 3.0.
- **Like for like, 1.7.** llama.cpp ran at its defaults with no drafts, one token a step, as Strata does with MTP off. The larger multiples include Strata's drafts.
- **No `mlx-lm` multiple.** `mlx-lm` reads MLX weights, and this pack is GGUF. llama.cpp reads the same two files, so it is the reference here.

## Chart

ELI5: The top speed on new code for each setting, at a 1K and a 4K prompt. Every bar reads the same two files.

![Bars of writing speed in tokens per second for Qwen3.8 Flash Next IQ3_S, greedy at temperature 0, new code, replies of up to 2,048 tokens. At a 1K and a 4K prompt. llama.cpp 58.2 and 57.4. Strata with MTP off 100.6 and 99.2. Strata with its setup's config, first start 183.3 and 179.7, second start 173.8 and 169.4. With --spec 4, 193.6 and 188.5. With --spec 5, 200.3 and 185.0.](chart_max.png)

## MTP on and off

ELI5: With MTP on, a small draft layer guesses the next few tokens and the full model checks them all in one step. With it off, the model writes one token a step. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s. MTP on is setup's config, first start `77bb7582fe47`. MTP off is `dff5db389042`.

| Test | Prompt | MTP off | MTP on | Text by text |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 100.6 (99.6 to 101.1) | 183.3 (180.5 to 193.4) | faster on 5 of 5, middle ratio 1.83 |
| Greedy, new code, replies up to 2,048 tokens | 4K | 99.2 (99.1 to 99.3) | 179.7 (167.5 to 190.6) | faster on 5 of 5, middle ratio 1.81 |
| Greedy, new code, 512-token replies | 1K | 101.5 (99.6 to 101.8) | 179.3 (162.8 to 184.1) | faster on 5 of 5, middle ratio 1.77 |
| Greedy, new code, 512-token replies | 4K | 99.1 (99.0 to 99.2) | 167.8 (163.8 to 183.0) | faster on 5 of 5, middle ratio 1.69 |
| Own sampler, mixed text, 512-token replies | 4K | 96.4 (96.2 to 96.4) | 136.5 (127.6 to 139.1) | faster on 5 of 5, middle ratio 1.42 |

- **MTP was faster on every text.** Long code replies, 10 of 10 with a middle ratio of 1.82. With the sampler, 5 of 5 with 1.42.
- **Plain decoding is about 100 tok/s whatever the text.** The five runs of each MTP-off cell sit within 2.2 tok/s of each other.
- **Strata's own log counts the drafts.** On the long code replies, 86.3% of drafts were accepted on the first start and 85.5% on the second.
- **More on easy text.** The same start wrote 240.0 tok/s on the copy task and 203.0 on the counting toy, at 1K. Strata also drafts from earlier text in the prompt, which pays when a reply repeats it. No copy or counting line goes on the summary.
- **Short replies.** 158.3 tok/s at 1K with 128-token replies, against 179.3 with 512.

## Pushing the max

ELI5: The draft window is how many guesses the draft layer may make before the model checks them. Setup writes 3 on this Mac, with a rule that it only guesses further when it is sure. I tried 4 and 5 with the same rule.

| Window | 1K, 2,048-token replies | 4K, 2,048-token replies | Drafts accepted | Text by text against setup's 3 |
|---|---|---|---|---|
| 3, setup's config, first start | 183.3 | 179.7 | 86.3% | |
| 3, setup's config, second start | 173.8 | 169.4 | 85.5% | |
| 4 | 193.6 | 188.5 | 83.1% | first start, faster on 9 of 10, middle ratio 1.06 |
| 5 | 200.3 | 185.0 | 77.9% | first start, faster on 10 of 10, middle ratio 1.05. Second start, faster on 10 of 10, middle ratio 1.11 |

- **A window of 5 was faster than setup's 3 on every long code reply.** Against the first start by a middle ratio of 1.05, and against the second by 1.11.
- **The two starts of setup's config differ by 5%.** Text by text the second was slower on 10 of 10 replies, with a middle ratio of 0.95. Their draft acceptance is level, 86.3% and 85.5%. So the gain from a window of 5 is somewhere from 1.05 to 1.11 times, and I can't pin it closer with one start of each window.
- **Each wider window accepts fewer drafts,** 86.3% at 3, 83.1% at 4 and 77.9% at 5. It still pays because each check covers more tokens.
- **I didn't try the sampler with the wider windows.**

## The text

ELI5: I asked the same 50 short questions twice on each start and compared the whole reply.

- **Setup's config and MTP off wrote the same text on 100 of 100 replies.** The 100 are the 50 questions on both passes, 64 tokens each, greedy. Strata's docs say MTP only proposes tokens and the full model checks each one, so the text should not change. Here it didn't.
- **Each start repeated itself on 50 of 50.**
- **This says nothing about answer quality.** I did not grade the answers.

## What the replies were

ELI5: The requests switched thinking off, and Strata honoured it. Every reply was answer text.

- **No thinking.** Every timed row counts 0 reasoning tokens. A check request with thinking off streamed 126 pieces of answer text, 517 characters, and nothing in the reasoning field, and stopped on its own after 137 tokens.
- **With no thinking field** the same request gave 496 characters of reasoning in its own field and 343 of answer.
- **22 of 60 long code replies ended on their own** before 2,048 tokens, the shortest at 1,424. The rest ran to the limit.

## Reference points

ELI5: The fairest yardstick is another engine reading the same files. llama.cpp does.

- **llama.cpp b12359, the newest stable release (v1.0.0), on the same two files.** 58.2 tok/s at the max and 55.7 with the sampler, at its defaults, with no drafts. Its log at the default verbosity names no Metal device or kernel path, so I can't confirm from it which kernels ran. It reads the prompt at 1,364 tok/s at 1K and 1,403 at 4K. Strata reads it at 2,344 and 2,904.
- **The first token** came after 0.41 s at 1K and 1.53 s at 4K on Strata, against 0.68 s and 3.16 s on llama.cpp.
- **Text by text Strata was faster on every reply.** On long code replies, 10 of 10 with a middle ratio of 3.15 for setup's first start. With the sampler, 5 of 5 with 2.47.
- **TensorFold's 4-bit and 6-bit MLX builds of this model** are in findings [7](../07_qwen38_tensorfold_130) and [19](../19_tensorfold_133_refresh), and oMLX's full-precision build in finding [16](../16_omlx_082_refresh). Those are different weights and bits, so I give no ratio to them.

## The setup

ELI5: Strata's own setup, run as its docs say, on files I downloaded and checked first. A fresh server start for every setting.

- **Engine.** [Strata](https://github.com/Niko1221/Strata) 0.2.19, the newest release, tag `v0.2.19` at commit c6f6427d. Built from source on this Mac by its own `./setup.sh`, which builds the Metal engine with Xcode's tools. The engine program prints `strata 0.1.65-metal`, the engine version this release ships.
- **Setup command.** Run in the source folder, on the files already downloaded. Setup checked the picture reader against its pinned SHA-256 and fetched the MTP draft layer's tensors from Qwen's own repository, each checked against a pinned SHA-256.

```bash
./setup.sh --family qwen --model IQ3_S --gguf-dir <models>/IQ3_S --models-dir <models> --data-dir <data> --host 127.0.0.1 --port 8230 --no-browser --no-start --yes
```

- **What setup chose for this Mac.** The IQ3_S pack held in memory, MTP on with `--spec 3 --spec-min-p 0.5`, a 64K context and pictures on. It also printed that the UD-Q4_K_XL pack would fit, with higher quality and slower decoding.
- **Serve command.** Setup's start script runs Strata's Python server with the config it wrote. I bound it to this Mac and closed outside fetches.

```bash
terminal/.venv/bin/python terminal/serve/server.py --engine strata --config strata-iq3_s.json --host 127.0.0.1 --port 8230 --offline
```

- **The engine flags setup wrote.** `--expert-cache 64 --prefill auto --spec 3 --spec-min-p 0.5 --mtp <draft layer> --max-context 65536 --mmap-experts --vision`, with `STRATA_METAL_STREAM=0`.
- **MTP off** is setup's own rule for a Mac without the draft layer, `--spec 2 --suffix-draft 0` and no `--mtp`. By `strata --help`, `--suffix-draft 0` leaves the MTP as the only drafter, so with no MTP one token a step.
- **`--spec 4` and `--spec 5`** change only that number in setup's config.
- **fp16 decode.** By comments in Strata's setup code at this tag, the engine turns on fp16 decode windows by itself for a resident IQ3_S pack, chosen from the file name, and the authors measured small differences from fp32. The log doesn't print it, so I can't confirm it ran.
- **Weights.** [ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) @ ed59f920, the IQ3_S files, 51.1 and 26.8 GiB. The first holds the model and the second a table Strata reads from disk. Every file was verified against the pinned commit, and Hugging Face's scan flagged nothing. Strata maps the 54.8 GB of experts from the file in place. The server and its children held 59 to 65 GiB.
- **The model.** [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next).
- **llama.cpp** b12359 served the first of the two files with its defaults, `-c 65536 -ngl all -np 1`.
- **Sampler.** The maker's thinking-off sampler, temperature 0.7, top-p 0.8, top-k 20 and presence penalty 1.5, on both engines. TensorFold's lines in findings 7 and 19 left the presence penalty out, as TensorFold refuses it.
- **Thinking** switched off in every request, with `chat_template_kwargs: {"enable_thinking": false}`.

| Run id | Setting | Started, SGT, 23 Nov 2026 |
|---|---|---|
| `77bb7582fe47` | Strata, setup's config | 02:23 |
| `dff5db389042` | Strata, MTP off | 02:29 |
| `ca9762656ee4` | Strata, `--spec 4` | 02:36 |
| `ef38b6483d5b` | Strata, `--spec 5` | 02:39 |
| `7b15a99cb722` | Strata, setup's config, second start | 02:42 |
| `37c6f64892e9` | llama.cpp b12359, the same files | 02:45 |

## How I measured

ELI5: Same Mac, same harness, same texts and same questions as findings 5 to 23.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line, so no prompt cache can hit. Strata's log shows 0 tokens reused on every timed request.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. On this model's tokenizer the code prompts came to 838 to 1,940 tokens and 3,532 to 4,945.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last. Strata's own log gives its speed for each request too, and it matches. On one `--spec 5` reply the log says 200.2 tok/s.
- **Not fully quiet.** Through the whole job, 02:22 to 02:54 SGT, I was working on this Mac beside it. I built and pushed this repository's previous update during setup's first start, and wrote files and ran a small code tool and its self-test during the later arms. All light CPU and disk work. The first start of setup's config, the one beside the push, came out the faster of its two starts.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **IQ3_S is about 3.5 bits a weight.** Fewer bits read less memory per token, so a 4-bit or 6-bit build of the same model has more to read. That is part of any gap to findings 7, 16 and 19.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Strata's setup picks the pack by the Mac's memory.** Another Mac may get another pack and other numbers.
- **Two starts of the same setting differed by 5% here.** Read single-start figures with that in mind.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 172 raw rows from the bench database. 155 timed requests and 17 warm-ups.
- **`runs.csv`.** The 6 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/24_qwen38_flash_next_strata_0219
```

## What I did not verify

- **A second start of `--spec 4`, `--spec 5` and MTP off.**
- **The text check on `--spec 4` and `--spec 5`.** It ran on setup's config and MTP off only.
- **The UD-Q4_K_XL pack** setup named as the higher-quality choice for this Mac, and Strata's DFlash2 drafter, which that pack prefers.
- **What the fewer bits cost in quality.** I did not grade answers or measure the pack against the full model.
- **Long prompts past 5K tokens, several users at once, and pictures.**
- **Strata's desktop app and its `strata launch` command.** I ran the source setup only.

## Credit

- **Engine.** [Strata](https://github.com/Niko1221/Strata) by [Niko1221](https://github.com/Niko1221).
- **Pack.** IQ3_S GSQ-RCO quantization by [ISTA-DASLab](https://huggingface.co/ISTA-DASLab).
- **Reference engine.** [llama.cpp](https://github.com/ggml-org/llama.cpp).
- **Model.** Qwen3.8 Flash Next by [Qwen](https://x.com/Alibaba_Qwen).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
