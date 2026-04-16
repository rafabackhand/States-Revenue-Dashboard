"""Build the tidy master dataset of state revenue metrics.

Reads the source workbook and produces data/master_revenue.csv with one row
per (state, year, metric) tuple. Handles inconsistent headers, state-name
variants, and NaN-for-zero cases (SGST pre-2017).
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("data/Financial Data of state Governments.xlsx")
OUT = Path("data/master_revenue.csv")


# ---------------------------------------------------------------------------
# State-name canonicalization
# ---------------------------------------------------------------------------

CANONICAL_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir",
    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Puducherry",
]

ALIASES = {
    "andhrapradesh": "Andhra Pradesh",
    "arunachalpradesh": "Arunachal Pradesh",
    "madhyapradesh": "Madhya Pradesh",
    "uttarpradesh": "Uttar Pradesh",
    "himachalpradesh": "Himachal Pradesh",
    "tamilnadu": "Tamil Nadu",
    "westbengal": "West Bengal",
    "jammuandkashmir": "Jammu & Kashmir",
    "jammu&kashmir": "Jammu & Kashmir",
    "j&k": "Jammu & Kashmir",
    "orissa": "Odisha",
    "pondicherry": "Puducherry",
    "nctofdelhi": "Delhi",
    "gnctdofdelhi": "Delhi",
    "nctdelhi": "Delhi",
    "uttaranchal": "Uttarakhand",
    "chattisgarh": "Chhattisgarh",  # source-sheet typo
    "chhatisgarh": "Chhattisgarh",
    "uttrakhand": "Uttarakhand",  # source-sheet typo
    "arunchalpradesh": "Arunachal Pradesh",  # source-sheet typo in A3/A4
    "telanaga": "Telangana",  # source-sheet typo in A4
}
CANONICAL_LOOKUP = {s.lower().replace(" ", ""): s for s in CANONICAL_STATES}
CANONICAL_LOOKUP.update(ALIASES)


def canonicalize_state(raw: object) -> str | None:
    if raw is None or (isinstance(raw, float) and np.isnan(raw)):
        return None
    s = str(raw).strip()
    if not s or s.lower() in {"nan", "states", "state"}:
        return None
    s = s.replace("(Total)", "").strip()
    key = s.lower().replace(" ", "").replace(".", "")
    return CANONICAL_LOOKUP.get(key)


# ---------------------------------------------------------------------------
# Year parsing
# ---------------------------------------------------------------------------

def fiscal_year_start(value: object) -> int | None:
    """'2023-24' -> 2023. Returns None if not a fiscal-year token."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    s = str(value).strip()
    if "-" in s and s[:4].isdigit():
        return int(s[:4])
    return None


def to_float(x: object) -> float:
    if x is None:
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "")
    if s in {"", "-", "NA", "nan", "N/A"}:
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


# ---------------------------------------------------------------------------
# Extractors
# ---------------------------------------------------------------------------

def extract_total_revenue(xls: pd.ExcelFile) -> pd.DataFrame:
    """A1.1: one row per state, year columns in cols 2..12."""
    df = pd.read_excel(xls, sheet_name="A1.1 Rev. Reciepts", header=None)
    header_row = 1
    years = [fiscal_year_start(v) for v in df.iloc[header_row, 2:13]]
    records = []
    for _, row in df.iloc[header_row + 1:].iterrows():
        # The sheet has a second unrelated table below the first; stop when
        # the row-number column becomes non-numeric.
        row_num = row.iloc[0]
        if pd.isna(row_num) or not isinstance(row_num, (int, float)):
            break
        state = canonicalize_state(row.iloc[1])
        if state is None:
            continue
        for col_idx, year in enumerate(years, start=2):
            if year is None:
                continue
            records.append({
                "state": state,
                "year": year,
                "metric": "Total Revenue Receipts",
                "value": to_float(row.iloc[col_idx]),
            })
    return pd.DataFrame(records)


COMPONENT_ROW_MAP = {
    "states own tax": "SOTR",
    "share in union taxes": "Share in Union Taxes",
    "grants in aid css": "_grants_css",
    "grants in aid others": "_grants_others",
    "non tax rev int div profit": "_nontax_idp",
    "non tax rev others": "_nontax_others",
}


