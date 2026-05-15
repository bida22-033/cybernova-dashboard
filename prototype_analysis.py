from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Create output folder if it does not already exist
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

# Define the dataset file path
data_file = Path("data/web_logs.csv")

# Load the dataset
df = pd.read_csv(data_file)

# Basic checks
print("\nFIRST 5 ROWS OF THE DATASET")
print(df.head())

print("\nDATASET INFORMATION")
print(df.info())

print("\nMISSING VALUES")
print(df.isnull().sum())

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# Create a full datetime column
df["date_time"] = pd.to_datetime(
    df["date"].dt.strftime("%Y-%m-%d") + " " + df["time"],
    errors="coerce"
)

# Core summaries
country_counts = df["country"].value_counts()
category_counts = df["request_category"].value_counts()
status_counts = df["status_code"].value_counts()
daily_counts = df.groupby(df["date"].dt.date).size()

demo_df = df[df["request_category"] == "schedule_demo"]
demo_by_country = demo_df["country"].value_counts()

assistant_df = df[df["request_category"] == "ai_virtual_assistant"]
assistant_by_country = assistant_df["country"].value_counts()

job_requests = (df["request_category"] == "job_request").sum()
demo_requests = (df["request_category"] == "schedule_demo").sum()
promo_requests = (df["request_category"] == "promotional_event").sum()
assistant_requests = (df["request_category"] == "ai_virtual_assistant").sum()

requests_per_day = df.groupby(df["date"].dt.date).size()
mean_requests = requests_per_day.mean()
std_requests = requests_per_day.std()
max_requests = requests_per_day.max()
min_requests = requests_per_day.min()

total_requests = len(df)
top_country = country_counts.idxmax()
top_category = category_counts.idxmax()
success_rate = round((df["status_code"] == 200).mean() * 100, 1)

print("\nKEY SUMMARY COUNTS")
print(f"Total requests: {total_requests}")
print(f"Top country: {top_country}")
print(f"Top category: {top_category}")
print(f"Success rate (200): {success_rate}%")
print(f"Job requests: {job_requests}")
print(f"Schedule demo requests: {demo_requests}")
print(f"Promotional event requests: {promo_requests}")
print(f"AI virtual assistant requests: {assistant_requests}")
print(f"Mean requests per day: {mean_requests:.2f}")
print(f"Standard deviation of requests per day: {std_requests:.2f}")
print(f"Maximum requests in one day: {max_requests}")
print(f"Minimum requests in one day: {min_requests}")

# Save summary tables
country_counts.to_csv(output_folder / "country_summary.csv", header=["count"])
category_counts.to_csv(output_folder / "category_summary.csv", header=["count"])
status_counts.to_csv(output_folder / "status_code_summary.csv", header=["count"])
daily_counts.to_csv(output_folder / "daily_request_summary.csv", header=["count"])

summary_report = pd.DataFrame({
    "metric": [
        "total_requests",
        "top_country",
        "top_category",
        "success_rate_200_percent",
        "job_requests",
        "schedule_demo_requests",
        "promotional_event_requests",
        "ai_virtual_assistant_requests",
        "mean_requests_per_day",
        "std_requests_per_day",
        "max_requests_in_one_day",
        "min_requests_in_one_day"
    ],
    "value": [
        total_requests,
        top_country,
        top_category,
        success_rate,
        job_requests,
        demo_requests,
        promo_requests,
        assistant_requests,
        round(mean_requests, 2),
        round(std_requests, 2),
        max_requests,
        min_requests
    ]
})
summary_report.to_csv(output_folder / "summary_report.csv", index=False)

# Build comparison table for one chart
comparison_df = pd.DataFrame({
    "Schedule Demo": demo_by_country,
    "AI Assistant": assistant_by_country
}).fillna(0)

# Create dashboard layout
fig = plt.figure(figsize=(18, 11))
gs = fig.add_gridspec(3, 4, height_ratios=[0.9, 2.2, 2.2])

fig.suptitle("CyberNova Web Log Analytics Dashboard", fontsize=20, fontweight="bold")

# KPI boxes
kpi_axes = [
    fig.add_subplot(gs[0, 0]),
    fig.add_subplot(gs[0, 1]),
    fig.add_subplot(gs[0, 2]),
    fig.add_subplot(gs[0, 3])
]

kpi_data = [
    ("Total Requests", str(total_requests)),
    ("Top Country", top_country),
    ("Top Category", top_category),
    ("Success Rate", f"{success_rate}%")
]

for ax, (title, value) in zip(kpi_axes, kpi_data):
    ax.axis("off")
    ax.text(
        0.5, 0.65, value,
        ha="center", va="center",
        fontsize=20, fontweight="bold"
    )
    ax.text(
        0.5, 0.25, title,
        ha="center", va="center",
        fontsize=11
    )
    ax.add_patch(
        plt.Rectangle(
            (0.05, 0.05), 0.9, 0.9,
            fill=False,
            transform=ax.transAxes,
            linewidth=1.5
        )
    )

# Chart 1: Requests by country
ax1 = fig.add_subplot(gs[1, 0:2])
country_counts.plot(kind="bar", ax=ax1)
ax1.set_title("Requests by Country", fontsize=13, fontweight="bold")
ax1.set_xlabel("Country")
ax1.set_ylabel("Number of Requests")
ax1.tick_params(axis="x", rotation=35)

# Chart 2: Requests by category
ax2 = fig.add_subplot(gs[1, 2:4])
category_counts.plot(kind="bar", ax=ax2)
ax2.set_title("Requests by Category", fontsize=13, fontweight="bold")
ax2.set_xlabel("Request Category")
ax2.set_ylabel("Number of Requests")
ax2.tick_params(axis="x", rotation=35)

# Chart 3: Daily request trend
ax3 = fig.add_subplot(gs[2, 0:2])
daily_counts.plot(kind="line", marker="o", ax=ax3)
ax3.set_title("Daily Request Trend", fontsize=13, fontweight="bold")
ax3.set_xlabel("Date")
ax3.set_ylabel("Number of Requests")
ax3.tick_params(axis="x", rotation=35)

# Chart 4: Demo vs AI assistant by country
ax4 = fig.add_subplot(gs[2, 2])
comparison_df.plot(kind="bar", ax=ax4)
ax4.set_title("Demo vs AI Assistant", fontsize=13, fontweight="bold")
ax4.set_xlabel("Country")
ax4.set_ylabel("Requests")
ax4.tick_params(axis="x", rotation=35)

# Chart 5: Status code distribution
ax5 = fig.add_subplot(gs[2, 3])
status_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax5)
ax5.set_title("Status Code Distribution", fontsize=13, fontweight="bold")
ax5.set_ylabel("")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(output_folder / "distinction_dashboard.png", dpi=300)
plt.show()

print("\nDashboard complete.")
print("Saved as outputs/distinction_dashboard.png")