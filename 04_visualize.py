"""Generate publication-quality charts for the Bihar revenue analysis.

Produces six PNGs in outputs/charts/:
  1_total_revenue_ranking.png
  2_sotr_per_capita.png
  3_sotr_composition.png
  4_bihar_components_timeseries.png
  5_cagr_heatmap.png
  6_opportunity_gaps.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

MASTER = Path("data/master_revenue.csv")
OUTDIR = Path("outputs/charts")
OUTDIR.mkdir(parents=True, exist_ok=True)

LATEST = 2023
PEERS = ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan", "Odisha",
         "Jharkhand", "West Bengal"]
TOP_PERFORMERS = ["Maharashtra", "Karnataka", "Gujarat"]

# 2011 Census; AP/Telangana post-2014 bifurcation figures.
POP = {
    "Andhra Pradesh": 49_577_103, "Arunachal Pradesh": 1_383_727,
    "Assam": 31_205_576, "Bihar": 104_099_452, "Chhattisgarh": 25_545_198,
    "Goa": 1_458_545, "Gujarat": 60_439_692, "Haryana": 25_351_462,
    "Himachal Pradesh": 6_864_602, "Jharkhand": 32_988_134,
    "Karnataka": 61_095_297, "Kerala": 33_406_061,
    "Madhya Pradesh": 72_626_809, "Maharashtra": 112_374_333,
    "Manipur": 2_855_794, "Meghalaya": 2_966_889, "Mizoram": 1_097_206,
    "Nagaland": 1_978_502, "Odisha": 41_974_218, "Punjab": 27_743_338,
    "Rajasthan": 68_548_437, "Sikkim": 610_577, "Tamil Nadu": 72_147_030,
    "Telangana": 35_193_978, "Tripura": 3_673_917,
    "Uttar Pradesh": 199_812_341, "Uttarakhand": 10_086_292,
    "West Bengal": 91_276_115,
}

SOTR_SUBS = ["SGST", "Sales/Trade Tax", "Stamps & Registration",
             "State Excise", "Motor Vehicle Tax"]

# Consistent palette
C_BIHAR = "#C8102E"           # strong red
C_PEER = "#1F77B4"            # blue
C_TOP = "#2CA02C"             # green
C_OTHER = "#B8B8B8"           # light grey
C_BIHAR_DARK = "#8B0A1F"
SOURCE = "Source: Financial Data of State Governments (Ministry of Finance, GoI). Population: Census 2011."

# Style
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})


def add_source(fig: plt.Figure, extra: str = "",
               bottom: float = 0.22) -> None:
    """Place source note below the axes, reserving figure bottom space so
    rotated x-tick labels don't overlap it."""
    note = SOURCE + (f"  |  {extra}" if extra else "")
    fig.subplots_adjust(bottom=bottom)
    fig.text(0.5, 0.02, note, ha="center", fontsize=8,
             style="italic", color="#555")


def state_color(state: str) -> str:
    if state == "Bihar":
        return C_BIHAR
    if state in PEERS:
        return C_PEER
    if state in TOP_PERFORMERS:
        return C_TOP
    return C_OTHER


def load() -> pd.DataFrame:
    return pd.read_csv(MASTER)


def wide_for(df: pd.DataFrame, year: int) -> pd.DataFrame:
    w = (df[df["year"] == year]
         .pivot_table(index="state", columns="metric",
                      values="value", aggfunc="first"))
    w["population"] = w.index.map(POP)
    return w


# ---------------------------------------------------------------------------
# 1. Bar chart: Total Revenue Receipts, all states, sorted desc
# ---------------------------------------------------------------------------

