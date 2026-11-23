# Apple M5 Ultra 512 GB, mlx-lm 0.32.2, Qwen3.8-27B 4-bit

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

Results in this skill's format, for its authors to take if they wish. The full report and every raw row are one folder up, in [finding 32](../README.md).

**mlx-lm 0.32.2 at its documented server line decoded Qwen3.8-27B 4-bit at 43.9 tok/s for one user with no seed, at most 70% of a 63.1 tok/s ceiling, and 45.2 with a seed. No config lever that mlx-lm 0.32.2 offers on this model raised it. With no seed, 8 users together reached 114.5 tok/s, every token over wall time.**

| Item | Value |
|---|---|
| Machine | Mac Studio, Apple M5 Ultra, 80-core GPU, 512 GB unified memory, macOS 27.2 |
| Engine | mlx-lm 0.32.2, mlx 0.32.4 |
| Model | mlx-community/Qwen3.8-27B-4bit, 14.97 GiB |
| Launch | `mlx_lm.server --model <path> --host 127.0.0.1 --port <port>` |
| c1 decode, no seed | 43.9 tok/s, median of 6, 1K prompt, 512-token replies, greedy, thinking off |
| c1 decode, with a seed | 45.2 tok/s, the same cell, mlx-lm's unbatched path |
| Ceiling, c1, no drafting | at least 63.1 tok/s, 1,014.0 GB/s (MLX kernel read, a floor) over 16.07 GB |
| Share of ceiling | at most 70% with no seed, 72% with one |
| c8 aggregate | 114.5 tok/s, every token over wall time, prompt reading included, no seed, 2K prompts, 512-token replies, median of 5 rounds |
| Prefix cache | on by default, 2,402 of 2,403 tokens reused on a repeat |
| bench.py c1 decode | 44.2 tok/s, 6 samples 43.9 to 44.3, none dropped, no seed, within 0.7% of the harness's seedless cell |

## Levers

- **Speculative decoding.** No route on this model and version. A draft model needs a trimmable cache, and the linear-attention layers use `ArraysCache`. `mlx_lm.generate --draft-model` stopped with "Speculative decoding requires a trimmable prompt cache (got {'ArraysCache'})". mlx-lm drops the checkpoint's `mtp.` weights on load. No n-gram option.
- **Prefill step 4096 against 2048.** No change this test could see in prompt reading at 16K and 64K, where the two controls alone differed by up to 2 times and 16%. Decode fell about 0.4%, on 6 of 6 pairs. Not kept.
- **Batching.** On by default, up to 32 requests, but only for requests with no seed and no quantized KV cache.
- **Startup caches, decode graphs, kernel tuning.** Nothing to set in mlx-lm 0.32.2.

## Method

- Control, candidate, control, each a separate server start, 6 timed runs a cell, same texts in the same order.
- Speed from a separate harness. `bench.py` at fda968e7fc ran once against a control start as a cross-check, with temperature 0 and the harness's thinking-off switch.
- Not used from the pinned commit. `queue.sh`, which needs `flock`, and `mem.sh`, which needs docker and `/proc`. The bench's own lock and memory probe stood in.

## Gotchas found

- **A seed turns mlx-lm's batching off.** A benchmark that sends a seed measures one user at a time. With seeds, 2 to 16 users stayed at about 40 tok/s in total on the same build. For one user the seeded path decoded 3% faster.
- **`/v1/models` can come back empty.** If `~/.cache/huggingface/hub` does not exist, mlx-lm 0.32.2 sends a 200 header, then fails with `CacheNotFound`. `bench.py`'s health check then reports "server not reachable". Setting `HF_HUB_CACHE` to an empty folder fixes it.
- **Prompt reading at 16K is noisy.** The first token came 9.6 to 24.3 s after the request within one start.

See [PLAN.md](PLAN.md) for the plan, the rule and the levers with no switch, and [ledger.json](ledger.json) for one record per lever, which the skill keeps one a line as `ledger.jsonl`.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
