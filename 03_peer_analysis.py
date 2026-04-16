"""Peer analysis for Bihar's revenue performance.

Compares Bihar to all states (rankings) and to a peer group (UP, MP,
Rajasthan, Odisha, Jharkhand, West Bengal) on revenue mix, absolute and
per-capita gaps, and 10-year CAGR.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

MASTER = Path("data/master_revenue.csv")
OUT = Path("outputs/peer_analysis.csv")

LATEST_YEAR = 2023   # fiscal year 2023-24
BASE_YEAR = 2013     # fiscal year 2013-14

PEER_STATES = ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan",
               "Odisha", "Jharkhand", "West Bengal"]

# Population (2011 Census of India; Andhra Pradesh and Telangana use
# post-2014 bifurcation figures consistent with census 2011 totals).
# Source: https://censusindia.gov.in/2011census/PCA/PCA_Highlights/pca_highlights_file/India/Chapter-1.pdf
POPULATION_2011 = {
    "Andhra Pradesh": 49_577_103,
    "Arunachal Pradesh": 1_383_727,
    "Assam": 31_205_576,
    "Bihar": 104_099_452,
    "Chhattisgarh": 25_545_198,
    "Goa": 1_458_545,
    "Gujarat": 60_439_692,
    "Haryana": 25_351_462,
    "Himachal Pradesh": 6_864_602,
    "Jharkhand": 32_988_134,
    "Karnataka": 61_095_297,
    "Kerala": 33_406_061,
    "Madhya Pradesh": 72_626_809,
    "Maharashtra": 112_374_333,
    "Manipur": 2_855_794,
    "Meghalaya": 2_966_889,
    "Mizoram": 1_097_206,
    "Nagaland": 1_978_502,
    "Odisha": 41_974_218,
    "Punjab": 27_743_338,
    "Rajasthan": 68_548_437,
    "Sikkim": 610_577,
    "Tamil Nadu": 72_147_030,
    "Telangana": 35_193_978,
    "Tripura": 3_673_917,
    "Uttar Pradesh": 199_812_341,
    "Uttarakhand": 10_086_292,
    "West Bengal": 91_276_115,
}

SOTR_SUBCOMPONENTS = ["SGST", "Sales/Trade Tax", "Stamps & Registration",
                      "State Excise", "Motor Vehicle Tax"]
CORE_METRICS = ["Total Revenue Receipts", "SOTR", "Share in Union Taxes",
                "Grants in Aid", "Non-Tax Revenue"]


def load_master() -> pd.DataFrame:
    df = pd.read_csv(MASTER)
    df["population_2011"] = df["state"].map(POPULATION_2011)
    assert df["population_2011"].notna().all(), "missing population for some state"
    return df


def wide_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Pivot to one row per state, one column per metric, for a given year."""
    sub = df[df["year"] == year]
    wide = sub.pivot_table(index="state", columns="metric",
                           values="value", aggfunc="first")
    wide["population_2011"] = wide.index.map(POPULATION_2011)
    return wide


def rank_table(wide: pd.DataFrame) -> pd.DataFrame:
    """Absolute and per-capita rank of each state on each metric (2023-24)."""
    metrics = [m for m in CORE_METRICS + SOTR_SUBCOMPONENTS if m in wide.columns]
    rows = []
    for metric in metrics:
        values = wide[metric].dropna()
        # Per-capita in rupees per person (value is in ₹ Crore = 1e7 ₹).
        pc = (values * 1e7) / wide.loc[values.index, "population_2011"]
        abs_rank = values.rank(ascending=False, method="min").astype(int)
        pc_rank = pc.rank(ascending=False, method="min").astype(int)
        for state in values.index:
            rows.append({
                "state": state,
                "metric": metric,
                "value_crore": values[state],
                "per_capita_rupees": pc[state],
                "rank_absolute": abs_rank[state],
                "rank_per_capita": pc_rank[state],
            })
    return pd.DataFrame(rows)


