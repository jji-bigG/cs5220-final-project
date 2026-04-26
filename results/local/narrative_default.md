# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..14
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=2.960 GFLOP/s, ELLPACK=2.827 GFLOP/s, BCSR2x2=2.561 GFLOP/s, BCSR4x4=2.712 GFLOP/s (best: CSR)
- block_structured: CSR=1.822 GFLOP/s, ELLPACK=1.742 GFLOP/s, BCSR2x2=1.751 GFLOP/s, BCSR4x4=1.758 GFLOP/s (best: CSR)
- fem_mesh: CSR=1.888 GFLOP/s, ELLPACK=1.913 GFLOP/s, BCSR2x2=1.702 GFLOP/s, BCSR4x4=1.577 GFLOP/s (best: ELLPACK)
- irregular_graph: CSR=1.969 GFLOP/s, ELLPACK=1.616 GFLOP/s, BCSR2x2=1.194 GFLOP/s, BCSR4x4=0.708 GFLOP/s (best: CSR)

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
