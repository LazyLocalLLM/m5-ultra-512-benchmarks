# Finding 14. Inkling 2 Mini on oMLX 0.8.1, max and median speed

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: Thinking Machines released Inkling 2 Mini on 21 Nov 2026. It is a small model that runs some of its layers three times for each token. oMLX 0.8.1 came out the same day and is the first oMLX release that loads it. I ran its two ready builds that afternoon, with the engine's drafts on and off. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**oMLX 0.8.1 wrote 96.3 tok/s on Inkling 2 Mini oQ4e at its max and 65.9 with the model's own sampler. With drafts off the same build wrote 54.5 and 54.4, so the drafts gave 1.8 times at the max. The smaller oQ3e build wrote 105.1 and 67.1. Every timed reply was reasoning text, though the request switched thinking off. The server held 16.6 GiB. One server start per setting. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 21 Nov 2026.**

| Build | Drafts | Max, tok/s | Median, tok/s |
|---|---|---|---|
| oQ4e, 15.7 GiB | On | 96.3 | 65.9 |
| oQ4e, 15.7 GiB | Off | 54.5 | 54.4 |
| oQ3e, 12.8 GiB | On | 105.1 | 67.1 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the better of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **These are reasoning speeds.** A benchmark that counts only answer tokens will show other numbers.

## Chart

ELI5: The top speed on new code for each setting. One bar per setting and prompt size.

![Bars of writing speed in tokens per second for Inkling 2 Mini on oMLX 0.8.1, greedy at temperature 0, new code, replies of up to 2,048 tokens. oQ4e with drafts on 96.3 at a 1K prompt and 80.1 at 4K. oQ4e with drafts off 54.5 and 53.7. oQ3e with drafts on 100.6 and 105.1.](chart_max.png)

## The oQ4e build, drafts on and off

ELI5: The build carries a small draft model, DSpark, that guesses several tokens ahead for the big model to check. With it off the model writes one token a step. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s. Drafts on is run `a3cf6857c4b5`, at the default depth. Drafts off is run `fe2a52ddebd0`.

| Test | Prompt | Drafts off | Drafts on | Gain |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 54.5 (54.3 to 54.5) | 96.3 (83.1 to 97.3) | 1.77 |
| Greedy, new code, replies up to 2,048 tokens | 4K | 53.7 (53.6 to 53.9) | 80.1 (79.5 to 98.3) | 1.49 |
| Greedy, new code, 512-token replies | 1K | 55.2 (55.1 to 55.3) | 79.9 (50.6 to 89.6) | 1.45 |
| Greedy, new code, 512-token replies | 4K | 54.4 (54.4 to 54.7) | 80.4 (69.7 to 87.2) | 1.48 |
| Own sampler, mixed text, 512-token replies | 4K | 54.4 (54.3 to 54.6) | 65.9 (59.2 to 67.7) | 1.21 |

- **Max.** 96.3 tok/s with drafts on. 96.3 / 54.5 = 1.77 times the same build with drafts off.
- **Median.** 65.9 tok/s. 65.9 / 54.4 = 1.21 times.
- **Plain decoding is about 54 tok/s whatever the text.** The five runs of every drafts-off cell sit within 0.3 tok/s of each other.
- **Text by text the drafts were faster** on 10 of 10 long replies with a middle ratio of 1.56, on 9 of 10 short replies with 1.46, and on 5 of 5 sampled replies with 1.21.
- **The drafted runs spread widely.** The 512-token cell at 1K goes from 50.6 to 89.6. Drafted speed depends on how well the draft guesses each text.
- **All 10 long replies ran to 2,048 tokens**, on both starts.
- **The log shows the draft at work.** "Inkling 2 DSpark drafter loaded: block=8 depth=7 adaptive=True". The last request of the drafted start kept 393 of 434 drafted tokens and reached depth 7. The drafts-off start has no draft line.

## The oQ3e build

ELI5: The same model stored at fewer bits. It is smaller and wrote faster here. I did not measure what the fewer bits cost in quality.

Decode tok/s with drafts on at the default depth, run `472bfd081962`.

| Test | 1K prompt | 4K prompt |
|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 100.6 (87.6 to 105.7) | 105.1 (92.2 to 111.9) |
| Greedy, new code, 512-token replies | 94.0 (82.5 to 100.6) | 81.5 (76.3 to 106.5) |
| Own sampler, mixed text, 512-token replies | not run | 67.1 (61.3 to 83.1) |

- **Max.** 105.1 tok/s at 4K, and 100.6 at 1K.
- **Median.** 67.1 tok/s.
- **Against the oQ4e build with drafts on**, text by text, it was faster on 10 of 10 long replies with a middle ratio of 1.13, and on 10 of 10 short replies with 1.12. One start of each, and the ranges overlap.
- **No drafts-off start on this build.**
- **Memory.** The server held 13.6 GiB at the end, against 16.6 GiB for oQ4e, by `ps`.

## What the replies were

ELI5: The request asked the model not to think. It thought anyway, as Inkling 2 Small did in finding 9. So the speeds are of thinking text.

- **Reasoning text.** Of the 45 timed replies of the oQ4e drafts-on start, 41 held 3 answer tokens at most and were reasoning otherwise. The other 4 closed their thinking and wrote some answer. On the drafts-off start it was 25 of 25, and on oQ3e 44 of 45.
- **The copy and counting questions got no answer inside 512 tokens** when I read one of each back, on both builds. The model spent the reply planning. So I publish no copy or counting line. The rows are in `rows.csv` under the contents `code_echo` and `code_count`.
- **I did not find a switch that stops the thinking.** I sent the two fields oMLX reads for thinking off. I did not try the model's own effort setting.

## The text with drafts on and off

