"""Cloud Cost Optimization Dashboard - Main Application."""
import dash
import dash_bootstrap_components as dbc
from layout import create_layout

# Initialize Dash app with dark Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "Cloud Cost & Performance Dashboard"

# Set the layout
app.layout = create_layout()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
