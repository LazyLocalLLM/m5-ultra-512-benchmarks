# Finding 27. Eight settings on TensorFold 1.3.4, a version refresh

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold 1.3.4 came out on 23 Nov 2026 at 04:53 SGT. Its notes say Qwen3.8 Flash Next decodes 2 to 5% faster on one stream on an M5 Ultra, with the same tokens. My lines for these builds came from 1.3.3, so I reran them on the new release at the same settings and on the same texts. Then I ran 1.3.4 and 1.3.3 back to back on one night for the two Qwen builds, and once more for Flash Next. DeepSeek V4.1 Flash ran the same way, from a source build of each tag.

**TensorFold 1.3.4 is about 2% faster on Qwen3.8 Flash Next 4-bit and level on the seven other settings I reran. On the counting toy, the steadiest test here, five of six 1.3.4 starts wrote 377.8 to 379.3 tok/s at a 1K prompt, where four 1.3.3 starts on two days wrote 369.4 to 369.8. 377.8 / 369.8 = 1.022. Three 1.3.4 starts run beside one 1.3.3 start were faster on 30 of 30 counting pairs, with a middle ratio of 1.02. The sixth 1.3.4 start ran partly at each release's speed and came out level. The replies are the same as on 1.3.3 on every check, and the Flash Next server holds 7.2 GiB less. DeepSeek V4.1 Flash, Qwen3.8 27B, GLM-5.3 Flash and Hy4-flash show no speed change I can call. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 23 Nov 2026.**

| Model and build | Max on 1.3.4 | Max on 1.3.3 | Median on 1.3.4 | Median on 1.3.3 |
|---|---|---|---|---|
| Qwen3.8 Flash Next, 4-bit | 211.5 | 209.5 | 128.4 | 130.9 |
| Qwen3.8 27B, 4-bit, DFlash2 drafter | 323.4 | 315.3 | 149.6 | 164.1 |
| GLM-5.3 Flash, 4-bit, MTP drafts | 102.5 | 102.8 | 78.5 | 79.8 |
| GLM-5.3 Flash, 4-bit, DFlash2 draft model | 104.7 | 101.6 | 85.9 | 84.2 |
| GLM-5.3 Flash, oQ4e, MTP drafts | 84.9 | 84.8 | 65.9 | 64.9 |
| Hy4-flash, 4-bit, defaults | 63.8 | 63.8 | 48.0 | 44.2 |
| Hy4-flash, 4-bit, `TF_HY4_DRAFT_BITS=8` | 79.0 | 73.3 | 51.6 | 54.5 |
| DeepSeek V4.1 Flash, the maker's files | 105.7 | 108.0 | 69.9 | 74.5 |

- **Max** is the middle of 5 greedy runs on new code with replies of up to 2,048 tokens, at the faster of the 1K and 4K prompts.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **Each 1.3.4 figure is the latest start that ran that test**, by my rule. The 1.3.3 columns are the lines the summary page held before today, from [finding 19](../19_tensorfold_133_refresh) and, for DeepSeek, [finding 18](../18_dsv41_tensorfold_133). They ran on 22 Nov 2026.
- **A gap in this table is not a release change** unless the text-by-text pairs below agree. Max and median move by a few percent from one start to the next on one release.
  - The Hy4-flash max with the switch reads 79.0 against 73.3, yet text by text it is faster on 5 of 10 long code pairs with a middle ratio of 1.00.
  - The Qwen3.8 27B median reads 149.6 against 164.1. On the same night the two releases wrote 147.8 and 140.4 over 20 sampled requests each. Its own section is below.
  - DeepSeek's 1.3.3 starts on this night wrote 106.6 and 97.6 at the max, so 105.7 sits inside them.
- **The Flash Next table cells don't show its gain.** Its long code cell at 4K spread by 9% between three starts on 1.3.3 and by 10% on 1.3.4. The counting toy spread by 0.1% at 1K and 0.8% at 4K on 1.3.3, so it can show a 2% change.
- **Hy4-flash wrote reasoning text**, as on 1.3.3. The other rows are answer text.
- **Not rerun.** Qwen3.8 Flash Next 6-bit and Hy4-flash 8-bit are parked on the external drive. Their 1.3.3 lines stay on the summary page, labelled 1.3.3.

## Chart

ELI5: The counting toy asks the model to count upward, so every reply is the same tokens and the drafts guess almost all of them. That makes it the steadiest speed test I have. One pair of bars a step of the test, one start a bar.

