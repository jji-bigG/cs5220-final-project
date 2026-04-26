# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..1
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=6.753 GFLOP/s, CSR_PREFETCH=6.169 GFLOP/s, ELLPACK=5.516 GFLOP/s, BCSR2x2=1.778 GFLOP/s, BCSR4x4=1.951 GFLOP/s, BCSR4x4_FMA=1.828 GFLOP/s (best: CSR)
- block_structured: CSR=5.965 GFLOP/s, CSR_PREFETCH=5.772 GFLOP/s, ELLPACK=3.810 GFLOP/s, BCSR2x2=2.243 GFLOP/s, BCSR4x4=3.133 GFLOP/s, BCSR4x4_FMA=2.937 GFLOP/s (best: CSR)
- fem_mesh: CSR=5.458 GFLOP/s, CSR_PREFETCH=5.923 GFLOP/s, ELLPACK=5.352 GFLOP/s, BCSR2x2=1.372 GFLOP/s, BCSR4x4=0.908 GFLOP/s, BCSR4x4_FMA=0.944 GFLOP/s (best: CSR_PREFETCH)
- irregular_graph: CSR=4.009 GFLOP/s, CSR_PREFETCH=3.923 GFLOP/s, ELLPACK=1.247 GFLOP/s, BCSR2x2=0.367 GFLOP/s, BCSR4x4=0.147 GFLOP/s, BCSR4x4_FMA=0.156 GFLOP/s (best: CSR)

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
