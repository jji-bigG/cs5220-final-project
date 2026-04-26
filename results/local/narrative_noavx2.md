# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..14
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=2.974 GFLOP/s, ELLPACK=3.006 GFLOP/s, BCSR2x2=2.543 GFLOP/s, BCSR4x4=2.591 GFLOP/s (best: ELLPACK)
- block_structured: CSR=1.907 GFLOP/s, ELLPACK=1.746 GFLOP/s, BCSR2x2=1.698 GFLOP/s, BCSR4x4=1.684 GFLOP/s (best: CSR)
- fem_mesh: CSR=1.959 GFLOP/s, ELLPACK=1.960 GFLOP/s, BCSR2x2=1.719 GFLOP/s, BCSR4x4=1.510 GFLOP/s (best: ELLPACK)
- irregular_graph: CSR=1.972 GFLOP/s, ELLPACK=1.740 GFLOP/s, BCSR2x2=1.179 GFLOP/s, BCSR4x4=0.683 GFLOP/s (best: CSR)

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
