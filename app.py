
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PULSEGROWTH — MARKETING INTELLIGENCE
# ============================================================

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "processed" / "pulsegrowth_deploy.duckdb"
DECISION_PATH = ROOT / "data" / "processed" / "campaign_decision_table.csv"

NAVY = "#101522"
PANEL = "#191F30"
LIME = "#C7F36B"
CYAN = "#61D9F7"
PURPLE = "#A99BFF"
MUTED = "#9CA8BC"
WHITE = "#F4F7FC"
RED = "#FF7F8B"
GRID = "rgba(156,168,188,0.16)"

st.set_page_config(
    page_title="PulseGrowth | Marketing Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# VISUAL DESIGN
# ============================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(ellipse at 15% 0%, rgba(97,217,247,.07), transparent 32%),
            radial-gradient(ellipse at 90% 8%, rgba(199,243,107,.055), transparent 28%),
            {NAVY};
        color: {WHITE};
    }}

    [data-testid="stHeader"] {{
        background: rgba(16,21,34,.88);
    }}

    [data-testid="stSidebar"] {{
        background: #0D111C;
        border-right: 1px solid rgba(255,255,255,.07);
    }}

    [data-testid="stSidebar"] * {{
        color: {WHITE};
    }}

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -.035em;
    }}

    .brand-lockup {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }}

    .brand-mark {{
        width: 43px;
        height: 43px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #111722;
        font-size: 25px;
        font-weight: 900;
        background: {LIME};
    }}

    .brand-name {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: -.8px;
    }}

    .brand-subtitle {{
        color: {MUTED};
        font-size: 10px;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }}

    .eyebrow {{
        color: {LIME};
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.3px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .hero {{
        background: linear-gradient(115deg, #202A3D 0%, #171E2D 58%, #1B2A2C 100%);
        border: 1px solid rgba(199,243,107,.17);
        border-radius: 23px;
        padding: 29px 32px;
        margin-bottom: 24px;
    }}

    .hero h1 {{
        font-size: clamp(30px, 4vw, 44px);
        line-height: 1.1;
        margin: 5px 0 13px;
        color: {WHITE};
    }}

    .hero p {{
        color: #B6C2D4;
        max-width: 760px;
        font-size: 14px;
        line-height: 1.7;
        margin: 0;
    }}

    .section-heading {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 21px;
        font-weight: 600;
        margin-top: 12px;
        margin-bottom: 4px;
    }}

    .section-caption {{
        color: {MUTED};
        font-size: 13px;
        margin-bottom: 15px;
    }}

    .metric-card {{
        background: linear-gradient(145deg, #1D2638, #171E2C);
        border: 1px solid rgba(255,255,255,.075);
        border-radius: 17px;
        padding: 19px 20px;
        min-height: 122px;
        box-shadow: 0 8px 28px rgba(0,0,0,.10);
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 12px;
        margin-bottom: 11px;
    }}

    .metric-value {{
        color: {WHITE};
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(22px, 2.2vw, 30px);
        font-weight: 700;
        letter-spacing: -1px;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }}

    .metric-note {{
        color: {LIME};
        font-size: 11px;
        margin-top: 9px;
    }}

    .pill {{
        display: inline-block;
        padding: 5px 10px;
        border-radius: 100px;
        color: {LIME};
        background: rgba(199,243,107,.09);
        border: 1px solid rgba(199,243,107,.19);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
    }}

    .callout {{
        background: rgba(199,243,107,.06);
        border-left: 3px solid {LIME};
        border-radius: 0 10px 10px 0;
        padding: 13px 16px;
        color: #DCE5F1;
        font-size: 13px;
        line-height: 1.65;
        margin: 10px 0 18px;
    }}

    .small-muted {{
        color: {MUTED};
        font-size: 11px;
        line-height: 1.6;
    }}

    .stButton > button {{
        border-radius: 10px;
        border: 1px solid rgba(199,243,107,.4);
        background: {LIME};
        color: #111722;
        font-weight: 700;
    }}

    div[data-baseweb="select"] > div {{
        background: #1B2333;
        border-color: rgba(255,255,255,.12);
    }}

    hr {{
        border-color: rgba(255,255,255,.09);
    }}

    footer {{
        visibility: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=60)
def load_campaign_mart():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB warehouse not found: {DB_PATH}"
        )

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        return con.execute(
            "SELECT * FROM analytics.mart_campaign_performance"
        ).df()
    finally:
        con.close()


@st.cache_data(ttl=60)
def load_decision_table():
    if DECISION_PATH.exists():
        df = pd.read_csv(DECISION_PATH)
        if not df.empty:
            return df

    from src.analytics.build_campaign_decision_table import (
        build_decision_table,
    )

    return build_decision_table(load_campaign_mart())


@st.cache_data(ttl=60)
def load_crm_results():
    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        return con.execute(
            """
            SELECT *
            FROM analytics.mart_crm_experiment_results
            ORDER BY segment, variant
            """
        ).df()
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()


@st.cache_data(ttl=60)
def load_optional_table(table_name):
    allowed = {
        "mart_cohort_retention",
        "mart_daily_campaign_performance",
        "fct_geo_experiments",
    }

    if table_name not in allowed:
        return pd.DataFrame()

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        return con.execute(
            f"SELECT * FROM main.{table_name}"
        ).df()
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()


try:
    raw_campaigns = load_campaign_mart()
    decision_all = load_decision_table()
    crm_all = load_crm_results()
    retention_all = load_optional_table("mart_cohort_retention")
    daily_all = load_optional_table("mart_daily_campaign_performance")
    geo_all = load_optional_table("fct_geo_experiments")
except Exception as exc:
    st.error(f"Unable to load PulseGrowth data: {exc}")
    st.info(
        "Generate the synthetic data, build the DuckDB warehouse, "
        "run dbt, and create the campaign decision table first."
    )
    st.stop()


# ============================================================
# SHARED HELPERS
# ============================================================

def col_name(df, candidates):
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def money(value):
    return "—" if pd.isna(value) else f"€{value:,.0f}"


def money_decimal(value):
    return "—" if pd.isna(value) else f"€{value:,.2f}"


def number(value):
    return "—" if pd.isna(value) else f"{value:,.0f}"


def percent(value):
    return "—" if pd.isna(value) else f"{value:.1%}"


def ratio(value):
    return "—" if pd.isna(value) else f"{value:.2f}x"


def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def heading(title, caption=None):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True,
    )
    if caption:
        st.markdown(
            f'<div class="section-caption">{caption}</div>',
            unsafe_allow_html=True,
        )


def chart_layout(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=WHITE, size=11),
        margin=dict(l=12, r=12, t=30, b=12),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
    )
    return fig


def filtered_decisions(df, channels, campaigns):
    result = df.copy()

    if "channel" in result.columns:
        result = result[result["channel"].isin(channels)]

    campaign_col = col_name(
        result, ["campaign_name", "campaign_id"]
    )
    if campaign_col:
        result = result[result[campaign_col].isin(campaigns)]

    return result.copy()


def safe_sum(df, column):
    if column not in df.columns:
        return 0.0
    return pd.to_numeric(df[column], errors="coerce").sum()


def calculate_aggregate_metrics(df):
    spend = safe_sum(df, "spend_eur")
    revenue = safe_sum(df, "attributed_revenue_eur")
    installs = safe_sum(df, "attributed_installs")
    payers = safe_sum(df, "paying_customers")
    clicks = safe_sum(df, "clicks")
    impressions = safe_sum(df, "impressions")

    return {
        "spend": spend,
        "revenue": revenue,
        "installs": installs,
        "payers": payers,
        "clicks": clicks,
        "impressions": impressions,
        "roas": revenue / spend if spend > 0 else np.nan,
        "cpi": spend / installs if installs > 0 else np.nan,
        "cac": spend / payers if payers > 0 else np.nan,
        "ctr": clicks / impressions if impressions > 0 else np.nan,
        "conversion": payers / installs if installs > 0 else np.nan,
    }


def weighted_rate(df, retained_column, eligible_column):
    eligible = pd.to_numeric(
        df[eligible_column], errors="coerce"
    )
    retained = pd.to_numeric(
        df[retained_column], errors="coerce"
    )

    denominator = eligible.sum(min_count=1)
    numerator = retained.sum(min_count=1)

    if pd.isna(denominator) or denominator <= 0:
        return np.nan

    return numerator / denominator


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-mark">ϟ</div>
            <div>
                <div class="brand-name">PulseGrowth</div>
                <div class="brand-subtitle">Marketing Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="eyebrow">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        [
            "Executive Overview",
            "Campaign Decision Centre",
            "Cohort & Retention",
            "Experimentation Lab",
            "Budget Simulator",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div class="eyebrow">CAMPAIGN FILTERS</div>',
        unsafe_allow_html=True,
    )

    all_channels = sorted(
        decision_all["channel"].dropna().astype(str).unique()
    )
    selected_channels = st.multiselect(
        "Marketing channels",
        all_channels,
        default=all_channels,
    )

    campaign_column = col_name(
        decision_all, ["campaign_name", "campaign_id"]
    )
    campaign_options = (
        sorted(
            decision_all[campaign_column]
            .dropna().astype(str).unique()
        )
        if campaign_column
        else []
    )

    selected_campaigns = st.multiselect(
        "Campaigns",
        campaign_options,
        default=campaign_options,
    )

    st.divider()

    st.markdown(
        """
        <div class="small-muted">
            <span class="pill">PORTFOLIO PROTOTYPE</span><br><br>
            Python · SQL · DuckDB · dbt · Streamlit<br><br>
            Designed for performance marketing in consumer health-tech.
        </div>
        """,
        unsafe_allow_html=True,
    )


decision = filtered_decisions(
    decision_all, selected_channels, selected_campaigns
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">GROWTH PERFORMANCE INTELLIGENCE</div>
        <h1>Turn marketing signals<br>into smarter decisions.</h1>
        <p>
            Explore acquisition efficiency, customer retention and
            experimentation. Understand where attributed revenue comes from,
            which campaigns need investigation, and where stronger evidence
            is needed before scaling.
        </p>
        <br>
        <span class="pill">SYNTHETIC DATA · PORTFOLIO DEMONSTRATION</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":
    if decision.empty:
        st.warning("No campaigns match the current filters.")
        st.stop()

    st.markdown(
        '<div class="eyebrow">01 / THE BIG PICTURE</div>',
        unsafe_allow_html=True,
    )
    heading(
        "Executive overview",
        "A high-level view of acquisition performance for selected campaigns.",
    )

    metrics = calculate_aggregate_metrics(decision)

    row1 = st.columns(4)
    cards1 = [
        ("AD SPEND", money(metrics["spend"]), "Selected campaigns"),
        ("ATTRIBUTED INSTALLS", number(metrics["installs"]),
         "Campaign-linked installs"),
        ("PAYING CUSTOMERS", number(metrics["payers"]),
         "Distinct attributed payers"),
        ("ATTRIBUTED ROAS", ratio(metrics["roas"]),
         "Initial revenue / spend"),
    ]

    for column, card in zip(row1, cards1):
        with column:
            metric_card(*card)

    row2 = st.columns(4)
    cards2 = [
        ("BLENDED CPI", money_decimal(metrics["cpi"]),
         "Spend / attributed installs"),
        ("BLENDED CAC", money_decimal(metrics["cac"]),
         "Spend / attributed payers"),
        ("CLICK-THROUGH RATE", percent(metrics["ctr"]),
         "Clicks / impressions"),
        ("INSTALL → PAYER", percent(metrics["conversion"]),
         "Payers / attributed installs"),
    ]

    for column, card in zip(row2, cards2):
        with column:
            metric_card(*card)

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        heading(
            "Campaign efficiency map",
            "Bubble size represents spend. Compare CPI with attributed ROAS.",
        )

        scatter = decision.dropna(
            subset=["cpi_eur", "attributed_roas"]
        )

        if not scatter.empty:
            fig = px.scatter(
                scatter,
                x="cpi_eur",
                y="attributed_roas",
                size="spend_eur",
                color="channel",
                hover_name="campaign_name",
                color_discrete_sequence=[LIME, CYAN, PURPLE, RED],
                labels={
                    "cpi_eur": "Cost per install (€)",
                    "attributed_roas": "Attributed ROAS (x)",
                    "channel": "Channel",
                },
            )
            fig.add_hline(
                y=1.0,
                line_dash="dash",
                line_color=MUTED,
                annotation_text="1.0x attributed ROAS",
            )
            st.plotly_chart(
                chart_layout(fig, 410),
                use_container_width=True,
            )
        else:
            st.info("No valid CPI and ROAS pairs are available.")

    with right:
        heading(
            "Channel contribution",
            "Spend compared with attributed initial subscription revenue.",
        )

        channel_data = (
            decision.groupby("channel", as_index=False)
            .agg(
                spend_eur=("spend_eur", "sum"),
                attributed_revenue_eur=(
                    "attributed_revenue_eur", "sum"
                ),
            )
        )

        fig = go.Figure()
        fig.add_bar(
            x=channel_data["channel"],
            y=channel_data["spend_eur"],
            name="Spend",
            marker_color="#46536B",
        )
        fig.add_bar(
            x=channel_data["channel"],
            y=channel_data["attributed_revenue_eur"],
            name="Attributed revenue",
            marker_color=LIME,
        )
        fig.update_layout(
            barmode="group",
            yaxis_title="EUR (€)",
            xaxis_title="",
        )
        st.plotly_chart(
            chart_layout(fig, 410),
            use_container_width=True,
        )

    channel_data["roas"] = (
        channel_data["attributed_revenue_eur"]
        / channel_data["spend_eur"].replace(0, np.nan)
    )

    if not channel_data.empty:
        best = channel_data.loc[channel_data["roas"].idxmax()]
        worst = channel_data.loc[channel_data["roas"].idxmin()]

        st.markdown(
            f"""
            <div class="callout">
                <strong>Highest attributed ROAS:</strong>
                {best['channel']} at {best['roas']:.2f}x.<br>
                <strong>Lowest attributed ROAS:</strong>
                {worst['channel']} at {worst['roas']:.2f}x.<br><br>
                Use these as investigation priorities, not proof of
                incremental performance. Revenue covers initial subscription
                transactions only.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE 2 — CAMPAIGN DECISION CENTRE
# ============================================================

elif page == "Campaign Decision Centre":
    if decision.empty:
        st.warning("No campaigns match the current filters.")
        st.stop()

    st.markdown(
        '<div class="eyebrow">02 / ACQUISITION PERFORMANCE</div>',
        unsafe_allow_html=True,
    )
    heading(
        "Campaign decision centre",
        "Compare campaign economics and prioritise investigation.",
    )

    table_columns = [
        "performance_rank",
        "campaign_name",
        "channel",
        "spend_eur",
        "attributed_installs",
        "cpi_eur",
        "paying_customers",
        "cac_eur",
        "click_through_rate",
        "attributed_roas",
        "recommendation",
    ]
    table_columns = [
        c for c in table_columns if c in decision.columns
    ]
    table = decision[table_columns].copy()

    formatters = {}
    for column in ["spend_eur", "cpi_eur", "cac_eur"]:
        if column in table.columns:
            formatters[column] = (
                lambda value: f"€{value:,.2f}"
                if pd.notna(value) else "—"
            )

    if "click_through_rate" in table.columns:
        formatters["click_through_rate"] = (
            lambda value: f"{value:.2%}"
            if pd.notna(value) else "—"
        )

    if "attributed_roas" in table.columns:
        formatters["attributed_roas"] = (
            lambda value: f"{value:.2f}x"
            if pd.notna(value) else "—"
        )

    st.dataframe(
        table.style.format(formatters),
        use_container_width=True,
        hide_index=True,
        height=460,
    )

    st.download_button(
        "↓ Download filtered campaign table",
        data=decision.to_csv(index=False).encode("utf-8"),
        file_name="pulsegrowth_campaign_decisions.csv",
        mime="text/csv",
    )

    left, right = st.columns(2, gap="large")

    with left:
        heading("ROAS leaderboard", "Attributed initial revenue / spend.")
        rank_data = decision.sort_values(
            "attributed_roas", ascending=True
        )
        fig = px.bar(
            rank_data,
            x="attributed_roas",
            y="campaign_name",
            color="channel",
            orientation="h",
            labels={
                "attributed_roas": "Attributed ROAS (x)",
                "campaign_name": "",
            },
            color_discrete_sequence=[LIME, CYAN, PURPLE, RED],
        )
        fig.add_vline(x=1, line_dash="dash", line_color=MUTED)
        st.plotly_chart(
            chart_layout(fig, 500),
            use_container_width=True,
        )

    with right:
        heading("Acquisition cost by campaign", "CAC in euros.")
        cac_data = decision.dropna(
            subset=["cac_eur"]
        ).sort_values("cac_eur", ascending=True)

        if not cac_data.empty:
            fig = px.bar(
                cac_data,
                x="cac_eur",
                y="campaign_name",
                color="channel",
                orientation="h",
                labels={"cac_eur": "CAC (€)", "campaign_name": ""},
                color_discrete_sequence=[CYAN, LIME, PURPLE, RED],
            )
            st.plotly_chart(
                chart_layout(fig, 500),
                use_container_width=True,
            )
        else:
            st.info("No valid CAC values are available.")

    st.markdown(
        """
        <div class="callout">
            A low CAC or high attributed ROAS is not sufficient evidence
            to scale. Validate retention, margin, attribution coverage and
            incremental lift first.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 3 — COHORT & RETENTION
# ============================================================

elif page == "Cohort & Retention":
    st.markdown(
        '<div class="eyebrow">03 / CUSTOMER QUALITY</div>',
        unsafe_allow_html=True,
    )
    heading(
        "Cohort & retention intelligence",
        "Measure user return behaviour and compare retention across channels.",
    )

    if retention_all.empty:
        st.warning(
            "The cohort retention mart is unavailable. "
            "Check main.mart_cohort_retention in DuckDB."
        )
        st.stop()

    required_columns = {
        "cohort_month",
        "channel",
        "cohort_users",
        "d1_eligible_users",
        "d1_retained_users",
        "d7_eligible_users",
        "d7_retained_users",
        "d30_eligible_users",
        "d30_retained_users",
    }

    missing_columns = required_columns - set(retention_all.columns)

    if missing_columns:
        st.error(
            "Missing retention columns: "
            + ", ".join(sorted(missing_columns))
        )
        st.stop()

    retention = retention_all.copy()
    retention["cohort_month"] = pd.to_datetime(
        retention["cohort_month"], errors="coerce"
    )

    count_columns = [
        "cohort_users",
        "d1_eligible_users",
        "d1_retained_users",
        "d7_eligible_users",
        "d7_retained_users",
        "d30_eligible_users",
        "d30_retained_users",
    ]

    for column in count_columns:
        retention[column] = pd.to_numeric(
            retention[column], errors="coerce"
        )

    retention = retention.dropna(
        subset=["cohort_month", "channel"]
    )

    # The retention mart is channel/cohort based, not campaign based.
    if selected_channels:
        retention = retention[
            retention["channel"].isin(selected_channels)
        ]
    else:
        retention = retention.iloc[0:0]

    if retention.empty:
        st.warning("No retention cohorts match the selected channels.")
        st.stop()

    # Recalculate rates from counts rather than averaging percentages.
    for day in ["d1", "d7", "d30"]:
        retention[f"{day}_retention_rate"] = (
            retention[f"{day}_retained_users"]
            / retention[f"{day}_eligible_users"].replace(0, np.nan)
        )

    st.markdown(
        """
        <div class="callout">
            <strong>How to read retention:</strong> D1, D7 and D30 represent
            users returning on the corresponding day after installation.
            Each rate uses the users eligible for that measurement window.
            Recent cohorts may not yet be mature enough for D30.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Weighted summary across all selected cohorts.
    d1_rate = weighted_rate(
        retention, "d1_retained_users", "d1_eligible_users"
    )
    d7_rate = weighted_rate(
        retention, "d7_retained_users", "d7_eligible_users"
    )
    d30_rate = weighted_rate(
        retention, "d30_retained_users", "d30_eligible_users"
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        metric_card(
            "D1 RETENTION",
            percent(d1_rate),
            f"{number(retention['d1_retained_users'].sum())} retained",
        )
    with k2:
        metric_card(
            "D7 RETENTION",
            percent(d7_rate),
            f"{number(retention['d7_retained_users'].sum())} retained",
        )
    with k3:
        metric_card(
            "D30 RETENTION",
            percent(d30_rate),
            f"{number(retention['d30_retained_users'].sum())} retained",
        )
    with k4:
        metric_card(
            "COHORT USERS",
            number(retention["cohort_users"].sum()),
            f"{retention['cohort_month'].nunique()} cohort months",
        )

    # Cohort-month counts and rates.
    cohort_totals = (
        retention.groupby("cohort_month", as_index=False)
        .agg(
            cohort_users=("cohort_users", "sum"),
            d1_eligible_users=("d1_eligible_users", "sum"),
            d1_retained_users=("d1_retained_users", "sum"),
            d7_eligible_users=("d7_eligible_users", "sum"),
            d7_retained_users=("d7_retained_users", "sum"),
            d30_eligible_users=("d30_eligible_users", "sum"),
            d30_retained_users=("d30_retained_users", "sum"),
        )
        .sort_values("cohort_month")
    )

    for day in ["d1", "d7", "d30"]:
        cohort_totals[f"{day}_retention_rate"] = (
            cohort_totals[f"{day}_retained_users"]
            / cohort_totals[f"{day}_eligible_users"].replace(0, np.nan)
        )

    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        heading(
            "Retention by cohort month",
            "Compare D1, D7 and D30 return rates over time.",
        )

        selected_day = st.selectbox(
            "Retention measurement",
            ["D1", "D7", "D30"],
            index=1,
        )
        rate_column = f"{selected_day.lower()}_retention_rate"

        fig = px.line(
            cohort_totals,
            x="cohort_month",
            y=rate_column,
            markers=True,
            custom_data=["cohort_users"],
            labels={
                "cohort_month": "Install cohort",
                rate_column: f"{selected_day} retention",
            },
        )
        fig.update_traces(
            line=dict(color=LIME, width=3),
            marker=dict(size=8, color=LIME),
            hovertemplate=(
                "Cohort: %{x|%b %Y}<br>"
                "Retention: %{y:.1%}<br>"
                "Cohort users: %{customdata[0]:,.0f}"
                "<extra></extra>"
            ),
        )
        fig.update_yaxes(tickformat=".0%", rangemode="tozero")
        st.plotly_chart(
            chart_layout(fig, 390),
            use_container_width=True,
        )

    with right:
        heading(
            "Channel comparison",
            "Weighted retention rate for the selected measurement day.",
        )

        channel_totals = (
            retention.groupby("channel", as_index=False)
            .agg(
                d1_eligible_users=("d1_eligible_users", "sum"),
                d1_retained_users=("d1_retained_users", "sum"),
                d7_eligible_users=("d7_eligible_users", "sum"),
                d7_retained_users=("d7_retained_users", "sum"),
                d30_eligible_users=("d30_eligible_users", "sum"),
                d30_retained_users=("d30_retained_users", "sum"),
            )
        )

        for day in ["d1", "d7", "d30"]:
            channel_totals[f"{day}_retention_rate"] = (
                channel_totals[f"{day}_retained_users"]
                / channel_totals[f"{day}_eligible_users"].replace(
                    0, np.nan
                )
            )

        channel_day = st.selectbox(
            "Compare channels on",
            ["D1", "D7", "D30"],
            index=1,
            key="retention_channel_day",
        )
        channel_rate_column = (
            f"{channel_day.lower()}_retention_rate"
        )

        channel_chart = channel_totals.sort_values(
            channel_rate_column, ascending=True
        )

        fig = px.bar(
            channel_chart,
            x=channel_rate_column,
            y="channel",
            orientation="h",
            labels={
                channel_rate_column: f"{channel_day} retention",
                "channel": "",
            },
            text=channel_chart[channel_rate_column].map(
                lambda value: (
                    f"{value:.1%}" if pd.notna(value) else "N/A"
                )
            ),
        )
        fig.update_traces(
            marker_color=CYAN,
            textposition="outside",
            cliponaxis=False,
        )
        fig.update_xaxes(tickformat=".0%", rangemode="tozero")
        st.plotly_chart(
            chart_layout(fig, 390),
            use_container_width=True,
        )

    # Count and eligibility diagnostics.
    heading(
        "Cohort data quality",
        "Check that retained counts do not exceed eligible counts and that eligibility is plausible.",
    )

    audit = retention.copy()

    for day in ["d1", "d7", "d30"]:
        eligible_col = f"{day}_eligible_users"
        retained_col = f"{day}_retained_users"

        audit[f"{day}_eligibility_pct"] = (
            audit[eligible_col]
            / audit["cohort_users"].replace(0, np.nan)
        )

        audit[f"{day}_count_check"] = np.where(
            audit[eligible_col].isna()
            | audit[retained_col].isna()
            | (audit[eligible_col] < 0)
            | (audit[retained_col] < 0)
            | (audit[retained_col] > audit[eligible_col])
            | (audit[eligible_col] > audit["cohort_users"]),
            "CHECK",
            "OK",
        )

    audit_columns = [
        "cohort_month",
        "channel",
        "cohort_users",
        "d1_eligible_users",
        "d1_retained_users",
        "d1_retention_rate",
        "d1_count_check",
        "d7_eligible_users",
        "d7_retained_users",
        "d7_retention_rate",
        "d7_count_check",
        "d30_eligible_users",
        "d30_retained_users",
        "d30_retention_rate",
        "d30_count_check",
    ]

    st.dataframe(
        audit[audit_columns].sort_values(
            ["cohort_month", "channel"],
            ascending=[False, True],
        ).style.format(
            {
                "d1_retention_rate": "{:.2%}",
                "d7_retention_rate": "{:.2%}",
                "d30_retention_rate": "{:.2%}",
            },
            na_rep="N/A",
        ),
        use_container_width=True,
        hide_index=True,
        height=380,
    )

    # Flag complete-looking eligibility counts for a maturity audit.
    full_d30_eligibility = (
        audit["d30_eligible_users"].eq(audit["cohort_users"])
    ).sum()

    st.info(
        f"{full_d30_eligibility:,} selected channel-cohort rows have "
        "D30-eligible counts equal to their full cohort size. This may be "
        "valid for mature cohorts, but the cohort-level mart alone cannot "
        "prove individual-user maturity. Verify the warehouse SQL against "
        "each user's install date and the observation cutoff before using "
        "D30 as a final performance metric."
    )

    st.caption(
        "The checks identify invalid counts but do not independently prove "
        "cohort maturity. All data in this portfolio prototype is synthetic."
    )


# ============================================================
# PAGE 4 — EXPERIMENTATION LAB
# ============================================================

elif page == "Experimentation Lab":
    st.markdown(
        '<div class="eyebrow">04 / CAUSAL LEARNING</div>',
        unsafe_allow_html=True,
    )
    heading(
        "Experimentation lab",
        "Separate attributed performance from evidence generated by controlled tests.",
    )

    if crm_all.empty:
        st.warning(
            "CRM experiment results are unavailable. Run the dbt CRM mart first."
        )
    else:
        segment_col = "segment"
        variant_col = "variant"
        rate_col = "conversion_rate"

        overall = crm_all[
            crm_all[segment_col].astype(str) == "ALL_SEGMENTS"
        ]

        control = overall[
            overall[variant_col].astype(str).str.lower() == "control"
        ]
        treatment = overall[
            overall[variant_col].astype(str).str.lower() == "treatment"
        ]

        if not control.empty and not treatment.empty:
            control_rate = float(control.iloc[0][rate_col])
            treatment_rate = float(treatment.iloc[0][rate_col])
            lift = treatment_rate - control_rate
            relative_lift = (
                lift / control_rate if control_rate > 0 else np.nan
            )

            a, b, c = st.columns(3)
            with a:
                metric_card(
                    "CONTROL CONVERSION",
                    percent(control_rate),
                    "Synthetic experiment",
                )
            with b:
                metric_card(
                    "TREATMENT CONVERSION",
                    percent(treatment_rate),
                    "Synthetic experiment",
                )
            with c:
                metric_card(
                    "ABSOLUTE LIFT",
                    f"{lift * 100:+.2f} pp",
                    f"Relative lift: {relative_lift:.1%}"
                    if pd.notna(relative_lift)
                    else "Relative lift unavailable",
                )

        segment_data = crm_all[
            crm_all[segment_col].astype(str) != "ALL_SEGMENTS"
        ].copy()

        heading(
            "Conversion rate by segment",
            "Control versus treatment conversion rates.",
        )

        if not segment_data.empty:
            fig = px.bar(
                segment_data,
                x=segment_col,
                y=rate_col,
                color=variant_col,
                barmode="group",
                labels={
                    segment_col: "User segment",
                    rate_col: "Conversion rate",
                    variant_col: "Variant",
                },
                color_discrete_map={
                    "control": CYAN,
                    "treatment": LIME,
                },
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(
                chart_layout(fig, 390),
                use_container_width=True,
            )

        st.dataframe(
            crm_all,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    heading("Geo-experiment data")

    if geo_all.empty:
        st.info("Geo-experiment source data is unavailable.")
    else:
        st.markdown(
            """
            <div class="callout">
                Geo-experiment data is synthetic. Before claiming incremental
                lift, assess pre-period comparability, treatment assignment,
                timing and potential confounding.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(
            geo_all.head(1000),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "The data generator deliberately introduces a CRM treatment effect. "
        "Results validate the analytical workflow, not real campaign efficacy."
    )


# ============================================================
# PAGE 5 — BUDGET SIMULATOR
# ============================================================

elif page == "Budget Simulator":
    st.markdown(
        '<div class="eyebrow">05 / SCENARIO PLANNING</div>',
        unsafe_allow_html=True,
    )
    heading(
        "Budget allocation simulator",
        "Explore a hypothetical budget shift using historical attributed ROAS.",
    )

    st.markdown(
        """
        <div class="callout">
            <strong>Scenario, not forecast:</strong> this tool assumes historical
            attributed ROAS remains constant after budget changes. Real campaigns
            can have diminishing returns, auction effects, audience saturation
            and changing customer quality.
        </div>
        """,
        unsafe_allow_html=True,
    )

    required = {
        "campaign_id",
        "campaign_name",
        "spend_eur",
        "attributed_revenue_eur",
        "attributed_roas",
    }

    if not required.issubset(decision.columns):
        st.warning(
            "The decision table is missing columns required for the simulator."
        )
    else:
        valid = decision.dropna(
            subset=["spend_eur", "attributed_revenue_eur"]
        ).copy()
        valid = valid[valid["spend_eur"] > 0]

        if len(valid) < 2:
            st.warning(
                "At least two campaigns with positive spend are required."
            )
        else:
            shift_pct = st.slider(
                "Budget shifted from lowest-ROAS campaigns",
                min_value=0,
                max_value=30,
                value=10,
                step=5,
                format="%d%%",
            )

            quartile_count = max(1, len(valid) // 4)
            sorted_campaigns = valid.sort_values(
                "attributed_roas", ascending=True
            )
            donors = sorted_campaigns.head(quartile_count)
            receivers = sorted_campaigns.tail(quartile_count)

            if set(donors["campaign_id"]) & set(receivers["campaign_id"]):
                st.warning("Too few distinct campaigns for this scenario.")
            else:
                total_spend = valid["spend_eur"].sum()
                transfer = total_spend * shift_pct / 100

                donor_spend = donors["spend_eur"].sum()
                receiver_spend = receivers["spend_eur"].sum()

                donor_roas = (
                    donors["attributed_revenue_eur"].sum() / donor_spend
                    if donor_spend > 0 else np.nan
                )
                receiver_roas = (
                    receivers["attributed_revenue_eur"].sum()
                    / receiver_spend
                    if receiver_spend > 0 else np.nan
                )

                baseline_revenue = valid[
                    "attributed_revenue_eur"
                ].sum()

                revenue_delta = (
                    transfer * (receiver_roas - donor_roas)
                    if pd.notna(receiver_roas)
                    and pd.notna(donor_roas)
                    else np.nan
                )

                scenario_revenue = (
                    baseline_revenue + revenue_delta
                    if pd.notna(revenue_delta)
                    else np.nan
                )

                a, b, c = st.columns(3)
                with a:
                    metric_card(
                        "TOTAL BUDGET",
                        money(total_spend),
                        "Selected campaign spend",
                    )
                with b:
                    metric_card(
                        "HYPOTHETICAL TRANSFER",
                        money(transfer),
                        f"{shift_pct}% of selected spend",
                    )
                with c:
                    metric_card(
                        "MODELLED REVENUE CHANGE",
                        money(revenue_delta),
                        "Constant-ROAS assumption",
                    )

                assumptions = pd.DataFrame(
                    [
                        {
                            "Group": "Budget donors",
                            "Campaigns": ", ".join(
                                donors["campaign_name"].astype(str)
                            ),
                            "Historical attributed ROAS": ratio(donor_roas),
                        },
                        {
                            "Group": "Budget recipients",
                            "Campaigns": ", ".join(
                                receivers["campaign_name"].astype(str)
                            ),
                            "Historical attributed ROAS": ratio(receiver_roas),
                        },
                    ]
                )

                heading("Scenario assumptions")
                st.dataframe(
                    assumptions,
                    use_container_width=True,
                    hide_index=True,
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            MODELLED ATTRIBUTED INITIAL REVENUE
                        </div>
                        <div class="metric-value">
                            {money(scenario_revenue)}
                        </div>
                        <div class="metric-note">
                            Baseline: {money(baseline_revenue)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.caption(
        "This simplified what-if calculation is not an MMM model, causal "
        "estimate or reliable prediction of future revenue."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    f"""
    <div style="display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;">
        <div>
            <span style="font-family:'Space Grotesk';font-weight:700;color:{WHITE};">
                PulseGrowth
            </span>
            <span style="color:{MUTED};font-size:12px;">
                &nbsp; Marketing Intelligence Platform
            </span>
        </div>
        <div class="small-muted">
            Portfolio prototype · Synthetic data · Python · DuckDB · dbt · Streamlit
        </div>
    </div>
    <p class="small-muted" style="margin-top:12px;">
        No live advertising-platform integrations or real customer records are used.
        Attributed revenue is not equivalent to incremental revenue, profit or lifetime value.
    </p>
    """,
    unsafe_allow_html=True,
)
