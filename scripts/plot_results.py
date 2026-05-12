#!/usr/bin/env python3
import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

FORMATS_ORDERED = [
    "CSR", "CSR_PREFETCH", "ELLPACK",
    "BCSR2x2", "BCSR4x4", "BCSR4x4_FMA",
    "SELL_C32", "FP32_CSR",
]

COLORS = {
    "CSR":          "tab:blue",
    "CSR_PREFETCH": "tab:cyan",
    "ELLPACK":      "tab:orange",
    "BCSR2x2":      "tab:green",
    "BCSR4x4":      "tab:red",
    "BCSR4x4_FMA":  "tab:purple",
    "SELL_C32":     "tab:brown",
    "FP32_CSR":     "tab:pink",
}

MARKERS = {
    "CSR":          "o",
    "CSR_PREFETCH": "v",
    "ELLPACK":      "s",
    "BCSR2x2":      "^",
    "BCSR4x4":      "D",
    "BCSR4x4_FMA":  "P",
    "SELL_C32":     "X",
    "FP32_CSR":     "*",
}


def read_rows(path):
    rows = []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["nrows"]          = int(row["nrows"])
            row["ncols"]          = int(row["ncols"])
            row["nnz"]            = int(row["nnz"])
            row["threads"]        = int(row["threads"])
            row["time_sec"]       = float(row["time_sec"])
            row["gflops"]         = float(row["gflops"])
            row["bandwidth_gbs"]  = float(row["bandwidth_gbs"])
            row["arith_intensity"]= float(row["arith_intensity"])
            row["stream_peak_gbs"]= float(row["stream_peak_gbs"])
            rows.append(row)
    return rows


