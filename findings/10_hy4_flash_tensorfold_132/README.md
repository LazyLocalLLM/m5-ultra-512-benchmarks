# Finding 10. Tencent Hy4-flash on TensorFold 1.3.2, max and median speed

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: Hy4-flash is Tencent's new open model, released on 16 Nov 2026. TensorFold was the only engine I found that loaded it when I ran this. oMLX 0.8.1 loads it too, and that run is [finding 12](../12_hy4_flash_omlx_081). I ran its two MLX builds, with the engine's drafts on and off. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**At its defaults TensorFold 1.3.2 wrote 65.3 and then 64.6 tok/s on Hy4-flash 4-bit at its max, on a morning and an evening start, and 50.8 and 47.6 on the 8-bit build. Thinking was on, the model's default. With the model's own sampler it wrote 50.0 and 51.3, and 36.8 and 37.1. One switch from the engine's source, `TF_HY4_DRAFT_BITS=8`, was faster on every code text on both builds on two starts each. Against the default start of the same evening it wrote 71.5 against 64.6 on the 4-bit build and 53.4 against 47.6 on the 8-bit build, with the same text on 100 of 100 short replies. With drafts off the builds wrote 42.2 and 34.0 on code at a 4K prompt. Nearly every timed reply was reasoning text from start to finish. With thinking switched off through the API the replies went off course on both builds, so I publish no thinking-off line.**

Updated on 21 Nov 2026 at 20:27 SGT. The draft switch has its second starts and an answer check, in the section "Draft switches, the second starts". By my rule the summary page now shows the evening default starts, and the switch as its own labelled line. The section "Thinking on, the model's default" still holds the morning starts.

Runs of 21 Nov 2026 SGT. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs.

| Build | Size on disk | Max, tok/s | Median, tok/s | Max with the switch | Median with the switch | Drafts off, code | Drafts off, own sampler |
|---|---|---|---|---|---|---|---|
| Hy4-flash 4-bit | 121.0 GiB | 64.6 | 51.3 | 71.5 | 51.0 | 42.2 | 41.3 |
| Hy4-flash 8-bit | 222.9 GiB | 47.6 | 37.1 | 53.4 | 40.9 | 34.0 | 33.2 |

- **Max** is the middle of 5 greedy runs on new code, replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The first four number columns are the evening starts**, the latest start of each setting. The morning default starts wrote 65.3 and 50.0 on the 4-bit build and 50.8 and 36.8 on the 8-bit build.
- **The switch** is `TF_HY4_DRAFT_BITS=8` in the server's environment. It is in the engine's source and not in its docs.
- **Drafts off** is the same server with `--no-drafts`, 512-token replies, 4K prompt, from the morning.
- **No `mlx-lm` baseline.** Apple's `mlx-lm` 0.32.2 has no model file for this model type, and neither had its main branch on 21 Nov 2026. oMLX 0.8.0 has none either. I did not try the other engines on this Mac. The drafts-off column is the reference here.

## Chart

ELI5: The top speed on new code for each build at two prompt sizes, at the defaults and with the draft-bits switch. These are the evening starts.

![Bars of writing speed in tokens per second for Hy4-flash on TensorFold 1.3.2, greedy at temperature 0, new code, thinking on, replies of up to 2,048 tokens, at the defaults and with TF_HY4_DRAFT_BITS=8. The 4-bit build writes 64.6 and 71.5 at a 1K prompt, and 60.4 and 70.7 at 4K. The 8-bit build writes 47.6 and 53.4 at 1K, and 46.8 and 52.0 at 4K.](chart_max.png)

## Thinking on, the model's default

ELI5: Hy4-flash thinks before it answers unless told not to. These runs leave that alone. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets. These are the morning starts, the only ones with a drafts-off start beside them.

### Hy4-flash 8-bit

Tok/s, run `bdcd2d9ede41` with drafts on and `b8e543b952e1` with drafts off.

| Test | Prompt | Drafts on | Drafts off | Times drafts off |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 50.8 (46.4 to 55.0) | not run | |
| Greedy, new code, replies up to 2,048 tokens | 4K | 50.4 (43.5 to 51.3) | not run | |
| Greedy, new code, 512-token replies | 1K | 50.8 (46.5 to 52.1) | 34.4 (33.2 to 34.6) | 1.48 |
| Greedy, new code, 512-token replies | 4K | 46.5 (43.7 to 48.1) | 34.0 (33.9 to 34.2) | 1.37 |
| Own sampler, mixed text, 512-token replies | 4K | 36.8 (35.7 to 47.5) | 33.2 (33.2 to 33.3) | 1.11 |

