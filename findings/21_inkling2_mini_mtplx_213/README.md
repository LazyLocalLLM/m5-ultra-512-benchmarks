# Finding 21. Inkling 2 Mini on MTPLX 2.13.1, three packs, drafts on and off

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Updated on 23 Nov 2026 at 12:08 SGT. MTPLX 2.13.2 reran the draft-on lines of all three packs and Bare Speed with the draft head off, in [finding 29](../29_inkling2_mini_mtplx_2132). At these requests' sampler it shows no speed change I can call and gives the same replies. With top-p 0.95 it is 2.8 times as fast as 2.13.1. This page stays as the 2.13.1 record.

Updated on 23 Nov 2026 at 02:30 SGT with a section on thinking switched off, checked again on 2.13.1 at 02:21 SGT.

ELI5: MTPLX added Inkling 2 Mini on 22 Nov 2026 in three packs made for it. Bare Speed is the smallest, Optimized Speed keeps more of the model in 8 bits, and Optimized Quality is the maker's weights unchanged. I ran all three on MTPLX 2.13.1, the newest release, with the pack's draft head on and then off. I ran 2.13.0 earlier the same evening, and it gave the same text. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**MTPLX 2.13.1 wrote 159.7 tok/s on Inkling 2 Mini Bare Speed at its max, on its latest start, and 161.1 on the start before. With the model's own sampler it wrote 130.0. With the draft head off the same pack wrote 90.1 and 78.5, so the drafts gave 1.77 times at the max and 1.66 times at the median. The drafts did not change a reply, 100 of 100 the same text with them on and off, on every pack. Optimized Speed wrote 148.0 and 115.1, and Optimized Quality 136.5 and 106.7. Replies were reasoning text. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 22 Nov 2026.**

| Pack | Size | Max, drafts on | Median, drafts on | Max, drafts off | Median, drafts off |
|---|---|---|---|---|---|
| Bare Speed, latest start | 14.9 GiB | 159.7 | not run on this start | 90.1 | 78.5 |
| Bare Speed, first start | 14.9 GiB | 161.1 | 130.0 | | |
| Optimized Speed | 16.1 GiB | 148.0 | 115.1 | 82.4 | 69.4 |
| Optimized Quality | 18.8 GiB | 136.5 | 106.7 | 69.6 | 62.7 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **Drafts off** is the same server with `--no-mtp`, which MTPLX describes as "target-only AR generation". It is the baseline here, since `mlx-lm` 0.32.2 can't run this model.
- **The summary page shows the latest start** of Bare Speed, 159.7, by my rule. The two starts are level text by text, below.
- **These are reasoning speeds.** A benchmark that counts only answer tokens will show other numbers.
- **Each pack is different weights.** A gap between packs is the weights and the engine together.

## Chart

ELI5: The top speed on new code for each pack, with the draft head off and on. 1K prompt.

![Bars of writing speed in tokens per second for Inkling 2 Mini on MTPLX 2.13.1, greedy at temperature 0, new code, replies of up to 2,048 tokens, 1K prompt. Bare Speed, drafts off 90.1, drafts on 159.7. Optimized Speed, 82.4 and 143.4. Optimized Quality, 69.6 and 136.5.](chart_max.png)

- **The chart is the 1K prompt only.** Optimized Speed's max in the table is its 4K cell, 148.0.

## Drafts on and off

ELI5: The pack carries a small draft head that guesses several tokens ahead for the full model to check. With it off, the model writes one token a step. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s on MTPLX 2.13.1.

| Pack | Test | Prompt | Drafts off | Drafts on |
|---|---|---|---|---|
| Bare Speed | Greedy, new code, replies up to 2,048 tokens | 1K | 90.1 (89.8 to 90.4) | 161.1 (154.0 to 166.7), second start 159.7 (136.3 to 163.1) |
| Bare Speed | Greedy, new code, replies up to 2,048 tokens | 4K | 88.4 (88.2 to 89.2) | 146.6 (136.8 to 206.1), second start 152.6 (128.8 to 162.8) |
| Bare Speed | Greedy, new code, 512-token replies | 1K | 91.0 (90.9 to 91.2) | 153.9 (116.7 to 161.1) |
| Bare Speed | Own sampler, mixed text | 4K | 78.5 (78.0 to 79.7) | 130.0 (115.0 to 159.3) |
| Optimized Speed | Greedy, new code, replies up to 2,048 tokens | 1K | 82.4 (82.1 to 82.6) | 143.4 (135.1 to 164.9) |
| Optimized Speed | Greedy, new code, replies up to 2,048 tokens | 4K | 81.5 (81.3 to 82.4) | 148.0 (132.8 to 149.7) |
| Optimized Speed | Own sampler, mixed text | 4K | 69.4 (69.4 to 69.8) | 115.1 (103.2 to 129.9) |
| Optimized Quality | Greedy, new code, replies up to 2,048 tokens | 1K | 69.6 (69.4 to 69.7) | 136.5 (123.4 to 157.8) |
| Optimized Quality | Greedy, new code, replies up to 2,048 tokens | 4K | 68.9 (68.8 to 69.2) | 127.9 (115.0 to 146.9) |
| Optimized Quality | Own sampler, mixed text | 4K | 62.7 (62.7 to 62.8) | 106.7 (81.6 to 118.0) |

