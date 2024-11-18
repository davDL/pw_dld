import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

server = app.server

app.layout = html.Div([
    html.Div([
        dash.page_container,
    ], style={'background-color':'#f5f6f8', 'display':'flex', 'flex-direction':'row', 'justify-content': 'center'})
])

if __name__ == '__main__':
    app.run(debug=True)