![Bars of writing speed in tokens per second for Qwen3.8 Flash Next 4-bit on the counting toy, greedy, 512-token replies, 1K prompt, four starts of TensorFold 1.3.3 against four of 1.3.4. First start of each release, 369.5 and 378.7. Same night 1, 369.4 and 369.9. Same night 2, 369.8 and 377.9. Check, 369.8 and 377.8.](chart_count.png)

- **The first pair ran on different days.** 1.3.3 ran on 22 Nov at 07:03 SGT and 1.3.4 on 23 Nov at 05:36 SGT. The other pairs ran on 23 Nov from 08:07 SGT.
- **The check pair** is the 1.3.3 start of 09:24 SGT and the 1.3.4 start right after it, the slowest of the three 1.3.4 check starts. The other two read 378.8 and 379.3.

## Qwen3.8 Flash Next 4-bit, both releases on one night

ELI5: One start a release on different days can't tell a 2% change from a good start. Homebrew keeps the old program when it upgrades, so I ran both releases back to back in the order 1.3.4, 1.3.3, 1.3.3, 1.3.4, with the same texts each time.

Decode tok/s, greedy unless named, 512-token replies unless named. Each cell is the middle of 5 runs.

| Start | Release | Counting, 1K | Counting, 4K | Copy, 1K | Copy, 4K | Code, 2,048, 1K | Code, 2,048, 4K | Own sampler, 4K |
|---|---|---|---|---|---|---|---|---|
| `58be1ddd40c3`, 22 Nov 07:03 | 1.3.3 | 369.5 | 359.5 | 322.3 | 327.7 | 206.8 | 209.5 | 130.9 |
| `8d40d469c26c`, 23 Nov 05:36 | 1.3.4 | 378.7 | 367.4 | 329.4 | 325.4 | 209.9 | 191.6 | 132.9 |
| `bd09ee7804f8`, 23 Nov 08:07 | 1.3.4 | 369.9 | 355.2 | 317.6 | 323.9 | 210.9 | 211.4 | 129.5 |
| `f30128456f7f`, 23 Nov 08:11 | 1.3.3 | 369.4 | 358.2 | 321.3 | 312.2 | 198.2 | 191.7 | 130.4 |
| `3cd0d10d6e5a`, 23 Nov 08:16 | 1.3.3 | 369.8 | 356.8 | 322.0 | 326.2 | 214.3 | 200.9 | 127.3 |
| `51182015de42`, 23 Nov 08:20 | 1.3.4 | 377.9 | 364.4 | 329.4 | 331.2 | 211.5 | 205.1 | 128.4 |

- **1.3.3 counts at one speed.** Three starts on two days read 369.4 to 369.8 at 1K and 356.8 to 359.5 at 4K. The fourth, in the check below, read 369.8 and 359.1.
- **Two of these 1.3.4 starts count faster.** At 1K, 378.7 / 369.5 = 1.025 and 377.9 / 369.8 = 1.022. At 4K, 367.4 / 359.5 = 1.022 and 364.4 / 356.8 = 1.021.
- **The third 1.3.4 start ran partly at each speed.** In `bd09ee7804f8` the first two counting runs at 1K read 378.5 and 377.9, 1.3.4's speed, and the other three read 361.1, 369.9 and 367.9. Its five 4K counting runs, taken in turn with the 1K ones, read 352.9 to 360.6, 1.3.3's speed, from the first. Its copy runs at 1K read below the 1.3.4 starts `8d40d469c26c` and `51182015de42` from the second run on. Its server log has the same lines as the other 1.3.4 starts. I did not find the cause.
- **Text by text on the same night,** each 1.3.4 start against each of the two 1.3.3 starts, so four pairs for each text.
  - Counting toy. `51182015de42` was faster on 20 of 20 pairs, middle ratio 1.02, and `bd09ee7804f8` on 12 of 20, 1.00. Together 32 of 40, 1.02.
  - Copy task. 16 of 20 at 1.03, and 8 of 20 at 0.99. Together 24 of 40, 1.01.
  - Code with 512-token replies, 25 of 40, 1.03.
  - Code with replies of up to 2,048 tokens, 30 of 40, 1.04.
  - Own sampler, 12 of 20, 1.02.
