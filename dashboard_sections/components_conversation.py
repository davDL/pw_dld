from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import common_utils
from common_components import text_table_cell, text_table_cell_header, table_text_action_button, text_table_cell_header_mid, text_table_cell_mid

def conversations_table_row(row, actions):
    return html.Tr([
        text_table_cell_mid(row.get("Company Number")),
        text_table_cell(row.get("Contact Id")),
        text_table_cell(row.get("Contact Type")),
        text_table_cell(row.get("Started At").split(' ')[0]),
        text_table_cell(row.get("Talk Time")),
        text_table_cell(row.get("Started At")),
        text_table_cell(row.get("Finished At")),
        text_table_cell(row.get("User Name")),
        text_table_cell(row.get("Wait Time")),
        #html.Td(actions)
    ], style={'height': '51px', 'width': '50px'})

def table_performances_conversations(search_icon, dataset):
    page_size = 5

    # create callback
    @callback(
        Output('conversations-table', 'children'),
        Input('conversations-pagination', 'active_page'),
    )
    def update_list_(page):
        # convert active_page data to integer and set default value to 1
        int_page = 1 if not page else int(page)

        # define filter index range based on active page
        filter_index_1 = (int_page - 1) * page_size
        filter_index_2 = int_page * page_size

        # get data by filter range based on active page number
        filter_conversations = dataset[filter_index_1:filter_index_2]

        # load data to dash bootstrap table component
        table = get_table_conversations(filter_conversations, (filter_index_1 + 1))

        return table

    return dbc.Container([
        html.Div([
            html.H5(["Conversazioni"], style={'color': '#365185'}),
            # html.Div([
            #     dbc.Input(size="sm", placeholder="Search...", type="text",style={'border': '0', 'border-radius': '20px'}),
            #     dbc.Container([
            #         html.Img(src=search_icon, style={'width': '15px', 'height': '15px'})
            #     ], style={'background-color': '#365185', 'width': '30px', 'height': '31px', 'border-top-right-radius': '20px', 'border-bottom-right-radius': '20px', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
            # ], style={'background-color': 'white', 'display': 'flex', 'flex-direction': 'row', 'align-self': 'flex-end', 'border-radius': '20px', 'border': '0.3mm solid #dee2e6'})
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'margin-bottom': '8px'}),
        dbc.Table(id='conversations-table', style={'min-height':'350px'}),
        dbc.Pagination(id = 'conversations-pagination', max_value=common_utils.get_total_page(page_size, dataset.shape[0]), previous_next=True, fully_expanded=False, style={'padding-bottom': '20px', 'align-self':'flex-end'})
    ], style={'display':'flex', 'flex-direction':'column'})

def get_table_conversations (dataset, counter):
    table_header = [
        html.Thead(
            html.Tr([
                text_table_cell_header_mid("Numero azienda"),
                text_table_cell_header("Id contatto"),
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