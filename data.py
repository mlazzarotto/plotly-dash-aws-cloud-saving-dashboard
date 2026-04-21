"""Mock data for Cloud Cost Optimization Dashboard."""
import pandas as pd
from datetime import datetime, timedelta

# KPI Data
KPI_DATA = {
    "total_cost": 12450,
    "total_cost_change": 5.2,
    "predicted_cost": 13100,
    "potential_savings": 3820,
    "efficiency_score": 68
}

# Cost by Service (for donut chart)
COST_BY_SERVICE = {
    "Service": ["EC2", "RDS", "S3", "Lambda", "Other"],
    "Cost": [5602.5, 2490, 1867.5, 1245, 1245],
    "Percentage": [45, 20, 15, 10, 10]
}

# Cost by Project (for horizontal bar chart)
COST_BY_PROJECT = {
    "Project": ["Phoenix", "Bluebird", "Atlas", "Sentinel", "Orion"],
    "Cost": [4500, 3200, 2100, 1800, 850]
}

# Optimization Actions (for table)
OPTIMIZATION_ACTIONS = [
    {
        "action": "Rightsizing EC2: instance-prod-01",
        "problem": "Over-provisioned (80% CPU idle)",
        "solution": "Downgrade from m5.2xlarge to m5.xlarge",
        "savings": 450
    },
    {
        "action": "Delete unused EBS volumes",
        "problem": "15 unattached volumes (>90 days)",
        "solution": "Dismissione volumi non utilizzati",
        "savings": 320
    },
    {
        "action": "Idle RDS instances",
        "problem": "2 istanze db-dev-* con 0 connessioni",
        "solution": "Stop instances during off-hours",
        "savings": 680
    },
    {
        "action": "Reserved Instances conversion",
        "problem": "On-demand EC2 running 24/7",
        "solution": "Convert to 1-year reserved instances",
        "savings": 1250
    },
    {
        "action": "S3 lifecycle optimization",
        "problem": "80% data infrequently accessed",
        "solution": "Move to Glacier after 90 days",
        "savings": 520
    }
]

# Daily time series data (last 30 days)
def generate_daily_data():
    """Generate mock daily cost and API response time data."""
    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    
    # Simulate cost with slight upward trend and weekly patterns
    import random
    random.seed(42)
    base_cost = 380
    daily_costs = []
    daily_api_times = []
    
    for i, date in enumerate(dates):
        # Cost with weekly spike on weekdays
        weekday_factor = 1.2 if date.weekday() < 5 else 0.9
        cost = base_cost + (i * 1.5) + random.uniform(-20, 30)
        daily_costs.append(round(cost * weekday_factor, 2))
        
        # API response time inversely correlated with cost efficiency
        # Lower cost (more optimized) = slightly better performance
        api_time = 120 + random.uniform(-15, 15) - (i * 0.3)
        daily_api_times.append(round(max(80, api_time), 2))
    
    return pd.DataFrame({
        "date": dates,
        "cost": daily_costs,
        "api_response_time": daily_api_times
    })

DAILY_DATA = generate_daily_data()
