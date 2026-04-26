#!/usr/bin/env python3
import csv
import math
import os
from collections import defaultdict

import matplotlib.pyplot as plt


def read_rows(path):
    rows = []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["nrows"] = int(row["nrows"])
            row["ncols"] = int(row["ncols"])
            row["nnz"] = int(row["nnz"])
            row["threads"] = int(row["threads"])
            row["time_sec"] = float(row["time_sec"])
            row["gflops"] = float(row["gflops"])
            row["bandwidth_gbs"] = float(row["bandwidth_gbs"])
            row["arith_intensity"] = float(row["arith_intensity"])
            row["stream_peak_gbs"] = float(row["stream_peak_gbs"])
            rows.append(row)
    return rows


def make_roofline(rows, out_path):
    max_stream = max(r["stream_peak_gbs"] for r in rows)
    max_gflops = max(r["gflops"] for r in rows)

    grouped = defaultdict(list)
    max_threads = max(r["threads"] for r in rows)
    for r in rows:
        if r["threads"] == max_threads:
            grouped[r["format"]].append(r)

    plt.figure(figsize=(9, 6))
    colors = {
        "CSR": "tab:blue", "CSR_PREFETCH": "tab:cyan",
        "ELLPACK": "tab:orange",
        "BCSR2x2": "tab:green",
        "BCSR4x4": "tab:red", "BCSR4x4_FMA": "tab:purple",
    }
    markers = {
        "CSR": "o", "CSR_PREFETCH": "v",
        "ELLPACK": "s",
        "BCSR2x2": "^",
        "BCSR4x4": "D", "BCSR4x4_FMA": "P",
    }

    for fmt, pts in grouped.items():
        x = [max(1e-4, p["arith_intensity"]) for p in pts]
        y = [max(1e-4, p["gflops"]) for p in pts]
        plt.scatter(x, y, label=fmt, color=colors.get(fmt), marker=markers.get(fmt, "o"), alpha=0.8)

    intensities = [10 ** p for p in [x / 20 for x in range(-40, 21)]]
    compute_peak = max_gflops * 1.2
    roof = [min(compute_peak, max_stream * i) for i in intensities]
    plt.plot(intensities, roof, linestyle="--", color="black", label="Roofline (STREAM fallback)")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Arithmetic Intensity (FLOP/Byte)")
    plt.ylabel("Performance (GFLOP/s)")
    plt.title(f"Roofline-style SpMV view (threads={max_threads})")
    plt.grid(True, which="both", linestyle=":")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def make_strong_scaling(rows, out_path):
    by_fmt_thread = defaultdict(list)
    for r in rows:
        by_fmt_thread[(r["format"], r["threads"])].append(r["time_sec"])

    fmts = sorted({r["format"] for r in rows})
    threads = sorted({r["threads"] for r in rows})
    baseline = {}
    for fmt in fmts:
        vals = by_fmt_thread.get((fmt, 1), [])
        if vals:
            baseline[fmt] = sum(vals) / len(vals)

    plt.figure(figsize=(9, 6))
    for fmt in fmts:
        if fmt not in baseline:
            continue
        speedups = []
        for th in threads:
            vals = by_fmt_thread.get((fmt, th), [])
            if not vals:
                speedups.append(float("nan"))
                continue
            t_avg = sum(vals) / len(vals)
            speedups.append(baseline[fmt] / t_avg if t_avg > 0 else float("nan"))
        plt.plot(threads, speedups, marker="o", label=fmt)

    ideal = [t for t in threads]
    plt.plot(threads, ideal, linestyle="--", color="black", label="Ideal")
    plt.xlabel("Threads")
    plt.ylabel("Speedup vs 1 thread")
    plt.title("Strong Scaling (average across all selected matrices)")
    plt.grid(True, linestyle=":")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def write_summary(rows, out_path):
    max_threads = max(r["threads"] for r in rows)
    by_family_format = defaultdict(list)
    for r in rows:
        if r["threads"] == max_threads:
            by_family_format[(r["family"], r["format"])].append(r["gflops"])

    families = sorted({r["family"] for r in rows})
    formats = ["CSR", "CSR_PREFETCH", "ELLPACK", "BCSR2x2", "BCSR4x4", "BCSR4x4_FMA"]

    with open(out_path, "w") as f:
        f.write("# SpMV Results Narrative\n\n")
        f.write(f"- Dataset count: {len(set(r['matrix'] for r in rows))}\n")
        f.write(f"- Thread sweep: 1..{max_threads}\n")
        f.write(f"- Timing protocol: 5 warm-up + 20 timed runs (median per point)\n\n")
        f.write("## Per-family behavior at max thread count\n\n")
        for fam in families:
            best_fmt = None
            best_val = -1.0
            f.write(f"- {fam}: ")
            parts = []
            for fmt in formats:
                vals = by_family_format.get((fam, fmt), [])
                if not vals:
                    continue
                avg = sum(vals) / len(vals)
                parts.append(f"{fmt}={avg:.3f} GFLOP/s")
                if avg > best_val:
                    best_val = avg
                    best_fmt = fmt
            f.write(", ".join(parts))
            if best_fmt:
                f.write(f" (best: {best_fmt})")
            f.write("\n")
        f.write("\n## Limitations\n\n")
        f.write("- Matrix set is synthetic but structured to mirror proposal families.\n")
        f.write("- Bandwidth roofline uses STREAM-style fallback estimate.\n")
        f.write("- AVX2 gather/scatter costs vary by CPU microarchitecture.\n")


def main():
    in_csv = os.environ.get("IN_CSV", "results/benchmark_results.csv")
    out_roofline = os.environ.get("OUT_ROOFLINE", "results/roofline.png")
    out_scaling = os.environ.get("OUT_SCALING", "results/strong_scaling.png")
    out_summary = os.environ.get("OUT_SUMMARY", "results/results_narrative.md")

    rows = read_rows(in_csv)
    make_roofline(rows, out_roofline)
    make_strong_scaling(rows, out_scaling)
    write_summary(rows, out_summary)
    print(f"Wrote {out_roofline}, {out_scaling}, {out_summary}")


if __name__ == "__main__":
    main()
