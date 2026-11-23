# Finding 31. Inkling 2 Mini on Ollama 0.40.17, its drafter 2.3 times as fast, with the thinking hidden

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Updated on 23 Nov 2026 at 16:25 SGT with one start at Ollama's default thinking. See that section.

ELI5: Ollama 0.40.17 added Inkling 2 Mini on Apple chips. Its library model is Thinking Machines' own release with the model's MTP drafter attached. I built that same model here from the maker's files with Ollama's own import, and it matches Ollama's library model tensor for tensor. Then I ran it with the drafter on and off. With thinking off the model still thinks, and Ollama hides that thinking from the reply. So every speed here is Ollama's own count of the tokens it decoded, hidden thinking included.

**Ollama 0.40.17 decoded Inkling 2 Mini at 76.8 tok/s at its max with its MTP drafter, and 51.0 with the model's own sampler, by Ollama's own count. With no drafter it decoded 33.6 and 32.4. So the drafter made greedy decoding on code prompts 2.3 times as fast, faster on 20 of 20 same-text pairs, and the sampler 1.6 times. With thinking off, Ollama asks for thinking effort 0, as the maker's template does for "none", and the model still thought before it answered. Ollama drops that thinking from the reply. So 27 of 40 greedy replies to code prompts, capped at 2,048 tokens, came back with no text, and so did all 60 of the replies capped at 512. Most decoded tokens were that thinking, not code. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Setting | Max, tok/s | Median, tok/s |
|---|---|---|
| MTP drafter on, as in Ollama's library model | 76.8 | 51.0 |
| No drafter | 33.6 | 32.4 |

- **Max** is the middle of 5 greedy runs on new code prompts with replies capped at 2,048 tokens, at the faster of the 1K and 4K prompts. Most of the decoded tokens were hidden thinking, not code.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt. The requests sent temperature 1.0 and top-p 1.0. Ollama's OpenAI route has no top-k field, so Ollama's default top-k of 40 applies, by its source (`api/types.go`). The other Inkling 2 Mini pages sample with no top-k.
- **Speed is Ollama's own decode rate,** `predicted_per_second` in each row's `extra` column. It is the tokens Ollama decoded over the time it spent decoding them, hidden thinking included. The harness's own writing speed starts at the first visible token, so here it is wrong or empty.
- **Where that figure comes from.** Ollama's OpenAI route streams a `timings` object, with `predicted_per_second` set to its eval count times 1,000 over its eval time in milliseconds (`openai/openai.go`). The harness stores it as sent. On all 100 timed rows it agrees with the decoded tokens over the request's own clock, less Ollama's prompt time, within 0.33%.
- **The arithmetic.** 76.8 / 33.6 = 2.29 at the max. 51.0 / 32.4 = 1.57 at the median.
- **Both lines are their latest start.** The first drafter start decoded 82.2 at the max and 55.3 with the sampler. The first start with no drafter decoded 33.5 and 32.2.
- **Ollama's library model always carries the drafter.** No drafter is an import without it, made here only to measure the drafter.
- **No `mlx-lm` multiple.** `mlx-lm` 0.32.2 has no Inkling 2 model. The line with no drafter is the baseline.

## Ollama's default thinking, one more start

ELI5: Added on 23 Nov 2026 at 16:25 SGT. With no thinking field Ollama asks for effort 0.9 and sends the thinking back in its own field. Then the harness can see every token, which checks the clock this page uses, and shows what a user with Ollama's default gets.

- **One drafter start,** run `b5f573f87f3c` at 16:13 SGT, the same library model and Modelfile, no thinking field sent.
- **Every reply was thinking.** All 2,048 or 512 tokens of each of the 25 timed replies came back in the reasoning field, and none as answer text within the cap.
- **The two clocks agree.** The harness's writing speed and Ollama's own count differ by at most 0.7% on all 25 rows. So where the harness can see the tokens, it reads what Ollama's count reads.
- **Speeds, harness clock, middle of 5.** Code 1K capped at 2,048, 76.6 tok/s. Code 4K capped at 2,048, 82.3. Code 1K capped at 512, 80.7. Code 4K capped at 512, 64.8. Mixed 4K with the sampler, 61.7.
- **So Ollama's default reads 82.3 at the max and 61.7 with the sampler.** These are on the summary page as Ollama's line, labelled as reasoning text.
- **The first token came at once.** 0.61 s at 1K and 2.51 s at 4K, the middle of 5.
- **Not the same text as thinking off.** Effort 0.9 thinks differently from effort 0, so these are not same-text pairs with the starts above.

