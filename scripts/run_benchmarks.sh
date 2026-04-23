#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

WARMUP="${WARMUP:-5}"
TIMED="${TIMED:-20}"
MIN_THREADS="${MIN_THREADS:-1}"
MAX_THREADS="${MAX_THREADS:-32}"
USE_AVX2="${USE_AVX2:-1}"
OUT_CSV="${OUT_CSV:-results/benchmark_results.csv}"

mkdir -p results
make all

ARGS=(
  "--warmup" "${WARMUP}"
  "--timed" "${TIMED}"
  "--min-threads" "${MIN_THREADS}"
  "--max-threads" "${MAX_THREADS}"
  "--output" "${OUT_CSV}"
)

if [[ "${USE_AVX2}" == "0" ]]; then
  ARGS+=("--no-avx2")
fi

echo "Running SpMV benchmark with ${MIN_THREADS}..${MAX_THREADS} threads"
./bin/spmv_bench "${ARGS[@]}"
echo "Results written to ${OUT_CSV}"
