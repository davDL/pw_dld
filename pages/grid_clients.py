import pandas as pd
import dash
import common_utils
from dash import html, Output, Input, callback
import dash_bootstrap_components as dbc
from common_components import text_table_cell, text_table_cell_header, table_action_button

dash.register_page(__name__)
client_data = pd.read_csv("assets/lavoratori.csv", sep = ';')

page_size = 50

def client_table_row(row, row_index, actions):
    return html.Tr([
        text_table_cell(row_index),
        text_table_cell(row.get("Contact Id")),
        text_table_cell(row.get("Phone Display Name")),
        #html.Td(actions)
    ], style={'height': '51px', 'width': '50px'})

def generate_table_rows_from_dataframe(dataset, actions):
    table_row_list = []
    for index, row in dataset.iterrows():
        table_row_list.append(client_table_row(row, actions))
    return table_row_list

def get_table_clients (dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header("Id"),
                text_table_cell_header("Contact Id"),
                text_table_cell_header("Phone Display Name"),
                #text_table_cell_header("Azioni")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    actions = dbc.Container([
        table_action_button(dash.get_asset_url('ic_edit_table.png'), "success", '#4fc971'),
        table_action_button(dash.get_asset_url('ic_cancel_table.png'), "danger", '#fe534d')
    ])

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(client_table_row(row, index, actions))
        counter += 1


    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table

@callback(
    Output('clients-table-detail', 'children'),
    Input('clients-pagination-detail', 'active_page'),
)
def update_list_scores(page):
    # convert active_page data to integer and set default value to 1
    int_page = 1 if not page else int(page)

    # define filter index range based on active page
    filter_index_1 = (int_page - 1) * page_size
    filter_index_2 = int_page * page_size

    # get data by filter range based on active page number
    filtered_clients = client_data[filter_index_1:filter_index_2]

    # load data to dash bootstrap table component
    table = get_table_clients(filtered_clients, (filter_index_1 + 1))

    return table


content = dbc.Container([
        html.Div([
            html.H5(["Elenco degli clienti"], style={'color': '#365185', 'margin-top':'32px'}),
            # html.Div([
            #     dbc.Container([
            #         html.Img(src=add_icon, style={'width': '15px', 'height': '15px'})
            #     ], style={'background-color': '#365185', 'width': '30px', 'height': '31px', 'border-top-left-radius': '20px', 'border-bottom-left-radius': '20px', 'display': 'flex','justify-content': 'center', 'align-items': 'center'}),
            #     dbc.Container([
            #         "Aggiungi agente"
            #     ], style={'color': '#ffffff', 'background-color': '#365185', 'height': '31px', 'border-top-right-radius': '20px', 'border-bottom-right-radius': '20px', 'text-align': 'center', 'padding-top': '2px'})
            # ], style={'background-color': 'white', 'display': 'flex', 'flex-direction': 'row', 'align-self': 'flex-start', 'border-radius': '20px', 'border': '0.3mm solid #dee2e6'})
        ]),
        dbc.Table(id='clients-table-detail', style={'width':'1270px', 'margin':'16px'}),
        dbc.Pagination(id='clients-pagination-detail', max_value=common_utils.get_total_page(page_size, client_data.shape[0]), previous_next=True, fully_expanded=False, style={'padding-right':'20px', 'padding-bottom': '20px', 'align-self': 'flex-end'}),
    ], style={'display': 'flex', 'flex-direction': 'column'})

layout = html.Div([
    html.Div([
        content
    ]),
], className='side', style={'justify-content': 'space-between'})