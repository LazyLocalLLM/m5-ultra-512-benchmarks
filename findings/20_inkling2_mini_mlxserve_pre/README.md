# Finding 20. Inkling 2 Mini on the mlx-serve 26.11.4 pre-release, max and median speed

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: mlx-serve's author released a pre-release on 22 Nov 2026 that adds Inkling 2 Mini, with an 8-bit pack made for it. A pre-release is not a stable release yet. Its code is the project's main branch at commit 2fe9be83, so I ran it and label every figure with that. I'll rerun it when 26.11.4 ships. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**mlx-serve 26.11.4-pre-release.1 wrote 146.8 tok/s on Inkling 2 Mini at its max, on its latest start, and 160.5 on the start before. With the model's own sampler it wrote 104.5. With its drafts off the same pack wrote 107.4, so text by text the drafts were faster on all 10 long code replies, with a middle ratio of 1.32. Every reply I read back was reasoning text, though the request switched thinking off. The server held 16.7 GiB. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 22 Nov 2026.**

| Setting | Max, tok/s | Median, tok/s |
|---|---|---|
| Drafts on, the engine's defaults, latest start | 146.8 | not run on this start |
| Drafts on, the engine's defaults, first start | 160.5 | 104.5 |
| Drafts off | 107.4 | not run |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The summary page shows the latest start**, 146.8, by my rule. The two starts are level text by text, below.
- **These are reasoning speeds, by the replies I read back.** The rows count them as answer tokens. The section "What the replies were" says why. A benchmark that counts only answer tokens may show other numbers.
- **Pre-release.** mlx-serve [v26.11.4-pre-release.1](https://github.com/ddalcu/mlx-serve/releases/tag/v26.11.4-pre-release.1), main at 2fe9be83, not in a stable release yet. The newest stable release was 26.11.3.

## Chart

ELI5: The top speed on new code for each setting. One bar per start and prompt size.

![Bars of writing speed in tokens per second for Inkling 2 Mini on the mlx-serve 26.11.4 pre-release, greedy at temperature 0, new code, replies of up to 2,048 tokens. At a 1K prompt, drafts off 107.4, drafts on first start 160.5, drafts on second start 146.8. At 4K, 105.6, 131.3 and 138.7.](chart_max.png)

## Drafts on and off

ELI5: The engine guesses several tokens ahead and the model checks them. With the guesses off, the model writes one token a step. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets.

Decode tok/s. The first drafted start is run `338b6385675f`, the second is `3f129b289ed7`, and drafts off is `8dddc3d76174`.

| Test | Prompt | Drafts off | Drafts on, first start | Drafts on, second start |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 107.4 (106.9 to 107.4) | 160.5 (133.8 to 162.1) | 146.8 (131.4 to 162.8) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 105.6 (105.4 to 106.0) | 131.3 (115.8 to 155.0) | 138.7 (112.5 to 140.2) |
| Greedy, new code, 512-token replies | 1K | 107.9 (106.8 to 108.2) | 124.9 (114.8 to 143.7) | not run |
| Greedy, new code, 512-token replies | 4K | 106.4 (105.6 to 107.0) | 125.4 (107.4 to 139.3) | not run |
| Own sampler, mixed text, 512-token replies | 4K | not run | 104.5 (102.9 to 107.3) | not run |

- **Max.** 146.8 tok/s on the latest start. 146.8 / 107.4 = 1.37 times drafts off.
- **Text by text the drafts were faster on every pair.** Long replies, 10 of 10 on each drafted start, with a middle ratio of 1.32 both times. Short replies, 10 of 10, with 1.16.
- **Plain decoding is about 107 tok/s whatever the text.** The five runs of each drafts-off cell sit within 1.4 tok/s of each other.
- **The drafted runs spread widely.** One cell goes from 115.8 to 155.0. Drafted speed depends on how well the guesses land on each text.
- **The two drafted starts are level.** Text by text the second was faster on 4 of 10 long replies, with a middle ratio of 0.99. So 160.5 and 146.8 are one setting read twice.
- **19 of 20 drafted long replies ran to 2,048 tokens.** One stopped at 1,871 on the second start. All 10 drafts-off long replies ran to 2,048.
- **The log shows the drafts at work.** On the drafted starts each request logs "spec=dspark (inkling2_loop native draft stages, block=8)", "mtp=enabled (streaming, depth=6)" and "pld=enabled (draft_len=5, key_len=3)". The drafts-off start logs "pld=off" and none of those lines.

## What the replies were

ELI5: The request asked the model not to think. It thought anyway, as it did on oMLX in [finding 14](../14_inkling2_mini_omlx_081). So the speeds are of thinking text.

- **Reasoning text.** I read back one copy reply and one counting reply. Of 512 tokens, the server counted 507 and 509 as reasoning, and the answer text was empty in both.
- **The timed rows say answer tokens.** The timed replies were streamed, and mlx-serve sent every streamed token in the answer field, with no reasoning field. So `rows.csv` counts them as answer tokens, 512 of 512. The read-backs and the answer check were not streamed, and there the server split the reasoning out.
- **So the reasoning reading rests on those replies.** I did not save the text of the streamed replies, so I can't show it. The model thought on every reply I could read, as on oMLX.
- **The answer check agrees.** 50 short greedy questions asked twice, 64 tokens each. All 100 replies were reasoning text with an empty answer.
- **So I publish no copy or counting line.** The model spent those replies planning. Their rows are in `rows.csv` under `code_echo` and `code_count`.
- **The release notes say Inkling models now follow the reasoning effort a client asks for.** I sent the thinking switch, not an effort setting. I did not try the effort setting.

## The text with drafts on

ELI5: I asked the same 50 short questions twice on one drafted start and compared the whole reply, thinking text included.

- **The second reply equalled the first on 43 of 50.** With greedy decoding and every guess checked, the text would not change. On this start it did on 7 of 50.
- **The same check on oMLX** gave 47 of 50 on 0.8.1, and 46 and 48 of 50 on two 0.8.2 starts, in findings 14 and 16. That is another engine and another pack.
- **I did not run the check with drafts off** on this engine.
- **This says nothing about which text is better.** I did not grade the answers.

## Reference points

ELI5: My usual baseline is Apple's `mlx-lm` on the same weights. Its newest release can't run this model, so the baseline here is the same pack with drafts off.

- **The baseline is drafts off on mlx-serve**, 107.4 tok/s, above.
- **`mlx-lm` 0.32.2 has no Inkling 2 model.** The pack's card says it loads in an `mlx-lm` pull request. That is unmerged code, so I did not run it.
- **oMLX 0.8.2 on its own oQ4e pack** is in [finding 16](../16_omlx_082_refresh). That is another engine and another pack, a different number of bits.

## The setup

ELI5: One engine at its pre-release, the author's own pack, and a fresh server start for every setting.

- **Engine.** [mlx-serve](https://github.com/ddalcu/mlx-serve) v26.11.4-pre-release.1, published 22 Nov 2026 13:27 SGT, marked pre-release. The release's own macOS tarball, `mlx-serve-bin-macos-arm64.tar.gz`, its SHA-256 equal to the digest GitHub lists (510de30e...). Unpacked into its own folder and run as shipped, with nothing patched. The project's Homebrew formula was still at 26.11.3.
- **Version.** `mlx-serve --version` prints "mlx-serve 26.11.4-pre-release.1 (fast)" with mlx 0.32.5. The tag is commit 2fe9be83, the same as main by GitHub's compare that day.
- **Serve command.** The author's documented command is `mlx-serve --model ddalcu/Inkling-2-Mini-MLX-8bit --serve`. I passed the local folder and bound it to this Mac.

```bash
mlx-serve --model <models>/inkling2-mini-mlxserve-8bit --serve --host 127.0.0.1 --port 8221 --ctx-size 131072 --max-concurrent 1
```

- **Drafts off** added `--no-mtp --no-drafter --no-pld`.
- **Weights.** [ddalcu/Inkling-2-Mini-MLX-8bit](https://huggingface.co/ddalcu/Inkling-2-Mini-MLX-8bit) @ cb7fa052, 17.5 GiB. Every file was verified against the pinned commit. The card says the experts are the release's own bytes, NVFP4 on layers 0 to 19 and MXFP8 on 20 to 23, with the attention, embedding and head in 8-bit.
- **The model.** [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini), 26.4B weights with 3.4B active per token. Apache 2.0.
- **Hugging Face's security scan of the pack was not finished** when I read it on 22 Nov 2026 at 17:27 SGT. No file was flagged. The files are safetensors, JSON, a chat template and text.
- **Sampler.** Temperature 1.0 and top-p 1.0, the model's own.
- **Thinking** switched off in every request, with `enable_thinking: false` at the top level and in `chat_template_kwargs`.

| Run id | Setting | Started, SGT, 22 Nov 2026 |
|---|---|---|
| `338b6385675f` | Drafts on, defaults | 18:00 |
| `3f129b289ed7` | Drafts on, defaults, second start | 18:08 |
| `8dddc3d76174` | Drafts off | 18:11 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as findings 5 to 19.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. On this model's tokenizer the code prompts came to 1,060 to 2,069 tokens and 4,412 to 6,074.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last, reasoning tokens included.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Reasoning text is not answer text.** Nothing here is an answer speed.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **A pre-release can change before it ships.** I'll rerun on the stable release.
- **Different packs are different weights.** This 8-bit pack is not the oQ4e pack of findings 14 and 16.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 83 raw rows from the bench database. 75 timed requests and 8 warm-ups.
- **`runs.csv`.** The 3 runs behind them, with engine, version, start time, settings and sampling.

From the top of this repository.

```bash
python3 tools/summarize.py findings/20_inkling2_mini_mlxserve_pre
```

## What I did not verify

- **The stable release.** 26.11.4 was not out yet.
- **The model with thinking truly off**, and the effort setting.
- **The sampler with drafts off**, and the answer check with drafts off.
- **A second start of the sampler block.**
- **What the timed replies say.** I read back two replies and the short previews of the answer check.
- **Answer quality, long prompts, several users at once, and images.**

## Credit

- **Engine and pack.** [mlx-serve](https://github.com/ddalcu/mlx-serve) by [@ddalcu](https://x.com/ddalcu).
- **Model.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
