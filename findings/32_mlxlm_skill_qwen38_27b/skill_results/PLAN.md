# Plan, Apple M5 Ultra 512 GB, mlx-lm 0.32.2, Qwen3.8-27B 4-bit

By Local LLM L-Plate. Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.

## Question

How close does mlx-lm 0.32.2 at its documented server line sit to this Mac's ceiling for Qwen3.8-27B 4-bit, and does a lever from the skill's list move it?

## Baseline

- The documented line, `mlx_lm.server --model <path>`. `mlx_lm/SERVER.md` at v0.32.2 shows it and recommends no other flag.
- Not a weak default. The bench's fairness rule forbids one.

## Ceiling

- c1 decode with no drafting reads every weight once a token. Measured c1 decode, 43.9 tok/s with no seed and 45.2 with one.
- Weights 14.97 GiB on disk, 16.07 GB.
- Bandwidth at least 1,014.0 GB/s, the median of an MLX matrix-vector kernel reading a 64 GB matrix on this Mac, 18 Nov 2026. A floor, not a device copy.
- 1,014.0 / 16.07 = 63.1 tok/s, so at least that.

## Rule, written before any data

- Each cell's control spread is the 6 same-text ratios of the second control over the first, lowest to highest.
- The candidate's 6 ratios are against the mean of the two controls on the same text.
- A cell moved if at least 5 of the 6 fall outside the control spread on one side. Otherwise it is inside noise.
- `bench.py`'s c1 decode must sit within 15% of the harness's, or the run stops for the cause. Any `bench.py` c1 sample above 63.1 is dropped and printed.

## Levers, in the skill's order

| # | Lever | Status | Evidence |
|---|---|---|---|
| 1 | Startup caches | Nothing to set | mlx-lm 0.32.2 has no such option |
| 2 | Decode graphs | Nothing to set | CUDA only |
| 3 | Draft model | No route | `ArraysCache` is not trimmable, the generate error quoted in the README |
| 3 | Built-in MTP | No route | `qwen3_5.py` `sanitize` drops `mtp.` weights |
| 3 | N-gram drafting | No route | No option in 0.32.2 |
| 4 | Prefix cache | On by default | cached_tokens 2,402 of 2,403 on a repeat |
| 4 | Batching | On by default, no seed only | `_is_batchable`, c8 aggregate 114.5 tok/s |
| 5 | Prefill step 4096 | Not kept | Prompt reading inside a wide control spread at 16K and 64K, decode down about 0.4% |
| 5 | Faster attention, int8 prefill | Nothing to set | No option in 0.32.2 |
| 6 | Kernel tile sizes | Out of scope | Needs code changes |
| 7 | Kernel work | Out of scope | Needs code changes |

## Status

Not a plateau by the skill's rule of three levers inside noise. One lever ran. The others have no switch in mlx-lm 0.32.2 for this model. Levers left, by cost.

1. Other prefill steps, such as 1024 or 8192. Cheap. Unlikely to move decode.
2. A drafting route in a later mlx-lm, a trimmable cache for linear attention, or MTP support for qwen3_5. Not available in 0.32.2.
3. Kernel work on the 4-bit matmul. Dear. Only after the above.

Follow [@LazyLocalLLM on X](https://x.com/LazyLocalLLM) for new benchmarks.
