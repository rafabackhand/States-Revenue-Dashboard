"""Interactive Plotly Dash dashboard for state revenue comparison.

Local run:    python app.py              (http://localhost:8050)
Production:   gunicorn app:server         (PORT supplied by host platform)
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

# Look for the CSV in the usual place (data/) first, then fall back to
# the repo root. The root fallback covers cases where the file was
# uploaded without preserving folder structure (e.g., github.com web UI
# when dragging individual files instead of a folder).
_CANDIDATES = [Path("data/master_revenue.csv"), Path("master_revenue.csv")]
MASTER = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])

# Census 2011; AP/Telangana post-2014 bifurcation figures.
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
CORE_METRICS = ["Total Revenue Receipts", "SOTR", "Share in Union Taxes",
                "Grants in Aid", "Non-Tax Revenue"]
CAPITAL_METRICS = ["Non-Debt Capital Receipts",
                   "Capital: Public Debt Receipts"]
FC_GRANT_METRICS = ["FC Grant: Revenue Deficit",
                    "FC Grant: Rural Local Bodies",
                    "FC Grant: Urban Local Bodies",
                    "FC Grant: SDRF", "FC Grant: SDMF", "FC Grant: Health"]
# ALL_METRICS drives the rankings table and comparison chart.
ALL_METRICS = (CORE_METRICS + SOTR_SUBS + CAPITAL_METRICS + FC_GRANT_METRICS)

# Default selections.
DEFAULT_STATE = "Bihar"
DEFAULT_PEERS = ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan",
                 "Odisha", "Jharkhand", "West Bengal"]

# Colors
C_PRIMARY = "#C8102E"     # selected state
C_PEER_AVG = "#1F77B4"    # peer average
C_NATIONAL = "#7F7F7F"    # national

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

df = pd.read_csv(MASTER)
STATES = sorted(df["state"].unique())
YEARS = sorted(df["year"].unique())
LATEST = max(YEARS)


def latest_wide() -> pd.DataFrame:
    w = (df[df["year"] == LATEST]
         .pivot_table(index="state", columns="metric",
                      values="value", aggfunc="first"))
    w["population"] = w.index.map(POPULATION)
    return w


WIDE_LATEST = latest_wide()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = Dash(__name__, title="State Revenue Explorer")

app.layout = html.Div(
    style={"fontFamily": "system-ui, -apple-system, sans-serif",
           "maxWidth": "1400px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Indian State Revenue Explorer",
                style={"marginBottom": "4px"}),
        html.P(f"FY 2013-14 through 2023-24 · Source: Financial Data of "
               f"State Governments, Ministry of Finance · "
               f"{len(STATES)} states",
               style={"color": "#666", "marginTop": "0"}),

        html.Div(
            style={"display": "grid",
                   "gridTemplateColumns": "1fr 2fr",
                   "gap": "24px",
                   "marginTop": "24px",
                   "marginBottom": "12px"},
            children=[
                html.Div([
                    html.Label("Focus state",
                               style={"fontWeight": "bold",
                                      "display": "block",
                                      "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="state-dropdown",
                        options=[{"label": s, "value": s} for s in STATES],
                        value=DEFAULT_STATE,
                        clearable=False,
                    ),
                ]),
                html.Div([
                    html.Label("Peer group (multi-select)",
                               style={"fontWeight": "bold",
                                      "display": "block",
                                      "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="peer-dropdown",
                        options=[{"label": s, "value": s} for s in STATES],
                        value=DEFAULT_PEERS,
                        multi=True,
                    ),
                ]),
            ],
        ),

        html.Div(id="kpi-row", style={"display": "grid",
                                      "gridTemplateColumns": "repeat(4, 1fr)",
                                      "gap": "12px",
                                      "marginBottom": "24px"}),

        html.H3("Revenue trend over time", style={"marginTop": "28px"}),
        dcc.Graph(id="trend-chart"),

        html.Div(style={"display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginTop": "12px"},
                 children=[
                     html.Div([
                         html.H3("SOTR composition (latest year)"),
                         dcc.Graph(id="composition-chart"),
                     ]),
                     html.Div([
                         html.H3("Focus state vs peer average (latest year)"),
                         dcc.Graph(id="comparison-chart"),
                     ]),
                 ]),

        html.H3("Rankings across all metrics (latest year)",
                style={"marginTop": "28px"}),
        html.Div(id="ranking-table"),

        html.P(
            "Absolute rank is the state's position among all 28 states on "
            "raw ₹-Crore values. Per-capita rank uses Census 2011 "
            "population. Lower rank = better.",
            style={"color": "#666", "fontSize": "12px",
                   "marginTop": "16px"}),
    ],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def kpi_card(label: str, value: str, sub: str = "") -> html.Div:
    return html.Div(
        style={"background": "#F7F7F9", "borderRadius": "8px",
               "padding": "14px 16px", "borderLeft": f"4px solid {C_PRIMARY}"},
        children=[
            html.Div(label, style={"fontSize": "11px", "color": "#666",
                                   "textTransform": "uppercase",
                                   "letterSpacing": "0.5px"}),
            html.Div(value, style={"fontSize": "22px", "fontWeight": "600",
                                   "marginTop": "4px"}),
            html.Div(sub, style={"fontSize": "11px", "color": "#888",
                                 "marginTop": "2px"}),
        ],
    )


def fmt_crore(x: float) -> str:
    if pd.isna(x):
        return "—"
    if x >= 1_00_000:
        return f"₹{x / 100_000:.2f} L Cr"
    return f"₹{x:,.0f} Cr"


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
)
def render_kpis(state: str, peers: list[str]):
    peers = [p for p in (peers or []) if p != state]
    state_row = WIDE_LATEST.loc[state]
    total = state_row.get("Total Revenue Receipts")
    sotr = state_row.get("SOTR")
    share_ut = state_row.get("Share in Union Taxes")
    grants = state_row.get("Grants in Aid")

    own_rev = (sotr or 0) + (state_row.get("Non-Tax Revenue") or 0)
    central = (share_ut or 0) + (grants or 0)
    central_share = central / total * 100 if total else 0

    pop = POPULATION[state]
    total_pc = (total * 1e7 / pop) if total else 0

    return [
        kpi_card("Total Revenue Receipts",
                 fmt_crore(total),
                 f"₹{total_pc:,.0f} per capita"),
        kpi_card("SOTR",
                 fmt_crore(sotr),
                 f"{(sotr / total * 100):.1f}% of total" if total else "—"),
        kpi_card("Central transfers",
                 fmt_crore(central),
                 f"{central_share:.1f}% of revenue"),
        kpi_card("Own revenue share",
                 f"{(own_rev / total * 100):.1f}%" if total else "—",
                 f"Peers avg: {peer_own_share(peers):.1f}%"
                 if peers else "(add peers to compare)"),
    ]


def peer_own_share(peers: list[str]) -> float:
    if not peers:
        return 0
    shares = []
    for p in peers:
        if p not in WIDE_LATEST.index:
            continue
        row = WIDE_LATEST.loc[p]
        total = row.get("Total Revenue Receipts")
        own = (row.get("SOTR") or 0) + (row.get("Non-Tax Revenue") or 0)
        if total:
            shares.append(own / total * 100)
    return sum(shares) / len(shares) if shares else 0


@app.callback(
    Output("trend-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
)
def render_trend(state: str, peers: list[str]):
    peers = [p for p in (peers or []) if p != state]

    state_series = (df[(df["state"] == state) &
                       (df["metric"] == "Total Revenue Receipts")]
                    .sort_values("year"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_series["year"], y=state_series["value"],
        mode="lines+markers", name=state,
        line=dict(color=C_PRIMARY, width=3),
        marker=dict(size=8),
    ))

    if peers:
        peer_series = (df[(df["state"].isin(peers)) &
                          (df["metric"] == "Total Revenue Receipts")]
                       .groupby("year")["value"].mean().reset_index())
        fig.add_trace(go.Scatter(
            x=peer_series["year"], y=peer_series["value"],
            mode="lines+markers", name=f"Peer avg ({len(peers)})",
            line=dict(color=C_PEER_AVG, width=2, dash="dash"),
            marker=dict(size=6),
        ))

    national = (df[df["metric"] == "Total Revenue Receipts"]
                .groupby("year")["value"].mean().reset_index())
    fig.add_trace(go.Scatter(
        x=national["year"], y=national["value"],
        mode="lines", name="National avg",
        line=dict(color=C_NATIONAL, width=1.5, dash="dot"),
    ))

    fig.update_layout(
        xaxis_title="Fiscal year (start)",
        yaxis_title="Total Revenue Receipts (₹ Crore)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=40),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
    )
    return fig


@app.callback(
    Output("composition-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
)
def render_composition(state: str, peers: list[str]):
    peers = [p for p in (peers or []) if p != state]

    def shares(states: list[str]) -> pd.Series:
        rows = WIDE_LATEST.loc[states, SOTR_SUBS]
        totals = rows.sum(axis=1)
        return (rows.div(totals, axis=0) * 100).mean()

    cols = {state: shares([state])}
    if peers:
        cols["Peer avg"] = shares(peers)

    comp = pd.DataFrame(cols).T[SOTR_SUBS]

    fig = go.Figure()
    palette = {
        "SGST": "#4C72B0", "Sales/Trade Tax": "#DD8452",
        "Stamps & Registration": "#55A868", "State Excise": "#C44E52",
        "Motor Vehicle Tax": "#8172B3",
    }
    for sub in SOTR_SUBS:
        fig.add_trace(go.Bar(
            name=sub, x=comp.index, y=comp[sub],
            text=[f"{v:.0f}%" if v >= 3 else "" for v in comp[sub]],
            textposition="inside", textfont=dict(color="white"),
            marker_color=palette[sub],
        ))
    fig.update_layout(
        barmode="stack", yaxis_title="% of SOTR", yaxis_range=[0, 105],
        margin=dict(l=20, r=20, t=20, b=20), height=380,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
    )
    return fig


@app.callback(
    Output("comparison-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
)
def render_comparison(state: str, peers: list[str]):
    peers = [p for p in (peers or []) if p != state]
    metrics = [m for m in ALL_METRICS if m in WIDE_LATEST.columns]

    state_pop = POPULATION[state]
    state_pc = [(WIDE_LATEST.loc[state, m] * 1e7 / state_pop)
                for m in metrics]
    peer_pc = []
    for m in metrics:
        if not peers:
            peer_pc.append(0)
            continue
        vals = WIDE_LATEST.loc[peers, m]
        pops = WIDE_LATEST.loc[peers, "population"]
        peer_pc.append((vals * 1e7 / pops).mean())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=state, y=metrics, x=state_pc, orientation="h",
        marker_color=C_PRIMARY,
    ))
    if peers:
        fig.add_trace(go.Bar(
            name=f"Peer avg ({len(peers)})", y=metrics, x=peer_pc,
            orientation="h", marker_color=C_PEER_AVG, opacity=0.85,
        ))
    fig.update_layout(
        barmode="group", xaxis_title="₹ per capita",
        margin=dict(l=20, r=20, t=20, b=40), height=380,
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
    )
    return fig


@app.callback(
    Output("ranking-table", "children"),
    Input("state-dropdown", "value"),
    Input("peer-dropdown", "value"),
)
def render_ranking(state: str, peers: list[str]):
    peers = [p for p in (peers or []) if p != state]
    metrics = [m for m in ALL_METRICS if m in WIDE_LATEST.columns]
    n = len(WIDE_LATEST)

    rows = []
    for m in metrics:
        values = WIDE_LATEST[m].dropna()
        if state not in values.index:
            continue
        pc = values * 1e7 / WIDE_LATEST.loc[values.index, "population"]
        abs_rank = int(values.rank(ascending=False, method="min")[state])
        pc_rank = int(pc.rank(ascending=False, method="min")[state])
        state_val = values[state]

        peer_avg_val = (WIDE_LATEST.loc[peers, m].mean()
                        if peers and m in WIDE_LATEST.columns else None)

        rows.append({
            "Metric": m,
            "Value": fmt_crore(state_val),
            f"Rank (abs / {n})": abs_rank,
            f"Rank (per-capita / {n})": pc_rank,
            "Peer avg": fmt_crore(peer_avg_val) if peer_avg_val else "—",
            "vs peer avg": (f"{((state_val - peer_avg_val) / peer_avg_val * 100):+.0f}%"
                            if peer_avg_val else "—"),
        })

    header = html.Tr([html.Th(c, style={"padding": "8px 12px",
                                        "background": "#F7F7F9",
                                        "textAlign": "left",
                                        "borderBottom": "2px solid #DDD",
                                        "fontSize": "12px"})
                      for c in rows[0].keys()])
    body = []
    for r in rows:
        cells = []
        for k, v in r.items():
            style = {"padding": "8px 12px",
                     "borderBottom": "1px solid #EEE",
                     "fontSize": "13px"}
            # Color rank columns
            if "Rank" in k and isinstance(v, int):
                if v <= 5:
                    style["color"] = "#2CA02C"
                    style["fontWeight"] = "600"
                elif v >= 20:
                    style["color"] = C_PRIMARY
                    style["fontWeight"] = "600"
            cells.append(html.Td(v, style=style))
        body.append(html.Tr(cells))

    return html.Table(
        [html.Thead(header), html.Tbody(body)],
        style={"width": "100%", "borderCollapse": "collapse",
               "fontFamily": "system-ui"},
    )


# ---------------------------------------------------------------------------
# Expose the underlying Flask instance for production WSGI servers like
# gunicorn. Render will run: `gunicorn app:server`.
server = app.server


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    if host == "127.0.0.1":
        print(f"\nOpen http://localhost:{port} in your browser\n")
    app.run(host=host, port=port, debug=False)
