from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import random
import time

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =======================================================
# PAGE SETUP
# =======================================================
st.set_page_config(
    page_title="Revenue Intelligence Command Centre",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =======================================================
# PREMIUM FULL-SCREEN STYLE
# =======================================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #050B18;
        color: #E8F0FF;
    }

    .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-top: 0.25rem !important;
        padding-bottom: 0.35rem !important;
        padding-left: 0.35rem !important;
        padding-right: 0.35rem !important;
    }

    section.main > div {
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    [data-testid="stAppViewContainer"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.45rem !important;
    }

    html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
    }

    .topbar {
        background: linear-gradient(135deg, #071327 0%, #0B1B34 55%, #071327 100%);
        border: 1px solid #21476F;
        border-radius: 12px;
        padding: 8px 13px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 0 26px rgba(34, 211, 238, 0.08);
    }

    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 10px;
        letter-spacing: 1.7px;
        color: #8CB3F2;
        margin-top: 3px;
        text-transform: uppercase;
    }

    .topbar-right {
        display: flex;
        gap: 7px;
        align-items: center;
        flex-wrap: wrap;
    }

    .badge {
        background: #0E2442;
        border: 1px solid #28558E;
        border-radius: 999px;
        padding: 5px 10px;
        color: #C7D7F4;
        font-size: 11px;
        font-weight: 700;
    }

    .live-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #7EF2C4;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.28);
    }

    .control-strip {
        background: #0B1B34;
        border: 1px solid #183A68;
        border-radius: 11px;
        padding: 7px 10px 1px 10px;
        margin-bottom: 6px;
    }

    .strip-title {
        color: #8CB3F2;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.6px;
        text-transform: uppercase;
    }

    .metric-card {
        background: linear-gradient(135deg, #09182E 0%, #0B1B34 100%);
        border: 1px solid #1E446F;
        border-radius: 11px;
        padding: 8px 10px;
        position: relative;
        min-height: 68px;
        margin-bottom: 5px;
        overflow: hidden;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .metric-card::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 3px;
        background: var(--accent);
        box-shadow: 0 0 14px var(--accent);
    }

    .metric-label {
        color: #8CB3F2;
        font-size: 8.5px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 15.5px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 3px;
    }

    .metric-subtext {
        color: #9CB1D4;
        font-size: 9.5px;
    }

    .signal-strip {
        background: linear-gradient(135deg, #09182E 0%, #0D2548 100%);
        border: 1px solid #24507F;
        border-left: 3px solid #22D3EE;
        border-radius: 11px;
        padding: 7px 11px;
        margin-bottom: 6px;
        color: #C9D8F0;
        font-size: 11px;
        line-height: 1.35;
    }

    .signal-strip b {
        color: #22D3EE;
    }

    .mini-ai-wrap {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 6px;
        margin-bottom: 6px;
    }

    .mini-ai-card {
        background: linear-gradient(135deg, #09182E 0%, #0B1B34 100%);
        border: 1px solid #1E446F;
        border-radius: 10px;
        padding: 8px 10px;
        min-height: 72px;
        box-shadow: 0 0 16px rgba(34, 211, 238, 0.05);
    }

    .mini-ai-pill {
        display: inline-block;
        font-size: 8px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 5px;
        padding: 2px 6px;
        border-radius: 999px;
        border: 1px solid currentColor;
    }

    .mini-ai-title {
        color: #F8FAFC;
        font-size: 10.5px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .mini-ai-action {
        color: #BFD0EC;
        font-size: 9.5px;
        line-height: 1.3;
    }

    .assurance-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 6px;
        margin-bottom: 6px;
    }

    .assurance-card {
        background: linear-gradient(135deg, #09182E 0%, #0B1B34 100%);
        border: 1px solid #1E446F;
        border-radius: 10px;
        padding: 9px 10px;
        min-height: 78px;
    }

    .assurance-title {
        color: #8CB3F2;
        font-size: 8.5px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .assurance-value {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .assurance-note {
        color: #BFD0EC;
        font-size: 9.5px;
        line-height: 1.3;
    }

    .high {color: #EF4444;}
    .medium {color: #F59E0B;}
    .opportunity {color: #22D3EE;}
    .good {color: #10B981;}

    div[data-testid="stPlotlyChart"] {
        background: #0B1B34;
        border: 1px solid #183A68;
        border-radius: 12px;
        padding: 2px 3px 0 3px;
        margin-bottom: 5px;
        box-shadow: 0 0 22px rgba(34, 211, 238, 0.05);
    }

    .section-label {
        font-size: 9px;
        font-weight: 800;
        color: #8CB3F2;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin: 1px 0 4px 3px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        margin-top: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #0B1B34;
        border: 1px solid #183A68;
        border-radius: 8px;
        color: #C7D7F4;
        padding: 5px 12px;
        height: 32px;
        font-size: 12px;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background-color: #12345F;
        color: #FFFFFF;
        border-bottom: 2px solid #22D3EE;
        box-shadow: 0 0 16px rgba(34, 211, 238, 0.18);
    }

    div[data-testid="stDataFrame"] {
        background: #0B1B34;
        border-radius: 10px;
        border: 1px solid #183A68;
    }

    .stDownloadButton button {
        background-color: #102648;
        color: #EAF1FB;
        border: 1px solid #28558E;
        border-radius: 9px;
        padding: 0.35rem 0.8rem;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


# =======================================================
# CONSTANTS
# =======================================================
C_BLUE = "#3B82F6"
C_CYAN = "#22D3EE"
C_GREEN = "#10B981"
C_ORANGE = "#F59E0B"
C_RED = "#EF4444"
C_PURPLE = "#8B5CF6"
C_PINK = "#EC4899"
PAPER = "#0B1B34"
GRID = "#19365C"
FONT = "Arial"
CHART_CONFIG = {"displayModeBar": False}
AUTO_REFRESH_SECONDS = 10

COUNTRY_COORDS = {
    "Botswana": (-22.3285, 24.6849),
    "South Africa": (-30.5595, 22.9375),
    "Namibia": (-22.9576, 18.4904),
    "Zimbabwe": (-19.0154, 29.1549),
    "Zambia": (-13.1339, 27.8493),
    "Lesotho": (-29.6100, 28.2336),
    "Mozambique": (-18.6657, 35.5296),
    "Eswatini": (-26.5225, 31.4659),
}

RESOURCE_MAP = {
    "/index.html": "other",
    "/services.html": "general_service",
    "/jobs.html": "job_request",
    "/apply-job.php": "job_request",
    "/scheduledemo.php": "schedule_demo",
    "/event.php": "promotional_event",
    "/promo.html": "promotional_event",
    "/assistant.php": "ai_virtual_assistant",
    "/contact.html": "general_service",
    "/webinar.html": "promotional_event",
    "/cyber-risk-report.html": "advisory_services",
    "/cybersecurity-support.html": "cybersecurity_support",
    "/incident-response.php": "cybersecurity_support",
    "/advisory-services.html": "advisory_services",
    "/risk-assessment.html": "advisory_services",
    "/monitoring-dashboard.html": "system_monitoring",
    "/threat-alerts.php": "system_monitoring",
    "/managed-detection.html": "system_monitoring",
}

SERVICE_CATEGORY_MAP = {
    "cybersecurity_support": "Cybersecurity Support",
    "ai_virtual_assistant": "Cybersecurity Support",
    "general_service": "Cybersecurity Support",
    "advisory_services": "Advisory Services",
    "schedule_demo": "Advisory Services",
    "promotional_event": "Advisory Services",
    "system_monitoring": "System Monitoring",
    "other": "System Monitoring",
    "job_request": "Sales / Onboarding",
}

SERVICE_CATEGORY_ORDER = [
    "Cybersecurity Support",
    "Advisory Services",
    "System Monitoring",
    "Sales / Onboarding",
]

WEIGHTED_COUNTRIES = (
    ["Botswana"] * 35 +
    ["South Africa"] * 30 +
    ["Namibia"] * 10 +
    ["Zimbabwe"] * 10 +
    ["Zambia"] * 6 +
    ["Lesotho"] * 3 +
    ["Mozambique"] * 3 +
    ["Eswatini"] * 3
)

# =======================================================
# HELPER FUNCTIONS
# =======================================================
def format_label(text):
    text = str(text).replace("_", " ").title()
    text = text.replace("Ai ", "AI ")
    text = text.replace("Http", "HTTP")
    return text


def format_money(value):
    if value >= 1_000_000:
        return f"BWP {value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"BWP {value / 1_000:.1f}K"
    return f"BWP {value:,.0f}"


def metric_card(title, value, subtext, colour):
    return f"""
    <div class="metric-card" style="--accent:{colour};">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    """


def assurance_card(title, value, note):
    return f"""
    <div class="assurance-card">
        <div class="assurance-title">{title}</div>
        <div class="assurance-value">{value}</div>
        <div class="assurance-note">{note}</div>
    </div>
    """


def anonymise_identifier(value):
    hashed_value = hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:8].upper()
    return f"CUST-{hashed_value}"


def add_service_categories(data):
    data = data.copy()
    data["service_category"] = data["request_category"].map(SERVICE_CATEGORY_MAP)
    data["service_category"] = data["service_category"].fillna(data["request_category"].apply(format_label))
    data["customer_request_type"] = (
        data["service_category"].astype(str) + " - " + data["request_category"].apply(format_label)
    )
    data["anonymous_customer_id"] = data["ip_address"].apply(anonymise_identifier)
    return data


def chart_layout(title, height=260, show_legend=True):
    return dict(
        title=title,
        height=height,
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(color="#E8F0FF", family=FONT, size=10),
        margin=dict(l=14, r=10, t=34, b=18),
        xaxis=dict(
            showgrid=True,
            gridcolor=GRID,
            linecolor=GRID,
            zeroline=False,
            tickfont=dict(color="#8CA8D8", size=9),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID,
            linecolor=GRID,
            zeroline=False,
            tickfont=dict(color="#8CA8D8", size=9),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#BBD2F6", size=9),
            orientation="h",
        ),
        showlegend=show_legend,
    )


def load_data():
    data_path = Path("data/web_logs.csv")

    if not data_path.exists():
        st.error("data/web_logs.csv was not found. Run generate_web_logs.py first.")
        st.stop()

    data = pd.read_csv(data_path)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"]).copy()

    data["date_time"] = pd.to_datetime(
        data["date"].dt.strftime("%Y-%m-%d") + " " + data["time"],
        errors="coerce"
    )

    data = data.dropna(subset=["date_time"]).copy()
    data["hour"] = data["date_time"].dt.hour
    data["day_name"] = data["date_time"].dt.day_name()

    return data


def add_business_values(data, scenario):
    data = add_service_categories(data)

    revenue_map = {
        "schedule_demo": 4200,
        "job_request": 1800,
        "ai_virtual_assistant": 650,
        "promotional_event": 900,
        "general_service": 1200,
        "cybersecurity_support": 2600,
        "advisory_services": 3400,
        "system_monitoring": 2100,
        "other": 120,
    }

    cost_map = {
        "schedule_demo": 3350,
        "job_request": 1420,
        "ai_virtual_assistant": 510,
        "promotional_event": 710,
        "general_service": 880,
        "cybersecurity_support": 1850,
        "advisory_services": 2400,
        "system_monitoring": 1450,
        "other": 94,
    }

    department_map = {
        "schedule_demo": "Sales",
        "job_request": "Sales",
        "ai_virtual_assistant": "Support",
        "promotional_event": "Marketing",
        "general_service": "Support",
        "cybersecurity_support": "Support",
        "advisory_services": "Marketing",
        "system_monitoring": "Operations",
        "other": "Operations",
    }

    scenario_multiplier = {
        "Conservative": 0.82,
        "Balanced": 1.00,
        "Growth": 1.22,
    }[scenario]

    data["department"] = data["request_category"].map(department_map).fillna("Operations")
    data["estimated_revenue"] = data["request_category"].map(revenue_map).fillna(100) * scenario_multiplier
    data["estimated_cost"] = data["request_category"].map(cost_map).fillna(88)
    data["estimated_profit"] = data["estimated_revenue"] - data["estimated_cost"]

    return data


def generate_live_rows(number_of_rows):
    now = datetime.now()
    rows = []

    for _ in range(number_of_rows):
        selected_resource = random.choice(list(RESOURCE_MAP.keys()))

        rows.append({
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "ip_address": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "country": random.choice(WEIGHTED_COUNTRIES),
            "request_method": random.choice(["GET", "POST"]),
            "resource": selected_resource,
            "status_code": random.choice([200, 200, 200, 200, 200, 200, 304, 404, 500]),
            "request_category": RESOURCE_MAP[selected_resource],
        })

    return rows


def make_recommendations(roi, standard_rate, error_rate, top_country, top_category, demo_requests, forecast_30d):
    recommendations = []

    if roi < 25:
        recommendations.append((
            "High",
            "Margin protection",
            "Review delivery costs and focus on higher-value service routes."
        ))
    else:
        recommendations.append((
            "Opportunity",
            "Revenue growth",
            f"Increase focus on {top_category} because it is the strongest service signal."
        ))

    if standard_rate < 90:
        recommendations.append((
            "High",
            "Operating reliability",
            "Investigate failed requests and prioritise high-value broken paths."
        ))
    else:
        recommendations.append((
            "Good",
            "Operating reliability",
            "Maintain monitoring and continue reducing error responses."
        ))

    if error_rate > 10:
        recommendations.append((
            "Medium",
            "Error exposure",
            "Review 404 and 500 responses before increasing campaign spend."
        ))

    recommendations.append((
        "Opportunity",
        "Market expansion",
        f"Prioritise marketing and sales follow-up in {top_country}."
    ))

    recommendations.append((
        "Opportunity",
        "Lead conversion",
        "Treat demo requests as warm leads and follow up quickly."
    ))

    if forecast_30d > 0:
        recommendations.append((
            "Opportunity",
            "Revenue forecast",
            "Use the forecast to plan capacity, campaigns and follow-up targets."
        ))

    return recommendations[:4]


def recommendation_html(recommendations):
    level_class = {
        "High": "high",
        "Medium": "medium",
        "Opportunity": "opportunity",
        "Good": "good",
    }

    cards = []
    for level, title, action in recommendations:
        css_class = level_class.get(level, "opportunity")
        cards.append(
            f'<div class="mini-ai-card">'
            f'<div class="mini-ai-pill {css_class}">{level}</div>'
            f'<div class="mini-ai-title">{title}</div>'
            f'<div class="mini-ai-action">{action}</div>'
            f'</div>'
        )

    return '<div class="mini-ai-wrap">' + ''.join(cards) + '</div>'




def create_arc(start_lat, start_lon, end_lat, end_lon, curve=1.3, points=30):
    t = np.linspace(0, 1, points)
    lat = start_lat + (end_lat - start_lat) * t
    lon = start_lon + (end_lon - start_lon) * t
    lon = lon + np.sin(np.pi * t) * curve
    return lat, lon


def market_action(row):
    if row["roi"] >= 35 and row["demo_leads"] >= 100:
        return "Scale campaign"
    if row["demo_leads"] >= 80:
        return "Follow up leads"
    if row["share"] >= 20:
        return "Protect market"
    return "Monitor growth"


# =======================================================
# LOAD DATA + LIVE RECORDS
# =======================================================
base_df = load_data()

if "live_rows" not in st.session_state:
    st.session_state.live_rows = []

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

st.session_state.live_rows.extend(generate_live_rows(random.randint(2, 6)))
st.session_state.live_rows = st.session_state.live_rows[-250:]
st.session_state.last_update = datetime.now()

if st.session_state.live_rows:
    live_df = pd.DataFrame(st.session_state.live_rows)
    df = pd.concat([base_df, live_df], ignore_index=True)
else:
    df = base_df.copy()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"]).copy()
df["date_time"] = pd.to_datetime(df["date"].dt.strftime("%Y-%m-%d") + " " + df["time"], errors="coerce")
df = df.dropna(subset=["date_time"]).copy()
df["hour"] = df["date_time"].dt.hour
df["day_name"] = df["date_time"].dt.day_name()
df = add_service_categories(df)


# =======================================================
# HEADER
# =======================================================
last_updated = st.session_state.last_update.strftime("%H:%M:%S")

st.markdown(f"""
<div class="topbar">
    <div>
        <div class="brand-title">Revenue Intelligence Command Centre</div>
        <div class="brand-subtitle">Revenue · ROI · Market Heat · Threat Hotspots · Forecasting · AI Insights</div>
    </div>
    <div class="topbar-right">
        <div class="badge live-badge">LIVE</div>
        <div class="badge">Updated {last_updated}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =======================================================
# CONTROLS
# =======================================================
st.markdown('<div class="control-strip"><div class="strip-title">Controls</div></div>', unsafe_allow_html=True)

full_min_date = df["date"].min().date()
full_max_date = df["date"].max().date()

control_1, control_2, control_3, control_4, control_5 = st.columns(5)

with control_1:
    market_focus = st.selectbox(
        "Market",
        ["All Markets"] + sorted(df["country"].dropna().unique().tolist())
    )

with control_2:
    request_type_focus = st.selectbox(
        "Request Type",
        ["All Request Types"] + [
            item for item in SERVICE_CATEGORY_ORDER
            if item in df["service_category"].dropna().unique().tolist()
        ]
    )

with control_3:
    service_focus = st.selectbox(
        "Service",
        ["All Services"] + sorted(df["request_category"].dropna().unique().tolist()),
        format_func=lambda x: "All Services" if x == "All Services" else format_label(x)
    )

with control_4:
    time_focus = st.selectbox(
        "Period",
        ["Full Period", "Last 30 Days", "First Quarter", "Second Quarter"]
    )

with control_5:
    revenue_scenario = st.selectbox(
        "Scenario",
        ["Conservative", "Balanced", "Growth"],
        index=1
    )

live_refresh = True

if time_focus == "Last 30 Days":
    start_date = full_max_date - timedelta(days=30)
    end_date = full_max_date
elif time_focus == "First Quarter":
    start_date = datetime(2026, 1, 1).date()
    end_date = datetime(2026, 3, 31).date()
elif time_focus == "Second Quarter":
    start_date = datetime(2026, 4, 1).date()
    end_date = full_max_date
else:
    start_date = full_min_date
    end_date = full_max_date

df = add_business_values(df, revenue_scenario)

filtered_df = df[
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
].copy()

if market_focus != "All Markets":
    filtered_df = filtered_df[filtered_df["country"] == market_focus].copy()

if request_type_focus != "All Request Types":
    filtered_df = filtered_df[filtered_df["service_category"] == request_type_focus].copy()

if service_focus != "All Services":
    filtered_df = filtered_df[filtered_df["request_category"] == service_focus].copy()

if filtered_df.empty:
    st.warning("No data matches the selected controls.")
    st.stop()


# =======================================================
# CALCULATIONS
# =======================================================
total_requests = len(filtered_df)
total_revenue = filtered_df["estimated_revenue"].sum()
total_cost = filtered_df["estimated_cost"].sum()
gross_profit = filtered_df["estimated_profit"].sum()
roi = round((gross_profit / total_cost) * 100, 1) if total_cost > 0 else 0

country_counts = filtered_df["country"].value_counts()
category_counts = filtered_df["request_category"].value_counts()
status_counts = filtered_df["status_code"].value_counts().sort_index()

demo_df = filtered_df[filtered_df["request_category"] == "schedule_demo"]
assistant_df = filtered_df[filtered_df["request_category"] == "ai_virtual_assistant"]
job_df = filtered_df[filtered_df["request_category"] == "job_request"]

demo_by_country = demo_df["country"].value_counts()
job_by_country = job_df["country"].value_counts()

demo_requests = int((filtered_df["request_category"] == "schedule_demo").sum())
assistant_requests = int((filtered_df["request_category"] == "ai_virtual_assistant").sum())
job_requests = int((filtered_df["request_category"] == "job_request").sum())
estimated_conversions = int(demo_requests * 0.22)

standard_count = int(filtered_df["status_code"].isin([200, 304]).sum())
standard_rate = round((standard_count / total_requests) * 100, 1)

error_count = int(filtered_df["status_code"].isin([404, 500]).sum())
error_rate = round((error_count / total_requests) * 100, 1)
count_404 = int((filtered_df["status_code"] == 404).sum())
count_500 = int((filtered_df["status_code"] == 500).sum())

top_country = country_counts.idxmax()
top_country_share = round((country_counts.max() / total_requests) * 100, 1)

top_category_raw = category_counts.idxmax()
top_category = format_label(top_category_raw)
top_category_share = round((category_counts.max() / total_requests) * 100, 1)

service_family_counts = filtered_df["service_category"].value_counts()
top_request_type = service_family_counts.idxmax()
top_request_type_share = round((service_family_counts.max() / total_requests) * 100, 1)

last_data_time = filtered_df["date_time"].max()
data_age_seconds = max(0, int((datetime.now() - last_data_time).total_seconds())) if pd.notna(last_data_time) else 0
refresh_status = "Current" if data_age_seconds <= 120 else "Delayed"

avg_revenue_per_request = total_revenue / total_requests if total_requests else 0
revenue_at_risk = error_count * avg_revenue_per_request
revenue_at_risk_pct = round((revenue_at_risk / total_revenue) * 100, 1) if total_revenue > 0 else 0

threat_score = min(100, round(error_rate * 2.2 + (count_500 / total_requests * 100) * 2.7, 1))

sales_df = filtered_df[filtered_df["department"] == "Sales"]
sales_revenue = sales_df["estimated_revenue"].sum()
sales_cost = sales_df["estimated_cost"].sum()
sales_profit = sales_df["estimated_profit"].sum()
sales_roi = round((sales_profit / sales_cost) * 100, 1) if sales_cost > 0 else 0

revenue_daily = filtered_df.groupby(filtered_df["date"].dt.date).agg(
    revenue=("estimated_revenue", "sum")
).reset_index()
revenue_daily.columns = ["date", "revenue"]

if len(revenue_daily) >= 5:
    x_values = np.arange(len(revenue_daily))
    coefficients = np.polyfit(x_values, revenue_daily["revenue"].values, 1)
    model = np.poly1d(coefficients)
    future_x = np.arange(len(revenue_daily), len(revenue_daily) + 30)
    future_dates = [revenue_daily["date"].max() + timedelta(days=i + 1) for i in range(30)]
    future_revenue = np.maximum(model(future_x), 0)
    forecast_30d = future_revenue.sum()
    trend_pct = round((coefficients[0] / revenue_daily["revenue"].mean()) * 100, 1) if revenue_daily["revenue"].mean() > 0 else 0
else:
    future_dates = []
    future_revenue = np.array([])
    forecast_30d = 0
    trend_pct = 0


# =======================================================
# KPI STRIP
# =======================================================
k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)

with k1:
    st.markdown(metric_card("Revenue", format_money(total_revenue), f"{total_requests:,} interactions", C_BLUE), unsafe_allow_html=True)

with k2:
    st.markdown(metric_card("ROI", f"{roi}%", f"Profit {format_money(gross_profit)}", C_CYAN), unsafe_allow_html=True)

with k3:
    st.markdown(metric_card("Sales", format_money(sales_revenue), f"ROI {sales_roi}%", C_PINK), unsafe_allow_html=True)

with k4:
    st.markdown(metric_card("Risk Value", format_money(revenue_at_risk), f"{revenue_at_risk_pct}% exposure", C_RED), unsafe_allow_html=True)

with k5:
    st.markdown(metric_card("Threat", f"{threat_score}/100", "Composite score", C_ORANGE), unsafe_allow_html=True)

with k6:
    st.markdown(metric_card("Standard", f"{standard_rate}%", "200 and 304", C_GREEN), unsafe_allow_html=True)

with k7:
    st.markdown(metric_card("Demo Leads", f"{demo_requests:,}", f"{estimated_conversions} conversions", C_PURPLE), unsafe_allow_html=True)

with k8:
    st.markdown(metric_card("Forecast", format_money(forecast_30d), f"{trend_pct:+.1f}%/day", C_CYAN), unsafe_allow_html=True)


# =======================================================
# SIGNAL + AI STRATEGIC INSIGHTS
# =======================================================
st.markdown(
    f"""
    <div class="signal-strip">
        <b>Signal:</b> {format_money(total_revenue)} revenue · 
        <b>ROI:</b> {roi}% · 
        <b>Top market:</b> {top_country} · 
        <b>Top request type:</b> {top_request_type} · 
        <b>Top service:</b> {top_category} · 
        <b>Standard rate:</b> {standard_rate}% · 
        <b>Risk value:</b> {format_money(revenue_at_risk)} · 
        <b>30-day forecast:</b> {format_money(forecast_30d)}
    </div>
    """,
    unsafe_allow_html=True
)

recommendations = make_recommendations(
    roi=roi,
    standard_rate=standard_rate,
    error_rate=error_rate,
    top_country=top_country,
    top_category=top_category,
    demo_requests=demo_requests,
    forecast_30d=forecast_30d
)

st.markdown(recommendation_html(recommendations), unsafe_allow_html=True)



# =======================================================
# TABS
# =======================================================
tab_exec, tab_revenue, tab_marketing, tab_sales, tab_ops = st.tabs([
    "Executive",
    "Revenue",
    "Marketing",
    "Sales",
    "Operations",
])


# =======================================================
# EXECUTIVE TAB
# =======================================================
with tab_exec:
    map_df = filtered_df.groupby("country", as_index=False).agg(
        revenue=("estimated_revenue", "sum"),
        requests=("ip_address", "count"),
        errors=("status_code", lambda x: x.isin([404, 500]).sum())
    )

    map_df["lat"] = map_df["country"].map(lambda x: COUNTRY_COORDS.get(x, (0, 0))[0])
    map_df["lon"] = map_df["country"].map(lambda x: COUNTRY_COORDS.get(x, (0, 0))[1])

    revenue_max = max(float(map_df["revenue"].max()), 1.0)
    error_max = max(float(map_df["errors"].max()), 1.0)

    map_df["revenue_norm"] = map_df["revenue"] / revenue_max
    map_df["error_norm"] = map_df["errors"] / error_max
    map_df["bubble_size"] = map_df["revenue_norm"] * 38 + 14

    executive_left, executive_middle, executive_right = st.columns([1.42, 0.82, 0.96])

    with executive_left:
        fig_map = go.Figure()

        fig_map.add_trace(go.Scattermapbox(
            lat=map_df["lat"],
            lon=map_df["lon"],
            mode="markers",
            marker=dict(
                size=map_df["bubble_size"] * 5.5,
                color=map_df["revenue"],
                colorscale=[
                    [0, "rgba(34,211,238,0.06)"],
                    [0.55, "rgba(139,92,246,0.11)"],
                    [1, "rgba(245,158,11,0.16)"]
                ],
                opacity=0.85,
                sizemode="diameter",
                showscale=False
            ),
            hoverinfo="skip",
            showlegend=False
        ))

        threat_df = map_df[map_df["errors"] > 0].copy()

        if not threat_df.empty:
            fig_map.add_trace(go.Scattermapbox(
                lat=threat_df["lat"],
                lon=threat_df["lon"],
                mode="markers",
                marker=dict(
                    size=threat_df["error_norm"] * 34 + 18,
                    color=C_RED,
                    opacity=0.18,
                    sizemode="diameter",
                    showscale=False
                ),
                hoverinfo="skip",
                showlegend=False
            ))

        hub_lat, hub_lon = COUNTRY_COORDS["Botswana"]

        for _, row in map_df.iterrows():
            if row["country"] == "Botswana":
                continue

            arc_lat, arc_lon = create_arc(hub_lat, hub_lon, row["lat"], row["lon"])

            fig_map.add_trace(go.Scattermapbox(
                lat=arc_lat,
                lon=arc_lon,
                mode="lines",
                line=dict(
                    width=max(0.8, row["revenue_norm"] * 2.6),
                    color=f"rgba(34,211,238,{max(0.14, row['revenue_norm'] * 0.55):.2f})"
                ),
                hoverinfo="skip",
                showlegend=False
            ))

        fig_map.add_trace(go.Scattermapbox(
            lat=map_df["lat"],
            lon=map_df["lon"],
            mode="markers",
            marker=dict(
                size=map_df["bubble_size"] * 1.65,
                color=C_CYAN,
                opacity=0.30,
                sizemode="diameter",
                showscale=False
            ),
            hoverinfo="skip",
            showlegend=False
        ))

        fig_map.add_trace(go.Scattermapbox(
            lat=map_df["lat"],
            lon=map_df["lon"],
            mode="markers+text",
            marker=dict(
                size=map_df["bubble_size"],
                color=map_df["revenue"],
                colorscale=[
                    [0, C_CYAN],
                    [0.45, C_PURPLE],
                    [0.8, C_PINK],
                    [1, C_ORANGE]
                ],
                opacity=0.96,
                sizemode="diameter",
                showscale=True,
                colorbar=dict(
                    title="Revenue",
                    thickness=8,
                    len=0.62,
                    x=1.01,
                    bgcolor="rgba(5,11,24,0.65)",
                    tickfont=dict(color="#9CB1D4", size=8),
                ),
            ),
            text=map_df["country"],
            textposition="top center",
            textfont=dict(color="#F8FAFC", size=9),
            customdata=map_df[["requests", "revenue", "errors"]],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Revenue: BWP %{customdata[1]:,.0f}<br>"
                "Requests: %{customdata[0]:,}<br>"
                "Errors: %{customdata[2]}<extra></extra>"
            ),
            showlegend=False
        ))

        fig_map.update_layout(
            title="Southern Africa Revenue and Threat Map",
            height=360,
            mapbox=dict(
                style="carto-darkmatter",
                center=dict(lat=-22.5, lon=26.5),
                zoom=3.65,
            ),
            paper_bgcolor="#050B18",
            plot_bgcolor="#050B18",
            font=dict(color="#E8F0FF", family=FONT, size=10),
            margin=dict(l=0, r=0, t=38, b=0),
        )

        st.plotly_chart(fig_map, use_container_width=True, config=CHART_CONFIG)

    with executive_middle:
        fig_roi = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=roi,
            delta={"reference": 25, "valueformat": ".1f"},
            title={"text": "Portfolio ROI"},
            number={"suffix": "%", "font": {"size": 27}},
            gauge={
                "axis": {"range": [0, max(120, roi + 20)]},
                "bar": {"color": C_CYAN, "thickness": 0.22},
                "bgcolor": PAPER,
                "steps": [
                    {"range": [0, 25], "color": "#2A1320"},
                    {"range": [25, 60], "color": "#14233C"},
                    {"range": [60, max(120, roi + 20)], "color": "#0F3028"},
                ],
                "threshold": {"line": {"color": C_ORANGE, "width": 2}, "value": 25},
            },
        ))

        fig_roi.update_layout(
            height=360,
            paper_bgcolor=PAPER,
            font=dict(color="#E8F0FF", family=FONT),
            margin=dict(l=10, r=10, t=38, b=10),
        )

        st.plotly_chart(fig_roi, use_container_width=True, config=CHART_CONFIG)

    with executive_right:
        department_df = filtered_df.groupby("department", as_index=False).agg(
            revenue=("estimated_revenue", "sum"),
            profit=("estimated_profit", "sum"),
        ).sort_values("revenue", ascending=True)

        fig_department = go.Figure()

        fig_department.add_trace(go.Bar(
            x=department_df["revenue"],
            y=department_df["department"],
            orientation="h",
            name="Revenue",
            marker=dict(color=C_PURPLE, opacity=0.78, line=dict(width=0)),
        ))

        fig_department.add_trace(go.Bar(
            x=department_df["profit"],
            y=department_df["department"],
            orientation="h",
            name="Profit",
            marker=dict(color=C_GREEN, opacity=0.82, line=dict(width=0)),
        ))

        fig_department.update_layout(**chart_layout("Department Revenue vs Profit", height=360))
        fig_department.update_xaxes(title="")
        fig_department.update_yaxes(title="", showgrid=False)

        st.plotly_chart(fig_department, use_container_width=True, config=CHART_CONFIG)

    exec2a, exec2b, exec2c, exec2d = st.columns(4)

    with exec2a:
        rank_df = map_df.sort_values("revenue", ascending=True).copy()

        fig_rank = go.Figure(go.Bar(
            x=rank_df["revenue"],
            y=rank_df["country"],
            orientation="h",
            marker=dict(
                color=rank_df["revenue"],
                colorscale=[[0, C_BLUE], [0.5, C_CYAN], [1, C_GREEN]],
                line=dict(width=0)
            ),
            text=[format_money(v) for v in rank_df["revenue"]],
            textposition="inside"
        ))

        fig_rank.update_layout(**chart_layout("Market Revenue Ranking", height=230, show_legend=False))
        fig_rank.update_xaxes(title="")
        fig_rank.update_yaxes(title="", showgrid=False)

        st.plotly_chart(fig_rank, use_container_width=True, config=CHART_CONFIG)

    with exec2b:
        hourly_df = filtered_df.groupby("hour", as_index=False).agg(
            requests=("ip_address", "count"),
            revenue=("estimated_revenue", "sum")
        )

        fig_hourly = go.Figure()

        fig_hourly.add_trace(go.Bar(
            x=hourly_df["hour"],
            y=hourly_df["requests"],
            name="Requests",
            marker=dict(color=C_PURPLE, opacity=0.8, line=dict(width=0))
        ))

        fig_hourly.add_trace(go.Scatter(
            x=hourly_df["hour"],
            y=hourly_df["revenue"] / 1000,
            name="Revenue (K)",
            mode="lines+markers",
            line=dict(color=C_CYAN, width=2),
            marker=dict(size=5)
        ))

        fig_hourly.update_layout(**chart_layout("Hourly Demand Pattern", height=230))
        fig_hourly.update_xaxes(title="")
        fig_hourly.update_yaxes(title="")

        st.plotly_chart(fig_hourly, use_container_width=True, config=CHART_CONFIG)

    with exec2c:
        risk_country = filtered_df.groupby("country", as_index=False).agg(
            total=("ip_address", "count"),
            errors=("status_code", lambda x: x.isin([404, 500]).sum())
        )

        risk_country["error_rate"] = (risk_country["errors"] / risk_country["total"] * 100).round(1)
        risk_country = risk_country.sort_values("error_rate", ascending=False)

        fig_risk = go.Figure(go.Bar(
            x=risk_country["country"],
            y=risk_country["error_rate"],
            marker=dict(
                color=risk_country["error_rate"],
                colorscale=[[0, C_GREEN], [0.5, C_ORANGE], [1, C_RED]],
                line=dict(width=0)
            ),
            text=[f"{v}%" for v in risk_country["error_rate"]],
            textposition="outside"
        ))

        fig_risk.update_layout(**chart_layout("Market Error Exposure", height=230, show_legend=False))
        fig_risk.update_xaxes(title="", tickangle=-18)
        fig_risk.update_yaxes(title="Error %")

        st.plotly_chart(fig_risk, use_container_width=True, config=CHART_CONFIG)

    with exec2d:
        request_type_df = filtered_df.groupby("service_category", as_index=False).agg(
            requests=("ip_address", "count"),
            revenue=("estimated_revenue", "sum"),
        )

        request_type_df["service_category"] = pd.Categorical(
            request_type_df["service_category"],
            categories=SERVICE_CATEGORY_ORDER,
            ordered=True
        )
        request_type_df = request_type_df.sort_values("service_category")

        fig_request_type = go.Figure(go.Bar(
            x=request_type_df["requests"],
            y=request_type_df["service_category"].astype(str),
            orientation="h",
            marker=dict(
                color=request_type_df["revenue"],
                colorscale=[[0, C_BLUE], [0.45, C_CYAN], [0.8, C_PURPLE], [1, C_ORANGE]],
                line=dict(width=0)
            ),
            text=[f"{int(v):,}" for v in request_type_df["requests"]],
            textposition="inside"
        ))

        fig_request_type.update_layout(**chart_layout("Demand by Service Category", height=230, show_legend=False))
        fig_request_type.update_xaxes(title="Requests")
        fig_request_type.update_yaxes(title="", showgrid=False)

        st.plotly_chart(fig_request_type, use_container_width=True, config=CHART_CONFIG)


# =======================================================
# REVENUE TAB
# =======================================================
with tab_revenue:
    revenue_col_1, revenue_col_2, revenue_col_3 = st.columns([1, 1.1, 0.9])

    category_finance = filtered_df.groupby(["service_category", "request_category"], as_index=False).agg(
        revenue=("estimated_revenue", "sum"),
        cost=("estimated_cost", "sum"),
        requests=("ip_address", "count"),
    )

    category_finance["profit"] = category_finance["revenue"] - category_finance["cost"]
    category_finance["roi"] = (category_finance["profit"] / category_finance["cost"] * 100).round(1)
    category_finance["service"] = category_finance["request_category"].apply(format_label)

    with revenue_col_1:
        fig_service = go.Figure(go.Bar(
            x=category_finance["service"],
            y=category_finance["revenue"],
            marker=dict(
                color=category_finance["roi"],
                colorscale=[[0, C_RED], [0.5, C_ORANGE], [0.75, C_CYAN], [1, C_GREEN]],
                line=dict(width=0)
            ),
            text=[f"{value}%" for value in category_finance["roi"]],
            textposition="inside",
        ))

        fig_service.update_layout(**chart_layout("Revenue by Service", height=285, show_legend=False))
        fig_service.update_xaxes(title="", tickangle=-18)
        fig_service.update_yaxes(title="BWP")

        st.plotly_chart(fig_service, use_container_width=True, config=CHART_CONFIG)

    with revenue_col_2:
        fig_forecast = go.Figure()

        revenue_daily["ma7"] = revenue_daily["revenue"].rolling(7, min_periods=1).mean()

        fig_forecast.add_trace(go.Scatter(
            x=revenue_daily["date"],
            y=revenue_daily["revenue"],
            mode="lines",
            name="Daily",
            line=dict(color=C_BLUE, width=1.5),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.07)",
        ))

        fig_forecast.add_trace(go.Scatter(
            x=revenue_daily["date"],
            y=revenue_daily["ma7"],
            mode="lines",
            name="7-day average",
            line=dict(color=C_CYAN, width=2.2, dash="dot"),
        ))

        if len(future_dates) > 0:
            fig_forecast.add_trace(go.Scatter(
                x=future_dates,
                y=future_revenue,
                mode="lines",
                name="Forecast",
                line=dict(color=C_PINK, width=2.2, dash="dash"),
                fill="tozeroy",
                fillcolor="rgba(236,72,153,0.06)",
            ))

        fig_forecast.update_layout(**chart_layout("Revenue Forecast", height=285))
        fig_forecast.update_xaxes(title="")
        fig_forecast.update_yaxes(title="BWP")

        st.plotly_chart(fig_forecast, use_container_width=True, config=CHART_CONFIG)

    with revenue_col_3:
        fig_funnel = go.Figure(go.Funnel(
            y=["Traffic", "AI Use", "Demo Leads", "Conversions"],
            x=[total_requests, assistant_requests, demo_requests, estimated_conversions],
            textinfo="value+percent initial",
            marker=dict(color=[C_BLUE, C_CYAN, C_ORANGE, C_GREEN]),
        ))

        fig_funnel.update_layout(
            title="Lead Funnel",
            height=285,
            paper_bgcolor=PAPER,
            plot_bgcolor=PAPER,
            font=dict(color="#E8F0FF", family=FONT, size=10),
            margin=dict(l=10, r=10, t=38, b=10),
        )

        st.plotly_chart(fig_funnel, use_container_width=True, config=CHART_CONFIG)

    st.markdown('<div class="section-label">Revenue Table</div>', unsafe_allow_html=True)

    revenue_table = category_finance[["service_category", "service", "requests", "revenue", "cost", "profit", "roi"]].rename(columns={
        "service_category": "Service Category",
        "service": "Service",
        "requests": "Requests",
        "revenue": "Revenue",
        "cost": "Cost",
        "profit": "Profit",
        "roi": "ROI (%)",
    }).sort_values("Revenue", ascending=False)

    st.dataframe(revenue_table, use_container_width=True, hide_index=True)


# =======================================================
# MARKETING TAB
# =======================================================
with tab_marketing:
    market_df = filtered_df.groupby("country", as_index=False).agg(
        requests=("ip_address", "count"),
        revenue=("estimated_revenue", "sum"),
        cost=("estimated_cost", "sum"),
    )

    market_df["profit"] = market_df["revenue"] - market_df["cost"]
    market_df["roi"] = (market_df["profit"] / market_df["cost"] * 100).round(1)
    market_df["share"] = (market_df["requests"] / total_requests * 100).round(1)
    market_df["demo_leads"] = market_df["country"].map(demo_by_country).fillna(0).astype(int)
    market_df["job_requests"] = market_df["country"].map(job_by_country).fillna(0).astype(int)

    marketing_col_1, marketing_col_2, marketing_col_3 = st.columns(3)

    with marketing_col_1:
        fig_market_roi = px.scatter(
            market_df,
            x="requests",
            y="roi",
            size="revenue",
            color="country",
            text="country",
            color_discrete_sequence=[C_BLUE, C_CYAN, C_ORANGE, C_GREEN, C_PURPLE, C_PINK, C_RED],
            size_max=46,
        )

        fig_market_roi.update_traces(
            textposition="top center",
            marker=dict(opacity=0.82, line=dict(width=0))
        )

        fig_market_roi.update_layout(**chart_layout("Market Size vs ROI", height=260, show_legend=False))
        fig_market_roi.update_xaxes(title="Requests")
        fig_market_roi.update_yaxes(title="ROI %")

        st.plotly_chart(fig_market_roi, use_container_width=True, config=CHART_CONFIG)

    with marketing_col_2:
        mix_df = filtered_df.groupby(["country", "request_category"], as_index=False).agg(
            revenue=("estimated_revenue", "sum")
        )

        mix_df["service"] = mix_df["request_category"].apply(format_label)

        fig_mix = px.bar(
            mix_df,
            x="country",
            y="revenue",
            color="service",
            color_discrete_sequence=[C_BLUE, C_CYAN, C_ORANGE, C_GREEN, C_PURPLE, C_PINK],
        )

        fig_mix.update_layout(**chart_layout("Revenue Mix by Market", height=260))
        fig_mix.update_xaxes(title="", tickangle=-18)
        fig_mix.update_yaxes(title="BWP")

        st.plotly_chart(fig_mix, use_container_width=True, config=CHART_CONFIG)

    with marketing_col_3:
        fig_leads = go.Figure()

        fig_leads.add_trace(go.Bar(
            name="Demo Leads",
            x=market_df["country"],
            y=market_df["demo_leads"],
            marker=dict(color=C_PINK, opacity=0.85, line=dict(width=0)),
        ))

        fig_leads.add_trace(go.Bar(
            name="Job Requests",
            x=market_df["country"],
            y=market_df["job_requests"],
            marker=dict(color=C_ORANGE, opacity=0.85, line=dict(width=0)),
        ))

        fig_leads.update_layout(**chart_layout("Leads by Market", height=260))
        fig_leads.update_xaxes(title="", tickangle=-18)
        fig_leads.update_yaxes(title="Count")

        st.plotly_chart(fig_leads, use_container_width=True, config=CHART_CONFIG)

    m2a, m2b, m2c = st.columns(3)

    with m2a:
        conv_df = market_df.copy()
        conv_df["expected_conversions"] = (conv_df["demo_leads"] * 0.22).round().astype(int)

        fig_conv = go.Figure()

        fig_conv.add_trace(go.Bar(
            x=conv_df["country"],
            y=conv_df["demo_leads"],
            name="Demo Leads",
            marker=dict(color=C_ORANGE, opacity=0.85, line=dict(width=0))
        ))

        fig_conv.add_trace(go.Bar(
            x=conv_df["country"],
            y=conv_df["expected_conversions"],
            name="Expected Conversions",
            marker=dict(color=C_GREEN, opacity=0.85, line=dict(width=0))
        ))

        fig_conv.update_layout(**chart_layout("Lead Conversion by Market", height=240))
        fig_conv.update_xaxes(title="", tickangle=-18)
        fig_conv.update_yaxes(title="Count")

        st.plotly_chart(fig_conv, use_container_width=True, config=CHART_CONFIG)

    with m2b:
        top_markets = market_df.sort_values("revenue", ascending=False)["country"].head(4).tolist()

        trend_markets = filtered_df[filtered_df["country"].isin(top_markets)].copy()
        trend_markets["month"] = trend_markets["date"].dt.to_period("M").astype(str)

        trend_markets = trend_markets.groupby(["month", "country"], as_index=False).agg(
            revenue=("estimated_revenue", "sum")
        )

        fig_trend = px.line(
            trend_markets,
            x="month",
            y="revenue",
            color="country",
            markers=True,
            color_discrete_sequence=[C_CYAN, C_BLUE, C_PURPLE, C_GREEN]
        )

        fig_trend.update_layout(**chart_layout("Top Market Revenue Trend", height=240))
        fig_trend.update_xaxes(title="")
        fig_trend.update_yaxes(title="BWP")

        st.plotly_chart(fig_trend, use_container_width=True, config=CHART_CONFIG)

    with m2c:
        heat_df = filtered_df.pivot_table(
            index="country",
            columns="request_category",
            values="ip_address",
            aggfunc="count",
            fill_value=0
        )

        fig_heat = go.Figure(data=go.Heatmap(
            z=heat_df.values,
            x=[format_label(c) for c in heat_df.columns],
            y=heat_df.index,
            colorscale=[
                [0, "#0B1B34"],
                [0.25, "#12345F"],
                [0.5, "#1D4ED8"],
                [0.75, "#22D3EE"],
                [1, "#10B981"]
            ],
            showscale=True
        ))

        fig_heat.update_layout(
            title="Service Demand Heatmap",
            height=240,
            paper_bgcolor=PAPER,
            plot_bgcolor=PAPER,
            font=dict(color="#E8F0FF", family=FONT, size=10),
            margin=dict(l=20, r=10, t=38, b=20),
        )

        st.plotly_chart(fig_heat, use_container_width=True, config=CHART_CONFIG)

    market_df["action"] = market_df.apply(market_action, axis=1)

    market_table = market_df.rename(columns={
        "country": "Market",
        "requests": "Requests",
        "share": "Share (%)",
        "revenue": "Revenue",
        "roi": "ROI (%)",
        "demo_leads": "Demo Leads",
        "job_requests": "Job Requests",
        "action": "Recommended Action",
    })[
        ["Market", "Requests", "Share (%)", "Revenue", "ROI (%)", "Demo Leads", "Job Requests", "Recommended Action"]
    ].sort_values("Revenue", ascending=False)

    st.dataframe(market_table, use_container_width=True, hide_index=True)


# =======================================================
# SALES TAB
# =======================================================
with tab_sales:
    sales_k1, sales_k2, sales_k3, sales_k4 = st.columns(4)

    with sales_k1:
        st.markdown(metric_card("Sales Revenue", format_money(sales_revenue), "Demo + job demand", C_BLUE), unsafe_allow_html=True)

    with sales_k2:
        st.markdown(metric_card("Sales ROI", f"{sales_roi}%", f"Profit {format_money(sales_profit)}", C_CYAN), unsafe_allow_html=True)

    with sales_k3:
        st.markdown(metric_card("Demo Leads", f"{demo_requests:,}", f"{estimated_conversions} expected", C_ORANGE), unsafe_allow_html=True)

    with sales_k4:
        st.markdown(metric_card("Job Requests", f"{job_requests:,}", "Service demand", C_PURPLE), unsafe_allow_html=True)

    sales_col_1, sales_col_2, sales_col_3 = st.columns(3)

    with sales_col_1:
        demo_trend = demo_df.groupby(demo_df["date"].dt.date).size().reset_index(name="leads")
        demo_trend["ma7"] = demo_trend["leads"].rolling(7, min_periods=1).mean()

        fig_demo = go.Figure()

        fig_demo.add_trace(go.Bar(
            x=demo_trend["date"],
            y=demo_trend["leads"],
            name="Daily",
            marker=dict(color=C_ORANGE, opacity=0.72, line=dict(width=0))
        ))

        fig_demo.add_trace(go.Scatter(
            x=demo_trend["date"],
            y=demo_trend["ma7"],
            name="7-day avg",
            mode="lines",
            line=dict(color=C_CYAN, width=2.1)
        ))

        fig_demo.update_layout(**chart_layout("Demo Lead Trend", height=250))
        fig_demo.update_xaxes(title="")
        fig_demo.update_yaxes(title="Leads")

        st.plotly_chart(fig_demo, use_container_width=True, config=CHART_CONFIG)

    with sales_col_2:
        job_trend = job_df.groupby(job_df["date"].dt.date).size().reset_index(name="jobs")
        job_trend["ma7"] = job_trend["jobs"].rolling(7, min_periods=1).mean()

        fig_jobs = go.Figure()

        fig_jobs.add_trace(go.Bar(
            x=job_trend["date"],
            y=job_trend["jobs"],
            name="Daily",
            marker=dict(color=C_PURPLE, opacity=0.72, line=dict(width=0))
        ))

        fig_jobs.add_trace(go.Scatter(
            x=job_trend["date"],
            y=job_trend["ma7"],
            name="7-day avg",
            mode="lines",
            line=dict(color=C_GREEN, width=2.1)
        ))

        fig_jobs.update_layout(**chart_layout("Job Request Trend", height=250))
        fig_jobs.update_xaxes(title="")
        fig_jobs.update_yaxes(title="Requests")

        st.plotly_chart(fig_jobs, use_container_width=True, config=CHART_CONFIG)

    with sales_col_3:
        fig_sales_funnel = go.Figure(go.Funnel(
            y=["Visitors", "Demo Leads", "Conversions", "Repeat"],
            x=[total_requests, demo_requests, estimated_conversions, int(estimated_conversions * 0.35)],
            textinfo="value+percent initial",
            marker=dict(color=[C_BLUE, C_ORANGE, C_GREEN, C_PURPLE]),
        ))

        fig_sales_funnel.update_layout(
            title="Sales Funnel",
            height=250,
            paper_bgcolor=PAPER,
            plot_bgcolor=PAPER,
            font=dict(color="#E8F0FF", family=FONT, size=10),
            margin=dict(l=10, r=10, t=38, b=10),
        )

        st.plotly_chart(fig_sales_funnel, use_container_width=True, config=CHART_CONFIG)

    sales_market = filtered_df.groupby("country", as_index=False).agg(
        demo_leads=("request_category", lambda x: (x == "schedule_demo").sum()),
        job_requests=("request_category", lambda x: (x == "job_request").sum()),
        revenue=("estimated_revenue", "sum")
    )

    sales_market["expected_conversions"] = (sales_market["demo_leads"] * 0.22).round().astype(int)

    s2a, s2b, s2c = st.columns(3)

    with s2a:
        fig_sales_market = go.Figure()

        fig_sales_market.add_trace(go.Bar(
            x=sales_market["country"],
            y=sales_market["demo_leads"],
            name="Demo Leads",
            marker=dict(color=C_ORANGE, opacity=0.82, line=dict(width=0))
        ))

        fig_sales_market.add_trace(go.Bar(
            x=sales_market["country"],
            y=sales_market["expected_conversions"],
            name="Expected Conversions",
            marker=dict(color=C_GREEN, opacity=0.82, line=dict(width=0))
        ))

        fig_sales_market.update_layout(**chart_layout("Lead Conversion by Market", height=240))
        fig_sales_market.update_xaxes(title="", tickangle=-18)
        fig_sales_market.update_yaxes(title="Count")

        st.plotly_chart(fig_sales_market, use_container_width=True, config=CHART_CONFIG)

    with s2b:
        sales_market_sorted = sales_market.sort_values("revenue", ascending=False)

        fig_sales_rev = go.Figure(go.Bar(
            x=sales_market_sorted["country"],
            y=sales_market_sorted["revenue"],
            marker=dict(
                color=sales_market_sorted["revenue"],
                colorscale=[[0, C_BLUE], [0.5, C_CYAN], [1, C_GREEN]],
                line=dict(width=0)
            ),
            text=[format_money(v) for v in sales_market_sorted["revenue"]],
            textposition="outside"
        ))

        fig_sales_rev.update_layout(**chart_layout("Sales Revenue by Market", height=240, show_legend=False))
        fig_sales_rev.update_xaxes(title="", tickangle=-18)
        fig_sales_rev.update_yaxes(title="BWP")

        st.plotly_chart(fig_sales_rev, use_container_width=True, config=CHART_CONFIG)

    with s2c:
        fig_balance = go.Figure()

        fig_balance.add_trace(go.Bar(
            x=sales_market["country"],
            y=sales_market["job_requests"],
            name="Job Requests",
            marker=dict(color=C_PURPLE, opacity=0.82, line=dict(width=0))
        ))

        fig_balance.add_trace(go.Bar(
            x=sales_market["country"],
            y=sales_market["demo_leads"],
            name="Demo Leads",
            marker=dict(color=C_CYAN, opacity=0.82, line=dict(width=0))
        ))

        fig_balance.update_layout(**chart_layout("Demand Balance by Market", height=240))
        fig_balance.update_xaxes(title="", tickangle=-18)
        fig_balance.update_yaxes(title="Count")

        st.plotly_chart(fig_balance, use_container_width=True, config=CHART_CONFIG)


# =======================================================
# OPERATIONS TAB
# =======================================================
with tab_ops:
    ops_col_1, ops_col_2, ops_col_3 = st.columns([0.85, 1, 1.15])

    with ops_col_1:
        fig_standard = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=standard_rate,
            delta={"reference": 95, "valueformat": ".1f"},
            title={"text": "Operating Standard"},
            number={"suffix": "%", "font": {"size": 26}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": C_GREEN if standard_rate >= 90 else C_ORANGE, "thickness": 0.22},
                "bgcolor": PAPER,
                "steps": [
                    {"range": [0, 70], "color": "#2A1320"},
                    {"range": [70, 90], "color": "#2A2614"},
                    {"range": [90, 100], "color": "#102A24"},
                ],
                "threshold": {"line": {"color": C_CYAN, "width": 2}, "value": 95},
            },
        ))

        fig_standard.update_layout(
            height=285,
            paper_bgcolor=PAPER,
            font=dict(color="#E8F0FF", family=FONT),
            margin=dict(l=10, r=10, t=38, b=10),
        )

        st.plotly_chart(fig_standard, use_container_width=True, config=CHART_CONFIG)

    with ops_col_2:
        status_colours = []

        for code in status_counts.index:
            if code == 200:
                status_colours.append(C_GREEN)
            elif code == 304:
                status_colours.append(C_BLUE)
            elif code == 404:
                status_colours.append(C_ORANGE)
            elif code == 500:
                status_colours.append(C_RED)
            else:
                status_colours.append("#94A3B8")

        fig_status = go.Figure(go.Pie(
            labels=[str(code) for code in status_counts.index],
            values=status_counts.values,
            hole=0.68,
            marker=dict(colors=status_colours, line=dict(color=PAPER, width=2)),
            textinfo="label+percent",
        ))

        fig_status.add_annotation(
            text=f"<b>{standard_rate}%</b><br>OK",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color=C_GREEN, size=15)
        )

        fig_status.update_layout(
            title="Status Code Distribution",
            height=285,
            paper_bgcolor=PAPER,
            plot_bgcolor=PAPER,
            font=dict(color="#E8F0FF", family=FONT, size=10),
            margin=dict(l=10, r=10, t=38, b=10),
            legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
        )

        st.plotly_chart(fig_status, use_container_width=True, config=CHART_CONFIG)

    with ops_col_3:
        action_queue = pd.DataFrame({
            "Area": ["Broken links", "Server errors", "Lead follow-up", "Revenue review"],
            "Trigger": [
                f"{count_404} page-not-found responses",
                f"{count_500} server-error responses",
                f"{demo_requests} demo leads",
                f"{roi}% ROI",
            ],
            "Priority": [
                "Medium" if count_404 > 0 else "Low",
                "High" if count_500 > 0 else "Low",
                "High" if demo_requests > 0 else "Low",
                "Review" if roi < 25 else "Normal",
            ],
            "Action": [
                "Audit missing pages",
                "Investigate server logs",
                "CRM follow-up",
                "Review pricing strategy",
            ],
        })

        st.markdown('<div class="section-label">Operating Action Queue</div>', unsafe_allow_html=True)
        st.dataframe(action_queue, use_container_width=True, hide_index=True)

    filtered_df["is_error"] = filtered_df["status_code"].isin([404, 500]).astype(int)

    error_timeline = filtered_df.groupby(filtered_df["date_time"].dt.floor("h")).agg(
        errors=("is_error", "sum"),
        total=("ip_address", "count")
    ).reset_index()

    error_timeline["error_rate"] = (error_timeline["errors"] / error_timeline["total"].clip(lower=1) * 100).round(1)

    fig_error = go.Figure()

    fig_error.add_trace(go.Scatter(
        x=error_timeline["date_time"],
        y=error_timeline["error_rate"],
        mode="lines",
        name="Error rate",
        line=dict(color=C_RED, width=1.8),
        fill="tozeroy",
        fillcolor="rgba(239,68,68,0.07)",
    ))

    fig_error.add_hline(y=error_rate, line_dash="dot", line_color=C_ORANGE, line_width=1)

    fig_error.update_layout(**chart_layout("Hourly Error Rate", height=225))
    fig_error.update_xaxes(title="")
    fig_error.update_yaxes(title="Error %")

    st.plotly_chart(fig_error, use_container_width=True, config=CHART_CONFIG)


# =======================================================
# DOWNLOAD REPORT
# =======================================================
summary_df = pd.DataFrame({
    "metric": [
        "market_focus",
        "request_type_focus",
        "service_focus",
        "time_focus",
        "revenue_scenario",
        "total_requests",
        "estimated_revenue",
        "estimated_cost",
        "estimated_profit",
        "roi_percent",
        "top_market",
        "top_market_share",
        "top_request_type",
        "top_request_type_share",
        "top_service",
        "top_service_share",
        "standard_rate",
        "error_rate",
        "demo_leads",
        "estimated_conversions",
        "revenue_at_risk",
        "threat_score",
        "forecast_30d",
        "refresh_seconds",
        "privacy_mode",
        "records_processed",
    ],
    "value": [
        market_focus,
        request_type_focus,
        service_focus,
        time_focus,
        revenue_scenario,
        total_requests,
        round(total_revenue, 2),
        round(total_cost, 2),
        round(gross_profit, 2),
        roi,
        top_country,
        top_country_share,
        top_request_type,
        top_request_type_share,
        top_category,
        top_category_share,
        standard_rate,
        error_rate,
        demo_requests,
        estimated_conversions,
        round(revenue_at_risk, 2),
        threat_score,
        round(forecast_30d, 2),
        AUTO_REFRESH_SECONDS,
        "SHA-256 anonymised customer IDs",
        len(df),
    ]
})

csv_data = summary_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Revenue Intelligence Report",
    data=csv_data,
    file_name="revenue_intelligence_report.csv",
    mime="text/csv"
)


# =======================================================
# AUTO LIVE REFRESH
# =======================================================
time.sleep(AUTO_REFRESH_SECONDS)
st.rerun()