def normalize_label(raw: str) -> str:
    """Fold label variants ('Non-Tax' vs 'Non Tax', 'Grant in aid' vs
    'Grants in Aid', 'aid-CSS' vs 'aid - CSS') to a canonical key."""
    s = raw.lower().strip()
    s = s.replace("grant in aid", "grants in aid")  # source uses both
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def extract_components_a21(xls: pd.ExcelFile) -> pd.DataFrame:
    """A2.1: blocks of rows per state. First row 'State (Total)' sets the
    current state; subsequent rows list components until the next 'Total' row.
    Grants CSS + Others are summed into 'Grants in Aid'; Non-Tax Int/Div/Profit
    + Others are summed into 'Non-Tax Revenue'.
    """
    df = pd.read_excel(xls, sheet_name="A2.1 Comp. wise Rev Receipt ",
                       header=None)
    header_row = 1
    years = [fiscal_year_start(v) for v in df.iloc[header_row, 1:12]]

    records = []
    current_state = None
    stop_markers = {"total of all states", "all states", "a1 figures",
                    "reconcilitation", "reconciliation", "sntr", "sotr"}
    for _, row in df.iloc[header_row + 1:].iterrows():
        label = row.iloc[0]
        if label is None or (isinstance(label, float) and np.isnan(label)):
            continue
        label_s = str(label).strip()
        # Once we enter the reconciliation/aggregate section below the main
        # state blocks, stop.
        if label_s.lower() in stop_markers:
            break
        if label_s.lower().endswith("(total)"):
            current_state = canonicalize_state(label_s)
            continue
        if current_state is None:
            continue
        key = normalize_label(label_s)
        metric = COMPONENT_ROW_MAP.get(key)
        if metric is None:
            continue
        for col_idx, year in enumerate(years, start=1):
            if year is None:
                continue
            records.append({
                "state": current_state,
                "year": year,
                "metric": metric,
                "value": to_float(row.iloc[col_idx]),
            })

    raw = pd.DataFrame(records)
    # Combine sub-components: Grants CSS + Others, Non-Tax IDP + Others.
    pivot = raw.pivot_table(
        index=["state", "year"], columns="metric", values="value",
        aggfunc="sum",
    ).reset_index()

    pivot["Grants in Aid"] = pivot.get("_grants_css", 0).fillna(0) \
        + pivot.get("_grants_others", 0).fillna(0)
    pivot["Non-Tax Revenue"] = pivot.get("_nontax_idp", 0).fillna(0) \
        + pivot.get("_nontax_others", 0).fillna(0)

    keep = ["state", "year", "SOTR", "Share in Union Taxes",
            "Grants in Aid", "Non-Tax Revenue"]
    tidy = pivot[keep].melt(id_vars=["state", "year"],
                            var_name="metric", value_name="value")
    return tidy


SOTR_SUB_MAP = {
    "sgst": "SGST",
    "excise": "State Excise",
    "stamps and registration fees": "Stamps & Registration",
    "motor vehicle tax": "Motor Vehicle Tax",
    "taxes on sales, trade etc.": "Sales/Trade Tax",
    # 'Others' is intentionally excluded — caller didn't request it.
}


def extract_sotr_subcomponents(xls: pd.ExcelFile) -> pd.DataFrame:
    """A2.2: state rows followed by a fixed set of component rows.
    Years 2023-24..2014-15 in cols 1..10. SGST is 0 before 2017-18 by design.
    """
    df = pd.read_excel(xls, sheet_name="A2.2_SOTR_Components", header=None)
    header_row = 3
    years = [fiscal_year_start(v) for v in df.iloc[header_row, 1:11]]

    records = []
    current_state = None
    component_keys = set(SOTR_SUB_MAP) | {"others"}
    for _, row in df.iloc[header_row + 1:].iterrows():
        label = row.iloc[0]
        if label is None or (isinstance(label, float) and np.isnan(label)):
            continue
        label_s = str(label).strip()
        key = label_s.lower()
        if key not in component_keys:
            # A non-component label: either a real state (set context) or an
            # aggregate header like 'Components (All States)' (clear context
            # so the following component rows are not attributed to the prior
            # state).
            current_state = canonicalize_state(label_s)
            continue
        if current_state is None:
            continue
        metric = SOTR_SUB_MAP.get(key)
        if metric is None:
            continue
        for col_idx, year in enumerate(years, start=1):
            if year is None:
                continue
            value = to_float(row.iloc[col_idx])
            # SGST was introduced in 2017-18. Any NaN before that is a 0.
            if metric == "SGST" and year < 2017 and np.isnan(value):
                value = 0.0
            records.append({
                "state": current_state,
                "year": year,
                "metric": metric,
                "value": value,
            })
    return pd.DataFrame(records)


