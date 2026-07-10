"""
Amazon Sales Analysis — Professional Analytics Dashboard
==========================================================
B.Tech Data Science Project

Run with:  streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import (
    MONTH_ORDER,
    WEEKDAY_ORDER,
    add_state_clean,
    compute_kpis,
    fmt_inr,
    fmt_pct,
    iqr_bounds,
    load_and_prepare,
)

# --------------------------------------------------------------------------
# PROJECT / STUDENT DETAILS — edit these for your own submission
# --------------------------------------------------------------------------
STUDENT_NAME = "Gaurvi Thakur"
COLLEGE_NAME = "DAV Institute of Engineering and Technology, Jalandhar"
BRANCH_NAME = "B.Tech — Data Science"
CSV_PATH = "Amazon_Sale_Report.csv"

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Amazon Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK_BG = "#0F1420"
CARD_BG = "#161D2C"
BORDER = "#2A3348"
TEXT = "#E7ECF5"
TEXT_MUTED = "#93A0B8"
AMBER = "#F5A524"
AMBER_DIM = "#B9781A"
SKY = "#38BDF8"

TEMPLATE = "plotly_dark"
ORANGE_SEQ = px.colors.sequential.Oranges[2:]
MAP_SCALE = "Oranges"

CUSTOM_CSS = f"""
<style>
    .main > div {{ padding-top: 1rem; }}
    #MainMenu, footer {{visibility: hidden;}}

    /* Dark slate theme, forced regardless of browser/OS setting */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {DARK_BG} !important;
        color: {TEXT} !important;
    }}
    [data-testid="stHeader"] {{ background-color: transparent !important; }}

    h1, h2, h3 {{ color: {AMBER} !important; font-weight: 700; }}
    p, span, label {{ color: {TEXT}; }}
    .stCaption, [data-testid="stCaptionContainer"] {{ color: {TEXT_MUTED} !important; }}

    /* KPI cards */
    div[data-testid="stMetric"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-left: 4px solid {AMBER};
        border-radius: 12px;
        padding: 14px 18px 10px 18px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245, 165, 36, 0.15);
    }}
    div[data-testid="stMetricLabel"] {{ font-weight: 600; color: {TEXT_MUTED} !important; }}
    div[data-testid="stMetricValue"] {{
        color: {TEXT} !important;
        font-size: 1.4rem !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {CARD_BG} !important;
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {{
        color: {TEXT} !important;
    }}

    /* Widgets */
    div[data-baseweb="select"] > div, .stTextInput input {{
        background-color: {DARK_BG} !important;
        border-color: {BORDER} !important;
        color: {TEXT} !important;
    }}
    span[data-baseweb="tag"] {{
        background-color: {AMBER_DIM} !important;
        color: {DARK_BG} !important;
    }}
    span[data-baseweb="tag"] * {{ color: {DARK_BG} !important; }}

    /* Expanders / dataframes */
    details, [data-testid="stExpander"] {{
        background: {DARK_BG};
        border: 1px solid {BORDER};
        border-radius: 8px;
    }}
    [data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 8px; }}

    /* Insight callouts */
    .insight-box {{
        background: #1E2A1A;
        border-left: 4px solid #8BC34A;
        border-radius: 8px;
        padding: 10px 16px;
        margin: 6px 0;
        font-size: 0.92rem;
        color: {TEXT} !important;
    }}

    /* Hero banner on Home */
    .hero {{
        background: linear-gradient(135deg, #7A4A0A 0%, {AMBER} 100%);
        border-radius: 16px;
        padding: 36px 40px;
        color: white;
        margin-bottom: 20px;
    }}
    .hero h1 {{ color: #FFFFFF !important; margin-bottom: 4px; }}
    .hero p {{ color: #FCEBD5 !important; font-size: 1.05rem; margin: 2px 0; }}
    .hero b {{ color: #FFFFFF !important; }}

    .stTabs [data-baseweb="tab"] {{ padding: 8px 16px; border-radius: 8px 8px 0 0; color: {TEXT}; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def insight(text: str):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)


def section_header(icon: str, title: str, caption: str = ""):
    st.markdown(f"## {icon} {title}")
    if caption:
        st.caption(caption)


# --------------------------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------------------------
try:
    df, cleaning_report = load_and_prepare(CSV_PATH)
except FileNotFoundError:
    st.error(
        f"Couldn't find **{CSV_PATH}**. Place the CSV next to `app.py` "
        "(or edit `CSV_PATH` at the top of the file) and rerun."
    )
    st.stop()
except Exception as e:
    st.error(f"Something went wrong while loading the data: {e}")
    st.stop()

if df.empty:
    st.warning("The dataset loaded but is empty after cleaning.")
    st.stop()

# Match ship-state -> GeoJSON state names ONCE on the full, stable dataset.
# This involves a network fetch + fuzzy string matching, so it must never run
# against the filtered dataframe (which changes on every widget interaction) —
# doing so was the main cause of the app feeling slow.
df, india_geojson = add_state_clean(df)


# --------------------------------------------------------------------------
# SIDEBAR — NAVIGATION
# --------------------------------------------------------------------------
st.sidebar.markdown(
    f"""
    <div style="text-align:center; padding: 6px 0 14px 0;">
        <div style="font-size:2rem;">📊</div>
        <div style="font-weight:700; font-size:1.05rem; color:{AMBER};">
            Amazon Sales Analytics
        </div>
        <div style="font-size:0.8rem; color:#5b6b85;">B.Tech Data Science Project</div>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES = [
    "🏠 Home",
    "🔍 Dataset Overview",
    "🧹 Data Cleaning",
    "📌 KPI Dashboard",
    "📈 Sales Analysis",
    "👕 Product Analysis",
    "📊 Advanced Analytics",
    "📦 Order Analysis",
    "🗺️ National Sales Analysis",
    "🧑‍🤝‍🧑 Customer Analysis",
    "📝 Conclusion & Recommendations",
]
page = st.sidebar.radio("Navigate", PAGES, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.header("🔎 Global Filters")
st.sidebar.caption("Leave a filter empty to include everything.")


def multiselect_all(label, options, key):
    """A multiselect where an empty selection means 'no filter' (= all)."""
    selected = st.multiselect(label, options, default=[], key=key)
    return list(options) if not selected else selected


years = sorted(df["Year"].dropna().unique().tolist())
months = [m for m in MONTH_ORDER if m in df["Month"].unique()]
categories = sorted(df["Category"].dropna().unique())
sizes = sorted(df["Size"].dropna().unique())
states = sorted(df["ship-state"].dropna().unique())
statuses = sorted(df["Status"].dropna().unique())

with st.sidebar.expander("🗓️ Time", expanded=True):
    f_year = multiselect_all("Year", years, key="f_year")
    f_month = multiselect_all("Month", months, key="f_month")

with st.sidebar.expander("🏷️ Product"):
    f_category = multiselect_all("Category", categories, key="f_category")
    f_size = multiselect_all("Size", sizes, key="f_size")

with st.sidebar.expander("📍 Location"):
    f_state = multiselect_all("State", states, key="f_state")
    city_search = st.text_input(
        "City contains (8,698 cities — type to search)", value="", key="f_city_search"
    )

with st.sidebar.expander("📦 Order"):
    f_status = multiselect_all("Status", statuses, key="f_status")
    f_fulfilment = (
        multiselect_all("Fulfilment", sorted(df["Fulfilment"].dropna().unique()), key="f_fulfilment")
        if "Fulfilment" in df.columns else None
    )
    f_courier = (
        multiselect_all("Courier Status", sorted(df["Courier Status"].dropna().unique()), key="f_courier")
        if "Courier Status" in df.columns else None
    )
    f_b2b = (
        multiselect_all("B2B / B2C", df["B2B"].dropna().unique().tolist(), key="f_b2b")
        if "B2B" in df.columns else None
    )

# ---- Apply filters ----
mask = (
    df["Year"].isin(f_year)
    & df["Month"].isin(f_month)
    & df["Category"].isin(f_category)
    & df["Size"].isin(f_size)
    & df["ship-state"].isin(f_state)
    & df["Status"].isin(f_status)
)
if city_search.strip():
    mask &= df["ship-city"].str.contains(city_search.strip(), case=False, na=False)
if f_fulfilment is not None:
    mask &= df["Fulfilment"].isin(f_fulfilment)
if f_courier is not None:
    mask &= df["Courier Status"].isin(f_courier)
if f_b2b is not None:
    mask &= df["B2B"].isin(f_b2b)

fdf = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"**{len(fdf):,}** of {len(df):,} cleaned rows match your filters.")
st.sidebar.download_button(
    "⬇️ Download filtered data",
    data=fdf.to_csv(index=False).encode("utf-8"),
    file_name="filtered_amazon_sales.csv",
    mime="text/csv",
    use_container_width=True,
)
st.sidebar.download_button(
    "⬇️ Download full cleaned dataset",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="amazon_sales_cleaned.csv",
    mime="text/csv",
    use_container_width=True,
)

if fdf.empty:
    st.warning("No rows match the current filters — widen your selection in the sidebar.")
    st.stop()

kpis = compute_kpis(fdf)


# ==========================================================================
# PAGE: HOME
# ==========================================================================
if page == "🏠 Home":
    st.markdown(
        f"""
        <div class="hero">
            <h1>📊 Amazon Sales Analysis Dashboard</h1>
            <p>An end-to-end analytics dashboard covering data cleaning, EDA,
            KPIs, and business insights from a real Amazon India sales export.</p>
            <p style="margin-top:14px;"><b>{STUDENT_NAME}</b> · {BRANCH_NAME} · {COLLEGE_NAME}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📄 Total Rows (raw)", f"{cleaning_report['raw_shape'][0]:,}")
    c2.metric("📊 Total Columns (raw)", cleaning_report["raw_shape"][1])
    c3.metric("✅ Rows After Cleaning", f"{cleaning_report['clean_shape'][0]:,}")
    c4.metric("🔁 Duplicates Removed", f"{cleaning_report['duplicates_removed']:,}")
    st.caption("📁 Data source: **Amazon Sale Report.csv**")

    st.markdown("### 📖 Project Overview")
    st.write(
        "This dashboard analyzes Amazon India order-level sales data to surface "
        "revenue trends, product and category performance, fulfilment and courier "
        "reliability, and state/city-level demand. The pipeline covers missing-value "
        "treatment, duplicate removal, date parsing, feature engineering (Year, Month, "
        "Weekday), outlier detection (IQR), an India choropleth for geographic sales, and an "
        "**Advanced Analytics** page with heatmaps, an interactive scatter plot, and a "
        "distribution explorer (box plots)."
    )

    st.markdown("### 🧭 How to use this dashboard")
    st.write(
        "Use the sidebar to navigate between pages and apply filters (Year, Month, "
        "Category, Size, State, City, Status, Fulfilment, Courier Status, B2B/B2C). "
        "Every chart across every page updates live based on your filter selection."
    )


# ==========================================================================
# PAGE: DATASET OVERVIEW
# ==========================================================================
elif page == "🔍 Dataset Overview":
    section_header("🔍", "Dataset Overview", "Structure and quality of the cleaned dataset")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Duplicate Rows (raw, removed)", cleaning_report["duplicates_removed"])

    st.markdown("#### 📋 Preview")
    n_rows = st.slider("Rows to preview", 5, 100, 20, step=5)
    st.dataframe(df.head(n_rows), use_container_width=True)

    with st.expander("📐 Column names & data types"):
        dtype_df = pd.DataFrame({"Column": df.dtypes.index, "Data Type": df.dtypes.values.astype(str)})
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with st.expander("❓ Missing values (cleaned dataset)"):
        miss = df.isna().sum()
        miss = miss[miss > 0].sort_values(ascending=False)
        if miss.empty:
            st.success("No missing values remain in the cleaned dataset.")
        else:
            st.dataframe(miss.rename("Missing Count"), use_container_width=True)

    with st.expander("📈 Summary statistics"):
        st.dataframe(df.describe(include="all").T, use_container_width=True)


# ==========================================================================
# PAGE: DATA CLEANING
# ==========================================================================
elif page == "🧹 Data Cleaning":
    section_header("🧹", "Data Cleaning", "Before vs after — every treatment step applied")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Raw dataset")
        st.metric("Shape", f"{cleaning_report['raw_shape'][0]:,} × {cleaning_report['raw_shape'][1]}")
    with c2:
        st.markdown("##### Cleaned dataset")
        st.metric("Shape", f"{cleaning_report['clean_shape'][0]:,} × {cleaning_report['clean_shape'][1]}")

    st.markdown("#### 🗑️ Columns dropped (redundant / near-empty)")
    st.write(", ".join(cleaning_report["dropped_columns"]) or "None")

    st.markdown("#### 🔁 Duplicate rows removed")
    st.write(f"**{cleaning_report['duplicates_removed']:,}** duplicate rows were found and removed.")

    st.markdown("#### 💰 Missing `Amount` values")
    st.write(
        f"**{cleaning_report['missing_amount_rows']:,}** rows had a missing `Amount` "
        "— these were dropped after confirming they were overwhelmingly Cancelled orders "
        "with no completed transaction value."
    )
    if "missing_amount_status_breakdown" in cleaning_report:
        st.dataframe(
            cleaning_report["missing_amount_status_breakdown"].rename("Row Count"),
            use_container_width=True,
        )

    st.markdown("#### 📅 Date conversion")
    st.write(
        f"`Date` was parsed to datetime (invalid dates become `NaT` instead of crashing). "
        f"Range: **{df['Date'].min().date()}** to **{df['Date'].max().date()}**."
    )

    st.markdown("#### 🛠️ Feature engineering")
    st.write(
        "Added `Year`, `Month` (ordered categorical), `Weekday` (ordered categorical), "
        "and `YearMonth` for trend analysis without merging across years."
    )

    st.markdown("#### 📊 Missing values before vs after")
    before = cleaning_report["raw_missing"]
    before = before[before > 0].sort_values(ascending=False)
    after = cleaning_report["clean_missing"]
    after = after.reindex(before.index).fillna(0)
    comp = pd.DataFrame({"Before Cleaning": before, "After Cleaning": after})
    fig = px.bar(
        comp.reset_index().melt(id_vars="index", var_name="Stage", value_name="Missing Count"),
        x="index", y="Missing Count", color="Stage", barmode="group",
        title="Missing Values — Before vs After Cleaning",
        template=TEMPLATE, color_discrete_sequence=[AMBER, SKY],
    )
    fig.update_xaxes(title="Column")
    st.plotly_chart(fig, use_container_width=True)


# ==========================================================================
# PAGE: KPI DASHBOARD
# ==========================================================================
elif page == "📌 KPI Dashboard":
    section_header("📌", "KPI Dashboard", "Headline metrics for the current filter selection")

    r1 = st.columns(4)
    r1[0].metric("💰 Total Revenue", fmt_inr(kpis["total_revenue"]))
    r1[1].metric("📦 Total Orders", f"{kpis['total_orders']:,}")
    r1[2].metric("🛒 Total Qty Sold", f"{kpis['total_qty']:,}")
    r1[3].metric("📊 Avg Order Value", fmt_inr(kpis["avg_order_value"]))

    r2 = st.columns(4)
    r2[0].metric("📐 Avg Quantity / Order", f"{kpis['avg_qty']:.2f}")
    r2[1].metric("🌍 States Covered", kpis["num_states"])
    r2[2].metric("🏙️ Cities Covered", kpis["num_cities"])
    r2[3].metric("🏷️ Categories", kpis["num_categories"])

    r3 = st.columns(4)
    r3[0].metric("❌ Cancellation Rate", fmt_pct(kpis["cancellation_rate"]))
    r3[1].metric("🏢 B2B Orders", f"{kpis['b2b_orders']:,}")
    r3[2].metric("🛍️ B2C Orders", f"{kpis['b2c_orders']:,}")
    r3[3].metric("↩️ Return Rate", fmt_pct(kpis["return_rate"]))

    insight(
        f"B2C accounts for {kpis['b2c_orders'] / max(kpis['b2b_orders']+kpis['b2c_orders'],1)*100:.1f}% "
        "of orders in the current selection — Amazon's marketplace here is overwhelmingly consumer-facing."
    )
    insight(f"The cancellation rate for the current filter is {fmt_pct(kpis['cancellation_rate'])}.")


# ==========================================================================
# PAGE: SALES ANALYSIS
# ==========================================================================
elif page == "📈 Sales Analysis":
    section_header("📈", "Sales Analysis", "Trends over time")

    monthly_sales = fdf.groupby("YearMonth")["Amount"].sum().reset_index()
    fig = px.line(
        monthly_sales, x="YearMonth", y="Amount", markers=True,
        title="Monthly Sales Trend", template=TEMPLATE,
    )
    fig.update_traces(line_color=AMBER, line_width=3)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        monthly_orders = fdf.groupby("YearMonth")["Order ID"].nunique().reset_index(name="Orders")
        fig = px.line(
            monthly_orders, x="YearMonth", y="Orders", markers=True,
            title="Orders per Month", template=TEMPLATE,
        )
        fig.update_traces(line_color=SKY, line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        rev_by_month = (
            fdf.groupby("Month", observed=True)["Amount"].sum().reset_index()
        )
        fig = px.bar(
            rev_by_month, x="Month", y="Amount", title="Revenue by Month (all years combined)",
            template=TEMPLATE, color="Amount", color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        weekday_sales = fdf.groupby("Weekday", observed=True)["Amount"].sum().reset_index()
        fig = px.bar(
            weekday_sales, x="Weekday", y="Amount", title="Weekday Sales Analysis",
            template=TEMPLATE, color="Amount", color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        daily = fdf.set_index("Date").resample("D")["Amount"].sum().reset_index()
        fig = px.line(daily, x="Date", y="Amount", title="Daily Sales Trend (drag the slider below to zoom)", template=TEMPLATE)
        fig.update_traces(line_color=AMBER_DIM)
        fig.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)

    top_month = rev_by_month.sort_values("Amount", ascending=False).iloc[0]
    top_weekday = weekday_sales.sort_values("Amount", ascending=False).iloc[0]
    insight(f"**{top_month['Month']}** generated the highest combined revenue in the current selection.")
    insight(f"**{top_weekday['Weekday']}** is the strongest day of the week for sales.")


# ==========================================================================
# PAGE: PRODUCT ANALYSIS
# ==========================================================================
elif page == "👕 Product Analysis":
    section_header("👕", "Product Analysis", "Category and size performance")

    c1, c2 = st.columns(2)
    with c1:
        cat_sales = fdf.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(
            cat_sales, x="Category", y="Amount", color="Amount", title="Category-wise Revenue",
            template=TEMPLATE, color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        cat_qty = fdf.groupby("Category")["Qty"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(
            cat_qty, x="Category", y="Qty", title="Units Sold by Category",
            template=TEMPLATE, color="Qty", color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.treemap(
        cat_sales, path=["Category"], values="Amount", title="Revenue Share by Category (Treemap)",
        template=TEMPLATE, color="Amount", color_continuous_scale=MAP_SCALE,
    )
    st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        size_counts = fdf["Size"].value_counts().reset_index()
        size_counts.columns = ["Size", "Orders"]
        fig = px.bar(
            size_counts, x="Size", y="Orders", color="Orders", title="Product Size Distribution",
            template=TEMPLATE, color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = px.box(
            fdf, x="Category", y="Amount", title="Amount Distribution by Category (Outliers)",
            template=TEMPLATE, color_discrete_sequence=[AMBER],
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    _, amt_upper, amt_out = iqr_bounds(fdf["Amount"])
    top_cat = cat_sales.iloc[0]
    top_size = size_counts.iloc[0]
    insight(f"**{top_cat['Category']}** is the top-grossing category with {fmt_inr(top_cat['Amount'])} in revenue.")
    insight(f"Size **{top_size['Size']}** has the highest order count ({top_size['Orders']:,} orders).")
    insight(f"{amt_out:,} orders sit outside the IQR bound (above {fmt_inr(amt_upper)}) — high-value outliers worth reviewing.")


# ==========================================================================
# PAGE: ADVANCED ANALYTICS  (heatmaps, scatter plot, interactive box plots)
# ==========================================================================
elif page == "📊 Advanced Analytics":
    section_header("📊", "Advanced Analytics", "Heatmaps, correlations, and relationship exploration — pick your own view")

    # ---- 1. Seasonality heatmap: Month x Weekday --------------------------
    st.markdown("#### 🔥 Sales Heatmap — Month × Weekday")
    heat_metric = st.radio(
        "Metric", ["Revenue (Amount)", "Orders"], horizontal=True, key="heat_metric"
    )
    if heat_metric == "Revenue (Amount)":
        pivot = fdf.pivot_table(
            index="Weekday", columns="Month", values="Amount", aggfunc="sum", observed=True
        )
    else:
        pivot = fdf.pivot_table(
            index="Weekday", columns="Month", values="Order ID", aggfunc="nunique", observed=True
        )
    pivot = pivot.reindex(index=[d for d in WEEKDAY_ORDER if d in pivot.index])
    pivot = pivot.reindex(columns=[m for m in MONTH_ORDER if m in pivot.columns])
    fig = px.imshow(
        pivot, color_continuous_scale=MAP_SCALE, aspect="auto",
        labels=dict(x="Month", y="Weekday", color=heat_metric),
        title=f"{heat_metric} by Month and Weekday", template=TEMPLATE,
    )
    fig.update_xaxes(side="bottom")
    st.plotly_chart(fig, use_container_width=True)

    # ---- 2. Category x Size heatmap ---------------------------------------
    st.markdown("#### 🔥 Order Count Heatmap — Category × Size")
    cat_size_pivot = fdf.pivot_table(
        index="Category", columns="Size", values="Order ID", aggfunc="nunique"
    ).fillna(0)
    fig = px.imshow(
        cat_size_pivot, color_continuous_scale=MAP_SCALE, aspect="auto",
        labels=dict(x="Size", y="Category", color="Orders"),
        title="Orders by Category and Size", template=TEMPLATE,
    )
    fig.update_xaxes(side="bottom")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---- 3. Interactive scatter plot --------------------------------------
    st.markdown("#### 🎯 Interactive Scatter Plot")
    numeric_cols = [c for c in ["Amount", "Qty"] if c in fdf.columns]
    color_options = [c for c in ["Category", "Status", "Fulfilment", "B2B", "ship-state", "Size"] if c in fdf.columns]

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        x_axis = st.selectbox("X-axis", numeric_cols, index=0, key="scatter_x")
    with sc2:
        y_axis = st.selectbox("Y-axis", numeric_cols, index=min(1, len(numeric_cols) - 1), key="scatter_y")
    with sc3:
        color_by = st.selectbox("Color by", color_options, index=0, key="scatter_color")
    with sc4:
        sample_n = st.slider(
            "Points to plot", min_value=200, max_value=min(10000, len(fdf)),
            value=min(2000, len(fdf)), step=200, key="scatter_sample",
        )

    scatter_df = fdf.sample(n=sample_n, random_state=42) if len(fdf) > sample_n else fdf
    fig = px.scatter(
        scatter_df, x=x_axis, y=y_axis, color=color_by,
        hover_data=[c for c in ["Order ID", "ship-state", "Status"] if c in scatter_df.columns],
        title=f"{y_axis} vs {x_axis}, colored by {color_by} ({sample_n:,}-point sample)",
        template=TEMPLATE, opacity=0.65,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Tip: click a legend entry to isolate it, drag to zoom, double-click to reset.")

    st.markdown("---")

    # ---- 4. Interactive box plot -------------------------------------------
    st.markdown("#### 📦 Interactive Box Plot — Distribution Explorer")
    box_group_options = [c for c in ["Category", "Size", "Status", "Fulfilment", "B2B", "Weekday", "Month"] if c in fdf.columns]
    bc1, bc2 = st.columns(2)
    with bc1:
        box_group = st.selectbox("Group by", box_group_options, index=0, key="box_group")
    with bc2:
        box_metric = st.selectbox("Metric", numeric_cols, index=0, key="box_metric")

    fig = px.box(
        fdf, x=box_group, y=box_metric, color=box_group, points="outliers",
        title=f"{box_metric} Distribution by {box_group}", template=TEMPLATE,
        color_discrete_sequence=ORANGE_SEQ,
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    corr = fdf[numeric_cols].corr().iloc[0, 1] if len(numeric_cols) > 1 else None
    if corr is not None:
        insight(f"Correlation between **{numeric_cols[0]}** and **{numeric_cols[1]}** in the current selection is **{corr:.2f}**.")
    insight("Use the controls above to swap axes, grouping, and sample size — every chart on this page reacts instantly to your choices and the sidebar filters.")


# ==========================================================================
# PAGE: ORDER ANALYSIS
# ==========================================================================
elif page == "📦 Order Analysis":
    section_header("📦", "Order Analysis", "Status, fulfilment, and courier performance")

    c1, c2 = st.columns(2)
    with c1:
        status = fdf["Status"].value_counts().reset_index()
        status.columns = ["Status", "Orders"]
        fig = px.bar(
            status, x="Status", y="Orders", color="Orders", title="Order Status Distribution",
            template=TEMPLATE, color_continuous_scale=MAP_SCALE,
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        if "Fulfilment" in fdf.columns:
            fulfil = fdf["Fulfilment"].value_counts().reset_index()
            fulfil.columns = ["Fulfilment", "Orders"]
            fig = px.pie(
                fulfil, values="Orders", names="Fulfilment", hole=0.5,
                title="Fulfilment Analysis (Amazon vs Merchant)", template=TEMPLATE,
                color_discrete_sequence=ORANGE_SEQ,
            )
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if "Courier Status" in fdf.columns:
            courier = fdf["Courier Status"].value_counts().reset_index()
            courier.columns = ["Courier Status", "Orders"]
            fig = px.pie(
                courier, values="Orders", names="Courier Status", hole=0.45,
                title="Courier Status Distribution", template=TEMPLATE,
                color_discrete_sequence=ORANGE_SEQ,
            )
            st.plotly_chart(fig, use_container_width=True)
    with c4:
        if "ship-service-level" in fdf.columns:
            ssl = fdf["ship-service-level"].value_counts().reset_index()
            ssl.columns = ["Ship Service Level", "Orders"]
            fig = px.bar(
                ssl, x="Ship Service Level", y="Orders", color="Orders",
                title="Ship Service Level", template=TEMPLATE, color_continuous_scale=MAP_SCALE,
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🔢 Order status counts")
    c5, c6, c7 = st.columns(3)
    pending_n = fdf["Status"].str.contains("Pending", case=False, na=False).sum()
    cancelled_n = fdf["Status"].str.contains("Cancel", case=False, na=False).sum()
    returned_n = fdf["Status"].str.contains("Return", case=False, na=False).sum()
    c5.metric("⏳ Pending Orders", f"{pending_n:,}")
    c6.metric("❌ Cancelled Orders", f"{cancelled_n:,}")
    c7.metric("↩️ Returned Orders", f"{returned_n:,}")

    top_status = status.sort_values("Orders", ascending=False).iloc[0]
    insight(f"**{top_status['Status']}** is the most common order status ({top_status['Orders']:,} orders).")
    insight(f"Cancelled orders make up {fmt_pct(kpis['cancellation_rate'])} of the current selection.")


# ==========================================================================
# PAGE: NATIONAL SALES ANALYSIS
# ==========================================================================
elif page == "🗺️ National Sales Analysis":
    section_header("🗺️", "National Sales Analysis", "State and city-level performance across India")

    state_sales = fdf.groupby("ship-state")["Amount"].sum().sort_values(ascending=False)
    state_orders = fdf.groupby("ship-state")["Order ID"].nunique().sort_values(ascending=False)

    if india_geojson is not None:
        state_sales_map = (
            fdf.dropna(subset=["state_clean"])
            .groupby("state_clean")["Amount"].sum().reset_index()
        )
        fig = px.choropleth(
            state_sales_map, geojson=india_geojson, featureidkey="properties.NAME_1",
            locations="state_clean", color="Amount", color_continuous_scale=MAP_SCALE,
            title="State-wise Sales — India", template=TEMPLATE,
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Map boundaries unavailable offline — showing the bar-chart view below instead.")

    top_n = st.slider("Number of top states / cities to show", min_value=5, max_value=25, value=10, step=1, key="geo_top_n")

    c1, c2 = st.columns(2)
    with c1:
        top10_states = state_sales.head(top_n).reset_index()
        top10_states.columns = ["State", "Amount"]
        fig = px.bar(
            top10_states.sort_values("Amount"), x="Amount", y="State", orientation="h",
            title=f"Top {top_n} States by Revenue", template=TEMPLATE, color="Amount",
            color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top10_orders = state_orders.head(top_n).reset_index()
        top10_orders.columns = ["State", "Orders"]
        fig = px.bar(
            top10_orders.sort_values("Orders"), x="Orders", y="State", orientation="h",
            title=f"Top {top_n} States by Orders", template=TEMPLATE, color="Orders",
            color_continuous_scale=MAP_SCALE,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"#### 🏙️ Top {top_n} Cities by Revenue")
    top10_cities = (
        fdf.groupby("ship-city")["Amount"].sum().sort_values(ascending=False).head(top_n).reset_index()
    )
    fig = px.bar(
        top10_cities, x="ship-city", y="Amount", color="Amount", text_auto=".2s",
        title=f"Top {top_n} Cities", template=TEMPLATE, color_continuous_scale=MAP_SCALE,
    )
    st.plotly_chart(fig, use_container_width=True)

    insight(f"**{state_sales.index[0]}** generates the highest revenue of any state in the current selection.")
    insight(f"The top 10 states contribute {fmt_inr(top10_states['Amount'].sum())} — "
            f"{top10_states['Amount'].sum()/fdf['Amount'].sum()*100:.1f}% of total filtered revenue.")


# ==========================================================================
# PAGE: CUSTOMER ANALYSIS
# ==========================================================================
elif page == "🧑‍🤝‍🧑 Customer Analysis":
    section_header("🧑‍🤝‍🧑", "Customer Analysis", "B2B vs B2C behaviour")

    if "B2B" not in fdf.columns:
        st.info("No `B2B` column found in this dataset.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            b2b_counts = fdf["B2B"].replace({True: "B2B", False: "B2C"}).value_counts().reset_index()
            b2b_counts.columns = ["Type", "Orders"]
            fig = px.pie(
                b2b_counts, values="Orders", names="Type", hole=0.5,
                title="B2B vs B2C Orders", template=TEMPLATE, color_discrete_sequence=[AMBER, SKY],
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            qty_by_type = (
                fdf.assign(Type=fdf["B2B"].replace({True: "B2B", False: "B2C"}))
                .groupby("Type")["Qty"].sum().reset_index()
            )
            fig = px.bar(
                qty_by_type, x="Type", y="Qty", color="Type", title="Quantity Distribution",
                template=TEMPLATE, color_discrete_sequence=[AMBER, SKY],
            )
            st.plotly_chart(fig, use_container_width=True)

        rev_by_type = (
            fdf.assign(Type=fdf["B2B"].replace({True: "B2B", False: "B2C"}))
            .groupby("Type")["Amount"].sum().reset_index()
        )
        fig = px.bar(
            rev_by_type, x="Type", y="Amount", color="Type", title="Revenue Distribution — B2B vs B2C",
            template=TEMPLATE, color_discrete_sequence=[AMBER, SKY],
        )
        st.plotly_chart(fig, use_container_width=True)

        b2c_share = b2b_counts.set_index("Type")["Orders"].get("B2C", 0) / b2b_counts["Orders"].sum() * 100
        insight(f"B2C orders make up {b2c_share:.1f}% of all orders in the current selection.")
        insight(f"B2B revenue share: {rev_by_type.set_index('Type')['Amount'].get('B2B', 0) / rev_by_type['Amount'].sum() * 100:.1f}% "
                "of total filtered revenue.")


# ==========================================================================
# PAGE: CONCLUSION & RECOMMENDATIONS
# ==========================================================================
elif page == "📝 Conclusion & Recommendations":
    section_header("📝", "Conclusion & Recommendations", "Summary of findings from the current filter selection")

    top_category = fdf.groupby("Category")["Amount"].sum().idxmax()
    top_state = fdf.groupby("ship-state")["Amount"].sum().idxmax()
    top_month_val = fdf.groupby("Month", observed=True)["Amount"].sum().idxmax()
    b2c_share = (
        (fdf["B2B"] == False).sum() / len(fdf) * 100 if "B2B" in fdf.columns else None  # noqa: E712
    )

    st.markdown("#### 🏁 Key Findings")
    st.markdown(
        f"""
        - **{top_category}** is the highest-revenue product category in the current selection.
        - **{top_state}** is the best-performing state by total revenue.
        - **{top_month_val}** was the strongest month for sales.
        - The cancellation rate stands at **{fmt_pct(kpis['cancellation_rate'])}** and the
          return rate at **{fmt_pct(kpis['return_rate'])}**.
        {f"- B2C orders account for **{b2c_share:.1f}%** of all orders — the marketplace is consumer-driven." if b2c_share is not None else ""}
        - Total revenue across the current selection is **{fmt_inr(kpis['total_revenue'])}**
          across **{kpis['total_orders']:,}** orders.
        """
    )

    st.markdown("#### 📌 Business Recommendations")
    st.markdown(
        """
        1. **Concentrate marketing spend** on the top-performing category and state to
           compound existing demand rather than spreading budget evenly.
        2. **Investigate the cancellation/return drivers** — cross-check against
           `Fulfilment` and `Courier Status` to see whether delivery reliability is
           a contributing factor.
        3. **Plan inventory around the seasonal peak month** identified above to avoid
           stockouts during the highest-demand period.
        4. **Expand B2B outreach** if B2B share is currently low relative to B2C — it is
           a comparatively under-penetrated channel in most Amazon India categories.
        5. **Monitor high-value order outliers** (flagged in the IQR analysis on the
           Product Analysis page) for fraud risk or wholesale-buyer opportunities.
        """
    )

    st.markdown("---")
    st.caption(
        "This dashboard and its underlying analysis were built as part of a B.Tech "
        f"Data Science project by {STUDENT_NAME}, {COLLEGE_NAME}."
    )


# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit · Pandas · Plotly")
st.sidebar.caption(f"© {STUDENT_NAME}")
