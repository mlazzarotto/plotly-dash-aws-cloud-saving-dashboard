"""Dashboard layout definition."""
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data import KPI_DATA, COST_BY_SERVICE, COST_BY_PROJECT, OPTIMIZATION_ACTIONS, DAILY_DATA

# Accent colors - brighter palette
ACCENT_COLOR = "#ff7940"
ACCENT_GREEN = "#3ddc84"
TEXT_PRIMARY = "#e6edf3"
TEXT_MUTED = "#a0aec0"
BG_PAGE = "#111827"
BG_CARD = "#1e2433"
BORDER_COLOR = "#2e3a52"
GRID_COLOR = "rgba(255,255,255,0.06)"

def create_kpi_card(title, value, subtitle, is_positive=False, is_highlight=False, icon=None):
    """Create a KPI card component."""
    # Brighter styling with top accent border
    top_border = f"2px solid {ACCENT_COLOR}" if not is_highlight else f"2px solid {ACCENT_GREEN}"
    border_style = f"1px solid {BORDER_COLOR}"
    bg_style = BG_CARD
    
    # Green glow for savings card
    box_shadow = "0 0 25px rgba(61, 220, 132, 0.15)" if is_highlight else "none"
    
    value_color = ACCENT_GREEN if is_positive else (ACCENT_COLOR if is_highlight else TEXT_PRIMARY)
    
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="card-title text-muted mb-2", 
                   style={"color": TEXT_MUTED, "letterSpacing": "0.5px", "fontSize": "13px", "textTransform": "uppercase"}),
            html.H2(value, className="card-text mb-2", style={"color": value_color, "fontWeight": "700", "fontSize": "32px"}),
            html.Small(subtitle, style={"color": TEXT_MUTED, "fontSize": "12px"})
        ]),
        style={
            "backgroundColor": bg_style,
            "border": border_style,
            "borderTop": top_border,
            "borderRadius": "12px",
            "height": "100%",
            "boxShadow": box_shadow
        }
    )

def create_donut_chart():
    """Create cost by service donut chart."""
    # Brighter, more vibrant color palette
    colors = [ACCENT_COLOR, "#60b4ff", ACCENT_GREEN, "#a78bfa", "#94a3b8"]
    
    fig = go.Figure(data=[go.Pie(
        labels=COST_BY_SERVICE["Service"],
        values=COST_BY_SERVICE["Cost"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=BG_CARD, width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color=TEXT_PRIMARY),
        hovertemplate="%{label}<br>€%{value:,.0f}<br>(%{percent})<extra></extra>"
    )])
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[dict(
            text="<b>Cost<br>by Service</b>",
            x=0.5, y=0.5,
            font=dict(size=14, color=TEXT_PRIMARY),
            showarrow=False
        )],
        height=300
    )
    
    return fig

def create_bar_chart():
    """Create cost by project horizontal bar chart."""
    df = pd.DataFrame(COST_BY_PROJECT)
    
    fig = px.bar(
        df,
        y="Project",
        x="Cost",
        orientation="h",
        text="Cost",
        color_discrete_sequence=[ACCENT_COLOR]
    )
    
    fig.update_traces(
        texttemplate="€%{x:,.0f}",
        textposition="outside",
        textfont=dict(color=TEXT_PRIMARY),
        marker=dict(line=dict(color=BG_CARD, width=1))
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=40, l=80, r=40),
        xaxis=dict(
            title=dict(text="Cost (€)", font=dict(color=TEXT_MUTED)),
            color=TEXT_MUTED,
            showgrid=True,
            gridcolor=GRID_COLOR,
            gridwidth=1
        ),
        yaxis=dict(
            title="",
            color=TEXT_PRIMARY,
            showgrid=False
        ),
        showlegend=False,
        height=280
    )
    
    return fig