- **Max.** 50.8 tok/s, greedy on new code at a 1K prompt, at both reply lengths.
- **Median.** 36.8 tok/s with the model's own sampler. Another start wrote 36.9 (36.2 to 44.9), run `10884ddb9c17`.
- **Drafts are worth 1.48 times on code at 1K.** 50.8 / 34.4 = 1.48. Drafts on was faster on 5 of 5 texts in each of the three cells.
- **Drafts are worth 1.11 times on sampled text.** 36.8 / 33.2 = 1.11.
- **Memory.** The server process held 313.3 GiB after loading and 346.7 GiB at the end of the drafts-on start, by `ps`. Its log says it keeps 163.6 GiB wired between requests.
- **Load time.** 20.9 to 26.8 s over four starts, by the server's banner.

### Hy4-flash 4-bit

Tok/s, run `b1f754c43ae4` with drafts on and `df5b641735e6` with drafts off.

| Test | Prompt | Drafts on | Drafts off | Times drafts off |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 63.2 (58.3 to 65.9) | not run | |
| Greedy, new code, replies up to 2,048 tokens | 4K | 65.3 (62.4 to 67.3) | not run | |
| Greedy, new code, 512-token replies | 1K | 57.5 (52.4 to 83.5) | 43.0 (41.1 to 43.0) | 1.34 |
| Greedy, new code, 512-token replies | 4K | 58.8 (52.4 to 66.8) | 42.2 (42.1 to 42.4) | 1.39 |
| Own sampler, mixed text, 512-token replies | 4K | 50.0 (43.7 to 55.6) | 41.3 (41.1 to 41.4) | 1.21 |

- **Max.** 65.3 tok/s, greedy on new code with replies of up to 2,048 tokens at a 4K prompt.
- **Median.** 50.0 tok/s with the model's own sampler. Another start wrote 47.2 (43.3 to 50.5), run `cad62d9be2d7`.
- **Drafts are worth 1.39 times on code at 4K.** 58.8 / 42.2 = 1.39. Drafts on was faster on 5 of 5 texts in each of the three cells.
- **Drafts are worth 1.21 times on sampled text.** 50.0 / 41.3 = 1.21.
- **The 4-bit build is 1.29 times the 8-bit build at max.** 65.3 / 50.8 = 1.29. With drafts off on code at 4K it is 42.2 / 34.0 = 1.24 times.
- **Memory.** The server process held 168.7 GiB after loading and 196.3 GiB at the end of the drafts-on start, by `ps`. Its log says it keeps 91.4 GiB wired between requests.
- **Load time.** 13.8 to 14.2 s over five starts on 1.3.2, by the server's banner.

### What the replies were

- **Reasoning text.** 89 of the 90 timed replies here spent their whole budget inside the thinking block, 2,048-token replies included. One 4-bit reply closed its thinking at 1,667 tokens and wrote 381 answer tokens.
- **So these are speeds of reasoning text.** A benchmark that counts only answer tokens will show other numbers.

## Draft switches, a first screen

ELI5: The model drafts a few tokens ahead with a small helper, DFly2, and then checks the drafts. TensorFold's source lists two switches for this model. One stores the helper at fewer bits. The other moves the model's lookup tables into memory. I tried each on one start. Storing the helper at 8 bits was faster on every text. This was the first screen. The second starts are in the next section.

Thinking on, drafts on, TensorFold 1.3.2, one start per row, tok/s, 21 Nov 2026.

Hy4-flash 4-bit.

| Setting | Run | Own sampler, 4K | Code, 512, 1K | Code, 512, 4K | Code, up to 2,048, 1K | Code, up to 2,048, 4K |
|---|---|---|---|---|---|---|
| Defaults, the start above | `b1f754c43ae4` | 50.0 (43.7 to 55.6) | 57.5 (52.4 to 83.5) | 58.8 (52.4 to 66.8) | 63.2 (58.3 to 65.9) | 65.3 (62.4 to 67.3) |
| Defaults, another start | `d341be8cafd5` | 45.1 (40.2 to 48.1) | 62.3 (54.9 to 73.3) | 57.1 (55.1 to 64.3) | 65.0 (54.3 to 70.5) | 62.4 (60.8 to 63.7) |
| `TF_HY4_ENGRAM=gpu` | `f9151885e458` | 49.5 (43.1 to 54.9) | 61.7 (58.0 to 70.4) | 58.0 (53.7 to 64.5) | 66.7 (57.7 to 93.7) | 65.4 (58.5 to 70.6) |
| `TF_HY4_DRAFT_BITS=8` | `ff37e56bb47f` | 52.8 (49.9 to 72.1) | 73.6 (67.3 to 92.4) | 71.2 (62.1 to 76.9) | 79.5 (69.0 to 107.5) | 71.3 (66.2 to 74.3) |

