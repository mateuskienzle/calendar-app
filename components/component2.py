from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import *


# =========  Layout  =========== #
layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Card header"),
                        dbc.CardBody([
                                html.H5("Card title", className="card-title"),
                                html.P("Component 2",
                                    className="card-text")]
                        )], color="primary", inverse=True)
                ]),
        ]) 
    ]) 