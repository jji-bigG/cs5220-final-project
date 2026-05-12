#!/bin/bash
#SBATCH --job-name=spmv_bench_v2
#SBATCH --account=m4776          # update to your account if different
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --time=01:30:00
#SBATCH --output=results/perlmutter_v2/slurm_%j.out
#SBATCH --error=results/perlmutter_v2/slurm_%j.err

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

mkdir -p results/perlmutter_v2

# ── build ──────────────────────────────────────────────────────────────────
module load gcc/12 || true
make all

echo "Binary built: $(./bin/spmv_bench --help 2>&1 | head -1 || echo ok)"

# ── STREAM bandwidth estimate (informational) ──────────────────────────────
echo "Hardware threads available: $(nproc)"

# ── full sweep: all 8 formats, 1..128 threads ─────────────────────────────
OUT_CSV="results/perlmutter_v2/benchmark_v2.csv"
MAX_T=$(nproc)

echo "Starting benchmark sweep: 1..${MAX_T} threads, 5 warmup, 20 timed"
./bin/spmv_bench \
    --warmup 5 \
    --timed  20 \
    --min-threads 1 \
    --max-threads "${MAX_T}" \
    --output "${OUT_CSV}"
echo "Benchmark done: ${OUT_CSV}"

# ── plots ──────────────────────────────────────────────────────────────────
IN_CSV="${OUT_CSV}" \
OUT_ROOFLINE="results/perlmutter_v2/roofline.png" \
OUT_SCALING="results/perlmutter_v2/strong_scaling.png" \
OUT_PADDING="results/perlmutter_v2/padding_overhead.png" \
OUT_SUMMARY="results/perlmutter_v2/narrative.md" \
    python3 scripts/plot_results.py

echo "All done. Results in results/perlmutter_v2/"
