# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..8
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=3.966 GFLOP/s, ELLPACK=4.090 GFLOP/s, BCSR2x2=2.995 GFLOP/s, BCSR4x4=3.022 GFLOP/s (best: ELLPACK)
- block_structured: CSR=2.666 GFLOP/s, ELLPACK=2.404 GFLOP/s, BCSR2x2=2.196 GFLOP/s, BCSR4x4=2.292 GFLOP/s (best: CSR)
- fem_mesh: CSR=3.079 GFLOP/s, ELLPACK=2.847 GFLOP/s, BCSR2x2=2.041 GFLOP/s, BCSR4x4=1.805 GFLOP/s (best: CSR)
- irregular_graph: CSR=3.066 GFLOP/s, ELLPACK=2.161 GFLOP/s, BCSR2x2=1.289 GFLOP/s, BCSR4x4=0.773 GFLOP/s (best: CSR)

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
