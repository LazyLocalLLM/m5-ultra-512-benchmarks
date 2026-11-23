# Finding 19. Seven builds on TensorFold 1.3.3, a version refresh

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Updated on 23 Nov 2026 at 09:33 SGT. TensorFold 1.3.4 reran every build here but Flash Next 6-bit and Hy4-flash 8-bit, in [finding 27](../27_tensorfold_134_refresh). It is a little faster on Flash Next 4-bit and level on the rest. This page stays as the 1.3.3 record.

Updated on 22 Nov 2026 at 16:43 SGT with Qwen3.8 Flash Next 6-bit and Hy4-flash 8-bit, brought back from the external drive and run on 1.3.3 from 15:57 SGT.

ELI5: TensorFold 1.3.3 came out on 22 Nov 2026 at 04:58 SGT. My lines for these builds came from 1.3.2, so I reran them on the new release, one fresh server start a setting, at the same settings and on the same texts. One cell came in low, so I tested it again against the old release on the same night. DeepSeek V4.1 Flash on 1.3.3 has its own page, [finding 18](../18_dsv41_tensorfold_133).

**I see no speed change on TensorFold 1.3.3 on any of these seven builds. Text by text against the latest 1.3.2 start, the middle ratio sits between 0.96 and 1.06 on every test but two, and the replies I checked are the same. One was Qwen3.8 27B with its own sampler, 136.2 tok/s on its first 1.3.3 start against 161.3 on 1.3.2. Run again on one night, the two releases wrote 147.0 and 147.3 over 20 requests each, so that was a low start and not the release. The other is Hy4-flash 8-bit with the draft-bits switch and its own sampler, 1.08, with 1.3.3 faster on only 3 of 5 texts. One thing is new. GLM-5.3 Flash can now draft with a DFlash2 model on a Mac, and it wrote 84.2 tok/s with its own sampler against 79.8 with the built-in MTP drafts, with the same replies. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 22 Nov 2026.**

| Model and build | Max on 1.3.3 | Max on 1.3.2 | Median on 1.3.3 | Median on 1.3.2 |
|---|---|---|---|---|
| Qwen3.8 27B, 4-bit, DFlash2 drafter | 315.3 | 328.9 | 164.1 | 161.3 |
| Qwen3.8 Flash Next, 4-bit | 209.5 | 206.8 | 130.9 | 129.7 |
| Qwen3.8 Flash Next, 6-bit | 201.3 | 200.1 | 114.5 | 114.1 |
| GLM-5.3 Flash, 4-bit, MTP drafts | 102.8 | 102.0 | 79.8 | 80.9 |
| GLM-5.3 Flash, 4-bit, DFlash2 draft model | 101.6 | not possible | 84.2 | not possible |
| GLM-5.3 Flash, oQ4e, MTP drafts | 84.8 | 82.9 | 64.9 | 67.5 |
| Hy4-flash, 4-bit, defaults | 63.8 | 64.6 | 44.2 | 51.3 |
| Hy4-flash, 4-bit, `TF_HY4_DRAFT_BITS=8` | 73.3 | 71.5 | 54.5 | 51.0 |
| Hy4-flash, 8-bit, defaults | 46.7 | 47.6 | 38.2 | 37.1 |
| Hy4-flash, 8-bit, `TF_HY4_DRAFT_BITS=8` | 55.2 | 53.4 | 44.8 | 40.9 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The 1.3.2 columns** are the latest 1.3.2 start of each setting, in findings [10](../10_hy4_flash_tensorfold_132), [11](../11_qwen38_tensorfold_132) and [15](../15_glm53_flash_two_builds). Their rows are in those folders.
- **One median looks apart and is not.** Hy4-flash 4-bit at defaults reads 44.2 against 51.3, and its five same-text pairs have a middle ratio of 1.00.
- **The Qwen3.8 27B median is its latest 1.3.3 start.** Four 1.3.3 starts read 136.2, 154.3, 154.3 and 164.1 on the same five texts. It has its own section below.
- **"Not possible"** means 1.3.2 refused to start GLM-5.3 Flash with a DFlash2 draft model on this Mac, as finding 15 records.
- **Hy4-flash wrote reasoning text**, as on 1.3.2. The other rows are answer text.

## Chart

ELI5: The same test on both releases. One pair of bars a build.

![Bars of writing speed in tokens per second, greedy at temperature 0, new code, replies of up to 2,048 tokens, 1K prompt, on TensorFold 1.3.2 and 1.3.3. Qwen3.8 27B 4-bit 328.9 and 315.3. Qwen3.8 Flash Next 4-bit 206.8 and 206.8. GLM-5.3 Flash 4-bit 101.4 and 102.1. GLM-5.3 Flash oQ4e 80.7 and 81.2. Hy4-flash 4-bit 64.6 and 61.8. Qwen3.8 Flash Next 6-bit 200.1 and 201.3. Hy4-flash 8-bit at defaults 47.6 and 46.7.](chart_max.png)

