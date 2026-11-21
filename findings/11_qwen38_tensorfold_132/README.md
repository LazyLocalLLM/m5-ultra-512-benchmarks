# Finding 11. Three Qwen builds on TensorFold 1.3.2, a version refresh

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: TensorFold 1.3.2 came out on 21 Nov 2026 at 03:27 SGT. My lines for these three builds came from 1.3.0, so I reran them on the new release, one fresh server start a build, at the same settings and on the same texts. Max is greedy at temperature 0 while writing new code. Median is the model's own sampler on mixed text.

**On TensorFold 1.3.2, on two server starts, Qwen3.8 27B 4-bit wrote 315.1 and 328.9 tok/s at its max, and 157.4 and 161.3 with its own sampler. Qwen3.8 Flash Next 4-bit wrote 219.4 and 206.8, and 130.1 and 129.7. The 6-bit build wrote 199.8 and 200.1, and 114.2 and 114.1. The answers did not change. On each build 250 of 250 short greedy answers match 1.3.0, on both starts. On new code I see no version change. On easy text Flash Next 4-bit wrote 7% faster than on 1.3.0 on both starts, on every same-text pair. Mac Studio M5 Ultra 512 GB, one user, median of 5 runs, 21 Nov 2026.**

| Build | Max on 1.3.2, two starts | Max on 1.3.0 | Median on 1.3.2, two starts | Median on 1.3.0 |
|---|---|---|---|---|
| Qwen3.8 27B, 4-bit | 315.1 and 328.9 | 331.3 | 157.4 and 161.3 | 148.2 |
| Qwen3.8 Flash Next, 4-bit | 219.4 and 206.8 | 204.4 | 130.1 and 129.7 | 126.7 |
| Qwen3.8 Flash Next, 6-bit | 199.8 and 200.1 | 193.0 | 114.2 and 114.1 | 117.4 |

- **Max** is the middle of 5 greedy runs on new code, replies of up to 2,048 tokens, 1K prompt.
- **Median** is the middle of 5 runs with the model's own sampler, mixed text, 512-token replies, 4K prompt.
- **The 1.3.0 columns** are the defaults starts of [finding 7](../07_qwen38_tensorfold_130), run on 20 and 21 Nov 2026. Their rows are in that folder.
- **Two starts on 1.3.2.** The second starts were added on 21 Nov 2026 at 12:53 SGT and are in their own section below. Finding 7 has five starts of the 27B on 1.3.0, one at defaults and four with a draft switch, and their max cell went from 320.9 to 331.3. The first 1.3.2 start wrote 315.1, below all five. The second wrote 328.9, inside them.

## Chart

ELI5: The top speed on new code for each build on 1.3.2. One bar per build and prompt size.

![Bars of writing speed in tokens per second on TensorFold 1.3.2, greedy at temperature 0, new code, replies of up to 2,048 tokens, the second of two server starts. Qwen3.8 27B 4-bit 328.9 at a 1K prompt and 241.6 at 4K. Qwen3.8 Flash Next 4-bit 206.8 and 194.6. Qwen3.8 Flash Next 6-bit 200.1 and 190.2.](chart_max.png)

## Second starts

ELI5: One start a release can't tell a version change from a lucky or unlucky start. So I started each build a second time on 1.3.2, with the same settings and the same texts, and ran every test again.

Decode tok/s at defaults, the second 1.3.2 start of each build.

| Test | Prompt | 27B 4-bit, `ab1caacd2961` | Flash Next 4-bit, `70284626631f` | Flash Next 6-bit, `51735d12713b` |
|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 328.9 (301.3 to 349.7) | 206.8 (191.7 to 257.5) | 200.1 (188.9 to 219.8) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 241.6 (223.4 to 298.6) | 194.6 (169.8 to 219.6) | 190.2 (172.3 to 218.9) |
| Greedy, new code, 512-token replies | 1K | 243.6 (225.6 to 274.1) | 185.8 (175.2 to 260.3) | 195.1 (186.9 to 201.4) |
| Greedy, new code, 512-token replies | 4K | 216.8 (203.5 to 266.4) | 179.1 (176.1 to 183.6) | 176.7 (161.9 to 202.4) |
| Own sampler, mixed text, 512-token replies | 4K | 161.3 (142.5 to 178.4) | 129.7 (123.5 to 134.1) | 114.1 (110.6 to 121.5) |
| Copy the prompt, 512-token replies | 1K | 812.0 (748.7 to 839.8) | 351.6 (262.9 to 371.7) | 260.0 (213.3 to 283.3) |
| Copy the prompt, 512-token replies | 4K | 660.9 (524.8 to 672.9) | 326.3 (228.4 to 416.8) | 257.4 (199.9 to 332.6) |
| Copy the prompt, 2,048-token replies | 4K | 814.3 (705.9 to 825.8) | 312.3 (277.4 to 344.1) | 253.6 (233.1 to 276.6) |
| Count from 1, 512-token replies | 1K | 448.9 (163.8 to 453.2) | 369.3 (359.4 to 370.0) | 296.4 (290.2 to 297.1) |
| Count from 1, 512-token replies | 4K | 431.7 (418.8 to 441.7) | 358.3 (358.2 to 358.9) | 289.4 (288.7 to 290.8) |