- **The first 1.3.4 start,** of 05:36 SGT, was faster than both same-night 1.3.3 starts on 20 of 20 counting pairs, middle ratio 1.03. Against the 1.3.3 start of 22 Nov it was faster on 10 of 10, from 1.021 to 1.040. On code it was faster on 9 of 10 short replies and 7 of 10 long ones, middle ratios 1.07 and 1.05.
- **Memory.** Every 1.3.4 start held 152.9 GiB when ready and every 1.3.3 start held 160.1. 160.1 − 152.9 = 7.2 GiB.
- **The notes name this change** as pull request 4547. They say the 4-bit expert scale and bias index is now built on Macs with tensor units, the M5 among them.

### The counting check

ELI5: One slow start in three could be the release or the start. So I ran four more short starts, three of 1.3.4 and one of 1.3.3, with the copy task and the counting toy only, in the order 1.3.4, 1.3.4, 1.3.3, 1.3.4.

| Start | Release | Counting, 1K | Counting, 4K | Copy, 1K | Copy, 4K |
|---|---|---|---|---|---|
| `ccce5f6ee788`, 09:21 | 1.3.4 | 378.8 | 367.1 | 361.8 | 338.8 |
| `0a30435cc437`, 09:22 | 1.3.4 | 379.3 | 367.8 | 329.8 | 330.9 |
| `2b05afe05352`, 09:24 | 1.3.3 | 369.8 | 359.1 | 321.9 | 322.1 |
| `dd4ddf3cf8cd`, 09:25 | 1.3.4 | 377.8 | 366.1 | 360.3 | 334.8 |

- **All three 1.3.4 starts counted faster.** Against the 1.3.3 start, 30 of 30 counting pairs were faster, middle ratio 1.02, the lowest 1.018. On the copy task 27 of 30 were, middle ratio 1.03.
- **So the slow start is one of six.** Five 1.3.4 starts counted at 377.8 to 379.3 at 1K. `bd09ee7804f8` read 369.9.
- **The arithmetic at 1K.** 378.8 / 369.8 = 1.024. 379.3 / 369.8 = 1.026. 377.8 / 369.8 = 1.022.

## Qwen3.8 27B, both releases on one night

ELI5: The model's own sampler on this build spreads widely from start to start, as [finding 19](../19_tensorfold_133_refresh) showed. So I ran 10 texts a start and four starts, two a release.

Decode tok/s, the model's own sampler on mixed text at 4K, and greedy code as a control. 512-token replies.

| Start | Release | Own sampler, 10 texts | The first 5 texts | Greedy code, 1K | Greedy code, 4K |
|---|---|---|---|---|---|
| `02652a7d80a2`, 08:24 | 1.3.4 | 145.1 | 144.9 | 239.8 | 205.9 |
| `8e2c327c932a`, 08:26 | 1.3.3 | 139.1 | 139.2 | 234.0 | 229.4 |
| `3c0ff50c3c59`, 08:29 | 1.3.3 | 146.1 | 138.8 | 246.0 | 216.1 |
| `2813d10958a6`, 08:31 | 1.3.4 | 151.5 | 170.4 | 230.1 | 219.3 |
| `52b0c20da4cb`, 08:33 | 1.3.4, the standard blocks | not run | 149.6 | not run | not run |

- **Over 20 sampled requests a release** the middle is 147.8 on 1.3.4 and 140.4 on 1.3.3. 147.8 / 140.4 = 1.05.
- **Text by text it is too spread to call.** 1.3.4 was faster on 25 of 40 pairs with a middle ratio of 1.04, and single pairs ran from 0.86 to 1.60.
- **Greedy code is level.** Faster on 22 of 40 pairs, middle ratio 1.01.
- **On 22 Nov this test read 136.2 to 164.1** on four 1.3.3 starts and the same five texts. Tonight's two 1.3.3 starts sit inside that. One 1.3.4 start read above it, 170.4.
- **The summary's median is the last start,** `52b0c20da4cb`, since the summary takes 5 texts. Its long code read 323.4 at 1K, against 315.3 on 1.3.3, and text by text that was faster on 5 of 10 pairs with a middle ratio of 1.01.
- **The notes touch this model's sampler.** It now accepts presence and frequency penalties (pull request 3145). These requests send both at 0, which the notes say leaves the default path unchanged.

## Same-text pairs, the other builds

ELI5: Each request's text is picked from its size and repeat number, so 1.3.4 got the very texts 1.3.3 got. A pair is one text on both releases. If a release were faster, most pairs would say so.

1.3.4 over the 1.3.3 start it replaces, one start each. "Faster on" counts the pairs where 1.3.4 wrote faster, then the middle ratio.