Hy4-flash 8-bit.

| Setting | Run | Own sampler, 4K | Code, 512, 1K | Code, 512, 4K | Code, up to 2,048, 1K | Code, up to 2,048, 4K |
|---|---|---|---|---|---|---|
| Defaults, the start above | `bdcd2d9ede41` | 36.8 (35.7 to 47.5) | 50.8 (46.5 to 52.1) | 46.5 (43.7 to 48.1) | 50.8 (46.4 to 55.0) | 50.4 (43.5 to 51.3) |
| `TF_HY4_ENGRAM=ram` | `6a939a1d10f5` | 41.5 (35.8 to 61.3) | 48.9 (45.8 to 50.8) | 47.9 (46.2 to 49.7) | 51.9 (46.6 to 52.9) | 46.4 (45.2 to 52.6) |
| `TF_HY4_ENGRAM=gpu` | `6a3036688221` | 42.2 (38.3 to 72.6) | 50.2 (48.1 to 51.3) | 48.2 (44.0 to 50.1) | 49.3 (48.1 to 50.3) | 49.8 (44.8 to 53.2) |
| `TF_HY4_DRAFT_BITS=8` | `2e6a99ccd0ea` | 45.7 (44.0 to 54.7) | 54.7 (53.7 to 62.1) | 52.0 (51.1 to 55.3) | 56.3 (52.5 to 59.9) | 54.8 (51.3 to 60.0) |

- **`TF_HY4_DRAFT_BITS=8` was faster on every code text, on both builds.** On the 4-bit build against the default start of the same morning, it was faster on 10 of 10 long replies with a middle ratio of 1.21, and on 10 of 10 short replies with 1.22. Against the first default start the middle ratios are 1.13 and 1.19, again 10 of 10. On the 8-bit build against its one default start they are 1.12 and 1.15, 10 of 10 each.
- **The 79.5 has a wide range.** Its five runs go from 69.0 to 107.5, and one of the five replies closed its thinking at 235 tokens and wrote 1,813 answer tokens. The steadier cell is the 4K one, 71.3 (66.2 to 74.3), all reasoning text. That is 71.3 / 62.4 = 1.14 times the default start of the same morning and 71.3 / 65.3 = 1.09 times the first.
- **One start, and no answer check, at the time of this screen.** The second starts and the check are in the next section.
- **What the switch is.** TensorFold's list of variables in `zig/src/platform/environment.zig` at v1.3.2 reads "4, 8 or 16 (Hy4-flash's DFly2 linears quantized at load; default 16, BF16)". It is not in the project's docs or changelog. The variable was in the server's process environment, checked with `ps`. Server memory after load was 168.0 GiB against 168.7 on the 4-bit build, and 312.6 against 313.3 on the 8-bit build.
- **`TF_HY4_ENGRAM` was level on code.** The list reads "nvme, ram or gpu (where Hy4-flash's Engram tables live; default nvme)". Text by text against a default start, the middle ratios on code are between 0.99 and 1.05 over the three starts. It cost memory. The 8-bit server held 444.6 GiB after load against 313.3, and the 4-bit server 241.0 against 168.7.
- **I make no claim on the sampler column.** The two 4-bit default starts wrote 50.0 and 45.1, and the second was slower on 5 of 5 texts. Differences of that size between rows are start to start spread.
- **A second 8-bit default start did not come up that morning.** My harness checks the listening ports before each start, and that check timed out after 5 seconds. That is my tool and says nothing about TensorFold. The evening job has that start.
- **What the replies were.** 145 of the 150 timed replies of these six starts were reasoning text from start to finish. The other 5 were on the 4-bit build at the 1K prompt.

## Draft switches, the second starts

ELI5: One start can't tell a switch from a lucky start. So I started each setting again that evening, in another order, with the defaults started after the switch. I also ran a check that compares the thinking text, since these replies are nearly all thinking.

Thinking on, drafts on, TensorFold 1.3.2, one start per row, tok/s, 21 Nov 2026 from 18:49 to 20:12 SGT.