- **The two 1.3.2 starts agree.** Text by text, the second over the first has a middle ratio of 0.99 to 1.05 on every code test, on all three builds.
- **The 27B max is back inside the 1.3.0 starts.** 328.9 against their 320.9 to 331.3. The first start's 315.1 was a low start, and I call no version change on new code.
- **The 27B median.** 161.3 and 157.4 on 1.3.2 against 148.2 on 1.3.0, with overlapping ranges.
- **Flash Next 4-bit is faster on easy text on both starts.** The second start counted 369.3 at 1K and 358.3 at 4K, against 344.2 to 345.6 and 334.9 to 336.4 on four 1.3.0 starts. Against the 1.3.0 start it was faster on 10 of 10 counting pairs and 10 of 10 short copy pairs, each with a middle ratio of 1.07.
- **Its max on new code is not clearly faster.** 219.4 and 206.8 on the two starts, against 204.4 on 1.3.0.
- **Flash Next 6-bit is 2% to 3% faster on easy text on both starts.** The second start was faster than the 1.3.0 start on 10 of 10 counting pairs, 10 of 10 short copy pairs and 5 of 5 long copy pairs, with middle ratios of 1.02, 1.02 and 1.03. It has one 1.3.0 start to stand against.
- **27B copying at 1K is 3% lower on both starts.** 819.4 and 812.0 against 841.0 to 844.8 on the four 1.3.0 starts with copied rows on. 812.0 / 841.0 = 0.97 times. At 4K the 660.9 sits inside their 638.0 to 662.2.
- **Same answers again.** Each second start gave the first start's answer on 250 of 250 short greedy questions, and the 1.3.0 start's on 250 of 250.
- **Long replies.** 7 of 10 ran to 2,048 tokens on the 27B, the shortest at 1,039. 9 of 10 on Flash Next 4-bit, and 4 of 10 on the 6-bit build.
- **Replies checked.** On each second start one extra copy request and one extra counting request were read back. The copy replies had 55 of 56, 56 of 56 and 56 of 56 lines in the prompt word for word. Each counting reply was 155 lines in order.
- **The summary page shows the second starts.** My rule is the latest start at defaults, picked by rule and not by value. So the Flash Next 4-bit max line reads 206.8 and not 219.4.

## Qwen3.8 27B 4-bit

ELI5: A 27B dense model with a small draft model, DFlash2, that guesses several tokens ahead. Each cell is the middle of 5 runs, with the slowest and fastest run in brackets. The last column holds 1.3.2 against Apple's `mlx-lm` on the same weights.

Decode tok/s at defaults. Run `f2d856e22771` on 1.3.0, run `7458a7a5beb6` on 1.3.2, run `0c5446c7acc1` on `mlx-lm` 0.32.2.

| Test | Prompt | TensorFold 1.3.0 | TensorFold 1.3.2 | `mlx-lm` 0.32.2 | 1.3.2 times `mlx-lm` |
|---|---|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 331.3 (245.7 to 342.1) | 315.1 (248.8 to 333.1) | 45.1 | 7.0 |
| Greedy, new code, replies up to 2,048 tokens | 4K | 250.8 (217.1 to 332.2) | 272.5 (212.6 to 301.0) | 44.2 | 6.2 |
| Greedy, new code, 512-token replies | 1K | 227.0 (222.2 to 278.6) | 260.8 (230.8 to 304.8) | 45.2 | 5.8 |
| Greedy, new code, 512-token replies | 4K | 206.2 (166.0 to 266.6) | 201.3 (197.8 to 270.4) | 44.3 | 4.5 |
| Own sampler, mixed text, 512-token replies | 4K | 148.2 (128.2 to 178.6) | 157.4 (138.3 to 173.7) | 43.6 | 3.6 |