| Build | Long code replies | Short code replies | Own sampler | Copy task | Counting toy |
|---|---|---|---|---|---|
| Qwen3.8 27B, 4-bit | 5 of 10, 1.01 | 2 of 10, 0.97 | 2 of 5, 0.95 | 6 of 10, 1.01 | 6 of 10, 1.00 |
| GLM-5.3 Flash, 4-bit, MTP | 4 of 10, 1.00 | 5 of 10, 1.00 | 2 of 5, 0.97 | 6 of 10, 1.00 | 4 of 10, 0.99 |
| GLM-5.3 Flash, 4-bit, DFlash2 | 8 of 10, 1.01 | 2 of 10, 0.95 | 4 of 5, 1.01 | not run | not run |
| GLM-5.3 Flash, oQ4e, MTP | 4 of 10, 0.98 | 6 of 10, 1.02 | 2 of 5, 0.99 | 8 of 10, 1.01 | 3 of 10, 0.99 |
| Hy4-flash, 4-bit, defaults | 5 of 10, 0.99 | 4 of 10, 0.99 | 2 of 5, 1.00 | not run | not run |
| Hy4-flash, 4-bit, draft-bits switch | 5 of 10, 1.00 | 6 of 10, 1.02 | 0 of 5, 0.99 | not run | not run |

- **The 1.3.3 starts** are those of finding 19, run on 22 Nov 2026. The 1.3.4 starts ran on 23 Nov from 05:29 SGT.
- **Two cells read 0.95, both one start each.**
  - GLM-5.3 Flash with the DFlash2 draft model on short code was faster on 2 of 10. On long code it was faster on 8 of 10. The notes change this draft head's matmul on Metal for NaN and Inf only, with finite outputs unchanged (pull request 4396).
  - The Qwen3.8 27B sampler on its first 1.3.4 start. On the same night above, the two releases show no change I can call.
- **Hy4-flash with the switch and its own sampler** was slower on all 5 texts, by 1% at the middle. One start each.
- **Everything else sits between 0.97 and 1.02.** I call none of it a change.

## DeepSeek V4.1 Flash

ELI5: DeepSeek runs on its own TensorFold server, built from source. I built it at the 1.3.4 tag and ran it against the 1.3.3 build of [finding 18](../18_dsv41_tensorfold_133) on one night, in the order 1.3.3, 1.3.4, 1.3.4, 1.3.3, on the same texts.

Decode tok/s, greedy unless named, the middle of 5 runs.

| Test | 1.3.3, `0e80ed2d7e88` | 1.3.4, `874680cb7d49` | 1.3.4, `33d0baeed473` | 1.3.3, `e19609544fdd` |
|---|---|---|---|---|
| Code, replies up to 2,048 tokens, 4K | 106.6 | 106.4 | 105.7 | 97.6 |
| Own sampler, mixed text, 4K | 70.8 | 73.8 | 69.9 | 71.2 |
| Code, 512-token replies, 32K | 90.4 | 86.7 | 92.5 | 80.8 |
| Prose, 512-token replies, 1K | 74.5 | 74.2 | 74.5 | 72.8 |
| Copy task, 1K | 188.7 | 190.2 | 185.1 | 180.4 |
| Counting toy, 1K | 138.9 | 139.0 | 138.3 | 132.0 |
| Started, SGT, 23 Nov 2026 | 06:38 | 07:04 | 07:30 | 07:46 |

- **Level with the first 1.3.3 start.** Text by text, each 1.3.4 start against `0e80ed2d7e88` has middle ratios from 0.98 to 1.02 on every test.
- **The second 1.3.3 start ran low.** Against its own first start it was slower on 10 of 10 counting pairs, middle ratio 0.96. So 1.3.4's middle ratios over it, 1.00 to 1.06, come from that start and not the release.
- **First token at 4K shows no clear change.** With mixed text it came at 3.52 s on both 1.3.4 starts and 3.66 s on both 1.3.3 starts. With code and 512-token replies the four starts read 3.68, 3.50, 3.67 and 3.69 s, in run order. With replies of up to 2,048 tokens they read 3.88, 3.53, 4.07 and 4.19 s.
- **The notes change cold prompts and the Engram row cache** on this server (pull request 3459). The log shows it. 1.3.4 caches 4,194,304 Engram records a layer and 1.3.3 caches 65,536. The server held 21.9 GiB when ready against 19.8.
- **A 126K prompt ran on the first start of each release only.** First token 80.3 s on 1.3.4 and 79.3 s on 1.3.3. The replies were short, about 76 tokens, so I give no writing speed for it.
- **The summary's line moves from 108.0 to 105.7.** That is the latest start of each release, two nights apart. On this night both releases read 97.6 to 106.6.

