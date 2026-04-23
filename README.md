# SpMV Final Project

This repository implements and benchmarks Sparse Matrix-Vector Multiplication (SpMV) formats:

- CSR (baseline)
- ELLPACK
- BCSR 2x2
- BCSR 4x4

The benchmark includes OpenMP parallelization, optional AVX2 paths, correctness checks against a dense reference, a fixed 12-matrix selection across 4 structural families, and scripts to generate roofline/scaling plots.

## Build

```bash
make all
```

## Run benchmark (proposal protocol defaults)

```bash
./scripts/run_benchmarks.sh
```

Defaults:

- warm-up runs: 5
- timed runs: 20
- thread sweep: 1..32
- output CSV: `results/benchmark_results.csv`

Optional environment overrides:

```bash
WARMUP=3 TIMED=10 MAX_THREADS=16 ./scripts/run_benchmarks.sh
```

## Generate figures and narrative

```bash
python3 scripts/plot_results.py
```

This generates:

- `results/roofline.png`
- `results/strong_scaling.png`
- `results/results_narrative.md`

## Matrix selection

Selection criteria and locked matrix list are in `docs/matrix_selection.md`.
