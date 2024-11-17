import pandas as pd
import dash
import common_utils
from dash import html, Output, Input, callback
import dash_bootstrap_components as dbc
from common_components import text_table_cell, text_table_cell_header, table_text_action_button, text_table_cell_header_mid, text_table_cell_mid

dash.register_page(__name__)
data = pd.read_csv("assets/lavoratori.csv", sep = ';')

page_size = 50

def conversations_table_row(row, actions):
    return html.Tr([
        text_table_cell_mid(row.get("talkdesk_phone_display_name")),
        text_table_cell(row.get("callsid")),
        text_table_cell(row.get("type")),
        text_table_cell(row.get("start_at").split('T')[0]),
        text_table_cell(row.get("total_time")),
        text_table_cell(row.get("start_at")),
        text_table_cell(row.get("end_at")),
        text_table_cell(row.get("user_name")),
        text_table_cell(row.get("wait_time")),
        #html.Td(actions)
    ], style={'height': '51px', 'width': '50px'})

def generate_table_rows_from_dataframe(dataset, actions):
    table_row_list = []
    for index, row in dataset.iterrows():
        table_row_list.append(conversations_table_row(row, actions))
    return table_row_list

def get_table_conversations (dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header_mid("Nome azienda"),
                text_table_cell_header("Id chiamata"),
                text_table_cell_header("Tipologia"),
                text_table_cell_header("Data"),
                text_table_cell_header("Durata"),
                text_table_cell_header("Inizio alle"),
                text_table_cell_header("Fine alle"),
                text_table_cell_header("Utente"),
                text_table_cell_header("Tempi attesa"),
                #text_table_cell_header("Azioni")
            ], style={'height': '51px', 'width': '50px'})
        )
    ]

    actions = dbc.Container([
        table_text_action_button("Sondaggio", "#627cea"),
    ])

    table_rows = []
    for index, row in dataset.iterrows():
        table_rows.append(conversations_table_row(row, actions))
        counter += 1


    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)

    return table


# create callback
@callback(
    Output('conversations-table-detail', 'children'),
    Input('conversations-pagination-detail', 'active_page'),
)
def update_list_scores(page):
    # convert active_page data to integer and set default value to 1
    int_page = 1 if not page else int(page)

    # define filter index range based on active page
    filter_index_1 = (int_page - 1) * page_size
    filter_index_2 = int_page * page_size

    # get data by filter range based on active page number
    filter_conversations = data[filter_index_1:filter_index_2]

    # load data to dash bootstrap table component
    table = get_table_conversations(filter_conversations, (filter_index_1 + 1))

    return table

content = dbc.Container([
    html.Div([
        html.H5(["Conversazioni"], style={'color': '#365185', 'margin-top':'32px'}),
        # html.Div([
        #     dbc.Input(size="sm", placeholder="Search...", type="text", style={'border': '0', 'border-radius': '20px'}),
        #     dbc.Container([
        #         html.Img(src=dash.get_asset_url('ic_search.png'), style={'width': '15px', 'height': '15px'})
        #     ], style={'background-color': '#365185', 'width': '30px', 'height': '31px',
        #               'border-top-right-radius': '20px', 'border-bottom-right-radius': '20px', 'display': 'flex',
        #               'justify-content': 'center', 'align-items': 'center'})
        # ], style={'background-color': 'white', 'display': 'flex', 'flex-direction': 'row', 'align-self': 'flex-end', 'border-radius': '20px', 'border': '0.3mm solid #dee2e6'})
    ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-bottom': '8px'}),
    dbc.Table(id='conversations-table-detail', style={'width':'1270px', 'margin':'16px'}),
    dbc.Pagination(id='conversations-pagination-detail', max_value=common_utils.get_total_page(page_size, data.shape[0]), previous_next=True, fully_expanded=False, style={'padding-right': '20px', 'padding-bottom': '20px', 'align-self': 'flex-end'})
], style={'display': 'flex', 'flex-direction': 'column'})

layout = html.Div([
    html.Div([
        content
    ]),
], className='side', style={'justify-content': 'space-between'})