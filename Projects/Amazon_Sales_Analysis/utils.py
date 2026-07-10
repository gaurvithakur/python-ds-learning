"""
utils.py
--------
Data loading, cleaning, feature engineering, and metric/insight helpers
for the Amazon Sales Analysis dashboard.

All the preprocessing logic here mirrors the project notebook
(amazon_sales_improved.ipynb) — it has just been converted into
reusable, cached functions so the Streamlit app never repeats a
calculation, and duplicates from the raw CSV are removed exactly once.
"""

from __future__ import annotations

from difflib import get_close_matches

import numpy as np
import pandas as pd
import requests
import streamlit as st

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]

# Columns that are redundant / near-empty in the raw Amazon export.
COLUMNS_TO_DROP = ["index", "New", "PendingS"]

# Raw ship-state values in this dataset that don't match the GeoJSON's
# official state names (abbreviations, typos, old names).
MANUAL_STATE_ALIASES = {
    "DELHI": "Delhi", "NEW DELHI": "Delhi", "NCT OF DELHI": "Delhi",
    "ORISSA": "Odisha",
    "PONDICHERRY": "Puducherry",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "PUNJAB/MOHALI/ZIRAKPUR": "Punjab",
    "RAJSHTHAN": "Rajasthan",
    "AR": "Arunachal Pradesh",
}

INDIA_GEOJSON_URL = (
    "https://raw.githubusercontent.com/Subhash9325/"
    "GeoJson-Data-of-Indian-States/master/Indian_States"
)


# --------------------------------------------------------------------------
# LOAD + CLEAN + ENGINEER  (single cached pipeline — never repeated)
# --------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading and cleaning dataset...")
def load_and_prepare(path: str) -> tuple[pd.DataFrame, dict]:
    """
    Loads the raw CSV, cleans it, and engineers time-based features.
    Returns (cleaned_df, cleaning_report) where cleaning_report captures
    before/after stats for the Data Cleaning page.
    """
    try:
        raw = pd.read_csv(path)
    except UnicodeDecodeError:
        raw = pd.read_csv(path, encoding="latin1")

    report: dict = {"raw_shape": raw.shape, "raw_missing": raw.isna().sum()}

    df = raw.copy()

    # ---- Drop redundant / empty columns -----------------------------
    existing_to_drop = [c for c in COLUMNS_TO_DROP if c in df.columns]
    df.drop(columns=existing_to_drop, inplace=True, errors="ignore")
    report["dropped_columns"] = existing_to_drop

    # ---- Duplicates ----------------------------------------------------
    dup_count = int(df.duplicated().sum())
    df.drop_duplicates(inplace=True)
    report["duplicates_removed"] = dup_count

    # ---- Dates -----------------------------------------------------------
    # This export mixes MM-DD-YY and MM-DD-YYYY within the same column, so a
    # single fixed format string fails on part of the data — "mixed" handles
    # both without falling back to the slow per-row dateutil warning path.
    try:
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False, errors="coerce")
    except (ValueError, TypeError):
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ---- Location fields: categorical -> fill with "Unknown" -----------
    for col in ["ship-city", "ship-state", "ship-country"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    if "ship-postal-code" in df.columns:
        postal_missing = df["ship-postal-code"].isna()
        df["ship-postal-code"] = (
            df["ship-postal-code"].astype("Int64").astype(str).where(~postal_missing, "Unknown")
        )

    # ---- Missing Amount: usually cancelled orders with no completed txn -
    missing_amount = int(df["Amount"].isna().sum())
    report["missing_amount_rows"] = missing_amount
    if missing_amount and "Status" in df.columns:
        report["missing_amount_status_breakdown"] = (
            df.loc[df["Amount"].isna(), "Status"].value_counts()
        )
    df = df.dropna(subset=["Amount"])

    report["clean_shape"] = df.shape
    report["clean_missing"] = df.isna().sum()

    # ---- Feature engineering --------------------------------------------
    df["Year"] = df["Date"].dt.year
    df["Month"] = pd.Categorical(
        df["Date"].dt.month_name(), categories=MONTH_ORDER, ordered=True
    )
    df["Weekday"] = pd.Categorical(
        df["Date"].dt.day_name(), categories=WEEKDAY_ORDER, ordered=True
    )
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    return df, report


# --------------------------------------------------------------------------
# INDIA CHOROPLETH SUPPORT
# --------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_india_geojson() -> dict | None:
    """Fetches an India state-boundary GeoJSON. Returns None if offline."""
    try:
        resp = requests.get(INDIA_GEOJSON_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _match_state(raw_name, official_states: list[str]) -> str | None:
    if pd.isna(raw_name):
        return None
    key = str(raw_name).strip().upper()
    if key in MANUAL_STATE_ALIASES:
        return MANUAL_STATE_ALIASES[key]
    title = str(raw_name).strip().title()
    if title in official_states:
        return title
    close = get_close_matches(title, official_states, n=1, cutoff=0.6)
    return close[0] if close else None


@st.cache_data(show_spinner="Matching states to map boundaries...")
def add_state_clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict | None]:
    """Adds a `state_clean` column matched against the India GeoJSON."""
    geojson = get_india_geojson()
    if geojson is None:
        return df, None
    official_states = [f["properties"]["NAME_1"] for f in geojson["features"]]
    df = df.copy()
    df["state_clean"] = df["ship-state"].apply(lambda n: _match_state(n, official_states))
    return df, geojson


# --------------------------------------------------------------------------
# KPI / METRIC HELPERS
# --------------------------------------------------------------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    kpis = {
        "total_revenue": df["Amount"].sum(),
        "total_orders": df["Order ID"].nunique() if "Order ID" in df else len(df),
        "total_qty": int(df["Qty"].sum()) if "Qty" in df else 0,
        "avg_order_value": df["Amount"].mean() if len(df) else 0,
        "avg_qty": df["Qty"].mean() if "Qty" in df and len(df) else 0,
        "num_states": df["ship-state"].nunique() if "ship-state" in df else 0,
        "num_cities": df["ship-city"].nunique() if "ship-city" in df else 0,
        "num_categories": df["Category"].nunique() if "Category" in df else 0,
    }

    if "Status" in df.columns and len(df):
        cancelled = df["Status"].str.contains("Cancel", case=False, na=False).sum()
        kpis["cancellation_rate"] = cancelled / len(df) * 100
        returned = df["Status"].str.contains("Return", case=False, na=False).sum()
        kpis["return_rate"] = returned / len(df) * 100
        pending = df["Status"].str.contains("Pending", case=False, na=False).sum()
        kpis["pending_rate"] = pending / len(df) * 100
    else:
        kpis["cancellation_rate"] = kpis["return_rate"] = kpis["pending_rate"] = 0

    if "B2B" in df.columns:
        kpis["b2b_orders"] = int((df["B2B"] == True).sum())   # noqa: E712
        kpis["b2c_orders"] = int((df["B2B"] == False).sum())  # noqa: E712
    else:
        kpis["b2b_orders"] = kpis["b2c_orders"] = 0

    return kpis


def iqr_bounds(series: pd.Series) -> tuple[float, float, int]:
    """Returns (lower_bound, upper_bound, outlier_count) for a numeric series."""
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = int(((series < lower) | (series > upper)).sum())
    return lower, upper, n_out


def fmt_inr(value: float) -> str:
    return f"₹ {value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"
