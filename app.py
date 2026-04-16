"""Interactive Plotly Dash dashboard for state revenue comparison.

Local run:    python app.py              (http://localhost:8050)
Production:   gunicorn app:server        (PORT supplied by host platform)
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

# ---------------------------------------------------------------------------
# Data path: try data/ subfolder, fall back to repo root.
# ---------------------------------------------------------------------------
_CANDIDATES = [Path("data/master_revenue.csv"), Path("master_revenue.csv")]
MASTER = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])

# 2011 Census; Andhra Pradesh / Telangana post-2014 bifurcation.
POPULATION = {
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
REVENUE_PILLARS = ["SOTR", "Share in Union Taxes",
                   "Grants in Aid", "Non-Tax Revenue"]
CORE_METRICS = ["Total Revenue Receipts"] + REVENUE_PILLARS
CAPITAL_METRICS = ["Non-Debt Capital Receipts",
                   "Capital: Public Debt Receipts"]
FC_GRANT_METRICS = ["FC Grant: Revenue Deficit",
                    "FC Grant: Rural Local Bodies",
                    "FC Grant: Urban Local Bodies",
                    "FC Grant: SDRF", "FC Grant: SDMF", "FC Grant: Health"]
ALL_METRICS = CORE_METRICS + SOTR_SUBS + CAPITAL_METRICS + FC_GRANT_METRICS

DEFAULT_STATE = "Bihar"
DEFAULT_PEERS = ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan",
                 "Odisha", "Jharkhand", "West Bengal"]

# Colours
C_PRIMARY = "#C8102E"        # focus state
C_PEER_AVG = "#1F77B4"       # peer average
C_NATIONAL = "#7F7F7F"       # national
C_BORROW = "#E07B00"         # borrowings
PILLAR_COLORS = {
    "SOTR": "#1F77B4",
    "Share in Union Taxes": "#2CA02C",
    "Grants in Aid": "#FF9E2C",
    "Non-Tax Revenue": "#9467BD",
}
SOTR_COLORS = {
    "SGST": "#4C72B0", "Sales/Trade Tax": "#DD8452",
    "Stamps & Registration": "#55A868", "State Excise": "#C44E52",
    "Motor Vehicle Tax": "#8172B3",
}

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
df = pd.read_csv(MASTER)
STATES = sorted(df["state"].unique())
YEARS = sorted(df["year"].unique())
LATEST = max(YEARS)

# Period definitions — each maps to {label, year span for averaging, CAGR start year}.
PERIODS = {
    "latest": {
        "label": f"FY {LATEST}-{(LATEST + 1) % 100:02d} only",
        "years": [LATEST],
        "cagr_span": None,  # single year, no CAGR
    },
    "last5": {
        "label": "Last 5 years (avg)",
        "years": list(range(LATEST - 4, LATEST + 1)),
        "cagr_span": 5,   # 5-year CAGR: (2018-19 → 2023-24)
    },
    "last10": {
        "label": "Last 10 years (avg)",
        "years": list(range(LATEST - 9, LATEST + 1)),
        "cagr_span": 10,  # 10-year CAGR: (2013-14 → 2023-24)
    },
}


def period_wide(period_key: str) -> pd.DataFrame:
    """Average all metric values over the period years → state × metric."""
    years = PERIODS[period_key]["years"]
    sub = df[df["year"].isin(years)]
    w = sub.pivot_table(index="state", columns="metric",
                        values="value", aggfunc="mean")
    w["population"] = w.index.map(POPULATION)
    return w


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Dash(__name__, title="State Revenue Explorer")

app.layout = html.Div(
    style={"fontFamily": "system-ui, -apple-system, sans-serif",
           "maxWidth": "1400px", "margin": "0 auto", "padding": "24px",
           "backgroundColor": "#FFFFFF"},
    children=[
        # Header
        html.H1("Indian State Revenue Explorer",
                style={"marginBottom": "4px"}),
        html.P([
            f"Fiscal years 2013-14 to {LATEST}-{(LATEST + 1) % 100:02d} · ",
            "Source: Financial Data of State Governments, Ministry of "
            "Finance · ",
            f"{len(STATES)} states",
        ], style={"color": "#666", "marginTop": "0"}),

        # Controls row
        html.Div(
            style={"display": "grid",
                   "gridTemplateColumns": "1.2fr 2fr 1.6fr",
                   "gap": "20px",
                   "marginTop": "20px",
                   "marginBottom": "20px",
                   "padding": "14px",
                   "backgroundColor": "#F7F7F9",
                   "borderRadius": "8px"},
            children=[
                html.Div([
                    html.Label("Focus state",
                               style={"fontWeight": "600",
                                      "display": "block",
                                      "fontSize": "12px",
                                      "textTransform": "uppercase",
                                      "color": "#555",
                                      "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="state-dropdown",
                        options=[{"label": s, "value": s} for s in STATES],
                        value=DEFAULT_STATE, clearable=False,
                    ),
                ]),
                html.Div([
                    html.Label("Peer group",
                               style={"fontWeight": "600",
                                      "display": "block",
                                      "fontSize": "12px",
                                      "textTransform": "uppercase",
                                      "color": "#555",
                                      "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="peer-dropdown",
                        options=[{"label": s, "value": s} for s in STATES],
                        value=DEFAULT_PEERS, multi=True,
                    ),
                ]),
                html.Div([
                    html.Label("Time period",
                               style={"fontWeight": "600",
                                      "display": "block",
                                      "fontSize": "12px",
                                      "textTransform": "uppercase",
                                      "color": "#555",
                                      "marginBottom": "6px"}),
                    dcc.RadioItems(
                        id="period-radio",
                        options=[{"label": PERIODS[k]["label"], "value": k}
                                 for k in ["latest", "last5", "last10"]],
                        value="latest",
                        labelStyle={"display": "block", "fontSize": "13px",
                                    "marginBottom": "3px"},
                    ),
                ]),
            ],
        ),

        # KPI row (5 cards)
        html.Div(id="kpi-row",
                 style={"display": "grid",
                        "gridTemplateColumns": "repeat(5, 1fr)",
                        "gap": "10px",
                        "marginBottom": "28px"}),

        # --- Section 1: Over time ---
        html.H3("How the state's revenue has evolved",
                style={"marginTop": "28px", "borderBottom": "1px solid #EEE",
                       "paddingBottom": "6px"}),

        html.Div([
            html.H4("Total revenue receipts — trend",
                    style={"marginBottom": "4px", "color": "#333"}),
            html.P("State vs peer average vs national average, ₹ Crore.",
                   style={"color": "#777", "fontSize": "12px",
                          "marginTop": "0"}),
            dcc.Graph(id="trend-chart"),
        ], style={"marginBottom": "24px"}),

        html.Div([
            html.H4("Revenue composition over time — where does each rupee come from?",
                    style={"marginBottom": "4px", "color": "#333"}),
            html.P(
                "Shows share of Total Revenue Receipts coming from each of "
                "the four pillars: own tax (SOTR), share in Union Taxes, "
                "grants, and non-tax revenue. A rising 'Share in Union "
                "Taxes' + 'Grants' share = growing dependence on the "
                "Centre.",
                style={"color": "#777", "fontSize": "12px",
                       "marginTop": "0"}),
            dcc.Graph(id="composition-evolution-chart"),
        ], style={"marginBottom": "24px"}),

        html.Div([
            html.H4("Borrowings vs revenue receipts — the fiscal leverage picture",
                    style={"marginBottom": "4px", "color": "#333"}),
            html.P(
                "Public Debt Receipts are gross new borrowings taken on by "
                "the state each year. Comparing against Revenue Receipts "
                "shows how leveraged the state's fiscal position is.",
                style={"color": "#777", "fontSize": "12px",
                       "marginTop": "0"}),
            dcc.Graph(id="borrow-chart"),
        ], style={"marginBottom": "24px"}),

        # --- Section 2: Growth ---
        html.H3("Growth — who's gaining ground",
                style={"marginTop": "28px", "borderBottom": "1px solid #EEE",
                       "paddingBottom": "6px"}),

        html.Div([
            html.H4(id="cagr-title",
                    style={"marginBottom": "4px", "color": "#333"}),
            html.P(
                "Compound annual growth rate (CAGR) of each revenue metric. "
                "Higher = revenue compounding faster. Select 'Last 5' or "
                "'Last 10 years' above to change the CAGR window.",
                style={"color": "#777", "fontSize": "12px",
                       "marginTop": "0"}),
            dcc.Graph(id="cagr-chart"),
        ], style={"marginBottom": "24px"}),

        # --- Section 3: vs Peers ---
        html.H3("Benchmarks — how the state stacks up against peers",
                style={"marginTop": "28px", "borderBottom": "1px solid #EEE",
                       "paddingBottom": "6px"}),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                   "gap": "20px", "marginBottom": "24px"},
            children=[
                html.Div([
                    html.H4("Per-capita comparison",
                            style={"marginBottom": "4px", "color": "#333"}),
                    html.P(
                        "₹ per person. Controls for population. Longer red "
                        "bar vs blue = state collects more per person than "
                        "peers.",
                        style={"color": "#777", "fontSize": "12px",
                               "marginTop": "0"}),
                    dcc.Graph(id="comparison-chart"),
                ]),
                html.Div([
                    html.H4("SOTR composition",
                            style={"marginBottom": "4px", "color": "#333"}),
                    html.P(
                        "Within own tax revenue, how is the pie divided? "
                        "Unusually high reliance on one tax signals "
                        "vulnerability.",
                        style={"color": "#777", "fontSize": "12px",
                               "marginTop": "0"}),
                    dcc.Graph(id="composition-chart"),
                ]),
            ],
        ),

        # --- Section 4: full rankings ---
        html.H3(id="rankings-title",
                style={"marginTop": "28px", "borderBottom": "1px solid #EEE",
                       "paddingBottom": "6px"}),
        html.P(
            "Each metric is ranked across all 28 states. 'Rank abs' uses "
            "raw ₹-Crore values (size). 'Rank per-capita' uses ₹ per "
            "person (effort). Lower rank = better. Green ≤ 5 (top). "
            "Red ≥ 20 (bottom).",
            style={"color": "#666", "fontSize": "12px",
                   "marginTop": "0", "marginBottom": "12px"}),
        html.Div(id="ranking-table"),

        html.Div(
            style={"marginTop": "36px", "paddingTop": "16px",
                   "borderTop": "1px solid #EEE", "color": "#888",
                   "fontSize": "11px"},
            children=[
                html.P([
                    "Notes: (i) 'SGST' was introduced July 2017 so its "
                    "pre-2017 values are 0, not missing. (ii) Electricity "
                    "Duty is only available for 2023-24 in the source. "
                    "(iii) State Excise is policy-driven — near-zero in "
                    "Bihar since 2016 (prohibition). (iv) Per-capita "
                    "computations use Census 2011 population."
                ]),
            ],
        ),
    ],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def kpi_card(label: str, value: str, sub: str = "",
             accent: str = C_PRIMARY) -> html.Div:
    return html.Div(
        style={"background": "#F7F7F9", "borderRadius": "8px",
               "padding": "12px 14px",
               "borderLeft": f"4px solid {accent}"},
        children=[
            html.Div(label, style={"fontSize": "10px", "color": "#666",
                                   "textTransform": "uppercase",
                                   "letterSpacing": "0.5px",
                                   "fontWeight": "600"}),
            html.Div(value, style={"fontSize": "19px", "fontWeight": "700",
                                   "marginTop": "4px"}),
            html.Div(sub, style={"fontSize": "11px", "color": "#888",
                                 "marginTop": "2px"}),
        ],
    )


def fmt_crore(x: float) -> str:
    if x is None or pd.isna(x):
        return "—"
    if abs(x) >= 1_00_000:
        return f"₹{x / 100_000:.2f} L Cr"
    return f"₹{x:,.0f} Cr"


def cagr(start: float, end: float, years: int) -> float | None:
    if start is None or end is None:
        return None
    if pd.isna(start) or pd.isna(end) or start <= 0:
        return None
    return (end / start) ** (1 / years) - 1


def peer_wide_avg(wide: pd.DataFrame, peers: list[str],
                  metric: str) -> float | None:
    if not peers:
        return None
    vals = wide.loc[[p for p in peers if p in wide.index], metric].dropna()
    return float(vals.mean()) if len(vals) else None


def peer_per_capita(wide: pd.DataFrame, peers: list[str],
                    metric: str) -> float | None:
    if not peers:
        return None
    valid = [p for p in peers if p in wide.index]
    if not valid:
        return None
    vals = wide.loc[valid, metric]
    pops = wide.loc[valid, "population"]
    pc = (vals * 1e7 / pops).dropna()
    return float(pc.mean()) if len(pc) else None


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
    Input("period-radio", "value"),
)
def render_kpis(state, peers, period):
    peers = [p for p in (peers or []) if p != state]
    wide = period_wide(period)
    row = wide.loc[state]

    total = row.get("Total Revenue Receipts")
    sotr = row.get("SOTR")
    share_ut = row.get("Share in Union Taxes")
    grants = row.get("Grants in Aid")
    nontax = row.get("Non-Tax Revenue")
    borrowings = row.get("Capital: Public Debt Receipts")

    own_rev = (sotr or 0) + (nontax or 0)
    central = (share_ut or 0) + (grants or 0)

    pop = POPULATION[state]
    total_pc = (total * 1e7 / pop) if total else 0

    own_share = (own_rev / total * 100) if total else 0
    central_share = (central / total * 100) if total else 0
    borrow_ratio = (borrowings / total * 100) if total and borrowings else 0

    # Peer averages for subtitles.
    peer_own = None
    peer_borrow = None
    if peers:
        peer_own_vals = []
        peer_borrow_vals = []
        for p in peers:
            if p not in wide.index:
                continue
            pr = wide.loc[p]
            pt = pr.get("Total Revenue Receipts")
            if not pt:
                continue
            p_own = (pr.get("SOTR") or 0) + (pr.get("Non-Tax Revenue") or 0)
            peer_own_vals.append(p_own / pt * 100)
            pb = pr.get("Capital: Public Debt Receipts")
            if pb is not None and not pd.isna(pb):
                peer_borrow_vals.append(pb / pt * 100)
        if peer_own_vals:
            peer_own = sum(peer_own_vals) / len(peer_own_vals)
        if peer_borrow_vals:
            peer_borrow = sum(peer_borrow_vals) / len(peer_borrow_vals)

    return [
        kpi_card("Total Revenue",
                 fmt_crore(total),
                 f"₹{total_pc:,.0f} per person"),
        kpi_card("Own tax (SOTR)",
                 fmt_crore(sotr),
                 f"{(sotr / total * 100):.1f}% of total" if total else "—"),
        kpi_card("Central transfers",
                 fmt_crore(central),
                 f"{central_share:.1f}% of total",
                 accent=PILLAR_COLORS["Share in Union Taxes"]),
        kpi_card("Own revenue share",
                 f"{own_share:.1f}%",
                 (f"Peers: {peer_own:.1f}%" if peer_own is not None
                  else "(add peers to compare)"),
                 accent=("#2CA02C" if peer_own and own_share >= peer_own
                         else C_PRIMARY)),
        kpi_card("Borrowings ÷ revenue",
                 f"{borrow_ratio:.1f}%",
                 (f"Peers: {peer_borrow:.1f}%" if peer_borrow is not None
                  else "Fiscal leverage"),
                 accent=C_BORROW),
    ]


@app.callback(
    Output("trend-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
)
def render_trend(state, peers):
    peers = [p for p in (peers or []) if p != state]
    metric = "Total Revenue Receipts"

    state_series = (df[(df.state == state) & (df.metric == metric)]
                    .sort_values("year"))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_series["year"], y=state_series["value"],
        mode="lines+markers", name=state,
        line=dict(color=C_PRIMARY, width=3), marker=dict(size=8),
    ))
    if peers:
        ps = (df[(df.state.isin(peers)) & (df.metric == metric)]
              .groupby("year")["value"].mean().reset_index())
        fig.add_trace(go.Scatter(
            x=ps.year, y=ps.value, mode="lines+markers",
            name=f"Peer avg ({len(peers)})",
            line=dict(color=C_PEER_AVG, width=2, dash="dash"),
            marker=dict(size=6),
        ))
    nat = (df[df.metric == metric].groupby("year")["value"]
           .mean().reset_index())
    fig.add_trace(go.Scatter(
        x=nat.year, y=nat.value, mode="lines", name="National avg",
        line=dict(color=C_NATIONAL, width=1.5, dash="dot"),
    ))
    fig.update_layout(
        xaxis_title="Fiscal year (start)",
        yaxis_title="₹ Crore", hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=40), height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
    )
    return fig


@app.callback(
    Output("composition-evolution-chart", "figure"),
    Input("state-dropdown", "value"),
)
def render_composition_evolution(state):
    pillars = (df[(df.state == state) & (df.metric.isin(REVENUE_PILLARS))]
               .pivot(index="year", columns="metric", values="value")
               .fillna(0)
               .sort_index())
    totals = pillars.sum(axis=1)
    share = pillars.div(totals, axis=0) * 100

    fig = go.Figure()
    for pillar in REVENUE_PILLARS:
        if pillar not in share.columns:
            continue
        fig.add_trace(go.Scatter(
            x=share.index, y=share[pillar], name=pillar,
            mode="lines", stackgroup="one",
            line=dict(width=0.5, color=PILLAR_COLORS[pillar]),
            hovertemplate=f"{pillar}: %{{y:.1f}}%<extra></extra>",
        ))
    fig.update_layout(
        xaxis_title="Fiscal year (start)",
        yaxis_title="Share of total revenue (%)",
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=40), height=340,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
    )
    return fig


@app.callback(
    Output("borrow-chart", "figure"),
    Input("state-dropdown", "value"),
)
def render_borrow(state):
    sub = (df[(df.state == state) &
              (df.metric.isin(["Total Revenue Receipts",
                               "Capital: Public Debt Receipts"]))]
           .pivot(index="year", columns="metric", values="value")
           .sort_index())

    fig = go.Figure()
    if "Total Revenue Receipts" in sub.columns:
        fig.add_trace(go.Bar(
            x=sub.index, y=sub["Total Revenue Receipts"],
            name="Revenue Receipts",
            marker_color=C_PRIMARY, opacity=0.88,
        ))
    if "Capital: Public Debt Receipts" in sub.columns:
        fig.add_trace(go.Bar(
            x=sub.index, y=sub["Capital: Public Debt Receipts"],
            name="Public Debt Receipts (borrowings)",
            marker_color=C_BORROW, opacity=0.88,
        ))

    # Ratio line on secondary y-axis.
    if {"Total Revenue Receipts",
            "Capital: Public Debt Receipts"}.issubset(sub.columns):
        ratio = (sub["Capital: Public Debt Receipts"] /
                 sub["Total Revenue Receipts"]) * 100
        fig.add_trace(go.Scatter(
            x=sub.index, y=ratio, name="Borrowings ÷ Revenue (%)",
            mode="lines+markers",
            line=dict(color="#333", width=2), yaxis="y2",
        ))

    fig.update_layout(
        barmode="group",
        xaxis_title="Fiscal year (start)",
        yaxis=dict(title="₹ Crore"),
        yaxis2=dict(title="Borrowings ÷ Revenue (%)",
                    overlaying="y", side="right",
                    range=[0, 100], showgrid=False),
        hovermode="x unified",
        margin=dict(l=20, r=60, t=20, b=40), height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
    )
    return fig


@app.callback(
    Output("cagr-chart", "figure"),
    Output("cagr-title", "children"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
    Input("period-radio", "value"),
)
def render_cagr(state, peers, period):
    peers = [p for p in (peers or []) if p != state]
    span = PERIODS[period]["cagr_span"]
    if span is None:
        fig = go.Figure()
        fig.add_annotation(
            text="CAGR needs a multi-year span.<br>"
                 "Select <b>Last 5 years</b> or <b>Last 10 years</b> "
                 "above to see growth comparison.",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=14, color="#666"),
        )
        fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False),
                          margin=dict(l=20, r=20, t=20, b=20), height=300)
        return fig, "Growth rate (CAGR) — select a multi-year period"

    end_year = LATEST
    start_year = LATEST - span

    metrics = ["Total Revenue Receipts", "SOTR", "Share in Union Taxes",
               "Grants in Aid", "Non-Tax Revenue"]

    def cagr_for(state_name, metric):
        sub = df[(df.state == state_name) & (df.metric == metric)]
        if sub.empty:
            return None
        try:
            s = sub[sub.year == start_year]["value"].iloc[0]
            e = sub[sub.year == end_year]["value"].iloc[0]
        except IndexError:
            return None
        return cagr(s, e, span)

    def peer_cagr(metric):
        if not peers:
            return None
        vals = [cagr_for(p, metric) for p in peers]
        vals = [v for v in vals if v is not None]
        return (sum(vals) / len(vals)) if vals else None

    def national_cagr(metric):
        agg = (df[df.metric == metric]
               .groupby("year")["value"].sum())
        if start_year not in agg.index or end_year not in agg.index:
            return None
        return cagr(agg.loc[start_year], agg.loc[end_year], span)

    state_vals = [cagr_for(state, m) for m in metrics]
    peer_vals = [peer_cagr(m) for m in metrics]
    nat_vals = [national_cagr(m) for m in metrics]

    def pct(x):
        return round(x * 100, 2) if x is not None else None

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=metrics, x=[pct(v) for v in state_vals], name=state,
        orientation="h", marker_color=C_PRIMARY,
        text=[f"{pct(v):.1f}%" if v is not None else "—"
              for v in state_vals],
        textposition="outside",
    ))
    if peers:
        fig.add_trace(go.Bar(
            y=metrics, x=[pct(v) for v in peer_vals],
            name=f"Peer avg ({len(peers)})",
            orientation="h", marker_color=C_PEER_AVG, opacity=0.85,
            text=[f"{pct(v):.1f}%" if v is not None else "—"
                  for v in peer_vals],
            textposition="outside",
        ))
    fig.add_trace(go.Bar(
        y=metrics, x=[pct(v) for v in nat_vals], name="National",
        orientation="h", marker_color=C_NATIONAL, opacity=0.7,
        text=[f"{pct(v):.1f}%" if v is not None else "—" for v in nat_vals],
        textposition="outside",
    ))
    fig.update_layout(
        barmode="group", xaxis_title=f"CAGR (%) over {span} years",
        margin=dict(l=20, r=60, t=20, b=40), height=380,
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
    )
    title = (f"{span}-year CAGR ({start_year}-{start_year % 100 + 1:02d} → "
             f"{end_year}-{(end_year + 1) % 100:02d})")
    return fig, title


@app.callback(
    Output("composition-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
    Input("period-radio", "value"),
)
def render_sotr_composition(state, peers, period):
    peers = [p for p in (peers or []) if p != state]
    wide = period_wide(period)

    def shares(states_):
        rows = wide.loc[states_, SOTR_SUBS]
        totals = rows.sum(axis=1)
        return (rows.div(totals, axis=0) * 100).mean()

    cols = {state: shares([state])}
    if peers:
        cols["Peer avg"] = shares(peers)
    comp = pd.DataFrame(cols).T[SOTR_SUBS]

    fig = go.Figure()
    for sub in SOTR_SUBS:
        fig.add_trace(go.Bar(
            name=sub, x=comp.index, y=comp[sub],
            text=[f"{v:.0f}%" if v >= 3 else "" for v in comp[sub]],
            textposition="inside", textfont=dict(color="white"),
            marker_color=SOTR_COLORS[sub],
        ))
    fig.update_layout(
        barmode="stack", yaxis_title="% of SOTR", yaxis_range=[0, 105],
        margin=dict(l=20, r=20, t=20, b=20), height=370,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    return fig


@app.callback(
    Output("comparison-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
    Input("period-radio", "value"),
)
def render_comparison(state, peers, period):
    peers = [p for p in (peers or []) if p != state]
    wide = period_wide(period)
    metrics = [m for m in ALL_METRICS if m in wide.columns]

    # Filter to only "main" metrics for this compact chart — keep it focused.
    focus_metrics = [m for m in CORE_METRICS + SOTR_SUBS
                     + ["Non-Debt Capital Receipts",
                        "Capital: Public Debt Receipts"]
                     if m in metrics]

    state_pop = POPULATION[state]
    state_pc, peer_pc = [], []
    for m in focus_metrics:
        sv = wide.loc[state, m] if m in wide.columns else None
        state_pc.append((sv * 1e7 / state_pop) if pd.notna(sv) else None)
        peer_pc.append(peer_per_capita(wide, peers, m))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=state, y=focus_metrics, x=state_pc, orientation="h",
        marker_color=C_PRIMARY,
    ))
    if peers:
        fig.add_trace(go.Bar(
            name=f"Peer avg ({len(peers)})", y=focus_metrics, x=peer_pc,
            orientation="h", marker_color=C_PEER_AVG, opacity=0.85,
        ))
    fig.update_layout(
        barmode="group", xaxis_title="₹ per person",
        margin=dict(l=20, r=20, t=20, b=40), height=430,
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.18),
    )
    return fig


@app.callback(
    Output("ranking-table", "children"),
    Output("rankings-title", "children"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
    Input("period-radio", "value"),
)
def render_ranking(state, peers, period):
    peers = [p for p in (peers or []) if p != state]
    wide = period_wide(period)
    metrics = [m for m in ALL_METRICS if m in wide.columns]
    n = len(wide)

    rows = []
    for m in metrics:
        values = wide[m].dropna()
        if state not in values.index:
            continue
        pc = values * 1e7 / wide.loc[values.index, "population"]
        abs_rank = int(values.rank(ascending=False, method="min")[state])
        pc_rank = int(pc.rank(ascending=False, method="min")[state])
        state_val = values[state]
        peer_avg_val = (wide.loc[peers, m].mean()
                        if peers and m in wide.columns else None)
        rows.append({
            "Metric": m,
            "Value": fmt_crore(state_val),
            f"Rank abs / {n}": abs_rank,
            f"Rank per-capita / {n}": pc_rank,
            "Peer avg": (fmt_crore(peer_avg_val)
                         if peer_avg_val else "—"),
            "vs peer avg": (
                f"{((state_val - peer_avg_val) / peer_avg_val * 100):+.0f}%"
                if peer_avg_val else "—"),
        })

    if not rows:
        table = html.Div("No data for selection.")
    else:
        header = html.Tr([
            html.Th(c, style={"padding": "8px 12px",
                              "background": "#F7F7F9",
                              "textAlign": "left",
                              "borderBottom": "2px solid #DDD",
                              "fontSize": "12px"}) for c in rows[0].keys()])
        body = []
        for r in rows:
            cells = []
            for k, v in r.items():
                style = {"padding": "8px 12px",
                         "borderBottom": "1px solid #EEE",
                         "fontSize": "13px"}
                if "Rank" in k and isinstance(v, int):
                    if v <= 5:
                        style["color"] = "#2CA02C"
                        style["fontWeight"] = "600"
                    elif v >= 20:
                        style["color"] = C_PRIMARY
                        style["fontWeight"] = "600"
                cells.append(html.Td(v, style=style))
            body.append(html.Tr(cells))
        table = html.Table(
            [html.Thead(header), html.Tbody(body)],
            style={"width": "100%", "borderCollapse": "collapse"},
        )

    title = f"Full rankings — {PERIODS[period]['label']}"
    return table, title


# ---------------------------------------------------------------------------
# Expose Flask server for gunicorn (`gunicorn app:server`)
server = app.server


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    if host == "127.0.0.1":
        print(f"\nOpen http://localhost:{port} in your browser\n")
    app.run(host=host, port=port, debug=False)