- **Max.** 315.1 tok/s. 315.1 / 45.1 = 7.0 times `mlx-lm`.
- **Median.** 157.4 tok/s. 157.4 / 43.6 = 3.6 times `mlx-lm`.
- **The other multiples.** 272.5 / 44.2 = 6.2, 260.8 / 45.2 = 5.8 and 201.3 / 44.3 = 4.5.
- **The `mlx-lm` rows are those of finding 7**, run on 20 Nov 2026 on the same weights and texts. I did not rerun them today.
- **New code is level between the releases.** Two cells rose and two fell. Text by text, 1.3.2 was faster on 5 of 10 long replies with a middle ratio of 0.99, and on 6 of 10 short replies with a middle ratio of 1.02.
- **6 of the 10 long replies ran to 2,048 tokens.** The model ended the other 4 itself, the shortest at 1,516 tokens.

Easy text, greedy at temperature 0, tok/s.

| Test | Prompt | TensorFold 1.3.0 | TensorFold 1.3.2 |
|---|---|---|---|
| Copy the prompt, 512-token replies | 1K | 841.0 (755.4 to 881.3) | 819.4 (753.4 to 874.4) |
| Copy the prompt, 512-token replies | 4K | 659.1 (504.4 to 693.2) | 647.9 (496.7 to 690.4) |
| Copy the prompt, 2,048-token replies | 4K | 824.0 (734.9 to 832.0), run `44a8ff4a173a` | 801.7 (708.0 to 824.2) |
| Count from 1, 512-token replies | 1K | 450.8 (169.0 to 454.8) | 440.4 (338.6 to 454.7) |
| Count from 1, 512-token replies | 4K | 427.6 (422.5 to 444.6) | 431.0 (421.9 to 439.1) |

- **Copying at 1K was below every comparable 1.3.0 start.** 819.4 against 841.0 to 844.8 on the four 1.3.0 starts of finding 7 that had copied rows on. 819.4 / 841.0 = 0.97 times. At 4K the 647.9 sits inside their 638.0 to 662.2. 1.3.2 was faster on 1 of 15 same-text copy pairs, with middle ratios of 0.98 on short replies and 0.97 on long ones. The second start repeated it, as the section "Second starts" shows.
- **Counting was level.** Faster on 3 of 10, middle ratio 0.99.
- **Replies checked.** One extra copy request returned 56 lines, and 55 are in the prompt word for word. One extra counting request returned 155 lines, each the next number. Neither is in `rows.csv`.

## Qwen3.8 Flash Next 4-bit

ELI5: A larger mixture-of-experts model with its own draft head. I served it with the M5 Ultra line of TensorFold's recipe, which is the same text in 1.3.0 and 1.3.2.

Decode tok/s at defaults. Run `7bf80be3a997` on 1.3.0, run `28e2161ebaca` on 1.3.2.

| Test | Prompt | TensorFold 1.3.0 | TensorFold 1.3.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 204.4 (176.6 to 247.5) | 219.4 (187.0 to 259.3) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 195.2 (162.2 to 207.2) | 189.9 (163.0 to 218.4) |
| Greedy, new code, 512-token replies | 1K | 174.1 (151.6 to 229.8) | 178.9 (169.7 to 239.5) |
| Greedy, new code, 512-token replies | 4K | 194.4 (169.7 to 217.0) | 189.5 (176.9 to 208.8) |
| Own sampler, mixed text, 512-token replies | 4K | 126.7 (115.9 to 131.9) | 130.1 (127.5 to 140.9) |
| Copy the prompt, 512-token replies | 1K | 298.1 (247.3 to 330.5) | 322.3 (305.2 to 356.0) |
| Copy the prompt, 512-token replies | 4K | 296.8 (222.3 to 383.2) | 321.7 (229.0 to 418.0) |
| Copy the prompt, 2,048-token replies | 4K | 292.2 (261.8 to 320.0), run `37a4c93bd874` | 312.4 (277.3 to 342.5) |
| Count from 1, 512-token replies | 1K | 344.7 (336.2 to 344.9) | 370.3 (361.3 to 370.9) |
| Count from 1, 512-token replies | 4K | 335.0 (329.4 to 335.7) | 359.5 (358.8 to 360.6) |