## Chart

ELI5: The same model with the drafter off and on. The drafter roughly doubles every greedy test and helps the sampler less. The bars name the prompt and the reply cap, since most replies were hidden thinking.

![Paired bars of decode speed in tokens per second, by Ollama's own count, for Inkling 2 Mini on Ollama 0.40.17, no drafter against the MTP drafter on. Code prompt at 1K, replies capped at 2,048 tokens, 33.6 and 76.8. The same at 4K, 33.2 and 75.8. Code prompt at 1K, capped at 512, 33.2 and 65.6. Mixed text at 4K with the model's own sampler, 32.4 and 51.0.](chart_draft.png)

## The same model as Ollama's library

ELI5: Ollama's `ollama pull` fetches its library model from Ollama's servers. This bench downloads weights only through its own pinned, checked download. So I rebuilt the library model from the maker's files and compared the two, piece by piece.

- **Weights.** [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) @ b85c3cfa, 18.8 GiB, every file checked against its SHA-256 or git fingerprint. Its tensors last changed in the upload commit of 21 Nov 2026 06:02 SGT, before Ollama's tag.
- **The drafter.** The release's `mtp.safetensors`, imported with the Modelfile's `DRAFT` line, beside a `config.json` made from the release's own `mtp_config`. That file has the same SHA-256 as the library model's `draft/config.json`.
- **The Modelfile.**

```text
FROM <folder of the release's files>
DRAFT <folder with mtp.safetensors and its config.json>
RENDERER inkling2
PARSER inkling2
REQUIRES 0.40.17
```

- **Compared with Ollama's library manifest,** read from Ollama's registry on 23 Nov 2026 at 13:58 SGT, metadata only, no weights.
  - All 1,250 tensors have the library model's digests, the 54 drafter tensors among them.
  - The image config, which names the renderer, the parser and the drafter, has the library's digest.
  - 7 of the 8 config files have the library's digests. `config.json` differs. The release's copy carries keys the library's lacks, such as `dtype`, which the release added on 21 Nov 2026 at 06:55 SGT. Ollama's Inkling runner reads none of the keys that differ, by its source (`mlxrunner/model/inkling2/config.go`).
  - The library model also carries a licence file, which I did not add.
- **The import without the drafter** has the same 1,196 other tensors. Only the 54 `draft.` tensors are missing.
- **The runner.** `ollama ps` showed `mlx` for every start.

## Thinking off hides the thinking

ELI5: Inkling 2 Mini has a thinking dial from 0 to 0.99. Thinking off sets it to 0. At 0 the model still wrote a thinking section first on these prompts. Ollama keeps that section out of the reply, so a capped reply could end before any answer appeared.

- **What Ollama asks for.** With `reasoning_effort` "none", Ollama 0.40.17 writes "Thinking effort level: 0" into the prompt, by its source (`model/renderers/inkling2.go`). The release's own chat template writes the same line for "none".
- **What the model wrote.** One untimed raw request, the same prompt written the way Ollama writes it, 300 tokens, greedy. The text began `<|message_model|><|content_thinking|>The user asks for a Python function returning n-th Fibonacci number`. That is a thinking section.
- **What Ollama returned.** The same prompt through Ollama's chat with thinking off returned 316 characters of answer and no thinking, from the same 300 tokens. The raw request returned 1,169 characters. Ollama's Inkling parser drops the thinking section when thinking is off, by its source (`model/parsers/inkling2.go`).
- **Replies with no text, all four starts.**
  - Greedy, code prompts, capped at 2,048 tokens. 10 of 20 at 1K had visible text, and 3 of 20 at 4K.
  - Greedy, code prompts, capped at 512 tokens. 0 of 40.
  - The sampler, capped at 512 tokens. 0 of 20.