def cagr(start: float, end: float, years: int) -> float:
    """Compound annual growth rate. Returns NaN if start is <= 0 or missing."""
    if start is None or end is None or np.isnan(start) or np.isnan(end):
        return np.nan
    if start <= 0:
        return np.nan
    return (end / start) ** (1 / years) - 1


def compute_cagr_table(df: pd.DataFrame) -> pd.DataFrame:
    """CAGR for Bihar vs national aggregate per metric."""
    rows = []
    for metric in CORE_METRICS + SOTR_SUBCOMPONENTS:
        sub = df[df["metric"] == metric]
        if sub.empty:
            continue
        years_avail = sorted(sub["year"].unique())
        start_year = years_avail[0]
        end_year = years_avail[-1]
        span = end_year - start_year
        if span < 1:
            continue

        # Bihar
        bihar = sub[sub["state"] == "Bihar"]
        b_start = bihar.loc[bihar["year"] == start_year, "value"].sum()
        b_end = bihar.loc[bihar["year"] == end_year, "value"].sum()

        # National aggregate (sum across states)
        nat_start = sub.loc[sub["year"] == start_year, "value"].sum()
        nat_end = sub.loc[sub["year"] == end_year, "value"].sum()

        rows.append({
            "metric": metric,
            "span_years": span,
            "start_year": start_year,
            "end_year": end_year,
            "bihar_start_crore": b_start,
            "bihar_end_crore": b_end,
            "bihar_cagr": cagr(b_start, b_end, span),
            "national_start_crore": nat_start,
            "national_end_crore": nat_end,
            "national_cagr": cagr(nat_start, nat_end, span),
        })
    return pd.DataFrame(rows)


def compute_peer_gap(wide: pd.DataFrame) -> pd.DataFrame:
    """For each SOTR sub-component and core metric, compare Bihar to peer avg
    on absolute, per-capita, and population-scaled hypothetical."""
    metrics = [m for m in CORE_METRICS + SOTR_SUBCOMPONENTS if m in wide.columns]
    bihar_pop = POPULATION_2011["Bihar"]
    rows = []
    for metric in metrics:
        bihar_val = wide.loc["Bihar", metric]
        peer_vals = wide.loc[PEER_STATES, metric].dropna()
        peer_pops = wide.loc[peer_vals.index, "population_2011"]
        peer_avg = peer_vals.mean()
        # Per-capita (rupees/person): value in crore → × 1e7 → ÷ population.
        bihar_pc = bihar_val * 1e7 / bihar_pop
        peer_pc = (peer_vals * 1e7 / peer_pops).mean()
        # Hypothetical: what would Bihar collect if its per-capita = peer avg
        # per-capita? (Expressed in ₹ Crore.)
        hypothetical = peer_pc * bihar_pop / 1e7
        rows.append({
            "metric": metric,
            "bihar_crore": bihar_val,
            "peer_avg_crore": peer_avg,
            "gap_absolute_crore": peer_avg - bihar_val,
            "bihar_per_capita_rupees": bihar_pc,
            "peer_avg_per_capita_rupees": peer_pc,
            "gap_per_capita_rupees": peer_pc - bihar_pc,
            "hypothetical_bihar_crore": hypothetical,
            "opportunity_crore": hypothetical - bihar_val,
        })
    return pd.DataFrame(rows)


def compute_revenue_mix(wide: pd.DataFrame) -> pd.DataFrame:
    """Share of each SOTR sub-component in total SOTR, Bihar vs peer avg."""
    def shares(state_rows: pd.DataFrame) -> pd.Series:
        total = state_rows[SOTR_SUBCOMPONENTS].sum(axis=1)
        return (state_rows[SOTR_SUBCOMPONENTS].div(total, axis=0) * 100).mean()

    bihar_share = shares(wide.loc[["Bihar"]])
    peer_share = shares(wide.loc[PEER_STATES])

    mix = pd.DataFrame({
        "sub_component": SOTR_SUBCOMPONENTS,
        "bihar_pct_of_sotr": bihar_share.values,
        "peer_avg_pct_of_sotr": peer_share.values,
        "difference_pp": (bihar_share - peer_share).values,
    })
    return mix


