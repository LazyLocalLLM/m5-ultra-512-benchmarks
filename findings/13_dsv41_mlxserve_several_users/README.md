# Finding 13. DeepSeek V4.1 Flash with 1 to 8 users on one Mac, mlx-serve 26.11.3

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: Every finding before this one times one user. Here I asked what happens when 2, 4 or 8 people ask at once. I borrowed the test from a public write-up of two Mac Studios joined by cable, so that one Mac with 512 GB can be read against it. The questions are short and open, and the model thinks at its highest effort. With several users the engine's drafts hardly land, so those rows are close to plain decoding. With one user it kept about one drafted token a round.

**One Mac Studio M5 Ultra 512 GB wrote 55.5 to 57.4 tok/s for one user on DeepSeek V4.1 Flash at full precision, on stock mlx-serve 26.11.3. With 8 users at once it wrote 115.0 to 116.2 tok/s in total, which is about 15 tok/s each. Short open questions, 768-token replies, reasoning effort max, temperature 0. Every reply was reasoning text. Four passes over two server starts, 21 Nov 2026.**

**Added on 22 Nov 2026 at 02:40 SGT. On a 3-bit pack, the one I take the write-up to have run on its one Studio, the same Mac and the same stock engine wrote 61.1 to 69.8 tok/s for one user and 139.8 to 140.9 in total with 8 users. That is about 1.2 times the full-precision pack at every user count. The section "The 3-bit pack" has it.**

| Users at once | All users together, tok/s | Each user, tok/s | First token, s |
|---|---|---|---|
| 1 | 55.5 (54.5 to 56.2) | 56.4 (55.5 to 57.4) | 0.26 |
| 2 | 74.1 (72.3 to 74.4) | 38.1 (37.0 to 40.6) | 0.37 |
| 4 | 97.0 (96.4 to 98.0) | 25.0 (24.5 to 30.6) | 0.69 |
| 8 | 115.7 (115.0 to 116.2) | 15.0 (14.5 to 16.7) | 1.18 |

- **All users together** is the reply tokens of every stream over the wall time, from the start to the last stream's end. The figure is the middle of the 4 passes, with the lowest and highest pass in brackets.
- **Each user** is one stream's own speed, from its first streamed piece to its last. The figure is the middle of every stream at that count, with the slowest and fastest stream in brackets.
- **First token** is the middle of every stream at that count. At 8 users the slowest stream waited 2.32 s.
- **This is not a median of 5 like my other findings.** It is 4 passes. With one user, every pass asked the same first question of the eight.

## Chart

ELI5: Grey is what the Mac writes in total. Blue is what each person gets.

![Paired horizontal bars of writing speed in tokens per second for DeepSeek V4.1 Flash on mlx-serve 26.11.3 on one Mac. With 1 user, 55.5 in total and 56.4 each. With 2 users, 74.1 and 38.1. With 4 users, 97.0 and 25.0. With 8 users, 115.7 and 15.0.](chart_users.png)

## What more users cost and buy

ELI5: The Mac can serve several people in one pass over the model. The total goes up and each person's share goes down.

- **Eight users got 2.1 times the total of one.** 115.7 / 55.5 = 2.08 times.
- **Each of the eight got about a quarter of a lone user's speed.** 15.0 / 56.4 = 0.27 times.
- **Two users got 1.3 times the total.** 74.1 / 55.5 = 1.34 times, at 38.1 each.
- **The passes agree.** At every count the four totals sit within 4% of each other.
- **Memory.** The server process held 99.2 GiB after load and 99.6 GiB at the end, by `ps`. The context was 65,536 tokens with 16 slots.

## The 3-bit pack

ELI5: The write-up I took the test from ran a smaller, 3-bit pack on its one Studio, because the full-precision pack does not fit in 256 GB. So I ran that same pack here, to set one Mac beside one Mac on the same weights.

Tok/s on mlx-serve 26.11.3, four passes over two server starts, 22 Nov 2026 from 02:29 SGT. The full-precision columns are the table at the top of this page.

| Users at once | 3-bit pack, all users together | Full precision, all users together | 3-bit over full | 3-bit pack, each user | First token, s |
|---|---|---|---|---|---|
| 1 | 65.1 (61.1 to 69.8) | 55.5 (54.5 to 56.2) | 1.17 | 66.3 (62.0 to 71.1) | 0.21 |
| 2 | 87.7 (86.8 to 88.4) | 74.1 (72.3 to 74.4) | 1.18 | 45.1 (44.5 to 45.7) | 0.32 |
| 4 | 117.4 (116.3 to 117.7) | 97.0 (96.4 to 98.0) | 1.21 | 30.3 (29.8 to 37.9) | 0.55 |
| 8 | 140.1 (139.8 to 140.9) | 115.7 (115.0 to 116.2) | 1.21 | 18.2 (17.7 to 19.8) | 1.02 |

