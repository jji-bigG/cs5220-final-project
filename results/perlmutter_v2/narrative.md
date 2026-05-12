# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..256
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=3.413 GFLOP/s, CSR_PREFETCH=3.401 GFLOP/s, ELLPACK=3.386 GFLOP/s, BCSR2x2=3.347 GFLOP/s, BCSR4x4=3.400 GFLOP/s, BCSR4x4_FMA=3.412 GFLOP/s, SELL_C32=3.322 GFLOP/s, FP32_CSR=3.409 GFLOP/s (best: CSR)
- block_structured: CSR=2.016 GFLOP/s, CSR_PREFETCH=2.017 GFLOP/s, ELLPACK=1.930 GFLOP/s, BCSR2x2=2.000 GFLOP/s, BCSR4x4=2.020 GFLOP/s, BCSR4x4_FMA=2.014 GFLOP/s, SELL_C32=2.007 GFLOP/s, FP32_CSR=2.020 GFLOP/s (best: FP32_CSR)
- fem_mesh: CSR=2.112 GFLOP/s, CSR_PREFETCH=2.079 GFLOP/s, ELLPACK=2.096 GFLOP/s, BCSR2x2=2.076 GFLOP/s, BCSR4x4=2.115 GFLOP/s, BCSR4x4_FMA=2.080 GFLOP/s, SELL_C32=2.098 GFLOP/s, FP32_CSR=2.096 GFLOP/s (best: BCSR4x4)
- irregular_graph: CSR=2.072 GFLOP/s, CSR_PREFETCH=2.079 GFLOP/s, ELLPACK=1.968 GFLOP/s, BCSR2x2=1.966 GFLOP/s, BCSR4x4=1.949 GFLOP/s, BCSR4x4_FMA=1.965 GFLOP/s, SELL_C32=2.041 GFLOP/s, FP32_CSR=2.063 GFLOP/s (best: CSR_PREFETCH)

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
| graph_large | 181.5% | 101.3% | 80.2pp |
| graph_medium | 176.7% | 99.4% | 77.3pp |
| graph_small | 175.6% | 97.2% | 78.4pp |

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
- SELL_C32 uses scalar kernel; AVX2 unroll left as future work.
- FP32_CSR accuracy bound: max |err| <= 1e-5 vs fp64 reference.