- **The chart is the 1K prompt only.** For four of its seven builds the max in the table above is the 4K cell. The Hy4-flash bars are at defaults.

## Same-text pairs

ELI5: Each request's text is picked from its size and repeat number, so 1.3.3 got the very texts 1.3.2 got. A pair is one text on both releases. If a release were faster, most pairs would say so.

1.3.3 over the latest 1.3.2 start. "Faster on" counts the pairs where 1.3.3 wrote faster, then the middle ratio.

| Build | Long code replies | Short code replies | Own sampler | Copy task | Counting toy |
|---|---|---|---|---|---|
| Qwen3.8 27B, 4-bit | 6 of 10, 1.01 | 9 of 10, 1.06 | 1 of 5, 0.89 | 6 of 10, 1.01 | 8 of 10, 1.00 |
| Qwen3.8 Flash Next, 4-bit | 6 of 10, 1.03 | 5 of 10, 1.00 | 2 of 5, 0.98 | 8 of 10, 1.00 | 9 of 10, 1.00 |
| Qwen3.8 Flash Next, 6-bit | 5 of 10, 1.00 | 4 of 10, 0.96 | 4 of 5, 1.02 | 1 of 10, 1.00 | 5 of 10, 1.00 |
| GLM-5.3 Flash, 4-bit, MTP | 6 of 10, 1.01 | 5 of 10, 1.00 | 2 of 5, 0.98 | 3 of 10, 0.99 | 6 of 10, 1.01 |
| GLM-5.3 Flash, oQ4e, MTP | 6 of 10, 1.03 | 6 of 10, 1.02 | 2 of 5, 0.98 | 4 of 10, 1.00 | 5 of 10, 1.00 |
| Hy4-flash, 4-bit, defaults | 5 of 10, 1.00 | 6 of 10, 1.02 | 2 of 5, 1.00 | not run | not run |
| Hy4-flash, 4-bit, draft-bits switch | 6 of 10, 1.02 | 8 of 10, 1.02 | 4 of 5, 1.02 | not run | not run |
| Hy4-flash, 8-bit, defaults | 5 of 10, 1.01 | 6 of 10, 1.06 | 3 of 5, 1.04 | not run | not run |
| Hy4-flash, 8-bit, draft-bits switch | 6 of 10, 1.00 | 6 of 10, 1.01 | 3 of 5, 1.08 | not run | not run |

- **One cell stands out, the Qwen3.8 27B sampler at 0.89.** The next section runs it again.
- **Hy4-flash 8-bit with the switch reads 1.08 with its own sampler.** 1.3.3 was faster on only 3 of its 5 texts, and its five runs went from 39.2 to 49.4. One start a release can't call that a change.
- **Everything else sits between 0.96 and 1.06.** I call none of it a change.
- **Same replies.** 250 of 250 short greedy answers match 1.3.2 on the three Qwen builds. On GLM-5.3 Flash and Hy4-flash a fuller check of 50 questions asked twice, with thinking and answer text together, matches 1.3.2 on 100 of 100. That holds for both Hy4-flash builds at both settings.

## The Qwen3.8 27B sampler, run again on one night

ELI5: The first 1.3.3 start read 136.2 where 1.3.2 had read 161.3 the day before. The 1.3.3 notes list a change to this model's sampled drafts, so a real change was possible. One start a release on different days can't tell. Homebrew keeps the old program when it upgrades, so I ran both releases back to back, in the order 1.3.3, 1.3.2, 1.3.2, 1.3.3, with 10 sampled texts a start.

Decode tok/s, the model's own sampler, mixed text, 512-token replies, 4K prompt, 22 Nov 2026 from 08:05 SGT.

| Start | Release | 10 texts | The first 5 texts | Greedy code, 512, 1K | Greedy code, 512, 4K |
|---|---|---|---|---|---|
| `7cab499e2054` | 1.3.3 | 146.8 (126.9 to 180.3) | 154.3 | 250.1 | 221.9 |
| `08c4f281a524` | 1.3.2 | 147.9 (129.3 to 166.6) | 151.6 | 245.6 | 204.5 |
| `c6618a74cbb9` | 1.3.2 | 143.0 (127.9 to 164.7) | 152.0 | 242.9 | 214.1 |
| `76824af96911` | 1.3.3 | 147.0 (121.6 to 193.5) | 154.3 | 228.1 | 229.0 |
| `e2420150405f` | 1.3.3, the standard 5 texts only | not run | 164.1 (133.1 to 184.0) | not run | not run |

