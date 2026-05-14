# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..2
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=6.756 GFLOP/s, CSR_PREFETCH=5.997 GFLOP/s, ELLPACK=5.786 GFLOP/s, BCSR2x2=2.636 GFLOP/s, BCSR4x4=3.046 GFLOP/s, BCSR4x4_FMA=2.702 GFLOP/s, SELL_C32=4.611 GFLOP/s, FP32_CSR=6.368 GFLOP/s (best: CSR)
- block_structured: CSR=5.357 GFLOP/s, CSR_PREFETCH=4.877 GFLOP/s, ELLPACK=3.694 GFLOP/s, BCSR2x2=2.693 GFLOP/s, BCSR4x4=3.264 GFLOP/s, BCSR4x4_FMA=3.548 GFLOP/s, SELL_C32=4.234 GFLOP/s, FP32_CSR=5.916 GFLOP/s (best: FP32_CSR)
- fem_mesh: CSR=5.499 GFLOP/s, CSR_PREFETCH=5.095 GFLOP/s, ELLPACK=5.112 GFLOP/s, BCSR2x2=1.935 GFLOP/s, BCSR4x4=1.612 GFLOP/s, BCSR4x4_FMA=1.540 GFLOP/s, SELL_C32=4.206 GFLOP/s, FP32_CSR=5.789 GFLOP/s (best: FP32_CSR)
- irregular_graph: CSR=3.602 GFLOP/s, CSR_PREFETCH=4.226 GFLOP/s, ELLPACK=1.915 GFLOP/s, BCSR2x2=0.708 GFLOP/s, BCSR4x4=0.307 GFLOP/s, BCSR4x4_FMA=0.298 GFLOP/s, SELL_C32=2.128 GFLOP/s, FP32_CSR=3.767 GFLOP/s (best: CSR_PREFETCH)

## Padding overhead (ELLPACK vs SELL_C32 vs CSR)

| Matrix | ELLPACK overhead | SELL_C32 overhead | Reduction |
|--------|-----------------|-------------------|----------|
| band_large | 0.0% | 0.0% | 0.0pp |
| band_medium | 0.0% | 0.2% | -0.1pp |
| band_small | 0.0% | 0.0% | 0.0pp |
| block_large | 0.0% | 0.0% | 0.0pp |
| block_medium | 0.0% | 0.0% | 0.0pp |
| block_small | 0.0% | 0.0% | 0.0pp |
| fem_large | 1.5% | 0.6% | 0.9pp |
| fem_medium | 1.8% | 0.8% | 1.0pp |
| fem_small | 2.4% | 1.1% | 1.3pp |
| graph_large | 170.9% | 95.8% | 75.1pp |
| graph_medium | 176.9% | 97.5% | 79.4pp |
| graph_small | 173.2% | 97.5% | 75.7pp |

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
- SELL_C32 uses scalar kernel; AVX2 unroll left as future work.
- FP32_CSR accuracy bound: max |err| <= 1e-5 vs fp64 reference.
