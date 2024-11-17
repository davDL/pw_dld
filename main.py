import dash
from dash import Dash, html, Output, Input
import dash_bootstrap_components as dbc
from common_components import sidebar_header_element_dashboard, sidebar_header_element_config, sidebar_collapse_element

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

server = app.server


@app.callback(
    Output("collapse1", "is_open"),
    Output("arrow_image", "src"),
    Input("collapse-button", "n_clicks")
)
def toggle_collapse1(n):
    if n is None:
        return False, app.get_asset_url('ic_arrow_right_black.png')
    else:
        return not n % 2, app.get_asset_url('ic_arrow_right_black.png') if n % 2 else app.get_asset_url('ic_arrow_down_black.png')

sideBar = html.Div([
    html.Div([
        sidebar_header_element_dashboard(app.get_asset_url('ic_dashboard.png'), app.get_asset_url('ic_arrow_right_black.png')),
        dbc.Collapse(
            html.Div([
                sidebar_collapse_element('HOME', app.get_asset_url('ic_no_fill_dot.png'), dash.page_registry['pages.dashboard']['path']),
                sidebar_collapse_element('AGENTI', app.get_asset_url('ic_no_fill_dot.png'), dash.page_registry['pages.grid_agents']['path']),
                sidebar_collapse_element('CLIENTI', app.get_asset_url('ic_no_fill_dot.png'), dash.page_registry['pages.grid_clients']['path']),
                sidebar_collapse_element('CONVERSAZIONI', app.get_asset_url('ic_no_fill_dot.png'), dash.page_registry['pages.grid_conversations']['path']),
                sidebar_collapse_element('SONDAGGI', app.get_asset_url('ic_no_fill_dot.png'), dash.page_registry['pages.grid_surveys']['path'])
            ], style={'padding-left': '32px'}),
            id="collapse1",
            is_open=True,
        ),
    ], style={'padding-bottom': '8px'}),
], className='menu')

app.layout = html.Div([
    html.Div([
        sideBar,
        html.Div([
            dash.page_container
        ])
    ], style={'background-color':'#f5f6f8', 'display':'flex', 'flex-direction':'row', 'justify-content': 'center'})
])

if __name__ == '__main__':
    app.run(debug=True)