- **The wait before any text.** With the drafter, on code prompts at 1K capped at 2,048, the first visible text came 4.8 to 24.8 s after the request, on the 5 replies that had any. With no drafter it came 20.5 to 59.6 s after, on 5.
- **Other engines at effort "none".** MTPLX streamed about 2,046 of 2,048 tokens as reasoning text on the same 4K code prompts ([finding 29](../29_inkling2_mini_mtplx_2132)). Strata answered at once, since its Inkling engine has no thinking mode ([finding 30](../30_inkling2_mini_strata_0220)).
- **Thinking "low",** effort 0.2, returned all 300 tokens as thinking, in its own field.

## The drafter on and off

ELI5: A drafter guesses several tokens and the model checks them in one step. Here the guesses landed about half the time on greedy replies to code prompts, so each step wrote more than three tokens.

Decode tok/s by Ollama's own count. Each cell is the middle of 5 runs. Greedy except the sampler.

| Test | No drafter, `9a9a2ca51a2d` | No drafter, `73fd93e9251b` | Drafter on, `9ed0d4ec4190` | Drafter on, `f09bb0f8b45f` |
|---|---|---|---|---|
| Code 1K, cap 2,048 | 33.5 | 33.6 | 82.2 | 76.8 |
| Code 4K, cap 2,048 | 33.1 | 33.2 | 75.7 | 75.8 |
| Code 1K, cap 512 | 33.1 | 33.2 | 68.4 | 65.6 |
| Code 4K, cap 512 | 32.7 | 32.7 | 64.8 | 67.1 |
| Mixed 4K, own sampler | 32.2 | 32.4 | 55.3 | 51.0 |

- **Text by text, against `73fd93e9251b`.** With the 2,048 cap the drafter starts read middle ratios of 2.42 and 2.30, then 2.29 and 2.29, faster on 5 of 5 pairs each, 20 of 20 in all. With the 512 cap they read 1.97 to 2.06, 20 of 20. The sampler read 1.71 and 1.57, 10 of 10.
- **The two starts with no drafter agree.** Middle ratio 1.00 on every greedy cell and 0.99 on the sampler.
- **What the drafter did, by Ollama's own log, latest drafter start.** On code prompts capped at 2,048 it kept 48.6% of its drafts at 1K and 47.6% at 4K, and each check step decoded 3.40 and 3.33 tokens. With the sampler it kept 34.1%, and each step decoded 2.26 tokens. Each log line was matched to its timed request by its end time.
- **Draft depth.** Ollama sets the depth itself, up to 7 drafted tokens a step here, since the drafter was trained on blocks of 8 (`mlxrunner/model/inkling2/draft.go`). In 0.40.17 the MLX runner does not read `draft_num_predict`, by its source at tag 23b94a2d.
- **Did the drafter change the text?** One reply says no, and the rest could not tell. The field check's 256-token reply had the same hash with the drafter on and off, 187 visible characters each. The 50-question check asks for 64-token replies, and every one of the 100 came back empty on both settings.

## Against other engines, with drafting off

ELI5: With drafting off an engine writes one token a step whatever the text, so plain decoding is the fairest line to set beside other engines. The weights differ.

Max with drafting off, by finding. The pack sizes are on disk.

- **mlx-serve 26.11.4 pre-release, its 8-bit pack, 17.5 GiB.** 107.4 tok/s, [finding 20](../20_inkling2_mini_mlxserve_pre). Its card says its experts are the release's own bytes.
- **Rapid-MLX 1.1.0, 4-bit, 16.1 GiB.** 39.8, [finding 23](../23_inkling2_mini_rapidmlx_110).
- **oMLX 0.8.3, oQ4e, 15.7 GiB.** 62.4, [finding 26](../26_omlx_083_refresh).
- **MTPLX 2.13.2, Bare Speed pack, 14.9 GiB.** 89.9, [finding 29](../29_inkling2_mini_mtplx_2132).
- **Strata 0.2.20, SQ-20, 18.6 GiB.** 61.5, [finding 30](../30_inkling2_mini_strata_0220).
- **Ollama 0.40.17, the maker's release, 18.8 GiB.** 33.6, this page. Two things set it apart. It is an import made here without the drafter, which Ollama's library model always carries. And it is Ollama's own decode count, where the others are the harness's clock on streamed text.
- **These are different weights and sizes, and not a ranking.**