- **The two releases wrote the same.** Over 20 sampled requests a release the middle is 147.0 on 1.3.3 and 147.3 on 1.3.2.
- **Text by text there is no winner.** 1.3.3 was faster on 5 of 10 and 6 of 10 pairs, with a middle ratio of 1.03 both times.
- **So the 136.2 was a low start.** Its five runs went 127, 128, 136, 181 and 158. The same five texts read 154.3 on both 1.3.3 starts an hour later.
- **And the 161.3 of 21 Nov was a high one.** The kept 1.3.2 program read 151.6 and 152.0 on those five texts on this night.
- **This test spreads widely on this model.** One text read 166, 194 and 127 on three 1.3.3 starts.
- **A caution on the first start.** I rebuilt pages on this Mac while its sampler block ran, a few seconds of one core. I built nothing during the four starts above.
- **One more start for the summary page.** Every median on the summary is 5 texts, so I took one more 1.3.3 start with the standard block at 08:19 SGT. It read 164.1. By my rule of the latest start that is the summary's line, and it is one start of a test that read 136.2 to 164.1 on this release.

## GLM-5.3 Flash with a DFlash2 draft model

ELI5: A draft model guesses several tokens ahead and the big model checks them. GLM-5.3 Flash ships with a built-in drafter, MTP. TensorFold 1.3.3 can also use a separate draft model, DFlash2, on a Mac. 1.3.2 refused to.

Decode tok/s on TensorFold's 4-bit build, 1.3.3, one start each. MTP is run `3a880091476a` and DFlash2 is run `1e3c46e52f5f`.

| Test | Prompt | MTP drafts, the default | DFlash2 draft model |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 102.1 (97.7 to 105.0) | 101.6 (97.8 to 107.8) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 102.8 (97.3 to 107.2) | 101.4 (100.6 to 108.7) |
| Greedy, new code, 512-token replies | 1K | 100.5 (92.1 to 103.4) | 103.5 (100.8 to 111.0) |
| Greedy, new code, 512-token replies | 4K | 99.9 (92.4 to 101.6) | 99.0 (98.0 to 107.2) |
| Own sampler, mixed text, 512-token replies | 4K | 79.8 (72.6 to 89.0) | 84.2 (83.6 to 85.4) |

