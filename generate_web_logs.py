import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# This file creates a test web server log dataset for the CyberNova dashboard.
# It saves the generated data into data/web_logs.csv.


# -------------------------------------------------------
# 1. Create the data folder
# -------------------------------------------------------
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

output_file = data_folder / "web_logs.csv"


# -------------------------------------------------------
# 2. Configuration
# -------------------------------------------------------
number_of_records = 5000
start_date = datetime(2026, 1, 1)
number_of_days = 181


countries = [
    "Botswana",
    "South Africa",
    "Namibia",
    "Zimbabwe",
    "Zambia",
    "Lesotho",
    "Mozambique",
    "Eswatini"
]


# These pages represent different types of customer activity.
resource_map = {
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
    "/cyber-risk-report.html": "general_service"
}


request_methods = ["GET", "POST"]


# 200 appears more often because most normal web requests should be successful.
status_codes = [200, 200, 200, 200, 200, 200, 200, 304, 404, 500]


# -------------------------------------------------------
# 3. Helper functions
# -------------------------------------------------------
def generate_ip_address():
    """
    Creates a random IP address.
    """
    return ".".join(str(random.randint(1, 255)) for _ in range(4))


def choose_country():
    """
    Gives some countries more records so the dashboard has realistic patterns.
    """
    weighted_countries = (
        ["Botswana"] * 35 +
        ["South Africa"] * 30 +
        ["Namibia"] * 10 +
        ["Zimbabwe"] * 10 +
        ["Zambia"] * 6 +
        ["Lesotho"] * 3 +
        ["Mozambique"] * 3 +
        ["Eswatini"] * 3
    )

    return random.choice(weighted_countries)


def choose_resource(day_offset):
    """
    Chooses a resource page.
    AI assistant and schedule demo requests become more common over time.
    """
    base_resources = [
        "/index.html",
        "/services.html",
        "/jobs.html",
        "/apply-job.php",
        "/event.php",
        "/promo.html",
        "/contact.html",
        "/webinar.html",
        "/cyber-risk-report.html"
    ]

    trending_resources = (
        ["/assistant.php"] * (5 + day_offset // 25) +
        ["/scheduledemo.php"] * (4 + day_offset // 30)
    )

    all_resources = base_resources + trending_resources
    return random.choice(all_resources)


# -------------------------------------------------------
# 4. Generate and save the dataset
# -------------------------------------------------------
print("Generating CyberNova web log dataset...")

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "date",
        "time",
        "ip_address",
        "country",
        "request_method",
        "resource",
        "status_code",
        "request_category"
    ])

    for record_number in range(number_of_records):
        day_offset = random.randint(0, number_of_days - 1)
        current_date = start_date + timedelta(days=day_offset)

        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        log_datetime = current_date.replace(
            hour=random_hour,
            minute=random_minute,
            second=random_second
        )

        resource = choose_resource(day_offset)
        request_category = resource_map[resource]

        writer.writerow([
            log_datetime.strftime("%Y-%m-%d"),
            log_datetime.strftime("%H:%M:%S"),
            generate_ip_address(),
            choose_country(),
            random.choice(request_methods),
            resource,
            random.choice(status_codes),
            request_category
        ])

print(f"Dataset created successfully: {output_file}")
print(f"Total records created: {number_of_records}")