## The setup

ELI5: Ollama's own release, run as its docs say, with the library model rebuilt from the maker's files.

- **Engine.** [Ollama](https://github.com/ollama/ollama) 0.40.17, a full release, tag `v0.40.17` at commit 23b94a2d of 21 Nov 2026 11:03 SGT. `ollama-darwin.tgz` matched GitHub's SHA-256 digest, starting 4b9db20d. Its notes add Inkling 2 Mini on Apple silicon.
- **It was still the newest release** when I published this, checked on 23 Nov 2026 at 16:07 SGT.
- **Server.** `ollama serve` bound to this Mac, with `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_CONTEXT_LENGTH=32768`, `OLLAMA_KEEP_ALIVE=-1` and `OLLAMA_NO_CLOUD=1`. Each start ran `ollama create` with the Modelfile above first, which took about 12 s.
- **Requests.** Ollama's OpenAI-style chat route, streamed, with `reasoning_effort` "none".

| Run id | Setting | Started, SGT, 23 Nov 2026 |
|---|---|---|
| `9ed0d4ec4190` | Drafter on | 15:05 |
| `9a9a2ca51a2d` | No drafter | 15:16 |
| `73fd93e9251b` | No drafter | 15:36 |
| `f09bb0f8b45f` | Drafter on | 15:51 |
| `b5f573f87f3c` | Drafter on, Ollama's default thinking | 16:13 |

- **One earlier start is left out.** Run `b0d94bae1783` at 14:58 SGT used a Modelfile with no `RENDERER` or `PARSER` line, so the prompt went in without Inkling's chat format. I stopped it after one timed request.

## How I measured

ELI5: Same Mac, same harness, same texts and same questions as the other Inkling 2 Mini pages. Only the clock differs.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Greedy** means temperature 0.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. Each prompt opens with a new session line so no prompt cache can hit.
- **Repeats.** 5 timed runs per cell, starts in the order drafter on, off, off, on. Each block of cells began with one 16-token warm-up request.
- **Nearly every reply hit its cap.** Ollama decoded the full 2,048 or 512 tokens on 99 of the 100 timed requests. One reply to a code prompt, capped at 2,048, stopped at 1,968.

## Things to know before you compare

- **Hidden thinking, not answer text.** Most decoded tokens were thinking that Ollama did not return. MTPLX's pages time the same kind of text, shown as reasoning. Strata's page times answer text.
- **The sampler here is not the other pages' sampler.** Ollama adds top-k 40.
- **Greedy replies were not the same from start to start.** With no drafter, 3 and then 2 of the same 5 code prompts at 1K, capped at 2,048, had visible text.
- **Max is not what a chat feels like.** A capped reply here may show nothing at all.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 140 raw rows from the bench database, with Ollama's own timing in the `extra` column.
- **`runs.csv`.** The 5 runs, with engine, version, start time and settings.
- **The harness's summary reads its own clock.** `tools/summarize.py` shows writing speed from the first visible token, which is wrong for these rows. Use `predicted_per_second` in `extra`.
- **On the summary page, the thinking-on start only.** The summary page measures the harness's clock on rows with visible text. The thinking-off starts have few such rows and a wrong clock, so only run `b5f573f87f3c` stands there.

## What I did not verify

- **Whether the drafter changes the replies.** One reply matched, and the text check came back empty.
- **Ollama's default beyond one start.** With no thinking field, Ollama asks for effort 0.9 and shows the thinking in its own field, by its source (`inkling2Effort`). I timed that once, with the drafter, above. Not with the drafter off, and not past the reply caps.
- **Ollama's ready-made library model itself.** I compared its manifest, not its files.
- **Why the model thinks at effort 0 on these prompts.** I saw that it does, not why.
- **Answer quality, long prompts, pictures, tools and two users at once.** Ollama's notes say it now serves several requests at once on Apple silicon.

## Credit

- **Engine.** [Ollama](https://github.com/ollama/ollama), [@ollama](https://x.com/ollama).
- **Model and drafter.** Inkling 2 Mini by [Thinking Machines](https://x.com/thinkymachines).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
