# Cloud Cost & Performance Dashboard

A Dash-based dashboard for monitoring and optimizing cloud infrastructure costs.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python app.py
```

Then open http://localhost:8050 in your browser.

## Features

- **KPI Cards**: Current cost, predicted cost, potential savings, and efficiency score
- **Cost by Service**: Donut chart showing cost breakdown (EC2, RDS, S3, etc.)
- **Cost by Project**: Horizontal bar chart of project costs
- **Optimization Actions**: Table with recommended cost-saving actions
- **Cost vs Performance**: Dual-axis chart tracking costs and API response times

## Docker

Build and run with Docker:

```bash
docker build -t cloud-cost-dashboard .
docker run -p 8050:8050 cloud-cost-dashboard
```

## Tech Stack

- Dash 4.0+
- Dash Bootstrap Components
- Plotly
- Pandas