## Did the text change

ELI5: Same question, same settings, same answer. A faster release that changes answers would be a different finding.

- **No reply changed on any check.**
  - Qwen3.8 27B and Flash Next. 250 of 250 short greedy answers match their 1.3.3 start, by the harness's identity test.
  - GLM-5.3 Flash, three settings, and Hy4-flash, two settings. 100 of 100 each match their 1.3.3 start. That is 50 short greedy questions asked twice, reasoning and answer hashed together.
  - DeepSeek V4.1 Flash. 250 of 250 short answers match 1.3.3. The engine author's own 16 prompts give the same greedy text on all four starts, 32 of 32 each.
- **The notes say the Flash Next change keeps the same tokens.** The 250 answers agree.

## The setup

ELI5: One engine at its newest release, the same weights and serve lines as the 1.3.3 pages.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.4, released 23 Nov 2026 04:53 SGT, installed from the project's Homebrew tap. The formula changed only its download link and hash. The hash equals the digest GitHub lists for `tensorfold-1.3.4-macos-arm64.tar.gz`. `tensorfold-native --version` prints 1.3.4.
- **It was still the newest release** when I published this, checked on 23 Nov 2026 at 09:33 SGT.
- **The 1.3.3 program of the same-night tests** is the copy Homebrew kept in its Cellar, run by its full path. Nothing was installed for it. It prints 1.3.3.
- **DeepSeek.** TensorFold's DeepSeek server built from the tag v1.3.4, commit `12ebd414`, on 23 Nov 2026 at 05:25 SGT in 76 s, with Zig 0.17.0. `--version` prints `tensorfold-native 1.3.4`. The binary's SHA-256 starts `fbdd1b9bb21c85d0`. The 1.3.3 build is the one of finding 18, commit `1e4a32cb`. The build and serve commands are those of finding 18.
- **Weights.**
  - [TensorFold/Qwen3.8-27B-MLX-4bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) with the drafter [z-lab/Qwen3.8-27B-DFlash2](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2).
  - [TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP).
  - [TensorFold/GLM-5.3-Flash-MLX-4bit-MTP](https://huggingface.co/TensorFold/GLM-5.3-Flash-MLX-4bit-MTP) with the draft model [incoai/GLM-5.3-Flash-DFlash2](https://huggingface.co/incoai/GLM-5.3-Flash-DFlash2), and [Jundot/GLM-5.3-Flash-oQ4e-mtp](https://huggingface.co/Jundot/GLM-5.3-Flash-oQ4e-mtp), a build made for another engine.
  - [TensorFold/Hy4-flash-MLX-4bit-MTP](https://huggingface.co/TensorFold/Hy4-flash-MLX-4bit-MTP).
  - [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017), the maker's own files.
- **Serve lines** are those of findings 18 and 19, unchanged. Qwen3.8 27B at `--context 262144 --parallel 1` with `--drafter`. Flash Next at the M5 Ultra line of the project's recipe, `--context 1048576 --parallel 2`. GLM-5.3 Flash and Hy4-flash at `--context 131072 --parallel 1`. DeepSeek at `--context 131072 --parallel 1` with drafts at defaults, "DSpark + copies".
- **Thinking** off for the Qwen, GLM and DeepSeek builds, and on for Hy4-flash, as on 1.3.3.

| Run id | Build and setting | Started, SGT, 23 Nov 2026 |
|---|---|---|
| `9466f37f6182` | Qwen3.8 27B 4-bit, 1.3.4 | 05:29 |
| `8d40d469c26c` | Qwen3.8 Flash Next 4-bit, 1.3.4 | 05:36 |
| `5d827a9f83a1` | GLM-5.3 Flash 4-bit, MTP, 1.3.4 | 05:43 |
| `2820399df996` | GLM-5.3 Flash 4-bit, DFlash2, 1.3.4 | 05:53 |
| `785a47562751` | GLM-5.3 Flash oQ4e, MTP, 1.3.4 | 06:00 |
| `3523a0e3371d` | Hy4-flash 4-bit, defaults, 1.3.4 | 06:12 |
| `0263bc06d9cf` | Hy4-flash 4-bit, `TF_HY4_DRAFT_BITS=8`, 1.3.4 | 06:24 |
| `0e80ed2d7e88` | DeepSeek V4.1 Flash, 1.3.3 | 06:38 |
| `874680cb7d49` | DeepSeek V4.1 Flash, 1.3.4 | 07:04 |
| `33d0baeed473` | DeepSeek V4.1 Flash, 1.3.4 | 07:30 |
| `e19609544fdd` | DeepSeek V4.1 Flash, 1.3.3 | 07:46 |
| `bd09ee7804f8` | Qwen3.8 Flash Next 4-bit, same night, 1.3.4 | 08:07 |
| `f30128456f7f` | Qwen3.8 Flash Next 4-bit, same night, 1.3.3 | 08:11 |
| `3cd0d10d6e5a` | Qwen3.8 Flash Next 4-bit, same night, 1.3.3 | 08:16 |
| `51182015de42` | Qwen3.8 Flash Next 4-bit, same night, 1.3.4 | 08:20 |
| `02652a7d80a2` | Qwen3.8 27B 4-bit, same night, 1.3.4 | 08:24 |
| `8e2c327c932a` | Qwen3.8 27B 4-bit, same night, 1.3.3 | 08:26 |
| `3c0ff50c3c59` | Qwen3.8 27B 4-bit, same night, 1.3.3 | 08:29 |
| `2813d10958a6` | Qwen3.8 27B 4-bit, same night, 1.3.4 | 08:31 |
| `52b0c20da4cb` | Qwen3.8 27B 4-bit, the standard blocks, 1.3.4 | 08:33 |
| `ccce5f6ee788` | Qwen3.8 Flash Next 4-bit, counting check, 1.3.4 | 09:21 |
| `0a30435cc437` | Qwen3.8 Flash Next 4-bit, counting check, 1.3.4 | 09:22 |
| `2b05afe05352` | Qwen3.8 Flash Next 4-bit, counting check, 1.3.3 | 09:24 |
| `dd4ddf3cf8cd` | Qwen3.8 Flash Next 4-bit, counting check, 1.3.4 | 09:25 |

## How I measured

ELI5: Same Mac, same harness, same texts and same questions as the 1.3.3 pages. Only the release changed.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** is each model's own, as on its 1.3.3 page.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. Each prompt opens with a new session line so no prompt cache can hit.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token.
- **Repeats.** 5 timed runs per cell, and 10 for the 27B same-night sampler test. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **One start a release on GLM-5.3 Flash and Hy4-flash.** A gap of a few percent between two starts is not a version change.
- **Different days.** The 1.3.3 lines ran on 22 Nov 2026 and the 1.3.4 lines on 23 Nov. The same-night tests are the places both ran together.
- **Reasoning text is not answer text.** The Hy4-flash rows are reasoning speeds.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 945 raw rows from the bench database. 850 timed requests and 95 warm-ups.
- **`runs.csv`.** The 24 runs behind them, with engine, version, start time, settings and sampling.
- **The 1.3.3 rows of 22 Nov** are in findings 18 and 19.
- **The answer checks are not in `rows.csv`.** They are hashes of untimed replies.

From the top of this repository.

```bash
python3 tools/summarize.py findings/27_tensorfold_134_refresh
```

## What I did not verify

- **Why the 1.3.4 start `bd09ee7804f8`** ran partly at 1.3.3's speed.
- **The top of the notes' range.** The notes say 2 to 5%. I measured 1.9 to 2.6% on the counting toy, on five starts of six.
- **Flash Next 6-bit and Hy4-flash 8-bit** on 1.3.4. They are parked on the external drive.
- **The drafts-off lines**, and a second 1.3.4 start of GLM-5.3 Flash and Hy4-flash.
- **A writing speed at 126K** for DeepSeek, and the 126K prompt on a second start.
- **What the timed replies say**, beyond the answer checks above.
- **Answer quality, long prompts, and two users at once.**

## Credit

- **Engine and MLX builds.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Draft models.** The Qwen DFlash2 drafter by [z-lab](https://huggingface.co/z-lab). The GLM DFlash2 drafter by [incoai](https://huggingface.co/incoai).
- **The oQ4e build.** Jundot, the author of oMLX.
- **Models.** Qwen3.8 27B and Flash Next by Qwen. GLM-5.3 Flash by Z.ai. Hy4-flash by Tencent. DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