Hy4-flash 4-bit.

| Setting | Run | Own sampler, 4K | Code, 512, 1K | Code, 512, 4K | Code, up to 2,048, 1K | Code, up to 2,048, 4K |
|---|---|---|---|---|---|---|
| Defaults, third start | `5498d94e70db` | 51.3 (44.0 to 70.4) | 55.2 (52.5 to 79.4) | 55.4 (53.5 to 59.8) | 64.6 (56.4 to 78.8) | 60.4 (56.9 to 65.9) |
| `TF_HY4_DRAFT_BITS=8`, second start | `b09695c3eab1` | 51.0 (49.4 to 59.1) | 67.5 (63.3 to 88.1) | 64.4 (63.5 to 69.9) | 71.5 (67.4 to 85.9) | 70.7 (61.1 to 77.4) |
| `TF_HY4_DRAFT_BITS=4` | `0f35e5ffa3e6` | 52.6 (51.9 to 88.5) | 67.5 (63.4 to 88.6) | 61.0 (60.8 to 72.3) | 72.7 (69.4 to 106.6) | 68.6 (64.4 to 84.0) |
| `TF_HY4_DRAFT_BITS=8` and `TF_HY4_ENGRAM=gpu` | `a9c0686461ad` | not run | 73.1 (68.7 to 76.6) | 67.1 (64.1 to 72.8) | 79.4 (66.1 to 100.2) | 76.4 (65.0 to 79.1) |

Hy4-flash 8-bit.

| Setting | Run | Own sampler, 4K | Code, 512, 1K | Code, 512, 4K | Code, up to 2,048, 1K | Code, up to 2,048, 4K |
|---|---|---|---|---|---|---|
| Defaults, second start | `a9fe24e89f10` | 37.1 (36.2 to 38.1) | 45.5 (43.2 to 50.4) | 44.6 (42.0 to 46.1) | 47.6 (44.1 to 50.5) | 46.8 (41.8 to 51.3) |
| `TF_HY4_DRAFT_BITS=8`, second start | `f3e0bbdd9f33` | 40.9 (40.7 to 44.1) | 53.2 (52.3 to 55.5) | 52.5 (47.7 to 61.2) | 53.4 (51.7 to 57.7) | 52.0 (48.1 to 55.3) |
| `TF_HY4_DRAFT_BITS=4` | `fb656f1743e9` | 41.8 (40.1 to 60.3) | 53.7 (52.8 to 57.9) | 53.6 (48.2 to 54.5) | 52.9 (50.0 to 56.5) | 53.0 (49.3 to 54.2) |

- **`TF_HY4_DRAFT_BITS=8` was faster on every code text again.** Against the default start of the same evening, on the same texts, it was faster on 10 of 10 long replies with a middle ratio of 1.13 on the 4-bit build, and on 10 of 10 short replies with 1.18. On the 8-bit build it was 10 of 10 with 1.12, and 10 of 10 with 1.20.
- **That is two starts a build, in two orders.** In the morning the switch ran after the defaults. In the evening the defaults ran after the switch. The switch was ahead on 10 of 10 code pairs both times.
- **The server's own banner shows why.** It prints the draft time at start. At defaults it read 3.12 ms a token on the 4-bit build and 3.38 on the 8-bit build. With the switch it read 1.30 and 1.49.
- **The text did not change.** 50 short greedy questions asked twice, with thinking and answer text hashed together. The switch start gave the default start's text on 100 of 100 replies, on each build. Inside each start the second pass gave the first pass's text on 50 of 50.
- **What that check covers.** Replies of 64 tokens at most, on prompts of about 256 tokens, all of them thinking text. All of these starts had drafts on. I did not compare them with a drafts-off start. The check files are not in `rows.csv`.
- **With the sampler the gain is smaller and less even.** Faster on 3 of 5 sampled texts with a middle ratio of 1.14 on the 4-bit build, where the two middles are 51.0 and 51.3. On the 8-bit build it was 5 of 5 with 1.12, at 40.9 against 37.1.
- **`TF_HY4_DRAFT_BITS=4` did the same as 8.** Against the default start it was faster on 10 of 10 long and 10 of 10 short code replies on both builds, with middle ratios of 1.13 to 1.19. Against `TF_HY4_DRAFT_BITS=8` it was level, with middle ratios of 0.98 to 1.02 on code. Its text matched the default start's on 100 of 100 too. One start a build.
- **Adding `TF_HY4_ENGRAM=gpu` wrote the highest figures here, on one start.** 79.4 and 76.4 on long code replies on the 4-bit build. Against the switch alone it was faster on 9 of 10 long replies with a middle ratio of 1.07, and on 8 of 10 short ones with 1.03. The server held 240.3 GiB after load against 168.0. It had no answer check and no sampled test, and the morning screen found Engram alone level. So it is not on the summary page.
- **The evening starts were mostly a little lower than the morning ones.** Same setting and same texts, evening over morning, the middle ratios on code run from 0.93 to 1.00. The defaults and the switch both moved. I did not find the cause. So compare a row with the rows of its own table and not across the two tables.
- **Memory.** After load the 4-bit server held 168.7 GiB at defaults, 168.0 with 8 bits and 167.6 with 4. The 8-bit server held 313.3, 312.6 and 312.2.
- **What the replies were.** 162 of the 170 timed replies of these seven starts were reasoning text from start to finish. The other 8 were on the 4-bit build, 7 at the 1K prompt and 1 at 4K.
- **On the summary page.** The default lines are now the evening starts, the latest at defaults. `TF_HY4_DRAFT_BITS=8` is its own line from its second start, labelled as a switch from the source.