def chart_total_revenue_ranking(wide: pd.DataFrame) -> None:
    s = wide["Total Revenue Receipts"].dropna().sort_values(ascending=False)
    colors = [state_color(st) for st in s.index]

    fig, ax = plt.subplots(figsize=(13, 8))
    bars = ax.bar(s.index, s.values, color=colors, edgecolor="white",
                  linewidth=0.5)

    # Annotate Bihar's bar
    bihar_idx = list(s.index).index("Bihar")
    bihar_rank = bihar_idx + 1
    bihar_bar = bars[bihar_idx]
    ax.annotate(f"Bihar\n#{bihar_rank} of {len(s)}",
                xy=(bihar_bar.get_x() + bihar_bar.get_width() / 2,
                    bihar_bar.get_height()),
                xytext=(0, 12), textcoords="offset points",
                ha="center", fontsize=10, fontweight="bold",
                color=C_BIHAR_DARK)

    ax.set_title("Total Revenue Receipts by State, FY 2023-24",
                 loc="left", pad=12)
    ax.set_ylabel("₹ Crore")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=75)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x / 1000:.0f}K"))

    # Legend
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=C_BIHAR, label="Bihar"),
        plt.Rectangle((0, 0), 1, 1, color=C_PEER, label="Peer group"),
        plt.Rectangle((0, 0), 1, 1, color=C_TOP, label="Top performers"),
        plt.Rectangle((0, 0), 1, 1, color=C_OTHER, label="Other states"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", frameon=False,
              fontsize=9)
    add_source(fig, bottom=0.28)
    fig.savefig(OUTDIR / "1_total_revenue_ranking.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Bar chart: SOTR per capita, major states (pop > 5M)
# ---------------------------------------------------------------------------

def chart_sotr_per_capita(wide: pd.DataFrame) -> None:
    sotr = wide["SOTR"].dropna()
    pc = (sotr * 1e7 / wide.loc[sotr.index, "population"])
    pc = pc[wide.loc[pc.index, "population"] > 5_000_000]
    pc = pc.sort_values(ascending=False)
    colors = [state_color(st) for st in pc.index]

    fig, ax = plt.subplots(figsize=(13, 8))
    bars = ax.bar(pc.index, pc.values, color=colors, edgecolor="white",
                  linewidth=0.5)

    median = pc.median()
    ax.axhline(median, ls="--", color="#555", linewidth=0.8, alpha=0.6)
    ax.text(len(pc) - 0.3, median * 1.03, f"Median: ₹{median:,.0f}",
            ha="right", fontsize=9, color="#555")

    bihar_idx = list(pc.index).index("Bihar")
    bihar_val = pc.iloc[bihar_idx]
    ax.annotate(f"Bihar\n₹{bihar_val:,.0f}",
                xy=(bars[bihar_idx].get_x() + bars[bihar_idx].get_width() / 2,
                    bihar_val),
                xytext=(0, 14), textcoords="offset points",
                ha="center", fontsize=10, fontweight="bold",
                color=C_BIHAR_DARK)

    ax.set_title("State Own Tax Revenue per Capita — Major States (pop > 5M), "
                 "FY 2023-24", loc="left", pad=12)
    ax.set_ylabel("₹ per person")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=70)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=C_BIHAR, label="Bihar"),
        plt.Rectangle((0, 0), 1, 1, color=C_PEER, label="Peer group"),
        plt.Rectangle((0, 0), 1, 1, color=C_TOP, label="Top performers"),
        plt.Rectangle((0, 0), 1, 1, color=C_OTHER, label="Other"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", frameon=False)
    add_source(fig, "Per-capita = state SOTR ÷ 2011 population.", bottom=0.26)
    fig.savefig(OUTDIR / "2_sotr_per_capita.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Stacked bar: SOTR composition — Bihar vs Peer Avg vs Top Avg
# ---------------------------------------------------------------------------

def chart_sotr_composition(wide: pd.DataFrame) -> None:
    def shares(rows: pd.DataFrame) -> pd.Series:
        total = rows[SOTR_SUBS].sum(axis=1)
        return (rows[SOTR_SUBS].div(total, axis=0) * 100).mean()

    comp = pd.DataFrame({
        "Bihar": shares(wide.loc[["Bihar"]]),
        "Peer\naverage": shares(wide.loc[PEERS]),
        "Top\nperformers\naverage": shares(wide.loc[TOP_PERFORMERS]),
    }).T

    # Reorder columns so the biggest components sit at the bottom
    comp = comp[SOTR_SUBS]

    sub_colors = {
        "SGST": "#4C72B0",
        "Sales/Trade Tax": "#DD8452",
        "Stamps & Registration": "#55A868",
        "State Excise": "#C44E52",
        "Motor Vehicle Tax": "#8172B3",
    }

    fig, ax = plt.subplots(figsize=(9, 6.5))
    bottom = np.zeros(len(comp))
    for sub in SOTR_SUBS:
        vals = comp[sub].values
        ax.bar(comp.index, vals, bottom=bottom, label=sub,
               color=sub_colors[sub], edgecolor="white", linewidth=0.8,
               width=0.55)
        for i, v in enumerate(vals):
            if v >= 3:  # avoid crowding for tiny slices
                ax.text(i, bottom[i] + v / 2, f"{v:.0f}%",
                        ha="center", va="center", fontsize=9,
                        color="white", fontweight="bold")
        bottom += vals

    # Highlight Bihar label in red
    xticklabels = ax.get_xticklabels()
    for lbl in xticklabels:
        if lbl.get_text() == "Bihar":
            lbl.set_color(C_BIHAR_DARK)
            lbl.set_fontweight("bold")

    ax.set_title("SOTR Composition: Bihar vs Peers vs Top Performers, FY 2023-24",
                 loc="left", pad=12)
    ax.set_ylabel("% of total SOTR")
    ax.set_ylim(0, 105)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False,
              title="Component")
    add_source(fig, f"Peers: {', '.join(PEERS)}.  "
                    f"Top performers: {', '.join(TOP_PERFORMERS)}.",
               bottom=0.14)
    fig.savefig(OUTDIR / "3_sotr_composition.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Line chart: Bihar's SOTR components over time
# ---------------------------------------------------------------------------

def chart_bihar_components_timeseries(df: pd.DataFrame) -> None:
    bihar = df[(df["state"] == "Bihar") & (df["metric"].isin(SOTR_SUBS))]
    ts = bihar.pivot(index="year", columns="metric", values="value")
    ts = ts.sort_index()

    fig, ax = plt.subplots(figsize=(13, 7))

    palette = {
        "SGST": "#4C72B0",
        "Sales/Trade Tax": "#DD8452",
        "Stamps & Registration": "#55A868",
        "State Excise": "#C44E52",
        "Motor Vehicle Tax": "#8172B3",
    }
    for sub in SOTR_SUBS:
        if sub not in ts.columns:
            continue
        series = ts[sub]
        ax.plot(series.index, series.values, marker="o", linewidth=2.2,
                color=palette[sub], markersize=5)
        # Label each line at its right-hand endpoint (replaces legend).
        last_x = series.index.max()
        last_y = series.loc[last_x]
        ax.annotate(f" {sub}", xy=(last_x, last_y),
                    xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=10, color=palette[sub],
                    fontweight="bold")

    # Set ylim before placing text annotations so coordinates are stable.
    ymax = ts.max().max() * 1.08
    ax.set_ylim(0, ymax)

    # Mark GST introduction (central).
    ax.axvline(2017, ls=":", color="#555", alpha=0.7)
    ax.text(2017, ymax * 0.98, " GST introduced\n (Jul 2017)",
            fontsize=8.5, color="#444", va="top", ha="left")

    # Mark prohibition — place lower so it doesn't collide with GST label.
    ax.axvline(2016, ls=":", color=C_BIHAR, alpha=0.55)
    ax.text(2016, ymax * 0.62, " Bihar prohibition\n (Apr 2016)",
            fontsize=8.5, color=C_BIHAR_DARK, va="top", ha="left")

    ax.set_title("Bihar: SOTR Sub-components over Time, FY 2014-15 to 2023-24",
                 loc="left", pad=12)
    ax.set_xlabel("Fiscal year (start)")
    ax.set_ylabel("₹ Crore")
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_xticks(ts.index)
    ax.set_xlim(ts.index.min() - 0.3, ts.index.max() + 2.2)
    add_source(fig, bottom=0.12)
    fig.savefig(OUTDIR / "4_bihar_components_timeseries.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Heatmap: CAGR of each SOTR component × state
# ---------------------------------------------------------------------------

def chart_cagr_heatmap(df: pd.DataFrame) -> None:
    # Use 2017 → 2023 (6 years). This is the GST-era window where SGST is
    # defined for everyone; other components are also fully populated.
    start, end = 2017, 2023
    span = end - start

    pivot_start = (df[df["year"] == start]
                   .pivot_table(index="state", columns="metric",
                                values="value", aggfunc="first"))
    pivot_end = (df[df["year"] == end]
                 .pivot_table(index="state", columns="metric",
                              values="value", aggfunc="first"))

    cagr = pd.DataFrame(index=pivot_start.index, columns=SOTR_SUBS, dtype=float)
    for sub in SOTR_SUBS:
        s = pivot_start.get(sub)
        e = pivot_end.get(sub)
        if s is None or e is None:
            continue
        ratio = e / s.where(s > 0)
        cagr[sub] = (ratio ** (1 / span) - 1) * 100

    # Sort states by population (descending) so big states are at top
    ordered = sorted(cagr.index, key=lambda s: -POP.get(s, 0))
    cagr = cagr.loc[ordered]

    fig, ax = plt.subplots(figsize=(9, 11))
    # Cap extreme values for color scaling (Bihar State Excise is ~-60%)
    vmax = 40
    vmin = -40
    sns.heatmap(
        cagr.astype(float), annot=True, fmt=".1f", cmap="RdYlGn",
        center=0, vmin=vmin, vmax=vmax, linewidths=0.4,
        linecolor="white", cbar_kws={"label": "CAGR (%)"}, ax=ax,
        annot_kws={"fontsize": 8},
    )

    # Bold + recolor Bihar's row label
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == "Bihar":
            lbl.set_color(C_BIHAR_DARK)
            lbl.set_fontweight("bold")

    ax.set_title(f"CAGR of SOTR Components by State, FY {start}–{end} ({span} years)",
                 loc="left", pad=12)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    add_source(fig, "NaN cells = start value was 0 (e.g., Bihar State Excise "
                    "after prohibition).", bottom=0.13)
    fig.savefig(OUTDIR / "5_cagr_heatmap.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Horizontal bar: opportunity gaps
# ---------------------------------------------------------------------------

def chart_opportunity_gaps(wide: pd.DataFrame) -> None:
    bihar_pop = POP["Bihar"]
    components = SOTR_SUBS + ["Non-Tax Revenue", "Grants in Aid"]

    rows = []
    for metric in components:
        if metric not in wide.columns:
            continue
        bihar_val = wide.loc["Bihar", metric]
        peer_pc = (wide.loc[PEERS, metric] * 1e7
                   / wide.loc[PEERS, "population"]).mean()
        hypothetical = peer_pc * bihar_pop / 1e7
        gap = hypothetical - bihar_val
        rows.append({"metric": metric, "bihar": bihar_val,
                     "hypothetical": hypothetical, "gap": gap})
    gaps = pd.DataFrame(rows).sort_values("gap", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    bar_color = [
        C_BIHAR if g < 0 else "#5B8FB9" for g in gaps["gap"]
    ]
    ax.barh(gaps["metric"], gaps["gap"], color=bar_color, edgecolor="white")

    # Annotate each bar with ₹ Crore
    for i, (_, row) in enumerate(gaps.iterrows()):
        g = row["gap"]
        x = g + (max(gaps["gap"]) * 0.01 if g >= 0 else min(gaps["gap"]) * 0.01)
        ax.text(x, i, f"₹{g:+,.0f} Cr", va="center",
                ha="left" if g >= 0 else "right",
                fontsize=9, color="#333")

    ax.axvline(0, color="#333", linewidth=0.8)
    ax.set_title("Bihar's Revenue Gap: Additional ₹ Crore if Bihar Matched Peer "
                 "Per-Capita Collection",
                 loc="left", pad=12)
    ax.set_xlabel("₹ Crore gap (positive = Bihar under-collecting vs peers)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    add_source(fig, f"Peer group: {', '.join(PEERS)}.  "
                    "State Excise gap reflects Bihar's prohibition policy.",
               bottom=0.14)
    fig.savefig(OUTDIR / "6_opportunity_gaps.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    df = load()
    wide = wide_for(df, LATEST)

    chart_total_revenue_ranking(wide)
    chart_sotr_per_capita(wide)
    chart_sotr_composition(wide)
    chart_bihar_components_timeseries(df)
    chart_cagr_heatmap(df)
    chart_opportunity_gaps(wide)

    for p in sorted(OUTDIR.glob("*.png")):
        print(f"  {p}  ({p.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
