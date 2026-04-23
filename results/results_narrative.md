# SpMV Results Narrative

- Dataset count: 12
- Thread sweep: 1..14
- Timing protocol: 5 warm-up + 20 timed runs (median per point)

## Per-family behavior at max thread count

- banded_pde: CSR=2.923 GFLOP/s, ELLPACK=2.953 GFLOP/s, BCSR2x2=2.484 GFLOP/s, BCSR4x4=2.547 GFLOP/s (best: ELLPACK)
- block_structured: CSR=1.817 GFLOP/s, ELLPACK=1.775 GFLOP/s, BCSR2x2=1.722 GFLOP/s, BCSR4x4=1.719 GFLOP/s (best: CSR)
- fem_mesh: CSR=1.931 GFLOP/s, ELLPACK=2.021 GFLOP/s, BCSR2x2=1.662 GFLOP/s, BCSR4x4=1.556 GFLOP/s (best: ELLPACK)
- irregular_graph: CSR=1.898 GFLOP/s, ELLPACK=1.641 GFLOP/s, BCSR2x2=1.158 GFLOP/s, BCSR4x4=0.699 GFLOP/s (best: CSR)

## Limitations

- Matrix set is synthetic but structured to mirror proposal families.
- Bandwidth roofline uses STREAM-style fallback estimate.
- AVX2 gather/scatter costs vary by CPU microarchitecture.