CAPITAL_ROW_MAP = {
    "misc capital receipts": "Capital: Misc Receipts",
    "recoveries of loans and advances": "Capital: Loan Recoveries",
    "internal debt": "Capital: Internal Debt",
    "loans and advances": "Capital: Loans from Centre",
    "public debt receipts": "Capital: Public Debt Receipts",
}


def extract_capital_receipts(xls: pd.ExcelFile) -> pd.DataFrame:
    """A3 (and duplicate A1.2): state blocks with a Total row then component
    rows (Misc Capital, Loan Recoveries, Internal Debt, Loans from Centre,
    Public Debt Receipts). We emit each component individually, plus a
    derived 'Non-Debt Capital Receipts' (Misc + Loan Recoveries) which is
    the only genuinely non-liability-creating portion.

    Note: the sheet title 'Non Debt Cap. Rec.' is misleading — the sheet
    actually contains ALL capital receipts, including borrowings.
    """
    df = pd.read_excel(xls, sheet_name="A3_Cap Receipts Components",
                       header=None)
    # Structure: row 0 is title, row 1 is header. State-name rows are in
    # col 2, component-name rows are also in col 2. Years span cols 3..13.
    header_row = 1
    years = [fiscal_year_start(v) for v in df.iloc[header_row, 3:14]]

    records = []
    current_state = None
    # The sheet has several reconciliation/cross-reference blocks below the
    # main state tables. Stop once we see any of these markers.
    stop_markers = {"non-debt capital receipt", "rec a1.1",
                    "total of all states", "all states", "reconciliation",
                    "reconcilitation"}
    for _, row in df.iloc[header_row + 1:].iterrows():
        label = row.iloc[2]
        if label is None or (isinstance(label, float) and np.isnan(label)):
            continue
        label_s = str(label).strip()
        if label_s.lower() in stop_markers:
            break
        if label_s.lower().endswith("(total)"):
            current_state = canonicalize_state(label_s)
            continue
        if current_state is None:
            continue
        key = normalize_label(label_s)
        metric = CAPITAL_ROW_MAP.get(key)
        if metric is None:
            continue
        for col_idx, year in enumerate(years, start=3):
            if year is None:
                continue
            records.append({
                "state": current_state,
                "year": year,
                "metric": metric,
                "value": to_float(row.iloc[col_idx]),
            })

    raw = pd.DataFrame(records)
    if raw.empty:
        return raw

    # Derive Non-Debt Capital Receipts = Misc + Loan Recoveries.
    pivot = raw.pivot_table(
        index=["state", "year"], columns="metric", values="value",
        aggfunc="sum",
    ).reset_index()
    misc = pivot.get("Capital: Misc Receipts", 0)
    recov = pivot.get("Capital: Loan Recoveries", 0)
    if isinstance(misc, int):
        misc = pd.Series(0, index=pivot.index)
    if isinstance(recov, int):
        recov = pd.Series(0, index=pivot.index)
    non_debt = (misc.fillna(0) + recov.fillna(0))
    derived = pivot[["state", "year"]].copy()
    derived["metric"] = "Non-Debt Capital Receipts"
    derived["value"] = non_debt.values

    return pd.concat([raw, derived], ignore_index=True)


FC_GRANT_ROW_MAP = {
    "revenue deficit grants": "FC Grant: Revenue Deficit",
    "grants for rural local bodies": "FC Grant: Rural Local Bodies",
    "grants for urban local bodies": "FC Grant: Urban Local Bodies",
    "gia for sdrf": "FC Grant: SDRF",
    "gia for sdmf": "FC Grant: SDMF",
    "grant for health sector": "FC Grant: Health",
    "others": "FC Grant: Others",
}