def create_optimization_table():
    """Create optimization actions table with enhanced styling."""
    columns = [
        {"name": "Azione", "id": "action"},
        {"name": "Problema", "id": "problem"},
        {"name": "Soluzione", "id": "solution"},
        {"name": "Risparmio (€/mese)", "id": "savings", "type": "numeric"}
    ]
    
    return dash_table.DataTable(
        id="optimization-table",
        columns=columns,
        data=OPTIMIZATION_ACTIONS,
        style_table={
            "overflowX": "auto",
            "backgroundColor": "transparent",
            "borderRadius": "8px"
        },
        style_header={
            "backgroundColor": "#252d3d",
            "color": ACCENT_COLOR,
            "fontWeight": "bold",
            "border": f"1px solid {BORDER_COLOR}",
            "textAlign": "left",
            "padding": "14px",
            "fontSize": "13px"
        },
        style_cell={
            "backgroundColor": "transparent",
            "color": TEXT_PRIMARY,
            "border": f"1px solid {BORDER_COLOR}",
            "textAlign": "left",
            "padding": "14px",
            "fontSize": "13px"
        },
        style_data={
            "backgroundColor": BG_CARD
        },
        style_data_conditional=[
            # Alternating row colors
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#1a2030"
            },
            # Green savings column
            {
                "if": {"column_id": "savings"},
                "color": ACCENT_GREEN,
                "fontWeight": "bold"
            }
        ],
        page_size=5
    )

def create_dual_axis_chart():
    """Create dual-axis line chart for cost vs API response time."""
    fig = go.Figure()
    
    # Cost line (left axis) - brighter orange
    fig.add_trace(go.Scatter(
        x=DAILY_DATA["date"],
        y=DAILY_DATA["cost"],
        name="Daily Cost (€)",
        line=dict(color=ACCENT_COLOR, width=3),
        mode="lines+markers",
        marker=dict(size=6, color=ACCENT_COLOR, line=dict(color=BG_CARD, width=2)),
        hovertemplate="Date: %{x}<br>Cost: €%{y:,.0f}<extra></extra>"
    ))
    
    # API response time line (right axis) - brighter blue
    fig.add_trace(go.Scatter(
        x=DAILY_DATA["date"],
        y=DAILY_DATA["api_response_time"],
        name="API Response (ms)",
        line=dict(color="#60b4ff", width=3, dash="dot"),
        mode="lines",
        yaxis="y2",
        hovertemplate="Date: %{x}<br>Response: %{y:.0f} ms<extra></extra>"
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=40, l=60, r=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
            font=dict(color=TEXT_MUTED, size=12),
            bgcolor="rgba(30, 36, 51, 0.8)",
            bordercolor=BORDER_COLOR,
            borderwidth=1
        ),
        xaxis=dict(
            color=TEXT_MUTED,
            showgrid=True,
            gridcolor=GRID_COLOR,
            gridwidth=1,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Daily Cost (€)", font=dict(color=ACCENT_COLOR)),
            color=ACCENT_COLOR,
            showgrid=False,
            zeroline=False,
            tickfont=dict(color=ACCENT_COLOR)
        ),
        yaxis2=dict(
            title=dict(text="API Response Time (ms)", font=dict(color="#60b4ff")),
            color="#60b4ff",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#60b4ff")
        ),
        height=320,
        hovermode="x unified"
    )
    
    return fig

def create_card_style():
    """Return standard card styling with top accent border."""
    return {
        "backgroundColor": BG_CARD,
        "border": f"1px solid {BORDER_COLOR}",
        "borderTop": f"2px solid {ACCENT_COLOR}",
        "borderRadius": "12px"
    }