- **Text by text the drafts were faster on every pair, on every pack.**

| Pack | Long code replies | Short code replies | Own sampler |
|---|---|---|---|
| Bare Speed | 10 of 10, 1.77 | 10 of 10, 1.49 | 5 of 5, 1.67 |
| Optimized Speed | 10 of 10, 1.78 | 10 of 10, 1.55 | 5 of 5, 1.66 |
| Optimized Quality | 10 of 10, 1.91 | 10 of 10, 1.63 | 5 of 5, 1.70 |

- **The middle ratio** is the median of drafts on over drafts off, text by text. Bare Speed's second drafted start gave 1.75 on long replies.
- **Max.** 159.7 / 90.1 = 1.77 times drafts off on Bare Speed. 148.0 / 82.4 = 1.80 on Optimized Speed. 136.5 / 69.6 = 1.96 on Optimized Quality.
- **Plain decoding follows the pack's size.** 90.1, 82.4 and 69.6 tok/s for 14.9, 16.1 and 18.8 GiB. The five runs of each drafts-off cell sit within 1.7 tok/s.
- **With drafts on the packs come closer.** Optimized Quality, the largest, gained the most from the drafts.
- **The two Bare Speed drafted starts are level.** Text by text the second was faster on 5 of 10 long replies, with a middle ratio of 1.00.
- **The drafted runs spread widely.** One cell goes from 136.8 to 206.1. Drafted speed depends on how well the draft head guesses each text.

## The text, drafts on and off

ELI5: I asked the same 50 short questions twice on each start and compared the whole reply, thinking text included.

- **Drafts did not change the text.** Drafts on against drafts off, 100 of 100 replies were the same on each of the three packs.
- **One start repeated itself**, 50 of 50, on every start where I ran the check.
- **The packs wrote different text from each other**, as different weights do. On 2.13.0, Optimized Speed matched Bare Speed on 0 of 100 replies and Optimized Quality on 2 of 100.
- **This says nothing about which text is better.** I did not grade the answers.

## 2.13.1 against 2.13.0

ELI5: 2.13.0 came out at 13:21 SGT and 2.13.1 at 18:35 SGT. Its notes call it a fix for Inkling 2 Mini failing to load on M1 Macs and say an M5 gives the same tokens. I ran 2.13.0 first that evening and then 2.13.1, with the draft head on, on the same texts.

| Pack | Max, 2.13.1 | Max, 2.13.0 | Median, 2.13.1 | Median, 2.13.0 |
|---|---|---|---|---|
| Bare Speed, latest start | 159.7 | 153.6 | 130.0 | 120.2 |
| Optimized Speed | 148.0 | 159.0 | 115.1 | 112.5 |
| Optimized Quality | 136.5 | 131.7 | 106.7 | 104.1 |

- **The same text.** 100 of 100 replies matched 2.13.0 on each pack.
- **Level text by text.** On long code replies 2.13.1 was faster on 7 of 10 with a middle ratio of 1.03 on Bare Speed, 4 of 10 with 0.97 on Optimized Speed, and 5 of 10 with 1.01 on Optimized Quality. The other tests sat between 0.96 and 1.10, except one.
- **The one is the copy task on Bare Speed**, faster on 6 of 10 with 1.17. I published no copy line, as the next section says.
- **One median looks apart and is not.** Bare Speed's sampler reads 130.0 on 2.13.1 against 120.2 on 2.13.0. Text by text 2.13.1 was faster on only 2 of 5, with a middle ratio of 0.96, and its five runs went from 115.0 to 159.3.
- **So I see no speed change.** The 2.13.0 rows are in this folder.