- **Max.** 219.4 tok/s, greedy on new code with replies of up to 2,048 tokens at 1K.
- **Median.** 130.1 tok/s with the model's own sampler on mixed text at 4K.
- **Easy text wrote 7% to 8% faster on 1.3.2.** The counting toy went from 344.7 to 370.3 at 1K, which is 370.3 / 344.7 = 1.07 times. The two ranges do not touch. Finding 7 has four 1.3.0 starts of this build, and they counted 344.2 to 345.6 at 1K and 334.9 to 336.4 at 4K. The 1.3.2 start counted 370.3 and 359.5. Text by text, 1.3.2 was faster on 10 of 10 counting pairs, 10 of 10 short copy pairs and 5 of 5 long copy pairs, with middle ratios of 1.07, 1.08 and 1.07.
- **New code is less clear.** Long replies were faster on 8 of 10 texts with a middle ratio of 1.05. Short replies were faster on 5 of 10 with a middle ratio of 1.00. The ranges overlap in every code cell.
- **The 1.3.2 notes list a change for Flash Next on M5 Macs**, [pull request 3271](https://github.com/ashhart/TensorFold/pull/3271). The author's own measurement is in the release notes.
- **No `mlx-lm` baseline for this model.** `mlx-lm` 0.32.2 did not load the build, as finding 7 shows.
- **8 of the 10 long replies ran to 2,048 tokens.** The other 2 ended at 1,856 and 1,913.
- **Replies checked.** One extra copy request returned 56 lines, all 56 in the prompt word for word. One extra counting request returned 155 lines in order.

## Qwen3.8 Flash Next 6-bit

ELI5: The same model with 6-bit weights, which keep more precision than the 4-bit build and cost some speed.

Decode tok/s at defaults. Run `2bc45b1272e8` on 1.3.0, run `53b6f58b2348` on 1.3.2.

| Test | Prompt | TensorFold 1.3.0 | TensorFold 1.3.2 |
|---|---|---|---|
| Greedy, new code, replies up to 2,048 tokens | 1K | 193.0 (178.5 to 212.3) | 199.8 (187.3 to 211.3) |
| Greedy, new code, replies up to 2,048 tokens | 4K | 191.4 (171.1 to 207.8) | 193.7 (171.8 to 216.7) |
| Greedy, new code, 512-token replies | 1K | 188.2 (177.9 to 192.6) | 183.7 (181.9 to 195.3) |
| Greedy, new code, 512-token replies | 4K | 184.9 (151.6 to 195.6) | 184.9 (153.7 to 212.5) |
| Own sampler, mixed text, 512-token replies | 4K | 117.4 (112.0 to 122.0) | 114.2 (111.2 to 118.5) |
| Copy the prompt, 512-token replies | 1K | 254.4 (208.5 to 276.9) | 261.3 (214.0 to 283.6) |
| Copy the prompt, 512-token replies | 4K | 251.1 (195.8 to 323.1) | 257.9 (200.1 to 333.8) |
| Copy the prompt, 2,048-token replies | 4K | 247.7 (223.1 to 268.9) | 253.9 (233.5 to 276.2) |
| Count from 1, 512-token replies | 1K | 290.0 (283.9 to 290.3) | 297.1 (291.5 to 297.8) |
| Count from 1, 512-token replies | 4K | 283.0 (282.1 to 284.7) | 290.3 (289.8 to 291.7) |

- **Max.** 199.8 tok/s, greedy on new code with replies of up to 2,048 tokens at 1K.
- **Median.** 114.2 tok/s with the model's own sampler on mixed text at 4K. It was 117.4 on 1.3.0, with overlapping ranges.
- **Easy text wrote about 3% faster on this start.** Counting went from 290.0 to 297.1 at 1K, which is 297.1 / 290.0 = 1.02 times, and the two ranges do not touch. Faster on 10 of 10 counting pairs, 10 of 10 short copy pairs and 5 of 5 long copy pairs, each with a middle ratio of 1.03. The second 1.3.2 start repeated it. The build still has one start on 1.3.0.
- **New code is level.** Long replies were faster on 8 of 10 texts with a middle ratio of 1.04. Short replies were faster on 5 of 10 with a middle ratio of 1.00.
- **6-bit against 4-bit on 1.3.2.** 199.8 / 219.4 = 0.91 times at the max and 114.2 / 130.1 = 0.88 times at the median, one start of each build.
- **7 of the 10 long replies ran to 2,048 tokens.** The shortest was 1,628.
- **Replies checked.** One extra copy request returned 56 lines, all 56 in the prompt word for word. One extra counting request returned 155 lines in order.

## Same answers on both releases

ELI5: A faster release is only a fair swap if it writes the same text. I ask 250 short questions greedily on each release and compare the replies by hash.

| Build | Runs compared | Answers that match |
|---|---|---|
| Qwen3.8 27B, 4-bit | `f2d856e22771` and `7458a7a5beb6` | 250 of 250 |
| Qwen3.8 Flash Next, 4-bit | `7bf80be3a997` and `28e2161ebaca` | 250 of 250 |
| Qwen3.8 Flash Next, 6-bit | `2bc45b1272e8` and `53b6f58b2348` | 250 of 250 |

- **Each answer is 64 tokens at most**, on a prompt of about 256 tokens.
- **Time to the first token did not move.** The middle value on the code cells was 0.53 s at 1K on both releases for the 27B, and 2.54 s against 2.57 s at 4K. Flash Next 4-bit read 0.36 s and 0.36 s at 1K, and 1.09 s and 1.10 s at 4K. The 6-bit build read 0.39 s and 1.16 s on both.

## DeepSeek V4.1 Flash is still on 1.3.0

ELI5: TensorFold's DeepSeek server for Macs is not in the Homebrew package. I build it from source. The 1.3.2 tag did not compile on this Mac with the command that built 1.3.0, so my DeepSeek lines stay on 1.3.0 for now.

- **What I ran**, on 21 Nov 2026 at 09:01 SGT.

```bash
git clone --depth 1 --branch v1.3.2 https://github.com/ashhart/TensorFold
zig build dsv41-metal-serve -Dcpu=apple_m1
```

- **Versions.** The clone is at commit `b472b9f8`, the tag's commit. Zig 0.17.0, the version in the repository's `.zig-version`.
- **What the compiler said.** One error, and no binary.

```text
zig/src/families/deepseek_v41/metal/target.zig:279:91: error: expected type 'u32', found 'usize'
```

- **The same command built 1.3.0** on 20 Nov 2026, in 71 s. [Finding 6](../06_dsv41_tensorfold_130_max_push) runs on that build.
- **I did not edit the source.** A patched build would not be release 1.3.2.
- **The 1.3.1 tag builds.** The same command built the server from tag v1.3.1 at `5e1e1912` on 21 Nov 2026 at 12:28 SGT. So the error arrived between 1.3.1 and 1.3.2. I have not run DeepSeek on 1.3.1.
- **Not tried.** The main branch.
- **If I built it wrong**, tell me the right command and I will rerun DeepSeek on 1.3.2.

## The setup

ELI5: One engine at its newest release, three sets of weights, and the serve lines the project documents. Nothing but the release differs from finding 7.

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) 1.3.2, released 21 Nov 2026 03:27 SGT, installed from the project's Homebrew tap. The formula's SHA-256 equals the digest GitHub lists for `tensorfold-1.3.2-macos-arm64.tar.gz`. `tensorfold-native --version` prints 1.3.2.
- **Weights.**
  - [TensorFold/Qwen3.8-27B-MLX-4bit](https://huggingface.co/TensorFold/Qwen3.8-27B-MLX-4bit) with the drafter [z-lab/Qwen3.8-27B-DFlash2](https://huggingface.co/z-lab/Qwen3.8-27B-DFlash2).
  - [TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-4bit-MTP).
  - [TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP](https://huggingface.co/TensorFold/Qwen3.8-Flash-Next-MLX-6bit-MTP).
- **Serve command, 27B.**

```bash
tensorfold serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 262144 --parallel 1 --drafter <DFlash2 folder>
```

- **Serve command, Flash Next**, the M5 Ultra line of `docs/recipes/qwen3.8-flash-next.md`. That file is the same in the 1.3.0 and 1.3.2 tags.

```bash
tensorfold serve <model folder> --name <name> --host 127.0.0.1 --port <port> --context 1048576 --parallel 2 --vision --prompt-cache-gib 8 --temperature 0 --no-update-check
```

- **Thinking** off. Every timed reply was answer text, with 0 reasoning tokens.
- **No switches.** Finding 7 tried four draft settings on the 27B and three on Flash Next on 1.3.0, and none beat the defaults. I did not repeat them on 1.3.2.

| Run id | Build | Engine | Started, SGT, 21 Nov 2026 |
|---|---|---|---|
| `7458a7a5beb6` | Qwen3.8 27B 4-bit | TensorFold 1.3.2, defaults | 09:02 |
| `28e2161ebaca` | Qwen3.8 Flash Next 4-bit | TensorFold 1.3.2, defaults | 09:08 |
| `53b6f58b2348` | Qwen3.8 Flash Next 6-bit | TensorFold 1.3.2, defaults | 09:15 |
| `ab1caacd2961` | Qwen3.8 27B 4-bit | TensorFold 1.3.2, defaults, second start | 12:28 |
| `70284626631f` | Qwen3.8 Flash Next 4-bit | TensorFold 1.3.2, defaults, second start | 12:35 |
| `51735d12713b` | Qwen3.8 Flash Next 6-bit | TensorFold 1.3.2, defaults, second start | 12:42 |

## How I measured

ELI5: Same Mac, same harness, same texts and same three questions as finding 7. Only the release changed.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Requests.** Chat requests through the model's chat template, streamed, one user at a time.
- **Greedy** means temperature 0 with no top-p or top-k sent. **Own sampler** means temperature 0.7, top-p 0.8 and top-k 20.
- **Text.** Code from open-source projects, or a mix of prose and code for the sampled test. The text of a request is picked from its size and repeat number, so both releases got the same texts. Each prompt opens with a new session line so no prompt cache can hit. Timed requests show at most 3 cached tokens on the 27B and 0 on Flash Next, on both releases.
- **Sizes.** "1K" and "4K" are targets at 3.5 characters per token.
- **Same-text pairs.** A pair is one text at one prompt size on 1.3.0 and on 1.3.2. The middle ratio is the median of 1.3.2 over 1.3.0 across the pairs.
- **Repeats.** 5 timed runs per cell. Each block of cells began with one 16-token warm-up request.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last. Tokens in the first piece are not timed.
- **The three questions** are those of [finding 7](../07_qwen38_tensorfold_130), word for word.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Two starts on 1.3.2, one at defaults on 1.3.0.** A gap of a few percent between two starts is not a version change. I call a change only where the new starts sit outside several starts of the older release and every same-text pair agrees. Here that is the easy text on Flash Next 4-bit, upward, and the 27B copy cell at 1K, downward by 3%. The 6-bit gain on easy text repeats on both starts and has one 1.3.0 start behind it.
- **One order only.** The 1.3.0 starts ran on 20 Nov 2026 and at 00:59 SGT on 21 Nov. The 1.3.2 starts ran from 09:02 and from 12:28 SGT on 21 Nov.
- **Max is not what a chat feels like.** The median is the everyday figure.
- **Copy and counting are ceilings.** Drafts guess that text almost every time. Neither is a speed you get when the model writes something new.

## Check it yourself

ELI5: Every timed request is in this folder. You can redo every median.

- **`rows.csv`.** 336 raw rows from the bench database. 300 timed requests and 36 warm-ups.
- **`runs.csv`.** The 6 runs behind them, with engine, version, start time, settings and sampling.
- **The 1.3.0 and `mlx-lm` rows** are in [finding 7](../07_qwen38_tensorfold_130).

From the top of this repository.

```bash
python3 tools/summarize.py findings/11_qwen38_tensorfold_132
```

## What I did not check

- **A second 1.3.0 start at defaults** on any build. The 27B and Flash Next 4-bit have switch starts on 1.3.0, and the 6-bit build has one start.
- **The draft switches of finding 7** on 1.3.2.
- **`mlx-lm` today.** Its rows are from 20 Nov 2026.
- **Answer quality** of any build here.
- **Longer prompts.** These runs stop at 4K.

## Credit

- **Engine.** [TensorFold](https://github.com/ashhart/TensorFold) by [@ashxhart](https://x.com/ashxhart).
- **Weights.** The MLX builds by TensorFold. The DFlash2 drafter by [z-lab](https://huggingface.co/z-lab).
- **Baseline.** [`mlx-lm`](https://github.com/ml-explore/mlx-lm) by Apple's MLX team.
- **Models.** Qwen3.8 27B and Qwen3.8 Flash Next by Qwen.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
