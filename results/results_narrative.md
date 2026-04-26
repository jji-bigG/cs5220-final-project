# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..128
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=4.936 GFLOP/s, CSR_PREFETCH=4.927 GFLOP/s, ELLPACK=4.606 GFLOP/s, BCSR2x2=4.668 GFLOP/s, BCSR4x4=4.904 GFLOP/s, BCSR4x4_FMA=4.893 GFLOP/s (best: CSR)
- block_structured: CSR=3.105 GFLOP/s, CSR_PREFETCH=3.120 GFLOP/s, ELLPACK=2.954 GFLOP/s, BCSR2x2=3.078 GFLOP/s, BCSR4x4=3.103 GFLOP/s, BCSR4x4_FMA=3.050 GFLOP/s (best: CSR_PREFETCH)
- fem_mesh: CSR=3.691 GFLOP/s, CSR_PREFETCH=3.687 GFLOP/s, ELLPACK=3.570 GFLOP/s, BCSR2x2=3.481 GFLOP/s, BCSR4x4=3.545 GFLOP/s, BCSR4x4_FMA=3.594 GFLOP/s (best: CSR)
- irregular_graph: CSR=2.932 GFLOP/s, CSR_PREFETCH=2.908 GFLOP/s, ELLPACK=2.600 GFLOP/s, BCSR2x2=2.506 GFLOP/s, BCSR4x4=2.515 GFLOP/s, BCSR4x4_FMA=2.602 GFLOP/s (best: CSR)

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
