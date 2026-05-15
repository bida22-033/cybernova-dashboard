# CyberNova Analytics Dashboard Prototype

## Project Overview

This project is a Business Intelligence and Data Analytics prototype developed for CyberNova Analytics Ltd. The prototype analyses web interaction and system activity data to help stakeholders understand customer engagement, request categories, service demand, regional activity and platform performance.

The solution is built as an interactive Streamlit dashboard. It uses a generated CSV web log dataset and presents the results through KPI cards, charts, maps, filters, summary tables and action-focused insights.

## Purpose of the Prototype

The purpose of the prototype is to demonstrate how web interaction data can be transformed into meaningful dashboard outputs for non-technical stakeholders. The dashboard supports decision-making by showing:

- customer interaction activity
- different request types
- service demand patterns
- regional engagement
- platform response behaviour
- operational and business support indicators

Revenue and ROI values are included only as supporting business indicators. They are based on assumptions in the simulated dataset and do not represent actual company financial performance.

## Project Files

| File or Folder | Description |
|---|---|
| `app.py` | Main Streamlit dashboard application |
| `generate_web_logs.py` | Script used to generate the web log dataset |
| `requirements.txt` | List of Python packages required to run the dashboard |
| `data/web_logs.csv` | Generated CSV dataset used by the dashboard |
| `README.md` | Project information and running instructions |

## Technologies Used

The prototype was developed using:

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- OpenPyXL
- CSV data storage

## Installation Instructions

First, open the project folder in Visual Studio Code.

Then open the terminal in the project directory and install the required packages:

```powershell
py -m pip install -r requirements.txt
