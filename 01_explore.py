"""Explore the structure of the state government financial data workbook.

Lists sheet names, prints shape/columns/head for each sheet, classifies
sheets as state-wise vs component-wise, and writes a data dictionary.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/Financial Data of state Governments.xlsx")
OUTPUT_PATH = Path("outputs/data_dictionary.md")

INDIAN_STATES = {
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jammu", "jharkhand",
    "karnataka", "kerala", "madhya pradesh", "maharashtra", "manipur",
    "meghalaya", "mizoram", "nagaland", "odisha", "orissa", "punjab",
    "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura",
    "uttar pradesh", "uttarakhand", "west bengal", "delhi", "puducherry",
    "all states", "all-states",
}


def find_state_mentions(df: pd.DataFrame) -> set[str]:
    """Return the set of Indian state names found anywhere in the sheet."""
    found = set()
    sample = df.astype(str).head(60)
    for col in sample.columns:
        for val in sample[col].tolist() + [str(col)]:
            low = val.lower().strip()
            for state in INDIAN_STATES:
                if state in low:
                    found.add(state)
    return found


def classify_sheet(df: pd.DataFrame) -> str:
    """Classify a sheet as state-wise, component-wise, or mixed/unclear."""
    states = find_state_mentions(df)
    if len(states) >= 5:
        return "state-wise"
    if len(states) >= 1:
        return "mixed / partial state data"
    return "component-wise"


def relevance_for_revenue(sheet_name: str, df: pd.DataFrame) -> str:
    """Heuristic relevance score for analyzing state revenue generation."""
    text = (sheet_name + " " + " ".join(str(c) for c in df.columns)).lower()
    head_text = " ".join(df.astype(str).head(20).values.flatten()).lower()
    blob = text + " " + head_text

    revenue_terms = [
        "revenue", "tax", "own tax", "non-tax", "gst", "sgst", "vat",
        "stamp", "excise", "devolution", "grants",
    ]
    hits = sum(1 for t in revenue_terms if t in blob)
    if hits >= 3:
        return "High"
    if hits >= 1:
        return "Medium"
    return "Low"


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Workbook not found at {DATA_PATH}")

    xls = pd.ExcelFile(DATA_PATH)
    print(f"Workbook: {DATA_PATH.name}")
    print(f"Total sheets: {len(xls.sheet_names)}")
    print("=" * 80)

    summaries = []
    for name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=name, header=None)
        kind = classify_sheet(df)
        relevance = relevance_for_revenue(name, df)

        print(f"\nSheet: {name!r}")
        print(f"  Shape: {df.shape}")
        print(f"  Classification: {kind}")
        print(f"  Revenue relevance: {relevance}")
        if df.empty:
            print("  (sheet is empty)")
            first_row = []
        else:
            first_row = [str(v) for v in df.iloc[0].head(8).tolist()]
            print(f"  Columns (row 0): {list(df.iloc[0].head(10))}")
            print("  First 5 rows:")
            with pd.option_context("display.max_columns", 8, "display.width", 160):
                print(df.head(5).to_string(index=False, header=False))
        print("-" * 80)

        summaries.append({
            "name": name,
            "shape": df.shape,
            "kind": kind,
            "relevance": relevance,
            "first_row": first_row,
            "preview": df.head(3),
        })

    write_dictionary(summaries)
    print(f"\nData dictionary written to {OUTPUT_PATH}")


def write_dictionary(summaries: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Data Dictionary — Financial Data of State Governments",
        "",
        f"Source: `{DATA_PATH.name}`  ",
        f"Total sheets: **{len(summaries)}**",
        "",
        "## Overview Table",
        "",
        "| # | Sheet | Shape (rows × cols) | Classification | Revenue relevance |",
        "|---|-------|--------------------|----------------|-------------------|",
    ]
    for i, s in enumerate(summaries, 1):
        lines.append(
            f"| {i} | `{s['name']}` | {s['shape'][0]} × {s['shape'][1]} "
            f"| {s['kind']} | {s['relevance']} |"
        )

    lines += ["", "## Sheet Details", ""]
    for s in summaries:
        lines += [
            f"### `{s['name']}`",
            "",
            f"- **Shape:** {s['shape'][0]} rows × {s['shape'][1]} columns",
            f"- **Classification:** {s['kind']}",
            f"- **Revenue relevance:** {s['relevance']}",
            f"- **First row (header-like):** {s['first_row']}",
            "",
            "```",
            s["preview"].to_string(index=False, header=False, max_cols=8),
            "```",
            "",
        ]

    high = [s["name"] for s in summaries if s["relevance"] == "High"]
    state_wise = [s["name"] for s in summaries if s["kind"] == "state-wise"]
    component_wise = [s["name"] for s in summaries if s["kind"] == "component-wise"]

    lines += [
        "## Most Relevant Sheets for State Revenue Analysis",
        "",
        "Sheets flagged as **High** relevance (contain revenue/tax/grants terms):",
        "",
    ]
    lines += [f"- `{n}`" for n in high] or ["- _(none detected — review manually)_"]

    lines += [
        "",
        "## State-wise vs Component-wise",
        "",
        "**State-wise sheets** (rows or columns enumerate Indian states):",
        "",
    ]
    lines += [f"- `{n}`" for n in state_wise] or ["- _(none detected)_"]
    lines += ["", "**Component-wise sheets** (revenue/expenditure categories, no state breakdown):", ""]
    lines += [f"- `{n}`" for n in component_wise] or ["- _(none detected)_"]

    OUTPUT_PATH.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