## What the replies were

ELI5: The model thought before answering on every reply, as it did on the other engines. MTPLX sends that thinking in its own field, so the rows count it as reasoning.

- **Reasoning text.** Of the 180 timed replies on 2.13.1, 170 held 3 answer tokens at most and were reasoning otherwise. The other 10 closed their thinking and wrote some answer.
- **So I publish no copy or counting line.** The model spent those replies planning. Their rows are in `rows.csv` under `code_echo` and `code_count`.
- **Thinking.** These requests carry no thinking field, so the server's default applies. A read-back with thinking switched on gave reasoning text of the same length, 1,645 characters, as one with no field. The oMLX and mlx-serve runs of findings 16 and 20 sent thinking switched off, and the model reasoned there too.

## Thinking switched off

ELI5: The timed rows above send no thinking field. I also sent the switch that turns thinking off, `chat_template_kwargs: {"enable_thinking": false}`, as on oMLX and mlx-serve. MTPLX's log shows the model thinking anyway. Short replies came back empty, and a longer one sent only its answer. My reading is that MTPLX holds back the thinking text when thinking is off. No speed with thinking off is published.

- **MTPLX 2.13.0, 22 Nov 2026, 17:36 to 18:00 SGT, Bare Speed and the other two packs.** One plain request came back with `finish_reason` length, 512 completion tokens, 0 reasoning tokens, and an empty answer and reasoning field. MTPLX's own log for that kind of request shows the text starting with `<think>`. Most streamed timed requests got no text piece, so no speed could be timed. On the answer check, 50 short questions asked twice, 100 of 100 replies had no text.
- **MTPLX 2.13.1, 23 Nov 2026, 02:21 SGT, Bare Speed.** The answer check again, 64-token replies. 100 of 100 had no text, each counted as 64 tokens. MTPLX's log shows all 100 starting with `<think>`.
- **A longer request on 2.13.1 did return text.** A greedy 512-token request to write a short Python function streamed 58 pieces, 363 characters, starting with the code. The reasoning field was empty. Usage counted 512 tokens, 0 of them reasoning. MTPLX's log shows that reply also starting with `<think>`. My reading is that the thinking closed inside the limit and only the answer after it was sent. The log shows only the opening of each reply, so I can't confirm it.
- **With no thinking field, the same request** gave 1,372 characters of reasoning in its own field and 293 of answer, with 394 of the 512 tokens counted as reasoning.
- **Why no speed with thinking off.** Every token is counted, but text arrived only after the part the log shows as thinking, or not at all. A streamed speed would time part of the reply against the whole count. The 2.13.0 runs with thinking off are `636cf90090bb`, `443a8f8dae85`, `e7580e9c251f` and `7fb039e7b9da`. They stay out of `rows.csv`.
- **The 2.13.1 check run is `846fb9fe78de`.** It has no timed rows.
- **I did not try MTPLX's reasoning-effort setting.** Only the thinking switch.

## Reference points

ELI5: My usual baseline is Apple's `mlx-lm` on the same weights. Its newest release can't run this model, so the baseline is the same pack with the draft head off.