- **With the sampler DFlash2 was faster on 4 of 5 texts**, with a middle ratio of 1.06. 84.2 / 79.8 = 1.06.
- **On short code replies it was faster on 8 of 10 texts**, middle ratio 1.06. On long ones it was level, 7 of 10 with 1.00.
- **Same replies.** 100 of 100 match the MTP start, 50 short greedy questions asked twice.
- **One start each.** A 6% gap is the size of the spread between two starts elsewhere on this page, so I call DFlash2 at least as fast and not yet faster.
- **The draft model.** [incoai/GLM-5.3-Flash-DFlash2](https://huggingface.co/incoai/GLM-5.3-Flash-DFlash2) @ 6cc6c481, 2.2 GiB, passed with `--drafter`. The banner reads "drafts: DFlash2 + copies".
- **The release notes name this** as pull request 3920.

## Hy4-flash and the draft-bits switch

ELI5: [Finding 10](../10_hy4_flash_tensorfold_132) found a variable in TensorFold's source that stores the draft helper at fewer bits and writes faster. I checked that it still does on 1.3.3.

- **Still faster on every code text.** On the 4-bit build, against the default start of this run, `TF_HY4_DRAFT_BITS=8` was faster on 10 of 10 long replies with a middle ratio of 1.16, and on 10 of 10 short ones with 1.18.
- **Same text.** 100 of 100 replies match the default start, and both match 1.3.2.
- **The 8-bit build too.** Brought back from the external drive and run on 1.3.3, the switch was faster on 10 of 10 long replies with a middle ratio of 1.17, on 10 of 10 short ones with 1.13, and on 5 of 5 sampled texts with 1.11. 100 of 100 replies match its default start.
- **That is three pairs of starts a build now**, two on 1.3.2 and one on 1.3.3.

## The setup

ELI5: One engine at its newest release, the same weights and serve lines as the 1.3.2 pages.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.3, released 22 Nov 2026 04:58 SGT, installed from the project's Homebrew tap. The formula's SHA-256 equals the digest GitHub lists for `tensorfold-1.3.3-macos-arm64.tar.gz`. `tensorfold-native --version` prints 1.3.3.
- **It was still the newest release** when I published this, checked on 22 Nov 2026 at 08:21 SGT, and again at 16:35 SGT for the two added builds.
- **The 1.3.2 program of the sampler test** is the copy Homebrew kept in its Cellar, run by its full path. Nothing was installed for it.
- **Weights.**
  - [TensorFold/Qwen3.8-27B-MLX-4bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) with the drafter [z-lab/Qwen3.8-27B-DFlash2](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2).
  - [TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP) and [TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP).
  - [TensorFold/GLM-5.3-Flash-MLX-4bit-MTP](https://huggingface.co/TensorFold/GLM-5.3-Flash-MLX-4bit-MTP) and [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp), a build made for another engine.
  - [TensorFold/Hy4-flash-MLX-4bit-MTP](https://huggingface.co/TensorFold/Hy4-flash-MLX-4bit-MTP) and [TensorFold/Hy4-flash-MLX-8bit-MTP](https://huggingface.co/TensorFold/Hy4-flash-MLX-8bit-MTP).
- **Serve lines** are those of findings 10, 11 and 15, unchanged. Qwen3.8 27B at `--context 262144 --parallel 1` with `--drafter`. Flash Next at the M5 Ultra line of the project's recipe. GLM-5.3 Flash and Hy4-flash at `--context 131072 --parallel 1`.
- **Thinking** off for the Qwen and GLM builds, and on for Hy4-flash, as on 1.3.2.

| Run id | Build and setting | Started, SGT, 22 Nov 2026 |
|---|---|---|
| `6a8e3b10559e` | Qwen3.8 27B 4-bit, 1.3.3 | 06:56 |
| `58be1ddd40c3` | Qwen3.8 Flash Next 4-bit, 1.3.3 | 07:03 |
| `3a880091476a` | GLM-5.3 Flash 4-bit, MTP, 1.3.3 | 07:10 |
| `1e3c46e52f5f` | GLM-5.3 Flash 4-bit, DFlash2, 1.3.3 | 07:19 |
| `0d05d0d3d24c` | GLM-5.3 Flash oQ4e, MTP, 1.3.3 | 07:26 |
| `9e3d9e5dce53` | Hy4-flash 4-bit, defaults, 1.3.3 | 07:38 |
| `95019a9ea00a` | Hy4-flash 4-bit, `TF_HY4_DRAFT_BITS=8`, 1.3.3 | 07:49 |
| `7cab499e2054` | Qwen3.8 27B 4-bit, sampler test, 1.3.3 | 08:05 |
| `08c4f281a524` | Qwen3.8 27B 4-bit, sampler test, 1.3.2 | 08:07 |
| `c6618a74cbb9` | Qwen3.8 27B 4-bit, sampler test, 1.3.2 | 08:10 |
| `76824af96911` | Qwen3.8 27B 4-bit, sampler test, 1.3.3 | 08:12 |
| `e2420150405f` | Qwen3.8 27B 4-bit, the standard sampler block, 1.3.3 | 08:19 |
| `e4b66d27e9cb` | Qwen3.8 Flash Next 6-bit, 1.3.3 | 15:57 |
| `998afef57c31` | Hy4-flash 8-bit, defaults, 1.3.3 | 16:05 |
| `bfcced24637c` | Hy4-flash 8-bit, `TF_HY4_DRAFT_BITS=8`, 1.3.3 | 16:20 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as the 1.3.2 pages. Only the release changed.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** is each model's own, as on its 1.3.2 page.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. Each prompt opens with a new session line so no prompt cache can hit. Timed requests show at most 3 cached tokens.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token.
- **Repeats.** 5 timed runs per cell, and 10 for the same-night sampler test. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **One start a release, except the Qwen3.8 27B sampler.** A gap of a few percent between two starts is not a version change.
- **Different days.** The 1.3.2 starts ran on 21 Nov 2026 and the 1.3.3 starts on 22 Nov. The sampler test is the one place both ran on one night.
- **Reasoning text is not answer text.** The Hy4-flash rows are reasoning speeds.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 502 raw rows from the bench database. 450 timed requests and 52 warm-ups.
- **`runs.csv`.** The 15 runs behind them, with engine, version, start time, settings and sampling.
- **The 1.3.2 rows** are in findings 10, 11 and 15.

From the top of this repository.

```bash
python3 tools/summarize.py findings/19_tensorfold_133_refresh
```

## What I did not verify

- **The drafts-off lines** of GLM-5.3 Flash and Hy4-flash on 1.3.3.
- **A second start** of any setting but the Qwen3.8 27B sampler.
- **Why the Qwen3.8 27B sampler read higher on 21 Nov than on 22 Nov**, on the same 1.3.2 program.
- **DFlash2 on the oQ4e build**, and DFlash2 against MTP on a second start.
- **What the timed replies say.** I read back one copy reply and one counting reply on four builds, as the job does, and no other.
- **Answer quality, long prompts, and two users at once.**

## Credit

- **Engine and MLX builds.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Draft models.** The Qwen DFlash2 drafter by [z-lab](https://huggingface.co/z-lab). The GLM DFlash2 drafter by [incoai](https://huggingface.co/incoai).
- **The oQ4e build.** Jundot, the author of oMLX.
- **Models.** Qwen3.8 27B and Flash Next by Qwen. GLM-5.3 Flash by Z.ai. Hy4-flash by Tencent.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
