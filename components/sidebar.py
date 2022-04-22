from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app


# =========  Layout  =========== #
layout = html.Div(
    [
        html.H2("ASIMOV", style={'font-family': 'Voltaire', 'font-size': '80px'}),
        html.Hr(), 
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Component 1", href="/", active="exact"),
                dbc.NavLink("Component 2", href="/comp2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ], style={"background-color": "#f8f9fa", "height": "100vh"}
)