- **`mlx-lm` 0.32.2 has no Inkling 2 model.**
- **The mlx-serve pre-release on its own 8-bit pack** is in [finding 20](../20_inkling2_mini_mlxserve_pre), and oMLX on its oQ4e pack in [finding 16](../16_omlx_082_refresh). Other engines and other packs.
- **The MTPLX release notes** are [here](https://github.com/youssofal/MTPLX/releases/tag/v2.13.1). Their figures are from an M5 Max with other settings, and this page is not a comparison with them.

## The setup

ELI5: One engine at its newest release, its three packs, and a fresh server start for every setting.

- **Engine.** [MTPLX](https://github.com/youssofal/MTPLX) 2.13.1, released 22 Nov 2026 18:35 SGT, tag v2.13.1 at commit cf39588f. Installed from the tagged source with `uv sync --locked --no-dev --extra server --python 3.12`. `mtplx --version` prints 2.13.1. The 2.13.0 runs used tag v2.13.0 at bebe21b5, installed the same way.
- **Serve command.** The packs' cards give `mtplx serve --model <pack>` for any client. I passed the local folder and bound it to this Mac. Drafts off added `--no-mtp`.

```bash
mtplx serve --model <models>/inkling2-mini-mtplx-bare-speed --host 127.0.0.1 --port 8121 --context-window 131072 --no-stats-footer
```

- **What MTPLX reported.** `mtplx inspect` on Bare Speed read "tier: verified", "support_level: native-runtime", "mtp_layers: 3" and "recommended_profile: sustained". At start the log reads "Runtime contract verified, profile: sustained" and "Inkling 2 Mini drafter is active". MTPLX logs no per-request draft count.
- **Weights.** Every file was verified against the pinned commit.
  - [Youssofal/Inkling-2-Mini-MTPLX-Bare-Speed](https://huggingface.co/Youssofal/Inkling-2-Mini-MTPLX-Bare-Speed) @ 84a7701f, 14.9 GiB.
  - [Youssofal/Inkling-2-Mini-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Inkling-2-Mini-MTPLX-Optimized-Speed) @ f4174ad3, 16.1 GiB.
  - [Youssofal/Inkling-2-Mini-MTPLX-Optimized-Quality](https://huggingface.co/Youssofal/Inkling-2-Mini-MTPLX-Optimized-Quality) @ 35fa85b1, 18.8 GiB.
- **What the packs are, by MTPLX's release notes.** Bare Speed keeps the maker's 4-bit experts and stores the attention, head and embedding in 4 bits. Optimized Speed keeps the attention and head in 8 bits. Optimized Quality is the maker's weights unchanged. Each carries the model's draft head.
- **The model.** [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini), 26.4B weights with 3.4B active per token. Apache 2.0.
- **Hugging Face's security scan of the three packs was not finished** when I read it on 22 Nov 2026 at 17:27 SGT. No file was flagged. The files are safetensors, JSON, a chat template, a tokenizer model and text.
- **Sampler.** Temperature 1.0 and top-p 1.0, the model's own and the packs' cards'.
- **Server memory** at the end of each start, resident. Drafts on 15.7, 16.8 and 19.6 GiB for the three packs. Drafts off 17.9, 18.9 and 21.7 GiB.

| Run id | Release | Pack | Drafts | Started, SGT, 22 Nov 2026 |
|---|---|---|---|---|
| `0bb9739897e0` | 2.13.1 | Bare Speed | On | 19:44 |
| `472c4ceb9644` | 2.13.1 | Optimized Speed | On | 19:51 |
| `f0dac5df559b` | 2.13.1 | Optimized Quality | On | 19:57 |
| `69e9ae98c9d1` | 2.13.1 | Bare Speed, second start | On | 20:03 |
| `a96cb656f07d` | 2.13.1 | Bare Speed | Off | 20:06 |
| `0f6c20468d28` | 2.13.1 | Optimized Speed | Off | 20:14 |
| `a28a0a8eae9d` | 2.13.1 | Optimized Quality | Off | 20:23 |
| `15120ef4588c` | 2.13.0 | Bare Speed | On | 19:08 |
| `e8af192bf883` | 2.13.0 | Optimized Speed | On | 19:15 |
| `b06906a7e390` | 2.13.0 | Optimized Quality | On | 19:20 |
| `ea4c8fa3bbcf` | 2.13.0 | Bare Speed, second start | On | 19:26 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as findings 5 to 20.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. On this model's tokenizer the code prompts came to 1,062 to 2,071 tokens and 4,414 to 6,075.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last, reasoning tokens included.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Reasoning text is not answer text.** Nothing here is an answer speed.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **One start per setting, and two for Bare Speed with drafts on.**
- **The release is hours old.** A setting I missed is likely. Tell me and I will rerun it.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 318 raw rows from the bench database. 285 timed requests and 33 warm-ups, on both releases.
- **`runs.csv`.** The 11 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/21_inkling2_mini_mtplx_213
```

## What I did not verify

- **Other thinking settings.** Every timed request here sent no thinking field. Thinking switched off has its own section, with no speeds. I did not try the reasoning-effort setting.
- **MTPLX's Mac app and `mtplx start`.** I ran the server only.
- **A second start** of Optimized Speed, Optimized Quality, drafts off, and the sampler block.
- **What the timed replies say.** I read back two copy replies on Bare Speed and the short previews of the answer check.
- **What the fewer bits of the speed packs cost in quality.**
- **Long prompts, several users at once, and images.**

## Credit

- **Engine and packs.** [MTPLX](https://github.com/youssofal/MTPLX) by [@Youssofal_](https://x.com/Youssofal_).
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