- **The 3-bit pack wrote about 1.2 times the full-precision pack.** 65.1 / 55.5 = 1.17, 87.7 / 74.1 = 1.18, 117.4 / 97.0 = 1.21 and 140.1 / 115.7 = 1.21.
- **Eight users got 2.2 times the total of one.** 140.1 / 65.1 = 2.15 times, at 18.2 tok/s each.
- **One user moved between the two starts.** The first start wrote 69.8 and 67.2 and the second 61.1 and 63.1, on the same question. With two or more users the four passes sit within 2% of each other.
- **Still reasoning text.** Every stream wrote 768 tokens and the server counted all 768 as reasoning. No request failed, 60 streams in all.
- **Drafts with one user.** The four one-user requests kept 0.72 to 0.95 drafted tokens a round. The log's plain step on them was 16.38 to 16.43 ms, and 1000 / 16.41 = 60.9 tok/s with no drafts.
- **Drafts with several users.** Over the 56 requests that ran beside others, the middle value kept was 0.06 a round and the highest 0.41.
- **Memory.** The server process held 83.6 GiB after load and 83.8 GiB at the end, by `ps`, against 99.2 and 99.6 on the full-precision pack.
- **The pack.** [ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-iQ-MLX-3.0bpw](https://huggingface.co/ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-iQ-MLX-3.0bpw) @ 6da9c4e4, the mlx-serve author's pack at 3.0 bits a weight, 46 files and 397.9 GiB on disk. Every file was verified against the pinned commit.
- **Same server, same flags, same questions as above.** The log again reads "lm head requantized to 8-bit".
- **Speed is all I measured.** I did not measure what 3 bits cost in answer quality.
- **Which pack the write-up ran.** Its notes call the one-Studio pack "3.0bpw" and give no link. I took it to be this pack, the mlx-serve author's public pack of that name.
- **How this sits beside the write-up.** Its one-Studio figures are in the how-to linked under "The test". I do not repeat them here. Mine came out lower at 1, 2 and 4 users, by less than on the full-precision pack.
- **The build is not the same.** The write-up's [lab notes](https://github.com/daflood/mlx-serve/blob/dsv41-two-macs/two-macs/REPORT.md) say its one-Studio figures ran "the PR build", a build of [pull request 1146](https://github.com/ddalcu/mlx-serve/pull/1146) on mlx-serve. That pull request was open and not merged when I checked on 22 Nov 2026 at 02:44 SGT. I ran the stock release. I do not publish runs on code that is not merged.

## Why this is lower than my code figures

ELI5: mlx-serve drafts a few tokens ahead and checks them. When the drafts are right the speed jumps. On this text they were right less often than on code, and with several users almost never.

- **Correction, 22 Nov 2026 02:44 SGT.** This section said one user here is plain decoding, and worked that out from a 17.70 ms step in the server's log. Both were wrong. The 0.06 to 0.08 was a middle value over all 30 requests of a start, and 28 of those ran beside other users. The 17.70 ms shows on 46 of the 56 several-user requests and on none of the one-user ones, so I now read it as a starting value and not a measured step. The lines below are split by user count.
- **[Finding 8](../08_dsv41_mlxserve_26113) has the same engine and the same weights at 84.0 to 95.3 tok/s.** That is greedy on new code with thinking off, one user.
- **With one user the drafts did land, less than on code.** The four one-user requests kept 0.75 to 1.11 drafted tokens a round. On finding 8's first start the server kept 1.27.
- **The log's plain step on those four requests was 19.54 to 19.71 ms.** 1000 / 19.585 = 51.1 tok/s with no drafts. The four wrote 55.5 to 57.4, so the drafts added about 10%. 56.4 / 51.1 = 1.10.
- **With several users the drafts hardly landed.** Over the 56 requests that ran beside others, the middle value kept was 0.06 a round and the highest 0.39.
- **Two things differ from finding 8 at once**, the questions and the thinking. I did not separate them.

## The test

ELI5: The requests are not mine. They come from a public benchmark of this model on two Mac Studios, so that anyone can line up the two.

- **Where the test is from.** A [post on r/MacStudio](https://www.reddit.com/r/MacStudio/s/gcFkKGbfUq) of 21 Nov 2026 and its [how-to](https://github.com/daflood/mlx-serve/blob/dsv41-two-macs/TWO-MACS.md). The figures for one and two 256 GB Studios are there. I do not repeat them here.
- **What I took.** The several-users suite of the script `two-macs/scripts/rw_bench.py` in that branch. Its eight questions, 768-token replies, `reasoning_effort` of `max`, temperature 0, streamed. I read the script and sent the same requests with my own client.
- **How a pass runs.** The streams start together. Stream 1 asks question 1, stream 2 asks question 2, and so on. Each prompt opens with a tag that names the pass, so no prompt cache can hit. Every request shows 0 cached tokens.
- **The questions** are short and open, about a CPU's memory system, replication protocols, a bakery's oven, a star's life, a job scheduler's API, stagflation, TLS 1.3 and a rail trip. The prompts came to 77 to 93 tokens.
- **What is not the same as the post.** In the first table, the pack. Mine is the full-precision Lossless pack below. The post ran a 3-bit pack on one Studio and a different 4-bit pack on two. The section "The 3-bit pack" runs the post's 3-bit pack. One machine here, and no patches.

## The setup

ELI5: One engine at its newest release, at its defaults, with the context and slot count of the how-to.

- **Engine.** [mlx-serve](https://github.com/ddalcu/mlx-serve) 26.11.3, the newest release on 21 Nov 2026, installed from the project's Homebrew formula.
- **Weights.** [ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless](https://huggingface.co/ddalcu/DeepSeek-V4.1-Flash-1017-MLX-Serve-Lossless), the mlx-serve author's pack at the precision DeepSeek ships, 4-bit experts and an 8-bit trunk.
- **Serve command.**

```bash
mlx-serve --model <model folder> --serve --host 127.0.0.1 --port <port> --ctx-size 65536 --max-concurrent 16 --warmup-full
```

- **What the log says about the start.** "batched decode on". "PLD speculative decoding: ENABLED". "DSpark 3 stages". "lm head requantized to 8-bit (MLX_SERVE_DSV41_HEAD8=0 keeps it dense)". So this is not a bit-exact run, as in finding 8.
- **Two starts.** Run `462a77fa2dc4` from 12:52 SGT with passes a and b, and run `9013484edbf3` from 12:58 SGT with passes c and d.
- **Two more starts for the 3-bit pack**, on 22 Nov 2026. Run `94a3eff454f1` from 02:29 SGT with passes a and b, and run `bb8559370dc5` from 02:33 SGT with passes c and d. mlx-serve 26.11.3 was still the newest release when I checked at 01:37 SGT.

## How I measured

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **One stream's speed** is its reply tokens minus one, over the time from its first streamed piece to its last. That is the script's own formula.
- **The total** is the reply tokens of all streams over the wall time of the pass.
- **Reply tokens** are the server's count in the stream's usage block. Every stream wrote 768 tokens, and the server counted all 768 as reasoning tokens.
- **No request failed.** 60 streams on each pack.

## Things to know before you compare

ELI5: A speed is only comparable with another speed measured the same way.

- **Reasoning text.** Nothing here is an answer speed.
- **One user is one question.** The other seven questions were asked only when several users ran.
- **Drafted speed depends on the text.** The same engine and weights wrote 84.0 to 95.3 on code. Neither figure is the model's one speed.
- **A different pack reads differently.** I have run two. The 3-bit pack wrote about 1.2 times the full-precision one.

## Check it yourself

ELI5: Every stream is in this folder. Open `rows.csv` on GitHub and it shows as a table you can search.

- **`rows.csv`.** 120 lines, one per stream, 60 for each pack. The run, the pass, the number of users, the stream, the question number, its own speed, the pass total, the wall time, the first token time and the token counts.
- **`runs.csv`.** The four server starts, with the version, the weights, the flags and what the log said.
- **No script.** The requests are those of the script linked above. `tools/summarize.py` does not read this folder.

## What I did not verify

- **The post's 4-bit pack on this Mac.** It is 477 GiB and I have not fetched it.
- **The write-up's build.** Its one-Studio column ran an open pull request's build, which I did not build or run.
- **That the 3-bit pack here is the write-up's pack.** The name matches. The notes give no link.
- **Answer quality of the 3-bit pack.**
- **Any other engine on this test.**
- **The same questions with thinking off**, or with the model's own sampler.
- **Long prompts with several users**, and more than 8 users.
- **What the replies say.** I kept the counts and not the text.
- **Peak memory during a pass.**

## Credit

- **The test.** u/runlocalmodels on r/MacStudio, and the `daflood/mlx-serve` branch `dsv41-two-macs`.
- **Engine and weights.** [mlx-serve](https://github.com/ddalcu/mlx-serve), the Lossless pack and the 3-bit pack by ddalcu.
- **Model.** DeepSeek V4.1 Flash by DeepSeek.

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
