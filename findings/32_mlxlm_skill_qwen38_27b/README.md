# Finding 32. mlx-lm 0.32.2 on Qwen3.8-27B 4-bit, the inference-optimisation skill's levers

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

ELI5: The [inference-optimisation skill](https://github.com/sybil-solutions/inference-optimisation-skill) is a method for making a model server faster. Work out the ceiling, change one thing at a time, and check each change against a control before and after. I ran it on `mlx-lm`, Apple's own reference server and this bench's baseline, with Qwen3.8-27B 4-bit on an M5 Ultra 512 GB. I used my own harness for the numbers, and the skill's script once as a cross-check.

**`mlx-lm` 0.32.2, run as its docs show, decoded Qwen3.8-27B 4-bit at 43.9 tok/s for one user sending no seed, as most clients do, at most 70% of this Mac's ceiling. With a seed, which keeps it on its unbatched path, it decoded 45.2. None of the skill's levers that `mlx-lm` 0.32.2 offers on this model raised either. It has no drafting route here, and the one lever I could run, a larger prefill step, showed no change this test could see. Its prompt cache works by default. With no seed, 8 users together got 114.5 tok/s in all. Mac Studio M5 Ultra 512 GB, median of 6 runs, 23 Nov 2026.**

| Setting | One user, decode tok/s | 8 users, all tokens over wall time, tok/s |
|---|---|---|
| `mlx_lm.server --model <path>`, as documented, no seed | 43.9 | 114.5 |
| The same, with the harness's seed | 45.2 | not batched |
| Prefill step 4096, with the seed | 45.1 | not run |
| Ceiling for one user, no drafting | at least 63.1 | |

- **One user** is the middle of 6 greedy runs, mixed text, 1K prompt, 512-token replies, thinking off. With no seed, run `0b37204c96ff`, 43.9. With the harness's seed, the three control starts read 45.2, 45.2 and 45.3.
- **Why the seed matters.** `mlx-lm` 0.32.2 serves a request that sends a seed on its own, outside its batching (`server.py`, `_is_batchable`). Alone, that path decoded 3% faster for one user. The lever test ran with the seed on all three of its starts, so its pairs compare like with like.
- **8 users together** is the middle of 5 rounds of the load test, 8 users starting at once with fresh 2K prompts and 512-token replies, every token over the round's wall time, prompt reading included, no seed sent. It is a different measure from one user's decode speed, so I set no ratio between them.
- **The ceiling.** One user decoding with no drafting reads every weight once a token. The weights are 14.97 GiB on disk, which is 16.07 GB. This Mac's GPU read memory at a median 1,014.0 GB/s in an MLX kernel test on 18 Nov 2026, a floor on its bandwidth. 1,014.0 / 16.07 = 63.1 tok/s, so the ceiling is at least that.
- **The arithmetic.** 43.9 / 63.1 = 0.70, so at most 70%. With the seed, 45.2 / 63.1 = 0.72.

## Chart

ELI5: One user sits well under the ceiling and no lever moved it. Several users at once get far more done in total. The one-user bars are decode speed and the user bars are every token over wall time, so the two kinds do not compare bar to bar.

![Bars in tokens per second for mlx-lm 0.32.2 on Qwen3.8-27B 4-bit. Ceiling for one user, at least 63.1. One user decoding with no seed, 43.9. One user with a seed, 45.2. With a seed and prefill step 4096, 45.1. All tokens over wall time with no seed, two users 67.7, four users 99.4, eight users 114.5.](chart_skill.png)

## The levers, in the skill's order

ELI5: The skill lists levers from cheapest to dearest. Most of them are switches `mlx-lm` 0.32.2 does not have for this model, or has on already.

1. **Startup caches.** `mlx-lm` has no setting for them.
2. **Decode graphs.** A CUDA feature. Nothing to set on a Mac.
3. **Speculative decoding. No route on this model.**
   - **A draft model.** `mlx-lm` needs a prompt cache it can trim, and Qwen3.8's linear-attention layers use `ArraysCache`, which it cannot (`mlx_lm/models/cache.py`). `mlx_lm.generate` with the model as its own draft stopped with "Speculative decoding requires a trimmable prompt cache (got {'ArraysCache'})". That check ran offline with `mlx_lm.generate`, not the server.
   - **The model's own MTP layers.** `mlx-lm` drops the `mtp.` weights when it loads this model (`qwen3_5.py`, `sanitize`).
   - **N-gram drafting.** `mlx-lm` 0.32.2 has none.
4. **Concurrency and the prompt cache.** Both on by default.
   - **Prompt cache.** The same 2,403-token prompt sent twice reused 2,402 tokens the second time, and the reply came back in 0.08 s instead of 1.50 s.
   - **Batching.** `mlx-lm` decodes up to 32 requests together by default, but only requests with no seed and no quantized cache (`_is_batchable` in `server.py`). See the users section.
5. **Prefill step size.** `--prefill-step-size 4096` against the default 2048. No change this test could see. See below.
6. **Kernel tile sizes and kernel work.** Out of reach without changing `mlx-lm`'s code.

The skill also lists faster attention libraries and int8 prefill. `mlx-lm` 0.32.2 has no switch for either.

## The prefill step

ELI5: The prefill step is how many prompt tokens the server reads in one go. Bigger steps can read long prompts faster. Here they did not.

Starts in the order control, candidate, control, 6 runs a cell.

| Cell | Control `a68c93d2eb17` | Step 4096 `069de0c18f4d` | Control `c84c4aa4c153` |
|---|---|---|---|
| Decode, 1K, tok/s | 45.2 | 45.1 | 45.2 |
| Prompt reading, 16K, tok/s | 1,584.5 | 1,409.6 | 1,329.5 |
| Prompt reading, 64K, tok/s | 1,251.6 | 1,301.8 | 1,350.6 |

- **The rule, written before any data.** Each cell's control spread is the 6 same-text ratios of the second control over the first. The candidate's 6 ratios are against the mean of the two controls. A cell moved if 5 of the 6 fall outside the control spread on the same side.
- **Prompt reading, inside noise at both sizes.** At 16K the two controls alone differed from 0.62 to 2.00 times text by text, and at 64K from 0.93 to 1.16. So this test could not see a change in prompt reading smaller than that. The first token of a 16K prompt came 9.6 to 24.3 s after the request in all three starts.
- **Decode, a small cost.** The step-4096 start was slower on 6 of 6 pairs, ratios 0.994 to 0.997, below a control spread of 0.997 to 1.001. So by the rule decode moved down, by about 0.4%.
- **So the lever gave nothing this test could see,** and cost a little decode. I did not keep it.

## Users together

ELI5: `mlx-lm` can decode several requests in one pass, which gets more done in total while each user waits a little longer. It only does that for requests that send no seed.

The load test, run `65e056974d16`, its own start, no seed sent. Middle of 5 rounds.

| Users | All users together, tok/s | Each user's writing speed, tok/s | First token, s |
|---|---|---|---|
| 1 | 26.8 | 42.9 | 7.2 |
| 2 | 67.7 | 40.8 | 2.6 |
| 4 | 99.4 | 33.6 | 5.4 |
| 8 | 114.5 | 20.7 | 11.0 |

- **The one-user total counts the prompt reading, and it slowed after two rounds.** In rounds 1 and 2 a fresh 2K prompt waited 1.2 and 1.3 s for its first token and the total read 39.1 and 38.8. In rounds 3 to 5 it waited 7.2 to 7.4 s, and the total read 26.6 to 26.8. Decoding held at 42.8 to 43.0 throughout. At that point the server's log shows its prompt cache holding 10 sequences in 15.4 GB, and about 7 s passed before it began reading the new prompt. I did not find the cause.
- **A seed turns batching off.** `mlx-lm` 0.32.2 serves a request with a seed on its own (`server.py`, `_is_batchable`). This bench's harness sends a seed by default. An older run, not in this folder, shows what that does. On 12 Nov 2026 the same version and build, with seeds and the same load test (2K prompts, 512-token replies, thinking off), averaged 40.2 tok/s with one user and 40.2, 38.6, 40.2 and 40.2 with 2, 4, 8 and 16 users together (run `2369a14d013e`). So a seeded test of `mlx-lm` measures one user at a time.

## The skill's own script

ELI5: The skill ships a benchmark script, `bench.py`. I ran it once against a control start, set as close to the harness as it allows, to check that the two agree.

- **Agreement.** `bench.py` read one-user decode at 44.2 tok/s, the middle of 6 samples from 43.9 to 44.3. It sends no seed. The harness's seedless cell read 43.9, 0.7% lower, on its own start. On the same start as `bench.py`, run `fea7c505b9a0`, the harness with its seed read 45.3.
- **Its prompt reading.** 1,678.3 tok/s over 2,799 tokens and 1,663.9 over 21,533.
- **Settings.** Temperature 0, the harness's thinking-off switch, the model path as the model name, one user. Its own short prompts and 512-token replies.
- **No sample was dropped.** The plan was to drop any one-user sample above 63.1, since the pinned script can count broken output as speed (open PR #9 on its repository). None was above.
- **It needed one change to start.** `bench.py` checks that `/v1/models` lists a model. On this Mac `mlx-lm` 0.32.2 sent a 200 header for that request and then failed with `CacheNotFound`, since `~/.cache/huggingface/hub` does not exist here, so the body was empty. For that start only, `HF_HUB_CACHE` pointed at a new empty folder. The model loads from its local path, so nothing else read that folder.
- **The pinned copy.** `sybil-solutions/inference-optimisation-skill` at commit fda968e7fc, all 15 files checked by SHA-256. `bench.py` SHA-256 starts acca9912. The skill is not installed here. It is a method I read, and its script ran once from a fresh folder.

## In the skill's own format

ELI5: The skill's repository collects results from other machines. This folder holds this run in its format, for its authors to take if they wish.

- [`skill_results/README.md`](skill_results/README.md), the summary.
- [`skill_results/PLAN.md`](skill_results/PLAN.md), the plan, the lever tried and the levers with no switch.
- [`skill_results/ledger.json`](skill_results/ledger.json), `bench.py`'s own record and one record a lever from the harness. The skill keeps these one a line in `ledger.jsonl`, a file type this repository does not publish.

## The setup

ELI5: `mlx-lm`'s own server, started the way its docs show.

- **Engine.** [mlx-lm](https://github.com/ml-explore/mlx-lm) 0.32.2, the newest release when I ran this, checked on 23 Nov 2026 at 16:21 SGT, with mlx 0.32.4.
- **Server.** `mlx_lm.server --model <path> --host 127.0.0.1 --port <port>`. Its docs (`mlx_lm/SERVER.md` at v0.32.2) show `mlx_lm.server --model <path_to_model_or_hf_repo>` and recommend no other flag.
- **Weights.** [mlx-community/Qwen3.8-27B-4bit](https://huggingface.co/mlx-community/Qwen3.8-27B-4bit), 14.97 GiB, every file checked against its SHA-256.
- **Requests.** Chat requests, streamed, with `enable_thinking` false in the chat template.

| Run id | Start | Started, SGT, 23 Nov 2026 |
|---|---|---|
| `a68c93d2eb17` | Control C1 | 16:24 |
| `069de0c18f4d` | Prefill step 4096 | 16:34 |
| `c84c4aa4c153` | Control C2 | 16:43 |
| `fea7c505b9a0` | Control C3, with `bench.py` | 16:54 |
| `65e056974d16` | Control C4, users, no seed | 16:58 |
| `0b37204c96ff` | Control C5, one user, no seed | 17:19 |

## How I measured

ELI5: Same Mac and same harness as every other page here.

- **Machine.** Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB, macOS 27.2, low power mode off.
- **Greedy** means temperature 0.
- **Text.** A mix of prose and code. Each prompt opens with a new session line, so no prompt cache can hit.
- **Repeats.** 6 timed runs per one-user cell, the number the skill asks for. 5 rounds per user count.
- **Writing speed** is tokens per second from the first streamed piece of the reply to the last. On the first control block the streamed pieces matched the server's token count within 5 tokens on every reply.

## Things to know before you compare

- **One model, one engine.** The skill's own results table has other machines and engines.
- **The ceiling is a floor.** A device-copy test might show more bandwidth, and the embedding table is looked up, not read in full. Either would raise the ceiling and lower the 70%.
- **Seed or no seed.** Most benchmarks and clients send no seed. This bench's harness sends one unless told not to.

## Check it yourself

ELI5: Every timed request is in this folder.

- **`rows.csv`.** 74 raw rows of the five speed starts.
- **`runs.csv`.** Those 5 runs.
- **`rows_users.csv` and `runs_users.csv`.** The 26 rows and the run of the users start.

From the top of this repository.

```bash
python3 tools/summarize.py findings/32_mlxlm_skill_qwen38_27b
```

## What I did not verify

- **Other prefill steps.** I tried 4096 only.
- **A quantized KV cache.** Not on the skill's list, and it turns batching off.
- **Long contexts past 64K, answer quality and needles.**
- **The replies to the skill's announcement on X.** Reading them needs a sign-in.

## Credit

- **Engine.** [mlx-lm](https://github.com/ml-explore/mlx-lm) by Apple's MLX team.
- **Method.** The [inference-optimisation skill](https://github.com/sybil-solutions/inference-optimisation-skill) by [@0xSero](https://x.com/0xSero).
- **Model.** Qwen3.8-27B by Qwen, converted by [mlx-community](https://huggingface.co/mlx-community).

If a setting here is wrong, open an issue and I will rerun it.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