ELI5: I sent 50 short greedy questions twice to each start and compared the whole reply, thinking text included. I report the counts and no cause.

| Compared | Replies with the same text |
|---|---|
| oQ4e drafts off, second pass against first | 50 of 50 |
| oQ4e drafts on, second pass against first | 47 of 50 |
| oQ3e drafts on, second pass against first | 48 of 50 |
| oQ4e, drafts off against drafts on | 43 of 100 |

- **With drafts on, one start did not always repeat itself.** 3 of 50 replies on oQ4e and 2 of 50 on oQ3e differed between two passes of the same question.
- **With drafts off it did**, on 50 of 50.
- **A reply is 64 tokens.** One early token that differs changes all the text after it.
- **This says nothing about which text is better.** I did not grade the answers.

## Reference points

ELI5: My usual baseline is Apple's `mlx-lm` on the same weights. I did not try it on this model, so the baseline here is the same build with drafts off.

- **The baseline is drafts off on oMLX**, 54.5 tok/s, above.
- **I did not try `mlx-lm` on this model.**
- **Inkling 2 Small**, the 594B model of the same family, wrote 51.6 tok/s at its max and 42.2 with its own sampler on oMLX 0.8.0, in [finding 9](../09_omlx_080_four_models). That is another model and an older release.
- **EXO Labs posted its own figures for this model** in [this post](https://x.com/exolabs/status/2123953913342935486), on an engine it calls upcoming. That engine is not released, so I could not run it, and this page is not a comparison with it.
- **The oMLX release notes** are [here](https://github.com/jundot/omlx/releases/tag/v0.8.1).

## The setup

ELI5: One engine, two ready builds, and a fresh server start for every setting.

- **Added 21 Nov 2026 17:07 SGT.** oMLX 0.8.2 came out at 12:20 SGT that day, two hours before these runs began at 14:21 SGT. I had not seen it. Its notes call it a hotfix for click positions on screenshots and say everything else is the same as 0.8.1. These runs are on 0.8.1. The oQ4e drafts-on start was rerun on 0.8.2 that evening, in [finding 16](../16_omlx_082_refresh). Its max came in at 83.5 and then 88.5 on two starts against the 96.3 here, with overlapping ranges, and that page says why I read it as start spread.

- **Engine.** [oMLX](https://github.com/jundot/omlx) 0.8.1, released 21 Nov 2026 09:17 SGT, installed from the tagged source with its custom kernels built (`OMLX_WITH_CUSTOM_KERNEL=1`).
- **Serve command.**

```bash
omlx serve --model-dir <models> --host 127.0.0.1 --port 8193 --max-concurrent-requests 1 --headless --no-hf-cache --base-path <home>
```

- **Weights.** Both made with oMLX 0.8.1 and uploaded to mlx-community on 21 Nov 2026. Every file was verified against the pinned commit.
  - [mlx-community/Inkling-2-Mini-oQ4e-mtp](https://huggingface.co/mlx-community/Inkling-2-Mini-oQ4e-mtp) @ 3eea0427, 15.7 GiB.
  - [mlx-community/Inkling-2-Mini-oQ3e-mtp](https://huggingface.co/mlx-community/Inkling-2-Mini-oQ3e-mtp) @ 5552e32e, 12.8 GiB.
- **The model**, by the build's card. [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini), 26.4B weights with 3.4B active per token, a looped mixture of experts whose middle 12 layers run three times a token. Apache 2.0.
- **Hugging Face's security scan of both repositories was not finished** when I read it on 21 Nov 2026 at 14:56 SGT. No file was flagged. The files I loaded are safetensors, JSON, a chat template and text.
- **Model settings**, in oMLX's own `model_settings.json`. `mtp_enabled` true, or false for the drafts-off start. `a8_prefill_enabled` false, `activation_fp16_enabled` false. No fixed depth.
- **Burst decode.** `server.burst_decode_mode` at `balanced`, the default.
- **Sampler.** Temperature 1.0 and top-p 1.0. The build's `generation_config.json` gives temperature 1.0 and no top-p.
- **Thinking** switched off in every request, with `enable_thinking: false` at the top level and in `chat_template_kwargs`.

| Run id | Build | Drafts | Started, SGT, 21 Nov 2026 |
|---|---|---|---|
| `a3cf6857c4b5` | oQ4e | On, default depth | 14:21 |
| `fe2a52ddebd0` | oQ4e | Off | 14:33 |
| `472bfd081962` | oQ3e | On, default depth | 14:45 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as findings 5 to 12.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. On this model's tokenizer the code prompts came to about 1,070 to 2,070 tokens and 4,400 to 6,070.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last, reasoning tokens included.
- **The three questions** are those of [finding 5](../05_dsv41_omlx_080_max_push), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Reasoning text is not answer text.** Nothing here is an answer speed.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **One start per setting.** Finding 3 measured 7% between two starts of one setting on this engine.
- **The model and the release are hours old.** A setting I missed is likely. Tell me and I will rerun it.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 128 raw rows from the bench database. 115 timed requests and 13 warm-ups.
- **`runs.csv`.** The 3 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/14_inkling2_mini_omlx_081
```

## What I did not verify

- **The model with thinking truly off.** I found no switch that stops it.
- **The model's own effort setting**, and a fixed draft depth.
- **What the fewer bits of oQ3e cost in quality.**
- **A second start** of any setting, and drafts off on oQ3e.
- **What the timed replies say.** I read back two replies per build and the short previews of the answer check.
- **Long prompts**, several users at once, and images.
- **Any other engine on this model.**

## Credit

- **Engine.** [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim).
- **Weights.** The oQ builds on [mlx-community](https://huggingface.co/mlx-community).
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