def extract_fc_grants(xls: pd.ExcelFile) -> pd.DataFrame:
    """A4 FC Grants: drill-down of Grants in Aid into Finance Commission
    categories. Only covers FY 2017-18 onwards (14th/15th FC era).

    IMPORTANT: The totals on this sheet are a SUBSET of 'Grants in Aid'
    already captured from A2.1, so we do NOT emit a total — only the
    sub-components with an 'FC Grant:' prefix to prevent accidental sums.
    """
    df = pd.read_excel(xls, sheet_name="A4 FC Grants", header=None)
    header_row = 1
    years = [fiscal_year_start(v) for v in df.iloc[header_row, 1:8]]

    records = []
    current_state = None
    stop_markers = {"total of all states", "total", "components"}
    for _, row in df.iloc[header_row + 1:].iterrows():
        label = row.iloc[0]
        if label is None or (isinstance(label, float) and np.isnan(label)):
            continue
        label_s = str(label).strip()
        if label_s.lower() in stop_markers:
            break
        # A header row may end in '(Total)' or just be the bare state name
        # ('Meghalaya' in A4). Try to canonicalize; if it matches a known
        # state, set context.
        if label_s.lower().endswith("(total)"):
            current_state = canonicalize_state(label_s)
            continue
        maybe_state = canonicalize_state(label_s)
        key = normalize_label(label_s)
        if maybe_state is not None and key not in FC_GRANT_ROW_MAP:
            current_state = maybe_state
            continue
        if current_state is None:
            continue
        metric = FC_GRANT_ROW_MAP.get(key)
        if metric is None:
            continue
        for col_idx, year in enumerate(years, start=1):
            if year is None:
                continue
            records.append({
                "state": current_state,
                "year": year,
                "metric": metric,
                "value": to_float(row.iloc[col_idx]),
            })
    return pd.DataFrame(records)


def extract_electricity_duty(xls: pd.ExcelFile) -> pd.DataFrame:
    """'SOTR components' sheet: only 2023-24 data, but has Electricity Duty."""
    df = pd.read_excel(xls, sheet_name="SOTR components", header=None)
    # Header row 1 has labels; row 0 cell (0,1) is '2023-24'. The sheet has
    # additional comparison blocks below the main table; stop at the first
    # 'Total' row so we don't double-count.
    year = fiscal_year_start(df.iloc[0, 1])
    records = []
    for _, row in df.iloc[2:].iterrows():
        label = row.iloc[0]
        if isinstance(label, str) and label.strip().lower() == "total":
            break
        state = canonicalize_state(label)
        if state is None:
            continue
        # Column 6 is 'Taxes and Duties on Electricity'.
        records.append({
            "state": state,
            "year": year,
            "metric": "Electricity Duty",
            "value": to_float(row.iloc[6]),
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    xls = pd.ExcelFile(SRC)
    parts = [
        extract_total_revenue(xls),
        extract_components_a21(xls),
        extract_sotr_subcomponents(xls),
        extract_electricity_duty(xls),
        extract_capital_receipts(xls),
        extract_fc_grants(xls),
    ]
    master = pd.concat(parts, ignore_index=True)
    master = master.dropna(subset=["state", "year", "metric"])
    master["year"] = master["year"].astype(int)
    master = master.sort_values(["state", "year", "metric"]).reset_index(drop=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(OUT, index=False)

    # Summary
    print(f"Wrote {OUT}")
    print(f"Rows: {len(master):,}")
    states = sorted(master["state"].unique())
    print(f"States covered: {len(states)}")
    print(f"  {', '.join(states)}")
    print(f"Year range: {master['year'].min()} – {master['year'].max()}")
    print(f"Metrics: {sorted(master['metric'].unique())}")

    print("\nRow counts per metric:")
    print(master.groupby("metric").size().to_string())

    print("\nCoverage matrix (non-null values per state × metric):")
    coverage = master.dropna(subset=["value"]).groupby(
        ["state", "metric"]).size().unstack(fill_value=0)
    print(coverage.to_string())

    # Missing-data report
    expected_metrics = {
        "Total Revenue Receipts", "SOTR", "Share in Union Taxes",
        "Grants in Aid", "Non-Tax Revenue",
    }
    print("\nStates missing one or more core metrics entirely:")
    missing = []
    for state in states:
        got = set(master.loc[master["state"] == state, "metric"])
        gap = expected_metrics - got
        if gap:
            missing.append(f"  {state}: missing {sorted(gap)}")
    print("\n".join(missing) if missing else "  (none)")

    print("\nNote: Electricity Duty is only available for 2023-24 "
          "(source sheet 'SOTR components' has no prior years).")
    print("Note: SGST NaN values before fiscal year 2017 converted to 0 "
          "(GST was introduced July 2017).")


if __name__ == "__main__":
    main()
