import dash
import dash_bootstrap_components as dbc

VALID_USERNAME_PASSWORD_PAIRS = {
    'asimov': 'academy'
}

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP] + [FONT_AWESOME])
# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.scripts.config.serve_locally = True
server = app.server