def create_layout():
    """Create the full dashboard layout with polished, bright styling."""
    return dbc.Container([
        # Header Row with bottom border
        dbc.Row([
            dbc.Col([
                html.H1([
                    html.Span("Cloud Cost", style={"color": ACCENT_COLOR}),
                    html.Span(" & Performance Dashboard", style={"color": "#ffffff"})
                ], style={"fontWeight": "700", "marginBottom": "0", "fontSize": "32px"}),
                html.P("Monitor and optimize your cloud infrastructure costs", 
                      style={"color": TEXT_MUTED, "marginTop": "8px", "fontSize": "15px", "letterSpacing": "0.3px"})
            ], md=6),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Label("Period", style={"color": TEXT_MUTED, "fontSize": "12px", "fontWeight": "500", "marginBottom": "4px"}),
                        dcc.DatePickerRange(
                            id="date-range",
                            start_date=(DAILY_DATA["date"].min()).strftime("%Y-%m-%d"),
                            end_date=(DAILY_DATA["date"].max()).strftime("%Y-%m-%d"),
                            display_format="DD/MM/YYYY",
                            className="dash-datepicker"
                        )
                    ], width=6),
                    dbc.Col([
                        html.Label("Environment", style={"color": TEXT_MUTED, "fontSize": "12px", "fontWeight": "500", "marginBottom": "4px"}),
                        dcc.Dropdown(
                            id="environment-dropdown",
                            options=[
                                {"label": "All Environments", "value": "all"},
                                {"label": "Production", "value": "prod"},
                                {"label": "Staging", "value": "staging"},
                                {"label": "Development", "value": "dev"}
                            ],
                            value="all",
                            className="dash-dropdown",
                            style={"backgroundColor": "#252d3d", "color": TEXT_PRIMARY, "borderRadius": "8px"}
                        )
                    ], width=6)
                ])
            ], md=6, className="d-flex align-items-center justify-content-end")
        ], className="mb-4 mt-4 pb-4", style={"borderBottom": f"1px solid {BORDER_COLOR}"}),
        
        # KPI Row
        dbc.Row([
            dbc.Col([
                create_kpi_card(
                    "Costo Mensile Corrente",
                    f"€ {KPI_DATA['total_cost']:,}",
                    f"+{KPI_DATA['total_cost_change']}% vs mese precedente"
                )
            ], md=3),
            dbc.Col([
                create_kpi_card(
                    "Costo Mensile Previsto",
                    f"€ {KPI_DATA['predicted_cost']:,}",
                    "Basato sul trend attuale"
                )
            ], md=3),
            dbc.Col([
                create_kpi_card(
                    "Risparmio Mensile Potenziale",
                    f"€ {KPI_DATA['potential_savings']:,}",
                    "Azioni di ottimizzazione identificate",
                    is_positive=True,
                    is_highlight=True
                )
            ], md=3),
            dbc.Col([
                create_kpi_card(
                    "Efficiency Score",
                    f"{KPI_DATA['efficiency_score']}%",
                    "Indicatore della salute dell'infrastruttura"
                )
            ], md=3)
        ], className="mb-4 g-3"),
        
        # Main Content Row
        dbc.Row([
            # Left Column - Cost Analysis
            dbc.Col([
                # Donut Chart Card
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Costo per Servizio", style={"color": TEXT_PRIMARY, "marginBottom": "20px", "fontWeight": "600"}),
                        dcc.Graph(figure=create_donut_chart(), config={"displayModeBar": False})
                    ])
                ], style={**create_card_style(), "marginBottom": "20px"}),
                
                # Bar Chart Card
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Costo per Progetto", style={"color": TEXT_PRIMARY, "marginBottom": "20px", "fontWeight": "600"}),
                        dcc.Graph(figure=create_bar_chart(), config={"displayModeBar": False})
                    ])
                ], style=create_card_style())
            ], md=5),
            
            # Right Column - Optimization
            dbc.Col([
                # Optimization Table Card
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Top 5 Quick Wins per il Risparmio", style={"color": TEXT_PRIMARY, "marginBottom": "20px", "fontWeight": "600"}),
                        create_optimization_table()
                    ])
                ], style={**create_card_style(), "marginBottom": "20px"}),
                
                # Dual Axis Chart Card
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Andamento Costi vs Performance", style={"color": TEXT_PRIMARY, "marginBottom": "20px", "fontWeight": "600"}),
                        dcc.Graph(figure=create_dual_axis_chart(), config={"displayModeBar": False})
                    ])
                ], style=create_card_style())
            ], md=7)
        ], className="g-3"),
        
        # Footer
        html.Hr(style={"borderColor": BORDER_COLOR, "marginTop": "40px", "marginBottom": "20px"}),
        html.P("Cloud Cost Optimization Dashboard © 2026 - Powered by Dash & Plotly",
               style={"color": TEXT_MUTED, "textAlign": "center", "fontSize": "12px"})
        
    ], fluid=True, style={"backgroundColor": BG_PAGE, "minHeight": "100vh", "padding": "0 30px"})
