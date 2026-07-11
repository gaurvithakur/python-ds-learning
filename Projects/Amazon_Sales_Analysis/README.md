# 📊 Amazon Sales Analysis Dashboard

An interactive, portfolio-level analytics dashboard built with **Streamlit** and
**Plotly**, analyzing an Amazon India order-level sales export. Built as a
B.Tech Data Science project — covers data cleaning, EDA, KPIs, and business
insights across a dedicated multi-page layout.

## ✨ Features

- **Home** — project overview and dataset summary
- **Dataset Overview** — shape, dtypes, missing values, summary statistics, adjustable preview
- **Data Cleaning** — before/after comparison of every cleaning step (duplicates, missing values, date parsing, feature engineering)
- **KPI Dashboard** — 12 metric cards with hover effects (revenue, orders, cancellation rate, B2B/B2C split, etc.)
- **Sales Analysis** — monthly/daily/weekday trends
- **Product Analysis** — category & size performance, treemap, outlier detection (IQR + box plots)
- **Order Analysis** — status, fulfilment, courier, ship-service-level breakdowns
- **National Sales Analysis** — India choropleth map (with state-name matching against a GeoJSON) + top states/cities bar charts
- **Customer Analysis** — B2B vs B2C revenue and quantity split
- **Conclusion & Recommendations** — auto-generated summary of key findings

Every page responds live to a shared set of sidebar filters: Year, Month,
Category, Size, State, City, Status, Fulfilment, Courier Status, and B2B/B2C.

## 📁 Project Structure

```
amazon-sales-dashboard/
├── app.py                  # Main Streamlit app — pages & UI
├── utils.py                # Data loading, cleaning, feature engineering, KPI helpers
├── requirements.txt        # Python dependencies
├── README.md                # This file
├── .streamlit/
│   └── config.toml          # Blue & white theme
└── Amazon_Sale_Report.csv   # ← add your dataset here (not included)
```

## 🚀 Setup

1. **Clone / download this folder.**

2. **Install dependencies** (a virtual environment is recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Add the dataset.** Place `Amazon_Sale_Report.csv` in the same folder as
   `app.py`. Expected columns include: `Order ID`, `Date`, `Status`,
   `Fulfilment`, `ship-service-level`, `Category`, `Size`, `Courier Status`,
   `Qty`, `currency`, `Amount`, `ship-city`, `ship-state`, `ship-postal-code`,
   `ship-country`, `B2B`. The app degrades gracefully if some optional
   columns are missing.

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. Open the URL Streamlit prints (usually `http://localhost:8501`).

## 🗺️ Notes on the India choropleth

The "National Sales Analysis" page fetches a public India state-boundary
GeoJSON at runtime (requires internet access) and matches your raw
`ship-state` values against it — including common abbreviations and
alternate spellings (e.g. `PB` → Punjab, `ORISSA` → Odisha). If the fetch
fails (e.g. no internet), the page automatically falls back to horizontal
bar charts for state-wise revenue and orders, so nothing breaks.

## ✏️ Personalizing for your submission

Open `app.py` and edit the constants near the top:

```python
STUDENT_NAME = "Your Name"
COLLEGE_NAME = "Your College Name"
BRANCH_NAME = "B.Tech — Data Science"
```

## 🛠️ Built With

- [Streamlit](https://streamlit.io) — app framework
- [Pandas](https://pandas.pydata.org) — data cleaning & aggregation
- [Plotly](https://plotly.com/python/) — all interactive charts
- [Requests](https://requests.readthedocs.io) — GeoJSON fetch for the choropleth



## Project Presentation

The complete project presentation is available in the `presentation/` folder.

- Amazon_Sales_Analysis_Presentation.pptx
- Amazon_Sales_Analysis_Presentation.pdf