def make_roofline(rows, out_path):
    max_stream = max(r["stream_peak_gbs"] for r in rows)
    max_gflops = max(r["gflops"] for r in rows)
    max_threads = max(r["threads"] for r in rows)

    grouped = defaultdict(list)
    for r in rows:
        if r["threads"] == max_threads:
            grouped[r["format"]].append(r)

    plt.figure(figsize=(10, 6))
    for fmt in FORMATS_ORDERED:
        pts = grouped.get(fmt, [])
        if not pts:
            continue
        x = [max(1e-4, p["arith_intensity"]) for p in pts]
        y = [max(1e-4, p["gflops"]) for p in pts]
        plt.scatter(x, y, label=fmt, color=COLORS.get(fmt),
                    marker=MARKERS.get(fmt, "o"), alpha=0.85, s=55)

    intensities = [10 ** (k / 20) for k in range(-40, 21)]
    compute_peak = max_gflops * 1.2
    roof = [min(compute_peak, max_stream * i) for i in intensities]
    plt.plot(intensities, roof, linestyle="--", color="black",
             label="Roofline (STREAM fallback)")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Arithmetic Intensity (FLOP/Byte)")
    plt.ylabel("Performance (GFLOP/s)")
    plt.title(f"Roofline-style SpMV view (threads={max_threads})")
    plt.grid(True, which="both", linestyle=":")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def make_strong_scaling(rows, out_path):
    by_fmt_thread = defaultdict(list)
    for r in rows:
        by_fmt_thread[(r["format"], r["threads"])].append(r["time_sec"])

    threads = sorted({r["threads"] for r in rows})
    baseline = {}
    for fmt in FORMATS_ORDERED:
        vals = by_fmt_thread.get((fmt, 1), [])
        if vals:
            baseline[fmt] = sum(vals) / len(vals)

    plt.figure(figsize=(10, 6))
    for fmt in FORMATS_ORDERED:
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
        plt.plot(threads, speedups, marker="o", label=fmt,
                 color=COLORS.get(fmt), markersize=4)

    ideal = list(threads)
    plt.plot(threads, ideal, linestyle="--", color="black", label="Ideal")
    plt.xlabel("Threads")
    plt.ylabel("Speedup vs 1 thread")
    plt.title("Strong Scaling (average across all matrices)")
    plt.grid(True, linestyle=":")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def make_padding_overhead(rows, out_path):
    """Bar chart: padding overhead of ELLPACK and SELL_C32 relative to CSR.

    Overhead = (bytes_format / bytes_csr) - 1, derived from arith_intensity:
        bytes = 2*nnz / arith_intensity  =>  ratio = csr_AI / fmt_AI - 1
    """
    max_threads = max(r["threads"] for r in rows)
    # collect per-matrix arith_intensity at max threads
    ai = defaultdict(dict)   # ai[matrix][format] = arith_intensity
    for r in rows:
        if r["threads"] == max_threads:
            ai[r["matrix"]][r["format"]] = r["arith_intensity"]

    matrices = sorted(ai.keys())
    ell_overhead  = []
    sell_overhead = []
    labels = []

    for mat in matrices:
        csr_ai  = ai[mat].get("CSR", None)
        ell_ai  = ai[mat].get("ELLPACK", None)
        sell_ai = ai[mat].get("SELL_C32", None)
        if csr_ai and ell_ai and sell_ai and csr_ai > 0:
            labels.append(mat)
            ell_overhead.append((csr_ai / ell_ai - 1) * 100)
            sell_overhead.append((csr_ai / sell_ai - 1) * 100)

    if not labels:
        return

    n = len(labels)
    x = list(range(n))
    w = 0.38

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar([xi - w/2 for xi in x], ell_overhead,  width=w,
           label="ELLPACK", color=COLORS["ELLPACK"],  alpha=0.85)
    ax.bar([xi + w/2 for xi in x], sell_overhead, width=w,
           label="SELL_C32", color=COLORS["SELL_C32"], alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.0f%%"))
    ax.set_ylabel("Padding overhead vs CSR (%)")
    ax.set_title("Memory traffic overhead due to padding\n"
                 "(ELLPACK pads all rows; SELL_C32 pads within 32-row slices)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.legend()
    ax.grid(True, axis="y", linestyle=":")
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def write_summary(rows, out_path):
    max_threads = max(r["threads"] for r in rows)
    by_family_format = defaultdict(list)
    for r in rows:
        if r["threads"] == max_threads:
            by_family_format[(r["family"], r["format"])].append(r["gflops"])

    # padding stats
    ai = defaultdict(dict)
    for r in rows:
        if r["threads"] == max_threads:
            ai[r["matrix"]][r["format"]] = r["arith_intensity"]

    families = sorted({r["family"] for r in rows})

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
            for fmt in FORMATS_ORDERED:
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

        f.write("\n## Padding overhead (ELLPACK vs SELL_C32 vs CSR)\n\n")
        f.write("| Matrix | ELLPACK overhead | SELL_C32 overhead | Reduction |\n")
        f.write("|--------|-----------------|-------------------|----------|\n")
        for mat in sorted(ai.keys()):
            csr_ai  = ai[mat].get("CSR", None)
            ell_ai  = ai[mat].get("ELLPACK", None)
            sell_ai = ai[mat].get("SELL_C32", None)
            if csr_ai and ell_ai and sell_ai and csr_ai > 0:
                ell_oh  = (csr_ai / ell_ai  - 1) * 100
                sell_oh = (csr_ai / sell_ai - 1) * 100
                reduction = ell_oh - sell_oh
                f.write(f"| {mat} | {ell_oh:.1f}% | {sell_oh:.1f}% | {reduction:.1f}pp |\n")

        f.write("\n## Limitations\n\n")
        f.write("- Matrix set is synthetic but structured to mirror proposal families.\n")
        f.write("- Bandwidth roofline uses STREAM-style fallback estimate.\n")
        f.write("- AVX2 gather/scatter costs vary by CPU microarchitecture.\n")
        f.write("- SELL_C32 uses scalar kernel; AVX2 unroll left as future work.\n")
        f.write("- FP32_CSR accuracy bound: max |err| <= 1e-5 vs fp64 reference.\n")


def main():
    in_csv       = os.environ.get("IN_CSV",       "results/benchmark_results.csv")
    out_roofline = os.environ.get("OUT_ROOFLINE",  "results/roofline.png")
    out_scaling  = os.environ.get("OUT_SCALING",   "results/strong_scaling.png")
    out_padding  = os.environ.get("OUT_PADDING",   "results/padding_overhead.png")
    out_summary  = os.environ.get("OUT_SUMMARY",   "results/results_narrative.md")

    rows = read_rows(in_csv)
    make_roofline(rows, out_roofline)
    make_strong_scaling(rows, out_scaling)
    make_padding_overhead(rows, out_padding)
    write_summary(rows, out_summary)
    print(f"Wrote {out_roofline}, {out_scaling}, {out_padding}, {out_summary}")


if __name__ == "__main__":
    main()
