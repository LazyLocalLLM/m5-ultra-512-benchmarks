# Finding 15. GLM-5.3 Flash, an all-4-bit build against a mixed 4-bit and 8-bit build

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: A model can be stored at 4 bits a weight everywhere, or with some parts kept at 8 bits. People ask whether the 8-bit parts buy quality, and whether they cost speed. Two public builds of GLM-5.3 Flash differ in just that way. I ran both on the same two engines, with the engines' drafts on and off, and I scored how well each build predicts the same fixed text.

**On TensorFold 1.3.2 with no drafts, TensorFold's all-4-bit build wrote 73.4 tok/s and the oQ4e build wrote 50.9, which is 0.69 times. oQ4e keeps 290 of its 419 tensors at 8 bits, by TensorFold's loader. oMLX 0.8.1 gave 72.5 and 51.7 for the same pair. With MTP drafts the all-4-bit build reached 102.0 tok/s at its max on TensorFold and oQ4e reached 82.9. The oQ4e build predicted fixed text slightly better, 0.4849 against 0.5079 nats a token over 31,056 tokens, and it was the lower one on 21 of 24 texts. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, one server start per setting, 21 Nov 2026 SGT.**

| Build | Engine | Max, tok/s | Median, tok/s | No drafts, tok/s | Reply text |
|---|---|---|---|---|---|
| TensorFold 4-bit, 169.3 GiB | TensorFold 1.3.2 | 102.0 | 80.9 | 73.4 | Answer |
| oQ4e, 173.6 GiB | TensorFold 1.3.2 | 82.9 | 67.5 | 50.9 | Answer |
| TensorFold 4-bit, 169.3 GiB | oMLX 0.8.1 | 85.1 | 76.8 | 72.5 | Reasoning |
| oQ4e, 173.6 GiB | oMLX 0.8.1 | 78.7 | 69.7 | 51.7 | Reasoning |

- **Max** is the middle of 5 greedy runs on new code with MTP drafts and replies of up to 2,048 tokens, at the better of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler and MTP drafts, mixed text, 512-token replies, 4K prompt.
- **No drafts** is the middle of 5 greedy runs on new code with drafts off, 512-token replies, 1K prompt.
- **Compare builds inside one engine.** TensorFold's replies were answer text and oMLX's were reasoning text, so a row of one engine is not a like for like with a row of the other.

## Chart

ELI5: The same question on four setups. Grey is the all-4-bit build and blue is the mixed build.

![Bars of writing speed in tokens per second for two builds of GLM-5.3 Flash, greedy at temperature 0, new code, 512-token replies, 1K prompt. TensorFold with no drafts, 73.4 for the all-4-bit build and 50.9 for oQ4e. TensorFold with MTP drafts, 101.5 and 74.6. oMLX with no drafts, 72.5 and 51.7. oMLX with MTP drafts, 88.9 and 80.7.](chart_builds.png)

## The two builds

ELI5: Both are GLM-5.3 Flash for a Mac. They differ in how many bits each part of the model gets, and in how they were made.