## Thinking off did not give clean answers

ELI5: I first ran everything with thinking switched off, as I do for most models. The replies planned out loud and lost the thread, on both builds. I then looked at the prompt the server built. It is not the prompt the model's own template builds for "no thinking".

### What the server did with each switch

One short prompt, greedy, 200 tokens, on both builds on 1.3.2.

| Request field | HTTP | Prompt tokens | Server log | Where the text landed |
|---|---|---|---|---|
| none | 200 | 43 | `thinking=True effort=none` | 200 reasoning tokens |
| `chat_template_kwargs: {"enable_thinking": true}` | 200 | 43 | `thinking=True effort=none` | 200 reasoning tokens |
| `chat_template_kwargs: {"enable_thinking": false}` | 200 | 44 | `thinking=False effort=none` | 200 answer tokens |
| `reasoning_effort: "none"`, top level | 200 | 44 | `thinking=False effort=none` | 200 answer tokens, the same reply |
| `chat_template_kwargs: {"reasoning_effort": "no_think"}` | 400 | | | refused, 4-bit build only |

- **The build's own chat template renders "no thinking" as 46 tokens.** I rendered `chat_template.jinja` offline with the build's tokenizer. The default is 43 tokens and ends with an open think tag. With `reasoning_effort` set to `no_think` it is 46 tokens. The system line then says `reasoning_effort:no_think`, and the prompt ends with an open and a closed think tag.
- **The server's thinking-off prompt is 44 tokens.** I can't see which text it built. More than one rendering comes to 44.
- **The template's own value was refused.** The server answered "reasoning_effort must be none, minimal, low, medium, high, xhigh or max". The template itself accepts `no_think`, `high` and `max`, and never reads `enable_thinking`.
- **So I found no request that gives the template's 46-token form** on 1.3.2. If there is one, I will rerun with it.
- **The `--no-thinking` start flag gave the same prompt.** On a 4-bit start with that flag, a request with no thinking field came to 44 prompt tokens and 0 reasoning tokens, as with the request switch, and returned the same reply as `enable_thinking: false` did on that start. Tried on 21 Nov 2026 at 09:28 SGT, on the 4-bit build only, with nothing timed.

### What the replies looked like

Greedy, thinking off by `enable_thinking: false`, one extra request each, not in `rows.csv`.

| Question | 8-bit | 4-bit |
|---|---|---|
| Short Fibonacci function | A code block with `a, b = 0, "1"` and an unfinished list, then "The previous response was malformed." | A code block whose docstring says "F(0)=0, F(0)=1", then a line that adds a string to `n`. |
| New code, 4K prompt, 512 tokens | Opened with a plan and a code block. Its last 300 characters were planning notes. | Opened "We need answer the user's request". Its last 300 characters were planning notes. |
| Copy the prompt, 4K, 2,048 tokens | 167 of 180 lines are in the prompt word for word, after 4 lines of planning. | 192 of 201 lines, after 2 lines of planning. |
| Count from 1 to 400, 1K prompt, 512 tokens | 4 of 169, 3 of 192 and 5 of 207 lines were the next number. Each reply wrote a few numbers, a literal `<think>` tag and planning notes, then counted. | 3 of 50 and 5 of 52. One reply wrote five numbers, planning notes, a literal `</think>` tag, then counted from 1. |

