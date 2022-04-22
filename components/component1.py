from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import *


# =========  Layout  =========== #
import calendar
    
yy = 2022
mm = 3

# display the calendar
calendar = calendar.month(yy, mm)

layout = dbc.Container([
            dbc.Row([
                html.Div(children=calendar)
        ]) 
    ]) 