| | TensorFold 4-bit | oQ4e |
|---|---|---|
| Repository | [TensorFold/GLM-5.3-Flash-MLX-4bit-MTP](https://huggingface.co/TensorFold/GLM-5.3-Flash-MLX-4bit-MTP) @ d2b17f52 | [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp) @ 9e5c75a9 |
| Size on the Hub | 169.3 GiB | 173.6 GiB |
| Bits, by TensorFold's loader | 4-bit on 408 tensors | 4-bit on 129 tensors, 8-bit on 290 |
| Weights in buffers, by TensorFold's loader | 180.58 GB | 185.11 GB |
| Server memory on TensorFold, by `ps` | 174.0 GiB | 178.2 GiB |

- **What oQ4e keeps at 8 bits**, by its `config.json`. The attention projections, the shared experts, the dense MLP of 3 layers, the token embedding and the output head. Every tensor the config does not name is at the default, 4 bits.
- **Two counts of the same thing.** The config names 554 tensors at 8 bits. TensorFold's loader reports 290 at 8 bits and 129 at 4. I did not work out how the loader groups them. The chart and the headline use the loader's count.
- **Earlier pages call oQ4e "GLM-5.3 Flash 4-bit".** Findings 2 and 9 ran oQ4e only. On this page and in the summary from today, "4-bit" is TensorFold's build and "oQ4e" is the mixed one.
- **oQ4e was also made with a calibration pass.** Its `oq_imatrix_report.json` says so. So the two builds differ in more than the 8-bit parts, and nothing here says which difference does what.
- **The chat templates differ, and a plain request renders the same.** The two `chat_template.jinja` files are not the same file, and the lines that differ are in their tool-call parts. I rendered one plain chat request through both offline and got the same text, 20 tokens. The tokenizer files are the same.
- **Both builds carry the model's MTP head**, the small part that drafts tokens ahead.

## Speed with no drafts

ELI5: With drafts off the model writes one token a step. This is the cleanest view of what the weights cost, because no draft model's luck is in it.

Decode tok/s, greedy, new code, 512-token replies. The slowest and fastest of the 5 runs are in brackets.

| Engine | Prompt | TensorFold 4-bit | oQ4e | oQ4e as a share |
|---|---|---|---|---|
| TensorFold 1.3.2 | 1K | 73.4 (72.4 to 73.6) | 50.9 (50.5 to 51.0) | 50.9 / 73.4 = 0.69 |
| TensorFold 1.3.2 | 4K | 73.1 (73.0 to 73.2) | 50.9 (50.9 to 50.9) | 50.9 / 73.1 = 0.70 |
| oMLX 0.8.1 | 1K | 72.5 (71.3 to 72.7) | 51.7 (51.0 to 51.8) | 51.7 / 72.5 = 0.71 |
| oMLX 0.8.1 | 4K | 68.9 (68.8 to 69.0) | 49.3 (49.3 to 49.4) | 49.3 / 68.9 = 0.72 |

- **The mixed build was slower on both engines**, by 28% to 31%.
- **Text by text it was slower on 20 of 20 pairs.**
- **The two engines agree within 2 tok/s at 1K** on each build.
- **Runs barely spread.** No cell's 5 runs are more than 1.4 tok/s apart.

## Speed with MTP drafts

ELI5: With drafts on, the model's own small head guesses tokens ahead and the big model checks them. Speed then depends on how often the guesses are kept.

### TensorFold 1.3.2

Decode tok/s. The 4-bit build is run `33ba6147e087`. oQ4e is run `787aea383796`.

| Test | Prompt | TensorFold 4-bit | oQ4e | oQ4e as a share |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 101.4 (99.6 to 104.4) | 80.7 (74.5 to 84.5) | 0.80 |
| Greedy, new code, replies up to 2,048 tokens | 4K | 102.0 (95.2 to 108.5) | 82.9 (77.1 to 89.2) | 0.81 |
| Greedy, new code, 512-token replies | 1K | 101.5 (91.2 to 107.0) | 74.6 (71.9 to 79.1) | 0.74 |
| Greedy, new code, 512-token replies | 4K | 98.6 (93.8 to 101.8) | 74.2 (71.4 to 83.7) | 0.75 |
| Own sampler, mixed text, 512-token replies | 4K | 80.9 (79.2 to 85.4) | 67.5 (64.3 to 70.0) | 0.83 |
| Greedy, asked to copy the prompt | 1K | 175.0 (118.0 to 183.3) | 156.8 (94.3 to 160.8) | 0.90 |
| Greedy, asked to copy the prompt | 4K | 174.5 (107.2 to 177.2) | 146.5 (105.9 to 157.6) | 0.84 |
| Greedy, asked to count | 1K | 105.6 (98.0 to 107.6) | 95.2 (83.1 to 96.5) | 0.90 |
| Greedy, asked to count | 4K | 111.1 (105.5 to 116.1) | 96.3 (86.7 to 99.5) | 0.87 |

- **Max.** 102.0 tok/s for the 4-bit build and 82.9 for oQ4e. 82.9 / 102.0 = 0.81.
- **Median.** 80.9 and 67.5. 67.5 / 80.9 = 0.83.
- **Text by text oQ4e was slower on 45 of 45 pairs.**
- **Drafts gave the 4-bit build 101.5 / 73.4 = 1.38 times** on short code replies at 1K, and oQ4e 74.6 / 50.9 = 1.47 times.
- **Every timed reply was answer text**, with 0 reasoning tokens.
- **The copy and counting lines are easy text.** I read one reply of each back on both builds. The copy replies repeated the prompt's lines and the counting replies were the next number on 245 of 245 lines.

### oMLX 0.8.1

Decode tok/s at the default draft depth. The 4-bit build is run `4f9da10c3691`. oQ4e is run `421e19a82f36`.

| Test | Prompt | TensorFold 4-bit | oQ4e | oQ4e as a share |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 82.3 (79.4 to 99.7) | 78.7 (73.7 to 86.2) | 0.96 |
| Greedy, new code, replies up to 2,048 tokens | 4K | 85.1 (79.6 to 87.0) | 73.4 (66.6 to 77.3) | 0.86 |
| Greedy, new code, 512-token replies | 1K | 88.9 (78.5 to 97.6) | 80.7 (73.4 to 82.3) | 0.91 |
| Greedy, new code, 512-token replies | 4K | 83.5 (80.8 to 89.5) | 73.2 (67.7 to 76.6) | 0.88 |
| Own sampler, mixed text, 512-token replies | 4K | 76.8 (68.9 to 78.3) | 69.7 (66.9 to 73.3) | 0.91 |

- **Max.** 85.1 tok/s for the 4-bit build and 78.7 for oQ4e. 78.7 / 85.1 = 0.92.
- **Median.** 76.8 and 69.7. 69.7 / 76.8 = 0.91.
- **The gap is smaller with drafts on than off on this engine.** Text by text oQ4e was slower on 23 of 25 pairs. The ranges of several cells overlap.
- **These are reasoning speeds.** The request switched thinking off, and every one of these timed replies was reasoning text all the same, as in [finding 9](../09_omlx_080_four_models).
- **The model's template has no thinking-off setting.** It reads a reasoning effort of low, high or max, and it always opens a think block. I rendered both builds' templates offline with and without `enable_thinking` and got the same prompt each time, with the effort at Max. TensorFold's recipe says its server closes that open think block when thinking is off, which is how its replies came out as answer text. I did not try a lower effort on oMLX.
- **No copy or counting line for oMLX.** Those replies mixed reasoning and answer text. The rows are in `rows.csv` under the contents `code_echo` and `code_count`.
- **TensorFold's build is documented for oMLX.** Its card lists oMLX 0.6.3rc3 as validated for baseline generation. The card also says to keep MTP off on that older build. On 0.8.1 here MTP on was faster than off, 88.9 against 72.5 tok/s on short code replies at 1K.

## How well each build predicts text

ELI5: Give a model a real piece of text and ask, at every token, how much chance it gave to the token that really came next. A better copy of the model gives the real token more chance. The score is in nats a token and lower is better. It is a common way to compare two builds of one model.

Mean negative log-likelihood per token. 24 fixed texts of about 5,250 characters each, 12 of code and 12 of mixed prose and code, raw text with no chat template.

| Texts | Scored tokens | TensorFold 4-bit | oQ4e | oQ4e minus 4-bit | oQ4e lower on |
|---|---|---|---|---|---|
| Code | 15,655 | 0.4695 | 0.4454 | -0.0241 | 11 of 12 texts |
| Mixed | 15,401 | 0.5470 | 0.5250 | -0.0220 | 10 of 12 texts |
| All | 31,056 | 0.5079 | 0.4849 | -0.0230 | 21 of 24 texts |

- **oQ4e predicted the text better.** 0.5079 - 0.4849 = 0.0230 nats a token. 0.0230 / 0.5079 = 4.5% lower.
- **Text by text.** The 24 differences have a mean of -0.0244 and a spread of 0.0354 (sample standard deviation). They run from -0.1669 to +0.0132.
- **One text carries a lot of it.** Without the text of the largest gap the mean of the other 23 is -0.0182, and oQ4e is lower on 20 of them.
- **Top guess right.** The real next token was the build's first choice on 27,414 of 31,056 tokens for the 4-bit build, 88.3%, and on 27,595 for oQ4e, 88.9%.
- **The score repeats.** Each build scored the first text twice and the largest gap at any token was 0.000000 nats.
- **Both builds saw the same tokens.** The token ids match on 24 of 24 texts.
- **This is text prediction, not task quality.** A 4.5% lower score does not say how much better an answer reads, and I ran no graded task.
- **It is oMLX 0.8.1's model code, not TensorFold's runtime.** I asked TensorFold 1.3.2 for the same score first, with the `prompt_logprobs` field of its `/v1/completions`. It answered HTTP 400 on both builds, "prompt_logprobs are not supported by this model or backend". So I loaded the weights with the model code oMLX ships and scored them with no server.
- **There is no full-precision reference here.** I did not score the original weights, so I cannot say how far either build is from them.
- **The texts are close to oQ4e's calibration set.** Its report names the set `oqe_code_multilingual`. My 24 texts are code and prose about code. I scored no text from another field.

## The text with drafts on and off

ELI5: I sent 50 short greedy questions twice to each start and compared the whole reply, thinking text included. Same text means the drafts did not change what the model wrote.

| Compared | Replies with the same text |
|---|---|
| TensorFold, each of 4 starts, second pass against first | 50 of 50 |
| TensorFold, 4-bit build, drafts on against off | 100 of 100 |
| TensorFold, oQ4e, drafts on against off | 100 of 100 |
| TensorFold, 4-bit build against oQ4e, drafts off | 2 of 100 |
| oMLX, drafts off, each build, second pass against first | 50 of 50 |
| oMLX, 4-bit build, drafts on, second pass against first | 47 of 50 |
| oMLX, oQ4e, drafts on, second pass against first | 49 of 50 |
| oMLX, 4-bit build, drafts on against off | 28 of 100 |
| oMLX, oQ4e, drafts on against off | 29 of 100 |

- **On TensorFold the drafts changed no reply**, on either build.
- **On oMLX they changed most replies.** I report the counts and no cause.
- **The two builds write different text**, as two sets of weights and two chat templates would.
- **A reply is 64 tokens.** One early token that differs changes all the text after it.
- **This says nothing about which text is better.** I did not grade the answers.

## What I could not run

ELI5: Two things I meant to test did not run on the public release. I state what the release printed.

- **The DFlash2 draft model on a Mac.** TensorFold 1.3.2 stopped at start with `--drafter` and this model. Its message lists the model classes `--drafter` supports, and GLM-5.3 Flash is not among them. The recipe `docs/recipes/glm-5.3-flash.md` at the 1.3.2 tag says the DFlash2 policies do not apply to the native binary. I misread that file when I planned the run.
- **The text-prediction score through TensorFold**, as above.
- **Other mixed builds.** oQ4e is the one public 4-bit and 8-bit mix of this model I know of. A mix with fewer 8-bit parts may behave differently.

## Reference points

ELI5: My usual baseline is Apple's `mlx-lm` on the same weights. It has no model code for GLM-5.3 Flash, so the baseline here is each engine with its drafts off.

- **`mlx-lm` 0.32.2 has no `glm5_next` model**, so it cannot load either build.
- **oQ4e on oMLX 0.8.0**, in [finding 9](../09_omlx_080_four_models), wrote 80.2 tok/s at its max and 67.8 with its own sampler. On 0.8.1 here it wrote 78.7 and 69.7. One start each. Finding 3 measured 7% between two starts of one setting on this engine.
- **oMLX 0.8.2 came out on 21 Nov 2026 at 12:20 SGT.** Its notes call it a hotfix for click positions on screenshots and say everything else is the same as 0.8.1. I ran 0.8.1. The oQ4e build's drafts-on start was rerun on 0.8.2 that evening, in [finding 16](../16_omlx_082_refresh), and I see no change.

## The setup

ELI5: Two engines, two builds, and a fresh server start for every setting. TensorFold is at its newest release. oMLX is one hotfix behind.

- **Added 22 Nov 2026 08:17 SGT.** Both builds were rerun on TensorFold 1.3.3 with MTP drafts. I see no change. 1.3.3 also starts with a DFlash2 draft model on a Mac, which this page records 1.3.2 refusing. The drafts-off lines stay on 1.3.2. That run is [finding 19](../19_tensorfold_133_refresh), and the summary page now shows its lines.
- **Engine 1.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.2, released 21 Nov 2026 03:27 SGT, installed from the project's Homebrew tap. `tensorfold-native --version` prints 1.3.2.

```bash
tensorfold serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 131072 --parallel 1
```

- **Drafts off on TensorFold** is the same command with `--no-drafts`. The server's start line says "drafts: off". With no flag it says "drafts: MTP + copies".
- **Engine 2.** [oMLX](https://github.com/jundot/omlx) 0.8.1, released 21 Nov 2026 09:17 SGT, installed from the tagged source with its custom kernels built (`OMLX_WITH_CUSTOM_KERNEL=1`).

```bash
omlx serve --model-dir <models> --host 127.0.0.1 --port 8193 --max-concurrent-requests 1 --headless --no-hf-cache --base-path <home>
```

- **Model settings on oMLX**, in its own `model_settings.json`. `mtp_enabled` true, or false for the drafts-off starts. `a8_prefill_enabled` false, `activation_fp16_enabled` false. No fixed depth. `server.burst_decode_mode` at `balanced`, the default. The 4-bit build got the same entry as oQ4e.
- **Weights.** Every file was verified against the pinned commit. Hugging Face's security scan of the TensorFold repository was done with no file flagged when I read it on 21 Nov 2026 at 14:22 SGT. The files I loaded are safetensors, JSON, a chat template and text.
- **The model.** [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash).
- **Sampler.** Temperature 1.0 and top-p 0.95, as for the other GLM-5.3 Flash builds on this bench.
- **Thinking** switched off in every request, with `enable_thinking: false` in `chat_template_kwargs`, and at the top level too on oMLX.

| Run id | Engine | Build | Drafts | Started, SGT, 21 Nov 2026 |
|---|---|---|---|---|
| `33ba6147e087` | TensorFold 1.3.2 | TensorFold 4-bit | MTP | 15:45 |
| `787aea383796` | TensorFold 1.3.2 | oQ4e | MTP | 15:54 |
| `3b571bd4b948` | TensorFold 1.3.2 | TensorFold 4-bit | Off | 16:09 |
| `06d0073eb3e8` | TensorFold 1.3.2 | oQ4e | Off | 16:13 |
| `5727fcf18ffb` | oMLX 0.8.1 | TensorFold 4-bit | Off | 16:22 |
| `9ab8740acc17` | oMLX 0.8.1 | oQ4e | Off | 16:26 |
| `4f9da10c3691` | oMLX 0.8.1 | TensorFold 4-bit | MTP, default depth | 16:32 |
| `421e19a82f36` | oMLX 0.8.1 | oQ4e | MTP, default depth | 16:43 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as findings 5 to 14. The text-prediction score is new on this page.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through each build's own chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent.
- **Text.** Code from open-source projects for the greedy tests, and the harness's mixed text for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Every timed request shows 0 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token. On this model's tokenizer the code prompts came to about 1,000 and 3,900 tokens.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last, reasoning tokens included.
- **The three questions** are those of [finding 5](../05_dsv41_omlx_080_max_push), word for word.
- **The text-prediction score.** The code of `score_text.py` in this folder, run with the Python of the oMLX 0.8.1 install and no network. It loads a build with `omlx.utils.model_loading.load_text_model`, tokenizes each text with the build's tokenizer, runs one forward pass a text and takes the cross-entropy of every token after the first. Nothing was served and nothing was timed.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Two builds are not a law.** This is one all-4-bit build and one mixed build of one model. Another mixed build with fewer 8-bit parts may cost less speed. I did not find one to test.
- **One start per setting.**
- **Reasoning text is not answer text.** Compare the builds inside one engine.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **A lower text-prediction score is not a graded task.**

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 244 raw rows from the bench database. 220 timed requests and 24 warm-ups.
- **`runs.csv`.** The 8 runs behind them, with engine, version, start time, settings and sampling.
- **`scores.csv`.** The 24 texts, each with its SHA-256, its scored tokens and both builds' scores.
- **`score_text.py`.** The scoring code of the script I ran, cut down to the two steps that matter. I did not run this copy's `score` step, only its `compare` step.

From the top of this repository.

```bash
python3 tools/summarize.py findings/15_glm53_flash_two_builds
```

## What I did not verify

- **Any graded task**, such as a coding test, on either build.
- **The original weights' score**, and so how far each build is from them.
- **Which difference between the builds** gives the speed gap or the score gap.
- **A second start** of any setting.
- **A fixed draft depth** on oMLX, and the drafts-off starts and TensorFold's build on oMLX 0.8.2.
- **A lower reasoning effort on oMLX**, and any way to close the think block there.
- **Long prompts**, several users at once, and images.
- **What the timed replies say.** I read back two replies per build on TensorFold and the short previews of the answer check.

## Credit

- **Engines.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart). [oMLX](https://github.com/jundot/omlx) by [@jundotkim](https://x.com/jundotkim).
- **Weights.** The 4-bit build by TensorFold and the oQ4e build by Jundot.
- **Model.** GLM-5.3 Flash by Z.ai.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