- **Both builds did it.** So I do not put it down to 4-bit weights.
- **With thinking on, the short prompt's reasoning read as normal planning** on both builds. I read back no timed thinking-on reply.

### The speeds with that switch

ELI5: These rows are real tokens per second, but of a model that was prompted in a way its template does not use. I keep them out of the summary page.

Tok/s, TensorFold 1.3.2, thinking off by `enable_thinking: false`.

| Test | Prompt | 8-bit, drafts on `8ff5ac9baafa` | 8-bit, drafts off `1d123ec673b6` | 4-bit, drafts on `cf930777f656` | 4-bit, drafts off `fff18d644690` |
|---|---|---|---|---|---|
| Greedy, new code, up to 2,048 tokens | 1K | 51.3 (47.9 to 72.4) | 34.1 (34.1 to 35.7) | 67.4 (59.1 to 96.2) | 42.2 (42.0 to 42.6) |
| Greedy, new code, up to 2,048 tokens | 4K | 49.8 (46.0 to 57.8) | 34.3 (34.3 to 34.5) | 63.1 (55.2 to 82.0) | 42.3 (42.3 to 42.4) |
| Greedy, new code, 512 tokens | 1K | 50.7 (47.9 to 65.3) | 34.7 (33.5 to 34.8) | 62.3 (51.4 to 68.4) | 43.1 (41.3 to 44.6) |
| Greedy, new code, 512 tokens | 4K | 56.3 (51.7 to 57.9) | 34.3 (34.3 to 34.3) | 57.4 (54.3 to 68.6) | 42.5 (42.3 to 42.6) |
| Own sampler, mixed text, 512 tokens | 4K | 38.0 (38.0 to 39.1) | 33.7 (33.6 to 33.7) | 44.8 (41.9 to 56.5) | 41.4 (41.3 to 41.8) |
| Asked to copy the prompt, 512 tokens | 1K | 56.4 (52.5 to 84.0) | not run | 73.7 (60.0 to 104.1) | not run |
| Asked to copy the prompt, 512 tokens | 4K | 60.9 (50.1 to 94.5) | not run | 74.2 (54.5 to 122.7) | not run |
| Asked to copy the prompt, 2,048 tokens | 4K | 90.1 (59.7 to 97.0) | not run | 90.1 (81.0 to 130.9) | not run |
| Asked to count from 1, 512 tokens | 1K | 57.0 (56.6 to 84.8) | not run | 64.3 (54.4 to 111.8) | not run |
| Asked to count from 1, 512 tokens | 4K | 68.9 (51.1 to 71.4) | not run | 60.3 (55.2 to 101.3) | not run |

- **Drafts on and off gave the same short answers.** On 250 short greedy questions, 250 of 250 answers match between the drafts-on and drafts-off starts, on each build.
- **The drafts-off speed is the same in both modes.** 34.3 against 34.0 on the 8-bit build and 42.5 against 42.2 on the 4-bit build, on code with 512-token replies at 4K.
- **The copy and counting rows are not copy and counting speeds.** The replies were part planning notes, as the table above shows. I enter no copy or count line on the summary page.

## TensorFold 1.3.1 against 1.3.2, 4-bit build

ELI5: 1.3.1 was the first release to serve this model. 1.3.2 came out under six hours later. I had already run the 4-bit build on 1.3.1, so here are both. Thinking off by the old switch, one start each.

| Test | Prompt | 1.3.1, drafts on `dfe2fad2ff2c` | 1.3.2, drafts on `cf930777f656` | 1.3.1, drafts off `84354146db7d` | 1.3.2, drafts off `fff18d644690` |
|---|---|---|---|---|---|
| Greedy, new code, up to 2,048 tokens | 1K | 61.8 (59.2 to 102.2) | 67.4 (59.1 to 96.2) | 42.7 (42.7 to 42.8) | 42.2 (42.0 to 42.6) |
| Greedy, new code, up to 2,048 tokens | 4K | 61.8 (59.6 to 111.6) | 63.1 (55.2 to 82.0) | 43.1 (43.0 to 43.1) | 42.3 (42.3 to 42.4) |
| Greedy, new code, 512 tokens | 1K | 60.2 (58.8 to 63.6) | 62.3 (51.4 to 68.4) | 43.7 (41.8 to 43.9) | 43.1 (41.3 to 44.6) |
| Greedy, new code, 512 tokens | 4K | 57.3 (51.4 to 59.4) | 57.4 (54.3 to 68.6) | 43.0 (43.0 to 43.0) | 42.5 (42.3 to 42.6) |
| Own sampler, mixed text, 512 tokens | 4K | 43.9 (43.5 to 44.9) | 44.8 (41.9 to 56.5) | 42.1 (42.0 to 42.1) | 41.4 (41.3 to 41.8) |