def main() -> None:
    df = load_master()
    wide = wide_year(df, LATEST_YEAR)

    ranks = rank_table(wide)
    cagr_tab = compute_cagr_table(df)
    peer_gap = compute_peer_gap(wide)
    mix = compute_revenue_mix(wide)

    # ---- Print section: Rankings ---------------------------------------
    print("=" * 80)
    print(f"BIHAR RANKINGS (among 28 states, FY {LATEST_YEAR}-{LATEST_YEAR + 1 - 2000:02d})")
    print("=" * 80)
    bihar_ranks = ranks[ranks["state"] == "Bihar"].set_index("metric")
    print(bihar_ranks[["value_crore", "rank_absolute",
                       "per_capita_rupees", "rank_per_capita"]]
          .to_string(float_format=lambda x: f"{x:,.2f}"))

    # ---- Print section: Revenue mix vs peer ----------------------------
    print("\n" + "=" * 80)
    print("SOTR REVENUE MIX — BIHAR vs PEER AVERAGE (% of total SOTR)")
    print("Peers:", ", ".join(PEER_STATES))
    print("=" * 80)
    print(mix.to_string(index=False, float_format=lambda x: f"{x:+.2f}"))

    # ---- Print section: Peer gaps --------------------------------------
    print("\n" + "=" * 80)
    print("PEER-GROUP GAP ANALYSIS (FY 2023-24)")
    print("=" * 80)
    print(peer_gap.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    # ---- Print section: CAGR -------------------------------------------
    print("\n" + "=" * 80)
    print("CAGR: BIHAR vs NATIONAL AGGREGATE")
    print("=" * 80)
    fmt = cagr_tab.copy()
    fmt["bihar_cagr"] = fmt["bihar_cagr"].map(lambda x: f"{x * 100:.2f}%" if pd.notna(x) else "n/a")
    fmt["national_cagr"] = fmt["national_cagr"].map(lambda x: f"{x * 100:.2f}%" if pd.notna(x) else "n/a")
    print(fmt[["metric", "span_years", "start_year", "end_year",
               "bihar_cagr", "national_cagr"]].to_string(index=False))

    # ---- Print section: biggest opportunity gaps -----------------------
    print("\n" + "=" * 80)
    print("OPPORTUNITY GAPS: ₹ Crore Bihar would gain by matching peer")
    print("per-capita collection (sorted largest to smallest)")
    print("=" * 80)
    opp = peer_gap.sort_values("opportunity_crore", ascending=False).copy()
    opp["opportunity_crore"] = opp["opportunity_crore"].round(0).astype(int)
    opp["bihar_crore"] = opp["bihar_crore"].round(0).astype(int)
    opp["hypothetical_bihar_crore"] = opp["hypothetical_bihar_crore"].round(0).astype(int)
    opp_print = opp[["metric", "bihar_crore", "hypothetical_bihar_crore",
                     "opportunity_crore"]]
    opp_print.columns = ["metric", "bihar_actual", "if_matched_peer_pc",
                         "opportunity_gain"]
    print(opp_print.to_string(index=False))

    # ---- Write combined output -----------------------------------------
    OUT.parent.mkdir(parents=True, exist_ok=True)
    combined = peer_gap.merge(
        cagr_tab[["metric", "bihar_cagr", "national_cagr",
                  "start_year", "end_year"]],
        on="metric", how="left",
    ).merge(
        bihar_ranks[["rank_absolute", "rank_per_capita"]].reset_index(),
        on="metric", how="left",
    ).merge(
        mix.rename(columns={"sub_component": "metric"}),
        on="metric", how="left",
    )
    combined.to_csv(OUT, index=False)
    print(f"\nWrote {OUT} ({len(combined)} rows)")


if __name__ == "__main__":
    main()