- **Drafts on, the ranges overlap in every cell.** I see no change.
- **Drafts off, 1.3.2 was 1% to 2% lower in all five cells.** 42.3 / 43.1 = 0.98 at the widest. One start each, so I do not call it a version change.
- **Same answers.** 250 of 250 short greedy answers match between the two releases with drafts on.
- **The 1.3.2 notes list no speed change for Hy4-flash on Macs.**

## The setup

ELI5: One engine at its newest release. The headline starts are at its defaults, and the switch starts name the one variable they set. A fresh server start for every setting.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.2, published 21 Nov 2026 03:27 SGT, from the author's Homebrew tap. The download's SHA-256 equals the digest GitHub lists for the release file.
- **Serve command.** `--no-drafts` is added for the drafts-off starts. Nothing else is set. No `TF_` variable is set except on the starts that name one.

```bash
tensorfold serve <build folder> --name <name> --host 127.0.0.1 --port 8188 --context 131072 --parallel 1 --no-update-check
```

- **Weights.** TensorFold's own MLX conversions of [tencent/Hy4-flash](https://huggingface.co/tencent/Hy4-flash), with the DFly2 drafter in the build.
  - [TensorFold/Hy4-flash-MLX-4bit-MTP](https://huggingface.co/TensorFold/Hy4-flash-MLX-4bit-MTP) @ dd375b3d, 121.0 GiB.
  - [TensorFold/Hy4-flash-MLX-8bit-MTP](https://huggingface.co/TensorFold/Hy4-flash-MLX-8bit-MTP) @ 0a4fe3df, 222.9 GiB.
- **Drafts.** The server's banner says "drafts: MTP + copies" at defaults and "drafts: off" with `--no-drafts`.
- **Sampler.** Temperature 0.9 and top-p 1.0, from the model's `generation_config.json`.
- **Thinking on** is `chat_template_kwargs: {"enable_thinking": true}`, which gave the same 43-token prompt as sending no field.
- **Licence.** The Tencent Hy License. Read it before you ship anything on this model.

| Run id | Build | Release | Drafts | Thinking | Started, SGT |
|---|---|---|---|---|---|
| `bdcd2d9ede41` | 8-bit | 1.3.2 | on | on | 21 Nov, 07:28 |
| `b8e543b952e1` | 8-bit | 1.3.2 | off | on | 21 Nov, 07:40 |
| `b1f754c43ae4` | 4-bit | 1.3.2 | on | on | 21 Nov, 07:45 |
| `df5b641735e6` | 4-bit | 1.3.2 | off | on | 21 Nov, 07:54 |
| `10884ddb9c17` | 8-bit | 1.3.2 | on | on, 5 rows inside the start of `8ff5ac9baafa` | 21 Nov, 05:54 |
| `cad62d9be2d7` | 4-bit | 1.3.2 | on | on, 5 rows inside the start of `cf930777f656` | 21 Nov, 06:44 |
| `8ff5ac9baafa` | 8-bit | 1.3.2 | on | off, old switch | 21 Nov, 05:54 |
| `1d123ec673b6` | 8-bit | 1.3.2 | off | off, old switch | 21 Nov, 06:22 |
| `cf930777f656` | 4-bit | 1.3.2 | on | off, old switch | 21 Nov, 06:44 |
| `fff18d644690` | 4-bit | 1.3.2 | off | off, old switch | 21 Nov, 07:06 |
| `dfe2fad2ff2c` | 4-bit | 1.3.1 | on | off, old switch | 21 Nov, 04:20 |
| `84354146db7d` | 4-bit | 1.3.1 | off | off, old switch | 21 Nov, 04:39 |
| `6a939a1d10f5` | 8-bit | 1.3.2 | on, `TF_HY4_ENGRAM=ram` | on | 21 Nov, 09:36 |
| `6a3036688221` | 8-bit | 1.3.2 | on, `TF_HY4_ENGRAM=gpu` | on | 21 Nov, 09:47 |
| `2e6a99ccd0ea` | 8-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=8` | on | 21 Nov, 09:59 |
| `d341be8cafd5` | 4-bit | 1.3.2 | on, defaults, another start | on | 21 Nov, 10:10 |
| `f9151885e458` | 4-bit | 1.3.2 | on, `TF_HY4_ENGRAM=gpu` | on | 21 Nov, 10:20 |
| `ff37e56bb47f` | 4-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=8` | on | 21 Nov, 10:29 |
| `b09695c3eab1` | 4-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=8`, second start | on | 21 Nov, 18:49 |
| `0f35e5ffa3e6` | 4-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=4` | on | 21 Nov, 18:59 |
| `5498d94e70db` | 4-bit | 1.3.2 | on, defaults, third start | on | 21 Nov, 19:09 |
| `a9c0686461ad` | 4-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=8` and `TF_HY4_ENGRAM=gpu` | on | 21 Nov, 19:21 |
| `f3e0bbdd9f33` | 8-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=8`, second start | on | 21 Nov, 19:31 |
| `fb656f1743e9` | 8-bit | 1.3.2 | on, `TF_HY4_DRAFT_BITS=4` | on | 21 Nov, 19:44 |
| `a9fe24e89f10` | 8-bit | 1.3.2 | on, defaults, second start | on | 21 Nov, 19:58 |

- **Two run ids were made after the fact.** Runs `10884ddb9c17` and `cad62d9be2d7` hold five thinking-on rows each that I sent inside a start recorded as thinking off. I moved them to their own run ids so each run has one thinking setting. No measured value changed.

## How I measured

ELI5: Same Mac, same harness and same text rules as findings 3 to 9.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test, as in finding 2. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes** are targets at 3.5 characters per token. A "1K" code prompt came to about 870 tokens on this model and a "4K" one to about 4,120.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first reply token to the last, reasoning tokens included.
- **The questions** are the three of [finding 5](../05_dsv41_omlx_080_max_push), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **These are reasoning tokens.** With thinking on, this model spent 512 and 2,048-token budgets thinking.
- **Starts differ.** The 4-bit build has three default starts. With the sampler they wrote 50.0, 45.1 and 51.3. On long code replies at 1K they wrote 63.2, 65.0 and 64.6. The 8-bit build's two default starts wrote 50.8 and 47.6 there.
- **The switch is not in the engine's docs.** I found it in the source's list of environment variables. Its name and its effect may change.
- **The author's own M5 Ultra figures** are in [TensorFold pull request 3941](https://github.com/ashhart/TensorFold/pull/3941). They use other prompts, so read them there and not against this table.
- **Max is not what a chat feels like.** The median column is the everyday figure.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 712 raw rows from the bench database. 635 timed requests and 77 warm-ups.
- **`runs.csv`.** The 25 runs behind them, with engine, version, start time, settings and sampling.
- **`render_template_tokens.py`.** Renders the build's chat template for each thinking setting and counts the tokens. It needs the `tokenizers` and `jinja2` packages.

From the top of this repository.

```bash
python3 tools/summarize.py findings/10_hy4_flash_tensorfold_132
```

## What I did not verify

- **What the timed thinking-on replies say.** I read back one short thinking-on reply per build and no timed one.
- **Which 44-token prompt the server built** for thinking off.
- **A thinking-off run in the template's own 46-token form.** I found no request that produces it.
- **The server's `--reasoning-effort` start flag.** Not tried.
- **Longer replies with drafts off and thinking on.**
- **That `TF_HY4_DRAFT_BITS=8` writes the same text as the default on long replies, or as a drafts-off start.** The check covers 64-token replies between starts with drafts on.
- **What the switch costs in draft quality.** The draft is stored at fewer bits. I measured speed and the final text, not how many drafted tokens were kept.
- **A second start** of `TF_HY4_DRAFT_BITS=4`, or of the switch with `TF_HY4_ENGRAM=gpu`.
- **Why the evening starts ran a little lower.**
- **Long prompts, and two users at once.**
- **Answer quality** of either build.
- **Peak memory.** The figures above are the process size by `ps` at two moments.
- **Any other engine on this model.** `mlx-lm` 0.32.2 and oMLX 0.8.0 have no model file for it. oMLX 0.8.1, released on 21 Nov 2026 at 09:17 SGT, loads it, and [finding 12](../12_hy4_flash_omlx_081) has that run on another build. The rest were not tried.

## Credit

- **Engine and MLX builds.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Model and DFly2 drafter.** Hy4-flash by Tencent.

If a setting here is wrong, open an issue and I will rerun it. That goes double for the thinking switch.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
